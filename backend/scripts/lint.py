#!/usr/bin/env python3
"""Run code quality checks (linting, formatting, type checking) in proper environment."""

import os
import subprocess
import sys
from pathlib import Path


def check_virtual_environment():
    """Check if we're in a virtual environment."""
    if hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        return True

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
    """Check if linting dependencies are available."""
    missing = []

    try:
        import ruff
    except ImportError:
        missing.append("ruff")

    try:
        import black
    except ImportError:
        missing.append("black")

    try:
        import mypy
    except ImportError:
        missing.append("mypy")

    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("💡 Install dependencies: pip install -r requirements-dev.txt")
        return False

    print("✅ Linting dependencies available")
    return True


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n🔍 {description}...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 40)

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print(f"✅ {description} passed!")
    else:
        print(f"❌ {description} failed!")

    return result.returncode == 0


def main():
    """Run all code quality checks."""
    print("🔍 PDF OCR Converter API - Code Quality Checks")
    print("=" * 60)

    # Change to backend directory
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)

    print(f"📁 Working directory: {backend_dir.absolute()}")
    print(f"🐍 Python: {sys.executable}")

    # Check virtual environment
    if not check_virtual_environment():
        sys.exit(1)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    print("\nRunning code quality checks...")

    all_passed = True

    # Run ruff check (linting)
    if not run_command([sys.executable, "-m", "ruff", "check", "."], "Ruff linting"):
        all_passed = False

    # Run ruff format check
    if not run_command(
        [sys.executable, "-m", "ruff", "format", "--check", "."],
        "Ruff formatting check",
    ):
        all_passed = False

    # Run black check
    if not run_command(
        [sys.executable, "-m", "black", "--check", "."], "Black formatting check"
    ):
        all_passed = False

    # Run mypy type checking
    if not run_command([sys.executable, "-m", "mypy", "app/"], "MyPy type checking"):
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All code quality checks passed!")
    else:
        print("💥 Some code quality checks failed!")
        print("\nTo fix formatting issues, run:")
        print(f"  {sys.executable} -m ruff format .")
        print(f"  {sys.executable} -m black .")
        print("\nTo fix linting issues, run:")
        print(f"  {sys.executable} -m ruff check . --fix")
        sys.exit(1)


if __name__ == "__main__":
    main()
