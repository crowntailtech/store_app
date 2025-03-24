const LAMBDA_URL = "https://out03xtzz3.execute-api.us-east-1.amazonaws.com/prod/register";

document.getElementById("registerForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  const payload = { name, email, password };

  try {
    const res = await fetch(LAMBDA_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    let data;
    try {
      data = await res.json(); // Try to parse JSON
    } catch (jsonErr) {
      console.warn("⚠️ Response is not JSON. Falling back.");
      data = { error: "Unexpected server response" };
    }

    if (res.ok && data.success) {
      alert("✅ Registered successfully!");
      window.location.href = "login.html";
    } else {
      alert("❌ " + (data.error || "Registration failed."));
    }
  } catch (err) {
    console.error("Register error:", err);
    alert("❌ Network error occurred during registration.");
  }
});
