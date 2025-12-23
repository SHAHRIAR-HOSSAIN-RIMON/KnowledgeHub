from rest_framework  import serializers
from .models import  FileAsset

class FileUploadSerializer(serializers.ModelSerializer):
    class  Meta:
        model=FileAsset

        fields=['id','file']
    def create(self,validated_data):
        file = validated_data['file']
    #“Grab the uploaded file from validated_data.”

        user=self.context['request'].user
        #“Get the current user from request context.”
        workspace=self.context['workspace']
        #“Get the workspace from serializer context (passed in by the view).


        return  FileAsset.objects.create(
#self.request.user → comes directly from the HTTP request object; always available in views and serializers if you pass the request in. It tells you who is making the request.

#self.context[...] → is a dictionary you manually pass extra data into when instantiating a serializer (like workspace); it’s for custom values the serializer wouldn’t know on its own.

#👉# In short: use self.request.user for the current user, and use self.context[...] when you need to inject extra info (like workspace) that isn’t part of the request object.
            workspace=workspace,
            file=file ,
            filename=file.name,
            file_size=file.size,
            file_type=file.content_type,
            uploaded_by=user
#These are provided by Django’s UploadedFile object. I can store them directly in the model.

        )


#If you expose them as writable fields, the client could lie:

#Send filename="secret.docx" while the actual file is report.pdf.

#Claim file_size=100 KB when the file is actually 5 MB.

#Fake mime_type="image/png" for a .exe file.

#tha't  why  in the using create which gonna extract data from  the   uplaodedfile
    