from django.contrib import admin

from .models import *

class AuditAdmin(admin.ModelAdmin):
    readonly_fields= ('created_at', 'updated_at',)

models = [
    Tweet,
    TweetRelation,
    Annotator,
    Question,
]
for model in models:
    admin.site.register(model)

admin.site.register(Annotation,AuditAdmin)
admin.site.register(Answer,AuditAdmin)
# Register your models here.
