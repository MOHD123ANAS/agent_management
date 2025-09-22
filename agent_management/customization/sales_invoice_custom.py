import frappe
from frappe.utils import flt

def set_supplier_sales_partner_si(doc, method):
    """Fetch supplier's sales partner + commission into Sales Invoice."""
    if doc.supplier:
        supplier = frappe.get_doc("Supplier", doc.supplier)

        commission_rate = flt(supplier.sales_partner_commission)

        doc.supplier_sales_partner = supplier.sales_partner
        doc.supplier_sales_partner_commission_rate = commission_rate

        if doc.total:  # or whichever field represents base amount
            doc.supplier_sales_partner_commission = (
                flt(doc.total) * commission_rate / 100
            )
