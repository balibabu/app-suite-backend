from git.models import FileId, Chunk
from .githubManager import GithubManager
from .repoSizeManager import RepoSizeManager
from django.db import transaction
import time

class FileManager:

    def __init__(self,username) -> None:
        self.git=GithubManager(username)
    
    def upload(self, chunks):
        fileId = None
        with transaction.atomic():
            fileId = FileId.objects.create()
            for chunk in chunks:
                repo=RepoSizeManager.get_free_repo()
                uname=str(time.time()).replace('.','')
                self.git.upload_file(chunk,uname,repo)
                Chunk.objects.create(fileId=fileId,repo=repo,uname=uname,size=len(chunk))
                RepoSizeManager.add_size(repo,len(chunk))
        return fileId

    def delete(self,fileId):
        chunks=Chunk.objects.filter(fileId=fileId)
        for chunk in chunks:
            self.git.delete_file(chunk.uname,chunk.repo)
            RepoSizeManager.remove_size(chunk.repo, chunk.size)
        fileId.delete()

    def download(self,fileId):
        fileContent=b''
        chunks=Chunk.objects.filter(fileId=fileId) #assuming chunks are sorted by id
        for chunk in chunks:
            fileContent+=self.git.download_file(chunk.uname,chunk.repo)
        return fileContent
        
        
