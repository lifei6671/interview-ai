# Interview AI

## Project Structure

This project follows the [Standard Go Project Layout](https://github.com/golang-standards/project-layout).

- **`cmd/`**: Main applications for this project.
  - `cmd/server/`: The entry point for the server application.
- **`internal/`**: Private application and library code. This code is not importable by other applications.
- **`pkg/`**: Library code that's ok to use by external applications.
- **`api/`**: OpenAPI/Swagger specs, JSON schema files, protocol definition files.
- **`configs/`**: Configuration file templates or default configs.
- **`scripts/`**: Scripts to perform various build, install, analysis, etc operations.
- **`docs/`**: Design and user documents.

## Getting Started

### Prerequisites

- Go 1.25+

### Running the server

```bash
go run cmd/server/main.go
```
