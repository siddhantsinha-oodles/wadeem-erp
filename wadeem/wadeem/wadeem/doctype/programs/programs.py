# -*- coding: utf-8 -*-
# Copyright (c) 2020, Siddhant and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.website.website_generator import WebsiteGenerator

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe import _

# def get_context(context):
#     program_name = frappe.form_dict.program_name
#     program = frappe.get_doc('Programs', program_name)
#     print(program_name)
#     context.program = program

# class Programs(WebsiteGenerator):
# 	website = frappe._dict(
# 		page_title_field="program_name",
# 		no_cache=1
# 	)


class Programs(WebsiteGenerator):
	website = frappe._dict(
		page_title_field="program_name",
		condition_field="show_in_website",
		no_cache=1
	)

	def validate(self):
		super(Programs, self).validate()

	def make_route(self):
		if not self.route:
			return '/' + self.scrub(self.program_name)

	def get_context(self, context):
		print("in program context")
		context.show_search = True
		children = frappe.frappe.get_all("Children", fields=["full_name"])
		context.children = children
		return context
