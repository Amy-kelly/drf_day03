from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from eshopapp import serializers
from eshopapp.models import Product


class ProductAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pro_id = kwargs.get("id")
        if pro_id:
            try:
                pro_obj = Product.objects.get(pk=pro_id, is_delete=False)
                pro_ser = serializers.ProductModelSerializer(pro_obj).data
                return Response({
                    "status": 200,
                    "message": "查询商品成功",
                    "results": pro_ser
                })
            except:
                return Response({
                    "status": 200,
                    "message": "查询商品不存在",
                })
        else:
            pro_list = Product.objects.filter(is_delete=False)
            pro_data = serializers.ProductModelSerializer(pro_list, many=True).data
            return Response({
                "status": 200,
                "message": "查询商品列表成功",
                "results": pro_data
            })
    def post(self, request, *args, **kwargs):
        request_data = request.data
        if isinstance(request_data, dict):
            many = False
        elif isinstance(request_data, list):
            many = True
        else:
            return Response({
                "status": 200,
                "message": "数据格式有误",
            })
        pro_ser = serializers.ProductModelSerializer(data=request_data, many=many)
        pro_ser.is_valid(raise_exception=True)
        pro_obj = pro_ser.save()
        return Response({
            "status": 200,
            "message": "success",
            "results": serializers.ProductModelSerializer(pro_obj, many=many).data
        })

    def delete(self,request,*args,**kwargs):
        pro_id = kwargs.get("id")
        if pro_id:
            ids = [pro_id]
        else:
            ids = request.data.get('ids')
        res = Product.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if res:
            return Response({
                "status": 200,
                "message": "删除成功",
            })

        return Response({
            "status": 500,
            "message": "删除失败或者已删除",
        })
    def put(self,request,*args,**kwargs):
        request_data = request.data
        pro_id = kwargs.get("id")
        try:
            pro_obj = Product.objects.get(pk=pro_id, is_delete=False)
        except:
            return Response({
                "status": 500,
                "message": "商品不存在",
            })
        pro_ser = serializers.ProductModelSerializer(data=request_data, instance=pro_obj, partial=False)
        pro_ser.is_valid(raise_exception=True)
        pro_ser.save()
        return Response({
            "status":200,
            "message":"更新商品成功",
            "results":serializers.ProductModelSerializer(pro_obj).data
        })

    def patch(self,request,*args,**kwargs):
        request_data = request.data
        pro_id = kwargs.get("id")
        try:
            pro_obj = Product.objects.get(pk=pro_id, is_delete=False)
        except:
            return Response({
                "status": 500,
                "message": "商品不存在",
            })
        pro_ser = serializers.ProductModelSerializer(data=request_data, instance=pro_obj, partial=True)
        pro_ser.is_valid(raise_exception=True)
        pro_ser.save()
        return Response({
            "status": 200,
            "message": "更新商品成功",
            "results": serializers.ProductModelSerializer(pro_obj).data
        })