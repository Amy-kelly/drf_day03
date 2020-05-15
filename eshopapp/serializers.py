from rest_framework import serializers

from eshopapp.models import Orders, Product


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        #fields应该是序列化和反序列化的并集
        fields = ("pro_name", "price","pro_detail","pro_order")
        extra_kwargs = {
            "pro_name": {
                "required": True,
                "min_length": 3,
                "error_messages": {
                    "required": "商品名是必填的",
                    "min_length": "商品名长度不够"
                },
            "price":{
                "write_only":True
            },
             "pro_detail":{
                 "read_only":True
             },
             "pro_order":{
                 "read_only":True
             }
            }
        }
    def validate_pro_name(self,value):
        if "咖啡" in value:
            raise serializers.ValidationError("此商品已存在")
        else:
            return value
