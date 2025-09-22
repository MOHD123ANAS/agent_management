import frappe
from frappe.utils import flt


def set_supplier_sales_partner(doc, method):
    if doc.supplier:
        supplier = frappe.get_doc("Supplier", doc.supplier)

        commission_rate = flt(supplier.sales_partner_commission)  # safe cast
        doc.supplier_sales_partner = supplier.sales_partner
        doc.supplier_sales_partner_commission_rate = commission_rate

        if doc.amount_eligible_for_commission:
            doc.supplier_sales_partner_commission = (
                flt(doc.amount_eligible_for_commission) * commission_rate / 100
            )

