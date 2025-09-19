from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    role = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class UserRegisterSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    confirm_password = fields.String(required=True)
    
    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data['password'] != data['confirm_password']:
            raise ValidationError('Passwords do not match', 'confirm_password')

class UserLoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
