class MessageManager(object):
    
    def __new__(cls):
        if not "instance" in cls.__dict__:
            cls.instance = object.__new__(cls)
            instance = cls.instance
            instance.messageCounter = 0
        return cls.instance
    
    def getMessageId(self):
        self.messageCounter += 1
        return self.messageCounter