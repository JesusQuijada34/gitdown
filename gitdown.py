#usr/bin/env/python
# Influent GardenHOuse Gits Downloader v1 TERMINAL BASH
# Autor: influent

print('GardenHouse Gits Downloader')

import argparse, os, sys, zipfile, shutil, requests, platform, subprocess, time

# Colores personalizados (ANSI)
def c(text, color):  # color: "green", "yellow", "red", "blue"
    codes = {"green": "\033[92m", "yellow": "\033[93m", "red": "\033[91m", "blue": "\033[96m", "reset": "\033[0m"}
    return f"{codes.get(color, codes['reset'])}{text}{codes['reset']}"

def get_downloads_dir():
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.environ["USERPROFILE"], "Downloads")
    else:
        return os.path.join(os.environ["HOME"], "Descargas")

def fancy_bar(duration=2.5):
    stages = ['-']
    for i in range(30):
        bar = stages[0] * (i % 10 + 1)
        sys.stdout.write(f"\r{c('[GARDENHOUSE] Revisando repositorio...', 'blue')} {bar}")
        sys.stdout.flush()
        time.sleep(duration / 30)
    print()

def download_repo_zip(user, repo):
    for branch in ["main", "master"]:
        url = f"https://github.com/{user}/{repo}/archive/refs/heads/{branch}.zip"
        response = requests.get(url)
        if response.status_code == 200:
            print(c(f"[SERVER] OK in: github/{user}/{repo}/{branch}.zip | url: {url}", "green"))
            zip_path = os.path.join(os.getcwd(), f"{repo}.zip")
            fancy_bar()
            with open(zip_path, "wb") as f:
                f.write(response.content)
            print(c(f"[SWIPPER] ZIP descargado desde la rama {branch}", "green"))
            return zip_path
    print(c("[SERVER] No se encontró una rama válida (main/master)", "red"))
    sys.exit(1)

def extract_zip(zip_path, user, repo):
    dest_dir = os.path.join(get_downloads_dir(), "GardenHouse Gits Downloader", f"{user}--{repo}")
    os.makedirs(dest_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(dest_dir)
    os.remove(zip_path)
    print(c(f"[SWIPPER] Descomprimido y eliminado | Archivos listos en → {dest_dir}", "green"))
    return dest_dir

def install_requirements(dest_dir):
    for root, _, files in os.walk(dest_dir):
        if "requirements.txt" in files:
            req_path = os.path.join(root, "requirements.txt")
            print(c(f"[GARDENHOUSE] Se han detectado dependencias en: {req_path}", "yellow"))
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_path])
            return True
    print(c("[GARDENHOUSE] No se encontraron dependencias para instalar", "blue"))
    return False

def run_sensors(dest_dir):
    py_found = False
    for root, _, files in os.walk(dest_dir):
        for f in files:
            if f.endswith(".py"):
                py_found = True
    print(c("[GARDENHOUSE] Entorno PYTHON detectado!" if py_found else "[GARDENHOUSE] No es un entorno PYTHON", "yellow" if py_found else "blue"))

def main():
    parser = argparse.ArgumentParser(description="GitHub Downloader Terminal Help Usage")
    parser.add_argument("--gitdown", required=True, help="Usuario GitHub")
    parser.add_argument("--repo", required=True, help="Nombre del repositorio")
    args = parser.parse_args()

    print(c(f"[SERVER] CHECK github/{args.gitdown}/{args.repo}", "blue"))
    zip_path = download_repo_zip(args.gitdown, args.repo)
    dest_dir = extract_zip(zip_path, args.gitdown, args.repo)
    run_sensors(dest_dir)
    install_requirements(dest_dir)
    print(c("[SWIPPER] ¡DESCARGADO!", "green"))

if __name__ == "__main__":
    main()

