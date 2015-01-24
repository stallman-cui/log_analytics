from models.signupdaymodel import SignupDayModel
from models.signuphourmodel import SignupHourModel

class SignupModel():
    def __init__(self):
        self.hour_model = SignupHourModel()
        self.day_model = SignupDayModel()

    def get_conf(self):
        conf = {
            'sub_conf' : ['signup_logcount'],
            'state' : 'signup'
        }
        return conf

    def handle(self, recv_body):
        if recv_body:
            hour_result = self.hour_model.handle(recv_body)
            if hour_result:
                day_result = self.day_model.handle(hour_result)
                return day_result
