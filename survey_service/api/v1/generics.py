from rest_framework import generics
from rest_framework import mixins


class GetPatchAPIView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView):
    """View для получения и частичного обновления экземпляра модели."""
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
