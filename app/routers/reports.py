"""
Reports router for handling report generation endpoints.
Author: Victor Velazquez - Invntio SRL
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from app.services.csv_service import CSVService
from app.services.pdf_service import PDFService
from app.models.sales import ReportResponse
from app.config.settings import settings
import os
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/reports/generate", response_model=ReportResponse)
async def generate_sales_report():
    """
    Generate a PDF sales report from CSV data.
    
    Returns:
        ReportResponse with report details and download URL
    """
    try:
        # Read CSV data
        sales_data = CSVService.read_sales_data()
        
        # Generate PDF report
        report_response = PDFService.generate_sales_report(sales_data)
        
        logger.info(f"Report generated successfully: {report_response.filename}")
        return report_response
        
    except FileNotFoundError as e:
        logger.error(f"CSV file not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sales data file not found. Please ensure ventas.csv exists in the data directory."
        )
    except ValueError as e:
        logger.error(f"Invalid data: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating the report."
        )

@router.get("/reports/download/{filename}")
async def download_report(filename: str):
    """
    Download a generated PDF report.
    
    Args:
        filename: Name of the PDF file to download
        
    Returns:
        FileResponse with the PDF file
    """
    filepath = os.path.join(settings.REPORTS_DIR, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file not found."
        )
    
    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/reports/list")
async def list_reports():
    """
    List all available reports.
    
    Returns:
        List of available report files
    """
    try:
        if not os.path.exists(settings.REPORTS_DIR):
            return {"reports": []}
        
        reports = []
        for filename in os.listdir(settings.REPORTS_DIR):
            if filename.endswith('.pdf'):
                filepath = os.path.join(settings.REPORTS_DIR, filename)
                stat = os.stat(filepath)
                reports.append({
                    "filename": filename,
                    "size": stat.st_size,
                    "created_at": stat.st_ctime,
                    "download_url": f"/api/v1/reports/download/{filename}"
                })
        
        return {"reports": reports}
        
    except Exception as e:
        logger.error(f"Error listing reports: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving reports list."
        )