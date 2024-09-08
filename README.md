# 📋 PlayRanker Project

La herramienta definitiva para los jugadores que buscan evaluar la dificultad y calidad de los juegos en PSN. Obtén un análisis detallado de trofeos, puntuaciones y tiempo de juego para encontrar los mejores juegos que se ajusten a tus preferencias.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
[![PlayRanker](https://github.com/rafacc87/PlayRanker/actions/workflows/python-app.yml/badge.svg)](https://github.com/rafacc87/PlayRanker/actions/workflows/python-app.yml)

## 🚀 Última Versión
¡No necesitas instalar Python para ejecutar PlayRanker! Puedes descargar la última release con el ejecutable listo para usar desde GitHub Releases:

[![Descargar Última Release](https://img.shields.io/github/v/release/rafacc87/PlayRanker)](https://github.com/rafacc87/PlayRanker/releases/latest)

## 🛠️ Instalación Manual

Si prefieres clonar y ejecutar el proyecto con Python, sigue estos pasos:

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

1. Inicia sesión en tu cuenta [My PlayStation](https://www.playstation.com/).

2. En otra pestaña, vaya a [https://ca.account.sony.com/api/v1/ssocookie](https://ca.account.sony.com/api/v1/ssocookie).

3. Si ha iniciado sesión, debería ver un texto similar a este
   ```json
   {"npsso":"<64 character npsso code>"}
   ```
4. Copia este código npsso, que te servirá para obtener y actualizar el token de autenticación.
## 🚀 Uso

### Configuración para PSN

Para obtener datos desde PSN, asegúrate de tener configurado el token `npsso` en el archivo `config.yml`. Aquí te mostramos cómo hacerlo:

1. **Obtén tu token `npsso`** siguiendo los pasos de la sección [Cómo obtener el Token de PSN](#🔑-cómo-obtener-el-token-de-psn).
   
2. **Configura tu token en el archivo `config.yml`:**

   ```yaml
   PSN:
     active: False  # Cambia a True para activar la funcionalidad de PSN
     token: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Tu token de autenticación para PSN.
     platforms: [PS5, PS4, PS3, PSVITA]  # Lista de plataformas de las que te interesan los datos.
     game_time: True  # Registrar el tiempo de juego.
     platinium_time: True  # Registrar el tiempo necesario para obtener el platino.
     export: xls  # Formato de exportación: csv o xls.
   ```
3. Una vez configurado todo, puedes ejecutar el proyecto con el siguiente comando:
   ```bash
   python app.py
   ```
El script obtendrá datos de varias fuentes en función del título de los videojuegos que ingreses, exportándolos a un archivo xls o csv según lo configures.

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
## 🚀 Desarrollos Completados

- **Obtención de Datos desde un Documento:**
   - Se ha implementado la funcionalidad para obtener datos de los videojuegos desde un archivo de tipo `CSV` o `Excel`. Los usuarios pueden configurar el archivo desde el cual se extraerán los datos en el archivo de configuración `config.yml`.
   - Los formatos de archivo soportados incluyen `CSV` y `Excel` (`xls` o `xlsx`), y se valida que el archivo y las columnas especificadas existan antes de procesarlos.
   - Configuración en `config.yml`:
     ```yaml
     document:
       active: True  # Activa la funcionalidad
       name: documents/list_games.xlsx  # Ruta del archivo
       column_name: title  # Columna con los títulos de los juegos
       game_time: True  # Registro del tiempo de juego
       platinium_time: True  # Registro del tiempo necesario para obtener el platino
     ```

## 🔮 Futuros Desarrollos

- **Automatización del Proceso de Tokenización**: Automatizar el proceso de obtención y renovación del token npsso, de manera que la autenticación con PSN sea más fluida y requiera menos intervención manual por parte del usuario.

- **Interfaz Gráfica de Usuario (GUI) (en progreso):** Desarrollar una interfaz gráfica que facilite la interacción con la aplicación, permitiendo a los usuarios gestionar sus listas de juegos y generar informes de manera más intuitiva.

- **Integración con APIs Adicionales:** Incorporar datos de otras fuentes o servicios API que ofrezcan más detalles sobre los juegos, como estadísticas de logros, tendencias de popularidad o análisis de usuarios.

- **Sistema de Recomendaciones:** Basado en los datos recopilados, crear un sistema que sugiera juegos similares a los que el usuario ya ha disfrutado, optimizando la búsqueda de nuevos títulos.

- **Soporte Multiplataforma:** Ampliar el soporte de la herramienta para incluir juegos de otras plataformas, como Xbox, Steam o Nintendo Switch, permitiendo una comparación cruzada entre plataformas.

- **Exportación a Formatos Adicionales:** Permitir la exportación de datos en otros formatos populares como PDF o Google Sheets, facilitando su acceso y distribución.

## 🙏 Agradecimientos

Este proyecto nació gracias a la inspiración obtenida del video [Por qué NUNCA TERMINAS tus JUEGOS](https://www.youtube.com/watch?v=yCWmnEHR1CI) de [Betto](https://www.youtube.com/@SrtoBetto). Su contenido fue fundamental para el desarrollo de este proyecto. Gracias a este contenido, pude llevar a cabo esta automatización.

Este proyecto no solo está inspirado por la pasión por los videojuegos y la programación, sino también por las personas que han sido parte de mi vida, quienes, con su apoyo, compañía y amistad, han dejado una huella profunda en mi corazón.

Quiero dedicar un espacio especial a la memoria de mi amigo **Toni**, que tristemente nos dejó. Siempre recordaré cuando lo ayudamos a subir azulejos y rodapié hasta su nuevo piso, sin ascensor, para luego terminar compartiendo una comida en el suelo. También cuando vino a mi casa para ayudarme a instalar un ventilador de techo, un gesto generoso y típico de él. Toni era el mejor, y su ausencia deja un vacío enorme. Este proyecto también es para ti.

## 🏗️ Estructura del Proyecto
   ```bash
      PlayRanker/
   │
   ├── app.py               # Archivo principal de la aplicación
   ├── config.yml           # Archivo de configuración del proyecto
   ├── core/
   │   └── document.py      # Funciones para procesar documentos
   ├── utils/
   │   ├── selenium_tools.py  # Funciones relacionadas con Selenium
   │   ├── utility.py         # Funciones auxiliares
   │   └── web.py             # Funciones relacionadas con el scraping
   ├── documents/           # Carpeta donde se almacenan los archivos del usuario
   ├── tests/               # Pruebas unitarias
   │   ├── test_selenium_tools.py
   │   ├── test_utility.py
   ├── README.md            # Documentación
   ├── requirements.txt     # Dependencias
   ```

## 📝 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
