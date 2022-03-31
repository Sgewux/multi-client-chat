
class User:
    '''
    User proxy class to wrap a socket object

    This class is meant to wrap a socket obj
    and "bind" it to a username, in order to 
    have a better user experience.
    '''
    def __init__(self, username, socket):
        self.username = username
        self.socket = socket

    def __getattr__(self, attr):
        '''
        Python will call this method every time we
        request an attribute that was not explicitly
        defined inside the class. This is how we achieve
        the "proxy" behavior.
        '''
        return getattr(self.socket, attr)

    def __ne__(self, other):
        '''
        Implementation of the behavior of the User instances when using !=
        '''
        if self.socket == other.socket:
            return False
        else:
            return True
