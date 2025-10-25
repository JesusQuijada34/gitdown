# GitDown: El Descargador de Repositorios de GitHub Moderno

**GitDown** es una herramienta de descarga de repositorios de GitHub que ha sido completamente revitalizada, ofreciendo una **Interfaz Gráfica de Usuario (GUI)** intuitiva con un diseño inspirado en **Windows 11**.

## 🚀 Características Principales

*   **GUI Moderna:** Interfaz principal desarrollada con **PyQt5** que simula el estilo de diseño de **GitHub** y la estética de **Windows 11**, ofreciendo una experiencia de usuario limpia y accesible.
*   **Descarga Eficiente:** Descarga directa de repositorios como archivos ZIP, con detección automática de ramas (`main` o `master`).
*   **Gestión de Dependencias:** Detección y sugerencia de instalación de `requirements.txt` dentro del repositorio descargado.
*   **CLI Opcional:** La versión de terminal mejorada (`gitdown-term.py`) sigue disponible para usuarios avanzados y automatización.

## 💻 Instalación

GitDown requiere Python 3.x y las siguientes librerías:

```bash
# Requisitos generales
pip install requests

# Requisito principal para la GUI (gitdown.py)
pip install PyQt5

# Requisito opcional para la CLI mejorada (gitdown-term.py)
pip install rich
```

## 🌐 Uso Principal (GUI)

El archivo principal del proyecto, `gitdown.py`, ahora ejecuta la Interfaz Gráfica de Usuario.

1.  Ejecute la aplicación:
    ```bash
    python gitdown.py
    ```
2.  Ingrese el **Usuario/Organización** de GitHub y el **Nombre del Repositorio**.
3.  Haga clic en **"Descargar Repositorio"**.
4.  Los archivos se guardarán en su carpeta de Descargas (`~/Descargas` o `%USERPROFILE%\Downloads`).

## ⚙️ Uso de la CLI Mejorada (Opcional)

Si prefiere la línea de comandos, puede usar la versión mejorada con `rich`:

```bash
python gitdown-term.py --user <usuario-github> --repo <nombre-repositorio>
```

## 📦 Estructura del Proyecto

```
gitdown/
├── gitdown.py              # -> NUEVA GUI (Punto de entrada principal)
├── gitdown-term.py         # -> CLI Mejorada (Terminal)

├── README.md               # Este archivo
├── CHANGELOG.md            # Historial de cambios
└── ...                     # Otros archivos y carpetas
```

---

## 👤 Autor

**JesusQuijada34** (Repositorio original)

**Mejoras y Refactorización por Manus AI**

