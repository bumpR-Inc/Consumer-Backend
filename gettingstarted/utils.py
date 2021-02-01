# auth0authorization/utils.py

from django.contrib.auth import authenticate
import json
import jwt
import requests
from hello.models import *

def jwt_get_username_from_payload_handler(payload):
    print(payload)
    username = payload.get('sub').replace('|', '.')
    user = authenticate(remote_user=username)

    if not User.objects.filter(id=user.id).exists():
        try:
            user.email = payload.get('https://www.goodneighbor.delivery/email')
        except:
            pass
        try:
            name = payload.get('https://www.goodneighbor.delivery/name').split(' ')
            user.first_name = name[0]
            user.last_name = name[1]
        except:
            pass
        user.save()

    if not Profile.objects.filter(user=user).exists():
        profile = Profile(
            user = user
        )

        try:
            profile.email = user.email
        except:
            pass
        try:
            profile.name = payload.get('https://www.goodneighbor.delivery/name')
        except:
            pass
        profile.save()

    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format('goodneighbor.us.auth0.com')).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = 'https://{}/'.format('goodneighbor.us.auth0.com')
    decoded =  jwt.decode(token, public_key, audience='https://goodneighbor.us.auth0.com/api/v2/', issuer=issuer, algorithms=['RS256'])
    print("decoded:" ,decoded)
    return decoded