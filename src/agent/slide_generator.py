"""
Slide Generator Module

Handles the generation of individual slides from text descriptions,
content structuring, and speaker notes generation.
"""

from typing import List, Dict, Any, Optional
import logging
import re


class SlideGenerator:
    """
    Generates slides from text descriptions and content.
    """
    
    def __init__(self):
        """Initialize the SlideGenerator."""
        self.logger = logging.getLogger(__name__)
        self.slide_templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load slide templates from configuration."""
        return {
            'title': {
                'layout': 'title_slide',
                'content_type': 'text',
            },
            'content': {
                'layout': 'bullet_points',
                'content_type': 'text',
            },
            'chart': {
                'layout': 'chart_slide',
                'content_type': 'visualization',
            },
            'comparison': {
                'layout': 'two_column',
                'content_type': 'text',
            },
        }
    
    def generate_slides_from_text(
        self,
        title: str,
        sections: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate slides from text descriptions.
        
        Args:
            title: Presentation title
            sections: List of section descriptions
            
        Returns:
            List of slide dictionaries
        """
        slides = []
        
        # Create title slide
        title_slide = {
            'id': 0,
            'title': title,
            'type': 'title',
            'content': {
                'heading': title,
                'subheading': 'Auto-generated Presentation',
            },
            'layout': self.slide_templates['title']['layout'],
        }
        slides.append(title_slide)
        
        # Create content slides from sections
        for i, section in enumerate(sections, 1):
            slide = self._parse_section_to_slide(section, slide_id=i)
            slides.append(slide)
        
        self.logger.info(f"Generated {len(slides)} slides from {len(sections)} sections")
        return slides
    
    def _parse_section_to_slide(
        self,
        section: str,
        slide_id: int
    ) -> Dict[str, Any]:
        """
        Parse a text section into a slide.
        
        Args:
            section: Section text
            slide_id: Slide ID
            
        Returns:
            Slide dictionary
        """
        # Extract title (first line or first sentence)
        lines = section.strip().split('\n')
        title = lines[0].strip()
        
        # Extract bullet points
        bullet_points = []
        for line in lines[1:]:
            line = line.strip()
            if line and not line.startswith('#'):
                bullet_points.append(line)
        
        slide = {
            'id': slide_id,
            'title': title,
            'type': 'content',
            'content': {
                'heading': title,
                'bullet_points': bullet_points if bullet_points else [section],
            },
            'layout': self.slide_templates['content']['layout'],
        }
        
        return slide
    
    def generate_speaker_notes(self, slide: Dict[str, Any]) -> str:
        """
        Generate speaker notes for a slide.
        
        Args:
            slide: Slide dictionary
            
        Returns:
            Speaker notes text
        """
        notes = []
        
        # Add title context
        if 'title' in slide:
            notes.append(f"Slide: {slide['title']}\n")
        
        # Add content context
        content = slide.get('content', {})
        if isinstance(content, dict):
            if 'bullet_points' in content:
                notes.append("Key points to discuss:")
                for point in content['bullet_points']:
                    notes.append(f"  - {point}")
        
        # Add chart/visualization notes if present
        if 'chart' in slide:
            notes.append("\nChart/Visualization: Present and explain the data trends.")
        
        return '\n'.join(notes)
    
    def add_speaker_notes_to_slides(
        self,
        slides: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Add speaker notes to all slides.
        
        Args:
            slides: List of slides
            
        Returns:
            Slides with speaker notes added
        """
        for slide in slides:
            slide['speaker_notes'] = self.generate_speaker_notes(slide)
        return slides
    
    def validate_slide(self, slide: Dict[str, Any]) -> bool:
        """
        Validate slide structure.
        
        Args:
            slide: Slide dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ['id', 'title', 'type', 'content', 'layout']
        return all(field in slide for field in required_fields)
    
    def get_slide_statistics(self, slides: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about the slides.
        
        Args:
            slides: List of slides
            
        Returns:
            Statistics dictionary
        """
        total_slides = len(slides)
        slide_types = {}
        total_content_length = 0
        
        for slide in slides:
            slide_type = slide.get('type', 'unknown')
            slide_types[slide_type] = slide_types.get(slide_type, 0) + 1
            
            # Count content words
            content = str(slide.get('content', ''))
            total_content_length += len(content.split())
        
        return {
            'total_slides': total_slides,
            'slide_types': slide_types,
            'average_content_length': total_content_length / total_slides if total_slides > 0 else 0,
        }