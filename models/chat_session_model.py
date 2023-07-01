
class ChatSessionModel:
    def __init__(self):
        self.observers = []
        self.guid = None

    def set_guid(self, guid):
        self.guid = guid

    #         - Chat session ID
    #         - User email address
    #         - User name
    #         - User organization
    #         - Display the start time
    #         - Display Start date of each chat session
    #         - Display running duration of each chat session
    #         - Display the current sentiment of the chat session
    #         - Display the running cost of each chat session
    #         - Display number of user queries submitted in each chat session
    #         - Display the number of prompts submitted in each chat session
    #         - Keywords/Topics of each chat session


    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)
