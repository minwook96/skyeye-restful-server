from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account


class AccountAdmin(UserAdmin):
    # 관리자 화면에 보여질 칼럼 지정
    list_display = ('email', 'username', 'name', 'create_at', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username', 'name')
    readonly_fields = ('id', 'create_at', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)