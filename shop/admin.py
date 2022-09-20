from django.contrib import admin
from .models import ProductCategory, Country, City, \
    Address, Profile, Customer, Employee, Manager, \
    Product, Order


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display: ['category_name']
admin.site.register(ProductCategory, ProductCategoryAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display: ['country_name']
admin.site.register(Country, CountryAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display: ['city_name', 'country_id']
admin.site.register(City, CityAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display: ['street', 'appartaments', 'zip_code', 'city_id']
admin.site.register(Address, AddressAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display: ['user', 'group', 'phone', 'address_id']
admin.site.register(Profile, ProfileAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display: ['profile']
admin.site.register(Customer, CustomerAdmin)

class ManagerAdmin(admin.ModelAdmin):
    list_display: ['profile']
admin.site.register(Manager, ManagerAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display: ['profile', 'chief']
admin.site.register(Employee, EmployeeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display: ['product_name', 'unit_price', 'country', 'product_category']
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display: ['employee', 'customer', 'city', 'date_of_order', 'product', 'price']
admin.site.register(Order, OrderAdmin)