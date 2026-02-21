"""
Main Presentation Agent Class

This module contains the core PresentationAgent class that orchestrates
 the generation of presentations across multiple formats.
"""

from typing import List, Dict, Optional, Any
from enum import Enum
import logging

from .slide_generator import SlideGenerator
from ..data.data_fetcher import DataFetcher
from ..visualizations.chart_generator import ChartGenerator
from ..templates.layout_suggester import LayoutSuggester
from ..exporters.pptx_exporter import PowerPointExporter
from ..exporters.pdf_exporter import PDFExporter
from ..exporters.gslides_exporter import GoogleSlidesExporter
from ..exporters.html_exporter import HTMLExporter


class ExportFormat(Enum):
    """Supported export formats"""
    POWERPOINT = "powerpoint"
    PDF = "pdf"
    GOOGLE_SLIDES = "google_slides"
    HTML = "html"


class PresentationAgent:
    """
    Core presentation generation agent.
    
    This agent orchestrates the creation of presentations from text descriptions,
    data sources, and design preferences, supporting multiple export formats.
    """
    
    def __init__(self, theme: str = "default", verbose: bool = False):
        """
        Initialize the Presentation Agent.
        
        Args:
            theme: Theme/template to use for presentations
            verbose: Enable verbose logging
        """
        self.theme = theme
        self.verbose = verbose
        
        # Configure logging
        self.logger = logging.getLogger(__name__)
        if verbose:
            self.logger.setLevel(logging.DEBUG)
        
        # Initialize components
        self.slide_generator = SlideGenerator()
        self.data_fetcher = DataFetcher()
        self.chart_generator = ChartGenerator()
        self.layout_suggester = LayoutSuggester()
        
        # Initialize exporters
        self.exporters = {
            ExportFormat.POWERPOINT: PowerPointExporter(),
            ExportFormat.PDF: PDFExporter(),
            ExportFormat.GOOGLE_SLIDES: GoogleSlidesExporter(),
            ExportFormat.HTML: HTMLExporter(),
        }
        
        self.slides = []
        self.metadata = {}
        
        self.logger.info(f"PresentationAgent initialized with theme: {theme}")
    
    def create_from_text(
        self,
        title: str,
        sections: List[str],
        data_source: Optional[str] = None,
        speaker_notes: bool = True
    ) -> 'PresentationAgent':
        """
        Create presentation from text descriptions.
        
        Args:
            title: Presentation title
            sections: List of section descriptions
            data_source: Optional path to data file (CSV, Excel, etc.)
            speaker_notes: Whether to generate speaker notes
            
        Returns:
            Self for method chaining
        """
        self.logger.info(f"Creating presentation: {title}")
        
        # Set metadata
        self.metadata['title'] = title
        
        # Generate slides from text
        self.slides = self.slide_generator.generate_slides_from_text(
            title=title,
            sections=sections
        )
        
        # Load data if provided
        if data_source:
            data = self.data_fetcher.fetch_data(data_source)
            self.logger.info(f"Loaded data from {data_source}")
        
        # Suggest layouts
        for slide in self.slides:
            suggested_layout = self.layout_suggester.suggest_layout(slide)
            slide['layout'] = suggested_layout
        
        if speaker_notes:
            self._generate_speaker_notes()
        
        self.logger.info(f"Created {len(self.slides)} slides")
        return self
    
    def add_chart(
        self,
        slide_index: int,
        chart_type: str,
        data: Optional[Dict[str, Any]] = None,
        data_column: Optional[str] = None
    ) -> 'PresentationAgent':
        """
        Add a chart to a specific slide.
        
        Args:
            slide_index: Index of the slide
            chart_type: Type of chart (pie, bar, line, etc.)
            data: Optional data dictionary
            data_column: Optional column name from fetched data
            
        Returns:
            Self for method chaining
        """
        if slide_index >= len(self.slides):
            self.logger.error(f"Slide index {slide_index} out of range")
            return self
        
        chart = self.chart_generator.generate_chart(
            chart_type=chart_type,
            data=data,
            theme=self.theme
        )
        
        self.slides[slide_index]['chart'] = chart
        self.logger.info(f"Added {chart_type} chart to slide {slide_index}")
        return self
    
    def generate_speaker_notes(self) -> 'PresentationAgent':
        """Generate speaker notes for all slides."""
        self._generate_speaker_notes()
        return self
    
    def _generate_speaker_notes(self):
        """Internal method to generate speaker notes."""
        for i, slide in enumerate(self.slides):
            notes = self.slide_generator.generate_speaker_notes(slide)
            slide['speaker_notes'] = notes
        self.logger.info("Generated speaker notes for all slides")
    
    def export(
        self,
        format_type: str,
        output_path: str,
        **kwargs
    ) -> bool:
        """
        Export presentation to specified format.
        
        Args:
            format_type: Export format (powerpoint, pdf, google_slides, html)
            output_path: Output file path
            **kwargs: Additional exporter-specific arguments
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            format_enum = ExportFormat[format_type.upper()]
        except KeyError:
            self.logger.error(f"Unsupported export format: {format_type}")
            return False
        
        exporter = self.exporters.get(format_enum)
        if not exporter:
            self.logger.error(f"Exporter not found for format: {format_type}")
            return False
        
        success = exporter.export(
            slides=self.slides,
            metadata=self.metadata,
            output_path=output_path,
            theme=self.theme,
            **kwargs
        )
        
        if success:
            self.logger.info(f"Successfully exported to {output_path}")
        else:
            self.logger.error(f"Export to {output_path} failed")
        
        return success
    
    def get_slides(self) -> List[Dict[str, Any]]:
        """Get all generated slides."""
        return self.slides
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get presentation metadata."""
        return self.metadata
