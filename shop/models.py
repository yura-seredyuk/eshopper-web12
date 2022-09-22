import uuid
from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils import timezone


class ProductCategory(models.Model):
    category_name = models.CharField(max_length=30, blank=False, unique=True)
    slug = models.SlugField(null=True)

    class Meta:
        verbose_name = "Product category"
        verbose_name_plural = "Product categories"

    def __str__(self) -> str:
        return self.category_name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', [self.slug])


class Country(models.Model):
    country_name = models.CharField(max_length=30, blank=False, unique=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self) -> str:
        return self.country_name


class City(models.Model):
    city_name = models.CharField(max_length=30, blank=False)
    country = models.ForeignKey(Country, related_name='pk', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self) -> str:
        return self.city_name


class Address(models.Model):
    street = models.CharField(max_length=100, blank=False)
    appartaments = models.CharField(max_length=10, blank=False)
    zip_code = models.CharField(max_length=10, blank=False)
    city = models.ForeignKey(City, related_name='pk', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self) -> str:
        return f"{self.street}, {self.appartaments}, {self.zip_code}"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_of_birth = models.DateField()
    user_group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=15, blank=False)
    address = models.ForeignKey(Address, related_name='pk', on_delete=models.DO_NOTHING)
    photo = models.ImageField(upload_to='profiles/', blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self) -> str:
        return f"{self.user}, {self.user_group}, {self.phone}"


class Customer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self) -> str:
        return f"{self.profile}"


class Manager(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Managers"

    def __str__(self) -> str:
        return f"{self.profile}"


class Employee(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    chief = models.ForeignKey(Manager, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employes"

    def __str__(self) -> str:
        return f"{self.profile} {self.chief}"


class Product(models.Model):
    product_name = models.CharField(max_length=30)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING)
    details = models.TextField(max_length=500, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    rating = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='products/', blank=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self) -> str:
        return f"{self.product_name} {self.unit_price} {self.product_category}"


class Order(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    date_of_order = models.DateTimeField(default=timezone.now)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=1)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self) -> str:
        return f"{self.customer} {self.city} {self.date_of_order} {self.product} {self.price}"
