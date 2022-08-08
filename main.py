from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import os

def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=800,600', '--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument)
        
    chrome_options.add_experimental_option('prefs', {
        # Desabilitar a confirmação de download
        'download.prompt_for_download': False,
        # Desabilitar notificações
        'profile.default_content_setting_values.notifications': 2,
        # Permitir multiplos downloads
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

driver = iniciar_driver()


# navegar até o site
driver.get('https://www.olx.pt/d/ads/q-consola-Super-Nintendo/')
driver.maximize_window()
botao_aceitar = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
botao_aceitar.click()
sleep(10)

while True:
    # Carregar todos os elementos na tela vai ao final da página e depois ao topo
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(2)
    driver.execute_script('window.scrollTo(0, document.body.scrollTop);')
    sleep(10)
    # Encontrar os títulos
    titulos = driver.find_elements(By.XPATH, '//div[@class="css-u2ayx9"]//h6')
    # Encontrar os preços
    precos = driver.find_elements(By.XPATH, '//p[@class="css-wpfvmn-Text eu5v0x0"]')
    # Encontrar os links dos anúncios
    links_anuncios = driver.find_elements(By.XPATH, '//a[@class="css-1bbgabe"]')
    # Guardar em arquivo .CSV
    for titulo, preco, link in zip(titulos, precos, links_anuncios):
        with open('precos.csv', 'a', encoding='utf-8', newline='') as arquivo:
            link_arquivo = link.get_attribute('href')
            arquivo.write(f'{titulo.text};{preco.text};{link_arquivo}{os.linesep}')
    # Fazer isso para todas as páginas existentes
    try:
        botao_forward = driver.find_element(By.XPATH, '//*[@data-testid="pagination-forward"]')
        sleep(1)
        botao_forward.click()
    except:
        print('Chegamos na última página')
        break


input('')
driver.close()