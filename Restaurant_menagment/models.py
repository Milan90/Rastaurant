from django.db import models


class Table(models.Model):
    number = models.SmallIntegerField()
    seats = models.SmallIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.number)


ORDER_STATUS = ((1, "to prepare"),
                (2, "order in progress"),
                (3, "ready to go"),
                (4, "served"))


class Orders(models.Model):
    status = models.SmallIntegerField(choices=ORDER_STATUS)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    archive = models.BooleanField(default=False)


class Category(models.Model):
    category = models.TextField()


class Dish(models.Model):
    meal_name = models.CharField(max_length=64)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    order = models.ManyToManyField(Orders)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comments(models.Model):
    comment = models.CharField(max_length=64)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.comment)
