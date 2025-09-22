import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_custom_fields():
    custom_fields = {
        "Supplier": [
            {
                "fieldname": "sales_partner_commission",
                "fieldtype": "Data",
                "label": "Sales Partner Commission",
                "fetch_from": "sales_partner.supplier_partner__commission",
                "insert_after": "sales_partner",
                "in_list_view": 1,
                "reqd": 0,
            },
            {
                "fieldname": "sales_partner",
                "fieldtype": "Link",
                "label": "Sales Partner",
                "insert_after": "default_price_list",
                "options": "Sales Partner",
                "in_list_view": 1,
                "reqd": 0,
            },
        ]
    }

    for doctype, fields in custom_fields.items():
        for field in fields:
            if not frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}):
                create_custom_field(doctype, field)

    frappe.db.commit()
    frappe.clear_cache(doctype="Supplier")


def delete_custom_fields():
    custom_fields_to_delete = {
        "Supplier": ["sales_partner_commission", "sales_partner"]
    }

    for doctype, fields in custom_fields_to_delete.items():
        for field_name in fields:
            if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field_name}):
                frappe.delete_doc("Custom Field", f"{doctype}-{field_name}", ignore_missing=True)

    frappe.db.commit()
    frappe.clear_cache(doctype="Supplier")
