from django.db import models

# Create your models here.
class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    class Meta:
        abstract = True

class Product(BaseModel):
    pro_name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    #自定义字段
    def pro_order(self):
        return self.oreders.product

    def pro_detail(self):
        return self.detail.pro_detail

    class Meta:
        db_table = "tb_product"
        verbose_name = "商品"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.pro_name

class User(BaseModel):
    user_name = models.CharField(max_length=30)
    pic = models.ImageField(upload_to="img", default="img/1.jpg")

    class Meta:
        db_table = "tb_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.user_name

class Orders(BaseModel):
    order_date = models.DateTimeField()
    product = models.ManyToManyField(to="Product",db_constraint=False,related_name="oreders")
    user = models.ForeignKey(to="User",on_delete=models.CASCADE,db_constraint=False,
        related_name="orders")
    class Meta:
        db_table = "tb_orders"
        verbose_name = "订单"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s的订单" % self.user.user_name

class ProdectDetail(BaseModel):
    pic = models.ImageField(upload_to="img", default="img/1.jpg")
    pro_detail = models.OneToOneField(to="Product", on_delete=models.CASCADE, related_name="detail")
    class Meta:
        db_table = "tb_detail"
        verbose_name = "商品详情"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s的商品详情" % self.pro_detail.pro_name