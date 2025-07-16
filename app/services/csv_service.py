"""
CSV service for reading sales data.
Author: Victor Velazquez - Invntio SRL
"""

import csv
import os
from typing import List
from app.models.sales import SalesItem, SalesReport
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class CSVService:
    """Service for handling CSV operations."""
    
    @staticmethod
    def read_sales_data(filename: str = "ventas.csv") -> SalesReport:
        """
        Read sales data from CSV file.
        
        Args:
            filename: Name of the CSV file
            
        Returns:
            SalesReport object with parsed data
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If CSV data is invalid
        """
        filepath = os.path.join(settings.DATA_DIR, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        
        items = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Handle different possible column names
                        product = row.get('Producto') or row.get('Product', '').strip()
                        quantity = int(row.get('Cantidad') or row.get('Quantity', 0))
                        price = float(row.get('Precio') or row.get('Price', 0))
                        
                        if not product:
                            logger.warning(f"Empty product name in row {row_num}")
                            continue
                            
                        item = SalesItem(
                            product=product,
                            quantity=quantity,
                            price=price
                        )
                        items.append(item)
                        
                    except (ValueError, TypeError) as e:
                        logger.error(f"Invalid data in row {row_num}: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            raise ValueError(f"Failed to read CSV file: {e}")
        
        if not items:
            raise ValueError("No valid sales data found in CSV file")
        
        return SalesReport(items=items)