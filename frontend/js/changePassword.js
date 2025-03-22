const API_BASE_URL = "https://your-api-gateway-url.com";

// Handle Change Password
document.getElementById("changePasswordForm")?.addEventListener("submit", async (event) => {
    event.preventDefault();

    let token = localStorage.getItem("token");
    let currentPassword = document.getElementById("current-password").value;
    let newPassword = document.getElementById("new-password").value;
    let confirmPassword = document.getElementById("confirm-password").value;

    // Validate new password & confirm password match
    if (newPassword !== confirmPassword) {
        alert("New passwords do not match!");
        return;
    }

    try {
        let response = await fetch(`${API_BASE_URL}/auth/change-password`, {
            method: "PUT",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ currentPassword, newPassword })
        });

        let data = await response.json();

        if (data.success) {
            alert("Password updated successfully!");
            window.location.href = "profile.html"; // Redirect to profile page
        } else {
            alert("Failed to update password. Please check your current password.");
        }
    } catch (error) {
        console.error("Error updating password:", error);
    }
});
