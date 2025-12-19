import random
import string

from .models import ShortURL

ALIAS_RESERVED =['admin' , 'api']

def generate_short_code(length=6):
    chars=string.ascii_letters+string.digits
    while True:
        code=''.join(random.choices(chars, k=length))
        if not ShortURL.objects.filter(short_code=code).exists():
            return code

def validate_short_url(alias):
    if alias in ALIAS_RESERVED:
        raise ValueError('This alias is reserved.')

    if ShortURL.objects.filter(custom_alias=alias).exists():
        raise ValueError('This alias is already taken.')