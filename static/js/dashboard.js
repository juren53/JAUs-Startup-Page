// Theme management
class ThemeManager {
    constructor() {
        this.themeToggle = document.getElementById('theme-toggle');
        this.body = document.body;
        
        // Initialize theme from localStorage or default to light
        const savedTheme = localStorage.getItem('theme') || 'light';
        this.setTheme(savedTheme);
        
        // Set up event listeners
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
    }
    
    setTheme(theme) {
        this.body.classList.remove('light-theme', 'dark-theme');
        this.body.classList.add(`${theme}-theme`);
        this.themeToggle.textContent = theme === 'light' ? '🌜' : '🌞';
        localStorage.setItem('theme', theme);
    }
    
    toggleTheme() {
        const newTheme = this.body.classList.contains('light-theme') ? 'dark' : 'light';
        this.setTheme(newTheme);
    }
}

// Section management
class SectionManager {
    constructor() {
        this.sections = document.querySelectorAll('.section');
        this.setupSections();
    }
    
    setupSections() {
        this.sections.forEach(section => {
            const header = section.querySelector('.section-header');
            const content = section.querySelector('.section-content');
            const icon = header.querySelector('.collapse-icon');
            
            // Get initial state from localStorage or data attribute
            const sectionId = section.getAttribute('data-section-id');
            const isCollapsed = localStorage.getItem(`section-${sectionId}`) === 'collapsed' ||
                              section.getAttribute('data-collapsed') === 'true';
            
            // Set initial state
            if (isCollapsed) {
                content.style.display = 'none';
                icon.textContent = '▼';
            }
            
            header.addEventListener('click', () => this.toggleSection(section));
        });
    }
    
    toggleSection(section) {
        const content = section.querySelector('.section-content');
        const icon = section.querySelector('.collapse-icon');
        const sectionId = section.getAttribute('data-section-id');
        
        // Toggle with animation
        if (content.style.display === 'none') {
            content.style.display = 'block';
            content.style.maxHeight = content.scrollHeight + 'px';
            icon.textContent = '▲';
            localStorage.setItem(`section-${sectionId}`, 'expanded');
        } else {
            content.style.maxHeight = '0';
            icon.textContent = '▼';
            localStorage.setItem(`section-${sectionId}`, 'collapsed');
            // Wait for animation before hiding
            setTimeout(() => {
                content.style.display = 'none';
            }, 300);
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
    window.sectionManager = new SectionManager();
});
