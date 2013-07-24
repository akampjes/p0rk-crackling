from porkweb.models import *
from django.contrib import admin

from djcelery.models import TaskMeta

class TaskMetaAdmin(admin.ModelAdmin):
	readonly_fields = ('result',)

class ParamInline(admin.TabularInline):
	model = AttackParam
	extra = 0

class AttackCharsetInline(admin.TabularInline):
	model = AttackCharset
	extra = 0

class AttackTypeAdmin(admin.ModelAdmin):
	inlines = [ParamInline, AttackCharsetInline]

class HashTypeDisplay(admin.ModelAdmin):
	list_display = ('name', 'hashcatType', 'hashcat', 'ocllite', 'oclplus')

class JobTaskInline(admin.TabularInline):
	model = JobTask
	extra = 0

class JobTaskDisplay(admin.ModelAdmin):
	list_display = ('job', 'taskid', 'taskstatus')

class CrackedInline(admin.TabularInline):
	model = Cracked
	extra = 0

class JobTaskAdmin(admin.ModelAdmin):
	inlines = [JobTaskInline, CrackedInline]


admin.site.register(JobServer)
admin.site.register(Job, JobTaskAdmin)
admin.site.register(AttackType, AttackTypeAdmin)
admin.site.register(HashType, HashTypeDisplay)
admin.site.register(TaskMeta, TaskMetaAdmin)
admin.site.register(JobTask, JobTaskDisplay)
admin.site.register(Cracked)
