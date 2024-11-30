# logger_config.py
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, filename='tarjan_route.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger instance
logger = logging.getLogger('tarjan_logger')
