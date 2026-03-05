# AI Credit Decision Engine

A production-style AI decision system that recommends borrower interventions based on evolving repayment belief.

## Architecture

FastAPI API  
Postgres database (persistent borrower state)  
Redis cache layer  
Dockerized infrastructure

## Features

- Borrower state management
- Decision engine for intervention selection
- Persistent decision logs
- Redis caching layer
- Containerized deployment with Docker Compose

## Endpoints

POST `/recommend_action`  
Recommends an intervention for a borrower.

GET `/health`  
Health check endpoint.

## Run Locally

```bash
docker compose up --build