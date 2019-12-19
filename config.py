import os

DEBUG = True
MONGO_URI = os.environ.get("DATABASE_URL", "mongodb://localhost:27017/ej1")
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = "secret"
JWT_SECRET_KEY = "secret"
