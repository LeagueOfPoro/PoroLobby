class ClientNotRunningException(Exception):
     def __init__(self, msg='The LoL Client process could not be found. Is it running?', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)