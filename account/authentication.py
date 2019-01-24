from django.contrib.auth.models import User
# from django.contrib.auth import authenticate


# the custom email authentication class has two method
# authenticate and get_user

class EmailAuthBackend(object):

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)

            if user.check_password(password):
                return User

            return None

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)

        except User.DoesNotExist:
            return None