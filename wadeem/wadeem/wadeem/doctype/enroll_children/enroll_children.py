# -*- coding: utf-8 -*-
# Copyright (c) 2020, Siddhant and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class EnrollChildren(Document):
	pass

@frappe.whitelist()
def create_form():
	args = frappe.form_dict
	print(args)
	doc = frappe.new_doc('Enroll Children')
	print("in create form")
	if args:
		print("in args")
		# doc.child_id = 'Abc'
		doc.program_id = args.get('program')
	doc.insert(ignore_permissions=True)
	doc.save(ignore_permissions=True)
	print("in create form",args)
	return doc