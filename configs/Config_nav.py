from cerberus.platforms.browser_config import BrowserConfig
from cerberus.platforms.spx_system import SpxDonwloader
import os
from dotenv import load_dotenv

load_dotenv()

def configura_navegador():

    DIR_ROOT = 'C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\temp'
    cache_navegador = os.path.join(DIR_ROOT, 'Cash_damon')
    caminho_webdriver = 'C:\\webdriver\\chromedriver.exe'
    diretorio_temporario = 'C:\\webdriver\\TEMP'
    browser = BrowserConfig(

        chrome_driver=caminho_webdriver,
        username=os.getenv('usuario'),
        password=os.getenv('senha'),
        chrome_cache=cache_navegador,
        temp_download=diretorio_temporario,
        headless_mode=False)
    
    return browser
    
