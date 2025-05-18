#!/usr/bin/env python3

import yaml
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

class DashboardGenerator:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load and parse the YAML configuration file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _generate_css_variables(self) -> str:
        """Generate CSS variables for both light and dark themes."""
        css_vars = []
        
        # Light theme variables
        for key, value in self.config['theme']['light'].items():
            # Convert underscores to hyphens in variable names
            css_key = key.replace('_', '-')
            css_vars.append(f"    --{css_key}-light: {value};")
            
        # Dark theme variables
        for key, value in self.config['theme']['dark'].items():
            # Convert underscores to hyphens in variable names
            css_key = key.replace('_', '-')
            css_vars.append(f"    --{css_key}-dark: {value};")
            
        # Default theme (light)
        css_vars.append("\n    /* Default theme variables */")
        for key in self.config['theme']['light'].keys():
            # Convert underscores to hyphens in variable names
            css_key = key.replace('_', '-')
            css_vars.append(f"    --{css_key}: var(--{css_key}-light);")
            
        return "\n".join([":root {"] + css_vars + ["}"])
    
    def _generate_link_buttons(self, links: List[Dict[str, str]]) -> str:
        """Generate HTML for a grid of link buttons."""
        grid_html = ['<div class="link-grid">']
        
        for link in links:
            name = link['name']
            url = link['url']
            button_html = f'    <a href="{url}" class="link-button" target="_blank">{name}</a>'
            grid_html.append(button_html)
            
        grid_html.append('</div>')
        return "\n".join(grid_html)
    
    def _generate_subsection(self, title: str, content: Dict[str, Any]) -> str:
        """Generate HTML for a subsection with title and content."""
        html_parts = [
            f'<div class="subsection">',
            f'    <h3 class="subsection-title">{title}</h3>'
        ]
        
        if 'links' in content:
            html_parts.append(self._generate_link_buttons(content['links']))
        
        html_parts.append('</div>')
        return "\n".join(html_parts)
    
    def _generate_section(self, section_id: str, section_config: Dict[str, Any]) -> str:
        """Generate HTML for a complete section with header and content."""
        icon = section_config.get('icon', '')
        title = f"{icon} {section_config['title']}" if icon else section_config['title']
        collapsed = 'true' if section_config.get('collapsed', False) else 'false'
        
        html_parts = [
            f'<div class="section" data-section-id="{section_id}" data-collapsed="{collapsed}">',
            f'    <div class="section-header">',
            f'        <span class="section-title">{title}</span>',
            f'        <span class="collapse-icon">{"▼" if collapsed == "true" else "▲"}</span>',
            f'    </div>',
            f'    <div class="section-content">'
        ]
        
        if 'links' in section_config:
            html_parts.append(self._generate_link_buttons(section_config['links']))
        elif 'subsections' in section_config:
            for subsection_id, subsection in section_config['subsections'].items():
                subsection_title = subsection.get('title', subsection_id.replace('_', ' ').title())
                html_parts.append(self._generate_subsection(subsection_title, subsection))
        
        html_parts.append('    </div>')
        html_parts.append('</div>')
        
        return "\n".join(html_parts)
    
    def _distribute_sections(self) -> Dict[str, List[str]]:
        """Distribute sections between two columns."""
        left_column = []
        right_column = []
        
        section_ids = list(self.config['sections'].keys())
        
        for i, section_id in enumerate(section_ids):
            section_config = self.config['sections'][section_id]
            section_html = self._generate_section(section_id, section_config)
            
            if i % 2 == 0:  # Even indexes go to left column
                left_column.append(section_html)
            else:  # Odd indexes go to right column
                right_column.append(section_html)
                
        return {
            'left': left_column,
            'right': right_column
        }
    
    def generate_html(self) -> str:
        """Generate the complete HTML document."""
        html_parts = []
        
        # Start HTML document
        html_parts.append("<!DOCTYPE html>")
        html_parts.append('<html lang="en">')
        
        # Head section
        head = [
            "<head>",
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '    <title>Dashboard</title>',
            '    <link rel="stylesheet" href="css/dashboard.css">',
            "    <style>",
            self._generate_css_variables(),
            "    </style>",
            "</head>"
        ]
        html_parts.extend(head)
        
        # Get sections distributed between columns
        columns = self._distribute_sections()
        
        # Body section with content
        body = [
            '<body class="light-theme">',
            '    <div id="dashboard">',
            '        <header class="header">',
            '            <h1>Dashboard</h1>',
            '            <button id="theme-toggle" class="theme-toggle">🌜</button>',
            '        </header>',
            '        <div class="columns-container">'
        ]
        
        # Left column
        body.append('            <div class="column">')
        for section in columns['left']:
            body.append('                ' + section.replace('\n', '\n                '))
        body.append('            </div>')
        
        # Right column
        body.append('            <div class="column">')
        for section in columns['right']:
            body.append('                ' + section.replace('\n', '\n                '))
        body.append('            </div>')
        
        # Close main containers
        body.extend([
            '        </div>',
            '    </div>',
            '    <script src="js/dashboard.js"></script>',
            '</body>'
        ])
        
        html_parts.extend(body)
        
        # Close HTML document
        html_parts.append('</html>')
        
        return "\n".join(html_parts)
    
    def _copy_static_files(self, output_dir: Path):
        """Copy static CSS and JavaScript files to the output directory."""
        # Create CSS directory
        css_dir = output_dir / 'css'
        css_dir.mkdir(exist_ok=True)
        
        # Create JS directory
        js_dir = output_dir / 'js'
        js_dir.mkdir(exist_ok=True)
        
        # Copy CSS file
        shutil.copy2('static/css/dashboard.css', css_dir / 'dashboard.css')
        
        # Copy JS file
        shutil.copy2('static/js/dashboard.js', js_dir / 'dashboard.js')
        
        print(f"Static files copied to {output_dir}")
    
    def generate_dashboard(self, output_path: str):
        """Generate the dashboard and save it to the specified path."""
        html_content = self.generate_html()
        
        output_file = Path(output_path)
        output_dir = output_file.parent
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy static files
        self._copy_static_files(output_dir)
        
        # Write HTML file
        output_file.write_text(html_content)
        print(f"Dashboard generated: {output_file}")

def main():
    config_path = "config.yaml"
    output_path = "output/index.html"
    
    print("Generating dashboard...")
    generator = DashboardGenerator(config_path)
    generator.generate_dashboard(output_path)
    print("\nDashboard generated successfully!")
    print(f"Open {output_path} in your browser to view it.")

if __name__ == "__main__":
    main()
