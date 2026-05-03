from github import Github
import base64
from .config import Configurations
from .crypto import encrypt_chunk, decrypt_chunk, derive_chunk_key

class GithubManager:
    def __init__(self,username) -> None:
        self.git=Github(Configurations.GIT_TOKEN)
        self.username=username

    def upload_file(self,fileContent,filename,repo_name):
        repo = self.git.get_repo("storeage/"+repo_name)
        file_path_in_repo=f'{self.username}/{filename}'
        key = derive_chunk_key(Configurations.MASTER_KEY, repo_name, filename)
        enc=encrypt_chunk(fileContent, key)
        repo.create_file(
            path=file_path_in_repo,
            message='uploaded '+filename,
            content=enc,
        )

    def download_file(self,filename,repo_name):
        repo = self.git.get_repo("storeage/"+repo_name)
        file = repo.get_contents(f'{self.username}/{filename}')
        blob_content = repo.get_git_blob(file.sha).content
        content_bytes = base64.b64decode(blob_content)
        key = derive_chunk_key(Configurations.MASTER_KEY, repo_name, filename)
        return decrypt_chunk(content_bytes, key)

    def create_repo(self,repo_name):
        user=self.git.get_user()
        user.create_repo(repo_name,private=True)
    
    def delete_file(self,filename,repo_name):
        repo = self.git.get_repo("storeage/"+repo_name)
        file = repo.get_contents(f"{self.username}/{filename}")
        sha = file.sha
        repo._requester.requestJsonAndCheck(
            "DELETE",
            f"/repos/storeage/{repo_name}/contents/{self.username}/{filename}",
            input={
                "message": f"Delete {filename} completely",
                "sha": sha,
                "branch": 'main'
            }
        )
