from tortoise import models, fields


class Cargo(models.Model):
    id = fields.IntField(pk=True)
    cargo_type = fields.CharField(
        max_length=64
    )
    rate = fields.FloatField()
    date = fields.DateField()
