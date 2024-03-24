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
from utils.log import logging,print_format_text,MessageType
from datetime import datetime, timedelta


load_dotenv()

class Track_Age:
    def __init__(self):
        self.cache_directory = 'C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\temp\\Cach\\cach_crome'
        self.download_directory = 'C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\TrackDownload'

        config_web = Config_WEB(
            download_directory=self.download_directory,
            cache_directory=self.cache_directory,
            start_minimized=False)

        navegador = config_web.get_driver()
        self.navegador = navegador

        hoje = datetime.now()
        self.inicio_mes = hoje - timedelta(days=14)
        self.inicio_mes_formatado = self.inicio_mes.strftime("%d/%m/%y")
        self.data_formatada = hoje.strftime("%d/%m/%y")

    def login_track(self):  
        self.navegador.get('https://maestro.trackage.io/admin/dashboard-dynamic')
        print_format_text("Verificando se já estamos logados no sistema TrackAge", MessageType.INFORMATION)

        try:
            campo_login = WebDriverWait(self.navegador, 15).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/app-root/mat-sidenav-container/mat-sidenav-content/div[2]/div/main/app-login-detail/div/div[1]/div/mat-stepper/div/div[2]/div[1]/form/div[1]/mat-form-field/div[1]/div/div[2]/input'))
            )
            print_format_text("Não logado, fazendo login...", MessageType.ALERT)
            campo_login.send_keys(os.getenv('usuario'))

            botao_next = WebDriverWait(self.navegador, 5).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/mat-sidenav-container/mat-sidenav-content/div[2]/div/main/app-login-detail/div/div[1]/div/mat-stepper/div/div[2]/div[1]/form/div[3]/span/button/span[2]'))
            )
            time.sleep(2)
            botao_next.click()

            campo_senha = WebDriverWait(self.navegador, 5).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div/div/div[1]/div/form/div[3]/input'))
            )
            campo_senha.send_keys(os.getenv('senhatrack'))

            botao = WebDriverWait(self.navegador, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//html/body/div/div/div/div/div/div[1]/div/form/div[5]/input[2]'))
            )
            time.sleep(2)
            botao.click()

            print_format_text("Login efetuado.", MessageType.SUCESS)

            self.realizar_downloads()

        except:
            print_format_text("Já logado. Pulando para a próxima etapa.", MessageType.INFORMATION)

            self.realizar_downloads()


    def realizar_downloads(self, max_tentativas=3):
        print_format_text("Realizando downloads...", MessageType.INFORMATION)
        self.navegador.get('https://maestro.trackage.io/admin/dashboard-dynamic')
        time.sleep(5)

        tentativas = 0

        while tentativas < max_tentativas:
            print_format_text(f'Realizando downloads - Tentativa {tentativas + 1}', MessageType.INFORMATION)

            try:

                self.navegador.get('https://maestro.trackage.io/admin/dashboard-dynamic')

                painel_1 = WebDriverWait(self.navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/mat-sidenav-container/mat-sidenav/div/mat-nav-list/a[1]/span/span/i'))
                )
                painel_1.click()

                time.sleep(3)

                painel_2 = WebDriverWait(self.navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/mat-sidenav-container/mat-sidenav/div/div/div/div[4]/a'))
                )
                painel_2.click()

                
                relaotorio = WebDriverWait(self.navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/mat-sidenav-container/mat-sidenav-content/div[2]/div/main/app-reports/div/div[1]/mat-card/mat-card-actions/button/span[2]'))
                )
                relaotorio.click()

                filtro = WebDriverWait(self.navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/mat-sidenav-container/mat-sidenav-content/div[2]/div/main/app-report-dynamic-filter/mat-expansion-panel/mat-expansion-panel-header/span[1]'))
                )
                time.sleep(3)
                filtro.click()

                filtro_check = WebDriverWait(self.navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="cdk-accordion-child-0"]/div/div/form/mat-form-field'))
                )
                filtro_check.click()

                filtro_perido = WebDriverWait(self.navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-option-6"]'))
                )
                filtro_perido.click()

                filtro_data = WebDriverWait(self.navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/mat-sidenav-container/mat-sidenav-content/div[2]/div/main/app-report-dynamic-filter/mat-expansion-panel/div/div/div/form/mat-form-field[2]/div[1]/div/div[2]/input'))
                )
                filtro_data.send_keys(self.inicio_mes_formatado)

                time.sleep(4)


                filtro_data_hoje = WebDriverWait(self.navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/mat-sidenav-container/mat-sidenav-content/div[2]/div/main/app-report-dynamic-filter/mat-expansion-panel/div/div/div/form/mat-form-field[3]/div[1]/div/div[2]/input'))
                )
                time.sleep(5)
                for _ in range(10):
                    filtro_data_hoje.send_keys(Keys.BACKSPACE)
                
                time.sleep(10)
                filtro_data_hoje.send_keys(self.data_formatada)
                filtro_data_hoje.send_keys(Keys.ENTER)


                print_format_text(f'Baixando Relatorio do dia {self.inicio_mes_formatado} até o dia {self.data_formatada}',MessageType.INFORMATION)

                filtro_descarregados = WebDriverWait(self.navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="cdk-accordion-child-0"]/div/div/form/mat-form-field[4]/div[1]/div/div[1]/div[2]'))
                )
                filtro_descarregados.click()

                descarregados = WebDriverWait(self.navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-option-25"]'))
                )
                descarregados.click()

                Add_filtro = WebDriverWait(self.navegador, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="cdk-accordion-child-0"]/div/div/form/button/span[3]'))
                )
                Add_filtro.click()

                time.sleep(15)

                get_download = WebDriverWait(self.navegador, 50).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/mat-sidenav-container/mat-sidenav-content/div[1]/mat-toolbar/div/div[2]/div/button[1]/span[4]'))
                )
                get_download.click()

                time.sleep(15)

                get_download_popup = WebDriverWait(self.navegador, 60).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/app-file-type-selector/mat-dialog-content/div/button[2]'))
                )
                get_download_popup.click()

                
                start_time = time.time()
                timeout = 120

                print_format_text(f'Aguardando arquivo carregar, tempo maximo: {timeout} Segundos....',MessageType.ALERT)

                arquivos_anteriores = set(os.listdir(self.download_directory))


                while True:
                    arquivos_apos_download = set(os.listdir(self.download_directory))
                    novo_arquivo = arquivos_apos_download - arquivos_anteriores
                    if novo_arquivo:
                        break
                    if time.time() - start_time > timeout:
                        raise print_format_text('Tempo maximo excedido',MessageType.ERROR)
                    time.sleep(1)

                nome_arquivo_baixado = novo_arquivo.pop()

                arquivo_original = os.path.join(self.download_directory, nome_arquivo_baixado)
                arquivo_destino = os.path.join(self.download_directory, "TrackAge.xlsx")

                if os.path.exists(arquivo_destino):
                    os.remove(arquivo_destino)

                os.rename(arquivo_original, arquivo_destino)

                print_format_text(f'Arquivo baixado em: {self.download_directory}', MessageType.SUCESS)

                self.atualizar_planilha()

                self.navegador.quit()

                break

            except Exception as e:
                tentativas += 1
                print_format_text(f"Erro durante o download: {e}", MessageType.ERROR)
                time.sleep(5)

        if tentativas == max_tentativas:
            print_format_text(f'Não foi possível realizar o download após {max_tentativas} tentativas. Encerrando.', MessageType.ERROR)
            self.limpar_cache_directory()
        else:
            print_format_text(f'Download feito na {tentativas + 1}ª tentativa.', MessageType.SUCESS)
            self.atualizar_planilha()

    def atualizar_planilha(self, arquivo_destino='C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\TrackDownload\\TrackAge.xlsx'):
        print_format_text('Subindo base de relatório para planilha "YMS"', MessageType.INFORMATION)

        try:
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            credentials_path = "C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\APIS\\static-bond-411402-799ceaad9ba5.json"
            credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
            client = gspread.authorize(credentials)

            spreadsheet_key = "1pIaRExNB8zteUwzJFQy5ghJWfYqbIIEQ4skNuX0Iuyw"
            worksheet_name = "YMS_BOT"

            worksheet = client.open_by_key(spreadsheet_key).worksheet(worksheet_name)
            worksheet.clear()
            
            df = pd.read_excel(arquivo_destino)
            
            df = df.applymap(str)
        
            rows_with_header = df.values.tolist()

            worksheet.append_rows(rows_with_header)

            print_format_text(f'Base adicionada na planilha: {worksheet_name}',MessageType.SUCESS)

        except Exception as e:
            print_format_text(f"Erro ao atualizar a planilha: {e}", MessageType.ERROR)

    def limpar_cache_directory(self):
        print_format_text("Tentativas maximas excedidas, limpando o diretório de cache...", MessageType.ALERT)
        try:
            self.navegador.quit()
            time.sleep(5)
            for filename in os.listdir(self.cache_directory):
                file_path = os.path.join(self.cache_directory, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print_format_text(f"Erro ao excluir {file_path}: {e}", MessageType.ERROR)
            print_format_text("Diretório de cache limpo com sucesso.", MessageType.SUCESS)
            time.sleep(15)
            track_instance()
        except Exception as e:
            print_format_text(f"Erro ao limpar o diretório de cache: {e}", MessageType.ERROR)


if __name__ == "__main__":
    track_instance = Track_Age()
    track_instance.login_track()
