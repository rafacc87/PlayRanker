import os
from bs4 import BeautifulSoup
import pytest
from unittest.mock import MagicMock, patch, mock_open
import utils.utility  # Cambiar la ruta de importación a utils.utility
import yaml


def load_config():
    # Cambiar para obtener una ruta absoluta de forma más directa
    config_path = os.path.join(os.path.abspath(os.curdir), "config.yml")
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


@patch('requests.get')
def test_get_alias(mock_get):
    # Simulamos la respuesta de la API Gist
    mock_response = MagicMock()
    mock_response.content = b'{"game_title": {"origin": "alias_value"}}'
    mock_get.return_value = mock_response

    alias = utils.utility.get_alias("game_title", "origin")
    assert alias == "alias_value"
    mock_get.assert_called_once_with(utils.utility.gist_url)

    # Probar el caso cuando no se encuentra el alias
    alias_not_found = utils.utility.get_alias("non_existent_game", "origin")
    assert alias_not_found == "non_existent_game"


def test_convert_time():
    assert utils.utility.convert_time("2 Hours") == 2.0
    assert utils.utility.convert_time("30 Mins") == 0.5
    assert utils.utility.convert_time("1½ Hours") == 1.5
    assert utils.utility.convert_time("45 Mins") == 0.75


def test_string_parse_for_url():
    assert utils.utility.string_parse_for_url("Game Title") == "game%20title"
    assert utils.utility.string_parse_for_url("Another Game® Title") == "another%20game%20title"


def test_clear_title():
    assert utils.utility.clear_title("Game Title®™") == "game title"
    assert utils.utility.clear_title("Some Trophies") == "some"


def test_get_number():
    assert utils.utility.get_number("Game Title 2") == 2
    assert utils.utility.get_number("No Number Here") is None
    assert utils.utility.get_number("Another Game 100") == 100


def test_matcher_game():
    # Simulamos algunos objetos BeautifulSoup
    html1 = '<div class="title">Game Title 1</div>'
    html2 = '<div class="title">Another Game 2</div>'
    html3 = '<div class="title">Unrelated Title</div>'

    soup1 = BeautifulSoup(html1, 'html.parser')
    soup2 = BeautifulSoup(html2, 'html.parser')
    soup3 = BeautifulSoup(html3, 'html.parser')

    posibles_titulos = [soup1, soup2, soup3]
    mejor_titulo = utils.utility.matcher_game("Game Title 1", posibles_titulos, "div", "title")

    assert mejor_titulo == soup1  # Comprobamos que encuentra la mejor coincidencia
