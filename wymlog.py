import logging

class Logger():
	def __init__(self,logname,logger):
		self.logger = logging.getLogger(logger)
		self.logger.setLevel(logging.DEBUG)
		
		fh = logging.FileHandler(logname)
		fh.setLevel(logging.INFO)
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		
		formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)
		
		self.logger.addHandler(fh)
		self.logger.addHandler(ch)

	def getlog(self):
		return self.logger
