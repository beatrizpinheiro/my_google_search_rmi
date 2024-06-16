import rpyc
from my_google_search import MyGoogleSearch


def create_slave_service_class(name):
    class_name = f"{name}Service"
    
    class SlaveService(rpyc.Service):
        def __init__(self):
            self.name = name

        def exposed_get_answer(self, a, b = None):
            if a == "1": 
                return MyGoogleSearch().upload_file(b)
            
            if a == "2":
                return MyGoogleSearch().remove_file(b)

            if a == "3":
                files = MyGoogleSearch().list_files()
                return files
            
            if a == "4":
                return MyGoogleSearch().search(b)
            
    SlaveService.__name__ = class_name
    return SlaveService