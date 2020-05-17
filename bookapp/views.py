from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from bookapp import serializers
from bookapp.models import Book


class BookAPIView(APIView):
    def get(self,request,*args,**kwargs):
        book_id = kwargs.get("id")
        if book_id:
            try:
                book_obj = Book.objects.get(pk=book_id)
                book_ser = serializers.BookModelSerializer(book_obj).data
                return Response({
                    "status":200,
                    "message":"查询图书成功",
                    "results":book_ser
                })
            except:
                return Response({
                    "status":404,
                    "message":"所查询的图书不存在"
                })
        else:
            book_list = Book.objects.all()
            book_data = serializers.BookModelSerializer(book_list,many=True).data
            return Response({
                "status": 200,
                "message": "查询图书成功",
                "results": book_data
            })
    def post(self,request,*args,**kwargs):
        request_data = request.data
        book_ser = serializers.BookModelDeSerializer(data=request_data)
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()
        return Response({
            "status":200,
            "message":"图书信息添加成功",
            "results":serializers.BookModelSerializer(book_obj).data
        })

#查询单个，多个；增加单个，多个；删除多个，单个；整体更新单个，局部个更新单个
class BookAPIView2(APIView):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            try:
                book_obj = Book.objects.get(pk=book_id, is_delete=False)
                book_ser = serializers.BookModelSerializerV2(book_obj).data
                return Response({
                    "status": 200,
                    "message": "查询图书成功",
                    "results": book_ser
                })
            except:
                return Response({
                    "status": 200,
                    "message": "查询图书不存在",
                })
        else:
            book_list = Book.objects.filter(is_delete=False)
            book_data = serializers.BookModelSerializerV2(book_list, many=True).data
            return Response({
                "status": 200,
                "message": "查询图书列表成功",
                "results": book_data
            })
    def post(self, request, *args, **kwargs):
        """
        单增：传的数据是与model类对应的一个字典
        群增：[ {} {} {} ]  群增的时候可以传递列表里面嵌套与model类对应的多个字典来完成群增
        """
        request_data = request.data
        if isinstance(request_data, dict):
            # 代表单增
            many = False
        elif isinstance(request_data, list):
            # 代表群增
            many = True
        else:
            return Response({
                "status": 200,
                "message": "数据格式有误",
            })
        # 反序列化的时候需要将参数赋值关键字 data
        book_ser = serializers.BookModelSerializerV2(data=request_data, many=many)
        # 校验数据是否合法
        # raise_exception=True: 当校验失败的时候，马上终止当前视图方法，抛出异常到前台
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()
        return Response({
            "status": 200,
            "message": "success",
            "results": serializers.BookModelSerializerV2(book_obj, many=many).data
        })

    def delete(self,request,*args,**kwargs):
        book_id = kwargs.get("id")
        if book_id:
            ids = [book_id]
        else:
            ids = request.data.get('ids')
        res = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
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
        book_id = kwargs.get("id")
        try:
            book_obj = Book.objects.get(pk=book_id, is_delete=False)
        except:
            return Response({
                "status": 500,
                "message": "图书不存在",
            })
        book_ser = serializers.BookModelSerializerV2(data=request_data, instance=book_obj, partial=False)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return Response({
            "status":200,
            "message":"更新图书成功",
            "results":serializers.BookModelSerializerV2(book_obj).data
        })

    # def patch(self,request,*args,**kwargs):
    #     request_data = request.data
    #     book_id = kwargs.get("id")
    #     try:
    #         book_obj = Book.objects.get(pk=book_id, is_delete=False)
    #     except:
    #         return Response({
    #             "status": 500,
    #             "message": "图书不存在",
    #         })
    #     book_ser = serializers.BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
    #     book_ser.is_valid(raise_exception=True)
    #     book_ser.save()
    #     return Response({
    #         "status": 200,
    #         "message": "更新图书成功",
    #         "results": serializers.BookModelSerializerV2(book_obj).data
    #     })

    def patch(self,request,*args,**kwargs):
        request_data = request.data
        book_id = kwargs.get("id")
        if book_id and isinstance(request_data,dict):
            book_ids = [book_id,]
            request_data = [request_data,]
        elif not book_id and isinstance(request_data,list):
            book_ids = []
            for dic in request_data:
                pk = dic.pop("pk",None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status":500,
                        "message":"ID不存在"
                    })
        else:
            return Response({
                "status":500,
                "message":"数据不存在或格式有误"
            })
        book_list = []
        new_data = []
        for index,pk in enumerate(book_ids):
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
                new_data.append(request_data[index])
            except:
                continue
        book_ser = serializers.BookModelSerializerV2(data=new_data, instance=book_list, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return Response({
            "status":200,
            "message":"更新成功",
            "results":serializers.BookModelSerializerV2(book_list, many=True).data
        })