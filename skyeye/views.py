from rest_framework import status
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
import logging

db_logger = logging.getLogger('db')

# Create your views here.
class SiteSerializer(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("사이트", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            db_logger.exception(status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_400_BAD_REQUEST)
