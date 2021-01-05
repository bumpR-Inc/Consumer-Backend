# auth0authorization/utils.py

from django.contrib.auth import authenticate
import json
import jwt
import requests

def jwt_get_username_from_payload_handler(payload):
    print(payload)
    username = payload.get('sub').replace('|', '.')
    user = authenticate(remote_user=username)
    print(type(user))
    profile = Profile(
        user = user
    )

    try:
        user.email = payload.get('https://www.goodneighbor.delivery/email')
        profile.email = user.email
    except:
        pass
    try:
        name = payload.get('https://www.goodneighbor.delivery/name').split(' ')
        user.first_name = name[0]
        user.last_name = name[1]
        profile.name = payload.get('https://www.goodneighbor.delivery/name')
    except:
        pass
    user.save()
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