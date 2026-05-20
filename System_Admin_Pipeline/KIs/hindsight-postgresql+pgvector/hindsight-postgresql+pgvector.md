# KI: Hindsight PostgreSQL+pgvector Configuration

## Summary

This document outlines the configuration for the PostgreSQL database used by the Hindsight API, which includes the `pgvector` extension for vector similarity search. The database is deployed as a Docker container and listens on a non-standard port to meet specific system requirements.

## Key Facts

- **Deployment:** The database runs inside a Docker container.
- **Port:** It listens on port `5433` instead of the default `5432`. This is specifically to accommodate glibc requirements.
- **Client:** The primary client is the Hindsight API, a Python service.
- **Connection URL:** The `HINDSIGHT_API_DATABASE_URL` environment variable is used by the API to connect to the database.

### Connection String

The full database connection URL is:

`postgresql://hindsight:hindsight@localhost:5433/hindsight`

- **Driver:** `postgresql://`
- **Username:** `hindsight`
- **Password:** `hindsight`
- **Host:** `localhost`
- **Port:** `5433`
- **Database Name:** `hindsight`
