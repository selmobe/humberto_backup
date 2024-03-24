
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class Config_WEB:
    def __init__(self, 
                 executable_path='C:\\webdriver\\chromedriver.exe', 
                 headless=False, 
                 download_directory=None,
                 cache_directory=None,
                 start_minimized=False,
                 maximize_window_out_of_screen=True):

        self.service = Service(executable_path)
        options = Options()

        if headless:
            options.add_argument('--headless')
        if download_directory:
            prefs = {"download.default_directory": download_directory}
            options.add_experimental_option("prefs", prefs)
        if cache_directory:
            options.add_argument(f'user-data-dir={cache_directory}')
        if start_minimized:
            options.add_argument('--start-minimized')
        if maximize_window_out_of_screen:
            options.add_argument('--window-position=-32000,-32000')
            options.add_argument('--start-maximized')

        self.driver = webdriver.Chrome(service=self.service, options=options)

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        self.driver.quit()
