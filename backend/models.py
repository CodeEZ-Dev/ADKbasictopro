from sqlalchemy import Column, String, Integer, Text, DateTime, Float, JSON, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from config import settings

Base = declarative_base()

class ADRAnalysis(Base):
    __tablename__ = "adr_analyses"
    
    id = Column(String, primary_key=True, index=True)
    original_content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Phase Results
    structural_analysis = Column(JSON)
    quality_assessment = Column(JSON)
    llm_detection = Column(JSON)
    improvement_suggestions = Column(JSON)
    enterprise_suggestions = Column(JSON)
    design_patterns = Column(JSON)
    technical_debt = Column(JSON)
    maturity_scoring = Column(JSON)
    standards_compliance = Column(JSON)
    
    # Overall scores
    overall_quality_score = Column(Float)
    overall_maturity_score = Column(Float)
    compliance_percentage = Column(Float)
    
    # Analysis metadata
    document_type = Column(String)  # markdown, pdf, text
    file_name = Column(String, nullable=True)

class ADRTemplate(Base):
    __tablename__ = "adr_templates"
    
    id = Column(String, primary_key=True, index=True)
    jira_ticket_id = Column(String, index=True)
    jira_summary = Column(String)
    jira_description = Column(Text)
    user_context = Column(Text, nullable=True)
    template_content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String, default="draft")  # draft, reviewed, approved

class JIRAIntegration(Base):
    __tablename__ = "jira_integrations"
    
    id = Column(String, primary_key=True, index=True)
    jira_ticket_id = Column(String, unique=True, index=True)
    issue_key = Column(String)
    summary = Column(String)
    description = Column(Text)
    status = Column(String)
    assignee = Column(String, nullable=True)
    fields_json = Column(JSON)
    synced_at = Column(DateTime, default=datetime.utcnow)

# Database setup
engine = create_engine(
    settings.database_url,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    echo=settings.debug
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
