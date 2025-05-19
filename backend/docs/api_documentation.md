# API Documentation for Data Science App

## Overview

This document provides detailed information about the API endpoints available in the Data Science App. The API allows users to interact with the application for data ingestion, querying, and processing.

## Endpoints

### Fetch Data

- **Endpoint**: `GET /api/fetch`
- **Description**: Fetch data from configured sources.
- **Request Parameters**: 
  - `source`: The data source to fetch from (e.g., URL).
- **Response**: 
  - `200 OK`: Returns the fetched data.
  - `400 Bad Request`: If the source is invalid.

### Query Data

- **Endpoint**: `GET /api/query`
- **Description**: Query data stored in DuckDB.
- **Request Parameters**: 
  - `query`: The SQL query to execute.
- **Response**: 
  - `200 OK`: Returns the query results.
  - `500 Internal Server Error`: If the query fails.

### Transform Data

- **Endpoint**: `POST /api/transform`
- **Description**: Transform data using specified rules.
- **Request Body**: 
  - `rules`: Transformation rules to apply.
- **Response**: 
  - `200 OK`: Returns the transformed data.
  - `400 Bad Request`: If the rules are invalid.

---
