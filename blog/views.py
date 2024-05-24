from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from blog.utility.githubPageManager import GithubPageManager
from .models import Blog


@api_view(['GET'])
def getBlogs(request):
    blogs=Blog.objects.all()
    blogList=[]
    for blog in blogs:
        blogList.append({'id':blog.id,'author':blog.user.username,'description':blog.description,'repo':blog.reponame})
    return Response(blogList)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createBlog(request):
    user=request.user
    indexFile=request.data.get('index')
    reponame=request.data.get('reponame')
    description=request.data.get('description')
    if(reponame and indexFile):
        mng=GithubPageManager()
        mng.create_repo(reponame)
        mng.upload_file(indexFile,'index.html',reponame)
        obj=Blog.objects.create(
            user=user,
            reponame=reponame,
            description=description
        )
        return Response({
            'id':obj.id,
            'repo':reponame,
            'description':description,
            'author':user.username,
        })
    return Response({'message':'please provide all the required fields value'},status=400)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def readBlog(request,id):
    user = request.user
    blog=Blog.objects.get(user=user, id=id)
    mng=GithubPageManager()
    content=mng.read_file(blog.reponame,'index.html')
    return Response(content)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateBlog(request,id):
    user = request.user
    blog=Blog.objects.get(user=user, id=id)
    indexFile=request.data.get('index')
    description=request.data.get('description')
    blog.description=description
    blog.save()
    mng=GithubPageManager()
    mng.update_content(indexFile,'index.html',blog.reponame)
    return Response(status=200)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteBlog(request,id):
    user = request.user
    blog=Blog.objects.get(user=user, id=id)
    mng=GithubPageManager()
    mng.delete_repo(blog.reponame)
    blog.delete()
    return Response(status=200)


    
