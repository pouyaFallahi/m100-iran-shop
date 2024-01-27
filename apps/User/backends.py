from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user

        except UserModel.DoesNotExist:
            return None

        def get_user(self, user_id):
            try:
                return UserModel.objects.get(pk=user_id)
            except UserModel.DoesNotExist:
                return None
