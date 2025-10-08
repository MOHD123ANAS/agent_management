import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_custom_fields():
    custom_fields = {
        "Sales Invoice": [
            {
                "fieldname": "supplier",
                "fieldtype": "Link",
                "label": "Supplier",
                "options": "Supplier",
                "insert_after": "set_posting_time",
                "in_list_view": 1,
                "reqd": 0,
            },
            {
                "fieldname": "supplier_sales_partner",
                "fieldtype": "Link",
                "label": "Supplier Sales Partner",
                "options": "Sales Partner",
                "insert_after": "sales_partner",
                "in_list_view": 1,
                "reqd": 0,
            },
            {
                "fieldname": "supplier_sales_partner_commission_rate",
                "fieldtype": "Float",
                "label": "Supplier Sales Partner Commission Rate",
                "insert_after": "commission_rate",
                "in_list_view": 1,
                "reqd": 0,
            },
            {
                "fieldname": "supplier_sales_partner_commission",
                "fieldtype": "Currency",
                "label": "Supplier Sales Partner Commission",
                "insert_after": "supplier_sales_partner_commission_rate",
                "in_list_view": 1,
                "reqd": 0,
                "read_only": 1
            },
            {
                "fieldname": "delivered",
                "fieldtype": "Check",
                "label": "Delivered?",
                "insert_after": "is_debit_note",
                "in_list_view": 1,
                "reqd": 0,
                "read_only": 1
            },

        ]
    }

    for doctype, fields in custom_fields.items():
        for field in fields:
            if not frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}):
                create_custom_field(doctype, field)

    frappe.db.commit()
    frappe.clear_cache(doctype="Sales Invoice")
    
def delete_custom_fields():
    custom_fields_to_delete = {
        "Sales Invoice": ["supplier", "supplier_sales_partner_commission", "supplier_sales_partner","supplier_sales_partner_commission_rate","delivered"]
    }

    for doctype, fields in custom_fields_to_delete.items():
        for field_name in fields:
            if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field_name}):
                frappe.delete_doc("Custom Field", f"{doctype}-{field_name}", ignore_missing=True)

    frappe.db.commit()
    frappe.clear_cache(doctype="Sales Invoice")
