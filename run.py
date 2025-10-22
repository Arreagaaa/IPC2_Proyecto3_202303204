import sys
import os
import subprocess
import time
from pathlib import Path

# Colors for terminal output (Windows compatible)


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(message):
    """Print a styled header message"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_success(message):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_error(message):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_info(message):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def print_warning(message):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent.absolute()


def get_venv_python():
    """Get the virtual environment Python executable"""
    project_root = get_project_root()
    venv_python = project_root / ".venv" / "Scripts" / "python.exe"

    if not venv_python.exists():
        print_warning("Virtual environment not found at .venv")
        print_info("Using system Python instead")
        return sys.executable

    return str(venv_python)


def check_dependencies():
    """Check if required dependencies are installed"""
    project_root = get_project_root()
    backend_reqs = project_root / "backend" / "requirements.txt"
    frontend_reqs = project_root / "frontend" / "requirements.txt"

    if not backend_reqs.exists() or not frontend_reqs.exists():
        print_error("requirements.txt files not found")
        return False

    print_success("Dependency files found")
    return True


def start_backend():
    """Start Flask backend server"""
    print_header("Starting Backend (Flask)")

    project_root = get_project_root()
    backend_dir = project_root / "backend"

    if not backend_dir.exists():
        print_error(f"Backend directory not found: {backend_dir}")
        return False

    os.chdir(backend_dir)
    python_exe = get_venv_python()

    print_info(f"Working directory: {backend_dir}")
    print_info(f"Python executable: {python_exe}")
    print_info("Starting Flask on http://127.0.0.1:5001")
    print_warning("Press Ctrl+C to stop the server")
    print()

    try:
        subprocess.run([python_exe, "app.py"], check=True)
    except KeyboardInterrupt:
        print()
        print_info("Backend server stopped")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to start backend: {e}")
        return False
    except FileNotFoundError:
        print_error("Python executable not found")
        print_info("Try: python run.py install")
        return False

    return True


def start_frontend():
    """Start Django frontend server"""
    print_header("Starting Frontend (Django)")

    project_root = get_project_root()
    frontend_dir = project_root / "frontend"

    if not frontend_dir.exists():
        print_error(f"Frontend directory not found: {frontend_dir}")
        return False

    os.chdir(frontend_dir)
    python_exe = get_venv_python()

    print_info(f"Working directory: {frontend_dir}")
    print_info(f"Python executable: {python_exe}")
    print_info("Starting Django on http://127.0.0.1:8000")
    print_warning("Press Ctrl+C to stop the server")
    print()

    try:
        subprocess.run([python_exe, "manage.py", "runserver"], check=True)
    except KeyboardInterrupt:
        print()
        print_info("Frontend server stopped")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to start frontend: {e}")
        return False
    except FileNotFoundError:
        print_error("Python executable not found")
        print_info("Try: python run.py install")
        return False

    return True


def start_all():
    """Start both backend and frontend servers"""
    print_header("Starting Full Application")

    print_info("This will open TWO terminal windows:")
    print_info("  1. Backend (Flask) on port 5001")
    print_info("  2. Frontend (Django) on port 8000")
    print()
    print_warning("Close the terminal windows to stop the servers")
    print()

    project_root = get_project_root()
    python_exe = get_venv_python()

    # Start backend in new window
    backend_cmd = f'start "Backend - Flask (5001)" cmd /k "{python_exe}" "{project_root}/backend/app.py"'
    print_info("Starting backend...")
    os.system(backend_cmd)
    time.sleep(2)  # Wait a bit for backend to start

    # Start frontend in new window
    frontend_cmd = f'start "Frontend - Django (8000)" cmd /k "cd /d {project_root}/frontend && {python_exe} manage.py runserver"'
    print_info("Starting frontend...")
    os.system(frontend_cmd)
    time.sleep(1)

    print()
    print_success("Both servers started successfully!")
    print()
    print_info("Backend running at: http://127.0.0.1:5001")
    print_info("Frontend running at: http://127.0.0.1:8000")
    print()
    print_warning("Close the terminal windows to stop the servers")

    return True


def run_tests():
    """Run project tests"""
    print_header("Running Tests")

    project_root = get_project_root()
    test_file = project_root / "test_backend_complete.py"

    if not test_file.exists():
        print_error(f"Test file not found: {test_file}")
        return False

    python_exe = get_venv_python()

    print_info(f"Test file: {test_file}")
    print_info(f"Python executable: {python_exe}")
    print()

    try:
        result = subprocess.run([python_exe, str(test_file)], check=False)
        if result.returncode == 0:
            print()
            print_success("All tests passed!")
            return True
        else:
            print()
            print_warning("Some tests failed - check output above")
            return False
    except FileNotFoundError:
        print_error("Python executable not found")
        return False
    except Exception as e:
        print_error(f"Failed to run tests: {e}")
        return False


def clean_project():
    """Clean temporary files and caches"""
    print_header("Cleaning Project")

    project_root = get_project_root()

    # Patterns to clean
    patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        "**/.pytest_cache",
        "**/.coverage",
        "**/htmlcov",
        "**/*.log",
    ]

    cleaned_count = 0

    for pattern in patterns:
        for path in project_root.glob(pattern):
            try:
                if path.is_file():
                    path.unlink()
                    cleaned_count += 1
                elif path.is_dir():
                    import shutil
                    shutil.rmtree(path)
                    cleaned_count += 1
                print_info(f"Removed: {path.relative_to(project_root)}")
            except Exception as e:
                print_warning(f"Could not remove {path}: {e}")

    print()
    if cleaned_count > 0:
        print_success(f"Cleaned {cleaned_count} items")
    else:
        print_info("Nothing to clean")

    return True


def install_dependencies():
    """Install project dependencies"""
    print_header("Installing Dependencies")

    project_root = get_project_root()
    python_exe = get_venv_python()

    # Install backend dependencies
    print_info("Installing backend dependencies...")
    backend_dir = project_root / "backend"
    os.chdir(backend_dir)

    try:
        subprocess.run([python_exe, "-m", "pip", "install",
                       "-r", "requirements.txt"], check=True)
        print_success("Backend dependencies installed")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install backend dependencies: {e}")
        return False

    print()

    # Install frontend dependencies
    print_info("Installing frontend dependencies...")
    frontend_dir = project_root / "frontend"
    os.chdir(frontend_dir)

    try:
        subprocess.run([python_exe, "-m", "pip", "install",
                       "-r", "requirements.txt"], check=True)
        print_success("Frontend dependencies installed")
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install frontend dependencies: {e}")
        return False

    os.chdir(project_root)
    print()
    print_success("All dependencies installed successfully!")

    return True


def show_help():
    """Show help message"""
    print_header("IPC2 Proyecto 3 - Sistema de Facturación")

    print(f"{Colors.BOLD}Comandos disponibles:{Colors.ENDC}\n")

    commands = [
        ("start", "Inicia backend y frontend en ventanas separadas"),
        ("backend", "Inicia solo el backend (Flask en puerto 5001)"),
        ("frontend", "Inicia solo el frontend (Django en puerto 8000)"),
        ("test", "Ejecuta las pruebas del proyecto"),
        ("clean", "Limpia archivos temporales y cache"),
        ("install", "Instala todas las dependencias"),
        ("help", "Muestra esta ayuda"),
    ]

    for cmd, desc in commands:
        print(f"  {Colors.OKGREEN}{cmd:12}{Colors.ENDC} - {desc}")

    print(f"\n{Colors.BOLD}Ejemplos:{Colors.ENDC}")
    print(f"  {Colors.OKCYAN}python run.py start{Colors.ENDC}     - Iniciar aplicación completa")
    print(f"  {Colors.OKCYAN}python run.py backend{Colors.ENDC}   - Solo backend para desarrollo")
    print(f"  {Colors.OKCYAN}python run.py test{Colors.ENDC}      - Ejecutar pruebas")

    print(f"\n{Colors.BOLD}URLs:{Colors.ENDC}")
    print(f"  Backend:  {Colors.OKBLUE}http://127.0.0.1:5001{Colors.ENDC}")
    print(f"  Frontend: {Colors.OKBLUE}http://127.0.0.1:8000{Colors.ENDC}")

    print(f"\n{Colors.BOLD}Estudiante:{Colors.ENDC} 202303204")
    print(f"{Colors.BOLD}Curso:{Colors.ENDC} IPC2 - USAC")
    print()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    command = sys.argv[1].lower()

    commands = {
        'start': start_all,
        'backend': start_backend,
        'frontend': start_frontend,
        'test': run_tests,
        'clean': clean_project,
        'install': install_dependencies,
        'help': show_help,
    }

    if command not in commands:
        print_error(f"Unknown command: {command}")
        print_info("Run 'python run.py help' for available commands")
        sys.exit(1)

    # Execute command
    success = commands[command]()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
