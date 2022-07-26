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

If you want to run REST API with UI run

```bash
python .\AMCEF_APP.py
```
