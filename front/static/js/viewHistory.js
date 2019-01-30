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

function getDataFromEndpoint(url, callback) {
    const token = localStorage.getItem("token");
    const xhr = new XMLHttpRequest();

    console.log(`Attempting a connection to the following endpoint: ${url}`);

    xhr.open("GET", url, true);
    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                console.log("GET SUCCESS!");
                console.log(`Server response:\n${this.response}`);
                parsedData = JSON.parse(this.response);
                callback(parsedData);
            } else {
                console.error("GET FAILURE!");
                console.error(`Server status: ${this.status}`);
                console.error(`Server response:\n${this.response}`);
            }
        }
    };

    xhr.onerror = function() {
        alert("Connection error!");
    };

    xhr.send();
}

function createEditReportForm(parsedData) {
    console.log("In createEditReportForm");
    console.log(JSON.stringify(parsedData));
    const cardBody = document.querySelector(".card-body");
    const fragment = document.createDocumentFragment();
    const title = parsedData.title;
    const dateCreated = new Date(parsedData.date_created).toLocaleDateString("en-us");
    

    if (cardBody.hasChildNodes() === true && cardBody.childNodes[1]) {
       cardBody.removeChild(cardBody.childNodes[1]); 
    }

    console.log(`Title: ${title}`);
    console.log(`Date Created: ${dateCreated}`);
    const form = document.createElement("form");

    const sections = parsedData.sections;
    for (let section in sections) {
        console.log(`Section title: ${sections[section].title}`);
        console.log(`Section html description: ${sections[section].html_description}`);

        let sectionTitle = document.createElement("p").innerHTML = sections[section].title;
        form.appendChild(title);
        let sectionDescription = sections[section].html_description; 
        form.appendChild(sectionDescription);
        
        for (let field in sections[section].fields) {
            console.log(`Field label: ${sections[section].fields[field].label}`); 
            console.log(`Field type: ${sections[section].fields[field].type}`); 
            console.log(`Field value: ${sections[section].fields[field].value}`); 
            

        }
    }
}

function displayListOfReports(parsedData) {
    const cardBody = document.querySelector(".card-body");
    const table = document.createElement("table");
    const reports = parsedData.reports;
    let reportsAdded = 0;

    // Create report table
    for (let i = 0; i < reports.length; i++) {
        let title = reports[i].title;
        let dateCreated = new Date(reports[i].date_created).toLocaleDateString("en-US");
        let state = reports[i].state;
        let dateSubmitted;
        let rid = reports[i].report_pk;

        // Create edit/view button
        let actionButton = document.createElement("button");
        actionButton.type = "submit";
        actionButton.setAttribute("data-rid", rid);
        actionButton.classList.add("btn");

        if (state === "created") {
            // Edit button
            dateSubmitted = "TBD";
            actionButton.classList.add("btn-primary");
            actionButton.innerHTML = "Edit";
            actionButton.addEventListener("click", openEditReportForm);
        } else {
            // View button
            dateSubmitted = new Date(reports[i].date_submitted).toLocaleDateString("en-US");
            actionButton.classList.add("btn-success");
            actionButton.innerHTML = "View";
        }

        // Insert data into the table object
        let bodyRow = table.insertRow(i); 
        bodyRow.insertCell(0).innerHTML = title;
        bodyRow.insertCell(1).innerHTML = dateCreated; 

        let stateCell = bodyRow.insertCell(2);
        stateCell.innerHTML = state;
        stateCell.classList.add("d-none", "d-lg-table-cell"); // Column visible only on large displays

        let dateSubmittedCell = bodyRow.insertCell(3);
        dateSubmittedCell.innerHTML = dateSubmitted;
        dateSubmittedCell.classList.add("d-none", "d-md-table-cell"); // Column visible on medium and larger displays

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

        const tr = document.createElement("tr");

        const headTitle = document.createElement("th");
        headTitle.innerHTML = "Title";
        tr.appendChild(headTitle);

        const headDateCreated = document.createElement("th");
        headDateCreated.innerHTML = "Date Created";
        tr.appendChild(headDateCreated);

        const headState = document.createElement("th");
        headState.innerHTML = "State";
        headState.classList.add("d-none", "d-lg-table-cell"); // Column visible only on large displays
        tr.appendChild(headState);

        const headDateSubmitted = document.createElement("th")
        headDateSubmitted.innerHTML = "Date Submitted";
        headDateSubmitted.classList.add("d-none", "d-md-table-cell"); // Column visible on medium and larger displays
        tr.appendChild(headDateSubmitted);

        const headAction = document.createElement("th")
        headAction.innerHTML = "Action";
        tr.appendChild(headAction);

        const thead = document.createElement("thead");
        thead.appendChild(tr);
        table.prepend(thead);
        table.classList.add("table", "table-striped", "table-responsive-sm");
        cardBody.appendChild(table);
    }
}

function getReportHistory(event) {
    const url = getEndpointDomain() + "api/v1/reports";
    getDataFromEndpoint(url, displayListOfReports);
}

function openEditReportForm(event) {
    const url = getEndpointDomain() + "api/v1/report/" + this.dataset.rid;
    getDataFromEndpoint(url, createEditReportForm);
}


document.addEventListener("DOMContentLoaded", getReportHistory);


