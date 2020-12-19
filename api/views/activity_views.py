from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..models.activity import Activity
from ..serializers import ActivitySerializer

# Create your views here.
class Activities(APIView):
    def get(self, request):
        """Index Request"""
        print(request)
        activities = Activity.objects.all()[:10]
        data = ActivitySerializer(activities, many=True).data
        return Response(data)

    serializer_class = ActivitySerializer
    def post(self, request):
        """Post request"""
        print(request.data)
        activity = ActivitySerializer(data=request.data['activity'])
        if activity.is_valid():
            a = activity.save()
            return Response(activity.data, status=status.HTTP_201_CREATED)
        else:
            return Response(activity.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivityDetail(APIView):
    def get(self, request, pk):
        """Show request"""
        activity = get_object_or_404(Activity, pk=pk)
        data = ActivityLogSerializer(activity).data
        return Response(data)

    def patch(self, request, pk):
        """Update Request"""
        activity = get_object_or_404(Activity, pk=pk)
        ms = ActivitySerializer(activity, data=request.data['activity'], partial=True)
        if ms.is_valid():
            ms.save()
            return Response(ms.data)
        return Response(ms.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete Request"""
        activity = get_object_or_404(Activity, pk=pk)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
