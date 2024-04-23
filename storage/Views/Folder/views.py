from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from storage.serializers import FolderSerializer
from storage.models import Folder

class FolderListCreateView(generics.ListCreateAPIView):
    serializer_class=FolderSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FolderUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=FolderSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)
