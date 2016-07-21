import logging

class Logger():
    def __init__(self, logname, logger):
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        __file_handler = logging.FileHandler(logname)
        __file_handler.setLevel(logging.INFO)
        __stream_handler = logging.StreamHandler()
        __stream_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
        __file_handler.setFormatter(formatter)
        __stream_handler.setFormatter(formatter)

        self.logger.addHandler(__file_handler)
        self.logger.addHandler(__stream_handler)

    def getlog(self):
        return self.logger
