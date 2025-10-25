# CHANGELOG

Todas las mejoras y cambios notables a **GitDown** serán documentados en este archivo.

## [2.0.0] - 2025-10-25

Esta es una actualización mayor que introduce una interfaz gráfica y una versión de terminal completamente renovada.

### ✨ Nuevas Características

-   **Interfaz Gráfica de Usuario (GUI):**
    -   Se introdujo `gitdown_gui.py`, una aplicación de escritorio completa construida con **PyQt5**.
    -   Diseño de la interfaz inspirado en la estética de **GitHub** y el sistema operativo **Windows 11** para una experiencia moderna.
    -   Permite la descarga de repositorios mediante campos de entrada simples y un botón de acción.
    -   Incluye una barra de progreso visual y mensajes de estado en tiempo real.
-   **Interfaz de Línea de Comandos (CLI) Mejorada:**
    -   Se creó `gitdown_cli.py`, una versión de terminal más robusta y visualmente atractiva.
    -   Implementación de la librería `rich` para una salida de consola característica, incluyendo:
        -   Barras de progreso animadas y detalladas.
        -   Colores y formato mejorados para una mejor legibilidad.
        -   Reglas y encabezados estilizados.

### 🛠️ Mejoras

-   **Refactorización del Código:** Se separó la lógica de la aplicación en tres archivos distintos (`gitdown.py`, `gitdown_gui.py`, `gitdown_cli.py`) para una mejor modularidad y mantenimiento.
-   **Documentación:**
    -   Se actualizó completamente el `README.md` para incluir la documentación de la GUI y la nueva CLI.
    -   Se agregó este `CHANGELOG.md` para rastrear las versiones.

### 🐛 Correcciones de Errores

-   Se mejoró la gestión de errores en la nueva CLI para proporcionar mensajes más claros al usuario en caso de fallos de red o de repositorio.

