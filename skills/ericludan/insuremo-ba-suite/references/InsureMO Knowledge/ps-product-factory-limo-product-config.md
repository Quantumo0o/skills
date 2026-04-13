# Life Insurance Product Configuration Guide — KB Reference
# Version 1.0 | 2026-03-25

> Sourced from: LIMO Product Definition Guide (limo_product_definition_guide)
> Purpose: Config path verification for Gap Analysis (Agent 1)
> Relevance: VUL/ILP = CORE, HIGH = High relevance, MEDIUM = Medium relevance

---


# Life Insurance Product Configuration Guide

Life Insurance Product Configuration Guide


## I. Main and Sales Information **[HIGH — min/max premium, min PFV]**

Main and Sales Information The Main and Sales Information section allows for the configuration of basic features and sales information related to the product
There are five parts under this section: I.1 Main Information I.2 Sales Information I.3 Product Version I.4 Product Provision I.5 Product Additional Information


### I.1. Main Information **[HIGH — basic product config]**

Main Information The Main Information page allows users to configure all basic information and features related to the product, including details such as Product Name, Product Category, and Pricing currency
note If Extra Information is unnecessary, the section can be removed through Product Module Configuration > Structure Configure > Product Category and Structure Mapping
Basic Information Field NameField DescriptionProduct IDThe Product ID is auto-generated during product creation and cannot be edited in this table
A maximum of 19 characters is allowed.Product CodeThe Product Code is configured in the New Product or Copy Product section and cannot be edited in this table
A maximum of 50 characters is allowed.Tenant CodeThe Organizational Code of the insurance company to which the product belongs, supporting products from different insurance companies.Product NameThe marketing name used to sell the product, e.g., “FLEXILIFE 60 (CB) PAID-UP” or “Super Kid’s Children’s Education Fund”
A maximum of 300 characters is allowed.Product Abbrev
NameA shortened version of the product name, e.g., “FL60(CB)-PU” for “FLEXILIFE 60 (CB) PAID-UP”
A maximum of 300 characters is allowed.Initial CodeThe Initial Code is the same as the Product Code from the beginning


### I.2. Sales Information

Sales Information The Sales Information page is designated for defining all sales-related details of the product, including modifiable fields like Launch Date, Withdraw Date, and Default Currency
This section is organized into five parts: Sales Management Information The Sales Management Information section includes critical dates(Launch Date and Withdraw Date) and setting related to the sales lifecycle of the product
Currency Allowed Table The Currency Allowed Table specifies the allowed policy currencies for each sales branch’s policy
It determines which currencies are presented in the ‘Initial Registration’ dropdown list, ensuring only allowed options are available
Multiple currencies can be allowed for a single branch
For example, the HK branch can allow both HK Dollars and US Dollars
All allowed policy currencies should be configured within this table
Operational Category Table The Operational Category Table is used to configure the operational category for the product according to its usage


### I.3. Product Version

Product Version The Product Version page is used to control different configurations under different product versions
We currently only support the following code tables: Code Tableconfiguret_age_limitAge Limit Tablet_liab_pay_relativeProduct Liability Tablet_liability_config, t_pay_liabilitySB/MB/AI Informationt_liability_configSB/MB/AI Tablet_prem_limitPremium Limit Tablet_product_aggr_riskProduct Risk Aggregationt_product_bonus_defAdvanced Bonus Configurationt_product_cs_ruleCS Rulest_product_pay_modePayment Method Tablet_sa_limitInitial SA limit Table Detailed Steps: See XIV.4
Field Description Field NameField DescriptionVersionThe default value is the product code, users are able to edit the version.Version Start DateThe start date of the version.Version DescriptionThe general description of the target product version.


### I.4. Product Provision

Product Provision The Product Provision page is used to record uploaded provision documents (product clause, etc.) for each product
All types of files can be uploaded (txt, word, excel, etc.)
note This function is only used to upload files or to add file links to the product
Detailed Steps Add Document: Enter the Sequence Number and enable/disable the Upload File
Select the file to be uploaded or add the URL, and click Save
Download Document: Select a document record and click Download on the right
Delete Document: Select a document record using the checkmark box and click Delete
Field Description Field nameField DescriptionSequence NumberThe sequence order of the document, for example, 1, 2, 3, etc.


### I.5. Product Additional Information

Product Additional Information Field Description Field NameField DescriptionInvestment Cash Rider IndicatorConfigure whether the product is an investment key rider
It is normally used for riders
If the attached product is an ILP(Investment Linked Policy) Product, the premium of the investment cash rider will be invested into the main account after deducting charges such as ad-hoc top up
If the attached product is a normal product, the premium of the investment cash rider will be treated as its renewal premium.Cashback Rider IndicatorConfigure whether the product is a cash rider
Its premium aligns with the changes of the attached product premium
When attached to the product terminal or surrendered, the cash-back rider requires a refund of the partial or the total amount of the paid premium.Hybrid IndicatorConfigure whether the product is a hybrid product
If configured as ‘Yes’, first check if it allows to deduct from the Total Investment Value (TIV) during the Non-Forfeiture Option (NFO) process.


## II. Premium ISA Rate Information **[HIGH — SA calculation, premium allocation]**

Premium ISA Rate Information There are two parts under this section: II.1
Premium SA Rate Information II.2


### II.1. Premium SA Rate Information

Premium SA Rate Information This page is designed to configure parameters related to premium and SA calculation, including fields such as Calculation Rules and Age Basis for premium calculation
Premium / Initial SA Calculation Feature Field NameField DescriptionCoverage Term for Premium/Initial SA CalculationConfigure whether ‘Fixed Policy Term’ or ‘Remaining Policy Term’ is used to calculate premium or sum assured
It is usually used for term life products
By default, ‘Fixed Policy Term’ is selected
‘Fixed Policy Term’ means that the product will use the coverage term at policy inception to capture the premium rate, with the premium remaining constant throughout the policy’s life
‘Remaining Policy Term’ means that the product will use the decreasing remaining policy term to recalculate the premium rate annually
For example, if the product coverage term is 10 years and the premium rate for coverage term is 0.1, the rate for year 9 would be 0.09
However, if using the Fixed Policy Term, then the premium will be calculated by 0.1 every year.The Date Options Used to Check Premium Rate Table/Insurance Charge Table in Renewal and CS(Renewal Calculation Date)Configure how ‘Effective Date’ is calculated to capture the premium rate or the insurance charge rate in the Rate Table


### II.2. Product Tariff Type

Product Tariff Type This page is dedicated to managing the tariff types applicable to Variable Annuity Products
A product can allow for multiple tariff types and these tariff types allowed can be selected on the ‘Product Data Entry’ page in New Business
If the product doesn’t apply a Tariff Type, the table can be left empty
Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionTariff TypeTariff Type is a feature used to determine the applicable guarantee charge rate throughout the policy’s life cycle regardless of fund changes
Tariff Type cannot be changed once it is selected in New Business
Here are four types supported in the system currently: - Active - Dynamic - Balance - Income NOTE: Tariff Type is maintained as a business code table, which means it can be modified to accommodate different project requirements (Currently can only be changed in the backend)
For example, if Tariff Type and Investment Scheme are designated as ‘Dynamic’ in New Business, then the Guarantee Charge Rate of Dynamic will be applied to the policy


## III. Liability **[HIGH — SA limits, death benefit, TI benefit]**

Liability The Liability section allows for the configuration of liability related information
There are two parts under this chapter: III.1
Product Liability Table III.2


### III.1. Product Liability Table

Product Liability Table The Product Liability Table page is designed to encompass all liabilities related to the product and to configure the payment information for each listed liability
Product Liability Table This table is used to configure liabilities covered by the product
Related information and basic payment formula for each liability are configured on the Formula page
For Download & Upload function under current menu, Product liability: Download through ’Product Liability Template’ & ’Product Liability Data’; Import through: ’Import Product Liability’ Formula through all liability: Download through ’All Liability Formulae’; Import through: ’Upload All Liability Formulae’ Factor through all liability: Download through ’All Liability Factor’; Import through: ’Upload All Liability Factor’ Accutor through all liability: Download through ’All Liability Accutor’; Import through: ’Upload All Liability Accutor’ Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionLiability CategoryThis field is used to select the category of the liability to be added to the table
After a category is selected, only liabilities under this category will be displayed in the dropdown list for the Liability Name field
The Liability Category is related to the Claim Type
NOTE: The Liability is a business code table that can be modified in different projects.Liability NameThis field is used to select the specific liability covered by the product


### III.2. Optional Liability Config

Optional Liability Config Before configuring the Optional Liability Config page, the Product Liability page must be set up
This page enables users to configure additional liabilities for the product, enhancing its flexibility and reducing redundancy when defining multiple products
When the optional liability indicator is configured as ‘YES’, users can use the ‘edit/view’ icon to configure or view the formula and rate table at the product liability level
Field Description Field nameField DescriptionLiabilityThe type of claim associated with the liability.Optional LiabilityThis field is used to configure whether the liability is optional, allowing for more flexible configurations at the liability level.Liability Calculation RulesThe rules used to calculate the optional liability.Surrender/Termination BasisThis field is used to configure the surrender or termination calculation basic
Here are three options supported: - No SV and no unexpired Premium - Trigger SV formula only - Trigger unexpired premium calculation only


## IV. SB/MB/AI Information **[MEDIUM — SA reduction, surrender benefit]**

SB/MB/AI Information The SB/MB/AI Information section allows for the configuration of Survival Benefit (SB), Maturity Benefit (MB), and Annuity Benefit (AI) information for products
Currently, this menu is configured to display Endowment and Annuity products.


### IV.1. SB/MB/AI Information

SB/MB/AI Information This table is used to configure whether the product has Survival Benefit, Maturity Benefit, or Annuity Installment
Endowment products may have either Survival Benefits or Maturity Benefits, while Annuity products typically feature only Annuity Installments
Field Description Field nameField DescriptionSurvival Benefit Indicator Annuity Installment IndicatorMaturity IndicatorThese fields are used to configure the benefits within the product
Here are three indicators supported: - Survival Benefit - Maturity Benefit - Annual Installment NOTE: Currently a product can only have one MB, SB, or AI.Unit RateThis field is used to configure the value of Unit Rate used in calculation formula
For example, Maturity Benefit formula is configured as ‘MB Rate * SA/Unit Rate’
MB Rate is 1.1 and SA is 50000
If Unit Rate is configured as 1000, then Maturity Benefit will be 50000 * 1.1/1000 = 55
If Unit Rate is configured as 1, then Maturity Benefit will be 50000*1.1/1=55000.


### IV.2. SB/MB/AI Table

SB/MB/AI Table This table is used to configure the benefit payment plan with rates to calculate the payment amount for each kind of benefit
Survival Benefit will be paid according to a pre-configure schedule, so detailed payment plans and rates should be configured in this table
Maturity Benefit will only be paid upon the maturity of the policy, so only the installment rate needs to be configured
For Annuity Installment, annuity installment plan will be configured in Term Limit Table under Common Servicing Rules, so only the payment rate needs to be configured
note Calculation Formula will be configured in Formula Configuration -> Formula List under related calculation type accordingly
![SB/MB/AI_Table](image/limo_product_factory_guide/SBMBAI_Table.PNG) Detail Steps Create configure rates: Step 1: Select the related rates from the Factor List
Step 2: Click Download -> Template to download the Excel file
Step 3: Open the Excel file and add values into the table Step 4: Click Upload and select the Excel file


### IV.3. SB/MB/AI Rate & Allot

SB/MB/AI Rate & Allot This table is used to configure the rate and allot for SB/MB/AI
Detail Steps Bonus Rate: Configure basic information like bonus formula, rate, etc
Bonus Allot: Configure allocation information
Field Description：See VII.4


### IV.4. Survival Benefit

Survival Benefit Option Table This table is used to configure allowed survival benefit options for the product
Multiple options can be selected for the policy
It is mandatory to configure this table if the product includes Survival Benefits
Field Description Field nameField DescriptionSurvival Benefit OptionThis field is used to select SB options allowed for this product
Currently, here are six options supported by the system: 1-To receive SB/CB in cash 2-To use SB/CB to pay premium 3-To leave SB/CB on deposit with Company 4-Option (3) for xx years thereafter Option (2) 5- To use SB/CB to buy additional paid-up sum assured 6- Invest into ILP account IV.4.2
Survival Benefit Frequency This table is used to configure allowed survival benefit payment frequencies for the product
Only the payment frequencies configured in this table can be selected during the survival benefit payment process.Survival Benefit Payment Modal FactorThis field is used to configure the modal factor for survival benefit payment frequencies.


## V. Annuity

Annuity The Annuity section allows for the configuration of Annuity Payment Frequency, Payment Method, Withdraw Payment Frequency, Withdraw Payment Method for GMWB (Guaranteed Minimum Withdrawal Benefit), and Guarantee Options for Variable Annuity Products
There are seven parts under this chapter: V.1
Product Annuity Option V.2
Product Annuity Pay Mode V.3
Product Annuity Frequency V.4
Product Annuity Payout V.5
Product Guarantee Option V.6
Product Withdraw Frequency


### V.1. Product Annuity Option

Product Annuity Option This table is used to configure the allowed annuity options for the product
Field Description Field nameField DescriptionAllowed Annuity OptionThe field is used to select the allowed annuity options that should be pre-configured in Business Configuration ->Annuity Option.


### V.2. Product Annuity Pay Mode

Product Annuity Pay Mode This table is used to configure payment methods allowed for annuity payments for both Fixed Annuity and Variable Annuities
Field Description Field nameField DescriptionAnnuity Pay ModeThis field is used to select payment methods allowed for annuity payments
Only the payment methods configured in this table can be selected in New Business Data Entry or modified by Annuity Update.


### V.3. Product Annuity Frequency

Product Annuity Frequency This table is used to configure payment frequencies allowed for annuity payments for both Fixed Annuity and Variable Annuity products
A Model Factor will also be configured for each payment frequency in this table to calculate installment annuity payout amounts
Field Description Field nameField DescriptionAnnuity Pay FrequencyThis field is used to select payment frequencies allowed for annuity payments
Only the payment frequencies configured in this table can be selected in New Business Data Entry or modified by Annuity Update.Annuity Payment Modal FactorThis field is used to configure the modal factor for each payment frequency
It is registered as a parameter in Formula List and used in formulas to calculate Installment Annuity Payout Amount for Variable Annuity Product.


### V.4. Product Annuity Payout

Product Annuity Payout This table is used to configure allowed Product Annuity Payout options for the product, with multiple options selectable
Field Description Field nameField DescriptionAnnuity Payout OptionThis field is used to select Annuity Payout Options allowed for this product
Here are six options supported by the system: 1-To receive SB/CB in cash 2-To use SB/CB to pay premium 3-To leave SB/CB on deposit with Company 4-Option (3) for xx years thereafter Option (2) 5- To use SB/CB to buy additional paid-up sum assured 6- Invest into ILP account


### V.5. Product Guarantee Option

Product Guarantee Option This table is used to configure Guarantee Options covered by Variable Annuity Product, with multiple options selectable
Field Description Field nameField DescriptionGuarantee OptionThis field is used to select Guarantee Options covered by the product
Selected guarantee options will be available in New Business Product Data Entry for customers to select
Currently here are four options supported: - GMDB (Guaranteed Minimum Death Benefit) - GMAB (Guaranteed Minimum Accumulation Benefit) - GMWB (Guaranteed Minimum Withdrawal Benefit) - GMIB (Guaranteed Minimum Investment Benefit)Is DefaultThis field is used to configure whether the guarantee option selected is the default option by the product
If configured as ‘YES’, then the guarantee option will be automatically selected in New Business Data Entry and cannot be removed
If configured as ‘NO’, then it will be an optional guarantee for customers to select.Accumulation TypeThis field is used to configure accumulation type for each guarantee option selected
Currently here are only two accumulation types supported: Roll Up and Step Up
Different guarantee types can select different accumulation types.Accumulation YearThis field is used to configure accumulation frequency for the accumulation type selected


### V.6. Product Withdraw Mode

Product Withdraw Mode This table is used to configure payment methods allowed for guarantee withdrawals if the product is a Variable Annuity Product with the GMWB option
Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionWithdraw ModeThis field is used to select payment methods allowed for guarantee withdrawals
Only the payment methods configured in this table can be selected in New Business Data Entry or modified by Annuity Update.


### V.7. Product Withdraw Frequency

Product Withdraw Frequency This table is used to configure payment frequencies allowed for guarantee withdrawals if the product is a Variable Annuity Product with the GWMB option
Model Factor will also be configured for each payment frequency in this table to calculate installment withdraw amounts
Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionProduct Withdraw FrequencyThis field is used to select payment frequencies allowed for guarantee withdrawals
Only the frequencies configured in this table can be selected in New Business Data Entry or modified by Annuity Update.Annuity Payment Modal FactorThis field is used to configure Modal Factor for each payment frequency
It is registered as a parameter in Formula List and used in formulates to calculate Installment Withdraw Amount.


## VI. ILP **[VUL CORE — ILP-specific config]**

ILP The ILP section allows for the configuration related to investment products
There are twelve parts under this section: VI.1
Allowed Minimum Invest Periods VI.3
Product Fund Premium Limit Table VI.4
Product Fund Limit Table (ILP Only), new name ‘Product Fund Table’ VI.5
Strategy Allowed Table VI.7
Invest Scheme Allowed VI.8
Top up/Withdrawal Rules VI.11


### VI.1. ILP Rules **[VUL CORE]**

ILP Rules This table is used to configure investment related rules, such as Top Up and Partial Withdrawal
The table is available only for products with investment components
Freelook Field nameField DescriptionFreelook Refund OptionThis field is used to configure the refund amount option for CS-Free Look
When the policy is under free look and configured as the Default Option, the refund amount will be the premium or TIV+ Charge, depending on which is smaller
- Default Option (Min(Premium, TIV+Charge)) - Refund Premium - Refund TIV+Charge VI.1.2
Investment Delay Field nameField DescriptionInvestment Delay OptionThis field is used to configure the investment delay option of the product
For example, if the value is ‘No invest during delay period’, which means there will be no interest accrued during the period from policy issuance day to invest into funds
If configure as option 2 or 3, the ‘Investment Delay Period (Days)’ field should be configure as well


### VI.2. Allowed Minimum Invest Periods **[VUL CORE]**

Allowed Minimum Invest Periods This table is used to configure the minimum invest period under the product, including the number and unit of the period
For products which cover whole life, if a minimum investment period is configured, the policyholder is required to make payments for the entire duration of that period
Once the full payment for the minimum investment period has been met, the policyholder has the option to either cease further payments or continue paying
Field Description Field nameField DescriptionMinimum Investment Period (MIP)This field is used to configure the minimum investment period, which is typically used alongside with the ‘Unit for Minimum Investment Period’ field
For example, if MIP is configured as ‘10’ and the Unit for MIP is ‘Year’, then the minimum investment period is 10 years.Unit for Minimum Investment Period (MIP)This field is to configure the units used for minimum investment period
Currently here are two options supported: - Year - MonthForce Surrender Period (Months)This field is used to configure the force surrender period in months
For example, if the force surrender period is configured as ‘2’, the Initial Premium must be paid for 2 months
After this period, if the premium is not paid by the due date, the policy can be surrendered.


### VI.3. Product Fund Premium Limit Table **[VUL CORE — min/max premium limits]**

Product Fund Premium Limit Table This table is used to configure the limitations of premiums, adhoc top ups, and recurring top ups for each fund at the product level
The global level limitation can be configured in Fund Configuration -> Fund Basic -> Fund Maintain
The system will check the limitations configuration both in this table and in Fund Maintain for validation
Field Description Field nameField DescriptionFundThis field is used to select funds that need to configure limitations on premium, ad-hoc top ups or recurring top ups
If the fund has no limitation or follows the limitations configured at the global level, it does not need to be selected.Payment MethodThis field is used to specify the limitations related to payment method
For example, if the Payment Method is configured as ‘cash’, the initial premium must not be less than 1000; but if the Payment Method is configured as ‘5000’, the initial premium must not be less than 5000.Premium Payment FrequencyThis field is used to specify limitations related to the frequency of premium payments
For example, if the Premium Payment Frequency is configured as ‘monthly’, the initial premium must not be less than 1000; but if the Premium Payment Frequency is configured as ‘yearly’, then the initial premium must not be less than 12000.Min Adhoc Top UpThis field is used to configure the minimum amount allowed for ad-hoc top up in this fund
For example, if the Min Ad-hoc Top Up is configured as ‘1000’, the system will prompt a warning message if the Ad-hoc top up amount in this fund is less than 1000 in CS- Ad-hoc Top Up.Min Recurring Top UpThis field is used to configure the minimum amount allowed for recurring top ups in this fund


### VI.4. Product Fund Limit Table (ILP Only), new name ‘Product Fund Table’

Product Fund Limit Table (ILP Only), new name ‘Product Fund Table’ This table is used to configure the Funds allowed to be invested for this product, as well as limitations for Partial Withdraw and Switch on each fund
If the fund is a ‘Saving Account’ with the fund type as ‘Cumulated Interest Type’, then the fund settlement information needs to be configured in this table
Field Description Field nameField DescriptionFundThis field is used to select funds that can be invested under this product
The funds available for selection are pre-configured in Fund Configuration -> Fund Basic -> Fund Maintain.Min Partial Withdrawal AmountThis field is used to configure the minimum amount allowed for partial withdraw from this fund
For example, if the Min Partial Withdrawal Amount is configured as ‘1000’, the system will prompt a warning message in CS-Partial Withdraw if the withdrawal amount is less than 1000.Min Remaining Amount After Partial WithdrawThis field is used to configure the minimum remaining amount allowed in this fund after partial withdraws
For example, if the Min Remaining Amount After Partial Withdraw is configured as ‘1000’, the system will prompt a warning message in CS-Partial Withdraw if the remaining amount after partial withdraw is less than 1000.Min Switch-out AmountThis field is used to configure the minimum amount allowed to be switched from this fund
For example, if the Min Switch-Out Amount is configured as ‘100’, the system will prompt a warning message in CS-Switch if the switch-out amount is less than 100.Min Remaining Amount after Switch-outThis field is used to configure minimum remaining amount allowed after switch-out from this fund
For example, if the Min Remaining Amount after Switch-out is configured as ‘100’, the system will prompt a warning message in CS-Switch if the total remaining amount after switch-out from the fund is less than 100.Unit Period for No


### VI.5. Product Charge List **[VUL CORE — establishment fee, admin fee, COI]**

Product Charge List This table is used to configure investment charges covered by the product,including how these charges are deducted and calculated
All charges associated with the product should be configured in this table
Field Description Field nameField DescriptionCharge CodeThis field is used to select the charge code available for this product
Here is a list of charges supported in the system and configured in this table: - Expense Fee - Acquisition Expense Loading (Alpha1) - Acquisition Expense Loading (Alpha2) - Acquisition Expense Loading (Beta) - Insurance Charge - Policy Fee - Guarantee Charge - GMAB Charge - GMDB Charge - GMWB Charge - GMIB Charge - Fund Management Fee - UDR Premium - Insurance Tax - Switch Fee - Surrender Charge - Admin Surrender Charge - Freelook Charge New charges can be added without coding if they can be mapped to an existing distribution type for accounting purposes.Fee SourceThis field is used to select the deduction source for the charge selected
Currently, here are 18 options supported: - Deduct from premium (e.g
Expense Fee) - Deducted from fund at bid price (e.g
Insurance Charge) - Deduct from Surrender Amount - For Surrender Charge, Admin Surrender Charge and Free-look Charge - Deduct from Switch Amount (Switch Out Fund) – For Switch Fee - Deduct from Switch Amount (Switch in Fund) – For Switch Fee - Pay additionally per application – For Switch Fee - etc.Calculation BaseThis field is used to select the calculation base for charges with Fee Source as ‘Deducted from fund at bid price’
Here are two options supported: - Policy Level - Fund Level If ‘Policy Level’ is selected, then this charge will be calculated in total (by Total Investment Value or a fixed amount) and then allocated to each fund


### VI.6. Strategy Allowed Table **[VUL CORE]**

Strategy Allowed Table This table is used to configure the investment strategy allowed for the product, which includes both Normal Strategy and DCA Strategy
If the product has Tariff Type, then Strategies allowed can be different for each Tariff Type
Multiple records can be selected and then allowed investment strategies will be available for customers to select in New Business and can be modified during Customer Service
Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionTariff TypeThis field can be selected if allowed investment strategy is different for each tariff type
This field is only used for products with tariff type
If the product does not have a tariff type, the field should be selected as NA
The options are: - Active - Dynamic - Balance - IncomeAllowed StrategyThis field is used to select investment strategies allowed for this product


### VI.7. Invest Scheme Allowed **[VUL CORE]**

Invest Scheme Allowed This table is used to configure Investment Schemes allowed for this product
Multiple records can be selected and then allowed investment schemes will be available for customers to select in New Business and can be modified by Customer Service
Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionScheme NameThis field is used to select investment schemes allowed for the product
Investment Schemes can be preconfigure using (>>) Invest Scheme or through Fund Configuration -> Fund Invest Scheme -> Invest Scheme.


### VI.8. MPV Rules **[VUL CORE — MPV calculation]**

MPV Rules Information about minimum protection value (MPV) for investment products are configure under this page
Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionRider Follow MainThe indicator used to configure whether if the rider product follows the MPV Rule of the attached product.SA MultiplierSA Multiplier is a number used to used to configure the SA multiplier of minimum protection value
For example, if configure as 3, and MPV formula is configure as MPV = MPV_SA_Multiplier * SA = 3 * SA
Multiple records can be inputted.Expiry AgeSA Expiry Age is a number used to configure the allowable expiry age of MPV
For example, it can be configure as 65 and 70
Multiple Records can be inputted.


### VI.9. Virtual Account **[VUL CORE]**

Virtual Account There are three pages under this section: VI.9.1
Product Allowed Virtual Account VI.9.2
Product Virtual Account Setup VI.9.3
Product Account Charge List VI.9.1
Product Allowed Virtual Account This page is used to configure the product level Virtual Accounts
To select the virtual accounts to set up, tick the checkboxes besides the account code
To create new tenant virtual accounts, click on the (>>) icon, which will bring you to General Configuration -> Invest Virtual Account configure Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionAccount CodeThis field is used to configure the code for the virtual account.Account NameThis field is used to configure the name of the virtual account.Account DescriptionThis field is used to provide descriptions for the virtual account


### VI.10. Top up/Withdrawal Rules **[VUL CORE — partial withdrawal, min amount]**

Top up/Withdrawal Rules For ilp, this page is used to configure the rules about top up and withdrawal under different currency
Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionCurrencyThe field is used to configure the currency
For all different currency which has different top up and withdrawal rules, need to configure here.Allow Ad-hoc Top upThis field is used to configure whether ad-hoc top up is allowed or not under target currency.Allow Recurring Top upThis field is used to configure whether recurring top up is allowed or not under target currency.Allow Partial WithdrawThis field is used to configure whether partial withdraw is allowed or not under target currency.Min Partial Withdrawal AmountMax Partial Withdrawal AmountThese fields are used to configure min/max partial withdrawal amount for the selected currency
The min default value is 0 while the max default value is 999999999999999.Min Remaining Amount after Partial WithdrawThis field is used to configure the minimum remaining amount after partial withdraw for the selected currency
The min default value is 0.Free Times Withdraw per Policy YearThis field is used to configure how many free times one can withdraw in one policy year for the selected currency.Regular Partial Withdraw PermitThis field is used to configure whether regular partial withdrawal is allowed or not under target currency.


### VI.11. Recurring Top up Frequency **[VUL CORE]**

Recurring Top up Frequency For ilp, this page is used to configure the recurring top up frequency and amount under different currency
Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionCurrencyThe field is used to configure the currency
For all different currency which has different recurring top up frequency and amount, need to configure here.Recurring Top up FrequencyThis field need to be configure when the recurring top up frequency is a related factor to the amount
There are several options like yearly, half yearly and so on.Min Recurring Top up AmountMax Recurring Top up AmountThese fields are used to configure min/max recurring top up amount for the selected currency and recurring top up frequency.


### VI.12. Regular Withdrawal Limit **[VUL CORE — min/max withdrawal]**

Regular Withdrawal Limit For ilp, this page is used to configure the withdrawal amount related to currency and payment frequency under different currency
Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionCurrencyThe field is used to configure the currency
For all different currency which has different regular withdrawal limit, need to configure here.Premium Payment FrequencyThis field need to be configure when the premium payment frequency is a related factor to the regular withdrawal limit
There are several options like yearly, half yearly and so on.Min Withdrawal AmountMax Withdrawal AmountThese fields are used to configure min/max withdrawal amount for the selected currency and premium payment frequency.


## VII. Bonus

Bonus The Bonus section allows for the configuration of Bonus related information, including Cash Bonuses, Reversionary Bonus, and Terminal Bonus
There are seven parts under this section: VII.1
Welcome Bonus & Allot VII.5
Loyalty Bonus & Allot VII.6
Investment Bonus & Allot VII.7
Other Bonus Configuration This section is only required for participating products.


### VII.1. Cash Bonus

Cash Bonus This section is used to configure whether if the product has a cash bonus, the related rules, and the cash bonus table
Cash Bonus This page determines if the product has a cash bonus and the related rules for the bonus
Field Description VII.1.1.1
Basic Bonus Info Field nameField DescriptionCash Bonus IndicatorThis field is used to determine whether the product has Cash Bonus or not.No
of Completed Policy Years for CB Becoming PayableThis field is used to configure the number of critical years for cash bonus to become payable
For example, if configure as 2, then cash bonus amount will not be deposited into the account during the first 2 years of the policy
Bonus Option Field nameField DescriptionCash Bonus OptionThis field is used to select CB options allowed for this product
Currently, there are 6 options able to be selected: - To receive SB/CB in cash - To use SB/CB to pay premium - To leave SB/CB on deposit with Company - Option (3) for xx years thereafter Option (2) - To use SB/CB to buy an additional paid-up sum assured - Invest into ILP account VII.1.2


### VII.2. Reversionary Bonus

Reversionary Bonus This section is used to configure whether if the product has a reversionary bonus, the related rules, and the Reversionary Bonus Rate
Reversionary Bonus This page determines if the product has a reversionary bonus and the related rules for the bonus
Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionReversionary Bonus IndicatorThis field is used to configure whether this product has Reversionary Bonus or not.Bonus Type Reversionary BonusThis field is used to configure the bonus type for reversionary bonus
RB Rate is related to Bonus Type which is used to facilitate rate Configuration
By using Bonus Type, it’s not necessary to configure rates for each product if rates are the same
If not related, then the bonus rates must be configure for this specific product
If one of the bonus types are selected, then this product will follow the same Bonus Rate configure for this product type


### VII.3. Terminal Bonus

Terminal Bonus This section is used to configure whether if the product has a terminal bonus, the related rules, and the Terminal Bonus Rate
Terminal Bonus This page is used to configure whether if the product has a terminal bonus and its related rules
Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionTerminal Bonus IndicatorThis field is used to configure whether if the product has terminal bonus or not.Interest Rate to calculate TBThis field is used to configure the interest rate which is used in Terminal Bonus calculation if necessary
If it is not used, then it can be configure as 0.No
of Completed Policy Years for Vesting on SurrenderThis field is used to configure the number of policy years before Terminal Bonus is allowed to be generated on surrender
For example, if it is configure as 3, then Terminal Bonus will only be available upon policy surrender after 3 completed years.No
of Completed Policy Years for Bonus Vesting on ClaimThis field is used to configure the number of policy years before Terminal Bonus is allowed to be generated on claim


### VII.4. Welcome Bonus Rate & Allot

Welcome Bonus Rate & Allot This page is used to configure the bonus rate and allot for Welcome bonus
Detail Steps: Please refer to VII.1.3
Cash Bonus Rate & Allot Field Description: Please refer to VII.4


### VII.5. Loyalty Bonus Rate & Allot

Loyalty Bonus Rate & Allot This page is used to configure the bonus rate and allot for loyalty bonus
Detail Steps: Please refer to VII.1.3
Cash Bonus Rate & Allot Field Description: Please refer to VII.4


### VII.6. Investment Bonus Rate & Allot

Investment Bonus Rate & Allot This page is used to configure the bonus rate and allot for investment bonus
Detail Steps: Please refer to VII.1.3
Cash Bonus Rate & Allot Field Description: Please refer to VII.4


### VII.7. Other Bonus Configuration

Other Bonus Configuration For products that have special bonuses such as special bonus, power-up bonus, etc
This page is used to configure such bonuses, its related rules, and calculation methods
Detail Steps These fields can only be accessed once a record has already been created
Basic: Click new button or edit icon to configure the basic info
Allot Config: Click the Allot Config link to configure allocation information, also can use download updload to setup data
For field descriptions, please refer to the Field Description link below
Allot Frequency: Click the Allot Frequency link to configure allocation frequency
Basic Field nameField DescriptionBonus TypeThis field is used to configure the type of bonus


## VIII. Formula Config **[MEDIUM — surrender value formula]**

Formula Config The Formula Config section allows for the configuration of product calculation related to formulas and rate tables
There are six parts under this section: VIII.1
CS Calculation Item Config VIII.4
Adacanced Premium Calculation Setup VIII.6
Discount Calculation Config


### VIII.1. Formula Setup

Formula Setup This table is used to configure calculation formulas used by the product
All necessary calculation items with its formulas should be configure in this table
There is a list of existing formulas ready to be used, but if no existing formula is suitable, then new formulas can be created from the (>>) icon beside Formula Name
Existing formulas are not able to be deleted or modified directly from the page, as formulas are shared with other products
If needed, formulas can be deleted or modified in Formula Configuration -> Formula List
Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionCalculation ItemThis field is used to select the calculation items of the formula to be added to the table
Detail-6 as following:Formula NameThis field is used to select a formula from the list


### VIII.2. Ratetable Setup

Ratetable Setup This table is used to configure RateTables used by the product and to enter or modify rates for each RateTable for this particular product
Each RateTable will belong to a RateTable Type
One RateTable Type can have different ratetables but only one RateTable can be selected for one particular product
With this table, we can easily know what kind of RateTables have been used for this product, whether it has premium rate, cash value rate, or whether if it has insurance charge rate, switch fee, etc
In addition, we can identify which RateTable is used for premium rate, which is used for insurance charge, etc
note Almost all rates have been configure in the RateTable except SB/MB/AI table and Bonus Rate Table
For product related rate tables, it is recommended to use the product Configuration to to go directly to RateTable, because the rate table configure in the RateTable Configuration will not be automatically linked to the product Configuration
If the RateTable is not tracked in RateTable Setup at Product Configuration, then it will lose checking for rule validation and product copy will not extract data from this RateTable as well as product exporting


### VIII.3. CS Calculation Item Config

CS Calculation Item Config Used to configure the advanced calculation method, for products which has advanced calculation method of some service
Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionCS ItemCurrently allow customer service items as following: 1 - Claim 2 - Fund Transaction 3 - Regular Premium 4 - Bonus Allocation 5 - Auto Maturity 6 - Survival Benefit Payment 7 - Process Vesting 8 - Annuity Payment 9 - Normal Lapse etc.Calculation ItemThis field is used to select the type of calculation
Here, the calculation item refers to Formula Configuration -> CS Calculation Type
- sumAssured - totalPaidPremium - annualPremium - regularTopupPremium - annualInvestmentPremium - annualRecurringTopup - COI - adminFee - totalChargesFee - GST - stampDuty - suspense - tiv - premium - adhocTopup - DB for Fund Trans NoticeFormula CategoryThis field is used to select a formula category to find formulas easier
Only [tenant] Product Category can be selected.Formula NameThis field is used to select a formula from the list
New formulas can be added through the (>>) icon.


### VIII.4. Illustration

Illustration This node is used to configure illustration related formulas
Illustration Config This table is used to configure illustration formulas which are used for Illustration Calculation
New calculation types can be added and new formulas can be created according to the requirements
Some illustration formulas may use special ratetables
For example, TIV performance rate, Bonus projection rate, etc
These ratetables should be configure in RateTable Configuration -> Ratetable List -> Category = [tenant] Illustration Detail Steps: Please refer to XIV.4
note The calculation type formula can be modified or added using ‘Maintain Calculation Type’ function
Field Description Field nameField DescriptionCalculation Item This field is used to select the calculation item


### VIII.5. Adacanced Premium Calculation Setup

Adacanced Premium Calculation Setup Page used to configure the all calculation item during the premium calculation
If use current menu, even one calculation item configure will all the items need to be configure, if no required you can configure a formula as r=0
Calculation Item & Related Formula premium calculation method: use SA to calculate premium Calculation ItemField DescriptionFormulasumAssuredSum Assuredr = SAstdPremBfStandard Premium before Modal Factornormal be configure as r = lookup premium ratetablestdPremAfStandard Premium after Modal Factorr = stdPremBf * Modal_FactorstdPremAnAnnulized Standard Premiumr = stdPremBfdiscntedPremBfDiscounted Premium before Modal Factorif product do not have discount r = stdPremBf else, r = stdPremBf * (1 - Discount_Rate)discntedPremAfDiscounted Premium after Modal Factorif product do not have discount r = stdPremAf else, r = stdPremAf * (1 - Discount_Rate)discntedPremAnAnnulized Discounted Premiumif product do not have discount r = stdPremAn else, r = stdPremAn * (1 - Discount_Rate)discntPremBfDiscount Premium before Modal Factorif product do not have discount r = 0 else, r = stdPremBf - discntedPremBfdiscntPremAfDiscount Premium after Modal Factorif product do not have discount r = 0 else, r = stdPremAf - discntedPremAfdiscntPremAnAnnulized Discount Premiumif product do not have discount r = 0 else, r = stdPremAn - discntedPremAnextraPremBfExtra Premium before Modal Factorif product do not have extra premium r = 0 else, r = Sample of Extra_Premium extraPremAfExtra Premium after Modal Factorr = extraPremBf * Modal_FactorextraPremAnAnnulized Extra Premiumr = extraPremBfpolicyFeeBfPolicy Fee before Modal Factorif product do not have policy fee r = 0 else, normal be configure as r = lookup policy fee ratetablepolicyFeeAfPolicy Fee after Modal Factorr = policyFeeBf * Modal_FactorpolicyFeeAnAnnulized Policy Feer = policyFeeBfunitUnit of Proudct Soldif product do not slod by unit r = 1 else, could be configure as r = unitgrossPremAfGross Premium after Modal Factorr = discntedPremAf + policyFeeAftotalPremAfTotal Premium after Modal Factorr = grossPremAf + ∑extraPremAfwaiveAnnualBenefitWaive Annual Benefit (Sum Assured)if product do not have waiver r = 0 else, could its formula as requiedwaiveAnnualPremiumWaive Annual Premiumif product do not have waiver r = 0 else, could its formula as requied Sample of Extra_Premium


### VIII.6. Discount Calculation Config

Discount Calculation Config This is not an default page for the product structure, user can add to the tenant product tree as required
Which is used to configure the muitple discount for standard premium or extra permium under target product
Field Description Discount Calculation Field NameField DescriptionOrderThis field used to configure the order of the discount
Using the up and down to modify, which will be generated automatical.Discount TypeThis field used to configure the type of discount, user can add tenant level discount type through menu General Configuration -> Dynamic Codetable -> T_DISCNT_TYPE
Here need to mention that 0-No special discount; 20-First Year Discount is platform data cannot be modifyDisocunted FormulaUsed to configure the discounted formula, to calculate the value after discountResult Parameter (Discounted)If need, can use the parameter to store the discounted valueDiscount FormulaUsed to configure the discount formula, to calculate the discount valueResult Parameter (Discount)If need, can use the parameter to store the discount valueRate FormulaIf need to get the discount rate, can use this field to configure the discount rate formula Final Value Field NameField DescriptionFinal Value Formula IndicatorThis indicator used to configure whether has special logic of final disocunt value
If the value of the indicator configure as ‘NO’, then the default final value which will use the last order under the Discount Calculation listDiscounted FormulaIf the value of ‘Final Value Formula Indicator’ configure as Yes, then this field is necessary
Used to configure the formula of discounted valueDiscount FormulaIf the value of ‘Final Value Formula Indicator’ configure as Yes, then this field is necessary
Used to configure the formula of discount value


## IX. Common Servicing Rules **[MEDIUM — min/max age, term limits]**

Common Servicing Rules The Common Servicing Rules section allows for the configuration of Common Product Rules
There are seven parts under this section: IX.1
Initial SA Limit Table IX.5
Product Risk Aggregation IX.7


### IX.1. Age Limit Table

Age Limit Table This table is used to configure the Age Limit for the product, including Age Limit for Life Assured, Policyholder, and Joint Life
Detail Steps: Please refer to XIV.4
Basic Field nameField DescriptionGenderThis field needs to be selected if gender is a relative factor for age limit
If not related, the default is ‘unknown’.Preferred Life of Life AssuredThis field needs to be selected if Preferred Life of Life Assured is a relative factor for age limit
If not related, the default is ‘NA’
Preferred Life Indicator is in Life Assured information entered in Data Entry to indicate whether if Life Assured is Preferred Life or notType of Coverage Field No
of Years/Coverage End AgeThese fields need to be selected if Coverage Period is a relative factor for age limit
Coverage Period is configure in Term Limit Table under Common Servicing Rules


### IX.2. Premium Limit Table

Premium Limit Table This table is used to configure Premium Limit for the product
It can be related with Age, SA Factor, Preferred Life Indicator, Payment Method, Premium Payment Frequency and Policy Currency
Multiple records are allowed if it related to these factors
For investment products, limitations such as min increase/decrease amount of regular premium, min increase/decrease amount of recurring top up, min recurring top up amount and min ad-hoc top up amount can also be configure
note This table is applied to investment products
Normally, the Premium Limit Table and Initial SA Limit table will be configure at the same time
If there’s no limit on initial SA, then this table does not need to be configure
Detail Steps: Please refer to XIV.4


### IX.3. Term Limit Table

Term Limit Table This table is used to configure Coverage Period and Premium Payment Period allowed for the product
All allowed coverage period and premium payment periods need to be configure in this table
For annuity product, deferment period and installment period will be configure in this table alongside guarantee period if it has withdraw period or if it’s a VA product with GMWB option
note Factors need to be selected before creating a new record
Detail Steps: Please refer to SB/MB/AI Table Factor List Factor NameFactor DescriptionCoverage PeriodThis factor is used to generate coverage period Configuration columns (Coverage Period, Coverage Year) in the Term Limit Template Excel file
This factor must be selected
That values that can be used in Coverage Period are as follows: ‘1’ - Cover Whole Life ‘2’ - Cover for Certain Years ‘3’ - Cover up to a Certain Age ‘4’ - Cover for a Certain Months ‘5’ - Cover for a certain daysPremium Payment Term and TypeThis factor is used to generate premium payment period Configuration columns (Type of Premium Payment Period, No
The values that can be used in Type of Premium Payment Period are as follows: ‘1’ - Single Premium ‘2’ - Pay for Certain Year ‘3’ - Pay Up to Certain Age ‘4’ - Pay for Whole Life ‘5’ - Pay for Certain MonthsDeferred PeriodThis factor is used to generate deferment period Configuration columns (Type of Deferred Period for Annuity, Deferred Period for Annuity)


### IX.4. Initial SA Limit Table

Initial SA Limit Table This table is used to configure Initial SA Limit for the product
It can be related with Age, Preferred Life Indicator, Payment Method, Occupation Class, and Policy Currency
Multiple records are allowed if it is related to these factors
For products that sell by units, the limitation of units can also be configure in this table
note This table is usually applied to Traditional Products, because SA limitation for investment products may not be a fixed amount and it will be configure as formulas under Formula Configuration
If there’s no limit on initial SA, then this table is no need to be configure
Detail Steps: Please refer to XIV.4
note If there’s no limitation on initial SA of the product, then this table can be left blank


### IX.5. Relationship Matrix

Relationship Matrix This table is used to configure relationships between products
The table currently supports Attached Product List and Parent Product List
Detail Steps: Please refer to XIV.4
New Product Relationship Field nameField DescriptionParent ProductThis field is used to select the parent products.Attached ProductThis field is used to select products which are allowed to be attached to the product
If it is a main product, then all allowed mains, riders or waivers can be selected
If it is an attached product, then all riders can coexist in the same policy and allowed waivers should be configure in this table.Type of RelationshipThis field is used to configure the relationship between parent product and attached product
- Rider product: If rider is the parent product, only rider can be chosen as the attached product during the Configuration of product relationship
The available options are: Co-exist, Dependent, Against, NA, and Attach


### IX.6. Product Risk Aggregation

Product Risk Aggregation This table is used to configure Risk Types of this product and related formulas to calculate risk aggregation
Aggregation formulas are configure by Formula List
Detail Steps: Please refer to XIV.4
Field Description Field nameField DescriptionRisk TypeThis field is used to select risk types covered by the product, multiple risk types can be selected
For tenant level risk type which could be configure under menu General Configuration -> Risk Aggregation TypeFormula CategoryThis field is used to select risk aggregation calculation formula category for each type of risk type selected
Currently, only formula category of ‘[tenant] Risk Aggregation’ can be selected in Product Risk Aggregation.Formula NameThis field is used to select risk aggregation calculation formula for each risk type selected
But currently, only formula under formula type of ‘[tenant] Risk Aggregation’ can be selected in Product Risk Aggregation, and different calculations according to different risk types are all covered by this formula.


### IX.7. Payment Method Table

Payment Method Table This table is used to configure allowed payment methods for this product
Allowed payment method can be different for different payment frequencies
For example, some products only allow direct debit if payment frequency is monthly
It can also be different for initial premium and subsequent / regular premium
For example, for initial premium, both Cash and Direct Debit are allowed, but for subsequent / regular premium, only Direct Debit can be used
Detail Steps: Please refer to XIV.4
Notice: Button Clear All used to delete all data under current page
Field Description Field nameField DescriptionPayment MethodThis field is used to configure allowed payment method for this product


## X. NB Rules **[MEDIUM — NB rules]**

NB Rules The NB Rules section allows for the configuration of New Business related rules
There are six parts under this section: X.1
Allowed Benefit Option Table X.3
Allowed Benefit Levels Table X.4
Agent Qualification Type X.5
Allowed Extra Premium Arith (Type)


### X.1. NB Rules

NB Rules This page is used to configure NB related parameters or indicators which will be used in New Business for different kinds of control
Basic Field nameField DescriptionAge BasisThis field is used to select which calculation rules will be applied to calculate age
Different countries may apply different age calculations
Currently, there are 5 age basis that are supported in the system: - Age Next Birthday - Age Last Anniversary Birthday - Age Last Monthlyversary Birthday - Age Nearest Birthday (Month) - Age Nearest Birthday (Day) - Age Nearest Birthday (Day of Year) Detail-7 as following:Allow DOPPThis field is used to configure whether this product is subject to the control of ‘Replacement of Policy’
This control is used to avoid cheating on commission
Currently, there are no rules built in the system directly for this control, but there is an interface to transfer information for policies with products that have this indicator as YES.Occupation LevelThis field is used to configure which category of job class is to be used for this product
It cannot be configure as ‘NA’ if the product calculation (e.g
Premium Rate) is related with Job Class


### X.2. Allowed Benefit Option Table

Allowed Benefit Option Table This table is used to configure the Benefit Option and its account way under the product
For Benefit Option, which is tenant level configuration, user can configure data under General Configuration -> Dynamic Codetable -> T_BENEFIT_OPTION
Detail Steps: Please refer to XIV.Configuration Methods Field Description Field nameField DescriptionBenefit OptionThis field is used to select benefit options allowed for the product
For tenant level, benefit options are configure under General Configuration -> Dynamic Codetable -> T_Benefit_Option.Count WayCurrently three types of count ways are supported in the system: - Premium calculation based on insured amount - Insured amount calculation based on premium - Agreed Premium.


### X.3. Allowed Benefit Levels Table

Allowed Benefit Levels Table This product is used to configure and easily view Benefit Levels allowed for this product
For Benefit level, which is tenant level configuration, user can configure data under General Configuration -> Dynamic Codetable -> T_BENEFIT_LEVEL
Detail Steps: Please refer to XIV.Configuration Methods Field Description Field nameField DescriptionBenefit LevelThis field is used to select the benefit levels allowed for the product
For tenant level, benefit options are configure under General Configuration -> Dynamic Codetable -> T_BENEFIT_LEVEL.Level NameThis field is used to configure the benefit name of each product
Input the type of char, e.g
note Normally for products that have benefit level configure, premium or sum assured will also be influenced by benefit level
This means that benefits also need to be configure in the related rate table.


### X.4. Agent Qualification Type

Agent Qualification Type This table is used to configure the qualifications required to sell this product
For example, if the qualification type required is ‘Health’, then an agent without the ‘Health’ qualification cannot sell the product
In product Configuration, only the relationship between product and qualification type needs to be configure
Relationship between producer and qualification type needs to be configure
The types are configure under Sales Configuration -> Sales Meta Data -> Agent Qualification Type
Detail Steps: Please refer to XIV.Configuration Methods Field Description Field nameField DescriptionAgent QualificationThis field is used to select the agent qualifications required for the product
Qualification Type is a part of the business data which should be initialized according to the insurance company during the implementation phase.


### X.5. Indexation Info

Indexation Info This table is used to configure Premium Indexation information for the product
Indexation Type, Indexation Rate for Dynamic Rate type, and Indexation Rules are all configure in this table
It has to be configured if ‘Indexation Indicator’ is configure as YES
note Indexation Rate for CPI type is configure in Indexation Rate under Global Set Up
Detail Steps: Please refer to XIV.Configuration Methods Field Description Field nameField DescriptionIndexation IndicatorThis indicator is used to configure whether or not Indexation information needs to be configured.Indexation Paced YearThis field is used to configure Indexation frequency
For example, every year (configure as 1) or every 5 years (configure as 5).Indexation TypeThis field is used to select the Indexation Type applied to the product
There are three options: - CPI - Dynamic - NA If CPI is selected, CPI rate needs to be configure
If Dynamic is selected, Dynamic rate needs to be configure


### X.6. Allowed Extra Premium Arith (Type)

Allowed Extra Premium Arith (Type) This table is used to configure calculation type of extra premium allowed for this product
Only the selected Extra Premium Type can be chosen during the Manual Underwriting process
Detail Steps: Please refer to XIV.Configuration Methods Field Description Field nameField DescriptionAllowed Extra Premium ArithThis field is used to select the extra premium type allowed for the product
There are currently 11 extra premium types supported in the system: 1) $ per 1,000 Sum Assured 2) Rating By Age 3) Times of Annual Premium 4) Times of Insurance Charge 5) Manual Extra Premium 6) % EM or amount per 1000 SA etc
Options 1), 2), 3), 5), and 6) are applied to traditional products, while option 4) is applied to investment products
All these calculation types are covered by two formulas, one is Extra_Premium (Traditional Product use) and the other is Extra_Charge (Investment Premium use)
These can be found in Formula Configuration -> Formula List -> New from template.


## XI. CS Rules

CS Rules The CS Rules section allows for the configuration of Customer Service related rules
There are two parts under this section: XI.1


### XI.1. CS Rules

CS Rules This page is used to configure CS related parameters or indicators that will be used in Customer Service for different kinds of controls
There are 16 sections under this section: XI.1.1
Premium Holiday Rules XI.1.12
Premium Voucher Rules XI.1.13
Reinstatement Rules XI.1.14
Reduced Paidup Rates XI.1.16
Surrender Rules Field Description XI.1.1
Annuity Rules Field nameField DescriptionAnnuity Surrender FactorThis field is used to configure Surrender Factor for Annuity Product


### XI.2. Not Allowed CS Items

Not Allowed CS Items This page is used to configure the CS items that will not be allowed during some period of the policy’s life cycle
Field Description Field nameField DescriptionPeriodThis field is used to settle the period which forbids CS items
Currently, two options are supported: - Investment Delay Period - Freelook PeriodNot Allowed CS ItemsThis field is used to configure which CS items aren’t allowed during the period
For example, increase SA is not allowed during the free look period.


## XII. RI Rules **[MEDIUM — reinsurance config]**

RI Rules The RI Rules section allows for the configuration of Service related rules
There are two parts under this section: XII.1


### XII.1. RI Rules

RI Rules This table is used to configure reinsurance related calculation and rules
If the product needs to apply reinsurance, this table must be configure
note Formula to create Sum at Risk is configured by Formula List, but it is currently not allowed to configure the formula directly from product Configuration, only to select existing formulas
Field Description Field nameField DescriptionRisk Amount Calculation FormulaThis field is used to select the calculation formula for SAR (Sum at Risk) for the product
Currently, these formulas cannot be edited from this page.Renewal FrequencyThis field is used to configure the Reinsurance renewal frequency for this product.Age Basis for RI Premium CalculationThis field is used to configure which type of age should be used to capture RI premium rate for this product
There are 3 options: - NA - Entry Age - Attained Age (If this option is selected, then RI premium will be recalculated at each renewal based on the age at renewal.)


### XII.2. Product Risk Type Table

Product Risk Type Table This table is used to configure the risk types covered by the product
Risk types are used to capture treaty that can cover the product
Multiple risk types can be selected in this table
Detail Steps: Please refer to XIV.Configuration Methods Field Description Field nameField DescriptionRisk TypeThis field is used to select risk types covered by the product for reinsurance purposes
Risk Type is a part of business data which should be initialized according to the insurance company during the implementation phase.


## XIII. Product Service Rules

Product Service Rules This section lists all the product rules which will run during the policy life cycle
The target rules can be enabled/disabled on the product level
Detail Steps: currently only disable & enable rule is available
Field Description Field nameField DescriptionService ItemThis field is used to configure the service item during the policy life cycle.Rule EventRule Event is used to configure the trigger point of rule or rule set during the business process.Rule SetRule Set is a group of rules, which can be nested within other rule sets
Trigger rule set means trigger all the rules.Rule NameThis field is used to configure the name of the rule.Error CodeThis field is used to configure the error code for the rule check
The error code can be linked to the error message.Rule DescriptionThis field is used to configure the description of the rule.


## XIV. Configuration Methods



### XIV.1. New

New Click ’+’ button, configure the fields, and then click Save
Click the ‘New’ button, configure the saves, then click Save.


### XIV.2. Edit

Edit Select record to be edited, modify fields and then click Save
Click the ‘Edit’ icon corresponding to chosen record, then modify and click Save.


### XIV.3. Delete

Delete Click the ’-’ button corresponding to the chosen record
Click the trash can icon corresponding to the chosen record, then click yes on the popup screen
Select the record that needs to be deleted by checking the checkbox beside it, press the delete button, and press yes.


### XIV.4. Download/Upload or Import

Download/Upload or Import Press the download process, to get the template or data file, then enter the required data
Press the upload process, which will process the delete the exisiting records and fully update the new data from file
Press the import process， which will insert the additional data
FeedbackWas this page helpful?|Provide feedback


## On this page

Main and Sales Information I.1
Product Additional Information II
Premium ISA Rate Information II.1
Premium SA Rate Information II.2
Product Liability Table III.1.1
Product Liability Table III.1.2
Auto Calculation Sequence III.1.7
Optional Liability Config IV
