#from  rest_framework import serializers
#from  django.contrib.auth.password_validation import  validate_password
#from .models import  User
from   rest_framework   import serializers
from django.contrib.auth.password_validation import validate_password  
from .models import User
#from  rest_framework import  serializers
#from django.contrib.auth.password_validation import validate_password
#convert Python objects → JSON
#from .models   import  User
#convert JSON → Python objects

#validate incoming data

#control what fields are exposed to the API

class  RegisterSerializers(serializers.ModelSerializer):

    password = serializers.CharField(write_only =True,required = True,validators = [validate_password])
    password2 = serializers.CharField(write_only =True,required =True )
    class Meta:
        model = User
        fields  =("id", "email", "username", "full_name", "password", "password2")

    def validate(self, attrs):
    # When DRF creates your serializer, it does:
    # serializer = RegisterSerializer(data=request.data)
    # self refers to that serializer instance
    # attrs = a dictionary of validated input data
    # json
    # {
    #     "email": "a@a.com",
    #     "password": "123",
    #     "password2": "123"
    # }
    # Then inside validate(self, attrs):
    # python
    # attrs = {
    #     "email": "a@a.com",
    #     "password": "123",
    #     "password2": "123"
    # }
     if attrs['password'] != attrs['password2']:
        raise serializers.ValidationError('didnot matched')
     return attrs

   # def create(self, validated_data):
      #create is a special method DRF looks for.
      #validated_data.pop("password2", None)
      #validated_data is a dictionary containing all the cleaned, validated input.
        #password  two is  not part of the User  model  cause it's  just  a  simple  confirm password so  clearning it

     # password = validated_data.pop("password")
      #deleting password from  the  dictonary as well cause  i can give  raw  data  to model

      #user = User(**validated_data)
      #“Take each key/value in the dictionary and pass it as arguments.”
      #user = User(
   # email="test@gmail.com",
   # username="john",
   # full_name="John Doe"
#)

     # user.set_password(password)
     # user.save()
     # return user
    #Django REST Framework needs to know how to create the User object.

#The default behavior would try to save the password as plain text, which is unsafe.

    def create(self,validated_data):
       validated_data.pop('password2',None)
       password=validated_data.pop('password')
       user  =User(**validated_data)
       user.set_password('password')
       user.save()
   
   

class Userserializer(serializers.ModelSerializer):
       class Meta:
        model = User
        fields = ("id", "email", "username", "full_name", "avatar_url")
        read_only_fields = ("id", "email")




#class RegisterSerializers(serializers.ModelSerializer):
    #self is the serializer instance.
    #This serializer is used when a new user signs up.
    #password =serializers.CharField(write_only = True ,  required = True , validators  = [validate_password])
    #write_only=True → API accepts password but never returns it
    #password2 = serializers.CharField(write_only=True,  required =True)
    #This is the “confirm password” field.
    #class Meta:
     #   model  = User
    #    fields = ("id", "email", "username", "full_name", "password", "password2")
    #    read_only_fields = ("id",)
#self lets you access:

#serializer fields

#serializer context

#serializer methods

#anything inside the class
   # def   validate(self, attrs):
    #    if  attrs.get(password)
#attrs is a dictionary of all the validated input data that the user sent.