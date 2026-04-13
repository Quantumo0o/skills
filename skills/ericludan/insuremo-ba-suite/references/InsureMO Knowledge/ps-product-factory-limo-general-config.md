# LIMO General Configuration Guide — KB Reference
# Version 1.0 | 2026-03-25

> Sourced from: InsureMO LIMO General Configuration Guide (HTML export)
> This is a REFERENCE document — not a configuration specification.

---

## Screen IDs Found

- `LIProductGeneralcfgRole_edit_default`

---


# LIMO General Configuration Guide

For tenant general information, user can be defined under General Information.
Use ’LIProductGeneralcfgRole_edit_default’ role to do edit button control.


## I. General Configuration


### I.1. Codetable & Business Table

I.1.1. Dynamic Codetable
The dynamic code table is used to define the master data of tenant. Tenant users are allowed to modify the records under the code table. But the code table list is at the platform level and user cannot edit.
Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.
Definition Method:
Input the search criteria and click the search icon, or click the filter icon next to Maintained By and choose to search by either Tenant or Platform codetables. Click Ok to search or Reset to clear the search criteria.
Click View under the action, which will show data list under the Dynamic Codetable.
Click New and input all the required information and the mandatory information must be filled in.
Click Save to save the record after all data entered, or else click Back to cancel the creation.
Find the target codetable and click Edit under the action to jump to the edit page. Click Add under the list and input code and description. Press Save store the current data, Back to leave the current page, Download to download template file, and Upload to insert data by upload excel file.
Also can create code table from Business Table, click New from Business Table button. Input the table name and description, select the required business table in field Data Source, select the column which defined as code and description
Field Descriptions
This function used to setup the tenant level code description. Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.
Function used to setup the business table, also can be the data source of Dynamic Codetable. Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.
In tab of ‘Table Information’ user can add the required the column, first two ‘ID’, ‘Code’ are default column.
Input the required records.


### I.2. Rate and Rounding Settings

I.2.1. Rounding Rule for Formula
Configure Rounding Rules provides the flexibility to configure different rounding rules to different calculation formula or the same formula under different products. Also different rounding rules can be configured according to different currencies. Value will be stored in db code table t_rounding_config.
Provide the test function to check the result.
If the rounding rule is not defined in this table, it will follow the default rounding rule. Current rounding rule is as following: if is Rupee (Indian) will round to the nearest 5 cents, the precision number is 6. If is not Rupee (Indian) will round to the nearest 5 cents, the precision number is 2.
Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.
Definition Method:
Input the search criteria then click Search to find the target record. If need, click Reset to clear search criteria.
Click Create and input all the required information and the mandatory information must be filled in. For formula preview after settling the formula click Save to save the record after all data entered, or else click Close to cancel the creation.
Find the target record and click Edit under the action to change the information in edit box.
Click Save to confirm the change, or else click Close to cancel the action.
Finding the target records and pitch on. Click Delete, then delete check box will pop up.
Click Yes to confirm the delete, or else click No to cancel the action.
After see following message delete successfully.
Field Description:
Which used to define the tenant level rounding rule. Data is store in the ratetable Default Rounding Configuration, which means after definition the ratetable need to deploy to target environment.
During the calculation process, one formula will only use one rounding , either tenant level or formula level. For formula which has formula level rounding definition (part I.5 Rounding Rule for Formula), will use it. Else, will use tenant level rounding if defined. If no will use the default rounding rule (Rounding Type: Round, Precision Number: 2) at the end
Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.
Field Description:
Refer to part I.2.1. Rounding Rule for Formula.
In this section, user can set the service rate for each rate type. All service rates set here are used to calculate interest for different transactions. Value of the service rate will be stored in db code table t_service_rate.
Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.
Definition Method:
Input the search criteria then click Search to find the target record. If need, click Reset to clear search criteria.
Click New and input all the required information and the mandatory information must be filled in.
Click Save to save the record after all data entered, or else click Close to cancel the creation.
Find the target record and click Edit under the action then change the information in edit box.
Click Save to confirm the change, or else click Close to cancel the action.
Find the target records and pitch on. Click Delete, then delete check box will pop up.
Click Yes to confirm the delete, or else click No to cancel the action.
After see following message delete successfully.
Field Description:
If the Product field is left empty, the current interest rate definition is applicable to ALL products/riders, except those with separate definitions.
As the table above shows, four interest rate definitions (same Interest Type and Product) start on different effective dates with different interest rates.
If a policy or account’s interest is expected to be settled on 23/09/2013, then the interest rate is 5(%), no matter when the interest is actually settled.
If a policy or account’s interest is expected to be settled on 30/11/2013, then the interest rate is 5.5(%), no matter when the interest is actually settled.
If a policy or account’s interest is expected to be settled on 01/02/2014, then the interest rate is 5.8(%), no matter when the interest is actually settled.
As the table above shows:
If the policy for interest settlement is of Product_01, then the interest rate is 5(%).
If the policy for interest settlement is of Product_02 (or any other product except ‘Product_01’) , then the interest rate is 5.5(%).
This page is used to define the Consumer Price Index (CPI) rate per tenant. This is used in Product Configuration -> Product Detail -> Product -> NB Rules -> Indexation Info and only when CPI is selected as the Indexation Type.
Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.
Definition Method:
Input the search criteria then click Search to find the target record. If need, click Reset to clear search criteria.
Click New and input all the required information and the mandatory information must be filled in.
Click Save to save the record after all data entered, or else click Close to cancel the creation.
Find the target record and click Edit under the action to change the information in edit box.
Click Save to confirm the change, or else click Close to cancel the action.
Finding the target records and pitch on. Click Delete, then delete check box will pop up.
Click Yes to confirm the delete, or else click No to cancel the action.
After see following message delete successfully.
Field Description:


### I.3. Account Management

I.3.1. Poilcy Account Type
This function used to config the account type on policy, which is not related to product.
Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.
Definition Method:
Click New to create records, click edit icon under action to modify the data.
Field Description:
Normal Question & Answer
Interest settlement and capitalization are two separate operations, with interest settlement performed before capitalization.
Interest is calculated based on the annual interest rate and the interest calculation period, using a daily calculation method.
Formulas for interest calculation:
Where:
p: Principal amount used for interest calculation
r: Annual interest rate
d: Number of interest accrual days, [startDate, endDate), inclusive of startDate and exclusive of endDate (the day of endDate is not counted in the accrual period).StartDate is typically the last interest settlement date; endDate is the current date when the account is being processed.
If the account uses compound interest calculation, the system currently supports daily interest calculation. After interest is calculated, it is immediately rolled into the principal.
If simple interest is used, the calculated interest is first stored in the field policyAccount.uncapitalizedInterest. It will only be added to the principal amount for interest calculation when the account reaches its scheduled Capitalization date.
When calling the LIMO policyAccount API, if the processDate is on or after the Capitalization date, the API will perform the capitalization process.
During project implementation, the capitalization action is typically triggered under two different scenarios:
The specific batch job name may vary by project and should be confirmed with the respective project team. LIMO provides policyAccount processing APIs (/magneto/rest/policy/policyaccount/interest/settlement) that can be invoked by project-specific batch jobs.
This page is used to define the virtual accounts allowed for products. All virtual accounts defined here will appear in Product Configuration -> Product Detail -> Product -> ILP -> Virtual Account -> Product Allowed Virtual Account.
Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.
Definition Method:
Input the search criteria then click Search to find the target record. If need, click Reset to clear search criteria.
Click New and input all the required information and the mandatory information must be filled in.
Click Save to save the record after all data entered, or else click Close to cancel the creation.
Find the target record and click Edit under the action to change the information in edit box.
Click Save to confirm the change, or else click Close to cancel the action.
Finding the target records and pitch on. Click Delete, then delete check box will pop up.
Click Yes to confirm the delete, or else click No to cancel the action.
After see following message delete successfully.
Field Description:
This page is used to define the different risk types available for the product.  NOTE: Only Enabled risk types will appear in Product Configuration -> Product Definition -> Product -> Common Servicing Rules -> Product Risk Aggregation.
Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.
Definition Method:
Input the search criteria then click Search to find the target record. If need, click Reset to clear search criteria.
Click New and input all the required information and the mandatory information must be filled in.
Click Save to save the record after all data entered, or else click Close to cancel the creation.
Find the target record and click Edit under the action to change the information in edit box.
Click Save to confirm the change, or else click Close to cancel the action.
Field Description:


### I.4. Advanced Configuration Options

I.4.1. Entity Extended Fields Define
Function used to defined the extended fields for other elements like fund, liability.
Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.
Definition Method:
To create a new field, click New button at the bottom of the screen.
To change any information on the field, click Edit under Action column.
3. Disable / Enable
To disable or enable one of the created fields, click Enabled/Disabled under Action column.
Field Description:
This feature is primarily designed for exporting tenant-level configuration data and is intended to be used with the “Tenant Skin Export” menu. The goal is to facilitate the reuse of configurations between similar tenants with more convenient and reusable.
Only user with role (LITenantSkinRole_export_default) can export the data, else will be readonly.
Currently supported the data under following dialog which will shown after click button New, select the requied items, than click Export. After the process finished download the file to the local desk.
This feature is primarily designed for importing tenant-level configuration data and is intended to be used with the “Tenant Skin Import” menu. The goal is to facilitate the reuse of configurations between similar tenants with more convenient and reusable.
Only user with role (LITenantSkinRole_import_default) can import the data, else will be readonly.
Click the Upload button, select the local file. If status is failed, download the information to see the detail.
This function used to define the translation data under current tenant. Following parts are not included:
Only user with edit role (LIProductGeneralcfgRole_edit_default) can import the data, else will be readonly.


## II. Business Configuration


### II.1. Annuity Option

Annuity Option is used to defined the option applicable for product including option name, joint life or single life and increased percentage, etc. All options defined here will be used on product configuration menu: Servicing Rules -> Annuity Servicing Rules -> Product Annuity Option -> ‘Allowed Annuity Option’ dropdown list. Value of Annuity Option will be stored in db code table t_product_annuity_option.
Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.
Definition Method:
Click the search or filter icon, input or select the required information and click Search / Ok. Click Reset to clear all search conditions.
After finding the target record, click View under the action, which will show details of the Annuity Option.
Click New and input all the required information and the mandatory information must be filled in.
Click Save to save the record after all data entered, or else click Close to cancel the creation.
Find the record which needs to be copied from and click Copy under the action to input all the required information. Click Save to save the record after all data entered, or else click Close to cancel the creation.
Find the target record and click Edit under the action to change the information in edit box.
Click Save to confirm the change, or else click Close to cancel the action.
Find the target record and pitch on. Click Delete, then delete check box will pop up.
Click Yes to confirm the delete, or else click No to cancel the action.
System will do the automatic check whether the Annuity Option had been used in the system, and return the message correspondingly.
Field Description:


### II.2. Workdays Setup

This page is used to define the workdays for a particular country. Only one [tenant]country can be defined.
Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.
Define the [tenant]country that needs to be edited
Choose the year and month that needs to be edited and click search
Adjust as necessary and press ‘Save Calendar’ once done.


### II.3. Basic Information

This page is used to define the tenant basic information, like tenant data formate and the tenant default currency.
Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.


## III. Sales Configuration


### III.1. Sales Meta Data

In this section, user can define the sales related information. Currently 2 parts in Sales Meta Data :
Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly. Users can only modify the tenant records from themselves and cannot modify the platform records.
In Sales Category part, defined the product sales category which used on report, etc. User can modify tenant data, for platform data only to disable and enable. Value will be stored in db code table t_sales_type.
Definition Method:
Click the search or filter icon, input or select the required information and click Search/Ok. For the sort button, user can sort the data to help finding the required record.
Click Reset to clear all search conditions.
Click New and input all the required information and the mandatory information must be filled in.
Click Save to save the record after all data entered, or else click Close to cancel the creation.
Finding the target record, click Edit under the action. Change the information in edit box.
Click Save to confirm the change, or else click Close to cancel the action.
Find the target record and click Delete under the action column, then a dialog box will pop up.
Click Yes to confirm the delete, or else click No to cancel the action.
After see following message delete successfully.
Field Description:
In Agent Qualification Type part, we need to define the qualification required to sell this product. If extra qualification types are needed, tenant qualification types can be created as required. For example, if the qualification type required is ‘Health’ for the product, then agent without ‘Health’ qualification cannot sell this product. Value will be stored in db code table t_test_type.
The relationship between product and qualification type needs to be defined in product configuration. Relationship between producer and qualification type will be maintain in sales channel management.
Definition Method:
Click the search icon, input the required information and click Search.
Click Reset to clear the search conditions.
Click New and input the type name.
Click Save to save the record after all data entered, or else click Close to cancel the creation.
Finding the target record, click Edit under the action. Change the information in edit box.
Click Save to confirm the change, or else click Close to cancel the action.
Find the target record and click Delete under the action, then one dialog box will pop up.
Click Yes to confirm the delete, or else click No to cancel the action.
After see following message delete successfully.
Field Description:


### III.2. Product Business Category

Product Business Category is used to define detailed Product Categories used to different products in different purpose. For example, reporting (valuation report), Finance, etc. When the category has been defined here, value will be stored in db code table t_prod_biz_category, and it can be linked to each product in product configuration -> Main and Sales Information -> Sales Information -> Operation Category.
Only user with edit role (LIProductGeneralcfgRole_edit_default) can modify the data, else will be readonly.
Definition Method:
Click the search or filter icon, input or select the required information and click Search/Ok. Click Reset to clear the search conditions.
Click New and input all the required information and the mandatory information must be filled in.
Click Save to save the record after all data entered, or else click Close to cancel the creation.
Finding the target record, click Edit under the action. Change the information in edit box.
Click Save to confirm the change, else click Close to cancel the action.
Find the target record and pitch on. Click Delete, then delete check box will pop up.
Click Yes to confirm the delete, or else click No to cancel the action.
System will do the automatic check whether the Product Business Category had been used in the system, and return the message correspondingly.
Field Description:


## IV. Audit Trail

The section store the audit trial during the product configuration period. Current following action will be triggered to create records in audit trial.
Definition Method:
Input the search criteria then click Search to find the target record. If need, click Reset to clear search criteria.
Field Description:


## On this page

×Hi, I'm AskInsureMO. Click me and start chatting.×Drag me anywhere freely./li_product_design/limo_general_configuration_guide
