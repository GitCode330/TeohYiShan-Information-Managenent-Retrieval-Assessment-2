# Information-Managenent-Retrieval-Assessment-2

**Trail Micro-service Implementation**

**Author:** Teoh Yi Shan  
**Student ID:** BSSE2506022  
**Programme of Study:** Bachelor of Science in Software Engineering  
**Module:** MAL2017 Information Management & Retrieval  
**Module Leader:** Dr. Ang Jin Sheng

## 📋 Overview

This repository contains the implementation of the **TrailService micro-service**, a RESTful API for managing walking trails as part of a well-being trail application. The service provides full CRUD (Create, Read, Update, Delete) operations for trail data, integrates with an external authentication service, and follows RESTful API principles.

### Prerequisites

- **Python 3.9+**
- **Microsoft SQL Server 2019+** (Docker or local installation)
- **ODBC Driver 17 for SQL Server**
- **Azure Data Studio** (or SQL Server Management Studio)
- **Postman** (for API testing)

### 1. Database Setup (Docker SQL Server)

#### Using Docker (Recommended)
```bash
# Pull SQL Server 2019 image
docker pull mcr.microsoft.com/mssql/server:2019-latest

# Run SQL Server container
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=C0mp2001!" \
   -p 1433:1433 --name sqlserver \
   -d mcr.microsoft.com/mssql/server:2019-latest

## 🐍 Python Environment Setup

### Prerequisites
Before setting up the Python environment, ensure you have:
- **Python 3.9 or higher** installed
- **Git** for version control
- **Docker** (for SQL Server database)
- **Postman** (for API testing, optional but recommended)

### Steps

#### 1. Clone the Repository
```bash
# Clone the repository to your local machine
git clone https://github.com/GitCode330/TeohYiShan-Information-Managenent-Retrieval-Assessment-2.git

# Navigate to the project directory
cd TeohYiShan-Information-Managenent-Retrieval-Assessment-2

2.  **Start the Database Container:**
    Run the following command in your terminal to start the MSSQL Docker container.
    ```bash
    docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=C0mp2001!" \
               -p 1433:1433 --name COMP2001sqlserv \
               -d mcr.microsoft.com/azure-sql-edge
    ```

    **Alternative: Using SQL Server 2019:**
    ```bash
    docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=C0mp2001!" \
               -p 1433:1433 --name sqlserver-cw2 \
               -d mcr.microsoft.com/mssql/server:2019-latest
    ```

3.  **Set Up the Python Environment:**
    Create and activate a virtual environment, then install the required packages.

    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate it (Windows)
    venv\Scripts\activate

    # Or activate it (macOS/Linux)
    source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the project root with the following content:

    ```env
    # Database Configuration
    DB_SERVER=localhost
    DB_NAME=COMP2001_Test
    DB_DRIVER=ODBC Driver 17 for SQL Server
    DB_USERNAME=SA
    DB_PASSWORD=C0mp2001!

    # Flask Configuration
    FLASK_DEBUG=True
    FLASK_APP=app.py
    SECRET_KEY=your-secret-key-here

    # CORS Configuration
    CORS_ORIGINS=http://localhost:3000,https://web.socem.plymouth.ac.uk
    ```

5.  **Install ODBC Driver (If Not Installed):**
    Download and install the ODBC Driver 17 for SQL Server from the [Microsoft Download Center](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server).

    **Verify Installation:**
    ```bash
    # Check if ODBC driver is installed
    python -c "import pyodbc; print(pyodbc.drivers())"
    ```
    Should output: `['ODBC Driver 17 for SQL Server', ...]`

6.  **Initialize the Database:**
    Run the database setup script to create the CW2 schema and tables.

    ```bash
    # Using Azure Data Studio or SQL Server Management Studio
    # Run the SQL script: sql/cw2_schema_setup.sql
    ```

7.  **Run the Application:**
    ```bash
    # Development server
    python app.py

    # Or using Flask CLI
    flask run --host=0.0.0.0 --port=5000
    ```
