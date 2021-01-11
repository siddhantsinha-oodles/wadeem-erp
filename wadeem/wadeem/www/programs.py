from __future__ import unicode_literals
import frappe
from frappe import _

sitemap = 1

def get_conditions(filter_list, and_or='and'):
	from frappe.model.db_query import DatabaseQuery
	if not filter_list:
		return ''
	conditions = []
	DatabaseQuery('Programs').build_filter_conditions(filter_list, conditions, ignore_permissions=True)
	join_by = ' {0} '.format(and_or)

	return '(' + join_by.join(conditions) + ')'

def get_programs_for_website(search=None):

	start = frappe.form_dict.start or 0
	search_condition = ''
	if search:
		default_fields = {'name', 'program_name'}
		meta = frappe.get_meta("Programs")
		meta_fields = set(meta.get_search_fields())
		search_fields = default_fields.union(meta_fields)
		try:
			if frappe.db.count('Programs', cache=True) > 50000:
				search_fields.remove('description')
		except KeyError:
			pass

		search = '%{}%'.format(search)
		or_filters = [[field, 'like', search] for field in search_fields]

		search_condition = get_conditions(or_filters, 'or')

	results = frappe.db.sql('''
		SELECT
			`tabItem`.`name`, `tabItem`.`program_name`,
			`tabItem`.`website_image`, `tabItem`.`image`,
			`tabItem`.`web_long_description`, `tabItem`.`description`,
			`tabItem`.`route`
		FROM
			`tabItem`
		WHERE
			{search_condition}
		GROUP BY
			`tabItem`.`name`
	'''.format(
			search_condition=search_condition,
			start=start
		)
	, as_dict=1)

	return results

def get_context(context):

	context.no_cache = True
	context.show_sidebar = True
	ls = frappe.get_all('Programs', fields=['program_name','program_topics','program_includes','prog_desc','image','price'])
	context.all_programs = ls
	if frappe.form_dict:
		search = frappe.form_dict.search
	else:
		search = None
	context.items = get_programs_for_website(search)




