from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


class AccountAdmin(UserAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = ('username', 'email', 'last_login', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, AccountAdmin)