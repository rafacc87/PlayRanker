import csv
from difflib import SequenceMatcher
import json
import os
import re
import sys
import time
import pandas as pd
import requests
import yaml


gist_url = "https://gist.githubusercontent.com/rafacc87/03b8cf3b7c903d5412f64217586a8ee5/raw"
alias_data: any = None


def get_resource_path():
    """Obtiene la ruta absoluta al recurso, ya sea en desarrollo o empaquetado."""
    if getattr(sys, 'frozen', False):
        # Ejecutándose como un archivo empaquetado por PyInstaller
        base_path = os.path.dirname(sys.executable)
        return os.path.join(base_path, "config.yml")
    else:
        # Ejecutándose en un entorno de desarrollo
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, "../config.yml")


def load_config():
    config_path = get_resource_path()
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_path}")
    with open(config_path, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg


def try_get_config(config, name):
    try:
        return config[name]
    except Exception:
        return None


def get_alias(game_title, origin):
    global alias_data
    try:
        # Hacer la solicitud para obtener el JSON desde el Gist
        if alias_data is None:
            response = requests.get(gist_url)
            alias_data = json.loads(response.content)

        # Verificar si el título tiene un alias en el archivo JSON
        if game_title in alias_data:
            return alias_data[game_title][origin]
        else:
            return game_title  # Si no se encuentra un alias, devolver el título original

    except Exception as e:
        print(f"Error obteniendo alias: {e}")
        return game_title


def convert_time(tiempo_str):
    # Reemplazar fracciones con decimales
    tiempo_str = tiempo_str.replace('½', '.5').replace('¼', '.25').replace('¾', '.75')

    # Convertir tiempo a horas
    if "Hours" in tiempo_str:
        horas = float(tiempo_str.replace(" Hours", ""))
    elif "Mins" in tiempo_str:
        minutos = float(tiempo_str.replace(" Mins", ""))
        horas = minutos / 60  # Convertir minutos a horas
    else:
        horas = 0  # En caso de que no haya tiempo

    return horas


def string_parse_for_url(game_title):
    return __clear_string(game_title).replace(' ', '%20')


def clear_title(titulo):
    return __clear_string(titulo).strip()


def __clear_string(text):
    return text.lower().replace('®', ' ').replace('™', ' ').replace('  ', ' ').replace(' trophies', '').replace('’', '\'').replace(':', '').replace('\n', '').replace(':', '')


def get_number(titulo):
    # Extrae el primer número que aparece en el título
    numeros = re.findall(r'\d+', titulo)
    return int(numeros[0]) if numeros else None


def matcher_game(titulo_original, posibles_titulos, label, class_method):
    titulo_original = clear_title(titulo_original)
    numero_original = get_number(titulo_original)
    mejor_coincidencia = None
    mayor_similitud = 0

    for titulo in posibles_titulos:
        name = titulo.find(label, class_=class_method)
        titulo_limpio = clear_title(name.text)
        numero_limpio = get_number(titulo_limpio)

        # Comparar similitud textual
        similitud = SequenceMatcher(None, titulo_original, titulo_limpio).ratio()

        # Dar más importancia si los números coinciden
        if numero_original and numero_limpio and numero_original == numero_limpio:
            similitud += 0.3  # Aumentar la similitud si los números coinciden

        if similitud > mayor_similitud:
            mayor_similitud = similitud
            mejor_coincidencia = titulo
        if (numero_original is not None and similitud >= 1.3) or (numero_original is None and similitud >= 1):
            return mejor_coincidencia

    return mejor_coincidencia


def validate_data(data, expected_length, columns_excel):
    for row in data:
        if len(row) != expected_length:
            # Imprimir los nombres de las columnas y la primera línea de datos
            if data:
                print("Columnas:", columns_excel)
                print("Primera línea de datos:", data[0])
            print(f"Error: Row {row} does not have the expected {expected_length} values.")
            return False
    return True


def create_excel(game_time, platinium_time, data, is_xls=True, platforms=True):
    columns_excel = []
    if platforms:
        columns_excel = ['Plataforma']
    columns_excel.extend(['Metacritic', 'Videojuego', '% Trofeos', 'Puntuación'])
    if game_time:
        columns_excel.extend(['Howlongtobeat', 'Duración', 'Calidad'])
    if platinium_time:
        columns_excel.extend(['Platprices', 'Dificultad trofeos', 'Duración trofeos', 'Calidad trofeos'])

    try:
        expected_length = len(columns_excel)
        if not validate_data(data, expected_length, columns_excel):
            return

        if is_xls:
            df = pd.DataFrame(sorted(data, key=lambda x: x[-1], reverse=True), columns=columns_excel)
            df.to_excel('documents/psn_juegos.xlsx', index=False)
            print("Excel exportado exitosamente.")
        else:
            raise ImportError  # Forzamos la exportación a CSV si is_xls es False
    except ImportError:
        with open('psn_juegos.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(columns_excel)
            for row in sorted(data, key=lambda x: x[-1], reverse=True):
                writer.writerow(row)
        print("Exportando como CSV.")


def process_time(num_titles, start_time, i):
    # Calcular tiempo transcurrido y restante
    elapsed_time = time.time() - start_time
    remaining_time = (elapsed_time / (i + 1)) * (num_titles - (i + 1))

    # Mostrar progreso y tiempo restante
    minutes, seconds = divmod(remaining_time, 60)
    if minutes > 9:
        print(f"Procesando juegos: {i + 1}/{num_titles} ({(i + 1) / num_titles:.2%}) - Tiempo restante: {int(minutes)} minutos       ", end='\r')
    elif minutes > 0:
        print(f"Procesando juegos: {i + 1}/{num_titles} ({(i + 1) / num_titles:.2%}) - Tiempo restante: {int(minutes)} min {int(seconds)} seg     ", end='\r')
    else:
        print(f"Procesando juegos: {i + 1}/{num_titles} ({(i + 1) / num_titles:.2%}) - Tiempo restante: {int(seconds)} segundos          ", end='\r')


def end_time(start_time, num_titles):
    elapsed_time = time.time() - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"Procesamiento completado para {num_titles} juegos en {int(hours)} horas, {int(minutes)} minutos y {int(seconds)} segundos.")
