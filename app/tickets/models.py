from django.db import models

from core.utils.models import StarterModel


class Ticket(StarterModel):
    event = models.ForeignKey("events.Event", on_delete=models.PROTECT)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("event", "user")
