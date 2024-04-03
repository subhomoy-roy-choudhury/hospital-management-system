# Hospital Management System
## Local Development Setup

Follow these steps to get your development environment set up:

### Prerequisites

- Ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed on your system.

### Setup Steps

1. **Environment Variables**:
   - Copy the contents of `.env.example` to a new file named `.env` in the same directory.
     ```bash
     cp .env.example .env
     ```
   - Modify the `.env` file as needed to match your local environment.

2. **Build and Run**:
   - Use the provided Makefile to build and start the application.
     ```bash
     make
     make runserver
     ```
   - The server will start running locally. Access it at the specified URL, typically `http://localhost:8000`.

## Using Docker

For those preferring Docker for development or testing, follow these instructions:

### Prerequisites

- Make sure you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your system.

### Setup Steps

1. **Build and Run with Docker Compose**:
   - Execute the following command to start your containers:
     ```bash
     docker-compose up --build --remove-orphans -d
     ```
   - This command will build the Docker images, handle orphans, and start the containers in detached mode.

2. **Accessing the Application**:
   - Once the containers are up and running, you can access the application as configured, typically at `http://localhost:8000`.