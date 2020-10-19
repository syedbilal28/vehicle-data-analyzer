import json
from channels.generic.websocket import WebsocketConsumer
class SearchConnector(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        names=list(text_data_json.keys())[0]
        file=text_data_json['csv_file']
        