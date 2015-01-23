from models.logindaymodel import LoginDayModel
from models.loginhourmodel import LoginHourModel

class LoginModel():
    def __init__(self):
        self.hour_model = LoginHourModel()
        self.day_model = LoginDayModel()

    def get_conf(self):
        conf = {
            'sub_conf' : ['login_logcount'],
            'state' : 'login'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            hour_result = self.hour_model.handle(recv_body)
            if hour_result:
                self.day_model.handle(hour_result)
                day_result = self.day_model.handle(hour_result)
                return day_result

