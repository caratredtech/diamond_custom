from os import lseek
from warnings import filters
from webbrowser import get
from requests.exceptions import RetryError
import frappe
import requests
import json
import importlib.util
from frappe.utils import cstr
import traceback
import requests
from frappe.utils import logger
import math
from datetime import datetime
from datetime import date
import sys
# from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import (
#     create_sales_invoice,
# )
# from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import get_outstanding_amount

# from erpnext.accounts.doctype.sales_invoice.sales_invoice import make_sales_return
# from erpnext.controllers.sales_and_purchase_return import make_return_doc


def payment_entry_reference(doc, method=None):
    data = doc.as_dict()
    if len(doc.references)>0:
        if  doc.references[0].reference_name == "Sales Invoice":
            get_sales_data = frappe.get_doc("Sales Invoice", doc.references[0].reference_name)
            sum_outstanding = doc.references[0].allocated_amount
            datetime_obj = datetime.strptime(str(doc.reference_date), '%Y-%m-%d')
            due_date = datetime.strptime(str(get_sales_data.due_date), '%Y-%m-%d')
            diff_date = datetime_obj - due_date
            get_cust = frappe.get_doc("Customer",get_sales_data.customer)
            if get_cust.auto_discount == 1:
                print(int(doc.total_allocated_amount),round(get_sales_data.grand_total),get_sales_data.name)
                if doc.total_allocated_amount == round(get_sales_data.grand_total):
                    if diff_date.days <= 30:
                        amount = 3*get_sales_data.total/100
                        doc_insert = frappe.get_doc({'doctype': 'Auto Discounts', 'posting_date': doc.reference_date,"customer":doc.party,"payment_entry_reference":doc.name,"discount_amount":amount,"discount_applied":"No","sales_invoice_number":get_sales_data})
                        doc_insert.submit()
                        for i in doc.references:
                            print(i.total_amount,i.allocated_amount,(round(i.total_amount)-round(i.allocated_amount)),"______________")
                            frappe.db.set_value('Payment Entry Reference',i.name,"outstanding_amount",(round(i.total_amount)-round(i.allocated_amount)))
                            frappe.db.set_value('Sales Invoice',get_sales_data.name,"outstanding_amount",(round(i.total_amount)-round(i.allocated_amount)))
                            # frappe.db.set_value('Sales Invoice',get_sales_data.name,"outstanding_amount",0.0)
                            frappe.db.set_value('Sales Invoice',get_sales_data.name,"Status","Paid")
                            frappe.db.commit()
                    elif diff_date.days >= 31 and diff_date.days <= 60:
                        amount = 2*get_sales_data.total/100
                        doc_insert = frappe.get_doc({'doctype': 'Auto Discounts', 'posting_date': doc.reference_date,"customer":doc.party,"payment_entry_reference":doc.name,"discount_amount":amount,"discount_applied":"No","sales_invoice_number":get_sales_data})
                        doc_insert.submit()
                        for i in doc.references:
                            print(i.total_amount,i.allocated_amount,(round(i.total_amount)-round(i.allocated_amount)),"______________")
                            frappe.db.set_value('Payment Entry Reference',i.name,"outstanding_amount",(round(i.total_amount)-round(i.allocated_amount)))
                            frappe.db.set_value('Sales Invoice',get_sales_data.name,"outstanding_amount",(round(i.total_amount)-round(i.allocated_amount)))
                            # frappe.db.set_value('Sales Invoice',get_sales_data.name,"outstanding_amount",0.0)
                            frappe.db.set_value('Sales Invoice',get_sales_data.name,"Status","Paid")
                            frappe.db.commit()
                    else:
                        for i in doc.references:
                            print(i.total_amount,i.allocated_amount,(round(i.total_amount)-round(i.allocated_amount)),"______________")
                            frappe.db.set_value('Payment Entry Reference',i.name,"outstanding_amount",(round(i.total_amount)-round(i.allocated_amount)))
                            frappe.db.set_value('Sales Invoice',get_sales_data.name,"outstanding_amount",(round(i.total_amount)-round(i.allocated_amount)))
                            # frappe.db.set_value('Sales Invoice',get_sales_data.name,"outstanding_amount",0.0)
                            frappe.db.set_value('Sales Invoice',get_sales_data.name,"Status","Paid")
                            frappe.db.commit()
                else:
                    # for i in doc.references:
                    #     frappe.db.set_value('Payment Entry Reference',i.name,"outstanding_amount",round(i.total_amount-i.allocated_amount))
                    #     frappe.db.set_value('Sales Invoice',get_sales_data.name,"outstanding_amount",round(i.total_amount-i.allocated_amount))
                    #     frappe.db.commit()
                    if doc.references[0].outstanding_amount == 0.0:
                        if diff_date.days <= 30:
                            amount = 3*get_sales_data.total/100
                            doc_insert = frappe.get_doc({'doctype': 'Auto Discounts', 'posting_date': doc.reference_date,"customer":doc.party,"payment_entry_reference":doc.name,"discount_amount":amount,"discount_applied":"No","sales_invoice_number":get_sales_data})
                            doc_insert.submit()
                        elif diff_date.days >= 31 and diff_date.days <= 60:
                            amount = 2*get_sales_data.total/100
                            doc_insert = frappe.get_doc({'doctype': 'Auto Discounts', 'posting_date': doc.reference_date,"customer":doc.party,"payment_entry_reference":doc.name,"discount_amount":amount,"discount_applied":"No","sales_invoice_number":get_sales_data})
                            doc_insert.submit()
                        else:
                            # frappe.("No Discount")
                            pass
    else:
        pass

        
def on_cancel_payment(doc, method=None):
    if len(doc.references):
        if  doc.references[0].reference_name == "Sales Invoice":
            for i in doc.references:
                get_sales_data = frappe.get_doc("Sales Invoice", doc.references[0].reference_name)
                frappe.db.set_value('Payment Entry Reference',i.name,"outstanding_amount",(round(i.total_amount)))
                frappe.db.set_value('Sales Invoice',get_sales_data.name,"outstanding_amount",(round(i.total_amount)))
                # frappe.db.set_value('Sales Invoice',get_sales_data.name,"outstanding_amount",0.0)
                frappe.db.commit()
    else:
        pass
                
def fetch_discount(doc, method=None):
    try:
        #get last Auto discounts based on customer
        get_last_discount = frappe.get_last_doc('Auto Discounts',filters={"customer":doc.customer})
        #if discounts exist get last sales invoice of the customer
        get_last_invoice = frappe.get_last_doc('Sales Invoice',filters={"customer":doc.customer})
        from frappe.utils import money_in_words
        in_words = money_in_words(doc.grand_total-get_last_discount.discount_amount)
        get_value=frappe.db.set_value('Sales Invoice',get_last_invoice.name,{
            # "total":round(doc.grand_total-get_last_discount.discount_amount),
            "auto_discount_amount":get_last_discount.discount_amount,
            "auto_discount_number":get_last_discount.name,
            "grand_total":round(doc.grand_total-get_last_discount.discount_amount),
            "rounding_adjustment":round(get_last_discount.discount_amount),
            "rounded_total":round(doc.grand_total-get_last_discount.discount_amount),
            "grand_total":doc.grand_total-get_last_discount.discount_amount,
            "outstanding_amount":round(doc.grand_total-get_last_discount.discount_amount),
            "discount_against_sales_invoice":get_last_discount.sales_invoice_number,"in_words":in_words,
            "base_total":doc.grand_total-get_last_discount.discount_amount,
            "base_rounded_total":doc.grand_total-get_last_discount.discount_amount,
            "base_grand_total":doc.grand_total-get_last_discount.discount_amount,
            "amount_eligible_for_commission":doc.grand_total-get_last_discount.discount_amount,
            "base_net_total":doc.grand_total-get_last_discount.discount_amount,
            # "net_total":doc.grand_total-get_last_discount.discount_amount
            })
    
        frappe.db.commit()
        for each_item in get_last_invoice.payment_schedule:
            get_doc=frappe.db.set_value('Payment Schedule',each_item.name,{"payment_amount":round(doc.grand_total-get_last_discount.discount_amount)
                                                                    ,"outstanding":round(doc.grand_total-get_last_discount.discount_amount),
                                                                    "base_payment_amount":round(doc.grand_total-get_last_discount.discount_amount)
                                                                    })
        
            frappe.db.commit()
    except Exception as e:
        print(e,"=============")
        
        
# def sales_order_fetch_discount(doc, method=None):
#     try:
#         #get last Auto discounts based on customer
#         get_last_discount = frappe.get_last_doc('Auto Discounts',filters={"customer":doc.customer})
#         #if discounts exist get last sales invoice of the customer
#         get_last_invoice = frappe.get_last_doc('Sales Invoice',filters={"customer":doc.customer})
#         from frappe.utils import money_in_words
#         in_words = money_in_words(doc.grand_total-get_last_discount.discount_amount)
#         get_value=frappe.db.set_value('Sales Invoice',get_last_invoice.name,{
#             # "total":round(doc.grand_total-get_last_discount.discount_amount),
#             "auto_discount_amount":get_last_discount.discount_amount,
#             "auto_discount_number":get_last_discount.name,
#             "grand_total":round(doc.grand_total-get_last_discount.discount_amount),
#             "rounding_adjustment":round(get_last_discount.discount_amount),
#             "rounded_total":round(doc.grand_total-get_last_discount.discount_amount),
#             "grand_total":doc.grand_total-get_last_discount.discount_amount,
#             "outstanding_amount":round(doc.grand_total-get_last_discount.discount_amount),
#             "discount_against_sales_invoice":get_last_discount.sales_invoice_number,"in_words":in_words,
#             "base_total":doc.grand_total-get_last_discount.discount_amount,
#             "base_rounded_total":doc.grand_total-get_last_discount.discount_amount,
#             "base_grand_total":doc.grand_total-get_last_discount.discount_amount,
#             "amount_eligible_for_commission":doc.grand_total-get_last_discount.discount_amount,
#             "base_net_total":doc.grand_total-get_last_discount.discount_amount,
#             # "net_total":doc.grand_total-get_last_discount.discount_amount
#             })
    
#         frappe.db.commit()
#         for each_item in get_last_invoice.payment_schedule:
#             get_doc=frappe.db.set_value('Payment Schedule',each_item.name,{"payment_amount":round(doc.grand_total-get_last_discount.discount_amount)
#                                                                     ,"outstanding":round(doc.grand_total-get_last_discount.discount_amount),
#                                                                     "base_payment_amount":round(doc.grand_total-get_last_discount.discount_amount)
#                                                                     })
        
#             frappe.db.commit()
#     except Exception as e:
#         print(e,"=============")
                
        
def discount_def(doc, method=None):
    if doc.customer_discount_category:
        get_ddef = frappe.get_doc("Discount Definitions", doc.customer_discount_category)
        if not frappe.db.exists("Pricing Rule",{"customer":doc.name}):
            for i in get_ddef.discount:
                # if i.discount_type == "Percentage":
                get_data_pricingrule = frappe.get_doc({"doctype":"Pricing Rule","title":"Customer Discount","apply_on":"Item Group","selling":1,"applicable_for":"Customer","sytem_generated":"Yes","customer":doc.name,"discount_percentage":i.amount,"priority":16,"rate_or_discount":"Discount Percentage","apply_multiple_pricing_rules":1,"item_groups":[i.as_dict()]})
                get_data_pricingrule.insert()
                # discount_doc = frappe.get_doc({"doctype":"Pricing Rule Mapping","customer":doc.name,"item_group":i.item_group,"discount":i.amount,"discount_definition_reference":doc.customer_discount_category,"rule_reference":get_data_pricingrule.name})
                # discount_doc.insert()
            # else:
            #     get_data_pricingrule = frappe.get_doc({"doctype":"Pricing Rule","title":"Customer Discount","apply_on":"Item Group","selling":1,"applicable_for":"Customer","customer":doc.name,"sytem_generated":"Yes","discount_percentage":i.amount,"rate_or_discount":"Discount Amount","priority":18,"apply_multiple_pricing_rules":1,"item_groups":[i.as_dict()]})           
            #     get_data_pricingrule.insert()
            #     discount_doc = frappe.get_doc({"doctype":"Pricing Rule Mapping","customer":doc.name,"item_group":i.item_group,"discount":i.amount,"discount_definition_reference":doc.customer_discount_category,"rule_reference":get_data_pricingrule.name})
            #     discount_doc.insert()
                
# def discount_update(doc, method=None):
#     get_mapping = frappe.db.get_list("Pricing Rule Mapping",fields=["name","item_group","discount","rule_reference"])
#     for i in get_mapping:
#         for j in doc.discount:
#             if i.item_group == j.item_group:
#                 frappe.db.set_value("Pricing Rule Mapping",i.name,"discount",j.amount)
#                 frappe.db.set_value("Pricing Rule",i.rule_reference,"discount_percentage",j.amount)
#                 frappe.db.commit()  
                
                
# def discount_update(doc, method=None):
#     print(doc,"///////")
#     get_customer_detail = frappe.db.get_list("Customer",{"customer_discount_category":doc.name},["name"])
#     # print(get_customer_detail,"////ccccccccddddddddddd")
#     get_group_discount_amount = frappe.db.get_list("Discount Definitions Item",{"parent":doc.name},["item_group","amount"])
#     # print(get_group_discount_amount,"/ddddddddddddddddd")
#     for i in get_customer_detail:
#         # print(i,"........................")
#         get_pricing_rules = frappe.db.get_list("Pricing Rule",{"title":"Customer Discount","customer":i["name"]},{"name"})
#         # print(get_pricing_rules,"/////////prrrrrrrrrrrrrrrrr")
#         if len(get_pricing_rules):
#             # print(get_pricing_rules,"/////////prrrrrrrrrrrrrrrrr")
#             for j in get_pricing_rules:
#                 get_group = frappe.db.get_list("Pricing Rule Item Group",{"parent":j['name']},["item_group"])
#                 for k in get_group_discount_amount:
#                     if get_group[0]['item_group'] == k["item_group"]:
#                         print(k["item_group"])
#                         frappe.db.set_value("Pricing Rule",j["name"],"discount_percentage",k["amount"])
#                         frappe.db.commit()


                
def discount_update(doc, method=None):
    # print(doc,"///////")
    get_customer_detail = frappe.db.get_list("Customer",{"customer_discount_category":doc.name},["name"])
    get_group_discount_amount = frappe.db.get_list("Discount Definitions Item",{"parent":doc.name},["item_group","amount"])
    for customer in get_customer_detail:
        get_pricing_rules = frappe.db.get_list("Pricing Rule",{"title":"Customer Discount","customer":customer["name"]},{"name","discount_percentage"})
        if len(get_pricing_rules):
            for pricing_rule in get_pricing_rules:
                get_group = frappe.db.get_list("Pricing Rule Item Group",{"parent":pricing_rule['name']},["item_group"])
                for discount in get_group_discount_amount:
                    if get_group[0]['item_group'] == discount["item_group"] and pricing_rule['discount_percentage'] != discount["amount"]:
                        print(discount["item_group"])
                        frappe.db.set_value("Pricing Rule",pricing_rule["name"],"discount_percentage",discount["amount"])
                        frappe.db.commit()
  
  
 
def create_auto_discount(doc,method=None):
    # print(doc.as_dict(),"/////////////////////")
    # Payment entry before sales invoice days , Auto Discount is create
    try:
        if doc.paid_to != "Rate Differance - DMPL":
            if frappe.db.exists('Customer',{"name":doc.party,"auto_discount":1}):
                payment_date = datetime.strptime(doc.posting_date, '%Y-%m-%d').date()
                if len(doc.references) > 0:
                    for i in range(len(doc.references)):
                        if doc.references[i].reference_doctype =="Sales Invoice":
                            
                            sales_date = frappe.db.get_list("Sales Invoice",{"name":doc.references[i].reference_name},["name","customer",'posting_date','base_net_total','status'])
                            # print(sales_date,"////////////////////,,,,,,,,,,,,,,,,,")
                            date_limit = (payment_date - sales_date[0]["posting_date"]).days
                            
                            # If payment of sales invoice outstanding is zero than this condition is apply.
                            
                            if date_limit <=15 and doc.references[i].outstanding_amount == 0:
                                # print("15.............................")
                                customer_detail = frappe.db.get_list("Customer",{"name":doc.party},['0_to_15_days_auto_discount'])
                                if float(customer_detail[0]["0_to_15_days_auto_discount"]):
                                    base_net_total = sales_date[0]['base_net_total']
                                    discount_amount = base_net_total*(float(customer_detail[0]["0_to_15_days_auto_discount"])/100)
                                    auto_data = frappe.get_doc({
                                        "doctype":"Auto Discounts",
                                        "posting_date" :payment_date,
                                        "customer":doc.party,
                                        "payment_entry_reference":doc.name,
                                        "discount_applied":"Yes",
                                        "discount_amount":discount_amount,
                                        "sales_invoice_number":doc.references[i].reference_name
                                    })
                                    auto_data.docstatus = 0
                                    auto_data.insert()
                                    frappe.db.commit()
                            
                            elif date_limit >= 16  and date_limit <= 30 and doc.references[i].outstanding_amount == 0:
                                # print("16................................")
                                
                                customer_detail = frappe.db.get_list("Customer",{"name":doc.party},['30_days_discount'])
                                if float(customer_detail[0]["30_days_discount"]):
                                    base_net_total = sales_date[0]['base_net_total']
                                    discount_amount = base_net_total*(float(customer_detail[0]["30_days_discount"])/100)
                                    auto_data = frappe.get_doc({
                                        "doctype":"Auto Discounts",
                                        "posting_date" :payment_date,
                                        "customer":doc.party,
                                        "payment_entry_reference":doc.name,
                                        "discount_applied":"Yes",
                                        "discount_amount":discount_amount,
                                        "sales_invoice_number":doc.references[i].reference_name
                                    })
                                    auto_data.docstatus = 0
                                    auto_data.insert()
                                    frappe.db.commit()
                            
                            elif date_limit >= 31 and date_limit <=45 and doc.references[i].outstanding_amount == 0:
                                # print("31...............................")
                                
                                customer_detail = frappe.db.get_list("Customer",{"name":doc.party},['31_to_45_days_auto_discount'])
                                if float(customer_detail[0]["31_to_45_days_auto_discount"]):
                                    base_net_total = sales_date[0]['base_net_total']
                                    discount_amount = base_net_total*(float(customer_detail[0]["31_to_45_days_auto_discount"])/100)
                                    auto_data = frappe.get_doc({
                                        "doctype":"Auto Discounts",
                                        "posting_date" :payment_date,
                                        "customer":doc.party,
                                        "payment_entry_reference":doc.name,
                                        "discount_applied":"Yes",
                                        "discount_amount":discount_amount,
                                        "sales_invoice_number":doc.references[i].reference_name
                                    })
                                    auto_data.docstatus = 0
                                    auto_data.insert()
                                    frappe.db.commit()
                                        
                            elif date_limit <= 60 and doc.references[i].outstanding_amount == 0:
                                # print("60...........................")
                                
                                customer_detail = frappe.db.get_list("Customer",{"name":doc.party},['60_days_discount'])
                                
                                if float(customer_detail[0]["60_days_discount"]):
                                    base_net_total = sales_date[0]['base_net_total']
                                    discount_amount = base_net_total*(float(customer_detail[0]["60_days_discount"])/100)
                                    auto_data = frappe.get_doc({
                                        "doctype":"Auto Discounts",
                                        "posting_date" :payment_date,
                                        "customer":doc.party,
                                        "payment_entry_reference":doc.name,
                                        "discount_applied":"Yes",
                                        "discount_amount":discount_amount,
                                        "sales_invoice_number":doc.references[i].reference_name
                                    })
                                    auto_data.docstatus = 0
                                    auto_data.insert()
                                    frappe.db.commit()
                            else:
                                pass
                        else:
                            pass            
                else:
                    if not frappe.db.exists("Auto Discounts",{"name":doc.reference_no}):
                        customer_detail = frappe.db.get_list("Customer",{"name":doc.party},['discount_on_advance'])
                        if float(customer_detail[0]["discount_on_advance"]):
                            discount_amount = (doc.paid_amount*float(customer_detail[0]["discount_on_advance"]))/100
                            auto_data = frappe.get_doc({
                                "doctype":"Auto Discounts",
                                "posting_date" :payment_date,
                                "customer":doc.party,
                                "payment_entry_reference":doc.name,
                                "discount_applied":"Yes",
                                "discount_amount":discount_amount,
                            })
                            # auto_data.docstatus = 0
                            auto_data.insert()
                            frappe.db.commit()
                        else:
                            pass
                    else:
                        pass
            else:
                pass
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc()), "create_auto_discount")
  
def apply_auto_discount_sum_into_sales_inv_total_adv(doc,method=None):
    try:
        # print(doc.as_dict(),"/////////////////////")
        if method == "on_submit":
            auto_discount_payment_entry = frappe.get_doc({
                "doctype":"Payment Entry",
                "party_type":"Customer",
                "party":doc.customer,
                "paid_from":doc.account_paid_from,
                "paid_to":doc.account_paid_to,
                "paid_amount":doc.discount_amount,
                "received_amount":doc.discount_amount,
                "reference_no":doc.name,
                "reference_date":doc.created_on,
                "cost_center":"Main - DMPL"
            })
            auto_discount_payment_entry.docstatus = 1
            auto_discount_payment_entry.insert()
            frappe.db.commit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc()), "apply_auto_discount_sum_into_sales_inv_total_adv")
