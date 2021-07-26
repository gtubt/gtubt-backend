from datetime import datetime

from django.db import models

from app.news.enums import NewsTypes
from core.utils.models import StarterModel


class News(StarterModel):
    title = models.CharField("Title", max_length=255)
    body = models.TextField("Body")
    cover_image_url = models.URLField("Cover Image URL")
    summary = models.CharField("Summary", max_length=255)
    type = models.CharField(
        choices=NewsTypes.choices, default=NewsTypes.news, max_length=12
    )
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
