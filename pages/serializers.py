from  rest_framework import   serializers
from .models  import  Page,PageVersion

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"
        read_only_fields = [
            'id',
            'created_by',
            'updated_by',
            'created_at',
            'updated_at',
            'is_deleted',
        ]

class PageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['title', 'content', 'parent']
        
class PageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'workspace', 'title', 'content', 'parent']
        read_only_fields = ['id']

class PageTreeSerializer(serializers.ModelSerializer):
    children=serializers.SerializerMethodField()
    #“this field doesn’t exist in the model, compute it with a method.”
    class Meta:
        model=Page 
        fields=['id','title','children']

    def get_children(self,obj):
        children=obj.children.filter(is_deleted=False)
        return  PageTreeSerializer(children,many=True).data


#
class PageVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageVersion
        fields = ["id", "page", "title", "content", "created_by", "created_at"]
        read_only_fields = ["id", "created_by", "created_at"]
