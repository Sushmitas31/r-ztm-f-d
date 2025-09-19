from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(allow_none=True)
    completed = fields.Boolean(load_default=False)
    user_id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class TaskCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String(allow_none=True)
    completed = fields.Boolean(load_default=False)

class TaskUpdateSchema(Schema):
    title = fields.String(validate=validate.Length(min=1, max=200))
    description = fields.String(allow_none=True)
    completed = fields.Boolean()
