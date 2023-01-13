from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
# from accounts.forms import RegistrationForm, AccountAuthForm
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response(token.key, status=status.HTTP_200_OK)

# def register_view(request, *args, **kwargs):
#     user = request.user
#     if user.is_authenticated:
#         return HttpResponse("You are already authenticated as " + str(user.email))
#
#     context = {}
#     if request.POST:
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username').lower()
#             raw_password = form.cleaned_data.get('password1')
#             accounts = authenticate(username=username, password=raw_password)
#             token = Token.objects.create(user=accounts)
#             print(token.key)
#             login(request, accounts)
#             # destination = kwargs.get("next")
#             destination = get_redirect_if_exists(request)
#             if destination:  # if destination != None
#                 return redirect(destination)
#             return redirect('home')
#         else:
#             context['registration_form'] = form
#     else:
#         form = RegistrationForm()
#         context['registration_form'] = form
#
#     return render(request, 'accounts/register.html', context)
#
#
# def logout_view(request):
#     logout(request)
#     return redirect("home")
#
#
# def login_view(request, *args, **kwargs):
#     context = {}
#
#     user = request.user
#     if user.is_authenticated:
#         return redirect("home")
#
#     destination = get_redirect_if_exists(request)
#     if request.POST:
#         form = AccountAuthForm(request.POST)
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(username=username, password=password)
#             token = Token.objects.get_or_create(user=user)
#             if user:
#                 login(request, user)
#                 if destination:
#                     return redirect(destination)
#                 return redirect("home")
#     else:
#         form = AccountAuthForm()
#
#     context['login_form'] = form
#
#     return render(request, "accounts/login.html", context)
#
#
# def get_redirect_if_exists(request):
#     redirect = None
#     if request.GET:
#         if request.GET.get("next"):
#             redirect = str(request.GET.get("next"))
#     return redirect
