from fastapi import APIRouter, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import json
from config import settings

if settings.openai_api_key:
    from openai import OpenAI
    openai_client = OpenAI(api_key=settings.openai_api_key)
else:
    openai_client = None

from models import ADRTemplate, get_db
from services.adr_analysis_engine import ADRAnalysisEngine

router = APIRouter()

ADR_TEMPLATE_PROMPT = """You are an expert Architecture Decision Record (ADR) writer. Generate a comprehensive ADR based on the provided information.

Create an ADR with all 24 standard sections:
1. Title and Identifier
2. Status
3. Context and Background
4. Decision Statement
5. Consequences
6. Alternatives Considered
7. Assumptions
8. Constraints
9. Risks and Mitigations
10. Stakeholders
11. Timeline and Milestones
12. Success Metrics
13. Dependencies
14. Cost Analysis
15. Security Considerations
16. Compliance Requirements
17. Scalability Considerations
18. Performance Impact
19. Maintainability Impact
20. Testing Strategy
21. Rollback Plan
22. Monitoring and Observability
23. Documentation and Knowledge Transfer
24. Review and Approval Process

Format as proper markdown with clear sections. Be specific and detailed.

JIRA Ticket Information:
{ticket_info}

Additional Context:
{user_context}

Generate a professional, comprehensive ADR:"""

@router.post("/templates/generate-from-jira")
async def generate_from_jira(
    jira_ticket_id: str = Form(...),
    user_context: Optional[str] = Form(None),
    use_api: bool = Form(False),
    db: Session = Depends(get_db)
):
    """Generate ADR template from JIRA ticket"""
    try:
        # Prepare ticket info
        ticket_info = f"JIRA Ticket: {jira_ticket_id}"
        
        if use_api and settings.jira_api_url:
            # Would fetch from JIRA API here
            ticket_info = await _fetch_jira_ticket_api(jira_ticket_id)
        else:
            # User will provide info in context
            ticket_info = f"JIRA Ticket ID: {jira_ticket_id}\n{user_context or ''}"
        
        # Generate template
        if openai_client:
            template_content = await _generate_template_with_openai(ticket_info, user_context or "")
        else:
            template_content = _generate_template_default(jira_ticket_id, ticket_info, user_context or "")
        
        # Save template
        template_id = f"template_{uuid.uuid4().hex[:8]}"
        template = ADRTemplate(
            id=template_id,
            jira_ticket_id=jira_ticket_id,
            jira_summary=jira_ticket_id,
            jira_description=ticket_info,
            user_context=user_context,
            template_content=template_content,
            status="draft"
        )
        db.add(template)
        db.commit()
        
        return {
            "id": template_id,
            "status": "success",
            "jira_ticket_id": jira_ticket_id,
            "template": template_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def _fetch_jira_ticket_api(ticket_id: str) -> str:
    """Fetch JIRA ticket from API"""
    # Implementation would use JIRA API
    return f"JIRA Ticket: {ticket_id}"

async def _generate_template_with_openai(ticket_info: str, user_context: str) -> str:
    """Generate template using OpenAI"""
    prompt = ADR_TEMPLATE_PROMPT.format(ticket_info=ticket_info, user_context=user_context)
    
    response = openai_client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": "You are an expert ADR writer following TOGAF principles."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    )
    
    return response.choices[0].message.content

def _generate_template_default(ticket_id: str, ticket_info: str, user_context: str) -> str:
    """Generate template without OpenAI (fallback)"""
    template = f"""# Architecture Decision Record: {ticket_id}

## 1. Title and Identifier
**Title**: [Decision Title Based on {ticket_id}]
**Identifier**: ADR-[NUMBER]
**Related Ticket**: {ticket_id}

## 2. Status
- **Status**: Proposed
- **Last Updated**: [DATE]
- **Owner**: [NAME]

## 3. Context and Background
[Describe the problem and background. What led to this decision?]

{ticket_info}

## 4. Decision Statement
We have decided to [DECISION] because [REASONING].

## 5. Consequences
### Positive Impacts
- [Benefit 1]
- [Benefit 2]

### Negative Impacts
- [Trade-off 1]
- [Trade-off 2]

## 6. Alternatives Considered
### Alternative 1: [Name]
[Description and why not chosen]

### Alternative 2: [Name]
[Description and why not chosen]

## 7. Assumptions
- [Assumption 1]
- [Assumption 2]

## 8. Constraints
- [Constraint 1]
- [Constraint 2]

## 9. Risks and Mitigations
| Risk | Mitigation |
|------|-----------|
| [Risk 1] | [Mitigation 1] |
| [Risk 2] | [Mitigation 2] |

## 10. Stakeholders
- **Decision Makers**: [Roles]
- **Affected Parties**: [Roles]
- **Approvers**: [Roles]

## 11. Timeline and Milestones
- **Decision Date**: [DATE]
- **Implementation Start**: [DATE]
- **Completion Target**: [DATE]

## 12. Success Metrics
- Metric 1: [How to measure]
- Metric 2: [How to measure]

## 13. Dependencies
- [Related ADR or System]
- [Related ADR or System]

## 14. Cost Analysis
- **Development Cost**: [Estimate]
- **Operational Cost**: [Estimate]
- **Expected ROI**: [Estimate and Timeline]

## 15. Security Considerations
- [Security concern 1]
- [Security concern 2]

## 16. Compliance Requirements
- [Regulatory requirement]
- [Policy requirement]

## 17. Scalability Considerations
- Current scale: [Details]
- Target scale: [Details]
- Scalability approach: [Strategy]

## 18. Performance Impact
- Expected latency: [Estimate]
- Throughput: [Estimate]
- Resource utilization: [Estimate]

## 19. Maintainability Impact
- Complexity level: [Low/Medium/High]
- Technical debt: [Impact]
- Knowledge requirements: [Skills needed]

## 20. Testing Strategy
- Unit tests: [Approach]
- Integration tests: [Approach]
- Performance tests: [Approach]

## 21. Rollback Plan
**How to rollback if needed:**
1. [Step 1]
2. [Step 2]
**Rollback time estimate**: [Duration]

## 22. Monitoring and Observability
- **Key Metrics**: [List metrics to monitor]
- **Alerts**: [Alert conditions]
- **Dashboards**: [Dashboard plan]

## 23. Documentation and Knowledge Transfer
- **Documentation**: [What needs to be documented]
- **Training**: [Training plan]
- **Knowledge base**: [KB articles]

## 24. Review and Approval Process
- **Reviewed by**: [Names/Roles]
- **Approved by**: [Names/Roles]
- **Approval date**: [DATE]
- **Sign-offs**: [Required sign-offs]

---

## Additional Context
{user_context if user_context else '[User context would appear here]'}

## Changelog
| Date | Author | Change |
|------|--------|--------|
| [Initial Date] | [Author] | Initial proposal |
"""
    return template

@router.get("/templates/{template_id}")
async def get_template(
    template_id: str,
    db: Session = Depends(get_db)
):
    """Get template"""
    template = db.query(ADRTemplate).filter(ADRTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return {
        "id": template.id,
        "jira_ticket_id": template.jira_ticket_id,
        "template": template.template_content,
        "status": template.status,
        "created_at": template.created_at
    }

@router.get("/templates")
async def list_templates(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List all templates"""
    templates = db.query(ADRTemplate).offset(skip).limit(limit).all()
    return {
        "total": db.query(ADRTemplate).count(),
        "templates": [
            {
                "id": t.id,
                "jira_ticket_id": t.jira_ticket_id,
                "status": t.status,
                "created_at": t.created_at
            }
            for t in templates
        ]
    }

@router.put("/templates/{template_id}")
async def update_template(
    template_id: str,
    content: str = Form(...),
    status: str = Form("draft"),
    db: Session = Depends(get_db)
):
    """Update template"""
    template = db.query(ADRTemplate).filter(ADRTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template.template_content = content
    template.status = status
    db.commit()
    
    return {"id": template.id, "status": "updated"}

@router.delete("/templates/{template_id}")
async def delete_template(
    template_id: str,
    db: Session = Depends(get_db)
):
    """Delete template"""
    template = db.query(ADRTemplate).filter(ADRTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    db.delete(template)
    db.commit()
    
    return {"status": "deleted"}
