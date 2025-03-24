const CAMPAIGN_API = "http://108.129.145.28:8000/campaigns/public/";
const DONATION_API_BASE = "http://108.129.145.28:8000/campaigns/public/donate/";

document.addEventListener("DOMContentLoaded", async () => {
  const campaignContainer = document.getElementById("campaigns");

  try {
    const response = await fetch(CAMPAIGN_API);
    const data = await response.json();

    if (data.campaigns && data.campaigns.length > 0) {
      data.campaigns.forEach((campaign) => {
        const campaignCard = document.createElement("div");
        campaignCard.classList.add("campaign-card");

        campaignCard.innerHTML = `
          <h3>${campaign.title}</h3>
          <p>${campaign.description}</p>
          <p><strong>Goal:</strong> ₹${campaign.goal}</p>
          <p><strong>Collected:</strong> ₹${campaign.amount_collected}</p>
          <input type="number" placeholder="Enter amount" id="donate-${campaign._id}" />
          <button onclick="donate('${campaign._id}')">Donate</button>
          <div class="donation-msg" id="msg-${campaign._id}"></div>
        `;

        campaignContainer.appendChild(campaignCard);
      });
    } else {
      campaignContainer.innerHTML = "<p>No public campaigns available.</p>";
    }
  } catch (error) {
    console.error("Error fetching campaigns:", error);
    campaignContainer.innerHTML = "<p>Error loading campaigns.</p>";
  }
});

async function donate(campaignId) {
  const amountInput = document.getElementById(`donate-${campaignId}`);
  const msgBox = document.getElementById(`msg-${campaignId}`);
  const amount = parseFloat(amountInput.value);

  if (isNaN(amount) || amount <= 0) {
    msgBox.textContent = "Please enter a valid amount.";
    msgBox.style.color = "red";
    return;
  }

  try {
    const res = await fetch(`${DONATION_API_BASE}${campaignId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        amount: amount,
        email: "anonymous@example.com",
      }),
    });

    const result = await res.json();

    if (res.ok) {
      msgBox.textContent = `✅ ${result.message} (Collected: ₹${result.result.total_collected})`;
      msgBox.style.color = "green";
      amountInput.value = "";
    } else {
      msgBox.textContent = `❌ ${result.error || "Donation failed."}`;
      msgBox.style.color = "red";
    }
  } catch (err) {
    console.error("Donation error:", err);
    msgBox.textContent = "❌ Network error.";
    msgBox.style.color = "red";
  }
}
