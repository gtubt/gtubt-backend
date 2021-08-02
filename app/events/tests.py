from datetime import datetime

from django.test import TestCase
from model_bakery import baker

from app.events.resources.serializers import EventSerializer
from app.events.service import EventService


class EventServiceTestCase(TestCase):
    service = EventService()
    serializer = EventSerializer

    def test_create_event(self):
        data = {
            "title": "test_title",
            "description": "test_description",
            "cover_image_url": "https://coverimage.url",
            "date": datetime.now(),
        }
        serializer = self.serializer(data=data)
        self.assertTrue(serializer.is_valid())
        event = self.service.create_event(**serializer.validated_data)
        self.assertEqual(event.title, data["title"])
        self.assertEqual(event.description, data["description"])

    def test_update_event(self):
        event = baker.make("events.Event", title="test_title")
        data = {
            "title": "test_title_update",
            "description": "test_description_update",
        }
        updated_event = self.service.update_event(event=event, **data)
        self.assertEqual(updated_event.title, data["title"])
        self.assertEqual(updated_event.description, data["description"])
