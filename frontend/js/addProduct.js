const API_BASE_URL = "https://your-api-gateway-url.com";

// Handle Add Product Form Submission
document.getElementById("addProductForm")?.addEventListener("submit", async (event) => {
    event.preventDefault();

    let token = localStorage.getItem("token");
    let name = document.getElementById("name").value;
    let price = document.getElementById("price").value;
    let currency = document.getElementById("currency").value;

    // Validate input
    if (!name || !price) {
        alert("Please fill in all fields.");
        return;
    }

    try {
        let response = await fetch(`${API_BASE_URL}/products/add`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, price, currency })
        });

        let data = await response.json();

        if (data.success) {
            alert("Product added successfully!");
            window.location.href = "home.html"; // Redirect to home page
        } else {
            alert("Failed to add product.");
        }
    } catch (error) {
        console.error("Error adding product:", error);
    }
});
