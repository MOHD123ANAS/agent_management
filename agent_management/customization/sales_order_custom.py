import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def create_custom_fields():
    custom_fields = {
        "Sales Order": [
            {
                "fieldname": "supplier",
                "fieldtype": "Link",
                "label": "Supplier",
                "insert_after": "set_warehouse",
                "in_list_view": 1,
                "reqd": 0,
                "options": "Supplier"
            },
            {
                "fieldname": "supplier_sales_partner",
                "fieldtype": "Link",
                "label": "Supplier Sales Partner",
                "fetch_from": "supplier.sales_partner",
                "insert_after": "sales_partner",
                "in_list_view": 1,
                "reqd": 0,
                "options": "Sales Partner"
            },
            {
                "fieldname": "supplier_sales_partner_commission_rate",
                "fieldtype": "Float",
                "label": "Supplier Sales Partner Commission Rate",
                "fetch_from": "supplier.sales_partner_commission",
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
            
        ]
    }

    for doctype, fields in custom_fields.items():
        for field in fields:
            if not frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}):
                create_custom_field(doctype, field)

    frappe.db.commit()
    frappe.clear_cache(doctype="Sales Order")


def delete_custom_fields():
    custom_fields_to_delete = {
        "Sales Order": ["supplier", "supplier_sales_partner_commission", "supplier_sales_partner","supplier_sales_partner_commission_rate"]
    }

    for doctype, fields in custom_fields_to_delete.items():
        for field_name in fields:
            if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": field_name}):
                frappe.delete_doc("Custom Field", f"{doctype}-{field_name}", ignore_missing=True)

    frappe.db.commit()
    frappe.clear_cache(doctype="Sales Order")
