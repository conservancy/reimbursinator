const reportType = {
    NEW : 1,
    EDIT : 2
};

// Hack to change endpoint url
function getEndpointDomain() {
    return "https://" + window.location.hostname + ":8444/";
}

/*
XMLHttpRequest wrapper for requesting or sending data to/from the backend

method (string): HTTP request type
url (string): the url of an api endpoint
callback (function): function to execute on success
optional: optional argument
payload (JSON): optional JSON payload
returns: n/a
*/
function makeAjaxRequest(method, url, callback, optional, payload) {
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
                optional ? callback(parsedData, optional) : callback(parsedData);
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

/*
Disables a button and changes its display text

button (object): the button to update
buttonText (string): the new display text
returns: n/a
*/
function animateButton(button, buttonText) {
    button.disabled = true;
    button.innerHTML = "";
    let span = document.createElement("span");
    span.classList.add("spinner-border", "spinner-border-sm");
    button.appendChild(span);
    button.appendChild(document.createTextNode(buttonText));
}


/*
Updates a section's header and footer based on its current state

parsedData (object): Object representing a section's data
saveButton (object): the button to update
returns: n/a
*/
function updateSection(parsedData, saveButton) {
    const sectionIdStr = "#section-" + parsedData.id + "-";
    const sectionState = document.querySelector(sectionIdStr + "state");
    const collapseDiv = document.querySelector(sectionIdStr + "collapse");

    // A completed section gets a header icon
    if (parsedData.completed) {
        const sectionAlert = collapseDiv.querySelector(".section-alert");
        if (sectionAlert) {
            collapseDiv.firstElementChild.removeChild(sectionAlert);
        }
        if (parsedData.rule_violations.length === 0) {
            // Complete with no rule violations
            sectionState.classList = "fas fa-check-square";
            collapseDiv.className = "collapse";
        } else {
            // Complete but with rule violations
            sectionState.classList = "fas fa-exclamation-triangle";
        }
    }

    // Add card footer with rule violations if needed
    const cardFooter = createCardFooter(parsedData.rule_violations);
    if (collapseDiv.lastElementChild.classList.contains("card-footer")) {
        collapseDiv.removeChild(collapseDiv.lastElementChild);
        if (cardFooter) {
            collapseDiv.appendChild(cardFooter);
        }
    } else {
        if (cardFooter) {
            collapseDiv.appendChild(cardFooter);
        }
    }

    saveButton.innerHTML = "Save";
    saveButton.disabled = false;
}

/*
Wraps a Bootstrap form group around a field

sectionIdStr (string): section id prefix
field (object): Object representing a field
returns: div element with form group styling
*/
function createFormGroup(sectionIdStr, field) {
    const inputId = sectionIdStr + field.field_name;
    const formGroup = document.createElement("div")
    formGroup.classList.add("form-group", "row");

    const label = document.createElement("label");
    label.classList.add("col-sm-4", "col-form");
    label.innerHTML = field.label + ": ";
    label.setAttribute("for", inputId);

    const div = document.createElement("div");
    div.classList.add("col-sm-6");

    const input = document.createElement("input");
    input.name = field.field_name;
    input.id = inputId;

    switch(field.field_type) {
        case "boolean":
            const select = document.createElement("select");
            select.name = field.field_name;
            select.id = inputId;
            select.classList.add("form-control");
            const yesOption = document.createElement("option");
            yesOption.innerHTML = "Yes";
            yesOption.value = "true";
            const noOption = document.createElement("option");
            noOption.innerHTML = "No";
            noOption.value = "false";
            if (field.value === true) {
                yesOption.setAttribute("selected", "selected");
            } else {
                noOption.setAttribute("selected", "selected");
            }
            select.appendChild(yesOption);
            select.appendChild(noOption);
            formGroup.appendChild(label);
            div.appendChild(select)
            formGroup.appendChild(div);
            break;
        case "date":
            input.type = "date";
            input.placeholder = "mm-dd-yyyy";
            if (field.value === "None") {
                input.value = "";
            } else {
                input.value = field.value;
            }
            input.classList.add("form-control");
            formGroup.appendChild(label);
            div.appendChild(input)
            formGroup.appendChild(div);
            break;
        case "string":
            input.type = "text";
            input.value = field.value;
            input.classList.add("form-control");
            formGroup.appendChild(label);
            div.appendChild(input)
            formGroup.appendChild(div);
            break;
        case "decimal":
            input.type = "number";
            if (field.value === "0.00") {
                input.value = "";
            } else {
                input.value = field.value;
            }
            input.classList.add("form-control");
            input.step = 0.01;
            input.min = 0.00;
            formGroup.appendChild(label);
            div.appendChild(input)
            formGroup.appendChild(div);
            break;
        case "integer":
            input.type = "number";
            if (field.value === 0) {
                input.value = "";
            } else {
                input.value = field.value;
            }
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

/*
Creates a card and card header

sectionIdStr (string): section id prefix
sectionTitle (string): section title for the collapse button
sectionCompleted (boolean): flag indicating section state
ruleViolations (array): list of policy rule violations for this section
returns: div element with card styling
*/
function createCollapsibleCard(sectionIdStr, sectionTitle, sectionCompleted, ruleViolations) {
    // Create card and header
    const card = document.createElement("div");
    card.classList.add("card");
    const cardHeader = document.createElement("div");
    cardHeader.classList.add("card-header");
    const sectionState = document.createElement("i");
    sectionState.id = sectionIdStr + "state";

    // A completed section gets a header icon
    if (sectionCompleted) {
        if (ruleViolations.length === 0) {
            sectionState.classList.add("fas", "fa-check-square");
        } else {
            sectionState.classList.add("fas", "fa-exclamation-triangle");
        }
    }

    // Create h2, button. Append button to h2, h2 to header, and header to card
    const h2 = document.createElement("h2");
    h2.classList.add("mb-0");
    const button = document.createElement("button");
    button.classList.add("btn", "btn-link");
    button.type = "button";
    button.setAttribute("data-toggle", "collapse");
    button.setAttribute("data-target", "#" + sectionIdStr + "collapse");
    button.innerHTML = sectionTitle;
    h2.appendChild(button);
    h2.appendChild(sectionState);
    cardHeader.appendChild(h2);
    card.appendChild(cardHeader);

    return card;
}

/*
Creates a collapsible card body

form (HTML element): form element
sectionIdStr (string): section id prefix
sectionDescription (string): HTML string description of this section
sectionCompleted (boolean): flag indicating section state
ruleViolations (array): list of policy rule violations for this section
returns: div element with collapse styling
*/
function createCollapsibleCardBody(form, sectionIdStr, sectionDescription, sectionCompleted, ruleViolations) {
    // Create wrapper div
    const collapseDiv = document.createElement("div");
    collapseDiv.id = sectionIdStr + "collapse";
    const cardBody = document.createElement("div");
    cardBody.classList.add("card-body");
    const sectionAlert = document.createElement("div");

    if (sectionCompleted && ruleViolations.length === 0) {
        collapseDiv.classList.add("collapse");
    } else if (sectionCompleted && ruleViolations.length > 0) {
        collapseDiv.classList.add("collapse", "show");
    } else {
        // Add section alert
        sectionAlert.classList.add("alert", "alert-danger", "section-alert");
        sectionAlert.innerHTML = "This section is not complete";
        collapseDiv.classList.add("collapse", "show");
    }

    // Create card body. Append form to body, body to wrapper div
    cardBody.appendChild(sectionAlert);
    cardBody.insertAdjacentHTML("beforeend", sectionDescription);
    cardBody.appendChild(form);
    collapseDiv.appendChild(cardBody);

    return collapseDiv;
}

/*
Creates a card footer and populates it with rule violations

ruleViolations (array): a list of policy rule violations
returns: div element with card footer styling
*/
function createCardFooter(ruleViolations) {
    if (ruleViolations.length === 0) {
        return null;
    }

    const cardFooter = document.createElement("div");
    cardFooter.classList.add("card-footer");
    const violationMessage = document.createElement("div");
    violationMessage.classList.add("alert", "alert-danger");
    const heading = document.createElement("div");
    heading.innerHTML = "Rule Violations";
    heading.classList.add("alert-heading");
    violationMessage.appendChild(heading);
    violationMessage.appendChild(document.createElement("hr"));

    for (let i = 0; i < ruleViolations.length; i++) {
        let violation = document.createElement("p");
        let violationLabel = document.createElement("strong");
        violationLabel.innerHTML = ruleViolations[i].label;
        violation.appendChild(violationLabel);
        violation.appendChild(document.createElement("br"));
        let ruleBreakText = document.createTextNode(ruleViolations[i].rule_break_text);
        violation.appendChild(ruleBreakText);
        violationMessage.appendChild(violation);
    }

    cardFooter.appendChild(violationMessage);
    return cardFooter;
}

/*
Creates a form within a modal popup

parsedData (object): Object representing report data
type (number): The report type (edit or new)
returns: n/a
*/
function createReportForm(parsedData, type) {
    let modalBody;
    let modalLabel;
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

    const reviewButton = document.querySelector(".review-report");
    if (reviewButton) {
        reviewButton.setAttribute("data-rid", parsedData.report_pk);
    }
    const finalizeButton = document.querySelector(".finalize-report");
    if (finalizeButton) {
        finalizeButton.setAttribute("data-rid", parsedData.report_pk);
    }

    while (modalBody.firstChild) {
        modalBody.removeChild(modalBody.firstChild);
    }

    // Add report title and date
    modalLabel.innerHTML = parsedData.title;

    // Traverse the report's sections array
    const sections = parsedData.sections;
    for (let i = 0; i < sections.length; i++) {

        // Create a new form
        let sectionIdStr = "section-" + sections[i].id + "-";
        let form = document.createElement("form");
        form.classList.add("form", "section-form");
        form.id = sectionIdStr + "form";
        form.setAttribute("data-rid", parsedData.report_pk);
        form.setAttribute("data-sid", sections[i].id);

        // Traverse the fields of this section
        let fields = sections[i].fields;
        for (let j = 0; j < fields.length; j++) {
            // Create a form group for each field and add it to the form
            form.appendChild(createFormGroup(sectionIdStr, fields[j]));
        }

        // Add save button to the current form
        let saveButton = document.createElement("button");
        saveButton.innerHTML = "Save";
        saveButton.type = "submit";
        saveButton.classList.add("btn", "btn-primary", "save-section");
        form.appendChild(saveButton);

        // Create collapsible card body, append form to it, append card to accordion
        let cardBody = createCollapsibleCardBody(form, sectionIdStr,
            sections[i].html_description, sections[i].completed, sections[i].rule_violations);
        let cardFooter = createCardFooter(sections[i].rule_violations);
        if (cardFooter) {
            cardBody.appendChild(cardFooter);
        }
        let collapsibleCard = createCollapsibleCard(sectionIdStr, sections[i].title,
            sections[i].completed, sections[i].rule_violations)
        collapsibleCard.appendChild(cardBody);
        accordion.appendChild(collapsibleCard);
    }

    modalBody.appendChild(accordion);
}

/*
Displays a table containing all of a user's reports

parsedData (object): Object representing report data
returns: n/a
*/
function displayListOfReports(parsedData) {
    const reports = parsedData.reports;
    const cardBody = document.querySelector(".card-body");
    const table = document.querySelector("table");
    cardBody.removeChild(cardBody.firstElementChild); // remove loading spinner

    if (reports.length === 0) {
        cardBody.removeChild(table);
        const h5 = document.createElement("h5");
        h5.innerHTML = "No reports found.";
        h5.classList.add("text-center");
        cardBody.appendChild(h5);
    } else {
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

            let dateSubmittedCell = bodyRow.insertCell(2);
            dateSubmittedCell.innerHTML = dateSubmitted;
            dateSubmittedCell.classList.add("d-none", "d-md-table-cell"); // Column visible on medium and larger displays
            bodyRow.insertCell(3).appendChild(actionButton);
        }

        table.style.visibility = "visible";
    }
}

/*
Populates modal popup with a readonly, finalized report

parsedData (object): Object representing report data
returns: n/a
*/
function displayReport(parsedData){
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
                let p1Value = "";
                if(field.field_type == "boolean")
                {
                    if(field.value == true)
                    {
                        p1Value = document.createTextNode(field.label + ": " + "Yes");
                        p1.appendChild(p1Value);
                        cardBody.appendChild(p1);
                    }
                    else
                    {
                        p1Value = document.createTextNode(field.label + ": " + "No");
                        p1.appendChild(p1Value);
                        cardBody.appendChild(p1);
                    }
                }
                else if(field.value == "")
                {
                    p1Value = document.createTextNode(field.label + ": " + "None");
                    p1.appendChild(p1Value);
                    cardBody.appendChild(p1);
                }
                else
                {
                    p1Value = document.createTextNode(field.label + ": " + field.value);
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

// Display list of reports on page load
document.addEventListener("DOMContentLoaded", function(event) {
    if (window.location.pathname === "/edit_report.html") {
        const url = getEndpointDomain() + "api/v1/reports";
        makeAjaxRequest("GET", url, displayListOfReports);
    }
});

// Listens for button click events
document.addEventListener("click", function(event) {
    if (event.target) {
        if (event.target.classList.contains("edit-report-button")) {
            // Edit button clicked
            const url = getEndpointDomain() + "api/v1/report/" + event.target.dataset.rid;
            const type = reportType.EDIT;
            makeAjaxRequest("GET", url, createReportForm, type);
        } else if (event.target.classList.contains("view-report-button")) {
            // View button clicked
            console.log("View button clicked");
            const url = getEndpointDomain() + "api/v1/report/" + event.target.dataset.rid;
            makeAjaxRequest("GET", url, displayReport);
        } else if (event.target.classList.contains("review-report")) {
            // Submit for review button clicked
            event.preventDefault();
            const result = confirm("Are you sure you want to submit this report for review?");
            if (result) {
                animateButton(event.target, "  Submitting...");
                const url = getEndpointDomain() + "api/v1/report/" + event.target.dataset.rid;
                makeAjaxRequest("PUT", url, function(parsedData) {
                    event.target.disabled = false;
                    event.target.innerHTML = "Submit for Review";
                    alert(parsedData.message);
                    location.reload(true);
                });
            }
        } else if (event.target.classList.contains("finalize-report")) {
            // Finalize report button clicked
            event.preventDefault();
            console.log("finalize-report");
            const result = confirm("Are you sure you want to finalize this report? This means you will no longer be able to modify it.");
            if (result) {
                animateButton(event.target, "  Submitting...");
                const url = getEndpointDomain() + "api/v1/report/" + event.target.dataset.rid + "/final";
                makeAjaxRequest("PUT", url, function(parsedData) {
                    event.target.disabled = false;
                    event.target.innerHTML = "Finalize Report";
                    alert(parsedData.message);
                    location.reload(true);
                });
            }
        } else if (event.target.classList.contains("delete-report")) {
            // Delete report button clicked
            event.preventDefault();
            const title = document.querySelector("#editReportModalLabel").textContent;
            const result = confirm("Are you sure you want to delete the report \"" + title + "\"?");
            if (result) {
                animateButton(event.target, "  Deleting...");
                const url = getEndpointDomain() + "api/v1/report/" + event.target.dataset.rid;
                makeAjaxRequest("DELETE", url, function(parsedData) {
                    event.target.disabled = false;
                    event.target.innerHTML = "Delete Report";
                    alert(parsedData.message);
                    location.reload(true);
                });
            }
        }
    }
});

// Listens for a create report submission
const newReportForm = document.querySelector(".new-report-form");
if (newReportForm) {
    newReportForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const url = getEndpointDomain() + "api/v1/report";
        const payload = JSON.stringify({ "title": event.target.elements.title.value, "reference": event.target.elements.reference.value });
        console.log("Payload:\n" + payload);
        const type = reportType.NEW;
        makeAjaxRequest("POST", url, createReportForm, type, payload);
    });
}

// Listens for a date input
document.addEventListener("input", function(event) {
    if (event.target.type === "date") {
        if (!moment(event.target.value, "YYYY-MM-DD", true).isValid()) {
            event.target.setCustomValidity("Invalid date format");
        } else {
            event.target.setCustomValidity("");
        }
    }
});

// Listens for a section saving event
document.addEventListener("submit", function(event) {
    if (event.target.classList.contains("section-form")) {
        event.preventDefault();
        let saveButton = event.target.lastElementChild;
        animateButton(saveButton, "  Saving...");
        const formData = new FormData(event.target);
        const url = getEndpointDomain() + "api/v1/section/" + event.target.dataset.sid;
        makeAjaxRequest("PUT", url, updateSection, saveButton, formData);
    }
});

// Jquery is required to handle this modal event
$(document).ready(function(){
    $("#newReportModal").on('hidden.bs.modal', function() {
        location.reload(true);
    });
});
