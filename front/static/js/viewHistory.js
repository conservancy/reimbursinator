const reportType = {
    NEW : 1,
    EDIT : 2,
    VIEW : 3
};

// Hack to change endpoint url
function getEndpointDomain() {
    return "https://" + window.location.hostname + ":8444/";
}

function alertCallback(parsedData) {
    alert(JSON.stringify(parsedData));
}

function makeAjaxRequest(method, url, callback, type, payload) {
    const token = localStorage.getItem("token");
    const xhr = new XMLHttpRequest();

    console.log("Attempting a connection to the following endpoint: " + url);

    xhr.open(method, url, true);
    xhr.setRequestHeader("Authorization", "Bearer " + token);

    switch (method) {
        case "PUT":
            break;
        case "POST":
            xhr.setRequestHeader("Content-Type", "application/json");
            break;
        default:
            payload = null;
            break;
    }

    xhr.onreadystatechange = function() {
        if (this.readyState === 4) {
            if (this.status === 200) {
                console.log(method + " SUCCESS!");
                console.log("Server response:\n" + this.response);
                let parsedData = JSON.parse(this.response);
                type ? callback(parsedData, type) : callback(parsedData);
            } else {
                console.error(method + " FAILURE!");
                console.error("Server status: " + this.status);
                console.error("Server response:\n" + this.response);
            }
        }
    };

    xhr.onerror = function() {
        alert("Connection error!");
    };

    xhr.send(payload);
}

// Wraps a Bootstrap form group around a field
function createFormGroup(field) {
    const formGroup = document.createElement("div")
    formGroup.classList.add("form-group", "row");

    const label = document.createElement("label");
    label.classList.add("col-sm-4", "col-form");
    label.innerHTML = field.label + ": ";
    label.setAttribute("for", field.field_name);

    const div = document.createElement("div");
    div.classList.add("col-sm-6");

    const input = document.createElement("input");
    input.name = field.field_name;
    input.id = field.field_name;

    switch(field.type) {
        case "boolean":
            input.type = "checkbox";
            if (field.value === true)
                input.setAttribute("checked", "checked");
            input.classList.add("form-check-input");
            label.className = "";
            label.classList.add("form-check-label");
            label.innerHTML = field.label;
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
        case "string":
            input.type = "text";
            input.value = field.value;
            input.classList.add("form-control");
            formGroup.appendChild(label);
            div.appendChild(input)
            formGroup.appendChild(div);
            break;
        case "decimal":
            input.type = "text";
            input.value = field.value;
            input.classList.add("form-control");
            input.pattern = "\\d+(\\.\\d{2})?";
            formGroup.appendChild(label);
            div.appendChild(input)
            formGroup.appendChild(div);
            break;
        case "integer":
            input.type = "number";
            input.value = field.value;
            input.classList.add("form-control");
            input.step = 1;
            input.min = 0;
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

function createCollapsibleCardBody(key, form, type, sectionDescription, sectionCompleted) {
    // Create wrapper div
    const div = document.createElement("div");
    div.id = "collapse" + key;
    const sectionAlert = document.createElement("div");
    const cardBody = document.createElement("div");
    cardBody.classList.add("card-body");

    if (sectionCompleted) {
        div.classList.add("collapse");
        sectionAlert.classList.add("alert", "alert-success");
        sectionAlert.innerHTML = "This section is complete";
    } else {
        div.classList.add("collapse", "show");
        sectionAlert.classList.add("alert", "alert-danger");
        sectionAlert.innerHTML = "This section is not complete";
    }

    if (type === reportType.EDIT) {
        div.setAttribute("data-parent", "#editReportAccordion");
    } else {
        div.setAttribute("data-parent", "#newReportAccordion");
    }

    // Create card body. Append form to body, body to wrapper div
    cardBody.appendChild(sectionAlert);
    cardBody.insertAdjacentHTML("beforeend", sectionDescription);
    cardBody.appendChild(form);
    div.appendChild(cardBody);

    return div;
}

function createReportForm(parsedData, type) {
    let modalBody;
    let modalLabl;
    const accordion = document.createElement("div");
    accordion.classList.add("accordion");

    if (type === reportType.EDIT) {
        modalBody = document.querySelector("#editReportModalBody");
        modalLabel = document.querySelector("#editReportModalLabel");
        accordion.id = "editReportAccordion";
        const deleteButton = document.querySelector(".delete-report");
        if (deleteButton) {
            deleteButton.setAttribute("data-rid", parsedData.report_pk);
        }
    } else if (type === reportType.NEW) {
        modalBody = document.querySelector("#newReportModalBody");
        modalLabel = document.querySelector("#newReportModalLabel");
        accordion.id = "newReportAccordion";
    } else {
        return;
    }

    while (modalBody.firstChild) {
        modalBody.removeChild(modalBody.firstChild);
    }

    // Add report title and date
    const reportTitle = parsedData.title;
    modalLabel.innerHTML = reportTitle;

    // Traverse the report's sections array
    const sections = parsedData.sections;
    for (let key in sections) {
        let section = sections[key];
        let collapsibleCard = createCollapsibleCard(key, section.title)

        // Create a new form with the section key index as id
        let form = document.createElement("form");
        form.classList.add("form", "section-form");
        form.id = "form" + key;
        form.setAttribute("data-rid", parsedData.report_pk);
        form.setAttribute("data-sid", section.id);

        // Traverse the fields of this section
        let fields = section.fields;
        for (let key in fields) {
            let field = fields[key];

            console.log("Field label: " + field.label);
            console.log("Field type: " + field.type);
            console.log("Field value: " + field.value);

            // Create a form group for each field and add it to the form
            let formGroup = createFormGroup(field);
            form.appendChild(formGroup);
        }

        // Add save button to the current form
        let saveButton = document.createElement("button");
        saveButton.innerHTML = "Save";
        saveButton.type = "submit";
        saveButton.classList.add("btn", "btn-primary", "save-section"); // TODO: add eventListener
        form.appendChild(saveButton);

        // Create collapsible card body, append form to it, append card to accordion
        let cardBody = createCollapsibleCardBody(key, form, type, section.html_description, section.completed);
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
                actionButton.setAttribute("data-toggle", "modal");
                actionButton.setAttribute("data-target", "#viewReportModal");
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
    //Able to get the correct report ID now just needs to display the
    //report as an modual
    const modalBody = document.querySelector(".modal-view");
    const modalLabel = document.querySelector("#viewReportModalLabel");

    while (modalBody.firstChild) {
        modalBody.removeChild(modalBody.firstChild);
    }

    // Add report title and date
    const reportTitle = parsedData.title;
    const dateCreated = new Date(parsedData.date_created).toLocaleDateString("en-US");
    modalLabel.innerHTML = reportTitle + " " + dateCreated;

    const card = document.createElement("div");
    card.classList.add("card");

    const cardHeader = document.createElement("div");
    cardHeader.classList.add("card-header");

    const cardBody = document.createElement("div");
    cardBody.classList.add("card-body");

    const sections = parsedData.sections;
    for (let key in sections) {
        let section = sections[key];
        if(section.completed) {
            const h4 = document.createElement("h4");
            const value = document.createTextNode(section.title);

            h4.appendChild(value);
            cardBody.appendChild(h4);
            let fields = section.fields;
            for (let key in fields) {
                let field = fields[key];
                const p1 = document.createElement("p");
                if(field.type === "boolean")
                {
                    let p1Value = document.createTextNode(field.label+ ": ");
                    let icon = document.createElement("input");
                    icon.setAttribute("type", "checkbox");
                    icon.setAttribute("disabled", "disabled");
                    if(field.value == "true")
                    {
                        icon.setAttribute("checked", "checked");
                    }
                    p1.appendChild(p1Value);
                    p1.appendChild(icon);
                    cardBody.appendChild(p1);
                }
                else if(field.value === null)
                {
                    let p1Value = document.createTextNode(field.label + ": " + "N/A");
                    p1.appendChild(p1Value);
                    cardBody.appendChild(p1);
                }
                else
                {
                    let p1Value = document.createTextNode(field.label + ": " + field.value);
                    p1.appendChild(p1Value);
                    cardBody.appendChild(p1);
                }
            }
            cardHeader.appendChild(cardBody);
            card.appendChild(cardHeader);
        }
    }

    modalBody.appendChild(card);
}

document.addEventListener("DOMContentLoaded", function(event) {
    if (window.location.pathname === "/edit_report.html") {
        const url = getEndpointDomain() + "api/v1/reports";
        makeAjaxRequest("GET", url, displayListOfReports);
    }
});

document.addEventListener("click", function(event) {
    if (event.target) {
        if (event.target.classList.contains("edit-report-button")) {
            const url = getEndpointDomain() + "api/v1/report/" + event.target.dataset.rid;
            const type = reportType.EDIT;
            makeAjaxRequest("GET", url, createReportForm, type);
        } else if (event.target.classList.contains("view-report-button")) {
            console.log("View button clicked");
            const url = getEndpointDomain() + "api/v1/report/" + event.target.dataset.rid;
            makeAjaxRequest("GET", url, displayReport);
        } else if (event.target.classList.contains("delete-report")) {
            event.preventDefault();
            const title = document.querySelector("#editReportModalLabel").textContent;
            const result = confirm("Are you sure you want to delete the report \"" + title + "\"?");
            if (result) {
                const url = getEndpointDomain() + "api/v1/report/" + event.target.dataset.rid;
                makeAjaxRequest("DELETE", url, function(parsedData) {
                    alert(parsedData.message);
                    location.reload(true);
                });
            }
        }
    }
});

const newReportForm = document.querySelector(".new-report-form");
if (newReportForm) {
    newReportForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const url = getEndpointDomain() + "api/v1/report";
        const payload = JSON.stringify({ "title": event.target.elements.title.value });
        console.log("Payload:\n" + payload);
        const type = reportType.NEW;
        makeAjaxRequest("POST", url, createReportForm, type, payload);
        this.reset();
    });
}

document.addEventListener("submit", function(event) {
    if (event.target.classList.contains("section-form")) {
        event.preventDefault();
        console.log(event.target);
        const formData = new FormData(event.target);
        const url = getEndpointDomain() + "api/v1/report/" + event.target.dataset.rid + "/section/" + event.target.dataset.sid;
        makeAjaxRequest("PUT", url, alertCallback, null, formData);
    }
});
