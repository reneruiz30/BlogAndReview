from django.contrib import admin
from .models import Blog, Review, Comment, SportsSubsection, SubsectionComment
from django.utils.html import format_html
from .models import Subsection

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'image_tag')
    readonly_fields = ('image_tag',)

    class Media:
        css = {
            'all': ('blogapp/css/admin.css',)
        }

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="120" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Imagen'

admin.site.register(Blog, BlogAdmin)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(SportsSubsection)
admin.site.register(SubsectionComment)

@admin.register(Subsection)
class SubsectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'blog')  # Ajusta los campos según tu modelo

    class Media:
        css = {
            'all': ('blogapp/css/admin.css',)
        }
