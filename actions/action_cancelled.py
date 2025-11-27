class ActionCancelled(Exception):
    """
    Eccezione personalizzata per annullare operazione
    """
    def __init__(self,message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
