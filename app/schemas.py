from marshmallow_sqlalchemy import ModelSchemaOpts
from marshmallow_sqlalchemy import ModelSchema
from .extensions import db

# Boiler Plate REF: https://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html
class BaseOpts(ModelSchemaOpts):
    def __init__(self, meta, ordered=False):
        if not hasattr(meta, "sqla_session"):
            meta.sqla_session = db.session
        super(BaseOpts, self).__init__(meta, ordered=ordered)


# All schemas should inherit this class
class BaseSchema(ModelSchema):
    OPTIONS_CLASS = BaseOpts
