from models.createroledaymodel import CreateroleDayModel
from models.createrolehourmodel import CreateroleHourModel

class CreateroleModel():
    def __init__(self):
        self.hour_model = CreateroleHourModel()
        self.day_model = CreateroleDayModel()

    def get_conf(self):
        conf = {
            'sub_conf' : ['createrole_logcount'],
            'state' : 'createrole'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            hour_result = self.hour_model.handle(recv_body)
            if hour_result:
                self.day_model.handle(hour_result)
                day_result = self.day_model.handle(hour_result)
                return day_result

