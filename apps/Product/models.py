from django.db import models


class Category(models.Model):
    name_category = models.CharField(max_length=254, blank=True, null=True)

    def __str__(self):
        return self.name_category

class Company(models.Model):
    company_name = models.CharField(max_length=254, blank=True, null=True)
    datil = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.company_name


class Product(models.Model):
    name_product = models.CharField(max_length=255, blank=True, null=True)
    datil = models.TextField()
    price = models.IntegerField()
    many = models.IntegerField()
    price = models.IntegerField()
    categotory = models.ForeignKey('Category', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)

    def __str__(self):
        return self.name_product

