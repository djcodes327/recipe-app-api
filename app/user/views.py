"""
Views for the User API.
"""
from rest_framework import generics
from user.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    """Create a New User in the System."""
    serializer_class = UserSerializer
