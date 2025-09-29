frappe.ui.form.on('Sales Partner Onboarding', {
    refresh: function(frm) {
        frm.clear_custom_buttons();

        // Show button only after submission and status = Accepted
        if (frm.doc.docstatus === 1 && frm.doc.status === "Accepted") {
            frm.add_custom_button("Create Sales Partner", function() {
                frappe.call({
                    method: "agent_management.sales_agent.doctype.sales_partner_onboarding.sales_partner_onboarding.create_sales_partner",
                    args: { docname: frm.doc.name },
                    callback: function(r) {
                        if (!r.exc && r.message) {
                            frappe.msgprint(__("Sales Partner Created: {0}", [r.message]));

                            // View Sales Partner button
                            frm.add_custom_button("View Sales Partner", function() {
                                frappe.set_route("Form", "Sales Partner", r.message);
                            }, __("View"));

                            frm.reload_doc();
                        }
                    }
                });
            });
        }

        // If a Sales Partner already exists → show view button
        frappe.db.get_list("Sales Partner", {
            filters: { sales_partner_onboarding: frm.doc.name },
            fields: ["name"]
        }).then(sp => {
            if (sp.length) {
                frm.add_custom_button("View Sales Partner", function() {
                    frappe.set_route("Form", "Sales Partner", sp[0].name);
                }, __("View"));
            }
        });
    }
});
