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

#### Option A: Using Docker (Recommended)
```bash
# Pull SQL Server 2019 image
docker pull mcr.microsoft.com/mssql/server:2019-latest

# Run SQL Server container
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=C0mp2001!" \
   -p 1433:1433 --name sqlserver \
   -d mcr.microsoft.com/mssql/server:2019-latest

