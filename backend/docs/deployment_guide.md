# Deployment Guide for Data Science App

## Overview

This guide provides instructions for deploying the Data Science App in various environments.

## Local Deployment

1. **Set Up Environment Variables**: Create a `.env` file with necessary configurations.
2. **Run the Application**:
   ```bash
   poetry run uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Production Deployment

1. **Choose a Hosting Provider**: Select a cloud provider (e.g., AWS, Azure).
2. **Set Up a Production Environment**: Configure the server and environment variables.
3. **Deploy the Application**: Use a process manager (e.g., Gunicorn) to run the application.

---
