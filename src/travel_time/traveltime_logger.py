import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s:\n %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info('traveltime logger initialized')
