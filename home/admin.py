from django.contrib import admin
from.models import Book,ClassName,Order,RatingAndReview,ReturnOrder,Otp,CreateCombetition,Combetition
# Register your models here.
from.models import Membership,Order2,Penalty,Cart
admin.site.register(Book),
admin.site.register(ClassName),
admin.site.register(Order),
admin.site.register(ReturnOrder),
admin.site.register(RatingAndReview),
admin.site.register(Otp),
admin.site.register(CreateCombetition),
admin.site.register(Combetition),
admin.site.register(Membership),
admin.site.register(Order2),
admin.site.register(Penalty),
admin.site.register(Cart),