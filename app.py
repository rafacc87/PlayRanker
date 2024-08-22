from psnawp_api import psnawp
import time

from selenium_tools import close_driver, initialize_selenium
from utility import create_excel, end_time, load_config
from web import read_psn


try:
    cfg = load_config()
    psn = cfg['PSN']
    is_xls = psn['export'] == 'xls'
    game_time = psn['game_time']
    platinium_time = psn['platinium_time']

    if game_time:
        initialize_selenium()

    # Autenticación en PSN
    psnawp = psnawp.PSNAWP(psn['token'])

    # Obtener perfil
    profile = psnawp.me()

    # Obtener la lista de juegos y el porcentaje de avance
    titles = profile.trophy_titles()

    data = []
    time.sleep(5)
    start_time = time.time()

    num_titles, data = read_psn(psn, game_time, platinium_time, titles, start_time)

    # Mostrar progreso y tiempo restante
    end_time(start_time, num_titles)

    # Guardar en Excel
    create_excel(game_time, platinium_time, data, is_xls)

    print("Hoja de cálculo generada exitosamente.")
except Exception as e:
    print()
    print(f"Ocurrió un error: {e}")
finally:
    close_driver()
