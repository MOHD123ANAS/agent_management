app_name = "agent_management"
app_title = "Agent Management"
app_publisher = "Winspire Tech PVT LTD"
app_description = "Agent Management"
app_email = "mohammedanas18025@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

doc_events = {
    "Sales Partner": {
            "before_insert": [
        "agent_management.customization.sales_partner_customization.set_sales_partner_name"
    ]
    },
    "Sales Order": {
        "before_save": "agent_management.customization.sales_order_comm.set_supplier_sales_partner"
        },
    "Sales Invoice":{
        "before_save":"agent_management.customization.sales_invoice_custom.set_supplier_sales_partner_si",
        "on_submit": ["agent_management.sales_agent.doctype.sales_agent_commission.sales_agent_commission.handle_sales_invoice_on_submit",
                      "agent_management.sales_agent.doctype.sales_agent_commission.sales_agent_commission.sales_invoice_on_submit"], 
        "on_cancel":"agent_management.sales_agent.doctype.sales_agent_commission.sales_agent_commission.handle_sales_invoice_on_cancel"
       
    },
    "Payment Entry":{
        "on_submit":["agent_management.sales_agent.doctype.sales_agent_commission.sales_agent_commission.handle_payment_entry_on_submit",
                     "agent_management.sales_agent.doctype.sales_agent_commission.sales_agent_commission.update_sales_agent_commission_from_payment"]
    }
  
}

override_whitelisted_methods = {
    "erpnext.accounts.doctype.payment_entry.payment_entry.get_party_account":
        "agent_management.agent_management.customization.payment_entry_customisation.get_party_account"
}


doctype_js = {
    "Sales Order": "public/js/sales_order_custom.js",
    "Sales Invoice":"public/js/sales_invoice_custom.js"
}

after_install = [
    "agent_management.customization.sales_partner_customization.create_custom_fields",
    "agent_management.customization.supplier_customization.create_custom_fields",
    "agent_management.customization.sales_order_custom.create_custom_fields",
    "agent_management.customization.sales_invoice_custom_fields.create_custom_fields",
    "agent_management.customization.payment_entry_custom.create_custom_fields"
]

after_migrate = [
    "agent_management.customization.sales_partner_customization.create_custom_fields",
    "agent_management.customization.supplier_customization.create_custom_fields",
    "agent_management.customization.sales_order_custom.create_custom_fields",
    "agent_management.customization.sales_invoice_custom_fields.create_custom_fields",
    "agent_management.customization.payment_entry_custom.create_custom_fields",
    "agent_management.customization.sales_partner_customization.disable_partner_name_mandatory"
]

before_uninstall = [
    "agent_management.customization.sales_partner_customization.delete_custom_fields",
    "agent_management.customization.sales_partner_customization.enable_partner_name_mandatory",
    "agent_management.customization.supplier_customization.delete_custom_fields",
    "agent_management.customization.sales_order_custom.delete_custom_fields",
    "agent_management.customization.sales_invoice_custom_fields.delete_custom_fields",
    "agent_management.customization.payment_entry_custom.delete_custom_fields"
]

# patches = ["agent_management.patches.sales_partner_name.execute"]
# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "agent_management",
# 		"logo": "/assets/agent_management/logo.png",
# 		"title": "Agent Management",
# 		"route": "/agent_management",
# 		"has_permission": "agent_management.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/agent_management/css/agent_management.css"
# app_include_js = "/assets/agent_management/js/agent_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/agent_management/css/agent_management.css"
# web_include_js = "/assets/agent_management/js/agent_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "agent_management/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "agent_management/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "agent_management.utils.jinja_methods",
# 	"filters": "agent_management.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "agent_management.install.before_install"
# after_install = "agent_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "agent_management.uninstall.before_uninstall"
# after_uninstall = "agent_management.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "agent_management.utils.before_app_install"
# after_app_install = "agent_management.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "agent_management.utils.before_app_uninstall"
# after_app_uninstall = "agent_management.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "agent_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"agent_management.tasks.all"
# 	],
# 	"daily": [
# 		"agent_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"agent_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"agent_management.tasks.weekly"
# 	],
# 	"monthly": [
# 		"agent_management.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "agent_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "agent_management.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "agent_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["agent_management.utils.before_request"]
# after_request = ["agent_management.utils.after_request"]

# Job Events
# ----------
# before_job = ["agent_management.utils.before_job"]
# after_job = ["agent_management.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"agent_management.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

