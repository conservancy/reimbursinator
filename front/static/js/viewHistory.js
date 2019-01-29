// Hack to change endpoint url for each OS
function getEndpointDomain() {
    let OSName;
    let domain;

    if (navigator.appVersion.indexOf("Win") !== -1)
        OSName = "Windows";
    else if (navigator.appVersion.indexOf("Mac") !== -1)
        OSName = "MacOS";
    else if (navigator.appVersion.indexOf("X11") !== -1)
        OSName = "UNIX";
    else if (navigator.appVersion.indexOf("Linux") !== -1)
        OSName = "Linux";
    else
        OSName = "Unknown OS";

    console.log(`Detected operating system: ${OSName}`);

    if (OSName === "Windows") {
        domain = "https://192.168.99.100:8444/";
    } else {
        domain = "https://localhost:8444/"
    }

    return domain;
}

function displayListOfReports(listOfReports) {
    const cardBody = document.querySelector(".card-body");
    const table = document.createElement("table");
    const reports = listOfReports.reports;
    let reportsAdded = 0;

    // Create report table
    for (let i = 0; i < reports.length; i++) {
        let title = reports[i].title;
        let dateCreated = new Date(reports[i].date_created).toLocaleDateString("en-US");
        let state = reports[i].state;
        let dateSubmitted;

        // Create edit/view button
        let actionButton = document.createElement("button");
        actionButton.type = "submit";
        actionButton.setAttribute("data-toggle", "modal");
        actionButton.classList.add("btn");

        if (state === "created") {
            // Edit button
            dateSubmitted = "TBD";
            actionButton.classList.add("btn-primary");
            actionButton.innerHTML = "Edit";
            actionButton.setAttribute("data-target", "#editReportModal");
        } else {
            // View button
            dateSubmitted = new Date(reports[i].date_submitted).toLocaleDateString("en-US");
            actionButton.classList.add("btn-success");
            actionButton.innerHTML = "View";
        }

        let bodyRow = table.insertRow(i); 
        bodyRow.insertCell(0).innerHTML = title;
        bodyRow.insertCell(1).innerHTML = dateCreated; 

        let stateCell = bodyRow.insertCell(2);
        stateCell.innerHTML = state;
        stateCell.classList.add("d-none", "d-lg-table-cell");


        let dateSubmittedCell = bodyRow.insertCell(3);
        dateSubmittedCell.innerHTML = dateSubmitted;
        dateSubmittedCell.classList.add("d-none", "d-md-table-cell");

        bodyRow.insertCell(4).appendChild(actionButton);
        reportsAdded++;
    }

    if (reportsAdded === 0) {
        // Report list is empty
        const p = document.createElement("p");
        p.innerHTML = "No reports found.";
        cardBody.appendChild(p);
    } else {
        // Report list exists and table rows have been created
        // Create table header, add it to the table, and append the result to the card body
        const thead = document.createElement("thead");
        const tr = document.createElement("tr");

        const headTitle = document.createElement("th");
        headTitle.innerHTML = "Title";
        tr.appendChild(headTitle);

        const headDateCreated = document.createElement("th");
        headDateCreated.innerHTML = "Date Created";
        tr.appendChild(headDateCreated);

        const headState = document.createElement("th");
        headState.innerHTML = "State";
        headState.classList.add("d-none", "d-lg-table-cell"); // Column shown only on large displays
        tr.appendChild(headState);

        const headDateSubmitted = document.createElement("th")
        headDateSubmitted.innerHTML = "Date Submitted";
        headDateSubmitted.classList.add("d-none", "d-md-table-cell"); // Column only shown on medium and larger displays
        tr.appendChild(headDateSubmitted);

        const headAction = document.createElement("th")
        headAction.innerHTML = "Action";
        tr.appendChild(headAction);

        thead.appendChild(tr);
        table.prepend(thead);
        table.classList.add("table", "table-striped", "table-responsive-sm");
        cardBody.appendChild(table);
    }
}

function getReportHistory(event) {
    const token = localStorage.getItem("token");
    const url = getEndpointDomain() + "backend/list_report";
    const xhr = new XMLHttpRequest();

    console.log(`Attempting a connection to the following endpoint: ${url}`);

    xhr.open("GET", url, true);
    //xhr.setRequestHeader("Authorization", `Token  ${token}`);
    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                console.log("GET list_report SUCCESS!");
                console.log(`Server response:\n${this.response}`);
                listOfReports = JSON.parse(this.response);
                displayListOfReports(listOfReports);
            } else {
                console.log("GET list_report FAILURE!");
                console.log(`Server status: ${this.status}`);
                console.log(`Server response:\n${this.response}`);
            }
        }
    };

    xhr.onerror = function() {
        alert("Connection error!");
    };

    xhr.send();
}

document.addEventListener("DOMContentLoaded", getReportHistory);
