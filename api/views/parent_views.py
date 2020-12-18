from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..models.parent import Parent
from ..serializers import ParentSerializer

# Create your views here.
class Parents(APIView):
    def get(self, request):
        """Index Request"""
        print(request.session)
        parents = Parent.objects.all()[:10]
        data = ParentSerializer(parents, many=True).data
        return Response(data)

    serializer_class = ParentSerializer
    def post(self, request):
        """Post request"""
        print(request.data)
        parent = ParentSerializer(data=request.data['parent'])
        if parent.is_valid():
            create = parent.save()
            return Response(parent.data, status=status.HTTP_201_CREATED)
        else:
            return Response(parent.errors, status=status.HTTP_400_BAD_REQUEST)

class ParentDetail(APIView):
    def get(self, request, pk):
        """Show request"""
        parent = get_object_or_404(Parent, pk=pk)
        data = ParentSerializer(parent).data
        return Response(data)

    def patch(self, request, pk):
        """Update Request"""
        parent = get_object_or_404(Parent, pk=pk)
        uopdate = ParentSerializer(parent, data=request.data['parent'])
        if update.is_valid():
            update.save()
            return Response(ms.data)
        return Response(ms.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete Request"""
        parent = get_object_or_404(Parent, pk=pk)
        parent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
