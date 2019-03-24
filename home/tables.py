import django_tables2 as tables
from home.models import User,propety,paypal_payments,booked_viewings

class UsersTable(tables.Table):
    class Meta:
        model = User
        template_name = 'adminhome.html'