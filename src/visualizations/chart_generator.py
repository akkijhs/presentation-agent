"""
Chart Generator Module

Handles generation of charts, graphs, and visualizations
for presentation slides.
"""

from typing import Dict, List, Any, Optional
import logging
from enum import Enum


class ChartType(Enum):
    """Supported chart types"""
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"
    BOX = "box"
    AREA = "area"


class ChartGenerator:
    """
    Generates charts and visualizations for presentations.
    """
    
    def __init__(self):
        """Initialize the ChartGenerator."""
        self.logger = logging.getLogger(__name__)
        self.default_theme = "default"
        self.chart_styles = self._load_chart_styles()
    
    def _load_chart_styles(self) -> Dict[str, Dict[str, Any]]:
        """Load default chart styles."""
        return {
            'default': {
                'colors': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
                'font_size': 12,
                'dpi': 100,
                'figsize': (10, 6),
            },
            'business': {
                'colors': ['#003366', '#006699', '#0099cc', '#00ccff', '#ccffff'],
                'font_size': 14,
                'dpi': 150,
                'figsize': (12, 7),
            },
            'minimal': {
                'colors': ['#000000', '#404040', '#808080', '#c0c0c0', '#ffffff'],
                'font_size': 11,
                'dpi': 100,
                'figsize': (10, 6),
            },
        }
    
    def generate_chart(
        self,
        chart_type: str,
        data: Optional[Dict[str, Any]] = None,
        theme: str = "default",
        title: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a chart.
        
        Args:
            chart_type: Type of chart (bar, line, pie, etc.)
            data: Data for the chart
            theme: Chart theme/style
            title: Chart title
            **kwargs: Additional chart-specific parameters
            
        Returns:
            Chart metadata dictionary
        """
        try:
            chart_enum = ChartType[chart_type.upper()]
        except KeyError:
            self.logger.error(f"Unsupported chart type: {chart_type}")
            return {}
        
        # Get chart style
        style = self.chart_styles.get(theme, self.chart_styles['default'])
        
        chart_config = {
            'type': chart_type,
            'title': title,
            'data': data,
            'theme': theme,
            'style': style,
            'kwargs': kwargs,
        }
        
        self.logger.info(f"Generated {chart_type} chart with theme {theme}")
        return chart_config
    
    def generate_bar_chart(
        self,
        categories: List[str],
        values: List[float],
        title: str = "Bar Chart",
        theme: str = "default",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a bar chart.
        
        Args:
            categories: Category labels
            values: Data values
            title: Chart title
            theme: Chart theme
            **kwargs: Additional parameters
            
        Returns:
            Chart metadata
        """
        data = {
            'categories': categories,
            'values': values,
        }
        return self.generate_chart('bar', data=data, theme=theme, title=title, **kwargs)
    
    def generate_line_chart(
        self,
        x_data: List[Any],
        y_data: List[float],
        title: str = "Line Chart",
        theme: str = "default",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a line chart.
        
        Args:
            x_data: X-axis data
            y_data: Y-axis data
            title: Chart title
            theme: Chart theme
            **kwargs: Additional parameters
            
        Returns:
            Chart metadata
        """
        data = {
            'x_data': x_data,
            'y_data': y_data,
        }
        return self.generate_chart('line', data=data, theme=theme, title=title, **kwargs)
    
    def generate_pie_chart(
        self,
        labels: List[str],
        values: List[float],
        title: str = "Pie Chart",
        theme: str = "default",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a pie chart.
        
        Args:
            labels: Slice labels
            values: Slice values
            title: Chart title
            theme: Chart theme
            **kwargs: Additional parameters
            
        Returns:
            Chart metadata
        """
        data = {
            'labels': labels,
            'values': values,
        }
        return self.generate_chart('pie', data=data, theme=theme, title=title, **kwargs)
    
    def generate_scatter_chart(
        self,
        x_data: List[float],
        y_data: List[float],
        title: str = "Scatter Chart",
        theme: str = "default",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a scatter chart.
        
        Args:
            x_data: X-axis data
            y_data: Y-axis data
            title: Chart title
            theme: Chart theme
            **kwargs: Additional parameters
            
        Returns:
            Chart metadata
        """
        data = {
            'x_data': x_data,
            'y_data': y_data,
        }
        return self.generate_chart('scatter', data=data, theme=theme, title=title, **kwargs)
    
    def get_supported_chart_types(self) -> List[str]:
        """
        Get list of supported chart types.
        
        Returns:
            List of chart type names
        """
        return [chart.value for chart in ChartType]
    
    def get_available_themes(self) -> List[str]:
        """
        Get list of available themes.
        
        Returns:
            List of theme names
        """
        return list(self.chart_styles.keys())
    
    def customize_chart(
        self,
        chart: Dict[str, Any],
        **custom_params
    ) -> Dict[str, Any]:
        """
        Customize an existing chart.
        
        Args:
            chart: Chart metadata
            **custom_params: Custom parameters
            
        Returns:
            Updated chart metadata
        """
        chart['kwargs'].update(custom_params)
        self.logger.info(f"Customized chart: {chart['title']}")
        return chart