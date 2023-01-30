from rest_framework import status
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response


# Create your views here.
class HelikiteViewSet(viewsets.ModelViewSet):
    queryset = Helikite.objects.all()
    serializer_class = HelikiteSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("헬리카이트", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        print(request.user)
        print(request.auth)

        return Response(status=status.HTTP_200_OK)