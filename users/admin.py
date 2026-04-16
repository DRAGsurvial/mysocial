from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0
    fields = ('nickname', 'slug', 'avatar', 'bio', 'role', 'is_banned', 'banned_reason')

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    inlines = [ProfileInline]
    actions = ['ban_users', 'unban_users', 'grant_site_admin', 'remove_site_admin', 'activate_accounts', 'deactivate_accounts']

    @admin.action(description='Полностью забанить выбранных пользователей')
    def ban_users(self, request, queryset):
        count = 0
        for user in queryset:
            if user.is_superuser:
                continue
            user.is_active = False
            user.save()
            if hasattr(user, 'profile'):
                user.profile.is_banned = True
                if not user.profile.banned_reason:
                    user.profile.banned_reason = 'Заблокирован администратором'
                user.profile.save()
            count += 1
        self.message_user(request, f'Заблокировано пользователей: {count}')

    @admin.action(description='Снять бан с выбранных пользователей')
    def unban_users(self, request, queryset):
        count = 0
        for user in queryset:
            user.is_active = True
            user.save()
            if hasattr(user, 'profile'):
                user.profile.is_banned = False
                user.profile.banned_reason = ''
                user.profile.save()
            count += 1
        self.message_user(request, f'Разблокировано пользователей: {count}')

    @admin.action(description='Выдать права администратора сайта')
    def grant_site_admin(self, request, queryset):
        count = 0
        for user in queryset:
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            if hasattr(user, 'profile'):
                user.profile.role = 'admin'
                user.profile.is_banned = False
                user.profile.banned_reason = ''
                user.profile.save()
            count += 1
        self.message_user(request, f'Админка выдана пользователям: {count}')

    @admin.action(description='Снять права администратора сайта')
    def remove_site_admin(self, request, queryset):
        count = 0
        for user in queryset:
            if user.username == 'admin':
                continue
            user.is_staff = False
            user.is_superuser = False
            user.save()
            if hasattr(user, 'profile') and user.profile.role == 'admin':
                user.profile.role = 'user'
                user.profile.save()
            count += 1
        self.message_user(request, f'Админка снята у пользователей: {count}')

    @admin.action(description='Активировать аккаунты')
    def activate_accounts(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активировано аккаунтов: {updated}')

    @admin.action(description='Деактивировать аккаунты')
    def deactivate_accounts(self, request, queryset):
        count = 0
        for user in queryset:
            if user.username == 'admin':
                continue
            user.is_active = False
            user.save()
            count += 1
        self.message_user(request, f'Деактивировано аккаунтов: {count}')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'user', 'role', 'is_banned', 'slug')
    search_fields = ('nickname', 'user__username', 'user__email', 'slug')
    list_filter = ('role', 'is_banned')
    actions = ['set_moderator', 'set_admin_role', 'set_user_role', 'ban_profiles', 'unban_profiles']

    @admin.action(description='Выдать роль moderator')
    def set_moderator(self, request, queryset):
        count = 0
        for profile in queryset:
            profile.role = 'moderator'
            profile.user.is_staff = True
            profile.user.save()
            profile.save()
            count += 1
        self.message_user(request, f'Роль moderator выдана: {count}')

    @admin.action(description='Выдать роль admin')
    def set_admin_role(self, request, queryset):
        count = 0
        for profile in queryset:
            profile.role = 'admin'
            profile.user.is_staff = True
            profile.user.is_superuser = True
            profile.user.is_active = True
            profile.user.save()
            profile.is_banned = False
            profile.banned_reason = ''
            profile.save()
            count += 1
        self.message_user(request, f'Роль admin выдана: {count}')

    @admin.action(description='Вернуть обычную роль user')
    def set_user_role(self, request, queryset):
        count = 0
        for profile in queryset:
            if profile.user.username == 'admin':
                continue
            profile.role = 'user'
            profile.user.is_staff = False
            profile.user.is_superuser = False
            profile.user.save()
            profile.save()
            count += 1
        self.message_user(request, f'Роль user установлена: {count}')

    @admin.action(description='Забанить выбранные профили')
    def ban_profiles(self, request, queryset):
        count = 0
        for profile in queryset:
            if profile.user.is_superuser:
                continue
            profile.is_banned = True
            if not profile.banned_reason:
                profile.banned_reason = 'Заблокирован администратором'
            profile.save()
            profile.user.is_active = False
            profile.user.save()
            count += 1
        self.message_user(request, f'Профилей забанено: {count}')

    @admin.action(description='Снять бан с выбранных профилей')
    def unban_profiles(self, request, queryset):
        count = 0
        for profile in queryset:
            profile.is_banned = False
            profile.banned_reason = ''
            profile.save()
            profile.user.is_active = True
            profile.user.save()
            count += 1
        self.message_user(request, f'Профилей разбанено: {count}')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.site_header = 'Управление MySocial'
admin.site.site_title = 'MySocial Admin'
admin.site.index_title = 'Панель управления'
