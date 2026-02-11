let allData = [];
let currentPage = 1;
const recordsPerPage = 10;

async function loadHistory() {
    try {
        const response = await fetch("http://127.0.0.1:8000/admin-security/visitor-history");
        const data = await response.json();

        allData = data.reverse(); // latest first
        renderTable();
        renderPagination();

    } catch (error) {
        console.error("Error loading history:", error);
    }
}

function renderTable() {
    const tableBody = document.getElementById("historyTable");
    tableBody.innerHTML = "";

    const start = (currentPage - 1) * recordsPerPage;
    const end = start + recordsPerPage;
    const pageData = allData.slice(start, end);

    pageData.forEach(item => {
        const row = `
            <tr>
                <td>${item.name}</td>
                <td>${item.phone}</td>
                <td>${item.purpose}</td>
                <td>${item.flat_number}</td>
                <td>${item.status}</td>
                <td>${item.created_at}</td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}

function renderPagination() {
    const totalPages = Math.ceil(allData.length / recordsPerPage);
    const paginationDiv = document.getElementById("pagination");
    paginationDiv.innerHTML = "";

    for (let i = 1; i <= totalPages; i++) {
        const start = (i - 1) * recordsPerPage + 1;
        const end = Math.min(i * recordsPerPage, allData.length);

        const btn = document.createElement("button");
        btn.innerText = `${start}-${end}`;
        btn.className = "page-btn";

        if (i === currentPage) {
            btn.classList.add("active-page");
        }

        btn.onclick = () => {
            currentPage = i;
            renderTable();
            renderPagination();
        };

        paginationDiv.appendChild(btn);
    }
}

loadHistory();
