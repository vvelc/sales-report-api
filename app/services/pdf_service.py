"""
PDF service for generating sales reports.
Author: Victor Velazquez - Invntio SRL
"""

import os
from typing import List
from datetime import datetime
from app.models.sales import SalesReport, ReportResponse
from app.config.settings import settings
import logging

# Using reportlab for better compatibility
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

logger = logging.getLogger(__name__)

class PDFService:
    """Service for generating PDF reports."""
    
    @staticmethod
    def generate_sales_report(sales_data: SalesReport) -> ReportResponse:
        """
        Generate PDF sales report.
        
        Args:
            sales_data: SalesReport object with sales data
            
        Returns:
            ReportResponse with report details
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sales_report_{timestamp}.pdf"
        filepath = os.path.join(settings.REPORTS_DIR, filename)
        
        # Ensure reports directory exists
        os.makedirs(settings.REPORTS_DIR, exist_ok=True)
        
        try:
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            
            # Get styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=colors.darkblue
            )
            
            # Title
            title = Paragraph("Sales Report - Invntio SRL", title_style)
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Summary
            summary_data = [
                ['Total Items Sold:', str(sales_data.total_items)],
                ['Total Revenue:', f"${sales_data.total_revenue:,.2f}"],
                ['Report Generated:', sales_data.generated_at.strftime("%Y-%m-%d %H:%M:%S")]
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 30))
            
            # Sales data table
            table_data = [['Product', 'Quantity', 'Unit Price', 'Total']]
            
            for item in sales_data.items:
                table_data.append([
                    item.product,
                    str(item.quantity),
                    f"${item.price:.2f}",
                    f"${item.total:.2f}"
                ])
            
            # Create table
            table = Table(table_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch])
            table.setStyle(TableStyle([
                # Header style
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                
                # Data style
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                
                # Grid
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(table)
            story.append(Spacer(1, 30))
            
            # Add chart
            chart = PDFService._create_sales_chart(sales_data)
            story.append(chart)
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"PDF report generated successfully: {filename}")
            
            return ReportResponse(
                filename=filename,
                generated_at=sales_data.generated_at,
                items_count=len(sales_data.items),
                total_revenue=sales_data.total_revenue,
                download_url=f"/api/v1/reports/download/{filename}"
            )
            
        except Exception as e:
            logger.error(f"Error generating PDF report: {e}")
            raise ValueError(f"Failed to generate PDF report: {e}")
    
    @staticmethod
    def _create_sales_chart(sales_data: SalesReport) -> Drawing:
        """Create a bar chart for sales data."""
        drawing = Drawing(400, 300)
        
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.height = 200
        chart.width = 300
        
        # Prepare data
        products = [item.product[:15] for item in sales_data.items]  # Truncate long names
        quantities = [item.quantity for item in sales_data.items]
        
        chart.data = [quantities]
        chart.categoryAxis.categoryNames = products
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(quantities) * 1.2 if quantities else 1
        
        # Styling
        chart.bars[0].fillColor = colors.darkblue
        chart.categoryAxis.labels.boxAnchor = 'ne'
        chart.categoryAxis.labels.dx = 8
        chart.categoryAxis.labels.dy = -2
        chart.categoryAxis.labels.angle = 45
        chart.categoryAxis.labels.fontSize = 8
        
        drawing.add(chart)
        
        return drawing