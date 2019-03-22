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

### Admin Files

In order to have CSS and JS working in the Django administrative pages, serve the contents of `admin/static` using the http server of your choice, and edit `back/reimbursinator/settings.py` to set the `STATIC_URL` address to the correct address to access these files.

## Usage

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

One test file, `test_backend.py`, covers Django models, views, etc. The other test file, `test_policy.py`, is specific to the rules implemented in the provided `policy.py` file, and need to be updated or removed as changes are made.
