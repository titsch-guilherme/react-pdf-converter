#!/usr/bin/env python3
"""Setup script for the PDF OCR Converter API with pyenv support."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description, check=True, capture_output=True):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}...")
    print(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd, check=check, capture_output=capture_output, text=True
        )
        if result.stdout and capture_output:
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr and capture_output:
            print(f"STDERR: {e.stderr.strip()}")
        return False


def get_pyenv_python_path(version="3.13.7"):
    """Get the full path to pyenv Python."""
    try:
        result = subprocess.run(
            ["pyenv", "prefix", version], capture_output=True, text=True, check=True
        )
        prefix = result.stdout.strip()
        return os.path.join(prefix, "bin", "python")
    except subprocess.CalledProcessError:
        return None


def check_pyenv():
    """Check if pyenv is available and working."""
    try:
        result = subprocess.run(
            ["pyenv", "--version"], capture_output=True, text=True, check=True
        )
        print(f"✅ {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pyenv not found. Please install pyenv first:")
        print("   macOS: brew install pyenv")
        print("   Linux: curl https://pyenv.run | bash")
        print("   Then add to your shell profile:")
        print('   export PATH="$HOME/.pyenv/bin:$PATH"')
        print('   eval "$(pyenv init -)"')
        return False


def setup_python_version():
    """Set up the correct Python version using pyenv."""
    target_version = "3.13.7"

    # Check if target version is installed
    try:
        result = subprocess.run(
            ["pyenv", "versions", "--bare"], capture_output=True, text=True, check=True
        )
        installed_versions = result.stdout.strip().split("\n")

        if target_version not in installed_versions:
            print(f"📥 Installing Python {target_version}...")
            if not run_command(
                ["pyenv", "install", target_version],
                f"Installing Python {target_version}",
                capture_output=False,
            ):
                print(f"❌ Failed to install Python {target_version}")
                print("💡 You can also install it manually: pyenv install 3.13.7")
                return False
        else:
            print(f"✅ Python {target_version} already installed")

        # Set local version
        if not run_command(
            ["pyenv", "local", target_version],
            f"Setting local Python version to {target_version}",
        ):
            return False

        # Get the Python path
        python_path = get_pyenv_python_path(target_version)
        if python_path and os.path.exists(python_path):
            print(f"✅ Python executable: {python_path}")

            # Test the Python version
            result = subprocess.run(
                [python_path, "--version"], capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"✅ {result.stdout.strip()}")
                return python_path

        return python_path

    except subprocess.CalledProcessError as e:
        print(f"❌ Error setting up Python version: {e}")
        return None


def setup_virtual_environment(python_path):
    """Set up virtual environment with specific Python version."""
    venv_path = Path("venv")

    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True

    print("📦 Creating virtual environment...")
    if not run_command(
        [python_path, "-m", "venv", "venv"], "Creating virtual environment"
    ):
        return False

    print("✅ Virtual environment created")
    return True


def get_venv_commands():
    """Get the correct commands for the virtual environment."""
    if os.name == "nt":  # Windows
        pip_cmd = str(Path("venv") / "Scripts" / "pip")
        python_cmd = str(Path("venv") / "Scripts" / "python")
    else:  # Unix-like
        pip_cmd = str(Path("venv") / "bin" / "pip")
        python_cmd = str(Path("venv") / "bin" / "python")

    return python_cmd, pip_cmd


def setup_directories():
    """Create necessary directories."""
    directories = ["uploads", "processed", "logs"]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")


def setup_environment():
    """Set up environment file."""
    env_example = Path(".env.example")
    env_file = Path(".env")

    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from .env.example")
        print("📝 Please edit .env file with your configuration")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("❌ .env.example file not found")
        return False

    return True


def install_dependencies():
    """Install Python dependencies in virtual environment."""
    python_cmd, pip_cmd = get_venv_commands()

    if not run_command([pip_cmd, "install", "--upgrade", "pip"], "Upgrading pip"):
        return False

    if not run_command(
        [pip_cmd, "install", "-r", "requirements-dev.txt"], "Installing dependencies"
    ):
        return False

    return True


def setup_pre_commit():
    """Set up pre-commit hooks."""
    python_cmd, _ = get_venv_commands()

    if not run_command(
        [python_cmd, "-m", "pre_commit", "install"], "Setting up pre-commit hooks"
    ):
        print("⚠️  Pre-commit setup failed, but continuing...")
        return True

    return True


def run_tests():
    """Run initial tests to verify setup."""
    print("\n🧪 Running initial tests...")
    python_cmd, _ = get_venv_commands()

    # Check if pytest is available
    result = subprocess.run(
        [python_cmd, "-m", "pytest", "--version"], capture_output=True, text=True
    )
    if result.returncode != 0:
        print("⚠️  Pytest not available, skipping tests")
        return True

    # Run a simple import test first
    test_cmd = [
        python_cmd,
        "-c",
        "from main import app; print('✅ FastAPI app imports successfully')",
    ]
    if not run_command(test_cmd, "Testing application imports", check=False):
        print("⚠️  Application import test failed, but setup continues")
        return True

    # Run actual tests
    if not run_command(
        [python_cmd, "-m", "pytest", "tests/", "-v", "--tb=short"],
        "Running tests",
        check=False,
    ):
        print("⚠️  Some tests failed, but setup is complete")
        return True

    return True


def verify_setup():
    """Verify the setup is working."""
    print("\n🔍 Verifying setup...")
    python_cmd, _ = get_venv_commands()

    # Test basic imports
    test_imports = [
        "import fastapi; print('✅ FastAPI available')",
        "import uvicorn; print('✅ Uvicorn available')",
        "import pytest; print('✅ Pytest available')",
        "import ruff; print('✅ Ruff available')",
    ]

    for test_import in test_imports:
        result = subprocess.run(
            [python_cmd, "-c", test_import], capture_output=True, text=True
        )
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print(f"⚠️  {test_import.split(';')[0]} - not available")


def create_activation_script():
    """Create a convenient activation script."""
    if os.name == "nt":  # Windows
        script_content = """@echo off
echo Activating PDF OCR Converter API environment...
call venv\\Scripts\\activate.bat
echo ✅ Environment activated!
echo 💡 Run: python scripts/start.py
"""
        script_path = Path("activate.bat")
    else:  # Unix-like
        script_content = """#!/bin/bash
echo "Activating PDF OCR Converter API environment..."
source venv/bin/activate
echo "✅ Environment activated!"
echo "💡 Run: python scripts/start.py"
"""
        script_path = Path("activate.sh")

    script_path.write_text(script_content)
    if not os.name == "nt":
        os.chmod(script_path, 0o755)

    print(f"✅ Created activation script: {script_path}")


def main():
    """Main setup function."""
    print("🚀 Setting up PDF OCR Converter API with pyenv")
    print("=" * 60)

    # Change to backend directory
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)
    print(f"📁 Working directory: {backend_dir.absolute()}")

    # Check pyenv
    if not check_pyenv():
        sys.exit(1)

    # Setup Python version with pyenv
    python_path = setup_python_version()
    if not python_path:
        print("❌ Failed to setup Python version")
        sys.exit(1)

    # Setup virtual environment
    if not setup_virtual_environment(python_path):
        print("❌ Failed to create virtual environment")
        sys.exit(1)

    # Setup directories
    setup_directories()

    # Setup environment
    if not setup_environment():
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)

    # Setup pre-commit
    setup_pre_commit()

    # Verify setup
    verify_setup()

    # Create activation script
    create_activation_script()

    # Run tests
    run_tests()

    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")

    # Show environment info
    python_cmd, _ = get_venv_commands()
    result = subprocess.run([python_cmd, "--version"], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"\n🐍 Python environment: {result.stdout.strip()}")

    print(f"📍 Virtual environment: {Path('venv').absolute()}")

    print("\nNext steps:")
    print("1. Activate virtual environment:")
    if os.name == "nt":
        print("   activate.bat")
        print("   # or: venv\\Scripts\\activate")
    else:
        print("   source activate.sh")
        print("   # or: source venv/bin/activate")
    print("2. Edit .env file with your configuration")
    print("3. Start the development server:")
    print("   python scripts/start.py")
    print("4. Visit http://localhost:8000/docs for API documentation")

    print("\nUseful commands (after activation):")
    print("- Run tests: python scripts/test.py")
    print("- Check code quality: python scripts/lint.py")
    print("- Start server: python scripts/start.py")
    print("- Verify structure: python scripts/verify.py")


if __name__ == "__main__":
    main()
