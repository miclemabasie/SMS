# Django Boilerplate Project

Welcome to the Django Boilerplate Project! This project is designed to serve as a robust starting point for serious Django projects, equipped with modularized settings, pre-configured Docker setup, logging functionalities, and a comprehensive testing setup using `pytest` and `factory-boy`.

## Table of Contents

- [Project Setup](#project-setup)
- [Environment Variables](#environment-variables)
- [Logging](#logging)
- [Database Configuration](#database-configuration)
- [Renaming the Project](#renaming-the-project)
- [Testing](#testing)
- [Docker Operations](#docker-operations)

## Project Setup

To set up the project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/miclemabasie/django_starter_project.git
   cd django_starter_project
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv env
   source env/bin/activate   # For Linux/Mac
   # or
   .\env\Scripts\activate    # For Windows
   ```

3. Install dependencies:

   ```bash
   cd src
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000/` in your browser to see the project in action.

## Environment Variables

By default the project is running on the sqlite3 database, to use postgres localy move on to configure the environment variables and edit `development.py` file inside the settings module inside the main application folder.
Environment variables are used to configure the project. Create a `.env` file in the project root and define the necessary variables. You can copy `.env.example` as a starting point.
Update the values with your specific configuration.

## Logging

The project comes with a logging configuration to handle different log levels. Logging is configured in `demo/settings/base.py`. Customize it based on your requirements, most importantly change `LOG_FILE_NAME` to point the the name which you wish to call your log file and then on the same level as the `manage.py` file, create a directory called `logs` and then create a file with the name you just indicated in the `base.py` for the `LOG_FILE_NAME`, note that errors will occur if this is not properly done, by default the log file should be called `demo.logs`. 

## Database Configuration

Database settings can be configured in the `.env` file as mentioned in the Environment Variables section. Update the variables accordingly.
In case you are using the dockerized version of the application, for the database configuration the following is the default config for postgres
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_HOST=postgres-db
```

Note that the `POSTGRES_HOST` is pointing to the name of the `postgres-db` service in the `compose.yml` file

## Renaming the Project

To rename the project using the custom rename command, follow these steps:

1. Run the following command in the project root:

   ```bash
   python manage.py rename YourNewProjectName
   ```

   Replace `YourNewProjectName` with the desired name for your project.

2. The command will perform a global search and replace for the project name in all files. After running the command, review the changes to ensure everything was updated correctly.

3. Optionally, you can remove the `rename` directory, which contains the script used for renaming, from your project.

## Testing

This project includes a comprehensive testing setup using `pytest` for test discovery and execution and `factory-boy` for creating test fixtures with coverage. Test files are located in the `tests/` directory, and factories for test data are in the `tests/factories/` directory.

### Running Tests

To run the tests, use the following command:

```bash
pytest
```

### Writing Tests

Example test files and factories are provided in the `tests/` and `tests/factories/` directories. Customize and expand these files based on your project's testing needs.

### Code Coverage

To check code coverage using `coverage`, run the following commands:

`pytest -p no:warnings --cov=. --cov-report html`

Certainly! Below is an updated section on Docker Operations to guide users on how to start the project using only Docker.

---

## Docker Operations

This project is Docker-ready and can be started using Docker commands. The `docker-compose.yml` file is configured for development purposes, and you can use Docker commands directly without relying on the Makefile.

### Starting the Project with Docker (Recommended)

To start the project using Docker, follow these steps:

1. Build Docker images:

   ```bash
   docker-compose build
   ```

2. Run Docker containers:

   ```bash
   docker-compose up
   ```

   This command starts the project and its dependencies in detached mode. You can add `-d` to run it in the background.

3. Access the Django development server:

   Open your web browser and navigate to `http://127.0.0.1:8000/` to see the project in action.

4. Stop Docker containers:

   To stop the running containers, use the following command:

   ```bash
   docker-compose down
   ```

### Additional Docker Commands

Feel free to explore the `docker-compose.yml` file for additional Docker commands. Here are some commonly used commands:

- **Stopping and Removing Containers:**

  ```bash
  docker-compose down
  ```

- **Removing Docker images and volumes:**

  ```bash
  docker-compose down -v --rmi all
  ```

- **Viewing logs:**

  ```bash
  docker-compose logs -f
  ```

- **Executing commands in a running container:**

  ```bash
  docker-compose exec <service_name> <command>
  ```

   Replace `<service_name>` with the name of the service in your `docker-compose.yml` file, and `<command>` with the desired command to execute.

These commands should cover most development scenarios. Adjust and customize them based on your project's specific Docker setup and requirements.
