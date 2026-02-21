"""
Data Fetcher Module

Handles fetching data from various sources (CSV, Excel, APIs, databases)
and preparing it for use in presentations.
"""

from typing import Dict, List, Any, Optional
import logging
import os
from pathlib import Path


class DataFetcher:
    """
    Fetches data from various sources for presentation integration.
    """
    
    def __init__(self):
        """Initialize the DataFetcher."""
        self.logger = logging.getLogger(__name__)
        self.cached_data = {}
    
    def fetch_data(self, source: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Fetch data from various sources.
        
        Args:
            source: Data source (file path, URL, or connection string)
            **kwargs: Additional parameters specific to the source type
            
        Returns:
            Data dictionary or None if fetch failed
        """
        # Check if data is already cached
        if source in self.cached_data:
            self.logger.info(f"Using cached data from {source}")
            return self.cached_data[source]
        
        # Determine source type and fetch accordingly
        if source.startswith('http://') or source.startswith('https://'):
            return self._fetch_from_url(source, **kwargs)
        elif source.endswith('.csv'):
            return self._fetch_from_csv(source, **kwargs)
        elif source.endswith(('.xlsx', '.xls')):
            return self._fetch_from_excel(source, **kwargs)
        elif source.endswith('.json'):
            return self._fetch_from_json(source, **kwargs)
        else:
            self.logger.error(f"Unsupported data source format: {source}")
            return None
    
    def _fetch_from_csv(self, filepath: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Fetch data from CSV file.
        
        Args:
            filepath: Path to CSV file
            **kwargs: Additional parameters (e.g., sheet_name)
            
        Returns:
            Data dictionary
        """
        try:
            import pandas as pd
            
            if not os.path.exists(filepath):
                self.logger.error(f"CSV file not found: {filepath}")
                return None
            
            df = pd.read_csv(filepath, **kwargs)
            data = {
                'source': filepath,
                'type': 'csv',
                'dataframe': df,
                'columns': df.columns.tolist(),
                'rows': df.shape[0],
                'data': df.to_dict('records'),
            }
            
            self.cached_data[filepath] = data
            self.logger.info(f"Fetched CSV data from {filepath}: {df.shape[0]} rows, {df.shape[1]} columns")
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching CSV data from {filepath}: {str(e)}")
            return None
    
    def _fetch_from_excel(self, filepath: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Fetch data from Excel file.
        
        Args:
            filepath: Path to Excel file
            **kwargs: Additional parameters (e.g., sheet_name)
            
        Returns:
            Data dictionary
        """
        try:
            import pandas as pd
            
            if not os.path.exists(filepath):
                self.logger.error(f"Excel file not found: {filepath}")
                return None
            
            sheet_name = kwargs.get('sheet_name', 0)
            df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)
            data = {
                'source': filepath,
                'type': 'excel',
                'dataframe': df,
                'columns': df.columns.tolist(),
                'rows': df.shape[0],
                'data': df.to_dict('records'),
                'sheet_name': sheet_name,
            }
            
            self.cached_data[filepath] = data
            self.logger.info(f"Fetched Excel data from {filepath}: {df.shape[0]} rows, {df.shape[1]} columns")
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching Excel data from {filepath}: {str(e)}")
            return None
    
    def _fetch_from_json(self, filepath: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Fetch data from JSON file.
        
        Args:
            filepath: Path to JSON file
            **kwargs: Additional parameters
            
        Returns:
            Data dictionary
        """
        try:
            import json
            
            if not os.path.exists(filepath):
                self.logger.error(f"JSON file not found: {filepath}")
                return None
            
            with open(filepath, 'r') as f:
                json_data = json.load(f)
            
            data = {
                'source': filepath,
                'type': 'json',
                'data': json_data,
            }
            
            self.cached_data[filepath] = data
            self.logger.info(f"Fetched JSON data from {filepath}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching JSON data from {filepath}: {str(e)}")
            return None
    
    def _fetch_from_url(self, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Fetch data from URL (API endpoint).
        
        Args:
            url: URL to fetch data from
            **kwargs: Additional parameters (headers, params, etc.)
            
        Returns:
            Data dictionary
        """
        try:
            import requests
            
            response = requests.get(url, timeout=10, **kwargs)
            response.raise_for_status()
            
            data = {
                'source': url,
                'type': 'api',
                'status_code': response.status_code,
                'data': response.json(),
            }
            
            self.cached_data[url] = data
            self.logger.info(f"Fetched data from URL: {url}")
            return data
            
        except Exception as e:
            self.logger.error(f"Error fetching data from URL {url}: {str(e)}")
            return None
    
    def get_columns(self, data: Dict[str, Any]) -> Optional[List[str]]:
        """
        Get column names from data.
        
        Args:
            data: Data dictionary
            
        Returns:
            List of column names
        """
        return data.get('columns')
    
    def get_dataframe(self, data: Dict[str, Any]):
        """
        Get pandas DataFrame from data.
        
        Args:
            data: Data dictionary
            
        Returns:
            Pandas DataFrame or None
        """
        return data.get('dataframe')
    
    def clear_cache(self):
        """Clear all cached data."""
        self.cached_data.clear()
        self.logger.info("Cleared data cache")
