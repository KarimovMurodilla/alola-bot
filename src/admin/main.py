#!/usr/bin/env python3

from fastapi import FastAPI
from sqladmin import Admin

from .auth import AdminAuth
from .settings import engine
from ..configuration import conf

app = FastAPI()
authentication_backend = AdminAuth(secret_key=conf.SECRET_KEY)
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend, templates_dir='src/admin/templates')


# Register your views
# admin.add_view(UserAdmin)
