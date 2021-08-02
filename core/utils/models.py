from django.db import models


class StarterModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if update_fields is not None:
            if not isinstance(update_fields, list):
                update_fields = list(update_fields)
            update_fields.append("modified_date")
        super(StarterModel, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
