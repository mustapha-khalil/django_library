# Library

Library is a web app where users can view all books in a book library. It also allows them to add, edit or delete existing books.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Setup](#setup)
- [Usage](#usage)

## Getting Started

These instructions will get your project up and running on your local machine.

### Prerequisites

- Python (version 3.11)
- Virtual environment (e.g., [venv](https://docs.python.org/3/library/venv.html))

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mustapha-khalil/django_library.git
   ```

2. Navigate to the project direcory

   ```bash
   cd django_library
   ```

3. Create and activate a virtual environment

   windows

   ```bash
   python -m venv envname
   envname\Scripts\activate
   ```

   macOS and Linux

   ```bash
   python -m venv envname
   source envname/bin/activate
   ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

### Setup

1. Apply database migrations using the following commands:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Usage

1. Start the development server:

   ```bash
   python manage.py runserver
   ```

2. Open a web browser and navigate to http://localhost:8000 to access the application
