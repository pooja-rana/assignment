import os

import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render
from django.utils.encoding import DjangoUnicodeDecodeError
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserDetail
from .serializer import RegisterSerializer, LoginSerializer, SetNewPasswordSerializer, CustomPasswordResetSerializer
from ..assignment_project import settings


# Create your views here.


class RegistrationAPIView(generics.CreateAPIView):
    """Creates a new user in the system"""
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSerializer

    def patch(self, request, pk):
        try:
            user = UserDetail.objects.get(id=pk)
        except:
            return Response(f"User does not exists at id:{pk}")
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "success": "User updated successfully"
            })

        return Response({"errors": serializer.errors, "status": status.HTTP_400_BAD_REQUEST})


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetAPIView(generics.GenericAPIView):
    serializer_class = CustomPasswordResetSerializer

    def post(self, request):
        email = request.data["email"]
        if UserDetail.objects.filter(email=email).exists():
            user_id = UserDetail.objects.get(email=email).id
            current_site = get_domain(request)

            redirect_url = request.data.get("redirect_url", "")
            send_password_reset_email.delay(redirect_url, current_site, user_id)

        return Response({"success": "We have sent you a link to reset your password"}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = UserDetail.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url + "?token_valid=False")
                    # return Response({"error": "Token is not valid, please request a new one."}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return CustomRedirect(os.getenv('FE_URL', '') + '?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    redirect_url + '?token_valid=True&message=Credentials Valid&uidb64=' + uidb64 + '&token=' + token)
                # return Response({"success": True, "message": "Credentials valid", "uidb64": uidb64, "token": token}, status=status.HTTP_200_OK)
            else:
                return CustomRedirect(os.getenv('FE_URL', '') + '?token_valid=False')


        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return CustomRedirect(redirect_url + "?token_valid=False")


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success": True, "message": "Password Reset Sucesss"}, status=status.HTTP_200_OK)
