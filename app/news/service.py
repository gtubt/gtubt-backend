from datetime import datetime

from django.db.transaction import atomic

from app.news import exceptions
from app.news.enums import NewsTypes
from app.news.models import News


class NewsService(object):
    @staticmethod
    def create_news(
        title: str,
        body: str,
        cover_image_url: str,
        summary: str,
        type: NewsTypes,
        start_date: datetime,
        end_date: datetime,
    ) -> News:
        try:
            News.objects.get(
                title=title, body=body, start_date=start_date, end_date=end_date
            )
            raise exceptions.NewsDuplicatedFieldException()
        except News.DoesNotExist:
            pass

        news = News(
            title=title,
            body=body,
            cover_image_url=cover_image_url,
            summary=summary,
            type=type,
            start_date=start_date,
            end_date=end_date,
        )

        with atomic():
            news.save()
        return news

    @staticmethod
    def update_news(news: News, **kwargs: dict) -> News:
        kwargs.pop("id", None)
        title = kwargs.get("title", news.title)
        body = kwargs.get("body", news.body)
        start_date = kwargs.get("start_date", news.start_date)
        end_date = kwargs.get("end_date", news.end_date)

        try:
            News.objects.exclude(id=news.id).get(
                title=title,
                body=body,
                start_date=start_date,
                end_date=end_date,
            )
            raise exceptions.NewsDuplicatedFieldException()
        except News.DoesNotExist:
            pass

        for key, value in kwargs.items():
            setattr(news, key, value)

        with atomic():
            news.save(update_fields=kwargs.keys())
        return news

    @staticmethod
    def delete_news(news: News):
        news.is_active = False
        with atomic():
            news.save(update_fields=["is_active"])
