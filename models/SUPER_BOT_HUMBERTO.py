import os
import schedule
import time
from cerberus.platforms.browser_config import BrowserConfig
from cerberus.platforms.spx_system import SpxDonwloader
from MandaReport import WhatsAppBot
from utils.Convert import Report
from models.example_daemon import Damon_exec
from models.sistem_trackage import  Track_Age
from dotenv import load_dotenv

load_dotenv()

def configura_navegador_SPX():

    DIR_ROOT = 'C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload'
    cache_navegador = os.path.join(DIR_ROOT, 'cache_chrome')
    caminho_webdriver = 'C:\\webdriver\\chromedriver.exe' 
    diretorio_temporario = 'C:\\webdriver\\TEMP'
    browser = BrowserConfig(

        chrome_driver=caminho_webdriver,
        username=os.getenv('usuario'),
        password=os.getenv('senha'),
        chrome_cache=cache_navegador,
        temp_download=diretorio_temporario,
        headless_mode=True)
    
    return browser
    
    
def execute_scripts():
    browser = configura_navegador_SPX() 
    spx = SpxDonwloader(browser)
    diretorio_salvamento = 'C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\BaseSPX'
    exec = spx.export_outbound(diretorio_salvamento, 'Base') 
    print(f'O arquivo foi salvo em: {exec}')
    time.sleep(4)
 

    daemon = Damon_exec()
    daemon.extrair_dados()
    track_instance = Track_Age()
    track_instance.login_track()
    track_instance.atualizar_planilha(arquivo_destino='C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\TrackDownload\\TrackAge.xlsx')
    

    bot = BotPrint(
        credentials_path="C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\static-bond-411402-799ceaad9ba5.json",
        spreadsheet_key="1e6YC-kj_hCj0IOrVyhHocOU927AEThvJjyXrQWGOm84",
        worksheet_name="BOT_TESTE",
        csv_path="C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\BaseSPX\\Base.csv",
    )

    time.sleep(30)

    report = Report()

    google_link ='https://docs.google.com/spreadsheets/d/1e6YC-kj_hCj0IOrVyhHocOU927AEThvJjyXrQWGOm84/export?exportFormat=pdf&format=pdf&size=21.35x11.621&scale=2&top_margin=0&bottom_margin=0&left_margin=0&right_margin=0&sheetnames=false&printtitle=false&pagenum=UNDEFINEDhorizontal_alignment=LEFT&gridlines=false&fmcmd=12&fzr=FALSE&gid=1547657593&r1=0&r2=53&c1=1&c2=25'
    report.open_google(google_link)

    pdf_file_path = "C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\PDF_BAIXADOS\\Produtividade SOC-SP 02 (BOT - Packing Control.pdf"
    output_directory = "C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\IMAGENS"

    images_paths = report.convert_pdf_to_images(pdf_file_path, output_directory)

    print("Imagens convertidas:")
    for img_path in images_paths:
        print(img_path)

    WhatsAppBot()

if __name__ == '__main__':

    schedule.every().hours.do(execute_scripts)

    execute_scripts()

    while True:
        print('Aguardando próximo horário...')
        schedule.run_pending()
        time.sleep(1)
