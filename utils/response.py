from rest_framework.response import Response
class MyResponse(Response):
    def __init__(self, data_status=100, data_message=0, results=None, http_status=None, headers=None, exception=False,
                 **kwargs):
        # 返回数据的初始状态
        data = {
            "status": data_status,
            "message": data_message
        }
        # 判断result是否有结果
        if results is not None:
            data['results'] = results
        # 如果有其他参数  r如果有参数就更新进去  没有不做任何操作
        data.update(kwargs)
        # 获取response对象， 将自定后的对象响应回去  调用父类的Response
        super().__init__(data=data, status=http_status, headers=headers, exception=exception)

# class MyResponse(Response):
#     def __init__(self,data_status=100,data_message=0,results=None,http_status=None,headers=None,exception= False,**kwargs):
#         data = {
#             "status":data_status,
#             "message":data_message
#         }
#         if results is not None:
#             data['results'] = results
#         data.update(kwargs)
#         super().__init__(data=data,status=http_status,headers=headers,exception=exception)