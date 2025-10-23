"""
IPC2 Proyecto 3 - Iniciador Automático
Estudiante: 202303204

Este script:
1. Verifica que las dependencias estén instaladas
2. Instala automáticamente lo que falta
3. Inicia backend y frontend en ventanas separadas

USO: Solo dale Play en VS Code o ejecuta: python start.py
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Colores para terminal


class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_step(message):
    """Imprime paso del proceso"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}► {message}{Colors.END}")


def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_error(message):
    """Imprime mensaje de error"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")


def print_warning(message):
    """Imprime advertencia"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def get_project_root():
    """Obtiene el directorio raíz del proyecto"""
    return Path(__file__).parent.absolute()


def get_venv_python():
    """Obtiene el ejecutable de Python del entorno virtual"""
    project_root = get_project_root()
    venv_python = project_root / ".venv" / "Scripts" / "python.exe"

    if venv_python.exists():
        return str(venv_python)

    # Si no hay venv, usar Python del sistema
    return sys.executable


def check_module_installed(module_name):
    """Verifica si un módulo está instalado"""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def install_dependencies():
    """Instala dependencias faltantes"""
    print_step("Verificando dependencias...")

    project_root = get_project_root()
    python_exe = get_venv_python()

    # Lista de módulos críticos a verificar
    critical_modules = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'django': 'Django',
    }

    missing_modules = []
    for module, package in critical_modules.items():
        if not check_module_installed(module):
            missing_modules.append(package)
            print_warning(f"Falta: {package}")

    if not missing_modules:
        print_success("Todas las dependencias están instaladas")
        return True

    # Instalar dependencias faltantes
    print_step("Instalando dependencias faltantes...")

    # Instalar backend
    backend_reqs = project_root / "backend" / "requirements.txt"
    if backend_reqs.exists():
        print(f"  → Instalando dependencias de backend...")
        try:
            result = subprocess.run(
                [python_exe, "-m", "pip", "install",
                    "-r", str(backend_reqs), "-q"],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode == 0:
                print_success("Backend dependencies instaladas")
            else:
                print_error("Error instalando backend dependencies")
                print(result.stderr)
                return False
        except Exception as e:
            print_error(f"Error: {e}")
            return False

    # Instalar frontend
    frontend_reqs = project_root / "frontend" / "requirements.txt"
    if frontend_reqs.exists():
        print(f"  → Instalando dependencias de frontend...")
        try:
            result = subprocess.run(
                [python_exe, "-m", "pip", "install",
                    "-r", str(frontend_reqs), "-q"],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode == 0:
                print_success("Frontend dependencies instaladas")
            else:
                print_error("Error instalando frontend dependencies")
                print(result.stderr)
                return False
        except Exception as e:
            print_error(f"Error: {e}")
            return False

    print_success("¡Todas las dependencias instaladas correctamente!")
    return True


def create_db_directories():
    """Crea los directorios necesarios para la base de datos"""
    project_root = get_project_root()

    dirs_to_create = [
        project_root / "backend" / "instance" / "data",
        project_root / "backend" / "instance" / "reports",
    ]

    for directory in dirs_to_create:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            print_success(
                f"Directorio creado: {directory.relative_to(project_root)}")


def start_servers():
    """Inicia backend y frontend en ventanas separadas"""
    print_step("Iniciando servidores...")

    project_root = get_project_root()
    python_exe = get_venv_python()

    # Crear directorios necesarios
    create_db_directories()

    # Iniciar backend
    backend_dir = project_root / "backend"
    backend_cmd = f'start "🔧 Backend - Flask (Puerto 5001)" cmd /k "cd /d {backend_dir} && {python_exe} app.py"'

    print(f"  → Iniciando Backend en http://127.0.0.1:5001")
    os.system(backend_cmd)
    time.sleep(2)

    # Iniciar frontend
    frontend_dir = project_root / "frontend"
    frontend_cmd = f'start "🌐 Frontend - Django (Puerto 8000)" cmd /k "cd /d {frontend_dir} && {python_exe} manage.py runserver"'

    print(f"  → Iniciando Frontend en http://127.0.0.1:8000")
    os.system(frontend_cmd)
    time.sleep(1)

    print_success("¡Servidores iniciados correctamente!")

    return True


def main():
    """Función principal"""
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}  IPC2 Proyecto 3 - Sistema de Facturación Cloud{Colors.END}")
    print(f"{Colors.BOLD}  Estudiante: 202303204{Colors.END}")
    print(f"{Colors.BOLD}{'='*70}{Colors.END}")

    try:
        # Paso 1: Instalar dependencias
        if not install_dependencies():
            print_error("\n❌ Error al instalar dependencias")
            print_warning(
                "Intentá ejecutar manualmente: python run.py install")
            input("\nPresioná Enter para salir...")
            sys.exit(1)

        # Paso 2: Iniciar servidores
        if not start_servers():
            print_error("\n❌ Error al iniciar servidores")
            input("\nPresioná Enter para salir...")
            sys.exit(1)

        # Mensaje final
        print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*70}{Colors.END}")
        print(
            f"{Colors.GREEN}{Colors.BOLD}  ✓ ¡APLICACIÓN INICIADA CORRECTAMENTE!{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}{'='*70}{Colors.END}\n")

        print(f"{Colors.BOLD}📍 URLs Disponibles:{Colors.END}")
        print(f"   {Colors.BLUE}Backend API:{Colors.END}  http://127.0.0.1:5001")
        print(f"   {Colors.BLUE}Frontend Web:{Colors.END} http://127.0.0.1:8000")

        print(f"\n{Colors.BOLD}💡 Instrucciones:{Colors.END}")
        print(f"   1. Abrí tu navegador")
        print(f"   2. Andá a: {Colors.BLUE}http://127.0.0.1:8000{Colors.END}")
        print(f"   3. Empezá a usar el sistema de facturación")

        print(f"\n{Colors.BOLD}🛑 Para detener:{Colors.END}")
        print(f"   Cerrá las 2 ventanas CMD que se abrieron")

        print(f"\n{Colors.YELLOW}{'─'*70}{Colors.END}")
        print(
            f"{Colors.YELLOW}Las ventanas de los servidores se abrieron por separado{Colors.END}")
        print(f"{Colors.YELLOW}Podés minimizar esta ventana{Colors.END}")
        print(f"{Colors.YELLOW}{'─'*70}{Colors.END}\n")

        input("Presioná Enter para cerrar este mensaje...")

    except KeyboardInterrupt:
        print(
            f"\n\n{Colors.YELLOW}⚠ Proceso cancelado por el usuario{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"\n❌ Error inesperado: {e}")
        input("\nPresioná Enter para salir...")
        sys.exit(1)


if __name__ == "__main__":
    main()
