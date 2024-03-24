from configs.Configuracao_WEB import Config_WEB
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import time
from datetime import datetime
from selenium.webdriver.common.keys import Keys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from selenium.common.exceptions import TimeoutException
from utils.log import logging,print_format_text,MessageType


load_dotenv()

class Sistem_SPX:
    def __init__(self):
        cache_directory = 'C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\temp\\CachTets'
        self.download_directory = 'C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\BaseSPX\\BaseSPX_INB'

        config_web = Config_WEB(
        download_directory=self.download_directory,
        cache_directory=cache_directory,
        headless=False,
        maximize_window_out_of_screen=True)

        navegador = config_web.get_driver()
        self.navegador = navegador

    def Login_Sistem(self):
        self.navegador.get('https://accounts.google.com')

        print_format_text("Verificando se já estamos logados no Sistema SPX",MessageType.INFORMATION)
        try:
            # Verifica se o elemento de login está presente

            campo_login = WebDriverWait(self.navegador, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="identifierId"]'))
            )
            
            print_format_text("Nao logado, fazendo login...",MessageType.ALERT)

            campo_login.send_keys(os.getenv('usuario'))


            Botao_avance = WebDriverWait(self.navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="identifierNext"]/div/button'))
            )

            time.sleep(5)
            Botao_avance.click()

            time.sleep(5)

  

            campo_senha = WebDriverWait(self.navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input'))
            )
            
            campo_senha.send_keys(os.getenv('senha'))

            Botao_avance = WebDriverWait(self.navegador, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button'))
            )

            Botao_avance.click()

        except TimeoutException:
            print_format_text("Sistema já está logado, iniciando download.",MessageType.SUCESS)

    def Download_in(self, max_tentativas=3):
        tentativas = 0

        while tentativas < max_tentativas:
            print_format_text(f'Realizando downloads Base Inbound - Tentativa{tentativas + 1}',MessageType.INFORMATION)

            self.navegador.get('https://spx.shopee.com.br/#/dashboard/toProductivity?page_type=Inbound')

            try:
                pop_up = WebDriverWait(self.navegador, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/p'))
                )
                pop_up.click()
            except TimeoutException:
                print_format_text("pop-up não encontrado, proseguindo",MessageType.INFORMATION)

                time.sleep(4)

                export = WebDriverWait(self.navegador, 50).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div[2]/div[3]/span/span/span/button'))
                )
                export.click()



                export_dow = WebDriverWait(self.navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/span/div/div/div[1]'))
                )
                export_dow.click()

                try:
                    export_dow_confirm = WebDriverWait(self.navegador, 240).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/span/div/div[1]/div/span/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/div[2]/button'))
                    )
                    export_dow_confirm.click()

                    nome_arquivo_baixado = self.esperar_download_concluido()
                    self.salvar_arquivo(nome_arquivo_baixado, "Inbound.xls")

                    print_format_text(f'Arquivo Inbound baixado e salvo em: {self.download_directory}',MessageType.SUCESS)
                    return  # Saia da função se o download for bem-sucedido

                except TimeoutException:
                    print_format_text("Tempo de espera para confirmação do download expirado. Verifique se o download foi concluído manualmente.",MessageType.ERROR)

            except Exception as e:
                tentativas += 1
                print_format_text(f"Erro durante o download: {e}",MessageType.ERROR)
                time.sleep(5)

                if tentativas == max_tentativas:
                    print_format_text(f'Não foi possível realizar o download após {max_tentativas} tentativas. Encerrando.',MessageType.ERROR)
                    break  # Sai do loop se as tentativas excederem o máximo (burro)
                else:
                    print_format_text(f'Download feito na {tentativas + 1}ª tentativa.',MessageType.SUCESS)


    def Download_out(self, max_tentativas=3):
        tentativas = 0

        while tentativas < max_tentativas:
            print_format_text(f'Realizando downloads Base Outbound - Tentativa{tentativas +1}',MessageType.INFORMATION)

            self.navegador.get('https://myaccount.google.com/')

            self.navegador.get('https://spx.shopee.com.br/#/dashboard/toProductivity?page_type=Outbound')

            time.sleep(15)

            export = WebDriverWait(self.navegador, 120).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div[1]/div[2]/div[3]/span/span/span/button'))
            )
            export.click()

            export_dow = WebDriverWait(self.navegador, 120).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/span/div/div/div[1]'))
            )
            export_dow.click()

            try:
                export_dow_confirm = WebDriverWait(self.navegador, 240).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/span/div/div[1]/div/span/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/div[2]/button'))
                )
                export_dow_confirm.click()

                nome_arquivo_baixado = self.esperar_download_concluido()
                self.salvar_arquivo(nome_arquivo_baixado, "BaseSPX_OUt.xls")

                print_format_text(f'Arquivo Outbound baixado e salvo em: {self.download_directory}',MessageType.SUCESS)
                return 

            except TimeoutException:
                print_format_text("Tempo de espera para confirmação do download expirado. Verifique se o download foi concluído manualmente.",MessageType.ERROR)

            except Exception as e:
                tentativas += 1
                print_format_text(f"Erro durante o download: {e}",MessageType.ERROR)
                time.sleep(5)

                if tentativas == max_tentativas:
                    print_format_text(f'Não foi possível realizar o download após {max_tentativas} tentativas. Encerrando.',MessageType.ERROR)
                    break  
                else:
                    print_format_text(f'Download feito na {tentativas + 1}ª tentativa.',MessageType.SUCESS)

                
    def esperar_download_concluido(self):
        arquivos_anteriores = set(os.listdir(self.download_directory))
        
        while True:
            arquivos_apos_download = set(os.listdir(self.download_directory))
            novo_arquivo = arquivos_apos_download - arquivos_anteriores
            if novo_arquivo:
                break
            time.sleep(1)

        return novo_arquivo.pop()

    def salvar_arquivo(self, nome_arquivo, nome_destino):
        arquivo_original = os.path.join(self.download_directory, nome_arquivo)
        arquivo_destino = os.path.join(self.download_directory, nome_destino)

        if os.path.exists(arquivo_destino):
            os.remove(arquivo_destino)

        os.rename(arquivo_original, arquivo_destino)

    def quit_navegador(self):
        self.navegador.quit()


if __name__ == "__main__":
    spx_instance = Sistem_SPX()
    spx_instance.Login_Sistem()
    spx_instance.Download_in()
    spx_instance.Download_out()
    spx_instance.quit_navegador()