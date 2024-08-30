from psnawp_api import psnawp
import time

from selenium_tools import close_driver
from utility import create_excel, end_time, load_config
from web import read_psn


try:
    print("Obteniendo configuración...")
    cfg = load_config()
    psn = cfg['PSN']
    is_xls = psn['export'] == 'xls'
    game_time = psn['game_time']
    platinium_time = psn['platinium_time']

    # Autenticación en PSN
    print("Obteniendo datos PSN...")
    psnawp = psnawp.PSNAWP(psn['token'])

    # Obtener perfil
    profile = psnawp.me()

    # Obtener la lista de juegos y el porcentaje de avance
    print("Obteniendo trofeos PSN...")
    titles = profile.trophy_titles()

    data = []
    num_titles, data, start_time = read_psn(psn, game_time, platinium_time, titles)

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
