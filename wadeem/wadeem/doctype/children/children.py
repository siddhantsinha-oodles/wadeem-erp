# -*- coding: utf-8 -*-
# Copyright (c) 2020, Siddhant and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class Children(Document):
	def validate(self):
		self.full_name = " ".join(filter(None, [self.first_name, self.middle_name ,self.last_name]))
