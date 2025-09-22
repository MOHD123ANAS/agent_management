# Copyright (c) 2025, Winspire Tech PVT LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class SalesPartnerOnboarding(Document):

    def before_save(self):
        self.set_full_name()
    
    def before_submit(self):
        self.pending()

    def validate(self):
        self.pan_number_validation()
        self.gst_number_validation()
        self.pincode_validation()

    def pan_number_validation(self):
        if self.pan_number:
            pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
            if not re.match(pattern, self.pan_number):
                frappe.throw("Invalid PAN Number format. Example: ABCDE1234F")

    def gst_number_validation(self):
        if self.gst_number:
            pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
            if not re.match(pattern, self.gst_number):
                frappe.throw("Invalid GST Number format. Example: 22AAAAA9999A1Z5")

    def pincode_validation(self):
        if self.pincode:
            pattern = r'^[1-9][0-9]{5}$'
            if not re.match(pattern, self.pincode):
                frappe.throw("Invalid PIN Code format. Example: 560001")

    def set_full_name(self):
        if self.first_name and self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}"
        else:
            self.full_name = self.first_name

    def pending(self):
        if self.status == 'Pending':
            frappe.throw('Cannot Submit Sales Partner Onboarding Form In Pending Status')

    @frappe.whitelist()
    def create_sales_partner(self):
        if self.status != "Accepted":
            frappe.throw("Sales Partner can only be created when status is 'Accepted'.")

        
        existing = frappe.get_all("Sales Partner", filters={"sales_partner_onboarding": self.name})
        if existing:
            frappe.msgprint("Sales Partner already exists for this onboarding.")
            return

        
        sp = frappe.get_doc({
            "doctype": "Sales Partner",
            "full_name": self.full_name,
            "territory": "All Territories",
            "commission_rate": 1,
            "sales_partner_onboarding": self.name
        })
        sp.insert()
        frappe.msgprint(f"Sales Partner '{sp.partner_name}' created successfully!")
@frappe.whitelist()
def create_sales_partner(docname):
    
    doc = frappe.get_doc("Sales Partner Onboarding", docname)
    doc.create_sales_partner()