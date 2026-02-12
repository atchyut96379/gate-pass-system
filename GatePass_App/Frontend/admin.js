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
        ? ""
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
      console.log("Backend Response:", result);

      if (!res.ok) {
      alert(result.detail || JSON.stringify(result));
      return;
}
      // ✅ Handle both string and object message
      if (typeof result.message === "string") {
      alert(result.message);
      } else if (typeof result.message === "object") {
      alert(JSON.stringify(result.message));
      } else {
      alert("User created successfully");
      }

      document.getElementById("createUserForm").reset();

    } catch (err) {
      console.error("Create User Error:", err);
      alert("Server connection failed.");
    }
  });