# Reimbursinator

Reimbursinator was developed by students at Portland State University with the sponsorship of Software Freedom Conservancy as an open source expense management solution with customizable policy rules. The front end is written in Javascript, with a back end API served by Django. The project is configured to be run using Docker containers.

## Development

Developed by: Daniel Dupriest, Logan Miller, Jack, Joe Arriaga, Preston, Rupika Dikkala, Shuaiyi Liang

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

## License
Reimbursinator is licensed under the [GNU Affero General Public License v3.0](https://opensource.org/licenses/AGPL-3.0)

## Features

- report format defined by policy file
- 6 data field types
  - boolean
  - string
  - integer
  - decimal
  - date
  - file
- custom data validation through Python functions

## Installation

To try out a temporary instance of Reimbursinator using the Docker configuration present in the repository, follow the instructions on the [Docker Deployment wiki page](https://github.com/danieldupriest/reimbursinator/wiki/Docker-Deployment).

To install a production version of Reimbursinator you will need to configure servers for:
- Serving front-end html files (e.g. Nginx)
- Running the Django backend (e.g. Gunicorn)
- (optional) Serving Django admin CSS/JS. (e.g. Nginx)

### Front End

Serve the content of `front/static/` using the http server of your choice.

### Back End

#### Django settings

Edit the `back/reimbursinator/settings.py` file and change the following lines to match the correct IP or domain name.

- `ALLOWED_HOSTS` - This tells Django which front end addresses should be served. It should include the address of the server providing the content of `front/`.
- `CORS_ORIGIN_WHITELIST` - This tells Django which front end addresses to provide CORS headers for. Include the same information here. (include port if necessary)
- `STATIC_URL` - This tells Django where admin css/js will be served from.
- `LOGIN_URL` and `LOGIN_REDIRECT_URL` - These should point to your front page, including port if necessary. e.g. `https://192.168.99.100:8443`

Also replace the `SECRET_KEY` value with your own and set `DEBUG` to False.

#### Email settings

The project is configured to use a gmail account as the system SMTP server. The configuration settings for this are stored in the `back/.env` file. If you will be using a gmail account in this way, you may replace the file's contents with your own settings.

If you will use your own SMTP server, it may be best to forego the .env file and edit the Django email settings in `back/reimbursinator/settings.py` directly.

#### Server environment

To use `pipenv` to run Reimbursinator with the versions defined in the project:

1. Ensure `pipenv` is installed. (`pip install pipenv`)
2. In the `back/` directory, run `pipenv install`. This only needs to be done once.
3. Run `pipenv shell`.

Serve the contents of `back/` using a Python WSGI server. For example, in the case of gunicorn running on port 444, and assuming your site's SSL certificates are in `/etc/ssl/private/`:

`gunicorn --bind 0.0.0.0:444 --keyfile /etc/ssl/private/certificate.key --certfile /etc/ssl/private/certificate.crt reimbursinator.wsgi:application`

#### Admin access

Once the server is up and running, log in to `https://backendaddress.com:port/admin/` using the username `admin` and password `admin`, then change the administrative password using the "change password" link.

Open the "Sites" view, and edit the one existing site's name to match your server name. This will be used in system emails.

#### Policy File

The policy file, located at `back/backend/policy.py` is the heart of the application, defining the report sections, fields and rules which make up a reimbursement policy. You must build a policy file using these components in order to display the relevant text to your users, as well as collect the necessary data and give feedback based on rules.

##### Sections

The `Section` constructor is used to build a logical "section" of the report. A section corresponds to one idea or topic for which certain data should be collected, and certain rules applied. For example, to create a "Lodging" section, use the `Section` constructor with the following parameters:

- `title`: The title you wish to display for that section
- `html_description`: A string of html used to describe the section to the user. This should contain any necessary instructions or links to reference materials. Plain text should be wrapped in paragraph `<p></p>` tags.
- `fields`: This is a python object with one or more fields (see next section) defined.

Example python:

```
lodging_section = Section(
    title="Hotel / Lodging",
    html_description="<p>Please submit a receipt from your hotel including both the total amount and the dates of your stay. Per diem rates can be found on <a href='https://www.gsa.gov/travel/plan-book/per-diem-rates' target='_blank'>the U.S. GSA website</a>.</p>",
    fields={
        "per_diem_rate": {"number": 0, "label": "USGSA Per diem rate", "field_type": "decimal"},
        "cost": {"number": 1, "label": "Total cost for lodging", "field_type": "decimal"},
        "check_in_date": {"number": 2, "label": "Check-in date", "field_type": "date"},
        "check_out_date": {"number": 3, "label": "Check-out date", "field_type": "date"},
        "invoice_screenshot": {"number": 4, "label": "Screenshot of invoice", "field_type": "file"},
    }
)
```

A section can have any number of rules added to them. See the "Rules" section for more details.

Once a section is ready, add it to the policy file by calling:

```
pol.add_section(lodging_section)
```

Sections will be presented to the user in the order that they are added with this command.

##### Fields

Fields defined in the policy file for a section will appear as form fields in the application. When defined inside a Python object, they appear like this:

```
"per_diem_rate": {"number": 0, "label": "USGSA Per diem rate", "field_type": "decimal"},
```

- "per_diem_rate" becomes the key for this field, and is used to reference the field within rules for that section.
- "number" specifies the order in which the fields should be shown to the user.
- "label" is the text which will be displayed to the user for this field.
- "field_type" determines what type of data to get from the user. Depending on the type of field specified, the user will be prompted to fill in different types of information. The current supported types are:
  - `boolean`: A true/false value. This is presented as "yes/no" to the user, and is useful to store the response to a yes/no question.
  - `date`: An ISO date in YYYY-MM-DD format. The browser's native date picker should appear for this field
  - `decimal`: A number with a whole part and fractional part up to two places. e.g. 10.50
  - `integer`: An integer number. e.g. 10
  - `file`: A generic file upload field. Currently this field can only hold one file at a time. To allow multiple file upload multiple fields should be provided.
  - `string`: A string of unicode characters. e.g. "Portland"

##### Rules

Rules allow an administrator to validate the information entered by a user in a specific section and provide feedback messages if desired. Rules will be called with a dictionary of field values passed in via the `fields` parameter, and any string returned will be displayed to the user.

An example of a simple rule that checks the boolean value of the field named 'economy' to check if a user has purchased an economy class ticket would be as follows:

```
my_flight_section.add_rule(
    title="Economy Check",
    rule=lambda report, fields: "Only economy class tickets are allowed." if fields['economy'] else None
```

For more complex, multi-line rules, a temporary function may be defined and passed to the "rule" parameter when adding a rule. Currently, accessing fields from other sections via the "report" parameter is not supported.

### Admin Files

In order to have CSS and JS working in the Django administrative pages, serve the contents of `admin/static` using the http server of your choice, and edit `back/reimbursinator/settings.py` to set the `STATIC_URL` address to the correct address to access these files.

## Tools, Libraries and Frameworks Used

The following are the versions used in development of Reimbursinator, and the versions pinned in `back/Pipfile`.

| Tool | Version |
|-------------|---------|
| Python | 3.5 |
| python-decouple | 3.1 |
| Django | 2.1.6 |
| Django CORS Headers | 2.4.0 |
| Django Rest Framework | 3.8.2 |
| Django Rest Authentication | 0.9.3 |
| nginx | 1.10.3 |
| gunicorn | 19.6.0 |

## Tests

### Front end

Tests for front end code are implemented with Q-Unit, and are located in the `front/tests/` directory. To run them, open `qunit_tests.html` in a browser.

### Back end

Tests for back end code are implemented with Python and Django testing libraries. To run these:

1. From the `back/` directory, run `pipenv shell` to load Django modules.
2. Run `python manage.py test`.

One test file, `test_backend.py`, covers Django models, views, etc. The other test file, `test_policy.py`, is specific to the rules implemented in the provided `policy.py` file, and needs to be updated or removed as changes are made.
