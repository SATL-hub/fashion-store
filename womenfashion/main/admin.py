from django.contrib import admin
from .models import *
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','category','description','price','available','stock','image',)

class ProductVariationAdmin(admin.ModelAdmin):
    list_display=('product','size','color')

class UserprofileAdmin(admin.ModelAdmin):
    list_display=('name','email')

class UsercartAdmin(admin.ModelAdmin):
    list_display=('user','product','no_of_item','size','color','individual_price','total_price')

class Wish_listAdmin(admin.ModelAdmin):
    list_display = ('user','product','product_price')
    def product_price(self,obj):
        return obj.product.price
    
class OrderitemsAdmin(admin.ModelAdmin):
    list_display=('user','email','mobile','payment_mode','status','ordered_on')

class ReviewsAdmin(admin.ModelAdmin):
    list_display=('user','product','message','rating')
    
class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','name','email','phone')
    
class ProfilepicAdmin(admin.ModelAdmin):
    list_display=('user','propic','resume')

class HistoryAdmin(admin.ModelAdmin):
    list_display=('user','item','no_of_item','size','color','individual_price','total_price','payment_mode','status','ordered_on')
    
admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductVariation,ProductVariationAdmin)
admin.site.register(Offers)
admin.site.register(Userprofile,UserprofileAdmin)
admin.site.register(Product_images)
admin.site.register(Usercart,UsercartAdmin)
admin.site.register(Wish_list,Wish_listAdmin)
admin.site.register(Orderitems,OrderitemsAdmin)
admin.site.register(Reviews,ReviewsAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Profilepic,ProfilepicAdmin)
admin.site.register(History,HistoryAdmin)