frappe.ui.form.on('Payment Entry', {
    onload: function(frm) {
        // Add Sales Partner to party_type dropdown
        frm.set_df_property('party_type', 'options', ['Customer', 'Supplier', 'Sales Partner']);
    },

    party_type: function(frm) {
        if (frm.doc.party_type === "Sales Partner") {
            frm.set_value('party', '');

            // Query Sales Partner for party field
            frm.set_query('party', function() {
                return {
                    query: "agent_management.agent_management.customization.payment_entry_customisation.sales_partner_query",
                    filters: {}
                };
            });

        } else {
            frm.set_query('party', null);
        }
    },

    party: function(frm) {
        if (frm.doc.party_type === "Sales Partner" && frm.doc.party) {
            // Fetch Sales Partner defaults (like default accounts)
            frappe.call({
                method: "agent_management.agent_management.customization.payment_entry_customisation.get_sales_partner_details",
                args: { sales_partner: frm.doc.party },
                callback: function(r) {
                    if (r.message) {
                        const data = r.message;

                        if (data.default_account) {
                            if (frm.doc.payment_type === 'Receive') {
                                frm.set_value('paid_from', data.default_account);
                            } else {
                                frm.set_value('paid_to', data.default_account);
                            }
                        }
                    }
                }
            });
        }
    }
});
