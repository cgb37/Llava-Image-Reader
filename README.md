# Llama Image Reader

## Description
This is a Quart web application that allows users to upload images and receive a description of the image using the Llava API. It is containerized using Docker for easy deployment.

## Requirements
- Docker
- docker-compose
- Ollama: Download and install from https://ollama.com/download
- Llava model: Pull the Llava model using Ollama by following the instructions at https://ollama.com/library/llava

## Installation and Running Locally
1. Clone this repository to your local machine.
2. Ensure you have Docker and docker-compose installed.
3. Install Ollama and pull the Llava model as per the instructions in the Requirements section.
4. Navigate to the project directory in your terminal.
5. Run the application using docker-compose:
   ```
   docker-compose up --build
   ```
6. Access the application in your web browser at `http://localhost:5000`

## Notes
- The application uses the Llava API for image description. Ensure that Ollama is running and accessible at `http://host.docker.internal:11434/api/generate` from within the Docker container.
- Uploaded images are stored in the `uploads` directory.