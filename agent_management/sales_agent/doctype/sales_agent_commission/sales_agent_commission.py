# Copyright (c) 2025, Winspire Tech PVT LTD and contributors
# For license information, please see license.txt

# sales_agent_commission.py

# sales_agent_commission.py

# Copyright (c) 2025, Winspire Tech PVT LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class SalesAgentCommission(Document):
    def before_save(self):
       
        self.calculate_totals()

    def calculate_totals(self):
        # --- Supplier commissions ---
        total_bill = 0
        total_supplier_commission = 0
        paid_supplier_referral_commission = 0
        referral_commission_balance=0

        for row in self.sales_partner_commission:   # child table
            total_bill += flt(row.eligible_amount_for_commission)
            total_supplier_commission += flt(row.commission_value)
            paid_supplier_referral_commission +=flt(row.commission_paid)
            referral_commission_balance += flt(row.balance_commission_amount)

        # --- Sales agent commissions ---
        total_sales = 0
        total_agent_commission = 0
        total_commission_paid = 0
        total_balance_commission = 0

        for row in self.sales_agent_commission:   # child table
            total_sales += flt(row.eligible_amount_for_commission)
            total_agent_commission += flt(row.commission_value)
            total_commission_paid += flt(row.commission_paid)
            total_balance_commission += flt(row.balance_commission_amount)

        # Assign values back to parent fields
        self.total_bill_value_from_supplier = total_bill
        self.total_commissions_earned_earned_from_supplier = total_supplier_commission
        self.total_sales_generated = total_sales
        self.total_commission_earned = total_agent_commission

        
        self.commission_paid = total_commission_paid
        self.commission_balance = total_balance_commission
        self.paid_supplier_referral_commission = paid_supplier_referral_commission
        self.referral_commission_balance = referral_commission_balance



    @staticmethod
    def get_or_create_parent(sales_partner):
        """Find or create Sales Agent Commission parent for given sales partner"""
        parent = frappe.db.exists("Sales Agent Commission", {"sales_partner_agent": sales_partner})
        if parent:
            return parent

        doc = frappe.get_doc({
            "doctype": "Sales Agent Commission",
            "sales_partner_agent": sales_partner
        })
        doc.insert(ignore_permissions=True)
        return doc.name



# ------------------------------
# CASE 1: Supplier Sales Partner
# ------------------------------
@frappe.whitelist()
def handle_sales_invoice_on_submit(doc, method=None):
    """Triggered when Sales Invoice is submitted for Supplier Sales Partner"""
    supplier_partner = doc.supplier_sales_partner
    
    # Try to get existing Sales Agent Commission with matching sales_partner_agent
    parent_name = frappe.db.exists("Sales Agent Commission", {"sales_partner_agent": supplier_partner})
    
    if parent_name:
        parent = frappe.get_doc("Sales Agent Commission", parent_name)
    else:
        # Create a new Sales Agent Commission if not found
        parent = frappe.get_doc({
            "doctype": "Sales Agent Commission",
            "sales_partner_agent": supplier_partner
        })
        parent.insert(ignore_permissions=True)
    
    # Append to the Supplier Partner Commission child table
    parent.append("sales_partner_commission", {
        "sales_invoice": doc.name,
        "commision_paid": doc.commission_rate,
        "eligible_amount_for_commission": doc.amount_eligible_for_commission,
        "commission_value": doc.supplier_sales_partner_commission,
        "commission_paid": 0,
        "balance_commission_amount": doc.supplier_sales_partner_commission - 0,
        "payment_status": "Unpaid"
    })
    
    parent.save(ignore_permissions=True)


# -------------------------
# CASE 2: Customer Partner
# -------------------------
@frappe.whitelist()
def sales_invoice_on_submit(doc, method=None):
    """Triggered when Sales Invoice is submitted for Sales Partner"""
    supplier_partner = doc.sales_partner
    if not supplier_partner:
        return

    parent_name = frappe.db.exists("Sales Agent Commission", {"sales_partner_agent": supplier_partner})
    if parent_name:
        parent = frappe.get_doc("Sales Agent Commission", parent_name)
    else:
        parent = frappe.get_doc({
            "doctype": "Sales Agent Commission",
            "sales_partner_agent": supplier_partner
        })
        parent.insert(ignore_permissions=True)

    # Ensure no duplicate invoice entry in Sales Agent Commission table
    existing = [row.sales_invoice for row in parent.sales_agent_commission]
    if doc.name in existing:
        return

    parent.append("sales_agent_commission", {
        "sales_invoice": doc.name,
        "commision_paid": doc.commission_rate,
        "eligible_amount_for_commission": doc.amount_eligible_for_commission,
        "commission_value": doc.total_commission,
        "commission_paid": 0,
        "balance_commission_amount": doc.total_commission,
        "payment_status": "Unpaid"
    })
    parent.save(ignore_permissions=True)

# ------------------------------
# Handle Invoice Cancel
# ------------------------------
@frappe.whitelist()
def handle_sales_invoice_on_cancel(doc, method=None):
    """Triggered when Sales Invoice is cancelled"""
    
    supplier_partner = doc.supplier_sales_partner or doc.sales_partner
    if not supplier_partner:
        return

    parent_name = frappe.db.exists("Sales Agent Commission", {"sales_partner_agent": supplier_partner})
    if not parent_name:
        return

    parent = frappe.get_doc("Sales Agent Commission", parent_name)

    # Handle Supplier Partner table
    for row in getattr(parent, "sales_partner_commission", []):
        if row.sales_invoice == doc.name:
            frappe.db.set_value(row.doctype, row.name, "payment_status", "Cancelled")
            frappe.db.set_value(row.doctype, row.name, "balance_commission_amount", 0)
            frappe.db.set_value(row.doctype, row.name, "commission_value", 0)
            # Handle typo in field
            if hasattr(row, "commision_paid"):
                frappe.db.set_value(row.doctype, row.name, "commision_paid", 0)
            if hasattr(row, "commission_paid"):
                frappe.db.set_value(row.doctype, row.name, "commission_paid", 0)
            break

    for row in getattr(parent, "sales_agent_commission", []):
        if row.sales_invoice == doc.name:
            frappe.db.set_value(row.doctype, row.name, "payment_status", "Cancelled")
            frappe.db.set_value(row.doctype, row.name, "balance_commission_amount", 0)
            frappe.db.set_value(row.doctype, row.name, "commission_value", 0)
            frappe.db.set_value(row.doctype, row.name, "commission_paid", 0)
            break





@frappe.whitelist()
def handle_payment_entry_on_submit(doc, method=None):
    # Only process if Payment Entry is marked as commission
    if not doc.is_sales_partner_commission:
        return

    if not doc.sales_invoice_id:
        return

    # Get the related Sales Invoice
    inv = frappe.get_doc("Sales Invoice", doc.sales_invoice_id)

    # Find or create Sales Agent Commission parent
    parent_name = frappe.db.exists("Sales Agent Commission", {"sales_partner_agent": inv.supplier_sales_partner})
    if parent_name:
        parent = frappe.get_doc("Sales Agent Commission", parent_name)
    else:
        parent = frappe.get_doc({
            "doctype": "Sales Agent Commission",
            "sales_partner_agent": inv.supplier_sales_partner
        })
        parent.insert(ignore_permissions=True)

    # Update the commission row for this invoice
    for row in parent.sales_partner_commission:
        if row.sales_invoice == inv.name:
            row.commission_paid += doc.paid_amount
            row.balance_commission_amount = row.commission_value - row.commission_paid
            row.payment_status = "Paid" if row.balance_commission_amount <= 0 else "Partially-Paid"
            row.payment_entry_receipt = doc.name
            row.payment_date = doc.posting_date
            row.mode_of_payment = doc.mode_of_payment
            break

    parent.save(ignore_permissions=True)

@frappe.whitelist()
def handle_payment_entry_on_submit(doc, method=None):
    """
    Updates commission tracking when Payment Entry is submitted.
    Handles both Supplier Partner Commission and Sales Agent Commission.
    """

    if not doc.sales_invoice_id:
        return

    # Get related Sales Invoice
    inv = frappe.get_doc("Sales Invoice", doc.sales_invoice_id)

    # -----------------------------
    # CASE 1: Supplier Partner
    # -----------------------------
    if getattr(doc, "is_sales_partner_commission", 0):
        parent_name = frappe.db.exists(
            "Sales Agent Commission", {"sales_partner_agent": inv.supplier_sales_partner}
        )
        if parent_name:
            parent = frappe.get_doc("Sales Agent Commission", parent_name)
        else:
            parent = frappe.get_doc({
                "doctype": "Sales Agent Commission",
                "sales_partner_agent": inv.supplier_sales_partner
            })
            parent.insert(ignore_permissions=True)

        for row in parent.sales_partner_commission:
            if row.sales_invoice == inv.name:
                row.commission_paid += doc.paid_amount
                row.balance_commission_amount = row.commission_value - row.commission_paid
                row.payment_status = "Paid" if row.balance_commission_amount <= 0 else "Partially-Paid"
                row.payment_entry_receipt = doc.name
                row.payment_date = doc.posting_date
                row.mode_of_payment = doc.mode_of_payment
                break

        parent.save(ignore_permissions=True)

@frappe.whitelist()
def update_sales_agent_commission_from_payment(doc, method=None):
    """
    Update Sales Agent Commission (child table) when a Payment Entry is submitted
    and marked as 'is_sales_partner'.
    """

    # treat 'doc' as the Payment Entry
    payment_entry = doc

    # 1. Ensure Payment Entry has linked Sales Invoice
    if not getattr(payment_entry, "sales_invoice_id", None):
        return

    # 2. Get the related Sales Invoice
    invoice = frappe.get_doc("Sales Invoice", payment_entry.sales_invoice_id)

    # 3. Only process if Payment Entry is for Sales Partner commission
    if not getattr(payment_entry, "is_sales_partner", 0):
        return

    # 4. Find or create the parent Sales Agent Commission doc
    parent_name = frappe.db.exists(
        "Sales Agent Commission", {"sales_partner_agent": invoice.sales_partner}
    )
    if parent_name:
        parent = frappe.get_doc("Sales Agent Commission", parent_name)
    else:
        parent = frappe.get_doc({
            "doctype": "Sales Agent Commission",
            "sales_partner_agent": invoice.sales_partner
        })
        parent.insert(ignore_permissions=True)

    # 5. Update the child row inside 'Sales Agent Commision Table'
    updated = False
    for row in parent.sales_agent_commission:
        if row.sales_invoice == invoice.name:
            row.commission_value = invoice.total_commission
            row.commission_paid = (row.commission_paid or 0) + payment_entry.paid_amount
            row.balance_commission_amount = row.commission_value - row.commission_paid
            row.payment_status = "Paid" if row.balance_commission_amount <= 0 else "Partially-Paid"

            # fill payment details
            row.payment_entry_receipt = payment_entry.name
            row.payment_date = payment_entry.posting_date
            row.mode_of_payment = payment_entry.mode_of_payment
            row.reference_number = payment_entry.reference_no
            updated = True
            break

    # If no existing row for this invoice → create one
    if not updated:
        parent.append("sales_agent_commission", {
            "sales_invoice": invoice.name,
            "commission_rate": invoice.supplier_sales_partner_commission_rate,
            "eligible_amount_for_commission": invoice.amount_eligible_for_commission,
            "commission_value": invoice.total_commission,
            "commission_paid": payment_entry.paid_amount,
            "balance_commission_amount": invoice.total_commission - payment_entry.paid_amount,
            "payment_entry_receipt": payment_entry.name,
            "mode_of_payment": payment_entry.mode_of_payment,
            "payment_date": payment_entry.posting_date,
            "reference_number": payment_entry.reference_no,
            "payment_status": (
                "Paid" if invoice.total_commission <= payment_entry.paid_amount else "Partially-Paid"
            )
        })

    # 6. Save the parent
    parent.save(ignore_permissions=True)
