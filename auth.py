import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


#-----------------------------------Auth0 Config-----------------------------------------#

#ADD THIS TO ENV

AUTH0_DOMAIN = 'aschonn.us.auth0.com'
ALGORITHMS = ["RS256"]
API_AUDIENCE = 'casting'

#--------------------------------- AuthError Exception-------------------------------------------#


class AuthError(Exception):
    '''A standardized way to communicate auth failure modes'''
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
    

#-----------------------------------Auth Wrapper Methods-----------------------------------------#


def get_token_auth_header():

    auth = request.headers.get('Authorization', None)
    # Raise error if no "Authorization" is part of header
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    # Raise error if no "Bearer" is part "Authorization"
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    # Raise error if "Authorization" only contains 1 part (it should have 2)
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    # Raise error if "Authorization" contains more than 2 parts (it should only have 2)
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    # When everyhting is fine, get the token which is the second part of the Authorization Header & return it
    return parts[1]

def check_permissions(permission, payload):

    #if permission is not in payload raise error
    if 'permissions' not in payload:
                        raise AuthError({
                            'code': 'invalid_claims',
                            'description': 'Permissions not included in JWT.'
                        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True

def verify_decode_jwt(token):

    # Verify token
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    
    # Check if Key id is in unverified header
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    rsa_key = {} 
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # Use Auth Config to decode JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        # Raise if token is not valid
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        # Error if wrong audience
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        # In all other Error cases
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    # raise error if no payload.
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)



def requires_auth(permission=''):

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                raise AuthError({
                    'code': 'unauthorized',
                    'description': 'Permissions not found'
                }, 401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator