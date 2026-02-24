# TitanicGPT - Deployment Guide

This project is fully containerized and ready for production deployment using Docker Compose.

## Prerequisites
- Docker
- Docker Compose

## How to Deploy

1. **Clone/Upload the repository** to your server.
2. **Build and start the containers**:
   ```bash
   docker-compose up -d --build
   ```
3. **Access the application**:
   - The Streamlit frontend will be available at `http://your-server-ip:8501`
   - The FastAPI backend will be available at `http://your-server-ip:8000`

## Architecture overview
- **`backend` service**: Runs FastAPI with Uvicorn on port 8000. It reads the dataset and processes LLM queries.
- **`frontend` service**: Runs Streamlit on port 8501. It is configured via the `API_URL` environment variable to securely communicate with the backend service internally. 

*Note: You still need to provide your Gemini API key in the Streamlit UI sidebar once the application is running.*
