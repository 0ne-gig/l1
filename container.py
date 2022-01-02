class ApplicationService():
    
    def __init__(self, env: str):
        self.ENV = env

    def get_env(self):
        return {"env" : self.ENV}