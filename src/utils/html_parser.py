from bs4 import BeautifulSoup
import datetime
from src.models.card_model import Card, Link, StartupPageModel

class HtmlParser:
    """Utility class for parsing and generating HTML for the Startup Page."""
    
    @staticmethod
    def parse_html(html_content):
        """Parse HTML content and return a StartupPageModel instance."""
        soup = BeautifulSoup(html_content, 'lxml')
        model = StartupPageModel()
        
        # Extract CSS styles
        style_tag = soup.find('style')
        if style_tag:
            model.css_styles = style_tag.string
        
        # Extract last updated date
        footer = soup.find('footer')
        if footer:
            last_updated_text = footer.get_text()
            if 'Last updated:' in last_updated_text:
                model.last_updated = last_updated_text.split('Last updated:')[1].strip()
        
        # Extract cards (sections)
        for section in soup.select('main.main-grid > section.card'):
            title_elem = section.select_one('h2.card-title')
            if title_elem:
                title = title_elem.get_text().strip()
                card = Card(title=title)
                
                # Extract links from the main link-grid
                for link_item in section.select('div.link-grid > div.link-item'):
                    a_tag = link_item.find('a')
                    if a_tag:
                        name = a_tag.get_text().strip()
                        url = a_tag.get('href', '')
                        card.add_link(Link(name=name, url=url))
                
                # Handle subsections (nested link-grids)
                subsection_grids = section.select('div.link-grid[style="margin-top: 1rem;"]')
                if subsection_grids:
                    # For simplicity, treating all additional link-grids as a single subsection
                    # In a full implementation, would need to handle proper subsection titles
                    subsection_title = "Additional Links"
                    for link_item in subsection_grids[0].select('div.link-item'):
                        a_tag = link_item.find('a')
                        if a_tag:
                            name = a_tag.get_text().strip()
                            url = a_tag.get('href', '')
                            card.add_subsection_link(subsection_title, Link(name=name, url=url))
                
                model.add_card(card)
        
        return model
    
    @staticmethod
    def generate_html(model):
        """Generate HTML content from a StartupPageModel instance."""
        # Define our masonry layout CSS
        masonry_css = """
/* Masonry-style layout for cards */
.main-grid {
    column-count: 3;
    column-gap: 1rem;
}

.card {
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 0.25rem;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
    break-inside: avoid;
    display: inline-block;
    width: 100%;
}

/* Media queries for responsive design */
@media (max-width: 992px) {
    .main-grid {
        column-count: 2;
    }
}

@media (max-width: 768px) {
    .main-grid {
        column-count: 1;
    }
}
"""
    
        # If we have existing CSS, force our masonry layout
        if model.css_styles:
            # Replace the original CSS with our modified version
            # This is a simple approach - in a production environment, 
            # a more sophisticated CSS parser would be better
            
            # First, try to find and remove existing main-grid and card style blocks
            import re
            
            # Remove existing .main-grid and .card style blocks
            model.css_styles = re.sub(r'\.main-grid\s*\{[^}]*\}', '', model.css_styles)
            model.css_styles = re.sub(r'\.card\s*\{[^}]*\}', '', model.css_styles)
            
            # If media queries for main-grid exist, remove them too
            model.css_styles = re.sub(r'@media[^{]*\{[^{]*\.main-grid\s*\{[^}]*\}[^}]*\}', '', model.css_styles)
            
            # Add our masonry CSS at the end
            model.css_styles += masonry_css
        
        if not model.css_styles:
            model.css_styles = """
:root {
    /* Light mode variables (default) - subdued version */
    --background: #e8e8e8;
    --text: #212529;
    --links: #0d6efd;
    --link-hover: #0a58ca;
    --card-bg: #f5f5f5;
    --heading-bg: #e5e5e5;
    --border-color: #d5d5d5;
    --secondary-bg: #e5e5e5;
}

/* Dark mode variables */
.dark-mode {
    --background: #212529;
    --text: #e9ecef;
    --links: #6ea8fe;
    --link-hover: #8bb9fe;
    --card-bg: #343a40;
    --heading-bg: #495057;
    --border-color: #495057;
    --secondary-bg: #343a40;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Helvetica', Arial, sans-serif;
    background-color: var(--background);
    color: var(--text);
    line-height: 1.6;
    transition: background-color 0.3s, color 0.3s;
    padding: 1rem;
    max-width: 1400px;
    margin: 0 auto;
}

a {
    color: var(--links);
    text-decoration: none;
    font-weight: bold;
    transition: color 0.2s;
}

a:hover {
    color: var(--link-hover);
    text-decoration: underline;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    gap: 1rem;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.header-center {
    font-size: 1.75rem;
    font-weight: bold;
    text-align: center;
    flex-grow: 1;
}

.header-right {
    text-align: right;
    font-size: 0.9rem;
}

.dark-mode-toggle {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
}

.dark-mode-toggle input {
    cursor: pointer;
    width: 1.25rem;
    height: 1.25rem;
}

/* Masonry-style layout for cards */
.main-grid {
    column-count: 3;
    column-gap: 1rem;
}

.card {
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 0.25rem;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
    break-inside: avoid;
    display: inline-block;
    width: 100%;
}

.card-title {
    font-size: 1.25rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1rem;
    padding: 0.5rem;
    background-color: var(--heading-bg);
    border-radius: 0.25rem;
}

.link-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
    gap: 0.5rem;
}

.link-item {
    padding: 0.5rem;
    text-align: center;
    background-color: var(--secondary-bg);
    border-radius: 0.25rem;
    transition: transform 0.2s, box-shadow 0.2s;
}

.link-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.link-group {
    margin-bottom: 1rem;
}

.link-group h3 {
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
    text-align: center;
}

.info-text {
    text-align: center;
    font-size: 0.9rem;
    margin: 0.5rem 0;
}

/* Media queries for responsive design */
@media (max-width: 992px) {
    .main-grid {
        column-count: 2;
    }
}

@media (max-width: 768px) {
    .header {
        flex-direction: column;
        text-align: center;
    }
    
    .header-left, .header-right {
        width: 100%;
        text-align: center;
    }
    
    .main-grid {
        column-count: 1;
    }
}

footer {
    margin-top: 2rem;
    padding: 1rem;
    border-top: 1px solid var(--border-color);
    font-size: 0.9rem;
}

.footer-content {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
}

.footer-left {
    text-align: left;
    flex: 0 0 auto; /* Don't allow this to grow or shrink */
    margin-right: 1rem;
}

.footer-center {
    text-align: center;
    flex: 1; /* Let this grow to take remaining space */
    margin: 0 auto; /* Center it */
}

.new-tab-toggle {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    white-space: nowrap; /* Keep label on one line */
}

.new-tab-toggle input {
    cursor: pointer;
    width: 1.25rem;
    height: 1.25rem;
}

/* Media query adjustment for footer on small screens */
@media (max-width: 768px) {
    .footer-content {
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }
    
    .footer-left {
        margin-right: 0;
    }
    
    .footer-left, .footer-center {
        width: 100%;
        text-align: center;
    }
}
"""
        
        template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JAU's Startup Page NG</title>
    <style>
{model.css_styles}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-left">
            <div class="dark-mode-toggle">
                <label for="darkModeToggle">Dark Mode:</label>
                <input type="checkbox" id="darkModeToggle">
            </div>
            <div>
                <a href="https://github.com/juren53/JAUs-Startup-Page/commits/main">History</a>
                &nbsp;&nbsp;&nbsp;
                <a href="about:restartrequired">Refresh Firefox</a>
            </div>
        </div>
        <div class="header-center">JAU's Startup Page</div>
        <div class="header-right">Updated: {datetime.datetime.now().strftime('%A, %Y-%m-%d %H:%M')}</div>
    </header>

    <main class="main-grid">
"""

        # Add each card section
        for card in model.cards:
            template += f"""        <!-- {card.title} Section -->
        <section class="card">
            <h2 class="card-title">{card.title}</h2>
            <div class="link-grid">
"""
            
            # Add main links
            for link in card.links:
                # Build inline style if needed
                style_attr = ""
                if hasattr(link, 'font_size') and link.font_size or hasattr(link, 'font_color') and link.font_color:
                    style = ""
                    if hasattr(link, 'font_size') and link.font_size:
                        style += f"font-size: {link.font_size}; "
                    if hasattr(link, 'font_color') and link.font_color:
                        style += f"color: {link.font_color}; "
                    style_attr = f' style="{style.strip()}"'
                
                template += f"""                <div class="link-item">
                    <a href="{link.url}"{style_attr}>{link.name}</a>
                </div>
"""
            
            template += "            </div>\n"
            
            # Add subsection links
            if card.subsections:
                for subsection_title, links in card.subsections.items():
                    if links:
                        template += f"""            <div class="link-grid" style="margin-top: 1rem;">
"""
                        for link in links:
                            # Build inline style if needed
                            style_attr = ""
                            if hasattr(link, 'font_size') and link.font_size or hasattr(link, 'font_color') and link.font_color:
                                style = ""
                                if hasattr(link, 'font_size') and link.font_size:
                                    style += f"font-size: {link.font_size}; "
                                if hasattr(link, 'font_color') and link.font_color:
                                    style += f"color: {link.font_color}; "
                                style_attr = f' style="{style.strip()}"'
                            
                            template += f"""                <div class="link-item">
                    <a href="{link.url}"{style_attr}>{link.name}</a>
                </div>
"""
                        template += "            </div>\n"
            
            template += "        </section>\n\n"
        
        # Add footer and closing tags
        template += f"""    </main>

    <footer>
        <div class="footer-content">
            <div class="footer-left">
                <div class="new-tab-toggle">
                    <label for="newTabToggle">Open links in new tab:</label>
                    <input type="checkbox" id="newTabToggle">
                </div>
            </div>
            <div class="footer-center">
                <p>JAU's Startup Page &copy; {datetime.datetime.now().year} | Last updated: {datetime.datetime.now().strftime('%A, %B %d, %Y')}</p>
            </div>
        </div>
    </footer>

    <script>
        // Handle Dark Mode toggle
        const darkModeToggle = document.getElementById('darkModeToggle');
        const body = document.body;

        // Check for saved preference
        if (localStorage.getItem('darkMode') === 'enabled') {{
            body.classList.add('dark-mode');
            darkModeToggle.checked = true;
        }}

        // Toggle dark mode
        darkModeToggle.addEventListener('change', function() {{
            if (this.checked) {{
                body.classList.add('dark-mode');
                localStorage.setItem('darkMode', 'enabled');
            }} else {{
                body.classList.remove('dark-mode');
                localStorage.setItem('darkMode', 'disabled');
            }}
        }});

        // Handle New Tab toggle
        const newTabToggle = document.getElementById('newTabToggle');
        const allLinks = document.getElementsByTagName('a');
        
        // Check for saved new tab preference
        if (localStorage.getItem('newTabMode') === 'enabled') {{
            newTabToggle.checked = true;
            // Apply target="_blank" to all links
            Array.from(allLinks).forEach(link => {{
                if (!link.getAttribute('href').startsWith('#')) {{
                    link.setAttribute('target', '_blank');
                    link.setAttribute('rel', 'noopener noreferrer');
                }}
            }});
        }}
        
        // Toggle new tab mode
        newTabToggle.addEventListener('change', function() {{
            if (this.checked) {{
                // Open links in new tab
                Array.from(allLinks).forEach(link => {{
                    if (!link.getAttribute('href').startsWith('#')) {{
                        link.setAttribute('target', '_blank');
                        link.setAttribute('rel', 'noopener noreferrer');
                    }}
                }});
                localStorage.setItem('newTabMode', 'enabled');
            }} else {{
                // Open links in same tab
                Array.from(allLinks).forEach(link => {{
                    link.removeAttribute('target');
                    link.removeAttribute('rel');
                }});
                localStorage.setItem('newTabMode', 'disabled');
            }}
        }});
    </script>
</body>
</html>
"""
        
        return template

    @staticmethod
    def load_from_file(file_path):
        """Load HTML from file and parse it."""
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return HtmlParser.parse_html(html_content)
    
    @staticmethod
    def save_to_file(model, file_path):
        """Generate HTML from model and save to file."""
        html_content = HtmlParser.generate_html(model)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

