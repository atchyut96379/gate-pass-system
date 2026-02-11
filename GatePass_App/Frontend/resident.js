document.getElementById("visitorForm").addEventListener("submit", async function(e) {

  e.preventDefault();   // Stop default submit

  const vname = document.getElementById("vname").value.trim();
  const vphone = document.getElementById("vphone").value.trim();
  const purpose = document.getElementById("purpose").value.trim();
  const flat = document.getElementById("flat").value.trim();
  const msg = document.getElementById("otpMsg");

  // ✅ EMPTY VALIDATION
  if (!vname || !vphone || !purpose || !flat) {
    msg.innerText = "Please fill all fields before generating OTP.";
    msg.style.color = "red";
    return;
  }

  // ✅ PHONE VALIDATION
  const phoneRegex = /^[0-9]{10}$/;
  if (!phoneRegex.test(vphone)) {
    msg.innerText = "Enter valid 10-digit phone number.";
    msg.style.color = "red";
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:8000/resident/create-visitor", {
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

    if (!res.ok) {
      msg.innerText = "Error creating visitor pass.";
      msg.style.color = "red";
      return;
    }

    const result = await res.json();

    msg.innerText = `OTP: ${result.otp} (valid for 5 mins)`;
    msg.style.color = "green";

    document.getElementById("visitorForm").reset();

  } catch (error) {
    msg.innerText = "Server error. Try again.";
    msg.style.color = "red";
  }

});
