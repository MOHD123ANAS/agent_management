import frappe

def execute():
    """
    Cleanup old workspaces safely.
    This patch is idempotent: safe to run multiple times.
    """

    old_workspaces = [
        "Sales Partner Portal"
    ]

    for ws in old_workspaces:
        if frappe.db.exists("Workspace", ws):
            try:
                frappe.delete_doc("Workspace", ws, force=1, ignore_permissions=True)
                print(f"✅ Removed old workspace: {ws}")
            except Exception as e:
                # Log but don’t block migration
                print(f"⚠️ Could not remove workspace {ws}: {e}")
        else:
            print(f"ℹ️ Workspace not found (already removed): {ws}")

    frappe.db.commit()
