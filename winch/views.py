from rest_framework import status
from rest_framework.views import APIView  # 직접 코딩 해야하는 클래스
from rest_framework import viewsets  # get, post, put, delete를 코딩하지 않아도 자동적으로 처리해주는 클래스
from drf_yasg.utils import swagger_auto_schema
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# Create your views here.
class WinchViewSet(viewsets.ModelViewSet):
    # # authentication 추가
    # authentication_classes = [BasicAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Winch.objects.all()
    serializer_class = WinchSerializer


class WinchDataLogViewSet(viewsets.ModelViewSet):
    queryset = WinchDataLog.objects.all()
    serializer_class = WinchDataLogSerializer


class WinchListAPIView(APIView):
    """
    GET
    """

    @swagger_auto_schema(tags=['윈치 데이터 로드'])
    def get(self, request):
        serializer = WinchSerializer(Winch.objects.all(), many=True)
        return Response(serializer.data)
        # winch_list = Winch.objects.all()
        # paginator = PageNumberPagination()
        #
        # # 페이지 사이즈를 주면 해당 사이즈로 지정
        # # 값이 없으면 기본 사이즈로 설정(settings.py안에)
        # page_size = request.GET.get('size')  # request.GET['size']를 써도 되지만 size가 없다면 에러를 발생시킴
        # if not page_size is None:  # request.GET.get('size')로 작성시 size가 없으면 None을 반환
        #     paginator.page_size = page_size
        #
        # result = paginator.paginate_queryset(winch_list, request)
        # serializers = WinchSerializer(result, many=True)
        # return paginator.get_paginated_response(serializers.data)

    """
    POST
    """

    # request_body는 해당 serializer에서 설정한 내용을 swagger에서 보이고 Try it out 버튼으로 보낼 수 있게 해줌.
    @swagger_auto_schema(tags=['윈치 데이터 생성'], request_body=WinchSerializer)
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            # print("윈치 데이터 : ", request.data)
            Winch.objects.create(
                serial_number=data['serial_number'],
                primary_sensor=data['primary_sensor'],
                extended_sensor=data['extended_sensor'],
                tetherline_length=data['tetherline_length'],
                tetherline_limit_tension=data['tetherline_limit_tension'],
                production_year=data['production_year']
            )

            return JsonResponse({'message': 'CREATE_SUCCESS'}, status=201)

        except Winch.DoesNotExist:
            return JsonResponse({'message': 'TASK_DOES_NOT_EXIST'}, status=400)


class WinchDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Winch, pk=pk)

    """
    GET 
    """

    @swagger_auto_schema(tags=['윈치 데이터 검색'])
    def get(self, request, pk, format=None):
        winch = self.get_object(pk)
        serializer = WinchSerializer(winch)
        return Response(serializer.data)

    """
    PUT 
    """

    @swagger_auto_schema(tags=['윈치 데이터 수정'])
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = WinchSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    DELETE
    """

    @swagger_auto_schema(tags=['윈치 데이터 삭제'])
    def delete(self, request, pk):
        winch = self.get_object(pk)
        winch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
