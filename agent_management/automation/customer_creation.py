import frappe

@frappe.whitelist()
def set_as_customer_default(sales_partner_name):
    sp = frappe.get_doc("Sales Partner", sales_partner_name)

    # If no linked customer, create one
    if not sp.customer:
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": sp.full_name,
            "customer_type": "Partnership",   # or "Company" if your use case
            "default_sales_partner": sp.name,
            "is_sales_partner":1
        })
        customer.insert(ignore_permissions=True)

        # Link back to Sales Partner
        sp.db_set("customer", customer.name)
        frappe.msgprint(f"New Customer '{customer.name}' created and linked to Sales Partner {sp.name}")

    else:
        # If customer exists, update default_sales_partner
        frappe.db.set_value("Customer", sp.customer, {"default_sales_partner":sp.name,
                                                      "is_sales_partner":1})
        frappe.msgprint(f"Customer {sp.customer} updated with default Sales Partner {sp.name}")

    return True
