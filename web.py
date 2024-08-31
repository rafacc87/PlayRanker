import time
from bs4 import BeautifulSoup
import requests
from selenium_tools import initialize_selenium, open_page_wait
from utility import convert_time, get_alias, matcher_game, process_time, string_parse_for_url


def metracritic_score(game_title):
    result_review = result_user = 0
    try:
        # Search game
        title = string_parse_for_url(game_title)
        metacritic_search = f"https://www.metacritic.com/search/{title}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(metacritic_search, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Obtener todos los contenedores de juegos
        posibles_titulos = soup.find_all('a', class_='c-pageSiteSearch-results-item')  # Ajusta según la estructura de la página
        # Encontrar el título más parecido al juego buscado
        title_element = matcher_game(game_title, posibles_titulos, 'p', 'g-text-medium-fluid')

        if title_element:
            metacritic_url = f"https://www.metacritic.com{title_element['href']}"
        else:
            metacritic_url = f"https://www.metacritic.com/game/{title}"

        # Game score
        response = requests.get(metacritic_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Score review
        result_review = get_score_metracritic(soup, 'c-siteReviewScore', True)

        # Score user
        result_user = get_score_metracritic(soup, 'c-siteReviewScore_user', False)
    except Exception as e:
        print()
        print(f"Error obteniendo puntuación de Metacritic para {game_title}: {e}")

    # Obtenemos las posibles revisiones de criticos si las hubiera y hacemos la media
    result_review = get_reviews(result_review, metacritic_url, 'critic-reviews', True)

    # Obtenemos las posibles revisiones de los usuarios si las hubiera y hacemos la media
    result_user = get_reviews(result_user, metacritic_url, 'user-reviews', False)

    if result_review == 0:
        result_review = result_user
    elif result_user == 0:
        result_user = result_review

    return metacritic_search, (result_user + result_review) / 2


def howlongtobeat_time(game_title):
    hltb_url = f"https://howlongtobeat.com/?q={string_parse_for_url(game_title)}"
    duration = -1

    try:
        try:
            soup = open_page_wait(hltb_url, 'back_darkish')
        except Exception:
            return hltb_url, duration

        # Obtener todos los contenedores de juegos
        posibles_titulos = soup.find_all('li', class_='back_darkish')  # Ajusta según la estructura de la página
        # Encontrar el título más parecido al juego buscado
        result = matcher_game(game_title, posibles_titulos, 'h2', '')

        if result:
            tiempos = []
            tiempos_detalles = result.find_all('div', class_='center')

            for tiempo in tiempos_detalles:
                tiempo_text = convert_time(tiempo.text.strip())
                # if 'Hours' in tiempo_text or 'Mins' in tiempo_text:
                tiempos.append(tiempo_text)

            if tiempos:
                duration = max(tiempos)
            if duration < 1:
                duration = -1
    except Exception as e:
        print()
        print(f"Error obteniendo duración de HowLongToBeat para {game_title}: {e}")

    return hltb_url, duration


def platprices_difficulty(game_title):
    duration = -1
    difficulty = 0
    try:
        url = f"https://platprices.com/search.php?q={string_parse_for_url(game_title)}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Obtener todos los contenedores de juegos
        posibles_titulos = soup.find_all('div', class_='game-container-lo')  # Ajusta según la estructura de la página
        # Encontrar el título más parecido al juego buscado
        game_container = matcher_game(game_title, posibles_titulos, 'div', 'game-name')

        # game_container = soup.find('div', class_='game-container-lo')
        if game_container:
            game_difficulty = game_container.find('div', class_='game-tile-difficulty')
            if game_difficulty:
                infos = game_difficulty.find_all('font')

                if len(infos) >= 2:
                    # Extraer la dificultad y horas
                    difficulty_str = infos[0].text.strip()
                    duration_str = infos[1].text.strip().replace(" Hours", "")

                    # Parsear la dificultad
                    if '/' in difficulty_str:
                        difficulty = int(difficulty_str.split('/')[0].strip())

                    # Parsear las horas y manejar intervalos
                    if 'hours' in duration_str:
                        duration_parts = duration_str.split()[0].split('-')
                        if len(duration_parts) == 2:
                            duration = max(float(duration_parts[0]), float(duration_parts[1]))
                        else:
                            duration = float(duration_parts[0])

    except Exception as e:
        print()
        print(f"Error obteniendo el tiempo necesario para platino de Platprices para {game_title}: {e}")

    return url, difficulty, duration


def get_reviews(result, metacritic_url, path, divid):
    if result == 0:
        try:
            metacritic_critic_reviews_url = f"{metacritic_url}{path}/"
            soup = open_page_wait(metacritic_critic_reviews_url, 'c-siteReviewScore')
            scores_div = soup.find_all('div', class_='c-siteReviewScore')

            scores = []
            for score in scores_div:
                tiempo_text = float(score.text.strip())
                scores.append(tiempo_text)

            if scores:
                result = sum(scores)
                if divid:
                    result = result / 10
                result = result / len(scores)
                if result < 1:
                    result = 1
        except Exception:
            pass
    return result


def get_score_metracritic(soup, class_name, divid):
    result = 0
    score_review = soup.find('div', class_=class_name)
    if score_review:
        score_review_span = score_review.find('span')
        if score_review_span:
            if score_review_span.text != 'tbd':
                result = float(score_review_span.text.strip())
                result = result
                if divid:
                    result = result / 10
    return result


def read_psn(psn, game_time, platinium_time, titles):
    data = []
    data_filter, total, plat_count = get_games_psn(psn, titles)

    if game_time:
        print("Iniciando recursos necesarios...")
        initialize_selenium()

    num_titles = len(data_filter)
    print(f"Se van a revisar {num_titles} de los {total} juegos que tienes. Ya tienes {plat_count} platinos!!!")
    start_time = time.time()
    for i2, title in enumerate(data_filter):
        # Obtener y filtrar por plataformas del juego
        platforms_list = [p.value for p in title.title_platform]
        platforms = ', '.join(platforms_list)

        game_title = title.title_name.replace('\n', '')
        progress = title.progress

        # Obtener puntuación de Metacritic
        url_metacritic, score = metracritic_score(get_alias(game_title, 'metacritic'))

        # Obtener duración del juego desde HowLongToBeat
        if game_time:
            # main_story = obtener_tiempo_juego(game_title, 'Main Story')
            # main_extra = obtener_tiempo_juego(game_title, 'Main + Extra')
            url_howlongtobeat, duration = howlongtobeat_time(get_alias(game_title, 'howlongtobeat'))

        # Obtener tiempo platino
        if platinium_time:
            url_platprices, difficulty_platinium, duration_platinium = platprices_difficulty(get_alias(game_title, 'platprices'))

        # Valores de las columnas
        columns_values = [platforms, url_metacritic, game_title, progress, score]
        if game_time:
            columns_values.extend([url_howlongtobeat, duration, score / duration])
        if platinium_time:
            columns_values.extend([url_platprices, difficulty_platinium, duration_platinium, score / duration_platinium])
        data.append(columns_values)

        # Calcular tiempo transcurrido y restante
        process_time(num_titles, start_time, i2)
    return num_titles, data, start_time


def get_games_psn(psn, titles):
    data_filter = []
    total = 0
    plat_count = 0

    for i, title in enumerate(titles):
        total = titles._total_item_count

        # Obtener y filtrar por plataformas del juego
        platforms_list = [p.value for p in title.title_platform]
        filter_list = psn['platforms']
        if filter_list:
            filtered_platforms = [p for p in platforms_list if p in filter_list]
        else:
            filtered_platforms = []
        if len(filtered_platforms) < 1:
            continue

        # Descartamos platinos completados o que no tengan
        plt_earned = title.earned_trophies.platinum
        plt_defined = title.defined_trophies.platinum
        if plt_defined > 0 and plt_earned != plt_defined:
            data_filter.append(title)
        elif plt_earned > 0:
            plat_count += 1
    return data_filter, total, plat_count
