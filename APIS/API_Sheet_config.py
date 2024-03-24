class PlanilhaConfig:
    def __init__(self, credentials_path=None, spreadsheet_key=None, worksheet_name=None, csv_path=None):
        self.credentials_path = credentials_path
        self.spreadsheet_key = spreadsheet_key
        self.worksheet_name = worksheet_name
        self.csv_path = csv_path

# Configurações da planilha outbound
planilha_outbound_config = PlanilhaConfig(
    credentials_path="C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\APIS\\static-bond-411402-799ceaad9ba5.json",
    spreadsheet_key="1e6YC-kj_hCj0IOrVyhHocOU927AEThvJjyXrQWGOm84",
    worksheet_name="BOT_TESTE",
    csv_path="C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\BaseSPX\\BaseSPX_INB\\BaseSPX_OUt.xls"
)

# Configurações da planilha inbound
planilha_inbound_config = PlanilhaConfig(
    credentials_path="C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\APIS\\static-bond-411402-799ceaad9ba5.json",
    spreadsheet_key="1pIaRExNB8zteUwzJFQy5ghJWfYqbIIEQ4skNuX0Iuyw",
    worksheet_name="BaseSPX_BOT",
    csv_path="C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\BaseSPX\\BaseSPX_INB\\Inbound.xls"
)
