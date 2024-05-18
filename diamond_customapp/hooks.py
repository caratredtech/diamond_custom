from . import __version__ as app_version

app_name = "diamond_customapp"
app_title = "Diamond Customapp"
app_publisher = "kiran@caratred.com"
app_description = "custom app for diamond"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "kiran@caratred.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/diamond_customapp/css/diamond_customapp.css"
# app_include_js = "/assets/diamond_customapp/js/diamond_customapp.js"

# include js, css files in header of web template
# web_include_css = "/assets/diamond_customapp/css/diamond_customapp.css"
# web_include_js = "/assets/diamond_customapp/js/diamond_customapp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "diamond_customapp/public/scss/website"

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

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }
fixtures = [
    {
        "dt":
        "Custom Field",
        "filters": [[
            "name",
            "in",
            [
                # "Purchase Order-po_type",
                # "Purchase Order-chaser_name",
                # "Payment Request-role_permission",
                'Sales Order Item-additional_customer_discount',
                'Sales Order-customer_discount_category'
                'Customer-customer_discount_category',
                'Pricing Rule-sytem_generated',
                'Sales Invoice-customer_discount_category', 
                "Sales Invoice Item-additional_discount",
				"Purchase Invoice Item-additional_discount",
				"Auto Discounts-account_paid_from",
				"Auto Discounts-account_paid_to",
				"Customer-30_days_discount",
				"Customer-60_days_discount",
				"Customer-discount_on_advance",
				"Customer-0_to_15_days_auto_discount",
				"Customer-31_to_45_days_auto_discount",
                ]
        ]]
    },
]

# Generators
# ----------
jenv = {
	"methods": [
		"get_jinja_data:erpnext.accounts.utils.get_balance_on"
	]
}
# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "diamond_customapp.install.before_install"
# after_install = "diamond_customapp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "diamond_customapp.uninstall.before_uninstall"
# after_uninstall = "diamond_customapp.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "diamond_customapp.notifications.get_notification_config"

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

doc_events = {
	# "Payment Entry": {
    # #  "after_insert": "diamond_customapp.events.payment_entry_reference_on_submit",
	#  "on_submit": "diamond_customapp.events.payment_entry_reference",
	#  "on_cancel":"diamond_customapp.events.on_cancel_payment"
	# },
	# "Sales Invoice": {
	# 	"after_insert": "diamond_customapp.events.fetch_discount",
	# 	"on_submit":"diamond_customapp.events.fetch_discount",
	# 	# "on_update":"diamond_customapp.events.fetch_discount"		
	# },
	"Customer": {
		"on_update":"diamond_customapp.events.discount_def"
	},
	"Discount Definitions": {
		"on_update":"diamond_customapp.events.discount_update"
	},
 	"Payment Entry":{
		"on_submit":"diamond_customapp.events.create_auto_discount"
	},
	"Auto Discounts":{
		"on_submit":"diamond_customapp.events.apply_auto_discount_sum_into_sales_inv_total_adv"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"diamond_customapp.tasks.all"
# 	],
# 	"daily": [
# 		"diamond_customapp.tasks.daily"
# 	],
# 	"hourly": [
# 		"diamond_customapp.tasks.hourly"
# 	],
# 	"weekly": [
# 		"diamond_customapp.tasks.weekly"
# 	]
# 	"monthly": [
# 		"diamond_customapp.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "diamond_customapp.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "diamond_customapp.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "diamond_customapp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"diamond_customapp.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []