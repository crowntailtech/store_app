document.addEventListener("DOMContentLoaded", () => {
    const convertBtn = document.getElementById("convertBtn");
  
    if (convertBtn) {
      convertBtn.addEventListener("click", convertCurrency);
    }
  
    async function convertCurrency() {
      const amount = parseFloat(document.getElementById("amount").value);
      const from = document.getElementById("from").value;
      const to = document.getElementById("to").value;
      const resultDiv = document.getElementById("result");
  
      resultDiv.innerText = "";
  
      if (!amount || amount <= 0) {
        resultDiv.style.color = "red";
        resultDiv.innerText = "❌ Please enter a valid amount.";
        return;
      }
  
      try {
        const url = `https://api.exchangerate-api.com/v4/latest/${from}`;
        const res = await fetch(url);
        const data = await res.json();
  
        if (!data.rates[to]) {
          resultDiv.style.color = "red";
          resultDiv.innerText = "❌ Conversion rate not available.";
          return;
        }
  
        const rate = data.rates[to];
        const converted = (amount * rate).toFixed(2);
  
        resultDiv.style.color = "green";
        resultDiv.innerText = `✅ ${amount} ${from} = ${converted} ${to}`;
      } catch (err) {
        console.error("Conversion error:", err);
        resultDiv.style.color = "red";
        resultDiv.innerText = "❌ Failed to fetch conversion rate.";
      }
    }
  });
  