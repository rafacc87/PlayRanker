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
Debes obtener el código de 64 caracteres de npsso. Debe seguir los siguientes pasos:

Inicia sesión en tu cuenta [My PlayStation](https://www.playstation.com/).

En otra pestaña, vaya a [https://ca.account.sony.com/api/v1/ssocookie](https://ca.account.sony.com/api/v1/ssocookie).

Si ha iniciado sesión, debería ver un texto similar a este

```json
{"npsso":"<64 character npsso code>"}
```
Este código npsso se utilizará en la API para fines de autenticación. El token de actualización que se genera a partir de npsso dura aproximadamente 2 meses. Después de eso, debe obtener un nuevo token npsso. El bot imprimirá una advertencia si quedan menos de 3 días para que caduque el token de actualización.
## 🚀 Uso
Una vez configurado todo, puedes ejecutar el proyecto con el siguiente comando:

   ```bash
   python app.py
   ```
El script obtendrá datos de varias fuentes en función del título de los videojuegos que ingreses exportandolo a un xls o csv dependiendo de como lo configures.

## ⚙️ Librerías necesarias
Las principales librerías que necesitas son:

- [psnawp](https://pypi.org/project/PSNAWP/)
- requests
- beautifulsoup4
- selenium
- webdriver_manager
- panda
- pytest (para pruebas)

Consulta el archivo requirements.txt para más detalles.

## 🧪 Pruebas
Para ejecutar las pruebas unitarias, utiliza pytest:

   ```bash
   pytest
   ```
## 🙏 Agradecimientos

Este proyecto nació gracias a la inspiración obtenida del video [Por qué NUNCA TERMINAS tus JUEGOS](https://www.youtube.com/watch?v=yCWmnEHR1CI) de [Betto](https://www.youtube.com/@SrtoBetto). Su contenido fue fundamental para el desarrollo de este proyecto. Gracias a este contenido, pude llevar a cabo esta automatización.

## 🏗️ Estructura del Proyecto
   ```bash
      PlayRanker/
   │
   ├── app.py               # Archivo principal
   ├── selenium_tools.py    # Funciones relacionadas con Selenium
   ├── utility.py           # Funciones auxiliares
   ├── web.py               # Funciones relacionadas con el scraping
   ├── tests/               # Pruebas unitarias
   ├── README.md            # Documentación
   └── requirements.txt     # Dependencias
   ```

## 📝 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
