from difflib import SequenceMatcher
import json
import re
import time
import requests # type: ignore
import yaml # type: ignore


gist_url = "https://gist.githubusercontent.com/rafacc87/03b8cf3b7c903d5412f64217586a8ee5/raw"
alias_data: any = None

def load_config():
    with open("config.yml", 'r') as ymlfile:     
        cfg = yaml.safe_load(ymlfile)
    return cfg

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
        if (numero_original != None and similitud >= 1.3) or (numero_original == None and similitud >= 1):
            return mejor_coincidencia

    return mejor_coincidencia


def process_time(num_titles, start_time, i):
    # Calcular tiempo transcurrido y restante
    elapsed_time = time.time() - start_time
    remaining_time = (elapsed_time / (i + 1)) * (num_titles - (i + 1))
    
    # Mostrar progreso y tiempo restante
    minutes, seconds = divmod(remaining_time, 60)
    if minutes > 9:
        print(f"Procesando juegos: {i + 1}/{num_titles} ({(i + 1) / num_titles:.2%}) - Tiempo restante: {int(minutes)} minutos       ", end='\r')
    elif minutes > 0:
        print(f"Procesando juegos: {i + 1}/{num_titles} ({(i + 1) / num_titles:.2%}) - Tiempo restante: {int(minutes)} min {seconds:.2f} seg     ", end='\r')
    else:
        print(f"Procesando juegos: {i + 1}/{num_titles} ({(i + 1) / num_titles:.2%}) - Tiempo restante: {seconds:.2f} segundos          ", end='\r')