from django.db import models


class NewsTypes(models.TextChoices):
    announcement = "announcement"
    news = "news"
