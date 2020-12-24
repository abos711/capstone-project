from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.activity import Activity
from ..serializers import ActivitySerializer, UserSerializer

# Create your views here.
class Activities(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = ActivitySerializer
    def get(self, request):
        """Index request"""
        # Get all the activities:
        # Activities = Activity.objects.all()
        # Filter the activitys by owner, so you can only see your owned activities
        activities = Activity.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = ActivitySerializer(activities, many=True).data
        return Response({ 'activities': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['activity']['owner'] = request.user.id
        # Serialize/create activity
        activity = ActivitySerializer(data=request.data['activity'])
        # If the activity data is valid according to our serializer...
        if activity.is_valid():
            # Save the created activity & send a response
            activity.save()
            return Response({ 'activity': activity.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(activity.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivityDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the activity to show
        activity = get_object_or_404(Activity, pk=pk)
        # Only want to show owned activitys?
        if not request.user.id == activity.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this activity')

        # Run the data through the serializer so it's formatted
        data = ActivitySerializer(activity).data
        return Response({ 'activity': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate activity to delete
        activity = get_object_or_404(Activity, pk=pk)
        # Check the activity's owner agains the user making this request
        if not request.user.id == activity.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this activity')
        # Only delete if the user owns the  activity
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['activity'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['activity'].get('owner', False):
            del request.data['activity']['owner']

        # Locate Mango
        # get_object_or_404 returns a object representation of our Mango
        activity = get_object_or_404(Activity, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == activity.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this activity')

        # Add owner to data object now that we know this user owns the resource
        request.data['activity']['owner'] = request.user.id
        # Validate updates with serializer
        data = ActivitySerializer(activity, data=request.data['activity'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
