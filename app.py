from psnawp_api import psnawp
import time

from core.document import document
from utils.selenium_tools import close_driver
from utils.utility import create_excel, end_time, load_config, try_get_config
from utils.web import read_psn


try:
    print("Obteniendo configuración...")
    cfg = load_config()
    conf_psn = try_get_config(cfg, 'PSN')
    conf_document = try_get_config(cfg, 'document')

    document(conf_document)

    if conf_psn and try_get_config(conf_psn, 'active'):
        print("Analizando cuenta PSN...")
        is_xls = conf_psn['export'] == 'xls'
        game_time = conf_psn['game_time']
        platinium_time = conf_psn['platinium_time']

        # Autenticación en PSN
        print("Obteniendo datos PSN...")
        psnawp = psnawp.PSNAWP(conf_psn['token'])

        # Obtener perfil
        profile = psnawp.me()

        # Obtener la lista de juegos y el porcentaje de avance
        print("Obteniendo trofeos PSN...")
        titles = profile.trophy_titles()

        data = []
        num_titles, data, start_time = read_psn(conf_psn, game_time, platinium_time, titles)

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
