import re
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

@dataclass
class StructuralAnalysisResult:
    """Results from structural analysis phase"""
    has_title: bool
    has_status: bool
    has_context: bool
    has_decision: bool
    has_consequences: bool
    mandatory_sections_count: int
    mandatory_sections_present: List[str]
    mandatory_sections_missing: List[str]
    optional_sections_found: List[str]
    structure_quality_score: float
    detailed_findings: str

@dataclass
class QualityAssessmentResult:
    """Results from quality assessment phase"""
    completeness_score: float
    clarity_score: float
    traceability_score: float
    consistency_score: float
    justification_score: float
    overall_quality_score: float
    quality_dimensions: Dict[str, Any]

@dataclass
class LLMDetectionResult:
    """Results from LLM detection phase"""
    confidence: float
    is_likely_ai_generated: bool
    ai_indicators: List[str]
    analysis_text: str

@dataclass
class ImprovementSuggestion:
    """Single improvement suggestion"""
    priority: str  # High, Medium, Low
    category: str
    description: str
    specific_example: str
    implementation_guidance: str

@dataclass
class EnterpriseArchitectureSuggestion:
    """TOGAF-aligned enterprise suggestion"""
    category: str  # Strategic Alignment, Governance, Integration, Security, Scalability, Data Management
    priority: str  # High, Medium, Low
    description: str
    rationale: str
    implementation_guidance: str
    impact_assessment: str

@dataclass
class DesignPattern:
    """Design pattern recommendation"""
    name: str
    category: str  # Architectural, Integration, Data, Resilience, Security, Scalability
    applicability: str
    benefits: List[str]
    considerations: List[str]
    implementation_hints: str

@dataclass
class TechnicalDebtItem:
    """Technical debt item"""
    type: str  # Code, Architectural, Design, Documentation, Test, Infrastructure, Knowledge
    severity: str  # High, Medium, Low
    description: str
    impact: str
    remediation_strategy: str
    estimated_effort: str  # Low, Medium, High

@dataclass
class ArchitectureMaturityResult:
    """Architecture maturity assessment"""
    overall_maturity_score: float
    maturity_level: str  # Initial, Developing, Defined, Managed, Optimizing
    documentation_quality: float
    decision_rationale: float
    risk_assessment: float
    alternative_analysis: float
    improvement_pathway: List[str]

@dataclass
class StandardsComplianceTopic:
    """Single compliance topic"""
    topic_name: str
    topic_description: str
    status: str  # Present, Missing
    content_summary: str
    recommendations: str

@dataclass
class StandardsComplianceResult:
    """Standards compliance analysis results"""
    total_topics: int
    present_topics_count: int
    missing_topics_count: int
    compliance_percentage: float
    topics: List[StandardsComplianceTopic]
    priority_improvements: List[str]

class ADRAnalysisEngine:
    """Nine-phase ADR Analysis Engine"""
    
    MANDATORY_SECTIONS = ["Title", "Status", "Context", "Decision", "Consequences"]
    OPTIONAL_SECTIONS = ["Alternatives", "Assumptions", "Constraints", "Risks", "Stakeholders"]
    
    STANDARD_ADR_TOPICS = [
        "Title and Identifier",
        "Status",
        "Context and Background",
        "Decision Statement",
        "Consequences",
        "Alternatives Considered",
        "Assumptions",
        "Constraints",
        "Risks and Mitigations",
        "Stakeholders",
        "Timeline and Milestones",
        "Success Metrics",
        "Dependencies",
        "Cost Analysis",
        "Security Considerations",
        "Compliance Requirements",
        "Scalability Considerations",
        "Performance Impact",
        "Maintainability Impact",
        "Testing Strategy",
        "Rollback Plan",
        "Monitoring and Observability",
        "Documentation and Knowledge Transfer",
        "Review and Approval Process",
    ]
    
    LLM_GENERIC_PHRASES = [
        "it is important to note that",
        "in conclusion",
        "furthermore",
        "in summary",
        "it should be noted that",
        "the significance of",
        "in light of",
        "as a result",
        "additionally",
        "in this context",
        "the implementation of",
        "positive impacts",
        "negative impacts",
        "various stakeholders",
        "best practices",
        "comprehensive approach",
        "scalable solution",
        "seamless integration",
        "robust architecture",
        "innovative approach"
    ]
    
    def __init__(self, content: str):
        self.content = content
        self.lines = content.split('\n')
        self.sections = self._extract_sections()
    
    def _extract_sections(self) -> Dict[str, str]:
        """Extract sections from ADR content"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in self.lines:
            # Check for markdown headers (# or ##)
            if line.startswith('#'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line.lstrip('#').strip().lower()
                current_content = []
            elif current_section:
                current_content.append(line)
        
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    # ===== PHASE 1: Structural Analysis =====
    def phase1_structural_analysis(self) -> StructuralAnalysisResult:
        """Analyze document structure"""
        mandatory_present = []
        mandatory_missing = []
        
        section_keys = list(self.sections.keys())
        
        for section in self.MANDATORY_SECTIONS:
            section_key = section.lower()
            if any(section_key in key for key in section_keys):
                mandatory_present.append(section)
            else:
                mandatory_missing.append(section)
        
        optional_found = []
        for section in self.OPTIONAL_SECTIONS:
            section_key = section.lower()
            if any(section_key in key for key in section_keys):
                optional_found.append(section)
        
        # Calculate structure quality score
        structure_quality = (len(mandatory_present) / len(self.MANDATORY_SECTIONS)) * 100
        if optional_found:
            structure_quality = structure_quality * 0.8 + (len(optional_found) / len(self.OPTIONAL_SECTIONS)) * 10 * 0.2
        
        return StructuralAnalysisResult(
            has_title=any('title' in key for key in section_keys),
            has_status=any('status' in key for key in section_keys),
            has_context=any('context' in key for key in section_keys),
            has_decision=any('decision' in key for key in section_keys),
            has_consequences=any('consequenc' in key for key in section_keys),
            mandatory_sections_count=len(mandatory_present),
            mandatory_sections_present=mandatory_present,
            mandatory_sections_missing=mandatory_missing,
            optional_sections_found=optional_found,
            structure_quality_score=min(structure_quality, 100),
            detailed_findings=f"Document has {len(section_keys)} sections. "
                             f"Mandatory sections present: {len(mandatory_present)}/{len(self.MANDATORY_SECTIONS)}."
        )
    
    # ===== PHASE 2: Quality Assessment =====
    def phase2_quality_assessment(self) -> QualityAssessmentResult:
        """Assess ADR quality"""
        # Completeness: measure detail depth and coverage
        completeness_score = 0
        if self.sections:
            avg_section_length = sum(len(v.split()) for v in self.sections.values()) / len(self.sections)
            completeness_score = min((avg_section_length / 100) * 100, 100)
        
        # Clarity: check for clear language patterns
        clarity_score = self._assess_clarity()
        
        # Traceability: check for references and linkages
        traceability_score = self._assess_traceability()
        
        # Consistency: check internal coherence
        consistency_score = self._assess_consistency()
        
        # Justification: assess decision rationale quality
        justification_score = self._assess_justification()
        
        overall_score = (completeness_score + clarity_score + traceability_score + 
                        consistency_score + justification_score) / 5
        
        return QualityAssessmentResult(
            completeness_score=completeness_score,
            clarity_score=clarity_score,
            traceability_score=traceability_score,
            consistency_score=consistency_score,
            justification_score=justification_score,
            overall_quality_score=overall_score,
            quality_dimensions={
                "completeness": completeness_score,
                "clarity": clarity_score,
                "traceability": traceability_score,
                "consistency": consistency_score,
                "justification": justification_score
            }
        )
    
    def _assess_clarity(self) -> float:
        """Assess clarity of writing"""
        clarity_score = 50  # baseline
        
        # Check for clear structure
        if self.sections:
            clarity_score += 20
        
        # Check sentence length (shorter is usually clearer)
        sentences = [s for s in self.content.split('.') if s.strip()]
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_sentence_length < 25:
                clarity_score += 20
            elif avg_sentence_length < 35:
                clarity_score += 10
        
        # Check for passive voice (less clear)
        passive_patterns = r'\bis\s+\w+en\b|\bwas\s+\w+en\b|\bwere\s+\w+en\b'
        passive_count = len(re.findall(passive_patterns, self.content, re.IGNORECASE))
        clarity_score -= min(passive_count * 2, 10)
        
        return min(clarity_score, 100)
    
    def _assess_traceability(self) -> float:
        """Assess traceability (references, links, dependencies)"""
        score = 30  # baseline
        
        # Check for references (links, ticket numbers)
        reference_patterns = [r'https?://\S+', r'#\d+', r'ADR-\d+', r'JIRA-\d+', r'issue\s+#\d+']
        reference_count = sum(len(re.findall(p, self.content)) for p in reference_patterns)
        
        score += min(reference_count * 5, 40)
        
        # Check for dependency mentions
        dependency_keywords = ['depends', 'prerequisite', 'related', 'impact', 'affects']
        dependency_count = sum(self.content.lower().count(kw) for kw in dependency_keywords)
        score += min(dependency_count * 3, 30)
        
        return min(score, 100)
    
    def _assess_consistency(self) -> float:
        """Assess internal consistency"""
        score = 50  # baseline
        
        # Check for consistent terminology
        major_terms = self._extract_major_terms()
        term_frequency = {}
        for term in major_terms:
            term_frequency[term] = self.content.lower().count(term.lower())
        
        # High variance in usage suggests inconsistency
        if term_frequency:
            frequencies = list(term_frequency.values())
            if len(frequencies) > 0:
                variance = max(frequencies) - min(frequencies)
                score += 50 - min(variance, 50)
        
        return min(score, 100)
    
    def _assess_justification(self) -> float:
        """Assess quality of decision justification"""
        score = 40  # baseline
        
        # Check for justification keywords
        justification_keywords = ['because', 'due to', 'since', 'therefore', 'rationale', 'reasoning', 'justify']
        justification_count = sum(self.content.lower().count(kw) for kw in justification_keywords)
        
        score += min(justification_count * 5, 40)
        
        # Check for consequence analysis
        consequence_keywords = ['will', 'may', 'might', 'could', 'result', 'impact', 'effect']
        consequence_count = sum(self.content.lower().count(kw) for kw in consequence_keywords)
        
        score += min(consequence_count * 2, 20)
        
        return min(score, 100)
    
    def _extract_major_terms(self) -> List[str]:
        """Extract major terms from the document"""
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', self.content)
        from collections import Counter
        counter = Counter(words)
        return [word for word, count in counter.most_common(10) if count > 1]
    
    # ===== PHASE 3: LLM Detection =====
    def phase3_llm_detection(self) -> LLMDetectionResult:
        """Detect AI-generated content patterns"""
        confidence = 0
        indicators = []
        
        # Count generic phrases
        generic_count = sum(
            len(re.findall(re.escape(phrase), self.content, re.IGNORECASE))
            for phrase in self.LLM_GENERIC_PHRASES
        )
        
        if generic_count > 5:
            confidence += generic_count * 3
            for phrase in self.LLM_GENERIC_PHRASES:
                if phrase in self.content.lower():
                    indicators.append(f"Generic phrase: '{phrase}'")
        
        # Check for repetitive structure
        lines = [l.strip() for l in self.lines if l.strip()]
        if len(lines) > 5:
            # Check for similar line patterns
            for i in range(len(lines) - 1):
                if len(lines[i]) > 10 and len(lines[i+1]) > 10:
                    if lines[i].split()[: -1] == lines[i+1].split()[: -1]:
                        confidence += 5
                        indicators.append("Repetitive sentence structure detected")
                        break
        
        # Check for perfect grammar/formatting (sometimes excessive)
        if re.search(r'[.!?]\s+[A-Z]', self.content):
            proper_sentences = len(re.findall(r'[.!?]\s+[A-Z]', self.content))
            total_sentences = len(re.findall(r'[.!?]', self.content))
            if total_sentences > 0 and proper_sentences / total_sentences > 0.9:
                confidence += 10
                indicators.append("Consistently perfect punctuation and capitalization")
        
        # Check for corporate jargon
        corporate_terms = ['leverage', 'synergy', 'paradigm', 'ecosystem', 'holistic', 'seamless']
        corporate_count = sum(self.content.lower().count(term) for term in corporate_terms)
        if corporate_count > 3:
            confidence += corporate_count * 2
            indicators.append(f"High corporate jargon usage ({corporate_count} terms)")
        
        # Normalize confidence to 0-100
        confidence = min(confidence, 100)
        is_likely_ai = confidence > 50
        
        return LLMDetectionResult(
            confidence=confidence,
            is_likely_ai_generated=is_likely_ai,
            ai_indicators=indicators,
            analysis_text=f"Confidence score: {confidence}. Detected {len(indicators)} AI-like indicators."
        )
    
    # ===== PHASE 4: Improvement Suggestions =====
    def phase4_improvement_suggestions(self) -> List[ImprovementSuggestion]:
        """Generate actionable improvement suggestions"""
        suggestions: List[ImprovementSuggestion] = []
        
        # Structural improvements
        if not self.sections:
            suggestions.append(ImprovementSuggestion(
                priority="High",
                category="Structure",
                description="Add markdown section headers for clarity",
                specific_example="Use # Title, ## Status, ## Context format",
                implementation_guidance="Refactor content to use proper markdown headers for each section"
            ))
        
        # Missing sections
        analysis = self.phase1_structural_analysis()
        for missing in analysis.mandatory_sections_missing:
            suggestions.append(ImprovementSuggestion(
                priority="High",
                category="Missing Content",
                description=f"Add missing '{missing}' section",
                specific_example=f"## {missing}\n[Detailed content about {missing.lower()}]",
                implementation_guidance=f"Create a new section that fully addresses {missing.lower()}"
            ))
        
        # Quality improvements
        quality = self.phase2_quality_assessment()
        if quality.clarity_score < 70:
            suggestions.append(ImprovementSuggestion(
                priority="Medium",
                category="Clarity",
                description="Improve clarity and readability",
                specific_example="Break long paragraphs into shorter sentences",
                implementation_guidance="Review for passive voice and overly complex sentences"
            ))
        
        if quality.justification_score < 70:
            suggestions.append(ImprovementSuggestion(
                priority="High",
                category="Justification",
                description="Strengthen decision rationale",
                specific_example="Add 'because' and 'therefore' statements",
                implementation_guidance="Explicitly explain why this decision was made and what led to it"
            ))
        
        # Traceability improvements
        if quality.traceability_score < 60:
            suggestions.append(ImprovementSuggestion(
                priority="Medium",
                category="Traceability",
                description="Add references and linkages",
                specific_example="Link to related ADRs or JIRA tickets",
                implementation_guidance="Include URLs, ticket numbers, and cross-references"
            ))
        
        return sorted(suggestions, key=lambda x: {"High": 0, "Medium": 1, "Low": 2}[x.priority])
    
    # ===== PHASE 5: Enterprise Architecture Suggestions =====
    def phase5_enterprise_suggestions(self) -> List[EnterpriseArchitectureSuggestion]:
        """TOGAF-aligned enterprise architecture suggestions"""
        suggestions: List[EnterpriseArchitectureSuggestion] = []
        
        # Strategic Alignment
        suggestions.append(EnterpriseArchitectureSuggestion(
            category="Strategic Alignment",
            priority="High",
            description="Align decision with business goals",
            rationale="Architecture decisions should directly support strategic objectives",
            implementation_guidance="Map decision to 2-3 key business drivers and quantify business value",
            impact_assessment="Enables better portfolio management and resource allocation"
        ))
        
        # Governance
        suggestions.append(EnterpriseArchitectureSuggestion(
            category="Governance",
            priority="High",
            description="Establish governance and approval routing",
            rationale="Clear governance ensures consistency and accountability",
            implementation_guidance="Define approval body, review criteria, and escalation paths",
            impact_assessment="Reduces rework and ensures compliance"
        ))
        
        # Integration
        suggestions.append(EnterpriseArchitectureSuggestion(
            category="Integration",
            priority="Medium",
            description="Plan integration with existing systems",
            rationale="Integration considerations prevent silos and data fragmentation",
            implementation_guidance="Document integration patterns, data flows, and API contracts",
            impact_assessment="Reduces integration costs and time-to-value"
        ))
        
        # Security
        suggestions.append(EnterpriseArchitectureSuggestion(
            category="Security",
            priority="High",
            description="Address security implications",
            rationale="Security must be architected in, not added after",
            implementation_guidance="Conduct threat modeling and document security controls",
            impact_assessment="Prevents costly security fixes and compliance issues"
        ))
        
        # Scalability
        suggestions.append(EnterpriseArchitectureSuggestion(
            category="Scalability",
            priority="Medium",
            description="Plan for scalability and growth",
            rationale="Architecture should support future growth without major rework",
            implementation_guidance="Define scaling strategy, capacity planning, and performance targets",
            impact_assessment="Reduces need for rearchitecting as users grow"
        ))
        
        # Data Management
        suggestions.append(EnterpriseArchitectureSuggestion(
            category="Data Management",
            priority="Medium",
            description="Establish data management principles",
            rationale="Consistent data management enables informed decision-making",
            implementation_guidance="Define data ownership, quality standards, and governance",
            impact_assessment="Improves data quality and accessibility"
        ))
        
        return suggestions
    
    # ===== PHASE 6: Design Pattern Recommendations =====
    def phase6_design_patterns(self) -> List[DesignPattern]:
        """Recommend applicable design patterns"""
        patterns: List[DesignPattern] = []
        
        # Architectural Patterns
        patterns.extend([
            DesignPattern(
                name="Microservices",
                category="Architectural",
                applicability="For large, complex systems with independent scaling needs",
                benefits=["Independent scaling", "Technology diversity", "Fault isolation"],
                considerations=["Distributed system complexity", "Data consistency challenges"],
                implementation_hints="Use service mesh, implement circuit breakers, establish API contracts"
            ),
            DesignPattern(
                name="Layered Architecture",
                category="Architectural",
                applicability="For traditional applications with clear separation of concerns",
                benefits=["Ease of organization", "Clear separation of concerns", "Team structure alignment"],
                considerations=["May become monolithic", "Vertical scaling limits"],
                implementation_hints="Enforce layer boundaries, avoid layer skipping, document interfaces"
            ),
            DesignPattern(
                name="Event-Driven Architecture",
                category="Architectural",
                applicability="For systems requiring real-time responsiveness and loose coupling",
                benefits=["Loose coupling", "Real-time processing", "Scalability"],
                considerations=["Event ordering complexity", "Testing challenges"],
                implementation_hints="Use event brokers, implement idempotency, define event schemas"
            ),
        ])
        
        # Integration Patterns
        patterns.extend([
            DesignPattern(
                name="API Gateway",
                category="Integration",
                applicability="For managing external access to microservices",
                benefits=["Simplified client architecture", "Cross-cutting concerns centralization"],
                considerations=["Single point of failure", "Performance bottleneck potential"],
                implementation_hints="Implement caching, rate limiting, and request routing"
            ),
            DesignPattern(
                name="Service Mesh",
                category="Integration",
                applicability="For managing service-to-service communication",
                benefits=["Observability", "Traffic management", "Security policies without code changes"],
                considerations=["Added complexity", "Performance overhead"],
                implementation_hints="Use sidecar proxies, implement fine-grained policies"
            ),
        ])
        
        # Resilience Patterns
        patterns.extend([
            DesignPattern(
                name="Circuit Breaker",
                category="Resilience",
                applicability="For preventing cascading failures",
                benefits=["Fail fast", "Prevent resource exhaustion", "Self-healing"],
                considerations=["State management", "Testing complexity"],
                implementation_hints="Define thresholds, implement exponential backoff, monitor state changes"
            ),
            DesignPattern(
                name="Bulkhead",
                category="Resilience",
                applicability="For isolating critical resources",
                benefits=["Fault isolation", "Resource protection"],
                considerations=["Resource overhead", "Complexity"],
                implementation_hints="Use thread pools or containers, monitor resource usage"
            ),
        ])
        
        # Data Patterns
        patterns.extend([
            DesignPattern(
                name="Event Sourcing",
                category="Data",
                applicability="For systems requiring audit trails and temporal queries",
                benefits=["Complete audit trail", "Event replay capability", "Temporal queries"],
                considerations=["Eventual consistency", "Storage overhead"],
                implementation_hints="Use append-only logs, implement snapshots, define projections"
            ),
            DesignPattern(
                name="CQRS",
                category="Data",
                applicability="For systems with different read/write patterns",
                benefits=["Scalability optimization", "Query flexibility", "Event sourcing alignment"],
                considerations=["Eventual consistency", "Complexity"],
                implementation_hints="Separate read/write models, use event projections"
            ),
        ])
        
        return patterns
    
    # ===== PHASE 7: Technical Debt Analysis =====
    def phase7_technical_debt(self) -> List[TechnicalDebtItem]:
        """Analyze technical debt"""
        debts: List[TechnicalDebtItem] = []
        
        quality = self.phase2_quality_assessment()
        
        if quality.overall_quality_score < 60:
            debts.append(TechnicalDebtItem(
                type="Documentation",
                severity="High",
                description="Documentation lacks completeness and clarity",
                impact="Increases onboarding time and decision ambiguity",
                remediation_strategy="Systematically improve each section with specific examples and rationale",
                estimated_effort="Medium"
            ))
        
        if not self.sections or len(self.sections) < 5:
            debts.append(TechnicalDebtItem(
                type="Architectural",
                severity="High",
                description="ADR lacks proper architectural documentation structure",
                impact="Makes it difficult to govern and evolve architecture",
                remediation_strategy="Restructure into proper ADR format with all required sections",
                estimated_effort="High"
            ))
        
        llm_detect = self.phase3_llm_detection()
        if llm_detect.confidence > 60:
            debts.append(TechnicalDebtItem(
                type="Knowledge",
                severity="Medium",
                description="ADR may lack authentic domain expertise insights",
                impact="Decisions may not account for organizational specifics",
                remediation_strategy="Review and enhance with team expertise and organizational context",
                estimated_effort="Medium"
            ))
        
        if quality.justification_score < 70:
            debts.append(TechnicalDebtItem(
                type="Design",
                severity="High",
                description="Decision rationale is not clearly documented",
                impact="Future maintainers may not understand decision context",
                remediation_strategy="Add explicit rationale, tradeoffs, and alternatives analysis",
                estimated_effort="Medium"
            ))
        
        if quality.traceability_score < 60:
            debts.append(TechnicalDebtItem(
                type="Code",
                severity="Medium",
                description="Lacks linkage to implementation and related decisions",
                impact="Difficult to trace decisions to code and maintain consistency",
                remediation_strategy="Add references to code, related ADRs, and tracking tickets",
                estimated_effort="Low"
            ))
        
        return debts
    
    # ===== PHASE 8: Architecture Maturity Scoring =====
    def phase8_maturity_scoring(self) -> ArchitectureMaturityResult:
        """Score architecture maturity"""
        quality = self.phase2_quality_assessment()
        analysis = self.phase1_structural_analysis()
        llm_detect = self.phase3_llm_detection()
        
        # Dimensions
        documentation_quality = quality.completeness_score
        decision_rationale = quality.justification_score
        risk_assessment = self._assess_risk_mitigation()
        alternative_analysis = quality.consistency_score
        
        overall_score = (documentation_quality + decision_rationale + risk_assessment + alternative_analysis) / 4
        
        # Determine maturity level
        if overall_score < 20:
            maturity_level = "Initial"
        elif overall_score < 40:
            maturity_level = "Developing"
        elif overall_score < 60:
            maturity_level = "Defined"
        elif overall_score < 80:
            maturity_level = "Managed"
        else:
            maturity_level = "Optimizing"
        
        # Improvement pathway
        improvements = []
        if documentation_quality < 70:
            improvements.append("Improve documentation completeness and detail")
        if decision_rationale < 70:
            improvements.append("Strengthen decision justification and rationale")
        if risk_assessment < 70:
            improvements.append("Add comprehensive risk assessment and mitigation strategies")
        if alternative_analysis < 70:
            improvements.append("Document alternatives evaluation and tradeoffs")
        
        if not improvements:
            improvements.append("Maintain high standards and seek continuous improvement")
        
        return ArchitectureMaturityResult(
            overall_maturity_score=overall_score,
            maturity_level=maturity_level,
            documentation_quality=documentation_quality,
            decision_rationale=decision_rationale,
            risk_assessment=risk_assessment,
            alternative_analysis=alternative_analysis,
            improvement_pathway=improvements
        )
    
    def _assess_risk_mitigation(self) -> float:
        """Assess risk identification and mitigation"""
        score = 30  # baseline
        
        # Check for risk-related keywords
        risk_keywords = ['risk', 'mitigation', 'threat', 'vulnerability', 'impact', 'consequence', 'failure']
        risk_count = sum(self.content.lower().count(kw) for kw in risk_keywords)
        
        score += min(risk_count * 3, 50)
        
        # Check for mitigation strategies
        mitigation_keywords = ['mitigate', 'prevent', 'monitor', 'control', 'contingency']
        mitigation_count = sum(self.content.lower().count(kw) for kw in mitigation_keywords)
        
        score += min(mitigation_count * 4, 20)
        
        return min(score, 100)
    
    # ===== PHASE 9: Standards Compliance Analysis =====
    def phase9_standards_compliance(self) -> StandardsComplianceResult:
        """Analyze compliance with 24-point ADR standard"""
        topics: List[StandardsComplianceTopic] = []
        
        for topic_name in self.STANDARD_ADR_TOPICS:
            # Simple check: is topic mentioned in content?
            topic_key = topic_name.lower()
            is_present = any(topic_key.replace(' ', '') in section_name.replace(' ', '')
                           for section_name in self.sections.keys())
            
            # For some topics, check for keywords
            keywords = {
                "Risks and Mitigations": ["risk", "mitigation", "threat"],
                "Security Considerations": ["security", "encrypt", "auth"],
                "Compliance Requirements": ["compliance", "regulation", "standard"],
                "Timeline and Milestones": ["timeline", "milestone", "schedule", "date"],
                "Success Metrics": ["metric", "kpi", "measurement", "success"],
                "Rollback Plan": ["rollback", "fallback", "revert"],
                "Monitoring and Observability": ["monitoring", "observability", "alert", "metric"],
            }
            
            if topic_name in keywords:
                keyword_found = any(kw in self.content.lower() for kw in keywords[topic_name])
                is_present = is_present or keyword_found
            
            topic = StandardsComplianceTopic(
                topic_name=topic_name,
                topic_description=f"Requirement: {topic_name}",
                status="Present" if is_present else "Missing",
                content_summary=f"{'Included in ADR' if is_present else 'Not addressed'}",
                recommendations="" if is_present else f"Add '{topic_name}' section with details"
            )
            topics.append(topic)
        
        present_count = sum(1 for t in topics if t.status == "Present")
        missing_count = len(topics) - present_count
        compliance_percentage = (present_count / len(topics)) * 100
        
        # Priority improvements
        priority_improvements = [t.topic_name for t in topics if t.status == "Missing"][:5]
        
        return StandardsComplianceResult(
            total_topics=len(topics),
            present_topics_count=present_count,
            missing_topics_count=missing_count,
            compliance_percentage=compliance_percentage,
            topics=topics,
            priority_improvements=priority_improvements
        )
    
    # ===== MAIN ANALYSIS METHOD =====
    def analyze(self) -> Dict[str, Any]:
        """Execute all 9 phases of analysis"""
        return {
            "phase_1_structural_analysis": asdict(self.phase1_structural_analysis()),
            "phase_2_quality_assessment": asdict(self.phase2_quality_assessment()),
            "phase_3_llm_detection": asdict(self.phase3_llm_detection()),
            "phase_4_improvements": [asdict(s) for s in self.phase4_improvement_suggestions()],
            "phase_5_enterprise": [asdict(s) for s in self.phase5_enterprise_suggestions()],
            "phase_6_design_patterns": [asdict(p) for p in self.phase6_design_patterns()],
            "phase_7_technical_debt": [asdict(d) for d in self.phase7_technical_debt()],
            "phase_8_maturity": asdict(self.phase8_maturity_scoring()),
            "phase_9_compliance": asdict(self.phase9_standards_compliance()),
        }
