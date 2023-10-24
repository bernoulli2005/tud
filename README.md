# Tud - Django Backend

**Tud** is a backend system developed by MLabs for a specific application. Built with Django, it offers robust and scalable solutions for your application's needs.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [Contact](#contact)
- [License](#license)

## Installation

Before starting the installation, make sure you have [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your machine.

1. **Set up a Conda environment**:
    ```bash
    conda create --name tud_env python=3.8
    conda activate tud_env
    ```

2. **Install the required packages**:
    Navigate to the project directory and run the following command to install the necessary packages:
    ```bash
    pip install -r requirements.txt
    ```

3. **Django setup**:
    - Initialize a new Django project if necessary.
    - Execute Django migrations:
      ```bash
      python manage.py migrate
      ```

## Configuration

1. **Set up email configuration**:
    Open the `settings.py` file in your project's main configuration directory. Find the following lines and replace them with your email credentials:

    ```python
    EMAIL_HOST_USER = ''  # Replace with your email address
    EMAIL_HOST_PASSWORD = ''  # Replace with your email password
    ```

   Make sure not to commit your email credentials to a public repository. Consider using environment variables or Django's `secrets` module to keep your sensitive data secure.

## Running the Server

After completing the installation and configuration steps, you can run the Django server with the following command:

```bash
python manage.py runserver
```

## Contact

For any queries or feedback, please reach out to the MLabs team at soporte@mlabs.com.ar.

## License

This project is licensed under the MIT License. This means you are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, 
but you must provide appropriate attribution, give any distributed works the same open source license, and not hold the authors or license holders liable.


