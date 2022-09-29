# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Box
from .serializers import BoxSerializer
from django_filters import rest_framework as filters
from django_filters import FilterSet

# Defining Staff Permission


class IsStaffUser(permissions.BasePermission):
    """
    Allows access only to staff users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class BoxFilter(FilterSet):
    length_more_than = filters.NumberFilter(
        field_name="length", lookup_expr='gte')
    length_less_than = filters.NumberFilter(
        field_name="length", lookup_expr='lte')

    class Meta:
        model = Box
        fields = ['length']


class BoxesAPIView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated, IsStaffUser]
    filter_backends = (filters.DjangoFilterBackend)
    filterset_class = BoxFilter
    filterset_fields = ['length_more_than', 'length_less_than']

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the Boxes in the inventory
        '''
        # boxes = Box.objects.filter(created_by = request.user.id)
        boxes = Box.objects.all()
        serializer = BoxSerializer(boxes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Box with given dimensions
        '''
        data = {
            'length': request.data.get('length'),
            'width': request.data.get('width'),
            'height': request.data.get('height'),
            'created_by': request.user.id,
            'updated_by': request.user.id
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
            return Box.objects.get(id=box_id, created_by=user_id)
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
        serializer = BoxSerializer(
            instance=box_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, box_id, *args, **kwargs):
        '''
        Deletes the Box with the given box_id and the created_by id
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
