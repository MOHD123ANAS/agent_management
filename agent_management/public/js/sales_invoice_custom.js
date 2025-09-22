frappe.ui.form.on("Sales Invoice", {
    supplier: function(frm) {
        if (frm.doc.supplier) {
            frappe.db.get_doc("Supplier", frm.doc.supplier).then(supplier => {
                frm.set_value("supplier_sales_partner", supplier.sales_partner);
                frm.set_value("supplier_sales_partner_commission_rate", supplier.sales_partner_commission);

                if (frm.doc.total) {
                    frm.set_value(
                        "supplier_sales_partner_commission",
                        frm.doc.total * (supplier.sales_partner_commission || 0) / 100
                    );
                }
            });
        } else {
            frm.set_value("supplier_sales_partner", "");
            frm.set_value("supplier_sales_partner_commission_rate", 0);
            frm.set_value("supplier_sales_partner_commission", 0);
        }
    }
});
