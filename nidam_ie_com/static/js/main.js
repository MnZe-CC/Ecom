// Main JavaScript for Nidam IE Commerce

document.addEventListener('DOMContentLoaded', function() {
    // Language switcher functionality
    const languageSwitcher = document.querySelector('.language-switcher');
    if (languageSwitcher) {
        languageSwitcher.addEventListener('change', function() {
            const selectedLang = this.value;
            window.location.href = `/switch-language/${selectedLang}`;
        });
    }

    // Product image gallery functionality
    const productImages = document.querySelectorAll('.product-image img');
    if (productImages.length > 0) {
        // Add click functionality to switch main image
        productImages.forEach(img => {
            img.addEventListener('click', function() {
                const mainImage = document.querySelector('.main-product-image');
                if (mainImage) {
                    mainImage.src = this.src;
                }
            });
        });
    }

    // Mobile menu toggle
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const navContainer = document.querySelector('.nav-container ul');

    if (mobileMenuButton && navContainer) {
        mobileMenuButton.addEventListener('click', function() {
            navContainer.classList.toggle('show');
        });
    }

    // Close flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s ease';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });
});

// Helper function to confirm deletions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Helper function to format currency
function formatCurrency(amount, currency = '$') {
    return currency + amount.toFixed(2);
}