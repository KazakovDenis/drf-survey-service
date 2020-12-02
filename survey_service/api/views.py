from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_versions_list(request, format=None):
    """API endpoint со списком доступных версий API"""
    return Response({
        'v1': reverse('api-v1-root', request=request, format=format),
    })
