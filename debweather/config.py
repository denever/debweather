class Config:
    def __init__(self, mainfile):
        self.APP_PATH = os.path.dirname(mainfile)
        if self.APP_PATH == '/usr/bin':
            self.PIX_PATH = os.path.join(os.path.dirname(self.APP_PATH), 'share/pixmaps/pydebweather')
            self.DATA_PATH = os.path.join(os.path.dirname(self.APP_PATH), 'share/pydebweather')
        else:
            self.PIX_PATH=os.path.join(self.APP_PATH, 'data/')
            self.DATA_PATH=os.path.join(self.APP_PATH, 'data/')
        logging.debug("self.PIX_PATH: %s" % self.PIX_PATH)
        logging.debug("self.DATA_PATH: %s" % self.DATA_PATH)

    def get_app_path(self):
        return self.APP_PATH
    
    def get_pix_path(self):
        logging.debug("self.PIX_PATH: %s" % self.PIX_PATH)
        return self.PIX_PATH

    def get_in_pix_path(self, file):
        logging.debug("self.PIX_PATH: %s" % self.PIX_PATH)
        return os.path.join(self.PIX_PATH,file)
    
    def get_data_path(self):
        logging.debug("self.DATA_PATH: %s" % self.DATA_PATH)
        return self.DATA_PATH

    def get_in_data_path(self, file):
        logging.debug("self.DATA_PATH: %s" % self.DATA_PATH)
        return os.path.join(self.DATA_PATH,file)

