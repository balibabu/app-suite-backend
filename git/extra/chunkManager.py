from git.models import  Chunk
from .githubManager import GithubManager
from .repoSizeManager import RepoSizeManager
import time

class ChunkManager:
    def __init__(self,username) -> None:
        self.git=GithubManager(username)

    def upload(self, chunk, fileId):
        repo=RepoSizeManager.get_free_repo()
        uname=str(int(time.time()))
        self.git.upload_file(chunk,uname,repo)
        chunkObject=Chunk.objects.create(fileId=fileId,repo=repo,uname=uname,size=len(chunk))
        RepoSizeManager.add_size(repo,len(chunk))
        return chunkObject

    def delete(self,id):
        chunk=Chunk.objects.get(id=id)
        self.git.delete_file(chunk.uname,chunk.repo)
        RepoSizeManager.remove_size(chunk.repo, chunk.size)
        chunk.delete()

    def download(self,id):
        chunk=Chunk.objects.get(id=id)
        chunkContent=self.git.download_file(chunk.uname,chunk.repo)
        return chunkContent
