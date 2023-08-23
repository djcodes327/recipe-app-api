"""
Views for the User API.
"""
# rest_framework handles a lot of the logic that we need to create objects in
# the database. It does that by providing different base classes that we can
# configure for our views that will handle the base request in a standardized
# way. We can also override some of that behaviour.
from rest_framework import generics, authentication, permissions
# rest_framework by default provides us with a View that helps us with AuthToken handling
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer


# The CreateAPIView base class from generics handles HTTP post requests
# designed for creating objects. You just need to tell it which Serializer
# to use. It knows which model to create the new object in because the model
# is defined in the serializer.
class CreateUserView(generics.CreateAPIView):
    """Create a New User in the System."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    # The authentication classes (TokenAuthentication in this case) validate the user's
    # credentials and authenticate them if the credentials are correct.
    authentication_classes = [authentication.TokenAuthentication]
    # The permission classes (IsAuthenticated in this case) check whether the
    # authenticated user has the necessary permissions to access the view.
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        # For a GET request, the get_object method is called, which returns the authenticated user's object.
        # In this case, the authenticated user's information is returned in the response.
        return self.request.user
