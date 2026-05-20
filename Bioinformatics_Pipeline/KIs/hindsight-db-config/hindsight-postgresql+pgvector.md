# Hindsight: PostgreSQL+pgvector Configuration

## Overview

This document outlines the standard configuration for the PostgreSQL database with the pgvector extension, as used by the Hindsight API. The database is containerized using Docker to manage specific system dependencies and avoid conflicts with host-level services.

## Key Configuration

-   **Database Type**: PostgreSQL with pgvector extension.
-   **Deployment**: Docker Container
-   **Host**: `localhost`
-   **Port**: `5433`
-   **Connection URL**: The Hindsight API service is configured to connect to the database using the following URL:
    ```env
    HINDSIGHT_API_DATABASE_URL=postgresql://hindsight:hindsight@localhost:5433/hindsight
    ```

## Rationale

The PostgreSQL+pgvector instance for Hindsight is intentionally deployed as a Docker container. This strategic choice addresses specific `glibc` (GNU C Library) version requirements, ensuring a stable and compatible runtime environment.

To prevent potential conflicts with any existing PostgreSQL instances running on the host machine, the container is configured to listen on the non-standard port `5433`. The Hindsight API, a Python service, is specifically configured to target this port for all database connections.
