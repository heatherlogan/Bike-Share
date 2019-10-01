# encoding: utf-8
from marshmallow import Schema, fields


class ScopeSchema(Schema):
    name = fields.Str()
