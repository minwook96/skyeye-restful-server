from .serializers import DetectionSerializer
from .models import Detection
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import logging

db_logger = logging.getLogger('db')

class DetectionView(viewsets.ModelViewSet):
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            print("detection", serializer.data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            db_logger.exception(status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_400_BAD_REQUEST)
