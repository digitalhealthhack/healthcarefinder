from mongo import Document

AUTH = {'host': 'localhost', 'port': 27017}

class HealthCenter(Document):
    __connection__ = AUTH
    __database__ = 'healthcenters'  # database name

