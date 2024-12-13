from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base.models import Workspace, Block
from .serializers import WorkspaceSerializer, BlockSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class BlockListView(APIView):
    pass
class WorkspaceDetailView(APIView):
    def get(self, request):
        workspace, created = Workspace.objects.get_or_create(user=request.user)
        serializer = WorkspaceSerializer(workspace)
        return Response(serializer.data)

class BlockListView(APIView):
    def post(self, request):
        workspace, created = Workspace.objects.get_or_create(user=request.user)
        data = request.data
        data['workspace'] = workspace.id  # Gắn workspace ID tự động
        serializer = BlockSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
