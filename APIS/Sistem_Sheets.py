import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import csv
import time
from APIS.API_Sheet_config import planilha_outbound_config, planilha_inbound_config
from utils.log import logging,print_format_text,MessageType

class BotPrint:
    def __init__(self, planilha_config):
        self.planilha_config = planilha_config

    def planilha_outbound(self):
        config = self.planilha_config

        # Verificar se todas as configurações foram definidas
        if None in (config.credentials_path, config.spreadsheet_key, config.worksheet_name, config.csv_path):
            print_format_text("As configurações da planilha não foram definidas corretamente.",MessageType.ERROR)
            return

        # Configurações do Google Sheets API
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(config.credentials_path, scopes=scope)
        client = gspread.authorize(creds)

        # Abrir a planilha do Google Sheets
        google_sheet = client.open_by_key(config.spreadsheet_key).worksheet(config.worksheet_name)
        google_sheet.clear()

        # Preencher a planilha do Google Sheets abrindo como "Modo leitor" e UTF-8 depois sobe como lista
        with open(config.csv_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            rows_with_header = list(csv_reader)
            google_sheet.insert_rows(rows_with_header)

        print_format_text('Configurando a Base, por favor aguarde...',MessageType.ALERT)
        time.sleep(5)
        print_format_text('Base configurada, prosseguindo',MessageType.SUCESS)

    def planilha_inbound(self):
        config = self.planilha_config

        # Verificar se todas as configurações foram definidas
        if None in (config.credentials_path, config.spreadsheet_key, config.worksheet_name, config.csv_path):
            print_format_text("As configurações da planilha não foram definidas corretamente.",MessageType.ERROR)
            return

        # Configurações do Google Sheets API
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(config.credentials_path, scopes=scope)
        client = gspread.authorize(creds)

        # Abrir a planilha do Google Sheets
        google_sheet = client.open_by_key(config.spreadsheet_key).worksheet(config.worksheet_name)
        google_sheet.clear()

        # Preencher a planilha do Google Sheets abrindo como "Modo leitor" e UTF-8 depois sobe como lista
        with open(config.csv_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            rows_with_header = list(csv_reader)
            google_sheet.insert_rows(rows_with_header)

        print_format_text('Configurando a Base, por favor aguarde...',MessageType.ALERT)
        time.sleep(5)
        print_format_text('Base configurada, prosseguindo',MessageType.SUCESS)

if __name__ == "__main__":
    bot_print_outbound = BotPrint(planilha_outbound_config)
    bot_print_outbound.planilha_outbound()

    bot_print_inbound = BotPrint(planilha_inbound_config)
    bot_print_inbound.planilha_inbound()
