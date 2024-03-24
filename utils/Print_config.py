class ColorPrint:
    @staticmethod
    def print_info(message):
        print("\033[93m{}\033[00m".format(message))  # Amarelo

    @staticmethod
    def print_error(message):
        print("\033[91m{}\033[00m".format(message))  # Vermelho

    @staticmethod
    def print_success(message):
        print("\033[92m{}\033[00m".format(message))  # Verde


