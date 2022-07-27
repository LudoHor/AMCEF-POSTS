# Getting Started

This is REST API service created in FLASK also provided with UI option.

## Installation

This is installation instruction for Windows OS, for Other OS please use respective commands.
[Python](https://www.python.org/) need to be installed on machine.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install virtualenv.

```bash
pip install virtualenv
```

```bash
python -m venv venv
venv\Scripts\activate
pip install -r .\requirements.txt
```

## Create Database

Before first time running app, you need to create database(if you already have one just change connection in models.py)

```bash
python .\create_db.py
```

## Running app

If you want to run REST API run

```bash
python .\AMCEF_REST_API.py
```

Documentation is available on http://127.0.0.1:5000/doc

If you want to run REST API with UI run

```bash
python .\AMCEF_APP.py
```

## Docker Container

Create container

```bash
docker build --tag amcef-docker .
```

Run the container

```bash
docker run -d -p 5000:5000 amcef-docker
```
