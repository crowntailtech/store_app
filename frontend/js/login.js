const LOGIN_URL = "https://ma6z6vv6syvlxpwsctj5puq7py0nqdct.lambda-url.us-east-1.on.aws/";

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
