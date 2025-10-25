# GitDown: El Descargador de Repositorios de GitHub Moderno

**GitDown** es una herramienta de descarga de repositorios de GitHub que ha sido completamente revitalizada. Ahora ofrece una **Interfaz Gráfica de Usuario (GUI)** intuitiva con un diseño inspirado en **Windows 11** y una **Interfaz de Línea de Comandos (CLI)** mejorada con un estilo visual característico, gracias a la librería `rich`.

## 🚀 Características Principales

*   **GUI Moderna:** Interfaz desarrollada con **PyQt5** que simula el estilo de diseño de **GitHub** y la estética de **Windows 11**, ofreciendo una experiencia de usuario limpia y accesible.
*   **CLI Característica:** Versión de terminal mejorada con colores, barras de progreso dinámicas y mensajes detallados, ideal para usuarios avanzados y scripts automatizados.
*   **Descarga Eficiente:** Descarga directa de repositorios como archivos ZIP, con detección automática de ramas (`main` o `master`).
*   **Gestión de Dependencias:** Detección y sugerencia de instalación de `requirements.txt` dentro del repositorio descargado.

## 💻 Instalación

GitDown requiere Python 3.x y las siguientes librerías:

```bash
# Requisitos generales
pip install requests

# Para la Interfaz Gráfica de Usuario (GUI)
pip install PyQt5

# Para la Interfaz de Línea de Comandos (CLI) mejorada
pip install rich
```

## 🌐 Uso de la Interfaz Gráfica (GUI)

La GUI es la forma más sencilla de usar GitDown.

1.  Ejecute el archivo principal de la GUI:
    ```bash
    python gitdown_gui.py
    ```
2.  Ingrese el **Usuario/Organización** de GitHub y el **Nombre del Repositorio**.
3.  Haga clic en **"Descargar Repositorio"**.
4.  El progreso se mostrará en la barra y los archivos se guardarán en su carpeta de Descargas (`~/Descargas` o `%USERPROFILE%\Downloads`).

## ⚙️ Uso de la Interfaz de Línea de Comandos (CLI)

La CLI ofrece una experiencia visualmente rica y es ideal para automatización.

1.  Ejecute la CLI con los argumentos necesarios:
    ```bash
    python gitdown_cli.py --user <usuario-github> --repo <nombre-repositorio>
    ```

**Ejemplo:**

```bash
python gitdown_cli.py --user JesusQuijada34 --repo gitdown
```

La CLI le proporcionará una salida detallada, incluyendo la verificación de ramas, la barra de progreso de descarga y la detección de dependencias.

## 📦 Estructura del Proyecto

```
gitdown/
├── gitdown.py          # Versión original (v1) de la CLI
├── gitdown_gui.py      # Nueva Interfaz Gráfica (GUI) con PyQt5
├── gitdown_cli.py      # Nueva Interfaz de Línea de Comandos (CLI) mejorada con rich
├── README.md           # Este archivo
├── CHANGELOG.md        # Historial de cambios
└── ...                 # Otros archivos y carpetas del repositorio original
```

---

## 👤 Autor

**JesusQuijada34** (Repositorio original)

**Mejoras y Refactorización por Manus AI**

