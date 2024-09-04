# 📋 PlayRanker Project

La herramienta definitiva para los jugadores que buscan evaluar la dificultad y calidad de los juegos en PSN. Obtén un análisis detallado de trofeos, puntuaciones y tiempo de juego para encontrar los mejores juegos que se ajusten a tus preferencias.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
[![PlayRanker](https://github.com/rafacc87/PlayRanker/actions/workflows/python-app.yml/badge.svg)](https://github.com/rafacc87/PlayRanker/actions/workflows/python-app.yml)

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
## 🚀 Desarrollos Completados

1. **Obtención de Datos desde un Documento:**
   - Se ha implementado la funcionalidad para obtener datos de los videojuegos desde un archivo de tipo `CSV` o `Excel`. Los usuarios pueden configurar el archivo desde el cual se extraerán los datos en el archivo de configuración `config.yml`.
   - Los formatos de archivo soportados incluyen `CSV` y `Excel` (`xls` o `xlsx`), y se valida que el archivo y las columnas especificadas existan antes de procesarlos.
   - Configuración en `config.yml`:
     ```yaml
     document:
       active: True  # Activa la funcionalidad
       name: documents/steam_rafa.xlsx  # Ruta del archivo
       column_name: Videojuegos Pendientes  # Columna con los títulos de los juegos
       game_time: True  # Registro del tiempo de juego
       platinium_time: True  # Registro del tiempo necesario para obtener el platino
     ```

2. **Soporte para Varias Extensiones de Archivo:**
   - La aplicación reconoce y procesa automáticamente archivos con extensiones `.csv`, `.xls`, y `.xlsx`. En función de la extensión, se utilizarán las bibliotecas adecuadas para la lectura del archivo (`pandas`).
   
3. **Manejo de Errores:**
   - Si la columna especificada no existe en el archivo o si la ruta del archivo es incorrecta, se generarán errores detallados para que el usuario pueda corregir la configuración.

4. **Interfaz Gráfica de Usuario (GUI) (en progreso):**
   - Comienzo del desarrollo de una interfaz gráfica de usuario para facilitar la interacción con la aplicación y mejorar la experiencia de usuario.
   
## 🔮 Futuros Desarrollos

- **Automatización del Proceso de Tokenización**: Automatizar el proceso de obtención y renovación del token npsso, de manera que la autenticación con PSN sea más fluida y requiera menos intervención manual por parte del usuario.

- **Interfaz Gráfica de Usuario (GUI):** Desarrollar una interfaz gráfica que facilite la interacción con la aplicación, permitiendo a los usuarios gestionar sus listas de juegos y generar informes de manera más intuitiva.

- **Integración con APIs Adicionales:** Incorporar datos de otras fuentes o servicios API que ofrezcan más detalles sobre los juegos, como estadísticas de logros, tendencias de popularidad o análisis de usuarios.

- **Sistema de Recomendaciones:** Basado en los datos recopilados, crear un sistema que sugiera juegos similares a los que el usuario ya ha disfrutado, optimizando la búsqueda de nuevos títulos.

- **Soporte Multiplataforma:** Ampliar el soporte de la herramienta para incluir juegos de otras plataformas, como Xbox, Steam o Nintendo Switch, permitiendo una comparación cruzada entre plataformas.

- **Exportación a Formatos Adicionales:** Permitir la exportación de datos en otros formatos populares como PDF o Google Sheets, facilitando su acceso y distribución.

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
