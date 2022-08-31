from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserDetail
from .serializer import RegisterSerializer, LoginSerializer


# Create your views here.


class RegistrationAPIView(generics.CreateAPIView):
    """Creates a new user in the system"""

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
    permission_classes = (IsAuthenticated,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
