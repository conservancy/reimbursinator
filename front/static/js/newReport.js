// Make a GET request to url and pass response to callback function
function fetDataFromEndpoint(event){
  event.preventDefault();

  const titleName = document.getElementById("title");

  const url = "https://reqres.in/api/createReport" // mock api service
  const xhr = new XMLHttpRequest();

  console.log(`title:\n${JSON.stringify(titleName)}`);

  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-Type", "application/json");
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

// Wraps a Bootstrap form group around a field
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
            formGroup.appendChild(label);
            formGroup.appendChild(input);
            let uploadMessage = document.createTextNode("Uploaded file:");
            formGroup.appendChild(uploadMessage);
            const link = document.createElement("a");
            link.href = field.value;
            link.innerHTML = field.value;
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

    return card;
}

function createCollapsibleCardBody(key, form, sectionDescription, sectionCompleted) {
    // Create wrapper div
    const div = document.createElement("div");
    sectionCompleted ? div.classList.add("collapse") : div.classList.add("collapse", "show");
    div.setAttribute("data-parent", "#createReportAccordion");
    div.id = "collapse" + key;

    // Create card body. Append form to body, body to wrapper div
    const cardBody = document.createElement("div");
    cardBody.classList.add("card-body");
    cardBody.insertAdjacentHTML("beforeend", sectionDescription);
    cardBody.appendChild(form);
    div.appendChild(cardBody);

    return div;
}

function createEmptyReportForm(parsedData){
    const col = document.querySelector(".col-sm-8");

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
    accordion.id = "createReportAccordion";

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

            console.log(`Field label: ${field.label}`);
            console.log(`Field type: ${field.type}`);
            console.log(`Field value: ${field.value}`);

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

    // Add submit button to accordion
    let submitButton = document.createElement("button");
    submitButton.innerHTML = "Submit Report";
    submitButton.type = "submit";
    submitButton.classList.add("btn", "btn-primary", "btn-lg", "btn-block"); // TODO: add eventListener
    accordion.appendChild(submitButton);

    fragment.appendChild(accordion)
    col.appendChild(fragment);

}
