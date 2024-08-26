# My Dockerized App

This README provides instructions for building and running the app within a Docker container using Docker Compose.

## Prerequisites

- **Docker**: Ensure Docker is installed and running on your machine.
- **Docker Compose**: Make sure Docker Compose is also installed.

## Getting Started

### 1. Build and Run the App

To build the app and containerize it, use the following command in the directory containing your `docker-compose.yml` file:

```bash
sudo docker-compose up --build
```

This command will build the Docker image and start the container based on the configuration specified in the `docker-compose.yml` file.

### 2. Access the Streamlit App

Once the container is running, you can access the Streamlit app by opening your web browser and navigating to:

```
http://localhost:8501
```

This URL should display the Streamlit app’s user interface.

### 3. Upload the Demo CSV File

Once the Streamlit app is open in your browser:

Click on the file upload section to upload the demo CSV file provided.

### 4. Stopping the App

To stop the app and container, you can use:

```bash
sudo docker-compose down
```
