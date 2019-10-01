# encoding: utf-8
from marshmallow import Schema, fields


class UserSchema(Schema):
    email = fields.Str()
    password = fields.Str()
