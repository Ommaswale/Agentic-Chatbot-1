from configparser import ConfigParser

class Config:
    def __init__(self, config_file='./src/App/UI/config.ini'):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get_page_title(self):
        return self.config['DEFAULT'].get('page_title')
    
    def get_llm_options(self):
        return self.config['DEFAULT'].get('LLMs').split(',')
    
    def get_usecases(self):
        return self.config['DEFAULT'].get('usecases').split(',')