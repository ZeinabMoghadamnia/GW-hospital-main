import logging

logging.basicConfig(filename='logfile.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)
handler = logging.FileHandler('logfile.log')
formatter = logging.Formatter('%(asctime)s -%(name)s- %(funcName)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

