from configs.Configuracao_WEB import Config_WEB
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import time
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from utils.log import logging,print_format_text,MessageType
import zipfile





class Tratativa_DowLoad:
    def __init__(self):
        cache_directory = 'C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\CachTets'
        self.download_directory = 'C:\\Users\\Seagroup\\Documents\\Humberto\\TO Tratativas'

        config_web = Config_WEB(
        download_directory=self.download_directory,
        cache_directory=cache_directory,
        headless=False,
        maximize_window_out_of_screen=False)

        navegador = config_web.get_driver()
        self.navegador = navegador

        hoje = datetime.now()

        self.data_formatada = hoje.strftime("%Y-%m-%d")


    def Login_Sistem(self):
        self.navegador.get('https://accounts.google.com')

        print_format_text("Verificando se já estamos logados no Sistema SPX",MessageType.INFORMATION)
        try:

            campo_login = WebDriverWait(self.navegador, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="identifierId"]'))
            )
            
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

            print_format_text("Login efetuado com sucesso.",MessageType.SUCESS)

        except TimeoutException:
            print_format_text("Sistema já está logado, iniciando download.",MessageType.INFORMATION)
            self.Download_BD()

    def Download_BD(self, max_tentativas_erro=5,max_tentativas=3):

        tentativas = 0

        print_format_text(f'Inicializando dowload, tentativa: {tentativas +1}',MessageType.INFORMATION)

        while tentativas < max_tentativas:
            try:
                self.navegador.get('https://spx.shopee.com.br/#/exceptionOrder/operationLog')
                
                tentativas_erro = 0

                try:
                    pop_up = WebDriverWait(self.navegador, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/p'))
                    )
                    pop_up.click()
                except TimeoutException:
                    print_format_text("pop-up não encontrado, proseguindo",MessageType.INFORMATION)


                while tentativas_erro < max_tentativas_erro:
                    try:
                        erro = WebDriverWait(self.navegador, 15).until(
                            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/p'))
                        )
                        print_format_text("Erro detectado. Atualizando a página.",MessageType.ERROR)
                        self.navegador.refresh()
                        tentativas_erro += 1
                        time.sleep(5)
                    except TimeoutException:
                        print_format_text("Erro não encontrado. Continuando com o processo.",MessageType.SUCESS)
                        break

                if tentativas_erro == max_tentativas_erro:
                    print_format_text("Maximo de tentativas exedido, Erro no SQL do SPX",MessageType.ERROR)
                
                else:

                    filtro_Data= WebDriverWait(self.navegador, 60).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div/div[1]/div[6]/form/div[2]/div/span/div/div/div[1]/input'))
                        )

                    filtro_Data.click()


                    filtro_Data_supenso= WebDriverWait(self.navegador, 60).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/span/div/div/div/div[1]/div[1]/span[1]/div/input'))
                        )

                    filtro_Data_supenso.send_keys(self.data_formatada)


                    filtro_Data_supenso_fim= WebDriverWait(self.navegador, 60).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/span/div/div/div/div[1]/div[2]/span[1]/div/input'))
                        )

                    filtro_Data_supenso_fim.send_keys(self.data_formatada)

                    confirm_button= WebDriverWait(self.navegador, 60).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/span/div/div/div/div[3]/button'))
                        )

                    confirm_button.click()


                    button_procurar = WebDriverWait(self.navegador,60).until(
                        EC.element_to_be_clickable((By.XPATH,'/html/body/div/div/div[2]/div[2]/div/div/div[1]/div[6]/form/div[4]/button[1]'))
                    )

                    button_procurar.click()



                    button_export = WebDriverWait(self.navegador,60).until(
                        EC.element_to_be_clickable((By.XPATH,'/html/body/div/div/div[2]/div[2]/div/div/div[1]/div[8]/div/div/button'))
                    )

                    button_export.click()


                    time.sleep(10)


                    button_confirm = WebDriverWait(self.navegador,60).until(
                        EC.element_to_be_clickable((By.XPATH,'/html/body/span/div/div[1]/div/span/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/div[2]/button')))
                    
                    time.sleep(30)

                    button_confirm.click()



                    start_time = time.time()
                    timeout = 120

                    print_format_text(f'Aguardando arquivo carregar, tempo maximo: {timeout} Segundos....',MessageType.INFORMATION)

                    arquivos_anteriores = set(os.listdir(self.download_directory))


                    while True:
                        arquivos_apos_download = set(os.listdir(self.download_directory))
                        novo_arquivo = arquivos_apos_download - arquivos_anteriores
                        if novo_arquivo:
                            break
                        if time.time() - start_time > timeout:
                            raise print_format_text("Tempo máximo de espera de download excedido.",MessageType.ERROR)
                        time.sleep(1)

                    nome_arquivo_baixado = novo_arquivo.pop()


                    if nome_arquivo_baixado.endswith('.zip'):
                        print_format_text('Arquivo .zip detectado, extraindo arquivos...',MessageType.INFORMATION)
                        self.extrair_arquivo_zip(nome_arquivo_baixado)
                    else:

                        arquivo_original = os.path.join(self.download_directory, nome_arquivo_baixado)
                        arquivo_destino = os.path.join(self.download_directory, "Tratativa.csv")

                        if os.path.exists(arquivo_destino):
                            os.remove(arquivo_destino)

                        os.rename(arquivo_original, arquivo_destino)

                        print_format_text(f'Arquivo baixado em: {self.download_directory}', MessageType.SUCESS)

                        self.navegador.quit()

                break

            except Exception as e:
                    tentativas += 1
                    print_format_text(f"Erro durante o download: {e}", MessageType.ERROR)
                    time.sleep(5)
        
            if tentativas == max_tentativas:
                    print_format_text(f'Não foi possível realizar o download após {max_tentativas} tentativas. Encerrando.', MessageType.ERROR)
                    self.navegador.quit()



    def extrair_arquivo_zip(self, nome_arquivo_zip):
        caminho_arquivo_zip = os.path.join(self.download_directory, nome_arquivo_zip)
        with zipfile.ZipFile(caminho_arquivo_zip, 'r') as zip_ref:
            zip_ref.extractall(self.download_directory)
        
        os.remove(caminho_arquivo_zip)

        print_format_text(f'Arquivo ZIP extraído: {nome_arquivo_zip}', MessageType.SUCESS)
        print_format_text(f'Arquivo ZIP removido: {nome_arquivo_zip}', MessageType.SUCESS)


        self.navegador.quit()        

if __name__ == "__main__":
    
    tratativa_instace = Tratativa_DowLoad()
    tratativa_instace.Login_Sistem()