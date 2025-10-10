__all__ = [
    'BaseAPI',
    'AuthAPI',
    'PostMeme',
    'PutMeme',
    'DeleteMeme',
    'GetMemes',
    'GetMeme',
]

from endpoints.base_api import BaseAPI
from endpoints.authorize import AuthAPI
from endpoints.post_meme import PostMeme
from endpoints.put_meme import PutMeme
from endpoints.delete_meme import DeleteMeme
from endpoints.get_meme import GetMemes, GetMeme
