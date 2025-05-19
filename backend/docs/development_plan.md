# Local-First Application (Data Science App to Process 1M-80M Rows)

## Overview

**Goal:** Build a performant and scalable local-first backend for ingesting, storing, processing, and serving large datasets (1M-80M rows) efficiently to a local frontend.

We will utilize AKA, SOLID, DDD, TDD, and Hexagonal Architecture to create modular code with small components that can be added, changed, improved, and extended in the future.

## Architecture

- **Ingestion:** Fetch and validate data daily using Polars, httpx, and pydantic.
- **Storage & Querying:** Parquet will serve as the primary storage format, with DuckDB used for in-memory analytics and persistent storage.
- **Processing:** Utilize Polars and DuckDB for filtering, aggregations, and slicing.
- **Server:** FastAPI will handle REST and WebSocket for streaming communication with the frontend.

### Constraints

- Local-first application targeting 8 GB RAM.
- Parquet-based storage (24 MB per 1M rows, 1.92 GB for 80M rows).
- Capable of handling up to 10 data sources, ingesting a maximum of 10M rows daily.
- Scalable processing for up to 80M rows using chunking and efficient query execution.

## Approach

- Develop in modular, testable increments, prioritizing core backend functionality first.
- Employ lazy evaluation and data chunking to optimize performance and memory usage.
- Focus on comprehensive unit tests and performance benchmarks throughout the development lifecycle.

## Development Plan: Backend Steps

### Phase 1: Core Ingestion and Storage (2-3 weeks)

**Objective:** Establish the foundation for fetching, validating, and storing data efficiently in Parquet format.

**Tasks:**

- **Environment Setup:**
  - Structure the project (e.g., `src/ingestion`, `src/storage`, `tests/`).
  - Install essential dependencies: Polars, httpx, pydantic, DuckDB.
  - Configure the virtual environment and linting tools (e.g., black, flake8).

- **Source Configuration:**
  - Define a flexible configuration mechanism (e.g., `sources.yaml`) to manage up to 10 data source details (URLs, API keys).
  - Implement robust schema validation using pydantic.

- **Data Ingestion Logic:**
  - Develop an asynchronous data fetching module (httpx) capable of concurrently downloading data from configured sources (CSV, JSON).
  - Utilize Polars for efficient parsing, validation, and transformation of incoming data into the Parquet format (~24 MB per 1M rows).
  - Implement intelligent chunking mechanisms in Polars for handling large data sources (>1M rows).

- **Parquet Storage:**
  - Implement a storage manager to organize and persist Parquet files locally.
  - Log essential metadata about each ingestion process (e.g., source, timestamp, row count).

- **Testing:**
  - Write comprehensive unit tests for the data fetching, validation, and Parquet writing functionalities.
  - Establish baseline performance benchmarks for the ingestion process.

**Deliverables:**
- Functional ingestion module.
- Well-defined configuration file and sample data.
- A suite of unit tests and initial performance benchmarks achieving ~90% code coverage.

### Phase 2: Data Access and Core Processing with DuckDB (3-4 weeks)

**Objective:** Integrate DuckDB for efficient in-memory querying and implement core data processing functionalities (filtering, aggregations).

**Tasks:**

- **Parquet Integration with DuckDB:**
  - Develop a DuckDB storage interface to seamlessly read Parquet files directly into DuckDB's in-memory database.
  - Implement functions to efficiently query the Parquet data loaded into DuckDB.

- **Core Data Processing:**
  - Build a dedicated processing module leveraging the power of Polars and DuckDB.
  - Implement flexible filtering capabilities and common aggregation functions.

- **Testing:**
  - Develop comprehensive unit tests for the data access and processing functionalities.
  - Establish performance benchmarks for filtering and aggregation operations.

**Deliverables:**
- DuckDB integration for Parquet access and querying.
- A robust processing module with filtering and aggregation capabilities.
- A comprehensive suite of unit tests and performance benchmarks.

### Phase 3: Backend Server and API Development (3-4 weeks)

**Objective:** Build the FastAPI server to expose data access and processing functionalities to the local frontend via REST and WebSockets.

**Tasks:**

- **FastAPI Application Setup:**
  - Initialize the FastAPI application.
  - Configure uvicorn for local development and deployment.

- **RESTful API Endpoints:**
  - Implement endpoints for filtering, aggregation, slicing, and data download.
  - Implement a WebSocket endpoint for real-time streaming of data slices.

- **Integration:**
  - Connect the FastAPI routes and WebSocket handlers to the underlying processing and data access modules.

- **Testing:**
  - Write unit and integration tests for all API endpoints.
  - Conduct performance benchmarks for API responses.

**Deliverables:**
- A fully functional FastAPI server with well-defined REST and WebSocket endpoints.
- Comprehensive API tests and performance metrics.

### Phase 4: Optimization, Scalability, and Documentation (2-3 weeks)

**Objective:** Optimize the backend for handling large datasets (up to 80M rows), ensure robustness, and create comprehensive documentation.

**Tasks:**

- **Performance Optimization:**
  - Refine the use of Polars' lazy evaluation and DuckDB's efficient query execution for handling large datasets.

- **Robust Error Handling:**
  - Implement comprehensive error handling throughout the application.

- **Benchmarking and Validation:**
  - Conduct thorough performance testing with various data sizes and validate resource usage.

- **Documentation:**
  - Generate API documentation and create a detailed setup and deployment guide.

**Deliverables:**
- An optimized and robust backend capable of handling 80M rows efficiently.
- Comprehensive documentation covering the API, architecture, and deployment.

## Total Timeline

**Duration:** 10-14 weeks (200-280 hours, ~2.5-3.5 months).

**Milestones:**
- Week 3: Core Ingestion and Storage complete (tested with 1M rows).
- Week 7: Data Access and Core Processing with DuckDB complete (tested with 10M rows).
- Week 11: Backend Server and API complete (tested with 10M rows).
- Week 14: Backend optimized and documented for 80M rows.

## Scalability Considerations (1M-80M Rows)

- **1M Rows:** ~24 MB Parquet, minimal chunking.
- **10M Rows:** ~240 MB Parquet, optional chunking for processing.
- **80M Rows:** ~1.92 GB Parquet, mandatory chunking for processing.

By focusing on DuckDB's capabilities for both in-memory analytics and persistent storage, we can simplify the technology stack and improve overall efficiency.