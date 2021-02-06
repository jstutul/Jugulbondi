from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.forms import UsercreationForm,UserchangeForm
from accounts.models import  Profile,FriendList,ContractUs,Messeges,SuccessStory,Comment

User=get_user_model()
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    add_form = UsercreationForm
    form=UserchangeForm
    list_display = ('id','email','first_name','last_name','is_active','is_staff','is_superuser','is_varified','verification' )
    # readonly_fields = ('email',)
    list_filter = ('is_superuser',)
    list_display_links = ('email','id')
    list_per_page = 10
    fieldsets = (
        (

            None, {'fields': ('email','first_name','last_name','password',)}
        ),
        (
            'Permissions',{
                'fields':('is_superuser','is_staff','is_active','is_varified','verification')
            }
        )
    )
    add_fieldsets = (
        (

            None,{
                'classes': ('wide',),
                'fields': ('email','first_name','last_name','password1','password2','is_active')
            }
        ),
        ('permissions',{'fields' : ('is_superuser','is_staff')}
         )
    )
    ordering = ('-id',)
    search_fields = ('email',)
    filter_horizontal = ()

admin.site.register(User,UserAdmin)
class ProfileAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('email','email_id',)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(FriendList)

class AdminContract(admin.ModelAdmin):
    list_display = ("name","email","receive_on")
    list_per_page = 10
    search_fields = ("name","email",)
    ordering = ("receive_on",)
admin.site.register(ContractUs,AdminContract)
class AdminMessage(admin.ModelAdmin):
    list_display = ("id","sender","receiver","subject","send_on","reply_on")
    list_per_page = 10
    search_fields = ("sender","sender",)
    list_filter = ("subject","send_on","reply_on",)
    ordering = ("send_on",)
admin.site.register(Messeges,AdminMessage)

class UserSuccess(admin.ModelAdmin):
    list_display = ("post_by","post_on")
    list_per_page = 10
    search_fields = ("post_by","post_on","describe",)
    list_filter = ("post_by",)
    ordering = ("post_on",)
admin.site.register(SuccessStory,UserSuccess)

admin.site.register(Comment)