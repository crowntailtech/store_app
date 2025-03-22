const API_BASE_URL = "https://your-api-gateway-url.com";

// Load user profile
async function loadUserProfile() {
    let token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "index.html";
        return;
    }

    try {
        let response = await fetch(`${API_BASE_URL}/auth/profile`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        let data = await response.json();

        if (data.success) {
            document.getElementById("profile-name").innerText = data.user.name;
            document.getElementById("profile-email").innerText = data.user.email;
            document.getElementById("profile-date").innerText = new Date(data.user.registeredDate).toDateString();
        } else {
            alert("Failed to load profile data.");
        }
    } catch (error) {
        console.error("Error loading profile:", error);
    }
}

// Edit Profile (Redirect to Edit Page)
function editProfile() {
    console.log("Edit Profile button clicked"); // Debugging
    window.location.href = "edit_profile.html";
}

// Change Password (Redirect to Change Password Page)
function changePassword() {
    console.log("Change Password button clicked"); // Debugging
    window.location.href = "change_password.html";
}

// Ensure functions are globally accessible
window.editProfile = editProfile;
window.changePassword = changePassword;
