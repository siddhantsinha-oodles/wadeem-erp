from __future__ import unicode_literals
import frappe
from frappe import _


def get_context(context):

    context.no_cache = True
    print("Working")
    if frappe.session.user != 'Guest':
        context.show_sidebar = True
        ls = frappe.get_all('Programs', fields=['program_name','program_topics','program_includes','prog_desc','image'])
        print(ls)
        context.all_programs = ls
        print("Context Program-------------------------------------")
    else:
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)

