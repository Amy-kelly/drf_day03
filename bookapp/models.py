from django.db import models

# Create your models here.
'''
表的关系：book与publish 多对一
          book与author  多对多
          author与author_detail 一对一
          BaseModel基类
'''
class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    class Meta:
        abstract = True

class Book(BaseModel):
    book_name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    pic = models.ImageField(upload_to="img",default="img/1.jpg")
    publish = models.ForeignKey(
        to="Press",
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name="books"
    )
    authors = models.ManyToManyField(to="Author",db_constraint=False,related_name="books")
    #自定义字段 返回结果值一样
    def example(self):
        return "example" #键值对的值
    #自定义返回出版社的名字（对已有的字段进行多表连接处理）
    @property
    def publish_name(self):
        print(self)
        return self.publish.press_name

    #自定义作者查询
    @property
    def author_list(self):
        # Book表是从表，Author表是主表 主->从：从表名小写
        # 从->主：外键字段 values显示的字段
        # Author是主表，detail是从表，
        return self.authors.values("author_name","age","detail__phone")

    class Meta:
        db_table = "tb_book"
        verbose_name = "图书"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.book_name

class Press(BaseModel):
    press_name = models.CharField(max_length=30)
    pic = models.ImageField(upload_to="img",default="img/1.jpg")
    address = models.CharField(max_length=128)
    class Meta:
        db_table = "tb_press"
        verbose_name = "出版社"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.press_name

class Author(BaseModel):
    author_name = models.CharField(max_length=30)
    age = models.IntegerField()
    class Meta:
        db_table = "tb_author"
        verbose_name = "作者"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.author_name

class AuthorDetail(BaseModel):
    phone = models.CharField(max_length=11)
    author = models.OneToOneField(to="Author",on_delete=models.CASCADE,related_name="detail")
    class Meta:
        db_table = "tb_author_detail"
        verbose_name = "作者详情"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s的详情" % self.author.author_name