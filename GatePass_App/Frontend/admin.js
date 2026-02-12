document.getElementById("createUserForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const role = document.getElementById("roleSelect").value;

    const data = {
      name: document.getElementById("name").value.trim(),
      email: document.getElementById("email").value.trim(),
      password: document.getElementById("password").value.trim(),
      phone: document.getElementById("phone").value.trim(),
      flat: role === "SECURITY"
        ? null
        : document.getElementById("flatNumber").value.trim(),
      role: role
    };

    try {
      const res = await fetch(`${API_BASE}/admin/create-user`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const result = await res.json();

      if (!res.ok) {
        alert(result.detail || "Error creating user");
        return;
      }

      alert(result.message);
      document.getElementById("createUserForm").reset();

    } catch (err) {
      console.error("Create User Error:", err);
      alert("Server connection failed.");
    }
  });