import time
import pandas as pd

from utils.selenium_tools import initialize_selenium
from utils.utility import process_time, create_excel, end_time, try_get_config
from utils.web import read_title_data


def document(conf_document):
    if conf_document and try_get_config(conf_document, 'active'):
        print("Tratando documento...")
        file_name = conf_document['name']
        column_name = conf_document['column_name']
        game_time = conf_document['game_time']
        platinium_time = conf_document['platinium_time']

        # Determinar la extensión del archivo
        file_extension = file_name.split('.')[-1].lower()

        # Leer archivo en base a la extensión
        if file_extension == 'csv':
            df = pd.read_csv(file_name)
        elif file_extension in ['xls', 'xlsx']:
            df = pd.read_excel(file_name)
        else:
            raise ValueError("Formato de archivo no soportado: {}".format(file_extension))

        # Verificar que la columna existe
        if column_name not in df.columns:
            raise ValueError("Columna '{}' no encontrada en el archivo.".format(column_name))

        # Extraer los datos de la columna especificada
        titles = df[column_name].dropna().tolist()

        if game_time:
            print("Iniciando recursos necesarios...")
            initialize_selenium()

        num_titles = len(titles)
        print(f"Se van a revisar {num_titles} juegos que tienes.")
        start_time = time.time()
        data = []
        for i2, titulo in enumerate(titles):
            columns_values = read_title_data(titulo, game_time, platinium_time, None, None)
            data.append(columns_values)

            # Calcular tiempo transcurrido y restante
            process_time(num_titles, start_time, i2)

        # Mostrar progreso y tiempo restante
        end_time(start_time, num_titles)

        # Guardar en Excel
        create_excel(game_time, platinium_time, data, file_extension in ['xls', 'xlsx'], False)
