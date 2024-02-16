import hashlib

class Message:
    def __init__(self,message):
        self.message = message
        self.hash = hashlib.sha256(message.encode()).hexdigest()
        self.received_from = []
        self.sent_to = []

    
