document.getElementById("createUserForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const role = document.getElementById("roleSelect").value;

    const data = {
      name: document.getElementById("name").value,
      email: document.getElementById("email").value,
      password: document.getElementById("password").value,
      phone: document.getElementById("phone").value,
      flatNumber: role === "SECURITY"
        ? null
        : document.getElementById("flatNumber").value,
      role: role
    };

    try {
      const res = await fetch(
        "https://gate-pass-system-auhy.onrender.com/admin/create-user",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        }
      );

      if (!res.ok) {
        alert("Error creating user");
        return;
      }

      alert("User created successfully!");
      document.getElementById("createUserForm").reset();
    } catch (err) {
      console.error(err);
      alert("Server error");
    }
  });
