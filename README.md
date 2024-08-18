# 📋 PlayRanker Project

La herramienta definitiva para los jugadores que buscan evaluar la dificultad y calidad de los juegos en PSN. Obtén un análisis detallado de trofeos, puntuaciones y tiempo de juego para encontrar los mejores juegos que se ajusten a tus preferencias.

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
[![PlayRanker](https://github.com/rafacc87/PlayRanker/actions/workflows/python-app.yml/badge.svg)](https://github.com/rafacc87/PlayRanker/actions/workflows/python-app.yml)
![Test Coverage](https://img.shields.io/codecov/c/github/rafacc87/PlayRanker)

## 🛠️ Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/ListGame.git
   cd ListGame
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa venv\Scripts\activate
   ```
3. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

## 🔑 Cómo obtener el Token de PSN
Para usar las funciones relacionadas con PSN, necesitas un token de autenticación. Sigue estos pasos:

Ve a la [página oficial de PlayStation](https://www.playstation.com/) e inicia sesión.
Usa las herramientas de desarrollo del navegador para interceptar la solicitud que contiene tu token de autenticación (**`access_token`**).
Copia el token y añádelo a tus variables de entorno o configúralo directamente en tu código.
## 🚀 Uso
Una vez configurado todo, puedes ejecutar el proyecto con el siguiente comando:

   ```bash
   python app.py
   ```
El script obtendrá datos de varias fuentes en función del título de los videojuegos que ingreses.

## ⚙️ Librerías necesarias
Las principales librerías que necesitas son:

- requests
- beautifulsoup4
- selenium
- webdriver_manager
- pytest (para pruebas)

Consulta el archivo requirements.txt para más detalles.

## 🧪 Pruebas
Para ejecutar las pruebas unitarias, utiliza pytest:

   ```bash
   pytest
   ```
## 🏗️ Estructura del Proyecto
   ```bash
   ListGame/
   │
   ├── app.py               # Archivo principal
   ├── selenium_tools.py    # Funciones relacionadas con Selenium
   ├── utility.py           # Funciones auxiliares
   ├── tests/               # Pruebas unitarias
   ├── README.md            # Documentación
   └── requirements.txt     # Dependencias   
   ```

## 📝 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
