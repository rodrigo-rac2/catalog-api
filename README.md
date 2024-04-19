<!-- Reminder: Ensure consistent formatting throughout this document. Check for proper closure of code blocks, consistent use of whitespace around headings and code blocks, and uniformity in bullet points and numbered lists. -->

## Table of Contents

- [Catalog API](#catalog-api)
    - [Disclaimer](#disclaimer)
  - [Quick Start](#quick-start)
  - [Project Description](#project-description)
  - [Getting Started](#getting-started)
    - [Docker Setup](#docker-setup)
    - [Local Setup](#local-setup)
  - [Detailed Installation Instructions](#detailed-installation-instructions)
    - [Running the Project with Docker](#running-the-project-with-docker)
    - [Database Scripts](#database-scripts)
    - [Running the Database Locally (Without Docker)](#running-the-database-locally-without-docker)
      - [Using the Shell Scripts](#using-the-shell-scripts)
  - [Shell Scripts](#shell-scripts)
    - [For Linux/Mac](#for-linuxmac)
    - [For Windows](#for-windows)
  - [Running the Flask Application](#running-the-flask-application)
    - [Prerequisites](#prerequisites)
    - [Step 1: Install Dependencies](#step-1-install-dependencies)
    - [Step 2: Set Environment Variables](#step-2-set-environment-variables)
    - [Step 3: Run the Flask Application](#step-3-run-the-flask-application)
    - [Accessing Swagger Documentation](#accessing-swagger-documentation)
  - [Advanced Setup and Tips](#advanced-setup-and-tips)
    - [Running with Docker](#running-with-docker)
    - [Troubleshooting Common Issues](#troubleshooting-common-issues)
  - [API Endpoints](#api-endpoints)
    - [Books](#books)
    - [Participants](#participants)
    - [Roles](#roles)
    - [Swagger Documentation](#swagger-documentation)
    - [Note on Usage](#note-on-usage)
  - [Next Steps and Usage](#next-steps-and-usage)
  - [Security Best Practices](#security-best-practices)
  - [Contributing to the Project](#contributing-to-the-project)
  - [Additional Resources](#additional-resources)
    - [Additional Information](#additional-information)
  - [License](#license)

# Catalog API

## Disclaimer

This project is currently in active development. Features and documentation are subject to change. While we strive to keep the information up-to-date, there may be discrepancies or incomplete features. We welcome feedback and contributions to help improve the project. For the most current information and to see how you can contribute, please visit the project's GitHub repository.

## Quick Start

For those familiar with Docker and looking to get the Catalog API up and running quickly, follow these steps:

1. **Prerequisites**: Make sure Docker and Docker Compose are installed on your machine. Visit [Docker's official website](https://docs.docker.com/get-docker/) for installation instructions if needed.

2. **Clone the Repository**: Run `git clone https://github.com/rodrigo-rac2/catalog-api` to clone the project to your local machine.

3. **Navigate to Project Directory**: Change into the project directory with `cd catalog-api/`.

4. **Start Services with Docker Compose**: Execute `docker-compose up -d` to build and start the PostgreSQL database and the Flask application containers.

5. **Access the Application**: The Flask application will be accessible at `http://localhost:5100`. Visit `http://localhost:5100` in your web browser to access the Swagger UI and interact with the API.

This Quick Start guide is intended to help you get the Catalog API running with minimal setup. For detailed instructions on local setup, database scripts, and other configurations, please refer to the sections below.


## Project Description

This project, `Catalog API`, is designed to manage a personal collection of various items including books, video games, Blu-ray/DVD movies, clothing, and more. The initial phase focuses on books, allowing users to catalog books with detailed attributes like title, description, author(s), translator(s), edition number, publisher, place of publication, publication date, number of pages, and ISBN.

This project can be set up using Docker for a containerized environment or locally by installing the necessary dependencies directly on your machine.

## Getting Started

### Docker Setup

1. **Prerequisites**: Ensure Docker and Docker Compose are installed. [Installation guide](https://docs.docker.com/get-docker/).
2. **Clone the Repository**: `git clone https://github.com/rodrigo-rac2/catalog-api`.
3. **Run Docker Compose**: Navigate to the project directory and run `docker-compose up -d`. This starts the services defined in `docker-compose.yml`, including the PostgreSQL database and Flask application.

### Local Setup

Follow these steps if you prefer to run the application directly on your local machine without Docker.

1. **Install PostgreSQL**: Follow the official [PostgreSQL installation guide](https://www.postgresql.org/download/).
2. **Database Setup**: Create a new database named `catalog`, and apply the schema and initial data using the provided SQL scripts.
3. **Python Environment Setup**: Install Python 3, set up a virtual environment, and install dependencies with `pip install -r requirements.txt`.
4. **Run the Flask Application**: Set the necessary environment variables and start the Flask server with `flask run`.

For detailed steps, see the sections below.

## Detailed Installation Instructions

### Running the Project with Docker

**Prerequisite**: Before you begin, make sure Docker and Docker Compose are installed on your machine. If you haven't installed them yet, please visit [Docker's official website](https://docs.docker.com/get-docker/) for guidance on how to do so.

The database and the application can be easily initialized and run using Docker and `docker-compose`. This approach automatically creates the database structure in a container, populates it with initial data, and loads the application flask in another container in the same docker network.

1. **Clone the Repository**

   Start by cloning the repository to your local machine.

2. **Navigate to the Project Directory**

   Change into the project directory where the `docker-compose.yml` file is located.

3. **Run Docker Compose**

   Run the following command to start the PostgreSQL database in a Docker container:

   ```sh
   docker-compose up -d
   ```

   This command starts both the database and Flask application services as defined in your Docker Compose configuration.

### Database Scripts

The database initialization and seed scripts are located under `postgres/scripts`:

- `ddl.catalog.sql` for schema creation.
- `dml.catalog.sql` for initial data loading.

### Running the Database Locally (Without Docker)

If you prefer to run the PostgreSQL database locally instead of using Docker, follow these steps after installing PostgreSQL on your system:

1. **Start PostgreSQL**

    Ensure your local PostgreSQL instance is running.

2. **Create the Database**

    Create a new database named `catalog` (or your preferred name).

3. **Run the DDL Script**

    Apply the schema by running the `ddl.catalog.sql` script against the newly created database.

4. **Run the DML Script**

    Populate the database with initial data using the `dml.catalog.sql` script.

#### Using the Shell Scripts

For convenience, shell scripts for Linux/Mac and a batch file for Windows are provided to run the SQL scripts against your local PostgreSQL database.

- **Linux/Mac**: Execute the `run_scripts.sh` script.
- **Windows**: Run the `run_scripts.bat` file.

Ensure to update the database name, user, and password in the scripts according to your local setup.

#### Using the Shell Scripts

Before using the provided shell scripts for Linux/Mac (`run_scripts.sh`) and Windows (`run_scripts.bat`), you'll need to update the `DATABASE_NAME`, `USER`, and `PASSWORD` variables in the scripts according to your local database setup. These scripts are designed to simplify the process of running the SQL scripts against your local PostgreSQL database.

## Shell Scripts

### For Linux/Mac

Create a file named `run_scripts.sh` with the following content:

```sh
#!/bin/bash

DATABASE_NAME=catalog
USER=postgres
PASSWORD=yourpassword

psql -d $DATABASE_NAME -U $USER -f postgres/scripts/ddl.catalog.sql
psql -d $DATABASE_NAME -U $USER -f postgres/scripts/dml.catalog.sql
```

Make the script executable:

```sh
chmod +x run_scripts.sh
```

Then, execute it:

```sh
./run_scripts.sh
```

### For Windows

Create a file named `run_scripts.bat` with the following content:

```bat
@echo off
SET DATABASE_NAME=catalog
SET USER=postgres
SET PASSWORD=yourpassword

psql -d %DATABASE_NAME% -U %USER% -f postgres/scripts/ddl.catalog.sql
psql -d %DATABASE_NAME% -U %USER% -f postgres/scripts/dml.catalog.sql
```
To run the batch file, simply double-click on it or execute it from the command prompt.

**Note:** Replace `yourpassword` with the actual password, and adjust the database name and user as necessary. In environments where password authentication is required, you might need to supply the password differently. For Windows, you could set the `PGPASSWORD` environment variable before running the batch file to avoid having to enter the password manually. Ensure your PostgreSQL bin directory is in your system's PATH to use the `psql` command from the command prompt.

## Running the Flask Application

After setting up the database, you're ready to run the Flask application. This section guides you through installing dependencies, setting environment variables, and starting the server.

### Prerequisites

- Ensure **Python 3** is installed on your machine. If not, you can download it from [the official Python website](https://www.python.org/downloads/).
- It is recommended to use a **virtual environment** for Python projects to manage dependencies efficiently.

### Step 1: Install Dependencies

Navigate to the `api/` directory within your project and install the required Python packages using pip:

```bash
# Navigate to the api/ directory
cd catalog-api/api/

# Install dependencies from the requirements file
pip install -r requirements.txt
```

### Step 2: Set Environment Variables

Create a `.env` file in the `api/` directory with the necessary environment variables:

```plaintext
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:password@localhost:5432/catalog
```

Adjust the `DATABASE_URL` as needed to match your PostgreSQL connection details.

### Step 3: Run the Flask Application

With the dependencies installed and the environment variables set, you can now run the Flask application by executing the following command in the terminal:

```bash
flask run
```

This command starts the Flask server, which is typically accessible at http://localhost:5100. At this point, you can use a web browser or tools like Postman to interact with your API.

### Accessing Swagger Documentation

To explore the API's capabilities interactively, visit the root URL of your API (http://localhost:5100 by default) in a web browser. This will open the Swagger UI documentation where you can test different endpoints.

## Advanced Setup and Tips

### Running with Docker

If you're utilizing Docker, ensure your `docker-compose.yml` file correctly defines services for both the Flask application and the PostgreSQL database. Running `docker-compose up -d` in your project directory will start both services in their respective containers, streamlining the setup process.

### Troubleshooting Common Issues

- **Database Connection Errors**: Verify that the `DATABASE_URL` in your `.env` file matches your PostgreSQL credentials and that the PostgreSQL service is running.
- **Dependency Installation Issues**: Ensure you're using a virtual environment if package conflicts occur. Recheck the `requirements.txt` file for the correct package versions.

## API Endpoints

This section details some of the specific endpoints of the API, particularly those related to participants and roles, which are crucial for managing the relationships within the catalog.

### Books

- **GET /books**:
  - Retrieves a list of all books in the catalog. This endpoint supports filtering by various attributes like title, ISBN, publisher, and more, allowing users to find books that meet specific criteria.

- **POST /books**:
  - Adds a new book to the catalog. Required fields typically include the title and ISBN. Optional fields might include description, edition number, publication date, etc.

- **GET /books/{bookid}**:
  - Fetches detailed information about a specific book using its unique identifier.

- **PUT /books/{bookid}**:
  - Updates the details of an existing book. All aspects of the book record (like title, description, number of pages) can be modified through this endpoint.

- **DELETE /books/{bookid}**:
  - Completely removes a book from the catalog based on its ID.

- **GET /books/{bookid}/participants**:
  - Retrieves a list of all participants related to a specific book, along with their roles, such as authors, editors, etc.

- **POST /books/{bookid}/participants**:
  - Adds a new participant with a role to a specific book, linking them through their role in the book's creation or publication.

- **PUT /books/{bookid}/participants/{participantid}/role/{roleid}**:
  - Updates the role of a specific participant associated with a book, useful for correcting or changing the participant's contribution details.

- **DELETE /books/{bookid}/participant/{participantid}**:
  - Removes a participant's association from a book, effectively deleting their contribution record from that specific book.

### Participants

- **GET /participants**:
  - Retrieves a list of all participants. Each participant represents an entity that can be associated with different items in the catalog, such as a book.

- **POST /participants**:
  - Creates a new participant. The request must include a name for the participant, which is used to identify them uniquely within the catalog.

- **GET /participants/{participantid}**:
  - Fetches a detailed view of a specific participant based on their unique identifier.

- **PUT /participants/{participantid}**:
  - Updates information for an existing participant. This can be used to change the name of the participant.

- **DELETE /participants/{participantid}**:
  - Removes a participant from the catalog entirely, ensuring that they are no longer linked to any items.

### Roles

- **GET /roles**:
  - Lists all roles available in the system. Roles define the capacity in which a participant is related to an item, such as "Author", "Editor", or "Translator" for books.

- **POST /roles**:
  - Allows the addition of a new role to the system, which can then be assigned to participants.

- **GET /roles/{roleid}**:
  - Retrieves detailed information about a specific role by its ID.

- **PUT /roles/{roleid}**:
  - Modifies an existing role, typically used to change the description of the role.

- **DELETE /roles/{roleid}**:
  - Deletes a role from the system, which will affect how participants can be associated with items if they were linked to this role.

### Swagger Documentation

To access interactive documentation and try out the API endpoints directly, navigate to the Swagger UI:

- **URL**: `http://localhost:5100/`

This Swagger UI provides a user-friendly interface to directly interact with all endpoints of the API. You can execute requests, see responses in real-time, and explore the full capabilities of the Catalog API without writing any additional code.

### Note on Usage

For all endpoints that modify data (POST, PUT, DELETE), ensure that your requests are correctly formatted and include all required fields as specified in the Swagger documentation. Incorrect requests may lead to errors or unintended behavior.

## Next Steps and Usage

After successfully starting the Flask application and accessing the Swagger UI:

1. **Try out API endpoints** using the interactive Swagger UI. This is a great way to familiarize yourself with the API's functionality.
2. **Review the Flask application's code** to understand the API's structure and how endpoints are implemented.

## Security Best Practices

When deploying your Flask application, consider the following security best practices:

- **Use HTTPS** to encrypt data in transit.
- **Keep dependencies updated** to mitigate vulnerabilities.
- **Configure proper error handling** to avoid revealing sensitive information in error messages.

## Contributing to the Project

We encourage contributions! If you have suggestions, bug reports, or contributions, please submit them via GitHub issues or pull requests. Review our contribution guidelines and code of conduct for more information on contributing to the project.

## Additional Resources

For more detailed instructions on setting up Flask, Docker, or managing Python environments, refer to the official documentation for:

- [Flask](http://flask.palletsprojects.com/)
- [Docker](https://docs.docker.com/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

### Additional Information

This project is set up to be flexible and can be extended in the future to include more types of items in the personal catalog. The initial focus is on books, but the design allows for easy addition of new categories. Please consult the project's documentation and code comments for further details on extending the project.

Contributions to the project are welcome. Please ensure to follow the project's contribution guidelines and code of conduct when submitting patches or features.

For any questions or issues, please open an issue on the project's GitHub repository, and a maintainer will get back to you as soon as possible.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The MIT License is a permissive license that is short and to the point. It lets people do anything they want with your code as long as they provide attribution back to you and don’t hold you liable.

