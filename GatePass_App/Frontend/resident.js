document.getElementById("visitorForm")
  .addEventListener("submit", async function(e) {

  e.preventDefault();

  const vname = document.getElementById("vname").value.trim();
  const vphone = document.getElementById("vphone").value.trim();
  const purpose = document.getElementById("purpose").value.trim();
  const flat = document.getElementById("flat").value.trim();
  const msg = document.getElementById("otpMsg");

  if (!vname || !vphone || !purpose || !flat) {
    msg.innerText = "Please fill all fields.";
    msg.style.color = "red";
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/resident/create-visitor`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        visitor_name: vname,
        visitor_phone: vphone,
        purpose: purpose,
        flat_number: flat,
        created_by: 2
      })
    });

    const result = await res.json();

    if (!res.ok) {
      msg.innerText = result.detail || "Error creating visitor pass.";
      msg.style.color = "red";
      return;
    }

    msg.innerText = `OTP: ${result.otp} (valid 5 mins)`;
    msg.style.color = "green";
    document.getElementById("visitorForm").reset();

  } catch (error) {
    msg.innerText = "Server error.";
    msg.style.color = "red";
  }
});