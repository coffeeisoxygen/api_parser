from utils.mylogger import logger


class AppService:
    def __init__(self):
        self.logger = logger
        self.logger.info("AppService initialized")
