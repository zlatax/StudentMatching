from flask_pymongo import PyMongo
import bcrypt
import certifi

import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# Usage: JSONEncoder().encode(analytics)

mongo = PyMongo()
salt = bcrypt.gensalt()
ca = certifi.where()


