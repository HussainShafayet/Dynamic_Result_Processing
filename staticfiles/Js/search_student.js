const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const tbody = document.querySelector(".table-body");
tableOutput.style.display = 'None ';
searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;
    if (searchValue.trim().length > 0) {
        console.log("searchValue", searchValue);
        tbody.innerHTML = "";
        fetch("student_search/", {
                body: JSON.
                stringify({
                    searchText: searchValue
                }),
                method: "POST",
            })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                appTable.style.display = "none"
                tableOutput.style.display = "block";

                if (data.length === 0) {
                    tableOutput.style.display = 'none';
                    appTable.style.display = 'block';
                    appTable.innerHTML = 'No result found'

                } else {
                    data.forEach((item) => {
                        tbody.innerHTML += `
                                    <tr>
                                    <td>${item.related_values.reg_no}</td>
                                    <td>${item.first_name} ${item.last_name}</td>
                                    <td>${item.related_values.batch}</td>
                                    <td>${item.related_values.session}</td>
                                    <td><a class="btn btn-primary" href="user_details/${item.id}">Details</a>
                                    </td>
                                    </tr> `
                    });
                }
            });
    } else {
        appTable.style.display = "block";
        tableOutput.style.display = "none";
    }
});