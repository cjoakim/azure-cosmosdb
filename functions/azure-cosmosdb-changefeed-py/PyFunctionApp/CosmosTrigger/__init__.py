import arrow
import logging
import azure.functions as func


def main(documents: func.DocumentList) -> str:
    utc = arrow.utcnow()
    logging.info('function invoked at: {}'.format(str(utc)))
    
    if documents:
        for doc in documents:
            #logging.info('Document id: %s', documents[0]['id'])
            logging.info(doc.to_json())
