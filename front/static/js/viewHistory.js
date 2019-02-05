// Hack to change endpoint url
function getEndpointDomain() {
    return "https://" + window.location.hostname + ":8444/";
}

// Make a GET request to url and pass response to callback function
function getDataFromEndpoint(url, callback) {
    const token = localStorage.getItem("token");
    const xhr = new XMLHttpRequest();

    console.log("Attempting a connection to the following endpoint: " + url);


    xhr.open("GET", url, true);
    xhr.setRequestHeader("Authorization", "Bearer " + token);
    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                console.log("GET SUCCESS!");
                console.log("Server response:\n" + this.response);
                parsedData = JSON.parse(this.response);
                callback(parsedData);
            } else {
                console.error("GET FAILURE!");
                console.error("Server status: " + this.status);
                console.error("Server response:\n" + this.response);
            }
        }
    };

    xhr.onerror = function() {
        alert("Connection error!");
    };

    xhr.send();
}

// Wraps a Bootstrap form group around a field
function createFormGroup(key, field) {
    const formGroup = document.createElement("div")
    formGroup.classList.add("form-group", "row");

    const label = document.createElement("label");
    label.classList.add("col-sm-4", "col-form");
    label.innerHTML = field.label + ": ";
    label.setAttribute("for", key);
    
    const div = document.createElement("div");
    div.classList.add("col-sm-6");

    const input = document.createElement("input");
    input.name = key;
    input.id = key;

    switch(field.type) {
        case "boolean":
            input.type = "checkbox";
            if (field.value === true)
                input.setAttribute("checked", "checked");
            input.classList.add("form-check-input");
            label.className = "";
            label.classList.add("form-check-label");
            outerLabel = document.createElement("div");
            outerLabel.classList.add("col-sm-4");
            outerLabel.innerHTML = "Flight type: ";
            formCheck = document.createElement("div");
            formCheck.classList.add("form-check");
            formCheck.appendChild(input);
            formCheck.appendChild(label);
            div.appendChild(formCheck);
            formGroup.appendChild(outerLabel);
            formGroup.appendChild(div);
            break;
        case "date":
        case "decimal":
            input.type = "text";
            input.value = field.value;
            input.classList.add("form-control");
            formGroup.appendChild(label);
            div.appendChild(input)
            formGroup.appendChild(div);
            break;
        case "file":
            input.type = "file";
            input.classList.add("form-control-file");
            let uploadMessage = document.createElement("p");
            uploadMessage.classList.add("form-text");
            uploadMessage.innerHTML = field.value;
            div.appendChild(input)
            div.appendChild(uploadMessage);
            formGroup.appendChild(label);
            formGroup.appendChild(div);
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

function createCollapsibleCardBody(key, form, sectionDescription, sectionCompleted) {
    // Create wrapper div
    const div = document.createElement("div");
    const sectionAlert = document.createElement("div");

    if (sectionCompleted) {
        div.classList.add("collapse");
        sectionAlert.classList.add("alert", "alert-success");
        sectionAlert.innerHTML = "This section is complete";
    } else {
        div.classList.add("collapse", "show");
        sectionAlert.classList.add("alert", "alert-danger");
        sectionAlert.innerHTML = "This section is not complete";
    }

    div.setAttribute("data-parent", "#editReportAccordion");
    div.id = "collapse" + key;

    // Create card body. Append form to body, body to wrapper div
    const cardBody = document.createElement("div");
    cardBody.classList.add("card-body");
    cardBody.appendChild(sectionAlert);
    cardBody.insertAdjacentHTML("beforeend", sectionDescription); 
    cardBody.appendChild(form);
    div.appendChild(cardBody);
    
    return div;
}

function createEditReportForm(parsedData) {
    const modalBody = document.querySelector(".modal-body");
    const modalLabel = document.querySelector("#editReportModalLabel");

    while (modalBody.firstChild) {
        modalBody.removeChild(modalBody.firstChild);
    }

    // Add report title and date
    const reportTitle = parsedData.title;
    const dateCreated = new Date(parsedData.date_created).toLocaleDateString("en-US");
    modalLabel.innerHTML = reportTitle + " " + dateCreated;

    // Create accordion
    const accordion = document.createElement("div");
    accordion.classList.add("accordion");
    accordion.id = "editReportAccordion";

    // Traverse the report's sections array
    const sections = parsedData.sections;
    for (let key in sections) {
        let section = sections[key];
        let collapsibleCard = createCollapsibleCard(key, section.title)

        // Create a new form with the section key index as id
        let form = document.createElement("form");
        form.classList.add("form");
        form.id = "form" + key;

        // Traverse the fields of this section
        let fields = section.fields;
        for (let key in fields) {
            let field = fields[key];

            console.log("Field label: " + field.label); 
            console.log("Field type: " + field.type); 
            console.log("Field value: " + field.value); 
            
            // Create a form group for each field and add it to the form
            let formGroup = createFormGroup(key, field);
            form.appendChild(formGroup);
        }

        // Add save button to the current form
        let saveButton = document.createElement("button");
        saveButton.innerHTML = "Save";
        saveButton.type = "submit";
        saveButton.classList.add("btn", "btn-primary"); // TODO: add eventListener
        form.appendChild(saveButton);

        // Create collapsible card body, append form to it, append card to accordion
        let cardBody = createCollapsibleCardBody(key, form, section.html_description, section.completed);
        collapsibleCard.appendChild(cardBody); 
        accordion.appendChild(collapsibleCard);
    }
   
    modalBody.appendChild(accordion);
}

function displayListOfReports(parsedData) {
    const reports = parsedData.reports;

    if (reports.length === 0) {
        const cardBody = document.querySelector(".card-body");
        const p = document.createElement("p");
        p.innerHTML = "No reports found.";
        cardBody.appendChild(p);
    } else {
        const table = document.querySelector("table");
        const tbody = document.querySelector("tbody");

        // Insert data into the table row
        for (let i = 0; i < reports.length; i++) {
            let title = reports[i].title;
            let dateCreated = new Date(reports[i].date_created).toLocaleDateString("en-US");
            let state = reports[i].submitted;
            let dateSubmitted;
            let rid = reports[i].report_pk;

            let bodyRow = tbody.insertRow(i); 
            bodyRow.insertCell(0).innerHTML = title;
            bodyRow.insertCell(1).innerHTML = dateCreated; 

            let stateCell = bodyRow.insertCell(2);
            stateCell.innerHTML = state;
            stateCell.classList.add("d-none", "d-lg-table-cell"); // Column visible only on large displays

            // Create edit/view button
            let actionButton = document.createElement("button");
            actionButton.type = "submit";
            actionButton.setAttribute("data-rid", rid);
            actionButton.classList.add("btn");

            if (state === false) {
                // Edit button
                dateSubmitted = "TBD";
                actionButton.classList.add("btn-primary", "edit-report-button"); // Add event listener class
                actionButton.innerHTML = "Edit";
                actionButton.setAttribute("data-toggle", "modal");
                actionButton.setAttribute("data-target", "#editReportModal");
            } else {
                // View button
                dateSubmitted = new Date(reports[i].date_submitted).toLocaleDateString("en-US");
                actionButton.classList.add("btn-success", "view-report-button");
                actionButton.innerHTML = "View";
            }

            let dateSubmittedCell = bodyRow.insertCell(3);
            dateSubmittedCell.innerHTML = dateSubmitted;
            dateSubmittedCell.classList.add("d-none", "d-md-table-cell"); // Column visible on medium and larger displays
            bodyRow.insertCell(4).appendChild(actionButton);
        }

        table.style.visibility = "visible";
    }
}

function displayReport(parsedData){
    window.alert(parsedData.date_created); //Able to get the correct report ID now just needs to display the
    //report as an modual
}

document.addEventListener("DOMContentLoaded", function(event) {
    const url = getEndpointDomain() + "api/v1/reports";
    getDataFromEndpoint(url, displayListOfReports);
});

document.addEventListener("click", function(event) {
    if (event.target && event.target.classList.contains("edit-report-button")) {
        console.log("Edit button clicked");
        const url = getEndpointDomain() + "api/v1/report/" + event.target.dataset.rid;
        getDataFromEndpoint(url, createEditReportForm);
    }
    if(event.target && event.target.classList.contains("view-report-button"))
    {
        console.log("View button clicked");
        const url = getEndpointDomain() + "api/v1/report/" + event.target.dataset.rid;
        getDataFromEndpoint(url, displayReport);
    }
    // TODO: Add view report
});
