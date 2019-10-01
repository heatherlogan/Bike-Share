# encoding: utf-8
from marshmallow import Schema, fields


class DocumentSchema(Schema):
    name = fields.Str()
    value = fields.Str()
