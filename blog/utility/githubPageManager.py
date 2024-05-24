from github import Github
import base64
from .config import Configurations

class GithubPageManager:

    def __init__(self) -> None:
        self.git=Github(Configurations.GIT_TOKEN)
        self.user=self.git.get_user()

    def create_repo(self,repo_name):
        self.user.create_repo(repo_name)
    
    def upload_file(self,fileContent,filename,repo_name):
        repo = self.git.get_repo("1-blog/"+repo_name)
        repo.create_file(
            path=filename,
            message='uploaded '+filename,
            content=fileContent,
        )
        default_branch=repo.get_branch(repo.default_branch)
        repo.create_git_ref(ref='refs/heads/gh-pages',sha=default_branch.commit.sha)

    def read_file(self,repo_name,filename):
        repo = self.git.get_repo("1-blog/"+repo_name)
        bcontent=repo.get_contents(filename,ref='gh-pages')
        content=bcontent.decoded_content.decode()
        return content

    def update_content(self,fileContent,filename,repo_name):
        repo = self.git.get_repo("1-blog/"+repo_name)
        file=repo.get_contents(filename,ref='gh-pages')
        repo.update_file(
            path=filename,
            message='updating'+filename,
            content=fileContent,
            sha=file.sha,
            branch='gh-pages'
        )

    def delete_file():
        pass

    def delete_repo(self,repo_name):
        repo = self.git.get_repo("1-blog/"+repo_name)
        repo.delete()
