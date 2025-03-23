const API_BASE_URL = "https://out03xtzz3.execute-api.us-east-1.amazonaws.com/prod";

window.onload = async function () {
  const container = document.getElementById("product-list");

  // Add Product Box (always present)
  const addBox = document.createElement("div");
  addBox.className = "add-card";
  addBox.innerHTML = "+ Add Product";
  addBox.onclick = () => showAddProductForm();
  container.appendChild(addBox);

  try {
    const res = await fetch(`${API_BASE_URL}/products`);
    const result = await res.json();

    console.log("✅ API response:", result);  // Debug line

    const products = result.products || [];

    if (products.length === 0) {
      const emptyMsg = document.createElement("p");
      emptyMsg.textContent = "No products available.";
      container.appendChild(emptyMsg);
      return;
    }

    products.forEach(product => {
      const card = document.createElement("div");
      card.className = "product-card";

      card.innerHTML = `
        <img src="${product.image_url}" alt="${product.name}" class="product-img" />
        <h3>${product.name}</h3>
        <p>Price: ${product.price} (${product.currency})</p>
        <button onclick="editProduct('${product._id}')">Edit</button>
        <button onclick="deleteProduct('${product._id}')">Delete</button>
      `;

      container.appendChild(card);
    });

  } catch (err) {
    console.error("❌ Error loading products:", err);
    const errorMsg = document.createElement("p");
    errorMsg.innerHTML = "<span style='color:red'>❌ Failed to load products.</span>";
    container.appendChild(errorMsg);
  }
};

function editProduct(id) {
  window.location.href = `edit_products.html?id=${id}`;
}

function deleteProduct(id) {
  if (!confirm("Are you sure you want to delete this product?")) return;

  fetch(`${API_BASE_URL}/products/${id}`, {
    method: "DELETE"
  }).then(res => {
    if (res.ok) {
      alert("Product deleted!");
      window.location.reload();
    } else {
      alert("Failed to delete product.");
    }
  }).catch(err => console.error("Delete error:", err));
}

function showAddProductForm() {
  window.location.href = "add_product.html";
}
