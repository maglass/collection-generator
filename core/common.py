import requests
import logging


def url_join(*args):
    return '/'.join(a.strip('/') for a in args)
