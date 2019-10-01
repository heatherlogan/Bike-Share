# encoding: utf-8
from marshmallow import Schema, fields


class ServiceProviderSchema(Schema):
    uid = fields.Str()
    name = fields.Str()
