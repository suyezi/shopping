from django.db import models


class Users(models.Model):
   
    username = models.CharField(max_length=32)
    name = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    sex = models.IntegerField(default=1)
    address = models.CharField(max_length=255)
    code = models.CharField(max_length=6)
    phone = models.CharField(max_length=16)
    email = models.CharField(max_length=50)
    state = models.IntegerField(default=1)
    addtime = models.IntegerField()

    class Meta:
        db_table = "users"  # 更改表名 真实表名

    def toDirct(self):
        return {'id':self.id,'username':self.username,'name':self.name,'phone':self.phone,'code':self.code,'email':self.email,'address':self.address}


#商品类别信息模型
class Types(models.Model):
    name = models.CharField(max_length=32)
    pid = models.IntegerField(default=0)
    path = models.CharField(max_length=255)

    class Meta:
        db_table = "type"  # 更改表名


#商品信息模型
class Goods(models.Model):
    typeid = models.IntegerField()
    goods = models.CharField(max_length=32)
    company = models.CharField(max_length=50)
    descr = models.TextField()
    price = models.FloatField()
    picname = models.CharField(max_length=255)
    state = models.IntegerField(default=1)
    store = models.IntegerField(default=0)
    num = models.IntegerField(default=0)
    clicknum = models.IntegerField(default=0)
    addtime = models.IntegerField()

    class Meta:
        db_table = "goods"  # 更改表名
    def toDirct(self):
        return {'id':self.id,'picname':self.picname,'goods':self.goods,'price':self.price,'addtime':self.addtime,'company':self.company,'descr':self.descr,'store':self.store,'num':self.num,'clicknum':self.clicknum}

# 自定义城市区县信息model类
class District(models.Model):
    name = models.CharField(max_length=255)
    upid = models.IntegerField()

    class Meta:
        db_table = "district"  # 指定真实表名


class Orders(models.Model):
    uid = models.IntegerField()
    linkman = models.CharField(max_length=32)
    address = models.CharField(max_length=255)
    code = models.CharField(max_length=6)
    phone = models.CharField(max_length=16)
    status = models.IntegerField(default=1)
    addtime = models.IntegerField()
    total = models.FloatField()

    class Meta:
        db_table = "orders"  # 更改表名


class Detail(models.Model):
    orderid = models.IntegerField()
    goodsid = models.IntegerField()
    num = models.IntegerField()
    name = models.CharField(max_length=32)
    price = models.FloatField()

    class Meta:
        db_table = "detail"  # 更改表名