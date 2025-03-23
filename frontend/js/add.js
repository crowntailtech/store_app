// File: js/add.js
const API_BASE_URL = "https://out03xtzz3.execute-api.us-east-1.amazonaws.com/prod";

const form = document.getElementById("addProductForm");

form?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const price = document.getElementById("price").value;
  const currency = document.getElementById("currency").value;
  const imageInput = document.getElementById("image");
  const imageFile = imageInput.files[0];

  if (!imageFile) {
    alert("Please select an image.");
    return;
  }

  try {
    const reader = new FileReader();

    reader.onload = async function () {
      console.log("✅ Reader loaded");

      const base64Image = reader.result.split(",")[1]; // remove data:image/...;base64,

      const payload = {
        name,
        price,
        currency,
        image_base64: base64Image,
        image_name: imageFile.name,
        image_type: imageFile.type
      };

      console.log("📦 Payload to send:", payload);

      const response = await fetch(`${API_BASE_URL}/products`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      console.log("📬 API Response:", data);

      if (response.ok && data.success) {
        alert("✅ Product added successfully!");
        window.location.href = "home.html";
      } else {
        alert("❌ Failed to add product: " + (data.error || "Unknown error"));
      }
    };

    console.log("⏳ Reading file...");
    reader.readAsDataURL(imageFile);
  } catch (error) {
    console.error("❌ Error:", error);
    alert("❌ Error while adding product.");
  }
});
