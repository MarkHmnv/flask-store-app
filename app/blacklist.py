"""
blacklist.py

This file contains the blacklist of the JWT tokens. It will be imported by
app and the logout view so that tokens can be added to the blacklist when the
user logs out.

TODO: Replace this with the Redis
"""

BLACKLIST = set()
