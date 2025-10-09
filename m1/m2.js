loadTableData();
const table = document.getElementById('dataTable');
let row = table.rows.length;
document.getElementById('addButton').addEventListener('click', function() {
    const qty = parseInt(document.getElementById('qty').value);
    const time = parseFloat(document.getElementById('time').value);
    const plusTime = parseFloat(document.getElementById('plustime').value);

    if (isNaN(qty) || isNaN(time)) {
        alert('Please enter valid numbers');
        return;
    }

    
    let allTime = ((qty * time) / 60) + plusTime / 60
    const allTimeFormatted = allTime.toFixed(2);
    const table = document.getElementById('dataTable');
    const newRow = table.insertRow();

    row +=1
   

    const cell1 = newRow.insertCell(0);
    const cell2 = newRow.insertCell(1);
    const cell3 = newRow.insertCell(2);
    const cell4 = newRow.insertCell(3);
    const cell5 = newRow.insertCell(4);
    const cell6 = newRow.insertCell(5);

    cell1.textContent = String(row);
    cell2.textContent = qty;
    cell3.textContent = time.toFixed(2);
    cell4.textContent = plusTime;
    cell5.textContent = allTimeFormatted;

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.className = "btn btn-outline btn-error btn-xs"
    deleteButton.addEventListener('click', function() {
        deleteRow(newRow);
    });
    cell6.appendChild(deleteButton);

    updateTotalAllTime();
    saveTableData();
    document.getElementById('qty').value = ""
    document.getElementById('time').value = ""
    document.getElementById('plustime').value = 0
});

function deleteRow(row) {
    // const table = document.getElementById('dataTable');
    row.remove();
    // table.deleteRow(row.rowIndex);
    updateTotalAllTime();
    saveTableData();
}

function updateTotalAllTime() {
    const table = document.getElementById('dataTable');
    let totalAllTime = 0;
    let all = 0

    

    for (let i = 0; i < table.rows.length; i++) {
        totalAllTime += parseFloat(table.rows[i].cells[4].textContent);
        all += parseInt(table.rows[i].cells[1].textContent)
    }
    if (totalAllTime < 7.5){ 
        let enouthTime = 7.5 - totalAllTime
        document.getElementById('enouthTime').textContent = enouthTime.toFixed(2);
        // document.getElementById('enouthTime').className = "text-red-600 font-bold";
    }else{
        document.getElementById('enouthTime').textContent = "It's enought"; 
    }

    document.getElementById('totalAllTime').textContent = totalAllTime.toFixed(2);
    document.getElementById('all').textContent = all
}
function saveTableData() {
    const table = document.getElementById('dataTable');
    const rows = [];

    for (let i = 0; i < table.rows.length; i++) { // Start from 1 to skip header row
        const cells = table.rows[i].cells;
        
        rows.push({
            qty: cells[1].textContent,
            time: cells[2].textContent,
            plusTime: cells[3].textContent,
            allTime: cells[4].textContent
        });
    }
    
    localStorage.setItem('tableData', JSON.stringify(rows));
}

function loadTableData() {
    const tableData = JSON.parse(localStorage.getItem('tableData'));
    let row = 0
    if (tableData) {
        const table = document.getElementById('dataTable');
        tableData.forEach(rowData => {
            const newRow = table.insertRow();
            const cell1 = newRow.insertCell(0);
            const cell2 = newRow.insertCell(1);
            const cell3 = newRow.insertCell(2);
            const cell4 = newRow.insertCell(3);
            const cell5 = newRow.insertCell(4);
            const cell6 = newRow.insertCell(5);

            row +=1
            cell1.textContent = String(row) 
            cell2.textContent = rowData.qty;
            cell3.textContent = rowData.time;
            cell4.textContent = rowData.plusTime;
            cell5.textContent = rowData.allTime;
            

            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.className = "btn btn-outline btn-error btn-xs"
            deleteButton.addEventListener('click', function() {
                deleteRow(newRow);
            });
            cell6.appendChild(deleteButton);
        });
        updateTotalAllTime();
    }
}

function openAddDataModal() {
    const modal = document.getElementById('addDataModal');
    modal.classList.add('modal-open');
}

