#!/usr/bin/env python3
"""Start the FastAPI development server with proper environment setup."""

import os
import subprocess
import sys
from pathlib import Path


def check_virtual_environment():
    """Check if we're in a virtual environment or can activate one."""
    # Check if already in virtual environment
    if hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("✅ Virtual environment is active")
        return True

    # Check if virtual environment exists
    venv_path = Path("venv")
    if venv_path.exists():
        print("⚠️  Virtual environment exists but not activated")
        print("💡 Please activate it first:")
        if os.name == "nt":
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        return False

    print("❌ Virtual environment not found")
    print("💡 Run setup first: python scripts/setup.py")
    return False


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import fastapi
        import uvicorn

        print("✅ Core dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("💡 Install dependencies: pip install -r requirements-dev.txt")
        return False


def check_environment_file():
    """Check if .env file exists."""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Environment file found")
        return True
    else:
        print("⚠️  .env file not found")
        print("💡 Copy from template: cp .env.example .env")
        # Continue anyway with defaults
        return True


def get_python_info():
    """Get Python version and path information."""
    print(f"🐍 Python version: {sys.version}")
    print(f"📍 Python executable: {sys.executable}")

    # Check if using pyenv
    try:
        result = subprocess.run(
            ["pyenv", "version"], capture_output=True, text=True, check=True
        )
        print(f"🔧 Pyenv version: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("🔧 Pyenv: Not detected")


def start_server():
    """Start the FastAPI development server."""
    try:
        # Import here to ensure dependencies are available
        import uvicorn

        print("\n🚀 Starting FastAPI development server...")
        print("📡 Server will be available at: http://localhost:8000")
        print("📚 API documentation: http://localhost:8000/docs")
        print("📖 Alternative docs: http://localhost:8000/redoc")
        print("❤️  Health check: http://localhost:8000/health")
        print("\n⏹️  Press Ctrl+C to stop the server")
        print("=" * 50)

        # Start uvicorn with reload
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            reload_dirs=["app"],
            reload_excludes=["tests", "scripts", "uploads", "processed", "logs"],
        )

    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print(
            "💡 Make sure dependencies are installed: pip install -r requirements-dev.txt"
        )
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)


def main():
    """Main function to start the development server."""
    print("🚀 PDF OCR Converter API - Development Server")
    print("=" * 50)

    # Change to backend directory
    backend_dir = Path(__file__).parent.parent
    original_dir = Path.cwd()
    os.chdir(backend_dir)

    try:
        print(f"📁 Working directory: {backend_dir.absolute()}")

        # Get Python info
        get_python_info()

        # Check virtual environment
        if not check_virtual_environment():
            print("\n💡 To activate virtual environment and start server:")
            if os.name == "nt":
                print("   venv\\Scripts\\activate && python scripts/start.py")
            else:
                print("   source venv/bin/activate && python scripts/start.py")
            sys.exit(1)

        # Check dependencies
        if not check_dependencies():
            sys.exit(1)

        # Check environment file
        check_environment_file()

        # Start the server
        start_server()

    finally:
        # Return to original directory
        os.chdir(original_dir)


if __name__ == "__main__":
    main()
