from rest_framework.decorators import action


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        Thanks to gonz: https://stackoverflow.com/a/22922156
        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()

    @action(methods=["get"], detail=True, url_path="detailed")
    def detailed(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(methods=["get"], detail=False, url_path="detailed-list")
    def detailed_list(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
