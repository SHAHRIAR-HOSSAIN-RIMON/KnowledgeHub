from rest_framework import serializers
from .models  import Workspaces, Membership
from django.contrib.auth import get_user_model

User =get_user_model()
## Connects to the active User model in Django's auth system (default or custom)
class  MembershipSerializer(serializers.ModelSerializer):
        class Meta:
            model =Membership
            fields  =[
                'id',
                'user_id',
                'email',
                'username',
                'role',
                'joined_at',
            ]
        user_id = serializers.UUIDField(source="user.id", read_only=True)
        email = serializers.EmailField(source="user.email", read_only=True)
        username = serializers.CharField(source="user.username", read_only=True)
#this   are  wrote in such  a way cause  this werern't part of the  Membership model 
class WorkspaceSerializer(serializers.ModelSerializer):
    owner_id = serializers.UUIDField(source="owner.id", read_only=True)

    members=MembershipSerializer(
        source ='memberships',
        many  =True,
        read_only=True
    )
   #cause i want  my frontend  to see all  the members on  the worksapce

    class  Meta:
        model=Workspaces
        fields=['id','name','description','owner_id','created_at','members']
  
    

class WorkspaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  =Workspaces
        fields=['id','name','description']
        read_only_fields=['id']
#when   want to save  new data  drf  calledmethod create

    def  create(self,validated_data):
        request = self.context['request']
        user = request.user
        workspace = Workspaces.objects.create(
            owner=user,
            **validated_data
        )

        # Auto-create OWNER membership
        Membership.objects.create(
            user=user,
            workspace=workspace,
            role=Membership.ROLE_OWNER
        )
        return workspace
