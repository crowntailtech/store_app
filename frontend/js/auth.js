const API_BASE_URL = "https://your-api-gateway-url.com";

// Handle Login
document.getElementById("loginForm")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    try {
        let response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        let data = await response.json();

        if (data.token) {
            localStorage.setItem("token", data.token);
            window.location.href = "home.html";  // Redirect to home page after login
        } else {
            alert("Login failed. Check credentials.");
        }
    } catch (error) {
        console.error("Error logging in:", error);
    }
});

// Handle Registration
document.getElementById("registerForm")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    
    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    try {
        let response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password })
        });

        let data = await response.json();

        if (data.success) {
            alert("Registration successful! Please log in.");
            window.location.href = "index.html";  // Redirect to login page
        } else {
            alert("Registration failed. Try again.");
        }
    } catch (error) {
        console.error("Error registering:", error);
    }
});

// Check if user is logged in (Redirect if not authenticated)
function checkAuth() {
    let token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "index.html";  // Redirect to login page
    }
}

// Logout function (Clear token and redirect)
function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";  // Redirect to login page
}
