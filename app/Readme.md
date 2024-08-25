# My Dockerized App

This README provides instructions for building and running the app within a Docker container using Docker Compose.

## Prerequisites

- **Docker**: Ensure Docker is installed and running on your machine. Download it from [Docker's official website](https://www.docker.com/products/docker-desktop).
- **Docker Compose**: Make sure Docker Compose is also installed. You can follow [these instructions](https://docs.docker.com/compose/install/) to install it if it's not already installed.

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

### 3. Stopping the App

To stop the app and container, you can use:

```bash
sudo docker-compose down
```

### 4. Updating the App

If you make changes to your app, re-run the build and start command:

```bash
sudo docker-compose up --build
```

This will rebuild the Docker image and restart the container with your updated app.

---

