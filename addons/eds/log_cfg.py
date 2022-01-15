import logging

def configure_eds_logging():
    """Configures the `logging` module output for EDS scripts"""

    # Get the logger
    logger = logging.getLogger("eds")
    
    # Set the logging level
    logger.setLevel(logging.DEBUG)

    # Set up formatting for console output
    formatter = logging.Formatter("[EDS -> %(levelname)s]: %(message)s")
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    logger.addHandler(stream)

