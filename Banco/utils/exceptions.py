

class SameAccount(Exception):
    """
    This exeption would raise if a user is trying to transfer money to his own account
    """
    def __init__(self):
        super().__init__()