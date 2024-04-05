import mongoengine as me

class DBService:
    def __init__(self, db_name, host, port):
        self.db_name = db_name
        self.host = host
        self.port = port
        self.connection = None

