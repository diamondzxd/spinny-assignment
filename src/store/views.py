# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Box
from .serializers import BoxSerializer

class BoxesAPIView(APIView):
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


class BoxDetailAPIView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_box(self, box_id, user_id):
        '''
        Helper method to get the box with given box_id and created_by id
        '''
        try:
            return Box.objects.get(id=box_id, created_by = user_id)
        except Box.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, box_id, *args, **kwargs):
        '''
        Retrieves the Box with given box_id
        '''
        box_instance = self.get_box(box_id, request.user.id)
        if not box_instance:
            return Response(
                {"res": "Box with the given id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BoxSerializer(box_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, box_id, *args, **kwargs):
        '''
        Updates the Box with updated Box properties if exists
        '''
        box_instance = self.get_object(box_id, request.user.id)
        if not box_instance:
            return Response(
                {"res": "Box with the given id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'length': request.data.get('length'),
            'width': request.data.get('width'),
            'height': request.data.get('height'), 
            'updated_by': request.user.id
        }
        serializer = BoxSerializer(instance = box_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, box_id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        box_instance = self.get_object(box_id, request.user.id)
        if not box_instance:
            return Response(
                {"res": "Box with the given id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        box_instance.delete()
        return Response(
            {"res": "Box deleted!"},
            status=status.HTTP_200_OK
        )