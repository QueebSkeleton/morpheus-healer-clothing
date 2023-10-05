<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<div align="center">
  <h3 align="center">Morpheus Healer Clothing</h3>
  <p align="center">
    A clothing line with handcrafted designs.
  </p>
</div>

## About the Project

Morpheus Healer Clothing Store is an E-Commerce store for selling clothes
with custom designs.

This software is submitted in partial fulfillment of the requirements for
the course **Web Development** under the *Computer Science* program of the
Polytechnic University of the Philippines.

## Features

1. Front Store
1. Login via Facebook and Google (OAuth2)
1. Management Facilities via Django Admin, including the following:
- Product Information
- Inventory
- Order Tracking

## Built With

This website is built with the following technologies:

[![Python][Python-shield]][Python-docs]
[![Django][Django-shield]][Django-docs]
[![Postgres][Postgres-shield]][Postgres-docs]

## Installation

Install the following beforehand:

1. Python 3.x
1. pipenv - `pip install pipenv`

To run on your development machine, do the following steps:

1. Clone the repo - `git clone https://github.com/QueebSkeleton/taglish-hybrid-integrated-hmm-pos.git`
1. Open the project directory on your terminal.
1. Install dependencies - `pipenv install`
1. Run a shell with the created virtualenv - `pipenv shell`
1. Run database migrations - `python manage.py migrate`
1. Create an admin account for the website - `python manage.py createsuperuser`
then follow the instructions.
1. Open the tagger frontend project on your terminal: `project_root/tagger/spas/tagger/`
1. Create a `.env` file, specify the ff.:
- SECRET_KEY - for cryptographic facilities (password hash generation, etc.)
- ALLOWED_HOSTS - colon-separated allowed hosts (e.g., localhost:www.example.com:www.another.com)
- FACEBOOK_KEY and FACEBOOK_SECRET - Facebook OAuth necessary information
- GOOGLE_KEY and GOOGLE_SECRET - Google OAuth necessary information
9. Go back to the root project directory, then run the dev server - `python manage.py runserver`

Then, the instance will now run on your local machine. Endpoints are:<br>
`localhost:8000` - the index page of the application. A head navigator
is presented to visit all the pages.

## Preview of the Pages

To be added.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Markdown Links & Images -->
[stars-shield]: https://img.shields.io/github/stars/QueebSkeleton/taglish-hybrid-integrated-hmm-pos?style=for-the-badge
[stars-url]: https://github.com/QueebSkeleton/taglish-hybrid-integrated-hmm-pos/stargazers
[issues-shield]: https://img.shields.io/github/issues/QueebSkeleton/taglish-hybrid-integrated-hmm-pos?style=for-the-badge
[issues-url]: https://github.com/QueebSkeleton/taglish-hybrid-integrated-hmm-pos/issues

[Python-shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-docs]: https://www.python.org/
[Django-shield]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white
[Django-docs]: https://www.djangoproject.com/
[Postgres-shield]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-docs]: https://www.postgresql.org/
