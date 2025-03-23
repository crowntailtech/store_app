const API_BASE_URL = "https://out03xtzz3.execute-api.us-east-1.amazonaws.com/prod";
const productId = new URLSearchParams(window.location.search).get("id");

window.onload = async () => {
  if (!productId) return alert("Missing Product ID");

  try {
    const res = await fetch(`${API_BASE_URL}/products/${productId}`);
    const product = await res.json();

    document.getElementById("name").value = product.name || "";
    document.getElementById("price").value = product.price || "";
    document.getElementById("currency").value = product.currency || "";

    if (product.image_url) {
      const img = document.createElement("img");
      img.src = product.image_url;
      img.alt = "Current Image";
      img.className = "preview-image";
      document.getElementById("editProductForm").prepend(img);
    }
  } catch (err) {
    console.error(err);
    alert("Failed to load product.");
  }
};

document.getElementById("editProductForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const price = document.getElementById("price").value;
  const currency = document.getElementById("currency").value;

  const imageInput = document.getElementById("image");
  let imageBase64 = null;

  if (imageInput.files.length > 0) {
    const file = imageInput.files[0];
    const reader = new FileReader();

    reader.onloadend = async () => {
      imageBase64 = reader.result.split(",")[1]; // remove data:image/...;base64,

      const payload = JSON.stringify({
        name,
        price,
        currency,
        image_base64: imageBase64,
        image_type: file.type
      });

      await sendUpdate(payload);
    };

    reader.readAsDataURL(file);
  } else {
    const payload = JSON.stringify({ name, price, currency });
    await sendUpdate(payload);
  }
});

async function sendUpdate(payload) {
  try {
    const res = await fetch(`${API_BASE_URL}/products/${productId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: payload
    });

    const data = await res.json();

    if (res.ok) {
      alert("✅ Product updated");
      window.location.href = "home.html";
    } else {
      alert(data.error || "❌ Failed to update");
    }
  } catch (err) {
    console.error("Update error:", err);
    alert("❌ Error occurred while updating");
  }
}
