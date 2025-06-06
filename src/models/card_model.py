class Link:
    """Represents a link item within a card section."""
    
    def __init__(self, name="", url="", font_size="", font_color=""):
        self.name = name
        self.url = url
        self.font_size = font_size  # Empty string means default size
        self.font_color = font_color  # Empty string means default color
    
    def __repr__(self):
        return f"Link(name='{self.name}', url='{self.url}', font_size='{self.font_size}', font_color='{self.font_color}')"


class Card:
    """Represents a card section in the startup page."""
    
    def __init__(self, title="", icon="", background_color=""):
        self.title = title
        self.icon = icon
        self.background_color = background_color  # Card background color
        self.links = []  # List of Link objects
        self.subsections = {}  # Dictionary of title -> list of Link objects
    
    def add_link(self, link):
        """Add a link to the main section of the card."""
        self.links.append(link)
    
    def add_subsection_link(self, subsection_title, link):
        """Add a link to a subsection of the card."""
        if subsection_title not in self.subsections:
            self.subsections[subsection_title] = []
        
        self.subsections[subsection_title].append(link)
    
    def remove_link(self, link):
        """Remove a link from the main section of the card."""
        if link in self.links:
            self.links.remove(link)
    
    def remove_subsection_link(self, subsection_title, link):
        """Remove a link from a subsection of the card."""
        if subsection_title in self.subsections and link in self.subsections[subsection_title]:
            self.subsections[subsection_title].remove(link)
            
            # Remove subsection if it's empty
            if not self.subsections[subsection_title]:
                del self.subsections[subsection_title]
    
    def __repr__(self):
        return f"Card(title='{self.title}', links={len(self.links)}, subsections={len(self.subsections)})"


class StartupPageModel:
    """Model representing the entire Startup Page."""
    
    def __init__(self):
        self.cards = []  # List of Card objects
        self.css_styles = ""  # CSS styles from the HTML file
        self.dark_mode_enabled = False
        self.last_updated = ""
    
    def add_card(self, card):
        """Add a card to the model."""
        self.cards.append(card)
    
    def remove_card(self, card):
        """Remove a card from the model."""
        if card in self.cards:
            self.cards.remove(card)
    
    def move_card(self, card, new_position):
        """Move a card to a new position in the list."""
        if card in self.cards:
            self.cards.remove(card)
            self.cards.insert(new_position, card)
    
    def __repr__(self):
        return f"StartupPageModel(cards={len(self.cards)})"

