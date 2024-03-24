from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import os
from selenium.webdriver.chrome.service import Service
import shutil


def open_google(link):
    chromedriver_path = "C:\\webdriver\\chromedriver.exe"
    download_directory = "C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\DamonDownload"
    link = 'http://10.48.50.206:8787/chart/SortingSummaryDWS'

    hoje = datetime.now()
    data_formatada = hoje.strftime("%d/%m/%y")


    chrome_options = Options()
    service = Service(chromedriver_path)
    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': download_directory,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True,
        'headless':True

    })

    chrome_cache = 'C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\Cash_damon'
    chrome_options.add_argument(f"user-data-dir={chrome_cache}")

    driver = webdriver.Chrome(options=chrome_options,service=service)

    # Obtém a data e hora atuais
    data_hora_atual = datetime.now()

    # Formata a hora cheia atual
    hora_cheia = data_hora_atual.strftime('%H:00:00')

    hora_anterior = data_hora_atual - timedelta(hours=1)

    hora_cheia_anterior = hora_anterior.strftime('%H:00:00')

    try:
        driver.get(link)

        time.sleep(5)

        xpath_login_presente = driver.find_elements(By.XPATH, '//*[@id="app"]/div/form/div[1]/div/div[1]/input')

        if xpath_login_presente:
            print('Login não encontrado, começando login')

            fazer_login(driver)
        else:
            print("XPath de login não encontrado. Começando o download.")

        fazer_download_DWS(driver, hora_cheia_anterior, hora_cheia,data_formatada)

        Download_CBS(driver, hora_cheia_anterior, hora_cheia,data_formatada)

    finally:
        driver.quit()

def fazer_login(driver):
    login_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/form/div[1]/div/div[1]/input'))
    )
    login_input.send_keys('shopee')

    login_senha = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/form/div[2]/div/div/input'))
    )
    login_senha.send_keys('shopee')

    confirm_login = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/form/div[3]/div/button'))
    )
    confirm_login.click()

def fazer_download_DWS(driver, hora_cheia_anterior, hora_cheia,data_formatada):
    hora = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/section/div/form/div[1]/div/div/input[1]'))
    )
    time.sleep(5)

    hora.click()

    hora_DWS = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div/div[1]/span[1]/span[2]/div[1]/input'))
    )

    hora_DWS.click()
    time.sleep(5)
    hora_DWS.clear()
    hora_DWS.send_keys(hora_cheia_anterior)

    hora_DWS_2 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div/div[1]/span[3]/span[2]/div[1]/input'))
    )

    hora_DWS_2.click()
    time.sleep(5)
    hora_DWS_2.clear()
    hora_DWS_2.send_keys(hora_cheia)

    botao_ok = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/button[2]'))
    )

    botao_ok.click()

    submit = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/section/div/form/div[2]/div/button/span'))
    )

    submit.click()

    dws = {
            'type': 'DWS' , 
            'Date': data_formatada,
            'Hour_Start': hora_cheia_anterior, 
            'Hour_End': hora_cheia, 
            'Total': WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/section/div/div[2]/div[3]/table/tbody/tr/td[2]/div'))).text,
            'Sucess': WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/section/div/div[2]/div[3]/table/tbody/tr/td[3]/div'))).text,
            'Rjct': WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/section/div/div[2]/div[3]/table/tbody/tr/td[3]/div'))).text, 
            'percent_rjct': WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/section/div/div[2]/div[3]/table/tbody/tr/td[3]/div'))).text,
            'NoRd': WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/section/div/div[2]/div[3]/table/tbody/tr/td[3]/div'))).text,
            'APIE': WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/section/div/div[2]/div[3]/table/tbody/tr/td[3]/div'))).text,
            'NoCh': WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/section/div/div[2]/div[3]/table/tbody/tr/td[3]/div'))).text,
            'Full': WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/section/div/div[2]/div[3]/table/tbody/tr/td[3]/div'))).text,
            'TrkFail':WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/section/div/div[2]/div[3]/table/tbody/tr/td[3]/div'))).text,
    }

    print(dws)

    input()


def Download_CBS(driver, hora_cheia_anterior, hora_cheia, download_directory):
    driver.get('http://10.48.50.206:8787/chart/SortingSummaryCBS')

    CBSHORA = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/div/form/div[2]/div/div/input[1]'))
    )

    CBSHORA.click()

    CBSHORA_2 = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div/div[1]/span[1]/span[2]/div[1]/input'))
    )

    CBSHORA_2.click()

    time.sleep(5)
    CBSHORA_2.clear()
    CBSHORA_2.send_keys(hora_cheia_anterior)

    CBSHORA_3 = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/div/div[1]/span[3]/span[2]/div[1]/input'))
    )

    CBSHORA_3.click()

    time.sleep(5)
    CBSHORA_3.clear()
    CBSHORA_3.send_keys(hora_cheia)

    botao_ok_2 = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/button[2]'))
    )

    botao_ok_2.click()

    submit = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/div/form/div[3]/div/button'))
    )

    submit.click()

    Download_up = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/div/div[1]/div[1]/button'))
    )

    Download_up.click()

    Download_up_pop_up = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div[3]/button[2]'))
    )

    Download_up_pop_up.click()

    nome_arquivo = f"ProdutividadeCBS_UP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    caminho_novo = os.path.join(download_directory, nome_arquivo)

    lista_arquivos = os.listdir(download_directory)
    arquivo_baixado = max(lista_arquivos, key=lambda x: os.path.getctime(os.path.join(download_directory, x)))

    caminho_antigo = os.path.join(download_directory, arquivo_baixado)

    # Copia o arquivo para o novo destino, mantendo o original
    shutil.copy(caminho_antigo, caminho_novo)

    cbs_down = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/section/div/form/div[1]/div/div/div[1]/input'))
    )

    cbs_down.click()


    cbs_down =  WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/section/div/form/div[1]/div/div/div[1]/input'))
    )
    
    cbs_down.click()


    cbs_down=  WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/section/div/form/div[1]/div/div/div[1]/input'))
    )
    
    cbs_down.click()

    cbs_down_confirm =  WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[1]/div[1]/ul/li[1]'))
    )

    cbs_down_confirm.click()

    cbs_down_=  WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/div/form/div[2]/div/div/input[1]'))
    )

    cbs_down_.click()


    
    cbs_down_=  WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[1]/div/div[1]/span[1]/span[2]/div[1]/input'
    ))
    )

    cbs_down_.click()
    cbs_down_.clear()
    cbs_down_.send_keys(hora_cheia_anterior)

    cbs_down_=  WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[1]/div/div[1]/span[3]/span[2]/div[1]/input'
    ))
    )

    cbs_down_.click()
    cbs_down_.clear()
    cbs_down_.send_keys(hora_cheia)


    cbs_down_ok=  WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[2]/button[2]'
    ))
    )

    cbs_down_ok.click()


    cbs_down_submit=  WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((By.XPATH, '//html/body/div[1]/div/div[2]/section/div/form/div[3]/div/button'
    ))
    )

    cbs_down_submit.click()

    cbs_down_submit_download=  WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[2]/section/div/div[1]/div[1]/button'
    ))
    )

    cbs_down_submit_download.click()

    time.sleep(14)

    cbs_down_submit_download_pop=  WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[3]/button[2]'
    ))
    )

    cbs_down_submit_download_pop.click()

    input()


# Exemplo de uso
google_link = "http://10.48.50.206:8787/login?redirect=%2Fchart%2FSortingSummaryDWS"
open_google(google_link)
