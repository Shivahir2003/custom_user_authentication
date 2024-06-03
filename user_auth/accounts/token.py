from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class TokenGenerator(PasswordResetTokenGenerator):
    """
        generate Token 
    """

    def _make_hash_value(self,user,timestamp):
        return(text_type(user.password) + text_type(user.pk))


token_generator = TokenGenerator()