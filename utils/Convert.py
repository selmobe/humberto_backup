import os
from pdf2image import convert_from_path
from configs.Configuracao_WEB import Config_WEB
import time 
from utils.log import logging,print_format_text,MessageType
class Report:
    def __init__(self):
        self.download_directorys = "C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\utils\\PDF_BAIXADOS"

    def open_google(self, link):
        self.download_directory = self.download_directorys

        config_web = Config_WEB(
            download_directory=self.download_directory,
            start_minimized=False)

        navegador = config_web.get_driver()
        self.navegador = navegador
        
        try:
            self.navegador.get(link)
            
            time.sleep(5) 
        finally:
            self.navegador.quit()

    def convert_pdf_to_images(self, pdf_path, output_directory, image_prefix="image"):
        poppler_path = r'C:\\Users\\Seagroup\\Documents\\Humberto\\VSCODE Humberto\\SPX Dowload\\utils\\POPPLER\\Library\\bin'
       
        images = convert_from_path(pdf_path, poppler_path=poppler_path)


        os.makedirs(output_directory, exist_ok=True)

        image_paths = []
        for i, img in enumerate(images):
            image_path = os.path.join(output_directory, f"{image_prefix}_{i + 1}.png")
            img.save(image_path, "PNG")
            image_paths.append(image_path)

        return image_paths

    def clean_directory(self, directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print_format_text(f"Erro ao excluir {file_path}: {e}",MessageType.ERROR)

    def download_pdf_and_convert_to_images(self, link):

        self.clean_directory(self.download_directorys)

        # Abre o link no navegador
        self.open_google(link)

        # Espera um tempo para garantir que o download seja concluído
        time.sleep(4)  # Ajuste conforme necessário

        # Localiza o PDF baixado
        pdf_files = [file for file in os.listdir(self.download_directorys) if file.endswith('.pdf')]
        if pdf_files:
            pdf_path = os.path.join(self.download_directorys, pdf_files[0])
            # Converte o PDF baixado em imagens
            images = self.convert_pdf_to_images(pdf_path, self.download_directorys)
            print_format_text(f'Imagens salvas em {self.download_directorys}',MessageType.SUCESS)
            return images
        else:
            print_format_text("Nenhum arquivo PDF encontrado após o download.",MessageType.ERROR)








        