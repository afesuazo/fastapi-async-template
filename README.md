# fastapi-async-template

afesuazo

## Introduction

This repository provides a ready-to-use template for Python FastAPI projects,
specifically designed with asynchronous programming in mind. 
It's a great starting point for beginners looking to get their hands dirty with FastAPI.

## Features

* Basic FastAPI application
* Database connection setup
* CRUD operations examples
* Database models examples

## Files

```
.
│
├── app/                     # Application source code
│   ├── api/                 
│   │   └── routes/          
│   │       ├── base.py      # Global router
│   │       ├── basic.py     # Simple route
│   │       └── users.py     # Route with db operations
│   │
│   ├── crud/                # CRUD operations
│   │       ├── base.py      # Abstract CRUD class
│   │       └── user.py      # CRUD implementation for user model
│   │
│   ├── dependencies/        # Dependencies for routes
│   │   └── db.py            # DB as a dependency
│   │
│   ├── models/              # Database Models
│   │       └── user.py      # Example model
│   │
│   ├── database.py          # Database connection setup
│   └── main.py              # FastAPI application entry point
│
├── config.py.              
├── requirements.txt        # Python dependencies
├── run.sh                  # Launch script
├── setup.sh                # Package installer script
├── LICENSE                 
└── README.md
```

## Getting Started

### Prerequisites
* Python 3.8 or higher
* Virtualenv (Recommended)

### (Optional) Create a virtual environment

```bash
# Create the venv
$ python3 -m venv env

# Activate it
$ source env/bin/activate
```

### Clone and Build the Chat Application

```bash
# Clone the repository
$ git clone https://github.com/afesuazo/fastapi-async-template.git
$ cd fastapi-async-template

# Run the setup script to install packages
# Same as pip3 install -r requirements.txt
$ chmod +x ./setup.sh
$ ./setup.sh
```

### Running the Program

```bash
$ chmod +x ./run.sh
$ ./run.sh
```

Or run it manually:

```bash
$ uvicorn app.main:app --reload
```

Then visit http://localhost:8000 in your web browser. 
You should see the words "Hello World!" printed to your screen.

You can also visit http://localhost:8000/docs to access an 
interactive API documentation interface using Swagger UI.

## Usage

TODO

## Feedback

If you come across any bugs or have any ideas for improvements, 
please create an issue ticket in the repository.

## License

This project is licensed under the terms of the MIT license. See the LICENSE file for details.

## To-Do List

- [X] Add CRUD operations
- [X] Add sample model
- [ ] Add redis dependency
- [ ] Add simple tests
- [ ] Provide detailed config instructions
- [ ] Add CONTRIBUTING.md