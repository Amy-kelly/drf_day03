from rest_framework import serializers

from bookapp.models import Book, Press


class PressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ("press_name","address","id")

class BookModelSerializer(serializers.ModelSerializer):
    press_address = serializers.SerializerMethodField()
    def get_press_address(self,obj):
        return obj.publish.address
    class Meta:
        model = Book
        #指定要序列化的字段,自定义字段在model类中写
        fields = ("book_name","price","pic","publish_name","press_address","author_list","publish")
        #序列化所有字段
        # fields = "__all__"
        #指定不序列化的字段
        # exclude = ("is_delete","status","id")
        #展示关联表的深度关系
        depth = 1

class BookModelDeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        #指定进行反序列化的字段
        fields = ("book_name","price","authors","publish")
        #添加系统校验规则
        extra_kwargs = {
            "book_name":{
                "required":True,
                "min_length":3,
                "error_messages":{
                    "required": "图书名是必填字段",
                    "min_length": "图书名长度不够"
                }
            }
        }
        #局部钩子  自己添加的额外的局部规则
        def validate_book_name(self,value):
            if "python" in value:
                return serializers.ValidationError("此图书已存在")
            return value
        #全局钩子
        def validate(self,attrs):
            print(self,"self")
            print(attrs,type(attrs),"attrs")
            publish = attrs.get("publish")
            book_name = attrs.get("book_name")
            book_obj = Book.objects.filter(book_name=book_name,publish=publish)
            if book_obj:
                raise serializers.ValidationError("该出版社出版过此图书")
            return attrs

class BookModelSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Book
        #fields应该是序列化和反序列化的并集
        fields = ("book_name", "price", "pic", "authors", "publish", "author_list", "publish_name",)
        extra_kwargs = {
            "book_name":{
                "required":True,
                "min_length":5,
                "error_messages":{
                    "required": "图书名是必填的",
                    "min_length": "图书名长度不够"
                }
            },
            "authors":{
                "write_only":True  #只参与反序列化
            },
            "publish":{
                "write_only":True
            },
            "author_list":{
                "read_only":True  #序列化
            },
            "publish_name":{
                "read_only":True
            },
            "pic":{
                "read_only":True
            }
        }
    def validate_book_name(self,value):
        if "python" in value:
            raise serializers.ValidationError("此图书已存在")
        else:
            return value
    def validate(self, attrs):
        publish = attrs.get("publish")
        book_name = attrs.get("book_name")
        # 一个出版社只能不能发布重复的书籍名
        book_obj = Book.objects.filter(book_name=book_name, publish=publish)
        if book_obj:
            raise serializers.ValidationError("该出版社已经发布过该图书")
        return attrs

