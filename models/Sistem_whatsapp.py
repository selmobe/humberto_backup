from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import pyautogui
import pygetwindow as gw
from configs.Configuracao_WEB import Config_WEB 
from datetime import datetime, timedelta
from pygetwindow import Desktop






class WhatsAppBot:
        def __init__(self):

            cache_directory = 'C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\cache_whats'
            self.download_directory = 'C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\TrackDownload'

            config_web = Config_WEB(
            download_directory=self.download_directory,
            cache_directory=cache_directory,
            start_minimized=True)

            navegador = config_web.get_driver()
            self.navegador = navegador
            data_hora_atual = datetime.now()
            date_in = data_hora_atual.strftime('%Y-%m-%d')
            hora_passada = data_hora_atual - timedelta(hours=1)
            hour_in = hora_passada.strftime('%H:00')


            self.navegador.get('https://web.whatsapp.com/')


            time.sleep(15)



            botao_element = WebDriverWait(self.navegador, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/button/div[2]/span'))
            )
            botao_element.click()


            time.sleep(2)

            # Aguarde até que o elemento de entrada de texto seja visível
            texto_element = WebDriverWait(self.navegador, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p'))
            )

            time.sleep(4)

            # Insira o texto
            texto_element.send_keys('Teste BOT 18/01/2023')

            # Pressione Enter
            texto_element.send_keys(Keys.ENTER)

            time.sleep(2)

            print('Enviando Print')

            # Aguarde 3 segundos (pode ajustar conforme necessário)
            time.sleep(3)
            opcao_imagem = WebDriverWait(self.navegador, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/div/span'))
            )
            opcao_imagem.click()

            time.sleep(3)

            print('Finalizando, por favor aguarde')
            
            image_option = self.navegador.find_element('xpath',
                                                 '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/ul/div/div[2]/li/div/span')
            image_option.click()

            attachment = WebDriverWait(self.navegador, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.bugiwsl0:nth-child(2) > li:nth-child(1) > div:nth-child(1) > span:nth-child(2)"))
            )

            attachment.click()
            print('Enviando report')

            
            explorer = Desktop(backend="uia").window(title="Abrir")

            # Localize o controle de edição de arquivo (normalmente é chamado de 'Edit')
            file_edit = explorer.child_window(title="Nome do arquivo:", control_type="Edit")

            # Insira o caminho do arquivo
            file_edit.set_edit_text("C:\\caminho\\para\\seu\\arquivo.jpg")

            # Localize e clique no botão 'Abrir'
            open_button = explorer.child_window(title="Abrir", control_type="Button")
            open_button.click()

            # Espere um pouco para a janela fechar
            time.sleep(2)

            texto_mensagem = WebDriverWait(self.navegador, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p'))
            )
            texto_mensagem.send_keys(f'Segue relatório de produtividade das {hour_in}Hrs')

            opcao_imagem = WebDriverWait(self.navegador, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div'))
            )
            opcao_imagem.click()

            time.sleep(3)

            self.navegador.quit()

            print("Reporte enviado")

if __name__ == "__main__":
    WhatsAppBot()



