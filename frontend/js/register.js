const LAMBDA_URL = "https://lambda-url-for-register.amazonaws.com"; // 🔁 Replace with actual Lambda URL

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
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (res.ok && data.success) {
      alert("✅ Registered successfully!");
      window.location.href = "login.html";
    } else {
      alert("❌ " + (data.error || "Registration failed."));
    }
  } catch (err) {
    console.error("Register error:", err);
    alert("❌ Error occurred during registration.");
  }
});
