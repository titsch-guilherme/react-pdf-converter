#!/usr/bin/env python3
"""Run tests with coverage reporting in proper environment."""

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
    """Check if test dependencies are available."""
    try:
        import coverage
        import pytest

        print("✅ Test dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing test dependencies: {e}")
        print("💡 Install dependencies: pip install -r requirements-dev.txt")
        return False


def run_tests():
    """Run pytest with coverage."""
    try:
        # Change to backend directory
        backend_dir = Path(__file__).parent.parent
        os.chdir(backend_dir)

        print("🧪 Running tests with coverage...")
        print(f"📁 Working directory: {backend_dir.absolute()}")
        print(f"🐍 Python: {sys.executable}")

        # Run pytest with coverage
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "--cov=app",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-report=xml",
            "--cov-fail-under=80",  # Lower threshold for initial setup
            "-v",
            "--tb=short",
        ]

        print(f"Command: {' '.join(cmd)}")
        print("=" * 50)

        result = subprocess.run(cmd)

        print("=" * 50)
        if result.returncode == 0:
            print("✅ All tests passed!")
            print("📊 Coverage report generated:")
            print("   - HTML: htmlcov/index.html")
            print("   - XML: coverage.xml")
        else:
            print("❌ Some tests failed or coverage is below threshold.")
            print("💡 Check the output above for details")
            return False

        return True

    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def main():
    """Main function to run tests."""
    print("🧪 PDF OCR Converter API - Test Runner")
    print("=" * 50)

    # Check virtual environment
    if not check_virtual_environment():
        sys.exit(1)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Run tests
    if not run_tests():
        sys.exit(1)

    print("\n🎉 Test run completed successfully!")


if __name__ == "__main__":
    main()
