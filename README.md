<!-- Reminder: Ensure consistent formatting throughout this document. Check for proper closure of code blocks, consistent use of whitespace around headings and code blocks, and uniformity in bullet points and numbered lists. -->
# Catalog API

## Project Description

This project, `Catalog API`, is designed to manage a personal collection of various items including books, video games, Blu-ray/DVD movies, clothing, and more. The initial phase focuses on books, allowing users to catalog books with detailed attributes like title, description, author(s), translator(s), edition number, publisher, place of publication, publication date, number of pages, and ISBN.

## Getting Started

### Running the Database with Docker

**Prerequisite**: Before you begin, make sure Docker and Docker Compose are installed on your machine. If you haven't installed them yet, please visit [Docker's official website](https://docs.docker.com/get-docker/) for guidance on how to do so.

The database can be easily initialized and run using Docker and `docker-compose`. This approach automatically creates the database structure and populates it with initial data.

1. **Clone the Repository**

   Start by cloning the repository to your local machine.

2. **Navigate to the Project Directory**

   Change into the project directory where the `docker-compose.yml` file is located.

3. **Run Docker Compose**

   Run the following command to start the PostgreSQL database in a Docker container:

   ```sh
   docker-compose up -d
   ```

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

### Security Best Practices

When configuring your environment, especially in production settings, adhering to security best practices is crucial. Avoid hard-coding sensitive details such as passwords directly into your scripts or Docker configuration files. 

## Contributing

We welcome contributions to the Catalog API project! If you're interested in helping, please first review our contribution guidelines and code of conduct. These documents will guide you on how to make contributions in a manner that is respectful, efficient, and aligned with our project's goals.

If these documents are not yet available, or if you have any questions about contributing, please feel free to open an issue or contact the project maintainers directly. We're excited to see what you bring to the project!

### Additional Information

This project is set up to be flexible and can be extended in the future to include more types of items in the personal catalog. The initial focus is on books, but the design allows for easy addition of new categories. Please consult the project's documentation and code comments for further details on extending the project.

Contributions to the project are welcome. Please ensure to follow the project's contribution guidelines and code of conduct when submitting patches or features.

For any questions or issues, please open an issue on the project's GitHub repository, and a maintainer will get back to you as soon as possible.

