class SessionConf:
    instance = None
    
    @classmethod
    def get(cls):
        return cls.instance
    
    @classmethod
    def new(cls):
        cls.instance = SessionConf()
        return cls.instance

    def __init__(self):
        self.selected_block = 0
        self.max_fps = 60
