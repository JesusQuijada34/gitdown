import argparse
import os
import sys
import zipfile
import shutil
import requests
import platform
import subprocess
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn

# Initialize rich console
console = Console()

def get_downloads_dir():
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Downloads")
    else:
        # Use 'Descargas' for Spanish-speaking systems, fallback to 'Downloads'
        return os.path.join(os.environ.get("HOME", os.path.expanduser("~")), "Descargas")

def download_repo_zip(user, repo):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        check_task = progress.add_task("[bold blue]Verificando ramas (main/master)...[/bold blue]", total=2)
        
        for branch in ["main", "master"]:
            url = f"https://github.com/{user}/{repo}/archive/refs/heads/{branch}.zip"
            progress.update(check_task, description=f"[bold blue]Intentando rama: {branch}[/bold blue]", advance=1)
            
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                
                total_size = int(response.headers.get('content-length', 0))
                
                console.print(f"[bold green][SERVER][/bold green] [green]OK[/green] en: [yellow]github/{user}/{repo}/{branch}.zip[/yellow]")
                
                zip_path = os.path.join(os.getcwd(), f"{repo}_{branch}.zip")
                
                download_task = progress.add_task(f"[bold magenta]Descargando {branch}.zip[/bold magenta]", total=total_size, visible=True)
                
                with open(zip_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        progress.update(download_task, advance=len(chunk))
                        
                progress.update(download_task, description=f"[bold green]Descarga de {branch}.zip completada![/bold green]", completed=total_size)
                return zip_path, branch
            
            except requests.exceptions.HTTPError:
                console.print(f"[bold red][SERVER][/bold red] [red]Fallo[/red] al obtener la rama [yellow]{branch}[/yellow].")
                continue
            except Exception as e:
                console.print(f"[bold red][ERROR][/bold red] Ocurrió un error: {e}")
                sys.exit(1)

        console.print("[bold red][SERVER][/bold red] [red]No se encontró una rama válida (main/master)[/red]")
        sys.exit(1)

def extract_zip(zip_path, user, repo):
    dest_dir = os.path.join(get_downloads_dir(), "GitDown", f"{user}--{repo}")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        extract_task = progress.add_task("[bold yellow]Extrayendo archivos...[/bold yellow]", total=100)
        
        os.makedirs(dest_dir, exist_ok=True)
        
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                # Estimate total files for a more realistic progress bar
                file_list = zip_ref.namelist()
                total_files = len(file_list)
                
                for i, member in enumerate(file_list):
                    zip_ref.extract(member, dest_dir)
                    progress.update(extract_task, advance=(100/total_files))
                    
            os.remove(zip_path)
            progress.update(extract_task, completed=100, description="[bold green]Extracción completada![/bold green]")
            
            console.print(f"[bold green][SWIPPER][/bold green] Descomprimido y eliminado | Archivos listos en → [cyan]{dest_dir}[/cyan]")
            return dest_dir
        
        except Exception as e:
            console.print(f"[bold red][ERROR][/bold red] Error durante la extracción: {e}")
            sys.exit(1)

def install_requirements(dest_dir):
    req_found = False
    for root, _, files in os.walk(dest_dir):
        if "requirements.txt" in files:
            req_path = os.path.join(root, "requirements.txt")
            req_found = True
            console.print(f"[bold yellow][GARDENHOUSE][/bold yellow] [yellow]Dependencias detectadas en:[/yellow] [magenta]{req_path}[/magenta]")
            
            console.print("[bold blue]Instalando dependencias...[/bold blue]")
            try:
                # Use a separate shell session to run pip for better output handling
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", req_path],
                    capture_output=True, text=True, check=True
                )
                console.print(f"[bold green]Instalación completada.[/bold green]")
                # Optionally print pip output for debugging/transparency
                # console.print(result.stdout, style="dim")
                return True
            except subprocess.CalledProcessError as e:
                console.print(f"[bold red][ERROR][/bold red] Fallo al instalar dependencias.")
                console.print(f"[red]Salida de error:[/red]\n{e.stderr}", style="red")
                return False
            except FileNotFoundError:
                console.print("[bold red][ERROR][/bold red] Comando 'pip' no encontrado. Asegúrese de que Python y pip estén configurados correctamente.")
                return False
            
    if not req_found:
        console.print("[bold blue][GARDENHOUSE][/bold blue] [blue]No se encontraron dependencias para instalar.[/blue]")
        return False

def run_sensors(dest_dir):
    py_found = False
    for root, _, files in os.walk(dest_dir):
        for f in files:
            if f.endswith(".py"):
                py_found = True
                break
        if py_found:
            break
            
    if py_found:
        console.print("[bold green][SENSOR][/bold green] [green]¡Entorno PYTHON detectado![/green]")
    else:
        console.print("[bold yellow][SENSOR][/bold yellow] [yellow]No es un entorno PYTHON (o no se encontraron archivos .py).[/yellow]")

def main():
    parser = argparse.ArgumentParser(
        description="""
        GitDown CLI: Descargador de Repositorios de GitHub con estilo.
        Uso: python gitdown_cli.py --user <usuario> --repo <repositorio>
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--user", required=True, help="Usuario o Organización de GitHub (Ej: JesusQuijada34)")
    parser.add_argument("--repo", required=True, help="Nombre del Repositorio (Ej: gitdown)")
    args = parser.parse_args()

    console.rule("[bold white on blue] GITDOWN CLI v2.0 [/bold white on blue]")
    console.print(f"[bold yellow]Iniciando descarga para:[/bold yellow] [cyan]{args.user}/{args.repo}[/cyan]\n")

    try:
        zip_path, branch = download_repo_zip(args.user, args.repo)
        dest_dir = extract_zip(zip_path, args.user, args.repo)
        run_sensors(dest_dir)
        install_requirements(dest_dir)
        
        console.rule("[bold white on green] ¡DESCARGA COMPLETA! [/bold white on green]")
        console.print(f"[bold white on green]Ruta de destino:[/bold white on green] [cyan]{dest_dir}[/cyan]")
        console.print("[bold green]Gracias por usar GitDown CLI.[/bold green]")

    except Exception as e:
        console.print(f"\n[bold white on red] ERROR FATAL [/bold white on red]")
        console.print(f"[red]Ocurrió un error inesperado: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()

