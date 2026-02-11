const API_BASE = "https://gate-pass-system-auhy.onrender.com";

async function verifyOtp() {
  const data = {
    flat_number: document.getElementById("flat").value,
    otp: document.getElementById("otp").value,
    verified_by: 3
  };

  const res = await fetch(`${API_BASE}/security/verify-otp`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const resultDiv = document.getElementById("result");

  const result = await res.json();

  if (!res.ok) {
    resultDiv.innerText = result.detail;
    resultDiv.style.color = "red";
    return;
  }

  resultDiv.innerText = result.message;
  resultDiv.style.color = "green";
}
