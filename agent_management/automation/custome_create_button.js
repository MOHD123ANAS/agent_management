frappe.ui.form.on("Sales Partner", {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Create Customer'), function() {
                frappe.call({
                    method: "agent_management.automation.customer_creation.set_as_customer_default", // update path if needed
                    args: {
                        sales_partner_name: frm.doc.name
                    },
                    callback: function(r) {
                        if (!r.exc) {
                            frm.reload_doc();
                        }
                    }
                });
            }, __("Actions"));   // 👈 This puts it under the Actions menu
        }
    }
});
// frappe.ui.form.on("Sales Partner", {
//     refresh: function(frm) {
//         console.log("✅ Refresh event fired for Sales Partner");
//         frm.add_custom_button(__('Test Button'), function() {
//             frappe.msgprint("Button clicked!");
//         }, __("Actions"));
//     }
// });
