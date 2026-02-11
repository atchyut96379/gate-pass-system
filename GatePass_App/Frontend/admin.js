document.getElementById("createUserForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const role = document.getElementById("role").value;

  const data = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
    phone: document.getElementById("phone").value,
    flat: role === "SECURITY" ? null : document.getElementById("flat").value,
    role: role
  };

  const res = await fetch("https://gate-pass-system-auhy.onrender.com/admin/create-user", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const msg = document.getElementById("msg");

  if (!res.ok) {
    msg.innerText = "Error creating user";
    msg.style.color = "red";
    return;
  }

  msg.innerText = "User created successfully";
  msg.style.color = "green";

  document.getElementById("createUserForm").reset();
});
