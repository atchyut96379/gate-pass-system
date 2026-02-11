async function verifyOtp() {
  const data = {
    flat_number: document.getElementById("flat").value,
    otp: document.getElementById("otp").value,
    verified_by: 3   // security user id (session later)
  };

  const res = await fetch("https://gate-pass-system-auhy.onrender.com/security/verify-otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = document.getElementById("result");

  if (!res.ok) {
    const err = await res.json();
    result.innerText = err.detail;
    result.style.color = "red";
    return;
  }

  const msg = await res.json();
  result.innerText = msg.message;
  result.style.color = "green";
}

