from rest_framework_simplejwt.tokens import AccessToken

def store_email_verification_token(user):
    token = AccessToken.for_user(user)
    token["email_verify"] = True
    return str(token)


