import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_custom_fields():
    custom_fields = {
        "Payment Entry": [
            {
            "fieldname": "is_sales_partner_commission",
            "fieldtype": "Check",
            "label": "Sales Partner Commission?",
            "insert_after": "party_name",
            "in_list_view": 1
        },
        {
            "fieldname": "sales_invoice_id",
            "fieldtype": "Link",
            "label": "Sales Invoice",
            "display_depends_on": "eval:doc.is_sales_partner_commission",
            "options": "Sales Invoice",
            "insert_after": "party_type",
            "in_list_view": 1,
            "mandatory_depends_on": "eval:doc.is_sales_partner_commission",
            
        },
        {
            "fieldname": "is_sales_partner",
            "fieldtype": "Check",
            "label": "Is Sales Partner",
            "insert_after": "party",
            "in_list_view":1

        }

                    ]
    }

    for doctype, fields in custom_fields.items():
        for field in fields:
            if not frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}):
                create_custom_field(doctype, field)

    frappe.db.commit()
    frappe.clear_cache(doctype="Payment Entry")
    
def delete_custom_fields():
    custom_fields_to_delete = {
        "Payment Entry": ["is_sales_partner_commission", "sales_invoice_id","is_sales_partner"]
    }

    for doctype, fields in custom_fields_to_delete.items():
        for field_name in fields:
            if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field_name}):
                frappe.delete_doc("Custom Field", f"{doctype}-{field_name}", ignore_missing=True)

    frappe.db.commit()
    frappe.clear_cache(doctype="Payment Entry")
