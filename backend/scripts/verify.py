#!/usr/bin/env python3
"""Verify the backend application structure and configuration."""

import os
import sys
from pathlib import Path


def check_file_exists(file_path, description):
    """Check if a file exists."""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} (MISSING)")
        return False


def check_directory_exists(dir_path, description):
    """Check if a directory exists."""
    if Path(dir_path).is_dir():
        print(f"✅ {description}: {dir_path}")
        return True
    else:
        print(f"❌ {description}: {dir_path} (MISSING)")
        return False


def main():
    """Verify the backend application structure."""
    print("🔍 Verifying PDF OCR Converter API Backend Structure")
    print("=" * 60)

    # Change to backend directory
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)

    all_good = True

    # Core application files
    print("\n📁 Core Application Files:")
    core_files = [
        ("main.py", "Application entry point"),
        ("requirements.txt", "Production dependencies"),
        ("requirements-dev.txt", "Development dependencies"),
        ("pyproject.toml", "Tool configuration"),
        (".env.example", "Environment template"),
        ("Dockerfile", "Container configuration"),
        ("docker-compose.yml", "Docker Compose configuration"),
        ("README.md", "Documentation"),
        (".pre-commit-config.yaml", "Pre-commit configuration"),
    ]

    for file_path, description in core_files:
        if not check_file_exists(file_path, description):
            all_good = False

    # Application structure
    print("\n📁 Application Structure:")
    app_dirs = [
        ("app", "Main application package"),
        ("app/api", "API package"),
        ("app/api/v1", "API v1 package"),
        ("app/api/v1/endpoints", "API endpoints"),
        ("app/core", "Core functionality"),
        ("app/services", "Business logic services"),
        ("app/schemas", "Pydantic schemas"),
        ("app/utils", "Utility functions"),
        ("app/models", "Data models"),
        ("tests", "Test suite"),
        ("tests/api", "API tests"),
        ("tests/services", "Service tests"),
        ("tests/utils", "Utility tests"),
        ("scripts", "Development scripts"),
    ]

    for dir_path, description in app_dirs:
        if not check_directory_exists(dir_path, description):
            all_good = False

    # Key application files
    print("\n📁 Key Application Files:")
    key_files = [
        ("app/__init__.py", "App package init"),
        ("app/core/config.py", "Configuration management"),
        ("app/core/security.py", "Security utilities"),
        ("app/core/dependencies.py", "FastAPI dependencies"),
        ("app/core/middleware.py", "Custom middleware"),
        ("app/core/logging.py", "Logging configuration"),
        ("app/api/v1/api.py", "API router"),
        ("app/api/v1/endpoints/auth.py", "Authentication endpoints"),
        ("app/api/v1/endpoints/convert.py", "Conversion endpoints"),
        ("app/api/v1/endpoints/status.py", "Status endpoints"),
        ("app/api/v1/endpoints/download.py", "Download endpoints"),
        ("app/services/conversion.py", "Conversion service"),
        ("app/schemas/auth.py", "Authentication schemas"),
        ("app/schemas/convert.py", "Conversion schemas"),
        ("app/schemas/status.py", "Status schemas"),
        ("app/utils/validation.py", "File validation"),
        ("app/utils/file_handler.py", "File handling"),
    ]

    for file_path, description in key_files:
        if not check_file_exists(file_path, description):
            all_good = False

    # Development scripts
    print("\n📁 Development Scripts:")
    script_files = [
        ("scripts/start.py", "Development server starter"),
        ("scripts/test.py", "Test runner"),
        ("scripts/lint.py", "Code quality checker"),
        ("scripts/setup.py", "Setup script"),
        ("scripts/verify.py", "Structure verification"),
    ]

    for file_path, description in script_files:
        if not check_file_exists(file_path, description):
            all_good = False

    # Test files
    print("\n📁 Test Files:")
    test_files = [
        ("tests/conftest.py", "Pytest configuration"),
        ("tests/api/test_health.py", "Health endpoint tests"),
        ("tests/api/test_auth.py", "Authentication tests"),
        ("tests/api/test_convert.py", "Conversion tests"),
        ("tests/services/test_conversion.py", "Conversion service tests"),
        ("tests/utils/test_validation.py", "Validation tests"),
    ]

    for file_path, description in test_files:
        if not check_file_exists(file_path, description):
            all_good = False

    # Count files
    print("\n📊 File Statistics:")
    py_files = list(Path(".").rglob("*.py"))
    print(f"✅ Total Python files: {len(py_files)}")

    test_files = list(Path("tests").rglob("*.py"))
    print(f"✅ Test files: {len(test_files)}")

    app_files = list(Path("app").rglob("*.py"))
    print(f"✅ Application files: {len(app_files)}")

    # Final result
    print("\n" + "=" * 60)
    if all_good:
        print("🎉 All structure verification checks passed!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements-dev.txt")
        print("2. Set up environment: cp .env.example .env")
        print("3. Run setup script: python scripts/setup.py")
        print("4. Start development server: python scripts/start.py")
    else:
        print("❌ Some structure verification checks failed!")
        print("Please ensure all required files are present.")
        sys.exit(1)


if __name__ == "__main__":
    main()
