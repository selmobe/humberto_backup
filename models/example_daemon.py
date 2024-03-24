import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from cerberus.platforms.daemon import Daemon, OPTIONS_SELECT
from configs.Config_nav import configura_navegador
from datetime import datetime, timedelta
from cerberus.tools.utils import MessageType,print_format_text

class Damon_exec():
    def __init__(self):
        self.__browser = configura_navegador()

    def extrair_dados(self, max_tentativas=3):
        tentativas = 0
        while tentativas < max_tentativas:
            try:
                print_format_text(f'Realizando download tentativa n {tentativas+1}', MessageType.SUCESS)
                data_hora_atual = datetime.now()
                date_in = data_hora_atual.strftime('%Y-%m-%d')
                hora_passada = data_hora_atual - timedelta(hours=1)
                hour_in = hora_passada.strftime('%H')
                file_inductions = os.path.join('induções_daemon_', hour_in, os.getcwd())

                daemon = Daemon(self.__browser, username='shopee', password='shopee')

                up = daemon.extract_cbs(date=date_in, hour=hour_in, type_cmb=OPTIONS_SELECT.CBS_UP)
                down = daemon.extract_cbs(date=date_in, hour=hour_in, type_cmb=OPTIONS_SELECT.CBS_DOWN)
                ptl = daemon.extract_cbs(date=date_in, hour=hour_in, type_cmb=OPTIONS_SELECT.PTL_2)
                dws = daemon.extract_dws(date=date_in, hour=hour_in)

                dados = [up, down, ptl, dws]
                dados_formatados = [[str(d)] for d in dados]

                # Baixa o arquivo com as induções utilizando a hora fechada
                file_inductions = daemon.extract_inductions_productivy(date=date_in, hour=hour_in, filepath_filename=file_inductions)

                print(f'CBS-UP: {up}\nCBS-DOWN: {down}\nCBS-PTL-2: {ptl}\nDWS: {dws}\nINDUÇÕES: {file_inductions}')

                # Adicione a lógica de planilha aqui
                self.atualizar_planilha(dados_formatados)

                self.__browser.__del__


            except Exception as e:
                tentativas += 1
                print(f"Ocorreu um erro: {e}")

            if tentativas == max_tentativas:
                print_format_text(f'Não foi possível realizar download após {max_tentativas} tentativas. Encerrando...', MessageType.ERROR)
            
            else:
                print_format_text(f'Download feito na {tentativas + 1}ª tentativa.', MessageType.SUCESS)
                break
            

    def atualizar_planilha(self, dados_formatados):
        try:
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            credentials_path = "C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\APIS\\static-bond-411402-799ceaad9ba5.json"
            credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
            client = gspread.authorize(credentials)

            spreadsheet_key = "1e6YC-kj_hCj0IOrVyhHocOU927AEThvJjyXrQWGOm84"
            worksheet_name = "BOT_TESTE_SORTER"

            worksheet = client.open_by_key(spreadsheet_key).worksheet(worksheet_name)
            worksheet.append_rows(dados_formatados)

            print("Dados adicionados à planilha com sucesso!")

        except Exception as e:
            print(f"Erro ao atualizar a planilha: {e}")


if __name__ == "__main__":
    daemon_executor = Damon_exec()
    daemon_executor.extrair_dados()
