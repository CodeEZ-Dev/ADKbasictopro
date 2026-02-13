from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
import httpx
from config import settings
from models import JIRAIntegration, get_db
import base64

router = APIRouter()

class JIRAClient:
    """JIRA API Client"""
    
    def __init__(self, base_url: str, username: str, token: str):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.token = token
        self.headers = {
            "Authorization": f"Basic {base64.b64encode(f'{username}:{token}'.encode()).decode()}",
            "Content-Type": "application/json"
        }
    
    async def get_issue(self, issue_key: str) -> dict:
        """Fetch issue from JIRA"""
        url = f"{self.base_url}/rest/api/3/issues/{issue_key}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="JIRA API error")
            return response.json()

def _parse_jira_response(issue: dict) -> dict:
    """Parse JIRA issue response"""
    fields = issue.get("fields", {})
    return {
        "key": issue.get("key"),
        "id": issue.get("id"),
        "summary": fields.get("summary", ""),
        "description": fields.get("description", ""),
        "status": fields.get("status", {}).get("name", ""),
        "assignee": fields.get("assignee", {}).get("displayName", ""),
        "issue_type": fields.get("issuetype", {}).get("name", ""),
        "priority": fields.get("priority", {}).get("name", ""),
        "labels": fields.get("labels", []),
        "created": fields.get("created", ""),
        "updated": fields.get("updated", ""),
        "due_date": fields.get("duedate", ""),
    }

@router.get("/jira/issues/{issue_key}")
async def get_jira_issue(
    issue_key: str,
    db: Session = Depends(get_db)
):
    """Fetch JIRA issue"""
    if not settings.jira_api_url or not settings.jira_api_token:
        raise HTTPException(status_code=400, detail="JIRA integration not configured")
    
    try:
        client = JIRAClient(settings.jira_api_url, settings.jira_username, settings.jira_api_token)
        issue_data = await client.get_issue(issue_key)
        parsed = _parse_jira_response(issue_data)
        
        # Cache in database
        jira_int = JIRAIntegration(
            id=f"jira_{issue_key}",
            jira_ticket_id=issue_key,
            issue_key=parsed["key"],
            summary=parsed["summary"],
            description=parsed["description"],
            status=parsed["status"],
            assignee=parsed.get("assignee"),
            fields_json=parsed
        )
        
        # Update or insert
        existing = db.query(JIRAIntegration).filter(JIRAIntegration.issue_key == issue_key).first()
        if existing:
            existing.summary = parsed["summary"]
            existing.description = parsed["description"]
            existing.status = parsed["status"]
            existing.fields_json = parsed
        else:
            db.add(jira_int)
        
        db.commit()
        
        return {
            "status": "success",
            "issue": parsed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jira/issues/cached")
async def list_cached_issues(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List cached JIRA issues"""
    issues = db.query(JIRAIntegration).offset(skip).limit(limit).all()
    return {
        "total": db.query(JIRAIntegration).count(),
        "issues": [
            {
                "key": i.issue_key,
                "summary": i.summary,
                "status": i.status,
                "assigned_to": i.assignee,
                "synced_at": i.synced_at
            }
            for i in issues
        ]
    }

@router.post("/jira/test-connection")
async def test_jira_connection():
    """Test JIRA API connection"""
    if not settings.jira_api_url:
        return {
            "status": "not_configured",
            "message": "JIRA integration not configured"
        }
    
    try:
        client = JIRAClient(settings.jira_api_url, settings.jira_username, settings.jira_api_token)
        # Try to fetch a test issue (use atlassian-jira project)
        result = await client.get_issue("TEST-1")
        return {
            "status": "success",
            "message": "Connection successful"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@router.get("/jira/config-status")
async def check_jira_config():
    """Check if JIRA is configured"""
    return {
        "configured": bool(settings.jira_api_url and settings.jira_api_token),
        "url": settings.jira_api_url if settings.jira_api_url else "Not configured",
        "username": settings.jira_username if settings.jira_username else "Not configured"
    }
