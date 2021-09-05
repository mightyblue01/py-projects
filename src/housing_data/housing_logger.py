import logging

logging.basicConfig(filename='housing.log',format='%(asctime)s - %(name)s - %(levelname)s:\n %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('housing logger initialized')
