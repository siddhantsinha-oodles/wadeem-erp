from __future__ import unicode_literals
import frappe

def set_default_role(doc, method):

	if frappe.flags.setting_role or frappe.flags.in_migrate:
		return

	roles = frappe.get_roles(doc.name)

	if frappe.get_value('Guardians', dict(email=doc.email)) and 'Guardians' not in roles:
		doc.add_roles('Guardians')

def create_guardian():

	user = frappe.session.user

	if frappe.db.get_value('User', user, 'user_type') != 'Website User':
		return

	user_roles = frappe.get_roles()
	portal_settings = frappe.get_single('Portal Settings')
	default_role = portal_settings.default_role

	if default_role not in ['Customer']:
		return

	# create customer / supplier if the user has that role
	if portal_settings.default_role and portal_settings.default_role in user_roles:
		doctype = portal_settings.default_role
	else:
		doctype = None

	if not doctype:
		return

	fullname = frappe.utils.get_fullname(user)

	if doctype == 'Customer':
		guardian = frappe.new_doc("Guardians")
		guardian.update({
			"first_name": fullname,
			"email_id": user
		})
		guardian.flags.ignore_mandatory = True
		guardian.insert(ignore_permissions=True)
		return guardian
	else:
		print("Guardian not craeted")
		return



