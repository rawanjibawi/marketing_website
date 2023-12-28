# file used for email verification
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six # we have to install this package

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return(
            six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_active)
            ) 
        
account_activation_token = AccountActivationTokenGenerator()