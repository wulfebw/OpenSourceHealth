from django.contrib import admin
from categories.models import Category, Group, ModeratedCategory

import logging
logger = logging.getLogger('log')

class ModeratedCategoryAdmin(admin.ModelAdmin):
	fields = ('name', 'group')
	list_display = ('name', 'group')
	ordering = ['name']
	actions = ['allow_changes']

	def allow_changes(self, request, queryset):
		for category in queryset:

			# check if it exists. If it does, do nothing
			try:
				existing_category = Category.objects.get(name=category.name)
				if existing_category:
					category.delete() # already exists so delete this moderated category
			except:	# doesn't exist

				# check if the group exists. If it does, use that group, o/w use None
				try: 
					group = Group.objects.get(name=category.group)
				except:
					group = None

				# create the actual category
				if group is not None:
					new_category = Category(name=category.name, group=category.group)
				else:
					new_category = Category(name=category.name)
				new_category.save()
				category.delete()


	allow_changes.short_description = "Enact the proposed changes selected below"

admin.site.register(ModeratedCategory, ModeratedCategoryAdmin)
admin.site.register(Category)
admin.site.register(Group)
