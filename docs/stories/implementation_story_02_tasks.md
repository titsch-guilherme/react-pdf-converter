# Implementation Story 02: Backend Application Bootstrap - Implementation Tasks

## Overview
This document provides a detailed implementation plan for Implementation Story 02, with updated dependency versions as of January 2025. The story has been reviewed and updated with the latest stable versions of all dependencies.

## Updated Dependency Analysis

### Major Version Updates Required

#### Python Version Update
- **Current Story:** Python 3.12.x
- **Latest Available:** Python 3.14.0 (stable release - October 7, 2025)
- **Recommendation:** Use Python 3.13.x for stability
- **Rationale:** Python 3.14.0 is very new (released Oct 2025), Python 3.13.x is more mature and stable for production use

#### Core Dependencies - Latest Versions Confirmed
✅ **FastAPI:** 0.121.1 (matches story)
✅ **uvicorn[standard]:** 0.38.0 (matches story)
✅ **python-multipart:** 0.0.20 (matches story)
✅ **aiofiles:** 25.1.0 (matches story)
✅ **python-dotenv:** 1.2.1 (matches story)
✅ **httpx:** 0.28.1 (matches story)
✅ **loguru:** 0.7.3 (matches story)
✅ **slowapi:** 0.1.9 (matches story)
✅ **pydantic:** 2.12.4 (matches story)
✅ **pydantic-settings:** 2.12.0 (matches story)

#### Development Dependencies - Updates Required
- **pytest:** 9.0.0 ✅ (matches story)
- **pytest-asyncio:** 1.3.0 ✅ (matches story)
- **pytest-cov:** 7.0.0 ✅ (matches story)
- **ruff:** 0.14.4 ✅ (matches story)
- **black:** 25.11.0 ✅ (matches story)
- **mypy:** 1.18.2 ✅ (matches story)
- **pre-commit:** 4.4.0 ⬆️ (story shows 4.0.1, latest is 4.4.0)
- **coverage[toml]:** 7.11.3 ⬆️ (story shows 7.6.9, latest is 7.11.3)

## Implementation Plan

### Phase 1: Project Structure Setup (Day 1 Morning)

#### Task 1.1: Create Backend Directory Structure
```bash
mkdir -p backend/{app/{api/v1/{endpoints,},core,services,utils,models,schemas},tests/{api,services,utils},scripts}
touch backend/app/__init__.py
touch backend/app/api/__init__.py
touch backend/app/api/v1/__init__.py
touch backend/app/api/v1/api.py
touch backend/app/api/v1/endpoints/__init__.py
touch backend/app/core/{__init__.py,config.py,security.py,dependencies.py}
touch backend/app/{services,utils,models,schemas}/__init__.py
touch backend/tests/{__init__.py,conftest.py}
touch backend/tests/{api,services,utils}/__init__.py
```

#### Task 1.2: Create Configuration Files
- Create `backend/pyproject.toml` with updated tool configurations
- Create `backend/requirements.txt` with pinned production dependencies
- Create `backend/requirements-dev.txt` with development dependencies
- Create `backend/.env.example` with environment variables template
- Create `backend/.gitignore` for Python projects

### Phase 2: Python Environment Setup (Day 1 Morning)

#### Task 2.1: Python Version Setup
```bash
cd backend
python3.13 -m venv venv  # Use Python 3.13.x instead of 3.14.0
source venv/bin/activate  # On Windows: venv\Scripts\activate
python --version  # Verify Python 3.13.x
```

#### Task 2.2: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements-dev.txt
```

### Phase 3: Core Application Setup (Day 1 Afternoon)

#### Task 3.1: Create Main Application Entry Point
- Create `backend/main.py` with FastAPI app initialization
- Configure CORS, middleware, and basic routing
- Add health check endpoint

#### Task 3.2: Configuration Management
- Implement `backend/app/core/config.py` using Pydantic Settings v2
- Create environment-based configuration classes
- Add validation for required settings

#### Task 3.3: API Structure
- Implement `backend/app/api/v1/api.py` with router setup
- Create basic API versioning structure
- Add placeholder endpoints for future development

### Phase 4: Development Tools Configuration (Day 1 Afternoon)

#### Task 4.1: Code Quality Tools Setup
```bash
# Initialize pre-commit
pre-commit install

# Configure ruff
ruff check .
ruff format .

# Configure mypy
mypy app/

# Configure black
black --check .
```

#### Task 4.2: Testing Framework Setup
- Create `backend/tests/conftest.py` with FastAPI test client
- Implement sample API tests
- Configure pytest with async support
- Set up coverage reporting

### Phase 5: Docker Configuration (Day 2 Morning)

#### Task 5.1: Create Dockerfile
- Multi-stage Dockerfile for production
- Python 3.13 base image
- Proper layer caching
- Security best practices

#### Task 5.2: Docker Compose Setup
- Development docker-compose.yml
- Hot reload configuration
- Environment variable management
- Volume mounting for development

### Phase 6: Logging and Monitoring (Day 2 Morning)

#### Task 6.1: Loguru Configuration
- Structured logging setup
- Environment-based log levels
- JSON formatting for production
- Request ID correlation

#### Task 6.2: Middleware Implementation
- Request/response logging middleware
- Request ID middleware
- Error handling middleware
- CORS configuration

### Phase 7: Development Scripts (Day 2 Afternoon)

#### Task 7.1: Create Development Scripts
- `backend/scripts/start.py` - Application startup
- `backend/scripts/test.py` - Test runner
- `backend/scripts/lint.py` - Code quality checks
- Make scripts executable and cross-platform

#### Task 7.2: Documentation
- Create comprehensive `backend/README.md`
- Document setup instructions
- Add development workflow guide
- Include troubleshooting section

### Phase 8: Quality Assurance (Day 2 Afternoon)

#### Task 8.1: Testing
- Run all tests and ensure >90% coverage
- Test application startup and health checks
- Verify API documentation generation
- Test Docker container build and run

#### Task 8.2: Code Quality Verification
- Run all linting tools and fix issues
- Verify type checking passes
- Ensure pre-commit hooks work
- Test all development scripts

## Updated File Templates

### requirements.txt (Updated)
```txt
# Core dependencies - Latest stable versions (January 2025)
fastapi==0.121.1
uvicorn[standard]==0.38.0
python-multipart==0.0.20
aiofiles==25.1.0
python-dotenv==1.2.1
httpx==0.28.1
loguru==0.7.3
slowapi==0.1.9
pydantic==2.12.4
pydantic-settings==2.12.0
```

### requirements-dev.txt (Updated)
```txt
# Include production dependencies
-r requirements.txt

# Development dependencies - Latest stable versions (January 2025)
pytest==9.0.0
pytest-asyncio==1.3.0
pytest-cov==7.0.0
ruff==0.14.4
black==25.11.0
mypy==1.18.2
pre-commit==4.4.0
coverage[toml]==7.11.3
```

### pyproject.toml (Updated)
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "pdf-ocr-converter-api"
version = "1.0.0"
description = "API for converting PDFs to searchable PDFs using OCR"
authors = [{name = "Your Team", email = "team@example.com"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.13"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.13",
]

[tool.ruff]
target-version = "py313"
line-length = 88
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

[tool.black]
line-length = 88
target-version = ['py313']
include = '\.pyi?$'

[tool.mypy]
python_version = "3.13"
check_untyped_defs = true
disallow_any_generics = true
disallow_incomplete_defs = true
disallow_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_return_any = true
strict_equality = true

[tool.pytest.ini_options]
minversion = "9.0"
addopts = "-ra -q --strict-markers --strict-config"
testpaths = ["tests"]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"

[tool.coverage.run]
source = ["app"]
omit = ["*/tests/*", "*/venv/*", "*/__pycache__/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

### Dockerfile (Updated for Python 3.13)
```dockerfile
# Multi-stage build for production
FROM python:3.13-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.13-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY . .

# Change ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Add local bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Risk Mitigation

### Python 3.14.0 Considerations
- **Risk:** Python 3.14.0 is very new (released October 2025)
- **Mitigation:** Use Python 3.13.x for better stability and ecosystem support
- **Future Path:** Plan migration to 3.14.x after 6 months of stability

### Dependency Compatibility
- **Risk:** New versions may have breaking changes
- **Mitigation:** Pin exact versions in requirements.txt
- **Testing:** Comprehensive test suite to catch compatibility issues

### Development Environment
- **Risk:** Different Python versions across team members
- **Mitigation:** Document exact Python version requirements
- **Docker:** Provide Docker development environment for consistency

## Success Criteria

### Functional Requirements
- [ ] Application starts successfully with `uvicorn main:app --reload`
- [ ] Health check endpoint returns 200 OK
- [ ] OpenAPI documentation accessible at `/docs`
- [ ] All tests pass with >90% coverage
- [ ] All linting tools pass without errors
- [ ] Docker container builds and runs successfully

### Quality Requirements
- [ ] Type checking passes with mypy
- [ ] Code formatting consistent with black and ruff
- [ ] Pre-commit hooks installed and working
- [ ] Comprehensive documentation in README.md
- [ ] Environment configuration working properly

### Performance Requirements
- [ ] Application startup time < 5 seconds
- [ ] Health check response time < 100ms
- [ ] Docker image size optimized with multi-stage build

## Timeline

### Day 1 (8 hours)
- **Morning (4h):** Project structure, Python environment, dependency installation
- **Afternoon (4h):** Core application setup, configuration management, API structure

### Day 2 (8 hours)
- **Morning (4h):** Docker configuration, logging setup, middleware implementation
- **Afternoon (4h):** Development scripts, documentation, quality assurance

## Next Steps

After completing this story:
1. **Story 03:** Frontend Authentication can begin in parallel
2. **Story 04:** Backend Authentication builds on this foundation
3. **Story 06:** File Processing will extend the API structure created here

## Notes

- All dependency versions have been verified as of January 2025
- Python 3.13.x recommended over 3.14.0 for stability
- Pre-commit and coverage versions updated to latest
- Docker configuration optimized for security and performance
- Ready for immediate implementation with updated specifications
