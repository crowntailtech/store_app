const API_BASE_URL = "https://your-api-gateway-url.com";

// Fetch all products from the API
async function fetchProducts() {
    try {
        let response = await fetch(`${API_BASE_URL}/products`);
        return await response.json();
    } catch (error) {
        console.error("Error fetching products:", error);
        return [];
    }
}

// Load products and ensure "Add Product" card stays first
async function loadProducts() {
    try {
        let products = await fetchProducts();
        const productListDiv = document.getElementById("product-list");

        // Clear existing products but keep "Add Product" card
        productListDiv.innerHTML = `
            <div class="product-card add-card" onclick="location.href='add_product.html'">
                <i class="fas fa-plus"></i>
                <p>+</p>
            </div>
        `;

        // Append products after "Add Product" card
        products.forEach(product => {
            let productCard = document.createElement("div");
            productCard.classList.add("product-card");
            productCard.innerHTML = `
                <h3>${product.name}</h3>
                <p>Price: $${product.price} (${product.currency})</p>
                <button onclick="viewProduct('${product.id}')">View</button>
                <button onclick="editProduct('${product.id}')">Edit</button>
                <button onclick="deleteProduct('${product.id}')">Delete</button>
            `;
            productListDiv.appendChild(productCard);
        });

    } catch (error) {
        console.error("Error loading products:", error);
    }
}

// Redirect to Product Details Page
function viewProduct(productId) {
    window.location.href = `product_details.html?id=${productId}`;
}

// Redirect to Edit Product Page
function editProduct(productId) {
    window.location.href = `edit_product.html?id=${productId}`;
}

// Delete product from database and UI
async function deleteProduct(productId) {
    if (!confirm("Are you sure you want to delete this product?")) return;

    try {
        let response = await fetch(`${API_BASE_URL}/products/delete/${productId}`, {
            method: "DELETE",
        });

        if (response.ok) {
            alert("Product deleted successfully!");
            loadProducts(); // Reload products after deletion
        } else {
            alert("Failed to delete product.");
        }
    } catch (error) {
        console.error("Error deleting product:", error);
    }
}

// Ensure products load when the page is ready
document.addEventListener("DOMContentLoaded", loadProducts);
