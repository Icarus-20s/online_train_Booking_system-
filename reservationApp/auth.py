from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from reservationApp.models import User
from django.conf import settings


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the token from cookies
        token = request.COOKIES.get("token")
        if not token:
            raise NotAuthenticated("Token cookie missing")

        try:
            payload = AccessToken(token).payload

            id = payload.get(settings.SIMPLE_JWT["USER_ID_CLAIM"])
            user = self.get_user_by_id(id) if id else None
            if not user:
                raise AuthenticationFailed("Invalid auth token")

            return user, None

        except AuthenticationFailed as e:
            raise e
        except Exception as e:
            raise AuthenticationFailed("Invalid auth token")

    def get_user_by_id(self, id):
        raise NotImplementedError("Subclasses must implement this method")


class UserAuthentication(JWTAuthentication):
    def get_user_by_id(self, id):
        return User.objects.filter(id=id).first()
