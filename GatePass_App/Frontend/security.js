// const API_BASE = "https://gate-pass-system-auhy.onrender.com";
async function verifyOtp() {

  const data = {
    flat_number: document.getElementById("flat").value.trim(),
    otp: document.getElementById("otp").value.trim(),
    verified_by: 3
  };

  try {
    const res = await fetch(`${API_BASE}/security/verify-otp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await res.json();
    const resultDiv = document.getElementById("result");

    if (!res.ok) {
      resultDiv.innerText = result.detail;
      resultDiv.style.color = "red";
      return;
    }

    resultDiv.innerText = result.message;
    resultDiv.style.color = "green";

  } catch (error) {
    alert("Server connection failed.");
  }
}