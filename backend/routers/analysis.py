from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import markdown
from PyPDF2 import PdfReader
from io import BytesIO

from models import ADRAnalysis, get_db
from services.adr_analysis_engine import ADRAnalysisEngine

router = APIRouter()

def extract_text_from_pdf(pdf_file: UploadFile) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PdfReader(BytesIO(pdf_file.file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

@router.post("/analyze/text")
async def analyze_text(
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    """Analyze ADR from text input"""
    try:
        # Run analysis
        engine = ADRAnalysisEngine(content)
        results = engine.analyze()
        
        # Save to database
        analysis_id = f"analysis_{uuid.uuid4().hex[:8]}"
        analysis = ADRAnalysis(
            id=analysis_id,
            original_content=content,
            document_type="text",
            structural_analysis=results["phase_1_structural_analysis"],
            quality_assessment=results["phase_2_quality_assessment"],
            llm_detection=results["phase_3_llm_detection"],
            improvement_suggestions=results["phase_4_improvements"],
            enterprise_suggestions=results["phase_5_enterprise"],
            design_patterns=results["phase_6_design_patterns"],
            technical_debt=results["phase_7_technical_debt"],
            maturity_scoring=results["phase_8_maturity"],
            standards_compliance=results["phase_9_compliance"],
            overall_quality_score=results["phase_2_quality_assessment"]["overall_quality_score"],
            overall_maturity_score=results["phase_8_maturity"]["overall_maturity_score"],
            compliance_percentage=results["phase_9_compliance"]["compliance_percentage"]
        )
        db.add(analysis)
        db.commit()
        
        return {
            "id": analysis_id,
            "status": "success",
            "analysis": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/markdown")
async def analyze_markdown(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Analyze ADR from markdown file"""
    try:
        content = await file.read()
        text = content.decode("utf-8")
        
        # Run analysis
        engine = ADRAnalysisEngine(text)
        results = engine.analyze()
        
        # Save to database
        analysis_id = f"analysis_{uuid.uuid4().hex[:8]}"
        analysis = ADRAnalysis(
            id=analysis_id,
            original_content=text,
            document_type="markdown",
            file_name=file.filename,
            structural_analysis=results["phase_1_structural_analysis"],
            quality_assessment=results["phase_2_quality_assessment"],
            llm_detection=results["phase_3_llm_detection"],
            improvement_suggestions=results["phase_4_improvements"],
            enterprise_suggestions=results["phase_5_enterprise"],
            design_patterns=results["phase_6_design_patterns"],
            technical_debt=results["phase_7_technical_debt"],
            maturity_scoring=results["phase_8_maturity"],
            standards_compliance=results["phase_9_compliance"],
            overall_quality_score=results["phase_2_quality_assessment"]["overall_quality_score"],
            overall_maturity_score=results["phase_8_maturity"]["overall_maturity_score"],
            compliance_percentage=results["phase_9_compliance"]["compliance_percentage"]
        )
        db.add(analysis)
        db.commit()
        
        return {
            "id": analysis_id,
            "status": "success",
            "analysis": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze/pdf")
async def analyze_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Analyze ADR from PDF file"""
    try:
        text = extract_text_from_pdf(file)
        
        # Run analysis
        engine = ADRAnalysisEngine(text)
        results = engine.analyze()
        
        # Save to database
        analysis_id = f"analysis_{uuid.uuid4().hex[:8]}"
        analysis = ADRAnalysis(
            id=analysis_id,
            original_content=text,
            document_type="pdf",
            file_name=file.filename,
            structural_analysis=results["phase_1_structural_analysis"],
            quality_assessment=results["phase_2_quality_assessment"],
            llm_detection=results["phase_3_llm_detection"],
            improvement_suggestions=results["phase_4_improvements"],
            enterprise_suggestions=results["phase_5_enterprise"],
            design_patterns=results["phase_6_design_patterns"],
            technical_debt=results["phase_7_technical_debt"],
            maturity_scoring=results["phase_8_maturity"],
            standards_compliance=results["phase_9_compliance"],
            overall_quality_score=results["phase_2_quality_assessment"]["overall_quality_score"],
            overall_maturity_score=results["phase_8_maturity"]["overall_maturity_score"],
            compliance_percentage=results["phase_9_compliance"]["compliance_percentage"]
        )
        db.add(analysis)
        db.commit()
        
        return {
            "id": analysis_id,
            "status": "success",
            "analysis": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis/{analysis_id}")
async def get_analysis(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """Retrieve analysis results"""
    analysis = db.query(ADRAnalysis).filter(ADRAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {
        "id": analysis.id,
        "created_at": analysis.created_at,
        "file_name": analysis.file_name,
        "document_type": analysis.document_type,
        "phase_1_structural_analysis": analysis.structural_analysis,
        "phase_2_quality_assessment": analysis.quality_assessment,
        "phase_3_llm_detection": analysis.llm_detection,
        "phase_4_improvements": analysis.improvement_suggestions,
        "phase_5_enterprise": analysis.enterprise_suggestions,
        "phase_6_design_patterns": analysis.design_patterns,
        "phase_7_technical_debt": analysis.technical_debt,
        "phase_8_maturity": analysis.maturity_scoring,
        "phase_9_compliance": analysis.standards_compliance,
        "overall_quality_score": analysis.overall_quality_score,
        "overall_maturity_score": analysis.overall_maturity_score,
        "compliance_percentage": analysis.compliance_percentage
    }

@router.get("/analyses")
async def list_analyses(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List all analyses"""
    analyses = db.query(ADRAnalysis).offset(skip).limit(limit).all()
    return {
        "total": db.query(ADRAnalysis).count(),
        "analyses": [
            {
                "id": a.id,
                "created_at": a.created_at,
                "file_name": a.file_name,
                "document_type": a.document_type,
                "overall_quality_score": a.overall_quality_score,
                "overall_maturity_score": a.overall_maturity_score,
                "compliance_percentage": a.compliance_percentage
            }
            for a in analyses
        ]
    }

@router.delete("/analysis/{analysis_id}")
async def delete_analysis(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """Delete analysis"""
    analysis = db.query(ADRAnalysis).filter(ADRAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    db.delete(analysis)
    db.commit()
    
    return {"status": "deleted"}
