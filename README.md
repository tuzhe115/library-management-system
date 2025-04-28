# Library Management System with Analysis

This project is a Library Management System that supports book management, user management, loan and reservation management, and provides data analysis based on library data.

## How to Run the System with Docker

### Prerequisites

- Install Docker Desktop on your machine.
- Ensure Docker is running before proceeding.

### Quick Start

1. Open a terminal or PowerShell window.
2. Navigate to the project root directory where `docker-compose.yml` is located.
3. Run the following commands:

```bash
docker-compose build
docker-compose up -d
```

4. After the containers start:
   - Frontend is accessible at: http://localhost:5173
   - Backend API is accessible at: http://localhost:8000

### Shutdown

To stop the system:

```bash
docker-compose down
```

## Project Structure

- `frontend/` - Vue.js frontend interface
- `backend/` - Django REST API server
- `db/` - MySQL database container

## Notes

- Default login credentials:
  - Username: root
  - Password: 123456
- Ensure ports 5173, 8000, and 3306 are available before starting the system.
- Environment variables are managed separately; test data is included in the file.
