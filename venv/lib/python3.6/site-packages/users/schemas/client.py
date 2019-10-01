# encoding: utf-8
from marshmallow import Schema, fields


class ClientSchema(Schema):
    name = fields.Str()
