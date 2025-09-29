import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field
from erpnext.setup.doctype.sales_partner.sales_partner import SalesPartner as SP



def create_custom_fields():
    custom_fields = {
        "Sales Partner": [
            {
                "fieldname": "supplier_partner__commission",
                "fieldtype": "Float",
                "label": "Supplier Partner Commission",
                "insert_after": "commission_rate",
                "in_list_view": 1,
                "reqd": 0,
            },
            {
                "fieldname": "full_name",
                "fieldtype":"Data",
                "label":"Full Name",
                "insert_after":"partner_name",
                "in_list_view":1,
                "reqd":1,

            },

            {
                "fieldname": "sales_partner_onboarding",
                "fieldtype":"Data",
                "label":"Sales Partner Onboarding",
                "insert_after":"full_name",
                "in_list_view":1,
                "reqd":0,

            },
            {
                "fieldname":"selection",
                "label":"Selection",
                "fieldtype":"Select",
                "options":"SAP -",
                "default":"SAP -",
                "hidden":0,
                "insert_after":"referral_code"
            },
            {
                "fieldname":"counter",
                "label":"Counter",
                "fieldtype":"Data",
                "read_only":1,
                "insert_after":"selection"
            },
                       {
                "fieldname":"customer",
                "label":"Customer Id",
                "fieldtype":"Link",
                "options":"Customer",
                "insert_after":"supplier_partner__commission"
            }
        ]
    }

    for doctype, fields in custom_fields.items():
        for field in fields:
            if not frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}):
                create_custom_field(doctype, field)
                
                frappe.db.commit()
                frappe.clear_cache(doctype=doctype)


def delete_custom_fields():
    custom_fields_to_delete = {
        "Sales Partner": ["supplier_partner__commission","full_name","sales_partner_onboarding","selection","counter","customer"]
    }

    for doctype, fields in custom_fields_to_delete.items():
        for field_name in fields:
            if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field_name}):
                frappe.delete_doc("Custom Field", f"{doctype}-{field_name}", ignore_missing=True)
                frappe.db.commit()
                frappe.clear_cache(doctype=doctype)

def disable_partner_name_mandatory():

    frappe.db.sql("""
        UPDATE `tabDocField`
        SET reqd = 0
        WHERE parent = 'Sales Partner' AND fieldname = 'partner_name'
    """)
    frappe.clear_cache(doctype="Sales Partner")


def enable_partner_name_mandatory():
    frappe.db.sql("""
        UPDATE `tabDocField`
        SET reqd = 1
        WHERE parent = 'Sales Partner' AND fieldname = 'partner_name'
    """)
    frappe.clear_cache(doctype="Sales Partner")

def set_sales_partner_name(doc, method=None):

 

    
    last_partner = frappe.get_all(
        "Sales Partner",
        filters={"selection": doc.selection},
        fields=["counter"],
        order_by="creation desc",
        limit=1
    )

    
    last_counter = 0
    if last_partner:
        try:
            last_counter = int(last_partner[0].counter or 0)
        except (TypeError, ValueError):
            last_counter = 0

   
    doc.counter = str(last_counter + 1)

    
    doc.partner_name = f"{doc.selection}{doc.counter}"
    doc.name = doc.partner_name
