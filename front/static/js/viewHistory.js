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

function createFormGroup(key, field) {
    const formGroup = document.createElement("div")
    formGroup.classList.add("form-group");

    const label = document.createElement("label");
    label.innerHTML = field.label;
    label.setAttribute("for", key);
    const input = document.createElement("input");
    input.name = key;
    input.id = key;

    switch(field.type) {
        case "boolean":
            input.type = "checkbox";
            if (field.value === true)
                input.setAttribute("checked", "checked");
            input.classList.add("form-check-input");
            formGroup.classList.add("form-check");
            label.classList.add("form-check-label");
            formGroup.appendChild(input); // Reversed order compared to others
            formGroup.appendChild(label);
            break;
        case "date":
            input.type = "datetime";
            input.value = field.value;
            input.classList.add("form-control");
            formGroup.appendChild(label);
            formGroup.appendChild(input);
            break;
        case "decimal":
            input.type = "text";
            input.value = field.value;
            input.classList.add("form-control");
            formGroup.appendChild(label);
            formGroup.appendChild(input);
            break;
        case "file":
            input.type = "file";
            input.classList.add("form-control-file");
            const link = document.createElement("a");
            link.href = field.value;
            link.innerHTML = field.value;
            formGroup.appendChild(label);
            formGroup.appendChild(input);
            formGroup.appendChild(link);
            break;
        default:
            break;
    }

    return formGroup;
}

function createCollapsibleCard(key, sectionTitle) {
    // Create card and header
    const card = document.createElement("div");
    card.classList.add("card");
    const cardHeader = document.createElement("div");
    cardHeader.classList.add("card-header");

    // Create h2, button. Append button to h2, h2 to header, and header to card
    const h2 = document.createElement("h2");
    const button = document.createElement("button");
    button.classList.add("btn", "btn-link");
    button.type = "button";
    button.setAttribute("data-toggle", "collapse");
    button.setAttribute("data-target", "#collapse" + key);
    button.innerHTML = sectionTitle;
    h2.appendChild(button);
    cardHeader.appendChild(h2);
    card.appendChild(cardHeader);

    return card;
}

function createCollapsibleCardBody(key, form, sectionDescription) {
    // Create wrapper div
    const div = document.createElement("div");
    div.classList.add("collapse", "show");
    div.setAttribute("data-parent", "#editReportAccordion");
    div.id = "collapse" + key;

    // Create card body. Append form to body, body to wrapper div
    const cardBody = document.createElement("div");
    cardBody.classList.add("card-body");
    cardBody.insertAdjacentHTML("beforeend", sectionDescription); 
    cardBody.appendChild(form);
    div.appendChild(cardBody);
    
    return div;
}

function createEditReportForm(parsedData) {
    const col = document.querySelector(".col-sm-8");
    const fragment = document.createDocumentFragment();

    while (col.firstChild) {
        col.removeChild(col.firstChild)
    }

    // Add report title and date to card header
    const reportTitle = parsedData.title;
    const dateCreated = new Date(parsedData.date_created).toLocaleDateString("en-US");
    const h3 = document.createElement("h3"); 
    h3.innerHTML = `${reportTitle}  ${dateCreated}`;
    h3.classList.add("text-center");
    fragment.appendChild(h3);

    // Create accordion
    const accordion = document.createElement("div");
    accordion.classList.add("accordion");
    accordion.id = "editReportAccordion";


    // Traverse report sections
    const sections = parsedData.sections;
    for (let key in sections) {

        let section = sections[key];

        console.log(`Section title: ${section.title}`);
        console.log(`Section html description: ${section.html_description}`);

        // Create a new collapsible card
        let card = createCollapsibleCard(key, section.title)

        // Create a new form with the section key index as id
        let form = document.createElement("form");
        form.classList.add("form");
        form.id = "form" + key;


        // Traverse the fields of this section
        let fields = section.fields;
        for (let key in fields) {

            // Create a form group for each field and add it to the form
            let field = fields[key];
            console.log(`Field label: ${field.label}`); 
            console.log(`Field type: ${field.type}`); 
            console.log(`Field value: ${field.value}`); 
            
            let formGroup = createFormGroup(key, field);
            form.appendChild(formGroup);
        }

        // Add save button to form
        let saveButton = document.createElement("button");
        saveButton.innerHTML = "Save";
        saveButton.type = "submit";
        saveButton.classList.add("btn", "btn-primary"); // TODO: add eventListener
        form.appendChild(saveButton);

        // Create collapsible card body, append form to it, append card to accordion
        let cardBody = createCollapsibleCardBody(key, form, section.html_description);
        card.appendChild(cardBody); 
        accordion.appendChild(card);
    }
   
    // Add submit button to accordion
    let submitButton = document.createElement("button");
    submitButton.innerHTML = "Submit Report";
    submitButton.type = "submit";
    submitButton.classList.add("btn", "btn-primary", "btn-lg", "btn-block"); // TODO: add eventListener
    accordion.appendChild(submitButton);

    fragment.appendChild(accordion) 
    col.appendChild(fragment);

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
