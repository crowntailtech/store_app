const LOGIN_URL = "https://out03xtzz3.execute-api.us-east-1.amazonaws.com/prod/login";

document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  const payload = { email, password };

  try {
    const res = await fetch(LOGIN_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (res.ok && data.success) {
      alert("✅ Login successful!");
      // optionally save user info or token
      localStorage.setItem("user", JSON.stringify(data.user));
      window.location.href = "home.html";
    } else {
      alert("❌ " + (data.error || "Login failed"));
    }
  } catch (err) {
    console.error("Login error:", err);
    alert("❌ Network error occurred during login.");
  }
});
