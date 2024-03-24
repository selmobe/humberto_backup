import schedule
import time
from models.example_daemon import Damon_exec
from dotenv import load_dotenv
from models.sistem_trackage import Track_Age
from models.SistemSPX import Sistem_SPX
from APIS.Sistem_Sheets import BotPrint, planilha_outbound_config, planilha_inbound_config 
from utils.Convert import Report
from models.Download_tratativa import Tratativa_DowLoad
from utils.log import logging,print_format_text,MessageType


load_dotenv()



def execute_scripts():
    duracao_script = time.time()
    print_format_text('Incializando sistema: DataGuardian..', MessageType.INFORMATION)

    spx_instance = Sistem_SPX()
    spx_instance.Login_Sistem()
    spx_instance.Download_in() 
    spx_instance.Download_out()
    spx_instance.quit_navegador()
    
    time.sleep(5)

    bot_print_outbound = BotPrint(planilha_outbound_config)
    bot_print_outbound.planilha_outbound()

    bot_print_inbound = BotPrint(planilha_inbound_config)
    bot_print_inbound.planilha_inbound()

    
    report_instance = Report()
    report_instance.download_pdf_and_convert_to_images('https://docs.google.com/spreadsheets/d/1e6YC-kj_hCj0IOrVyhHocOU927AEThvJjyXrQWGOm84/export?exportFormat=pdf&format=pdf&size=21.35x11.621&scale=2&top_margin=0&bottom_margin=0&left_margin=0&right_margin=0&sheetnames=false&printtitle=false&pagenum=UNDEFINEDhorizontal_alignment=LEFT&gridlines=false&fmcmd=12&fzr=FALSE&gid=1547657593&r1=0&r2=53&c1=1&c2=25')

    track_instance = Track_Age()
    track_instance.login_track()
    track_instance.atualizar_planilha(arquivo_destino='C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\TrackDownload\\TrackAge.xlsx')

    time.sleep(4)

    tratativa_instace = Tratativa_DowLoad()
    tratativa_instace.Login_Sistem()
    tratativa_instace.Download_BD()

    Tempo_execucao = time.time() - duracao_script
    tempo_restante = 3600 - Tempo_execucao  # 3600 = 1 Hora 

    if tempo_restante > 0:
        print_format_text(f"A execução do Script dorou: {Tempo_execucao/60:.2f} segundos...",MessageType.SUCESS)
        print_format_text(f"Esperando proxima execução em: {tempo_restante/60:.0f} Minutos",MessageType.INFORMATION)
        time.sleep(tempo_restante)

if __name__ == '__main__':
    while True:
        execute_scripts()
        schedule.run_pending()
        time.sleep(1)
