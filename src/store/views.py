# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Box
from .serializers import BoxSerializer

class BoxAPIView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        boxes = Box.objects.filter(created_by = request.user.id)
        # boxes = Box.objects.all()
        serializer = BoxSerializer(boxes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'length': request.data.get('length'),
            'width': request.data.get('width'),
            'height': request.data.get('height'),
            'created_by': request.user.id,
            'updated_by' : request.user.id
        }
        serializer = BoxSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)