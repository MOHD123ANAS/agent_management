// Copyright (c) 2025, Winspire Tech PVT LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Partner Onboarding', {
    refresh: function(frm) {
        frm.clear_custom_buttons(); // prevent duplicate buttons

        if (frm.doc.status === "Accepted") {
            frm.add_custom_button("Create Sales Partner", function() {
                frappe.call({
                    method: "agent_management.sales_agent.doctype.sales_partner_onboarding.sales_partner_onboarding.create_sales_partner",
                    args: { docname: frm.doc.name },
                    callback: function(r) {
                        frm.reload_doc();
                    }
                });
            });
        }
    }
});
