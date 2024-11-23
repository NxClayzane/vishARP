"""
LOGGING MODULE
"""
import logging

def LogFile():

    try: 
        logging.basicConfig(filename='vishARP.log', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    except Exception as e:
        print("Failed to Log Err:{e}")
        



    