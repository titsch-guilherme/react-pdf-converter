# PDF OCR Converter API

A FastAPI-based backend service for converting PDFs to searchable PDFs using OCR technology. This service supports batch file processing, real-time status tracking, and Google OAuth authentication.

## Features

- **Batch PDF Processing**: Upload and convert multiple PDF files simultaneously
- **Real-time Status Tracking**: Monitor conversion progress with detailed status updates
- **Google OAuth Integration**: Secure authentication using Google OAuth tokens
- **RESTful API**: Clean, documented API endpoints with OpenAPI/Swagger documentation
- **Async Processing**: Background job processing with progress tracking
- **File Validation**: Comprehensive validation for file type, size, and content
- **Rate Limiting**: Built-in rate limiting to prevent abuse
- **Structured Logging**: Comprehensive logging with request tracing
- **Docker Support**: Containerized deployment with Docker and Docker Compose

## Quick Start

### Prerequisites

- Python 3.13.x
- pip (Python package manager)
- Docker (optional, for containerized deployment)

### Local Development Setup

1. **Clone and navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3.13 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements-dev.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Run the development server**:
   ```bash
   python scripts/start.py
   # Or directly: uvicorn main:app --reload
   ```

6. **Access the application**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

### Docker Development Setup

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **Access the application**:
   - Same URLs as local development

## API Documentation

### Authentication

All API endpoints (except `/health` and `/docs`) require authentication using a session ID obtained from Google OAuth token validation.

#### Validate Google OAuth Token
```http
POST /api/v1/auth/validate
Content-Type: application/json

{
  "access_token": "google_oauth_access_token"
}
```

**Response**:
```json
{
  "session_id": "session_uuid",
  "user_id": "google_user_id",
  "expires_at": "2025-01-XX T XX:XX:XX",
  "user_info": {
    "email": "user@example.com",
    "name": "User Name",
    "picture": "profile_picture_url"
  }
}
```

### File Conversion

#### Convert PDF Files
```http
POST /api/v1/convert
Content-Type: multipart/form-data
session-id: your_session_id

files: [file1.pdf, file2.pdf, ...]
```

**Response**:
```json
{
  "jobs": [
    {
      "job_id": "job_uuid",
      "filename": "file1.pdf",
      "status": "queued"
    }
  ]
}
```

### Status Tracking

#### Get Job Status
```http
GET /api/v1/status/{job_id}
session-id: your_session_id
```

**Response**:
```json
{
  "job_id": "job_uuid",
  "filename": "file.pdf",
  "status": "completed",
  "progress": 100,
  "created_at": "2025-01-XX T XX:XX:XX",
  "updated_at": "2025-01-XX T XX:XX:XX",
  "download_url": "/api/v1/download/job_uuid",
  "error": null
}
```

#### Get All User Jobs
```http
GET /api/v1/status
session-id: your_session_id
```

### File Download

#### Download Converted File
```http
GET /api/v1/download/{job_id}
session-id: your_session_id
```

Returns the converted PDF file as a download attachment.

## Development

### Code Quality

This project uses modern Python tooling for code quality:

- **Ruff**: Ultra-fast linting and import sorting
- **Black**: Code formatting
- **MyPy**: Static type checking
- **Pre-commit**: Git hooks for code quality

#### Run Code Quality Checks
```bash
python scripts/lint.py
```

#### Auto-fix Formatting Issues
```bash
ruff format .
black .
```

### Testing

The project includes comprehensive test coverage with pytest:

```bash
# Run all tests with coverage
python scripts/test.py

# Run specific test file
pytest tests/api/test_auth.py -v

# Run tests with coverage report
pytest --cov=app --cov-report=html
```

### Pre-commit Hooks

Set up pre-commit hooks to ensure code quality:

```bash
pre-commit install
```

This will run linting, formatting, and type checking on every commit.

## Configuration

### Environment Variables

Key configuration options (see `.env.example` for full list):

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Environment: development, testing, production |
| `DEBUG` | `true` | Enable debug mode |
| `MAX_FILE_SIZE_MB` | `50` | Maximum file size in MB |
| `MAX_FILES_PER_BATCH` | `10` | Maximum files per batch upload |
| `SESSION_EXPIRE_HOURS` | `24` | Session expiration time |
| `RATE_LIMIT_PER_MINUTE` | `60` | Rate limit per user per minute |
| `LOG_LEVEL` | `INFO` | Logging level |

### File Storage

- **Upload Directory**: `uploads/` (configurable via `UPLOAD_DIR`)
- **Processed Directory**: `processed/` (configurable via `PROCESSED_DIR`)

Files are automatically cleaned up after 24 hours (configurable).

## Architecture

### Project Structure

```
backend/
├── app/
│   ├── api/v1/endpoints/     # API endpoint handlers
│   ├── core/                 # Core functionality (config, security, middleware)
│   ├── services/             # Business logic services
│   ├── schemas/              # Pydantic models for request/response
│   ├── utils/                # Utility functions
│   └── models/               # Data models (future database integration)
├── tests/                    # Test suite
├── scripts/                  # Development scripts
├── main.py                   # Application entry point
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── pyproject.toml           # Tool configuration
└── Dockerfile               # Container configuration
```

### Key Components

- **FastAPI Application**: Modern, fast web framework with automatic API documentation
- **Async Processing**: Background job processing using asyncio
- **Session Management**: In-memory session storage (Redis recommended for production)
- **File Validation**: Comprehensive validation using file content analysis
- **Structured Logging**: JSON-formatted logs with request tracing
- **Error Handling**: Comprehensive error handling with proper HTTP status codes

## Deployment

### Production Considerations

1. **Session Storage**: Replace in-memory session storage with Redis
2. **File Storage**: Use cloud storage (AWS S3, Google Cloud Storage) for scalability
3. **Database**: Add database for persistent job storage and user management
4. **Load Balancing**: Use multiple instances behind a load balancer
5. **Monitoring**: Add application monitoring and alerting
6. **Security**: Implement additional security measures (WAF, DDoS protection)

### Docker Production Deployment

```bash
# Build production image
docker build -t pdf-ocr-api .

# Run production container
docker run -d \
  --name pdf-ocr-api \
  -p 8000:8000 \
  -e ENVIRONMENT=production \
  -e DEBUG=false \
  -v /path/to/uploads:/app/uploads \
  -v /path/to/processed:/app/processed \
  pdf-ocr-api
```

## Monitoring and Logging

### Health Check

The application provides a health check endpoint:

```http
GET /health
```

Returns application status, version, and environment information.

### Logging

All requests are logged with structured JSON format including:

- Request ID for tracing
- User ID and session information
- Processing times
- Error details with context

Logs are written to stdout and can be collected by log aggregation systems.

### Metrics

Key metrics to monitor:

- Request rate and response times
- Conversion success/failure rates
- File processing times
- Active sessions and concurrent jobs
- Error rates by endpoint

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're in the correct directory and virtual environment is activated
2. **Permission Errors**: Check file permissions for upload/processed directories
3. **Port Already in Use**: Change the port in the start command or stop conflicting services
4. **Memory Issues**: Monitor memory usage during large file processing

### Debug Mode

Enable debug mode for detailed error information:

```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
```

### Log Analysis

Check application logs for detailed error information:

```bash
# View recent logs
tail -f logs/app.log

# Search for specific errors
grep "ERROR" logs/app.log
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and code quality checks
5. Submit a pull request

### Development Workflow

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
python scripts/test.py

# Run code quality checks
python scripts/lint.py

# Start development server
python scripts/start.py
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For support and questions:

1. Check the API documentation at `/docs`
2. Review the troubleshooting section
3. Check application logs for error details
4. Create an issue in the project repository
