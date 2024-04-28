from rest_framework import serializers
from .models import Folder, File, SharedFile

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Folder
        fields=['id','title','inside']
        read_only_fields = ['user']
        
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id','title','size', 'timestamp','inside']
        read_only_fields = ['user', 'fileId']

class SharedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model=SharedFile
        fields = '__all__'
        read_only_fields = ['sharedWith','file']
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     file_instance = instance.file
    #     representation = {
    #         'id': file_instance.id,
    #         'title': file_instance.title,
    #         'size': file_instance.size,
    #         'timestamp': file_instance.timestamp,
    #         'inside': file_instance.inside.id if file_instance.inside else None,
    #         'user': file_instance.user.username,
    #         'anyoneKey': instance.anyoneKey,
    #         'sharedId':instance.id

    #     }
    #     return representation
