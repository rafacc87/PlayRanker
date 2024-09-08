import pytest
from unittest.mock import patch, MagicMock
import utils.selenium_tools


@patch('utils.selenium_tools.webdriver.Chrome')
@patch('utils.selenium_tools.ChromeService')
def test_initialize_selenium(mock_service, mock_chrome):
    utils.selenium_tools.initialize_selenium()
    mock_service.assert_called_once()
    mock_chrome.assert_called_once()


@patch('utils.selenium_tools.webdriver.Chrome.get')
@patch('utils.selenium_tools.WebDriverWait.until')
def test_open_page_wait(mock_until, mock_get):
    # Simulamos que el driver ya está inicializado
    utils.selenium_tools.driver = MagicMock()
    utils.selenium_tools.driver.get = mock_get  # Asegúrate de que get es un MagicMock
    # Simulamos la respuesta de BeautifulSoup con un HTML falso
    utils.selenium_tools.driver.page_source = '<html><body><div class="gLFyf"></div></body></html>'

    # Llamamos a la función open_page_wait con la URL de ejemplo y la clase del campo de búsqueda
    soup = utils.selenium_tools.open_page_wait("http://example.com", "gLFyf")

    # Verificamos que se llamó al método get() del driver con la URL correcta
    mock_get.assert_called_once_with("http://example.com")

    # Verificamos que se llamó a WebDriverWait.until() para esperar el elemento con la clase 'gLFyf'
    mock_until.assert_called_once()

    # Verificamos que BeautifulSoup recibió la página fuente correcta
    assert '<div class="gLFyf">' in str(soup)


@patch('utils.selenium_tools.webdriver.Chrome.quit')  # Parchea el método quit()
def test_close_driver(mock_quit):
    # Simulamos que el driver ya está inicializado
    utils.selenium_tools.driver = MagicMock()
    utils.selenium_tools.driver.quit = mock_quit  # Asegúrate de que quit es un MagicMock
    utils.selenium_tools.driver.closed = False  # Marcamos que no está cerrado

    # Llamamos a la función close_driver
    utils.selenium_tools.close_driver()

    # Verificamos que se llamó al método quit() del driver
    mock_quit.assert_called_once()

    # Verificamos que se imprime el mensaje adecuado si intentamos cerrar de nuevo
    with patch('builtins.print') as mock_print:
        utils.selenium_tools.close_driver()
        mock_print.assert_called_with("Navegador ya estaba cerrado.")
