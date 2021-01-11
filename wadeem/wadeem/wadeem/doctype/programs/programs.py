# -*- coding: utf-8 -*-
# Copyright (c) 2020, Siddhant and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe import _


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
		context.show_search = True
		children = frappe.frappe.get_all("Children", fields=["full_name"])
		context.children = children
		return context
