from rest_framework import serializers
from .models  import Workspaces, Membership,WorkspaceInvites,ActivityLog
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
        
        # Log workspace creation
        ActivityLog.objects.create(
            workspace=workspace,
            user=user,
            action=ActivityLog.ACTION_WORKSPACE_CREATED,
        )
        
        return workspace

class WorkspaceInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model=WorkspaceInvites
        fields=['id','email','role','created_at']
        read_only_fields=['id','created_at']
#self → the serializer instance (so you can access context, request, etc.).

    def validate(self,attrs):
#attrs → the dictionary of cleaned data from the request that you’re checking before saving.
          # Get workspace from the view's kwargs through context
          request = self.context['request']
          workspace_id = self.context['view'].kwargs['workspace_id']
          workspace = Workspaces.objects.get(id=workspace_id)
          email =attrs['email']
#attrs is a dictionary of the data being validated.
#validate (serializer method)
#Purpose: enforce business rules before saving.
          if Membership.objects.filter(
            workspace =workspace,
            user__email=email
          ).exists():
            raise serializers.ValidationError("Your are already a member")
          return attrs
#Think: “Is this data allowed? Should I reject it before it touches the database?”

#Example:

#Prevent inviting someone who is already a member.

#Prevent inviting yourself.

#Prevent duplicate invites
# (extra check beyond unique_together).
class ActivityLogSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = ActivityLog
        fields = [
            "id",
            "action",
            "user_email",
            "metadata",
            "created_at",
        ]
