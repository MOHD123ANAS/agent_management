frappe.ui.form.on("Sales Order", {
    supplier: function(frm) {
        if (frm.doc.supplier) {
            frappe.db.get_value("Supplier", frm.doc.supplier, ["sales_partner", "sales_partner_commission"])
                .then(r => {
                    if (r.message) {
                        frm.set_value("supplier_sales_partner", r.message.sales_partner || "");
                        frm.set_value("supplier_sales_partner_commission_rate", r.message.sales_partner_commission || 0);

                        // auto calculate Commission amount
                        if (r.message.sales_partner_commission) {
                            let eligible = frm.doc.amount_eligible_for_commission || 0;
                            let rate = r.message.sales_partner_commission || 0;
                            frm.set_value("supplier_sales_partner_commission", (eligible * rate / 100));
                        }
                    }
                });
        } else {
            frm.set_value("supplier_sales_partner", "");
            frm.set_value("supplier_sales_partner_commission_rate", 0);
            frm.set_value("supplier_sales_partner_commission", 0);
        }
    }
});
