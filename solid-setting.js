// JavaScript to support the collapsible sections and compact mode toggle

// Function to initialize collapsible sections
function initCollapsibleSections() {
    const headers = document.querySelectorAll('.collapsible-header');
    
    headers.forEach(header => {
        header.addEventListener('click', function() {
            this.classList.toggle('collapsed');
            const content = this.nextElementSibling;
            content.classList.toggle('collapsed');
            
            // Save state to localStorage
            const sectionId = this.parentElement.id;
            if (sectionId) {
                localStorage.setItem(
                    `section-${sectionId}-collapsed`, 
                    this.classList.contains('collapsed')
                );
            }
        });
        
        // Restore state from localStorage if available
        const sectionId = header.parentElement.id;
        if (sectionId) {
            const isCollapsed = localStorage.getItem(`section-${sectionId}-collapsed`) === 'true';
            if (isCollapsed) {
                header.classList.add('collapsed');
                header.nextElementSibling.classList.add('collapsed');
            }
        }
    });
}

// Function to initialize ultra-compact mode toggle
function initCompactToggle() {
    const toggle = document.querySelector('.compact-toggle');
    if (toggle) {
        toggle.addEventListener('click', function() {
            document.body.classList.toggle('ultra-compact');
            
            // Save state to localStorage
            localStorage.setItem(
                'ultra-compact-mode',
                document.body.classList.contains('ultra-compact')
            );
            
            // Update button text
            this.textContent = document.body.classList.contains('ultra-compact') 
                ? 'Normal View' 
                : 'Compact View';
        });
        
        // Restore state from localStorage if available
        const isCompact = localStorage.getItem('ultra-compact-mode') === 'true';
        if (isCompact) {
            document.body.classList.add('ultra-compact');
            toggle.textContent = 'Normal View';
        }
    }
}

// Initialize everything when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initCollapsibleSections();
    initCompactToggle();
});

