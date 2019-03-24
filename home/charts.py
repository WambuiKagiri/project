import pygal

from home.models import User,propety,listrequest,booked_viewings,paypal_payments

class UserChart():
    def __init__(self,**kwargs):
        self.chart = pygal.Pie(**kwargs)
        self.chart.title = 'Registered Users'

    def get_data(self):
        data = {}
        for user in User.objects.all():
            data[user.username] = user.groups
        return data

    def generate(self):
        chart_data = self.get_data()

        for key, value in chart_data.items():
            self.chart.add(key, value)

class PropertyChart():
    def __init__(self,**kwargs):
        self.chart = pygal.Pie(**kwargs)
        self.chart.title = 'Listed properties'

    def get_data(self):
        data = {}
        for p in propety.objects.all():
            data[p.location] = p.rentbuy
        return data

    def generate(self):
        chart_data = self.get_data()

        for key, value in chart_data.items():
            self.chart.add(key, value)
