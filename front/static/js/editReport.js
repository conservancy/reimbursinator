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

function populateEditReportForm(specificReport) {
    const cardBody = document.querySelector(".card-body");

    cardBody.innerHTML = JSON.stringify(specificReport);
}

function getSpecificReport(event) {
    event.preventDefault();

    const token = localStorage.getItem("token");

    // need to get rid from option value here
    const rid = this.elements.rid.value;
    console.log(`rid for this report is ${rid}`);
    const url = getEndpointDomain() + "backend/get_report";
    const xhr = new XMLHttpRequest();

    console.log("getSpecificReport");
    console.log(`Attempting a connection to the following endpoint: ${url}`);

    console.log("Before open()");
    xhr.open("GET", url, true);
    //xhr.setRequestHeader("Authorization", `Token  ${token}`);

    console.log("After open()");
    xhr.onreadystatechange = function() {
        console.log(`In onreadystate, readyState = ${this.readyState}`);
        if (this.readyState === 4) {
            if (this.status === 200) {
                console.log("GET get_report SUCCESS!");
                console.log(`Server response:\n${this.response}`);
                specificReport = JSON.parse(this.response);
                populateEditReportForm(specificReport);
            } else {
                console.log("GET get_report FAILURE!");
                console.log(`Server status: ${this.status}`);
                console.log(`Server response:\n${this.response}`);
            }
        }
    };

    xhr.onerror = function() {
        alert("Connection error!");
    };

    console.log("Before send()");
    xhr.send();
    console.log("After send()");
}

function populateSelectDropdown(listOfReports) {
    const select = document.querySelector("select");
    const reports = listOfReports.reports;
    const fragment = document.createDocumentFragment();

    for (let i = 0; i < reports.length; i++) {
        if (reports[i].state === "created") {
            let title = reports[i].title;
            let dateCreated = new Date(reports[i].date_created).toLocaleDateString("en-US");
            let rid = 2;
            let option = document.createElement("option");
            option.innerHTML = `${title}, ${dateCreated}`;
            option.value = rid;
            fragment.appendChild(option);            
        }
    }

    if (fragment.hasChildNodes() === false) {
        // Empty unfinished report list
        const emptyOption = document.createElement("option");
        emptyOption.innerHTML = "No unfinshed reports found.";
        fragment.appendChild(emptyOption);
    }

    select.appendChild(fragment);
}

function getAllReports(event) {
    const token = localStorage.getItem("token");
    const url = getEndpointDomain() + "backend/list_report";
    const xhr = new XMLHttpRequest();

    console.log("getAllReports");
    console.log(`Attempting a connection to the following endpoint: ${url}`);

    console.log("Before open()");
    xhr.open("GET", url, true);
    console.log("After open()");

    //xhr.setRequestHeader("Authorization", `Token  ${token}`);
    xhr.onreadystatechange = function() {
        console.log(`In onreadystatechange, readyState = ${this.readyState}`);
        if (this.readyState === 4) {
            if (this.status === 200) {
                console.log("GET list_report SUCCESS!");
                console.log(`Server response:\n${this.response}`);
                listOfReports = JSON.parse(this.response);
                populateSelectDropdown(listOfReports);
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

    console.log("Before send()");
    xhr.send();
    console.log("After send()");
}

document.addEventListener("DOMContentLoaded", getAllReports);
const editReportForm = document.querySelector("#editReportForm");
editReportForm.addEventListener("submit", getSpecificReport);
