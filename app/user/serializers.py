"""
Serializers for the User API View.
"""

from django.contrib.auth import get_user_model, authenticate
# Serializers model includes the tools we need for defining serializers.
# Serializers convert objects to and from python objects. They take
# 'adjacent' input from the API, validates it to make sure it is secure and
# adheres to validation rules, and then converts it into a python object or
# a model we can use in our database.
from rest_framework import serializers

# To get/use Django OTB translations feature.
from django.utils.translation import gettext as _


# ModelSerializer is a base class from the serializers module. It creates
# model serializers - which allow us to validate and save thing to a model
# defined in our serializer.
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User object."""

    # The Meta class tells the django rest framework the model, fields and
    # any additional arguments we want to pass to the serializer.
    class Meta:
        model = get_user_model()
        # The list of fields that we ant to make available through the serializer
        # they are created when we make a request to be saved in the model that is
        # created. We don't want to include things like is_active or is_staff
        # because when users create objects they should not set those values
        # themselves in the request. Only allow fields that you want the user to
        # be able to change using the API.
        fields = ['email', 'password', 'name']
        # Dict allowing us to provide extra meta-data to the fields e.g.
        # whether we want a field to be write-only/read-only. Write_only
        # means the user will be able to set the value but the value won't
        # be returned in the API response. So they can write values to password
        # but not read it.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # This method overrides the serializers behaviour when creating new
    # objects. The default behaviour to create an object with whatever
    # values are passed in. E.g. if you pass in the password field, by default
    # the serializer will save it as text in the model. We want it to
    # pass out password through encryption. We do so using the create_user
    # method we provided to our model manager.
    # We pass in the validated data from our serializer. The create() method
    # is only called when the validation is successful.
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        # This line extracts the value of the 'password' field from the validated_data dictionary if it exists.
        # It uses the pop method, which removes the 'password' key from the dictionary if it's present and assigns its value to the password variable.
        # If the 'password' key is not present in validated_data, the None value is assigned to password.
        password = validated_data.pop('password', None)
        # This line calls the update method of the parent class (which is serializers.ModelSerializer).
        # This method updates the fields of the provided instance (an existing user instance) with the data in validated_data.
        # The updated user instance is assigned to the user variable.
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        #  The user instance is returned from the update method, which represents the updated
        #  user with possible changes made to the password or other fields.
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the User Auth Token."""
    email = serializers.EmailField()
    # We have added Style an
    # input_type style to override the default text input type for Browsable API.
    # By default, django trims the input string so to avoid that we use trim_whitespace.
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    # Validate is called at validation level by our view from view
    # it is passed to serializer and from serializer to validator.
    # attrs are attributes that we get from the request.
    def validate(self, attrs):
        """Validate and authenticate the user request."""
        email = attrs.get('email')
        password = attrs.get('password')
        # We are passing 3 parameters here 1) Request which is a required field which is used
        # to validate the request and headers along with 2nd and 3rd parameters username and password.
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password,
        )

        # If provided credentials are incorrect.
        if not user:
            msg = _('Unable to authenticate with Provided Credentials')
            raise serializers.ValidationError(msg, code="Authorization")
        # else return the user.
        attrs['user'] = user
        return attrs
