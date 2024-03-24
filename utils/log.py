import logging
from datetime import datetime
from enum import Enum
import os



logs_folder = 'logs'
logs_path = os.path.join(os.getcwd(), logs_folder)
os.makedirs(logs_path, exist_ok=True)  # Cria a pasta de logs se não existir

# Configuração do logger para salvar os logs no arquivo dentro da pasta "logs"
log_file_path = os.path.join(logs_path, 'app.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Definição da enumeração para os tipos de mensagem
class MessageType(Enum):
    INFORMATION = 1
    ALERT = 2
    SUCESS = 3
    ERROR = 4

def print_format_text(textForPrint, message_type=None):
    """
    Imprime a mensagem formatada no console e registra no arquivo de log utilizando o módulo logging.
    """
    color_map = {
        MessageType.INFORMATION: '\033[34m',  
        MessageType.ALERT: '\033[33m',     
        MessageType.SUCESS: '\033[32m',   
        MessageType.ERROR: '\033[31m'       
    }

    color_end = '\033[0m' 
  
    if not isinstance(message_type, MessageType):
        message_type = MessageType.INFORMATION 


    color = color_map.get(message_type)
    formatted_message = f'{color}{get_datetime_string()} - {textForPrint}{color_end}'

  
    if message_type == MessageType.INFORMATION:
        logging.info(textForPrint)
    elif message_type == MessageType.ALERT:
        logging.warning(textForPrint)
    elif message_type == MessageType.SUCESS:
        logging.info(textForPrint)
    elif message_type == MessageType.ERROR:
        logging.error(textForPrint)


    print(formatted_message)

def get_datetime_string():
    """
    Retorna uma string formatada com a data e hora atuais.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

