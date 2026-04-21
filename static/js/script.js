// Simple cart functionality
document.addEventListener('DOMContentLoaded', function() {
    // Fetch and display products
    fetchAndDisplayProducts();

    // Fetch and display categories
    fetchAndDisplayCategories();

    // Add to cart buttons event listener (will be attached to dynamically added buttons)
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('add-to-cart')) {
            const productCard = e.target.closest('.product-card');
            const productName = productCard.querySelector('.product-name')?.textContent ||
                               productCard.querySelector('.product-info h3')?.textContent ||
                               'this item';

            // Visual feedback
            const originalText = e.target.textContent;
            e.target.textContent = 'Added!';
            e.target.style.backgroundColor = '#27ae60';

            setTimeout(() => {
                e.target.textContent = originalText;
                e.target.style.backgroundColor = '';
            }, 1000);

            // Show alert
            alert(`Added ${productName} to cart!`);
        }
    });

    // Search functionality
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const productCards = document.querySelectorAll('.product-card');

            productCards.forEach(card => {
                const productName = card.querySelector('.product-name')?.textContent.toLowerCase() ||
                                   card.querySelector('.product-info h3')?.textContent.toLowerCase() || '';

                if (productName.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Mobile menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }
});

async function fetchAndDisplayProducts() {
    try {
        const response = await fetch('/api/products');
        const products = await response.json();

        const container = document.getElementById('products-container');
        let productsHTML = '<h2>Featured Products</h2>';
        productsHTML += '<div class="product-grid">';

        products.forEach(product => {
            productsHTML += `
                <div class="product-card">
                    <img src="${product.image}" alt="${product.name}" class="product-image">
                    <div class="product-info">
                        <h3>${product.name}</h3>
                        <p class="price">$${product.price.toFixed(2)}</p>
                        <p class="product-description">${product.description}</p>
                        <button class="add-to-cart">Add to Cart</button>
                    </div>
                </div>
            `;
        });

        productsHTML += '</div>';
        container.innerHTML = productsHTML;
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

async function fetchAndDisplayCategories() {
    try {
        const response = await fetch('/api/categories');
        const categories = await response.json();

        const container = document.getElementById('categories-container');
        let categoriesHTML = '<div class="categories-grid">';

        categories.forEach(category => {
            categoriesHTML += `
                <div class="category-card">
                    <img src="${category.image}" alt="${category.name}">
                    <h3>${category.name}</h3>
                </div>
            `;
        });

        categoriesHTML += '</div>';
        container.innerHTML = categoriesHTML;
    } catch (error) {
        console.error('Error fetching categories:', error);
    }
}