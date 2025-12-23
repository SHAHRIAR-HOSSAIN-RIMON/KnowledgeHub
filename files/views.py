from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.response import Response
from workspaces.models import Workspaces
from .serializers import FileUploadSerializer
from .models import FileAttachment,FileAsset
from  pages.models import  Page
class FileUploadView(generics.CreateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=FileUploadSerializer

    def get_serializer_context(self):
#Override to inject workspace into serializer context.
#When the serializer needs extra data that isn’t part of the request body
        
#Can the serializer build the model instance with only what the client sends in the request body?”

#If yes → no extra context needed.
        context=super().get_serializer_context()
        workspace = Workspaces.objects.get(id=self.kwargs['workspace_id'])
        context['workspace']=workspace
        return context
#What it is:  
#This calls the parent class’s get_serializer_context() method.

#Why:  
#DRF automatically builds a default context dictionary with things like:

#"request" → the current HTTP request object
#This line fetches the actual Workspace object based on the ID in the URL

#"format" → the response format (json, etc.)

#"view" → the view instance itself
#Example: if your URL is /workspaces/5/files/, then self.kwargs["workspace_id"] = 5.

#So: You start with that default context, then add your own keys (like "workspace") before returning it.

#If no → you must pass extra data via context.
# Create your views here.




#attaching the file t o the  page

class  AttachFileToPageView(generics.CreateAPIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):
        #👉 Use when you don’t know how many named values will be passed.
#*args → collects any extra positional arguments into a tuple.
#**kwargs → collects any extra keyword arguments into a dictionary.
#👉 Use when you don’t know how many named values will be passed.
#*args extra  position  argument  
#which  means  when you don't know how many parameters  gonna be passed
         page=Page.objects.get(id=kwargs['page_id'])
         file_id = request.data.get('file_id')
         file_asset=FileAsset.objects.get(id=file_id)

         FileAttachment.objects.create(
             page=page,
             file_asset=file_asset 
         )
         return Response({'status':'attached'})