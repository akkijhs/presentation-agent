"""
Layout Suggester Module

Recommends optimal slide layouts and designs based on content type
and presentation context.
"""

from typing import Dict, List, Any, Optional
import logging


class LayoutSuggester:
    """
    Suggests optimal slide layouts based on content analysis.
    """
    
    def __init__(self):
        """Initialize the LayoutSuggester."""
        self.logger = logging.getLogger(__name__)
        self.layouts = self._load_layouts()
    
    def _load_layouts(self) -> Dict[str, Dict[str, Any]]:
        """Load available slide layouts."""
        return {
            'title_slide': {
                'name': 'Title Slide',
                'description': 'Large title and subtitle',
                'elements': ['title', 'subtitle'],
                'zones': {
                    'title': {'position': 'top', 'size': 'large'},
                    'subtitle': {'position': 'center', 'size': 'medium'},
                },
            },
            'bullet_points': {
                'name': 'Bullet Points',
                'description': 'Title with bullet points',
                'elements': ['title', 'bullet_points'],
                'zones': {
                    'title': {'position': 'top', 'size': 'medium'},
                    'content': {'position': 'center', 'size': 'large'},
                },
            },
            'chart_slide': {
                'name': 'Chart/Visualization',
                'description': 'Title with chart or image',
                'elements': ['title', 'chart'],
                'zones': {
                    'title': {'position': 'top', 'size': 'small'},
                    'chart': {'position': 'center', 'size': 'large'},
                },
            },
            'two_column': {
                'name': 'Two Column',
                'description': 'Title with two columns of content',
                'elements': ['title', 'left_column', 'right_column'],
                'zones': {
                    'title': {'position': 'top', 'size': 'small'},
                    'left': {'position': 'left', 'size': 'medium'},
                    'right': {'position': 'right', 'size': 'medium'},
                },
            },
            'image_and_text': {
                'name': 'Image and Text',
                'description': 'Image on one side, text on the other',
                'elements': ['title', 'image', 'text'],
                'zones': {
                    'title': {'position': 'top', 'size': 'small'},
                    'image': {'position': 'left', 'size': 'large'},
                    'text': {'position': 'right', 'size': 'large'},
                },
            },
            'blank': {
                'name': 'Blank',
                'description': 'Completely blank slide',
                'elements': [],
                'zones': {},
            },
        }
    
    def suggest_layout(
        self,
        slide: Dict[str, Any]
    ) -> str:
        """
        Suggest a layout for a slide based on its content.
        
        Args:
            slide: Slide dictionary
            
        Returns:
            Recommended layout name
        """
        slide_type = slide.get('type', 'content')
        content = slide.get('content', {})
        
        # Title slide
        if slide_type == 'title':
            return 'title_slide'
        
        # Chart slide
        if 'chart' in slide:
            return 'chart_slide'
        
        # Two columns if content suggests it
        if isinstance(content, dict):
            if 'left_column' in content and 'right_column' in content:
                return 'two_column'
            if 'image' in content and 'text' in content:
                return 'image_and_text'
            if 'bullet_points' in content:
                return 'bullet_points'
        
        # Default to bullet points
        return 'bullet_points'
    
    def get_layout_details(self, layout_name: str) -> Optional[Dict[str, Any]]:
        """
        Get details of a specific layout.
        
        Args:
            layout_name: Name of the layout
            
        Returns:
            Layout details dictionary or None
        """
        return self.layouts.get(layout_name)
    
    def get_available_layouts(self) -> List[str]:
        """
        Get list of all available layouts.
        
        Returns:
            List of layout names
        """
        return list(self.layouts.keys())
    
    def validate_content_for_layout(
        self,
        content: Dict[str, Any],
        layout_name: str
    ) -> bool:
        """
        Validate if content fits a specific layout.
        
        Args:
            content: Content dictionary
            layout_name: Layout name
            
        Returns:
            True if content fits layout, False otherwise
        """
        layout = self.layouts.get(layout_name)
        if not layout:
            return False
        
        required_elements = layout['elements']
        content_elements = list(content.keys())
        
        # Check if all required elements are present
        return all(elem in content_elements for elem in required_elements)
    
    def recommend_modifications(
        self,
        slide: Dict[str, Any],
        layout_name: str
    ) -> List[str]:
        """
        Recommend modifications to fit a layout.
        
        Args:
            slide: Slide dictionary
            layout_name: Target layout name
            
        Returns:
            List of recommendations
        """
        layout = self.layouts.get(layout_name)
        if not layout:
            return []
        
        recommendations = []
        content = slide.get('content', {})
        required_elements = layout['elements']
        
        for element in required_elements:
            if element not in content:
                recommendations.append(f"Add {element} to content")
        
        return recommendations
    
    def get_layout_by_content_type(self, content_type: str) -> str:
        """
        Get recommended layout by content type.
        
        Args:
            content_type: Type of content (text, chart, comparison, etc.)
            
        Returns:
            Recommended layout name
        """
        mapping = {
            'text': 'bullet_points',
            'chart': 'chart_slide',
            'comparison': 'two_column',
            'image': 'image_and_text',
            'title': 'title_slide',
        }
        return mapping.get(content_type, 'bullet_points')
    
    def apply_theme(
        self,
        layout: str,
        theme: str
    ) -> Dict[str, Any]:
        """
        Apply a theme to a layout.
        
        Args:
            layout: Layout name
            theme: Theme name
            
        Returns:
            Theme-customized layout dictionary
        """
        layout_dict = self.get_layout_details(layout)
        if not layout_dict:
            return {}
        
        # Deep copy layout
        themed_layout = dict(layout_dict)
        
        # Apply theme customizations
        theme_overrides = self._get_theme_overrides(theme)
        if theme_overrides:
            themed_layout['theme'] = theme
            themed_layout['overrides'] = theme_overrides
        
        return themed_layout
    
    def _get_theme_overrides(self, theme: str) -> Dict[str, Any]:
        """
        Get theme-specific overrides.
        
        Args:
            theme: Theme name
            
        Returns:
            Theme overrides dictionary
        """
        theme_config = {
            'default': {
                'colors': ['#1f77b4', '#ff7f0e'],
                'font': 'Arial',
            },
            'business': {
                'colors': ['#003366', '#006699'],
                'font': 'Calibri',
            },
            'minimal': {
                'colors': ['#000000', '#ffffff'],
                'font': 'Helvetica',
            },
        }
        return theme_config.get(theme, {})
