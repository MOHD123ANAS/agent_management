import frappe
from frappe import _
from erpnext.accounts.doctype.payment_entry.payment_entry import get_party_account as original_get_party_account


@frappe.whitelist()
def sales_partner_query(doctype, txt, searchfield, start, page_len, filters=None):
    """Fetch Sales Partner list for Payment Entry autocomplete"""
    txt = txt or ''
    return frappe.db.get_all(
        "Sales Partner",
        filters={"sales_partner_name": ["like", f"%{txt}%"]},
        fields=["name as value", "sales_partner_name as description"],
        limit_start=start,
        limit_page_length=page_len
    )


@frappe.whitelist()
def get_sales_partner_details(sales_partner):
    """Return defaults for Sales Partner like default accounts"""
    sp = frappe.get_doc("Sales Partner", sales_partner)
    return {
        "default_account": sp.default_account if hasattr(sp, "default_account") else None
    }


@frappe.whitelist()
def get_party_account(party_type, party, account_type, company):
    if party_type == "Sales Partner":
        sp = frappe.get_doc("Sales Partner", party)
        return sp.default_account
    else:
        return original_get_party_account(party_type, party, account_type, company)