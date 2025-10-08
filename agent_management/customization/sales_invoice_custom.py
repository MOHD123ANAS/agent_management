import frappe
from frappe.utils import flt

def set_supplier_sales_partner_si(doc, method):
    
    if doc.supplier:
        supplier = frappe.get_doc("Supplier", doc.supplier)

        commission_rate = flt(supplier.sales_partner_commission)

        doc.supplier_sales_partner = supplier.sales_partner
        doc.supplier_sales_partner_commission_rate = commission_rate

        if doc.total:
            doc.supplier_sales_partner_commission = (
                flt(doc.total) * commission_rate / 100
            )
def sales_invoice_after_submit(doc, method):
    if doc.workflow_state == "Delivered" and not doc.delivered:
        doc.db_set("delivered", 1)
