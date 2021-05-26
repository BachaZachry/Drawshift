from urllib.parse import parse_qs

# Third Party Stuff
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from knox.auth import TokenAuthentication


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(
            scope["query_string"]
        )  # used for querystring token url auth
        headers = dict(scope["headers"])
        knoxAuth = TokenAuthentication()
        if b"token" in query_string:
            try:
                token_key = query_string[b"token"][0]
                user, auth_token = knoxAuth.authenticate_credentials(token_key)
                scope["user"] = user
                close_old_connections()
            except Exception:
                scope["user"] = AnonymousUser()
        elif b"authorization" in headers:
            try:
                token_name, token_key = headers[b"authorization"].decode().split()
                if token_name == "Token":
                    user, auth_token = knoxAuth.authenticate_credentials(
                        token_key.encode()
                    )
                    scope["user"] = user
                    close_old_connections()
            except Exception:
                scope["user"] = AnonymousUser()
        else:
            pass  # session auth or anonymous
        return await self.inner(scope, receive, send)


def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))