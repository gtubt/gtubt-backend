from datetime import datetime

from django.db.transaction import atomic

from app.events import exceptions
from app.events.models import Event


class EventService(object):
    @staticmethod
    def create_event(
        title: str,
        description: str,
        cover_image_url: str,
        date: datetime,
        **kwargs: dict,
    ) -> Event:
        try:
            Event.objects.get(
                title=title,
                description=description,
                cover_image_url=cover_image_url,
                date=date,
            )
            raise exceptions.EventDuplicatedFieldException()
        except Event.DoesNotExist:
            pass

        event = Event(
            title=title,
            description=description,
            cover_image_url=cover_image_url,
            date=date,
            **kwargs,
        )

        with atomic():
            event.save()
        return event

    @staticmethod
    def update_event(event: Event, **kwargs: dict) -> Event:
        kwargs.pop("id", None)
        title = kwargs.get("title", event.title)
        description = kwargs.get("description", event.description)
        cover_image_url = kwargs.get("cover_image_url", event.cover_image_url)
        date = kwargs.get("date", event.date)

        try:
            Event.objects.exclude(id=event.id).get(
                title=title,
                description=description,
                cover_image_url=cover_image_url,
                date=date,
            )
            raise exceptions.EventDuplicatedFieldException()
        except Event.DoesNotExist:
            pass

        for key, value in kwargs.items():
            setattr(event, key, value)

        with atomic():
            event.save(update_fields=kwargs.keys())

        return event
