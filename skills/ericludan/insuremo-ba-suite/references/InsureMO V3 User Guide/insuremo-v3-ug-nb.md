# InsureMO V3 User Guide 鈥?New Business (LifeSystem 3.8.1)
# Source: 02_New Business_LS3.8.1_0.pdf (214 pages)
# Version: V3 (legacy)
# Scope: BA knowledge base 鈥?for BSD writing and rule reference
# Updated: 2026-03-26

---

## 1. Purpose of This File

Answers questions about New Business workflows, field validations, underwriting rules, and policy activation logic in LifeSystem 3.8.1 (V3). Used for BSD writing when detailed NB rules are needed.

---

## 2. Module Overview

```
New Business (LifeSystem 3.8.1)
鈹?鈹溾攢鈹€ 1. Initial Registration
鈹?  鈹溾攢鈹€ Register Initial Information
鈹?  鈹溾攢鈹€ Image Scan (optional)
鈹?  鈹斺攢鈹€ Task Allocation
鈹?鈹溾攢鈹€ 2. Data Entry
鈹?  鈹溾攢鈹€ Basic Information
鈹?  鈹溾攢鈹€ Proposer (Company / Individual)
鈹?  鈹溾攢鈹€ Life Assured
鈹?  鈹溾攢鈹€ Premium Payer
鈹?  鈹溾攢鈹€ Payment Method (Cash / DDA / Credit Card)
鈹?  鈹溾攢鈹€ Benefit Information (Traditional / ILP / Annuity / Mortgage / Variable Annuity)
鈹?  鈹溾攢鈹€ Investment Strategy
鈹?  鈹溾攢鈹€ Waiver Benefit
鈹?  鈹溾攢鈹€ Beneficiary
鈹?  鈹溾攢鈹€ Trustee
鈹?  鈹斺攢鈹€ Commission Split
鈹?鈹溾攢鈹€ 3. Verification
鈹?  鈹溾攢鈹€ Auto-check errors
鈹?  鈹斺攢鈹€ Send Back for Modification
鈹?鈹溾攢鈹€ 4. Underwriting
鈹?  鈹溾攢鈹€ Auto-UW (standard limits)
鈹?  鈹溾攢鈹€ Manual UW (loading / decline / postpone)
鈹?  鈹溾攢鈹€ Escalation
鈹?  鈹斺攢鈹€ Fac Reinsurance
鈹?鈹溾攢鈹€ 5. Collection
鈹?  鈹溾攢鈹€ Premium collection before inforce
鈹?  鈹斺攢鈹€ Collection status tracking
鈹?鈹溾攢鈹€ 6. Inforce
鈹?  鈹溾攢鈹€ Policy activation
鈹?  鈹溾攢鈹€ Waiting period
鈹?  鈹溾攢鈹€ Suicide clause
鈹?  鈹斺攢鈹€ Dispatch

---

# New Business — Full Process Guide

Table 15: Field Description of Waiver Benefit Information Page..................................150

Table 17: Field Description of Company Trustee Information Page............................155
Table 18: Field Description of Individual Trustee Information Page...........................157
Table 19: Field Description of Comment Area on Data Entry Page.............................161


Table 26: Field Description of Update Policy Acknowledgement Page.....................169

Table 28: Field Description of Items for Medical Billing Area.........................................171
Table 29: Different Rules for Displaying Manual Entered LIA Information and Upload-


x



xi


New Business Overview
New Business is the fundamental and initial procedure for insurance business.
LifeSystem New Business module is a high-efficient application for business/insurance operators
to do insurance information entry and underwriting. In addition, due to the complexity of the
insurance business, for example, withdraw and reversal before or after the policy issuance,
LifeSystem also takes these practices to New Business module to deal with all the possibilities that
may occur in real business.


Create a Policy
You can work through the following stages to create a policy:
(cid:129) Initial Registration
After receiving a new proposal from the sales channel, the counter staff needs to register
proposal information to the LifeSystem and print receipt for the received documents. Such
process is called initial registration or reception. Image scanning can be done at reception
stage.
(cid:129) Data Entry
Data entry refers to the entry of proposal information into the system, including basic
proposal information, proposer information, life assured information, premium payer
information, payment method information, benefit information, beneficiary information,
trustee information and commission information.
(cid:129) Verification
After data entry is complete, verification can be performed to check if there are any errors
during data entry. When incorrect information is found, the proposal can be sent to data entry
for modification.
(cid:129) Underwriting
The system will check the proposal information in auto-underwriting process. If there are any
risks that must be manually evaluated, the proposal will be sent to underwriting. Underwriters
will assess the risks and make appropriate decisions accordingly.
(cid:129) Collection
Premium needs to be fully collected if the benefit is not allowed to take effect without
premium.
(cid:129) Inforce
A policy needs to pass a set of validations to take effect. The validations are triggered
(cid:129) Dispatch Policies
After a policy takes effect, the insurance company will dispatch the policy to client. At the same
time, the client is required to sign receipt for the policy.


(cid:129) The workflow above lists a typical new business workflow of creating a policy. LifeSystem
supports multiple new business workflows and the workflow is configurable in two aspects:
鈥?User can configure which workflow to be used for different scenarios.
鈥?User can configure how the tasks can be automatically transferred within one workflow.
(cid:129) For details about how to configure a workflow, refer to the LifeSystem Configuration Guide.
Initial Registration
This topic explains related concepts about initial registration.
After receiving a new proposal from the sales channel, the counter staff needs to register proposal
information to the LifeSystem and print receipt for the received documents. Such process is called
initial registration or reception.
The following flowchart shows the workflow of initial registration.

This topic describes how to enter simple proposal information in the System.
Create a Policy Initial Registration 3


1. From the main menu, select New Business > Initial Registration > Register Initial
Information.
STEP RESULT: The Register Initial Information page is displayed.

NOTE: Refer to Register Initial Information Page for field descriptions.
2. On the Reception tab page, enter the proposal prefix for Proposal No., an agent code, a
main benefit code, a proposal date and the initial premium.
3. After the required information is entered, you can choose to do:
Click Submit. Complete the registration in the system
immediately.
Click the Image Scan tab. Upload scan images via scanner or by
importing (see Figure 4), and then click
For details on Image Scan, refer to Image
Management User Manual.
STEP RESULT: The Image Scan page is as follows:
Create a Policy Initial Registration 4



Once submitted:
1) A proposal number and policy number are generated and displayed on the top of the page.
(cid:129) Write down the proposal/policy number in application form.
(cid:129) Archive the proposal documents.
2) The proposal status changes to Waiting for date entry.
3) The proposal will be allocated to date entry users by predefined strategy.
Example 1: Proposal Number and Policy Number Generated
Proposal No.: HO0424414 Policy No.: 0000075815 Actor: TEST34
As example 1 shows, the registration generates a proposal number 鈥淗O 0424414鈥?and a policy
number 鈥?000075815鈥? The proposal is sent to user 鈥淭EST34鈥?to complete data entry.
Register Initial Information Rules
Create a Policy Initial Registration 5


This topic describes how to print the registration slip after the initial registration is completed.
Register Initial Information task has been finished.
1. From the main menu, select New Business > Initial Registration > Print Registration
Slip.
STEP RESULT: The Print Registration Slip page is displayed.

2. On the Print Registration Slip page, enter the proposal number or policy number to be
printed, and then click Search.
STEP RESULT: The matching result is displayed on the page.

3. Select the proposal and click Print to print this registration slip for the client.
STEP RESULT: The Initial Registration Receipt page is displayed for preview on the receipt. If a printer is
connected, the printing job is sent to the printer.
Create a Policy Initial Registration 6



Amend Initial Registration Information
Amend Initial Registration Information
This task is optional. After initial registration, you can amend the initial registration information
during data entry step.
(cid:129) Register Initial Information has been finished.
(cid:129) The policy status is NOT Waiting for Data Entry.
1. From the main menu, select New Business > Initial Registration > Register Initial
Information.
STEP RESULT: The Register Initial Information page is displayed.

2. On the Register Initial Information page, click Search.
STEP RESULT: The Data Entry Search page is displayed.

Create a Policy Initial Registration 7


3. On the Data Entry Search page, enter the proposal number or policy number, and then
click Search.
STEP RESULT: The basic information of this proposal is displayed.

4. On the Basic Information page, amend the information as needed, and click Submit.
Data Entry
This topic explains related concepts about data entry.
Data entry (or detailed registration) is the module for users to input all the information in
application form, including basic proposal information, proposer information, life assured
information, payment method information, benefit information, beneficiary information, trustee
information and commission information.
The following flowchart shows the workflow of data entry.

Create a Policy Data Entry 8


This topic describes how to search out the target proposal鈥檚 data entry task.
(cid:129) Register Initial Information has been finished.
(cid:129) The proposal status is Waiting for Data Entry or Data Entry in Progress.
2. In the Task Classification pane, click Data Entry under PA Process.
STEP RESULT: The Data Entry Search Task page is displayed.

3. On the Search Task pane, set search criteria in the Data Entry Search Criteria section, and
Create a Policy Data Entry 9



If you fail to search out a proposal by policy number or proposal number, probably the target
proposal has been assigned to another user.
If you do need to continue data entry with the proposal, go to New Business Watch List to reassign
the proposal鈥檚 data entry task to yourself. For details, refer to Task Reassignment.
4. In the Search Result section, select the target data entry task, and you can choose to do:
To work on the proposal鈥檚 data entry task. 1 Click Work On.
2 The Data Entry page is displayed. For the following
process, refer to Enter Basic Information.
following process, refer to View Process.
View Process
This task is optional. You can follow the steps to view the process diagram and process basic
information. It also displays the task information and let you reassign the task.
Search Out the Target Proposal has been finished.
Create a Policy Data Entry 10


1. Continue with the Step 4 in the topic Search Out the Target Proposal. In the Data Entry
Work List, select the target data entry task, and click View Process.
STEP RESULT: The Process Diagram page is displayed. The green nodes show the steps that have been
taken, and the red node shows the step which the proposal is currently in.

2. Click Process Basic Info tab.
STEP RESULT: The Process Basic Info tab page is displayed. The information is read-only.

3. Click Tasks Info tab.
STEP RESULT: The Tasks Info tab page is displayed.

Create a Policy Data Entry 11


4. On the Tasks Info tab page, you can choose to do:
To work on the data entry task. 1 Click Work On.
2 The Data Entry page is displayed (see Figure 17). For
the following process, refer to Enter Basic Informa-
tion.
To reassign the task. 1 Click Reassign.
2 The Task Basic Info page is displayed (see Figure 18).
Enter the actor in Reassign To, and click Reassign
To.
3 The data entry task is reassigned to the actor you
appointed.
STEP RESULT:
Create a Policy Data Entry 12




Create a Policy Data Entry 13


This topic describes how to enter policy basic information on the Data Entry page.
Search Out the Target Proposal has been finished.
1. On the Data Entry Search Result list, select the target task and click Work On.
STEP RESULT: The Data Entry page is displayed.

2. On the Data Entry page, enter or modify the basic proposal information in the Basic
Information section.
STEP RESULT: The Basic Information section displays as follows.
Create a Policy Data Entry 14



NOTE: Refer to Basic Information Area for field descriptions.
Basic Information Area
This topic describes how to enter proposer information on the Data Entry page.
1. On the Data Entry Page, in the Proposer section, set Legal Entity Indicator according to
your purpose:
To add a company proposer. Set Legal Entity Indicator to Y.
To add an individual proposer. Set Legal Entity Indicator to N.
STEP RESULT: The Proposer section displays as follows.
Create a Policy Data Entry 15



2. Click Add to add a proposer.
(cid:129) If the Legal Entity Indicator is set to Y, the Company Proposer Information page is displayed.

NOTE: Refer to Field Description of Company Proposer Information Page for field
(cid:129) If the Legal Entity Indicator is set to N, the Individual Proposer Information page is displayed.

NOTE: Refer to Field Description of Individual Proposer Information Page for field
Create a Policy Data Entry 16


3. On the Company/Individual Proposer Information page, enter proposer information and
STEP RESULT: The proposer is added. After the proposer is added, the Add button is disabled.

4. You can click the hyperlinks to modify the proposer information, or click Delete to delete
the proposer.
Proposer Information Page
This topic describes how to enter life assured information on the Data Entry page.
Enter Proposer Information has been finished.
1. On the Data Entry Page, in the Life Assured section, click Add to enter life assured
information.
STEP RESULT: The Life Assured Information is displayed.
Create a Policy Data Entry 17



NOTE: Refer to Life Assured Information Page for field descriptions.
2. On the Life Assured Information page, enter the information for the life assured, and then
STEP RESULT: The life assured is added in the Life Assured section, see an example as follows.

3. You can click the hyperlinked texts in the record to modify the life assured information, or
click Delete to delete this record.
4. If declaration information of the life assured is required, click the N hyperlink under
Declaration Detail.
STEP RESULT: The Declaration Information page is displayed.
Create a Policy Data Entry 18



5. On the Declaration Information page, select declaration items and answer questions
accordingly. Then click Submit.
STEP RESULT: The Declaration Detail is updated to Y.

6. (Optional) In the Life Assured section, click Add and repeat the steps above to add
additional life assured customer.
Life Assured Information Page
Create a Policy Data Entry 19


This topic describes how to enter premium payer information on the Data Entry page.
Enter Life Assured Information has been finished.
1. On the Data Entry Page, in the Premium Payer section, set Legal Entity Indicator
according to your purpose:
To add a company premium payer. Set Legal Entity Indicator to Y.
To add an individual premium payer. Set Legal Entity Indicator to N.
STEP RESULT: The Premium Payer section displays as follows.

2. Click Add to add a payer.
(cid:129) If the Legal Entity Indicator is set to Y, the Company Premium Payer Information page is

Create a Policy Data Entry 20


NOTE: Refer to Field Description of Company Premium Payer Information Page for
field descriptions.
(cid:129) If the Legal Entity Indicator is set to N, the Individual Premium Payer Information page is

NOTE: Refer to Field Description of Individual Premium Payer Information Page for
field descriptions.
3. On the Company/Individual Premium Payer Information page, enter payer information
and click Submit.
STEP RESULT: The premium payer is added. After the payer is added, the Add button is disabled.

4. You can click the hyperlinks to modify the payer information, or click Delete to delete the
payer.
Premium Payer Information Page
Create a Policy Data Entry 21


This topic describes how to enter payment method information on the Data Entry page.
Enter Premium Payer Information has been finished.
1. On the Data Entry Page, in the NB Payment Method section, click Add to enter NB
payment method information.
STEP RESULT: The Payment Method Information page is displayed.
The NB Payment Method section displays as follows.

2. On the Payment Method Information page, select a payment method for New Business.
STEP RESULT: The Payment Method Information page varies with the different payment method
selections. See the examples as follows.


Create a Policy Data Entry 22



NOTE: Refer to Payment Method Information Page for field descriptions.
3. Enter the required information for the payment method and click Submit.
STEP RESULT: The payment method is added in the NB Payment Method section. After the payment
method is added, the Add button is disabled.

4. You can click the hyperlinked text under Payment Method to modify the information, or
click Delete to delete the payment method.
5. The same payment method is also displayed in the Renewal Payment Method section.
You can click the hyperlinked text under Payment Method to modify the information.
STEP RESULT: The Renewal Payment Method section displays as follows.

Payment Method Information Page
This topic describes how to modify main benefit information on the Data Entry page.
Enter Payment Method Information has been finished.
Create a Policy Data Entry 23


1. On the Data Entry Page, in the Benefit Name section, the main benefit selected during
Register Initial Information is displayed.
STEP RESULT: The Benefit Name section displays as follows.

2. In the Benefit Name section, click the hyperlinked text under Benefit Name to enter the
detailed information.
STEP RESULT: The Benefit Information page is displayed. The fields on this page vary with different
benefit types selected.

NOTE: The fields on the Benefit Information page deffer when different benefit types are selected.
Refer to Benefit Information Page for examples and field descriptions.
3. Enter the required information for the benefit and click Save.
STEP RESULT: The main benefit details are added in the Benefit Name section.

4. You can click the hyperlinked text in the record to modify the information, or click Delete
to delete the benefit.
Create a Policy Data Entry 24


Benefit Information Page
This task is optional. After the main benefit details are entered, you can add more benefits or riders
if neccessary. This topic describes how to add additional benefits or riders on the Data Entry page.
Modify Main Benefit Information has been finished.
1. On the Data Entry Page, in the Benefit Name section, click Add.
STEP RESULT: The Benefit Information page is displayed.

2. On the Benefit Information page, directly enter a benefit code or click the magnifier icon to
select a benefit code from the list.
STEP RESULT: The Benefit Information page is updated with the benefit related data entry fields. The
fields vary with different benefit codes selected.

NOTE: Only the products allowed to be attached to the main benefit (according to product definition)
is displayed in the Benefit Name list. If the user enters a benefit code which is not allowed to be
attached to the main benefit, an error message will be displayed.
Create a Policy Data Entry 25


3. Enter the required information for the benefit and click Save.
STEP RESULT: The additional benefit details are added in the Benefit Name section.

4. You can click the hyperlinked text in the record to modify the information, or click Delete
to delete the benefit.
5. Also you can click Add and repeat the steps above to add more benefits or riders.
This task is optional. You can add an investment strategy for an investment product. This topic
describes how to enter investment strategy.
(cid:129) Modify Main Benefit Information has been finished.
(cid:129) It is for investment products ONLY.
1. On the Data Entry Page, in the Benefit Name section, click Add.
STEP RESULT: The Benefit Information page is displayed.

2. On the Benefit Information page, directly enter the benefit code of investment product or
click the magnifier icon to select the benefit code of the investment product from the list.
STEP RESULT: The Benefit Information page (see Figure 132) is updated with the benefit related data
entry fields.
Create a Policy Data Entry 26


3. On the Benefit Information page, enter the required information for the benefit and click
Investment Strategy.
STEP RESULT: The Investment Strategy page is displayed.

(cid:129) Refer to Investment Strategy Page for field descriptions.
(cid:129) If Investment Strategy is defined, there is no need to specify funds for Premium
Apportionment, Single Premium Top Up Apportionment and Recurring Top Up Premium
Apportionment on the Benefit Information page.
4. On the Investment Strategy page, select funds and enter strategy details to define the
investment strategy and click Submit.
Create a Policy Data Entry 27


Investment Strategy Page
This topic describes how to calculate premium on the Data Entry page.
(cid:129) Modify Main Benefit Information has been finished.
(cid:129) All the benefits/riders information is entered.
1. On the Data Entry Page, in the Benefit Name section, click Calculation.
STEP RESULT: The total enforcing premium is calculated and displayed in the Total Inforcing Premium

Create a Policy Data Entry 28


This task is optional. You can add waiver of benefit on the Data Entry page.
All the benefit entry has been finished.
1. On the Data Entry Page, in the Benefit Name section, select a waiver鈥檚 plan code from the
Waiver of Premium list.
STEP RESULT: The Waiver of Premium selection displays as follows.

2. After the selection of Waiver of Premium, click Add Waiver.
STEP RESULT: The Waiver Benefit Information page is displayed.

Create a Policy Data Entry 29


The system performs benefit matrix validation check based on product definition to validate the
relationship between the rider and the benefit. If at least one benefit can be attached with the waiver
selected, the system automatically attaches the waiver to the benefit that is allowed.
(cid:129) If no error is found, the system prompts warning message: Please complete all
benefit entry before waiver benefit entry. If you still need to add benefit
information, complete benefit entry; if you confirm the waiver benefit entry, click Continue .
(cid:129) Then system will input fields with default values according to product definition.
(cid:129) The system then relates the waiver to waived benefits according to the product setup,
generates waiver information for each waived benefits, calculate the premium paid for the
waived benefits, saves the waiver information, and updates the benefit list in the benefit
summary table.
By default, if the waived product is not Whole Life product, coverage term of waiver benefit
= coverage term of waived benefit or maximum term allowed as defined; premium term of
waiver benefit = premium term of waived benefit or maximum term allowed as defined.
If the waived product is Whole Life Product, coverage term and premium term should be
manually entered.
Life assured: If the waiver is the waiver of premium, the life assured of the waiver is the same
as life assured of waived benefit; if the waiver is the payer benefit, the life assured of waiver
is the same as the payer of the policy; if it is a spouse waiver, only the insured who is the
spouse of the policyholder can be selected as the life assured for this product. If there is no
such insured, the message The Life Assured must be policy holder's
spouse will be displayed.
3. On the Waiver Benefit Information page, enter/modify the waiver information, and then
click Save.
NOTE: If the waiver selected can attach to several benefits, you need to enter the waiver information
again according to the attached product.
4. On the Data Entry Page, in the Benefit Name section, you can click Delete Waiver to
delete the waiver if neccessary.
Waiver Benefit Information Page
This topic describes how to enter beneficiary information on the Data Entry page.
1. On the Data Entry Page, in the Beneficiary section, click Add.
STEP RESULT: The Beneficiary page is displayed.
Create a Policy Data Entry 30



NOTE: Refer to Beneficiary Page for field descriptions.
2. On the Beneficiary page, enter the beneficiary basic information, and then choose to do as
follows accordingly:
Submit the entry. Click Submit.
To enter the indentifier details. Go to Step 3.
To enter the beneficiary鈥檚 address. Go to Step 4.
To add another beneficiary. Go to Step 5.
3. Enter the indentifier details.
a On the Beneficiary page, click Indentifier Details.
RESULT: The Identifier Information page is displayed.

b On the Identifier Information page, click the hyperlink text under Detail Information.
RESULT: The Identifier Details page is displayed.

c On the Identifier Details page, enter the required information and click Submit.
Create a Policy Data Entry 31


4. Enter the beneficiary鈥檚 address.
a On the Beneficiary page, click Enter Address.
RESULT: The Correspondence Address page is displayed.

b On the Correspondence Address page, enter the required information in the Address
Information section, and then click Apply.
RESULT: The address is added in the Address List section and appointed an unique Address Rec
No.
c (Optional) Repeat Step b to enter address information for a different address type.
d Select an address record from the Address List and click Submit.
5. Add another beneficiary.
a On the Beneficiary page, click Add Other.
NOTE: Enter a number greater than zero for Share% before clicking Add Other. Otherwise, a
warning message will be displayed. Make sure the total sum of all the beneficiarys鈥?share equals
to 100%.
RESULT: Another blank Beneficiary page is displayed.
b Repeat Step 2 to enter the additional beneficiary鈥檚 information.
The beneficiary information is added in the Beneficiary section on the Data Entry page.

Create a Policy Data Entry 32


Beneficiary Page
This task is optional. This topic describes how to enter trustee information on the Data Entry page.
1. On the Data Entry Page, in the Trustee section, choose the action according to the trustee
type being added.
Trustee type Action
Company trustee Set Company Indicator to Y, then go to Step
a.
Individual trustee Set Company Indicator to N, then go to Step
b.
a In the Trustee section, click Add.
RESULT: The Company Trustee Information page is displayed.

NOTE: Refer to Field Description of Company Trustee Information Page for field
b In the Trustee section, click Add.
RESULT: The Individual Trustee Information page is displayed.
Create a Policy Data Entry 33



NOTE: Refer to Field Description of Individual Trustee Information Page for field
2. On the Company/Individual Trustee Information page, enter the required information and
The trustee information is added in the Trustee section on the Data Entry page.
Trustee Information Page
This task is optional. This topic describes how to split commission as needed on the Data Entry
(cid:129) Enter Basic Information has been finished.
(cid:129) There is more than one commission agent.
1. On the Data Entry Page, in the Commission section, set Split Commission Indicator to Y.
STEP RESULT: The Commission section is displayed.
Create a Policy Data Entry 34



2. In the Commission section, enter the Commission Agent Code and Percentage for each
agent.
NOTE: Make sure the total sum of all the agents鈥?percentage equals to 100%.
3. If there is special commission, set Special Commission Indicator to Y.
This task is optional. This topic describes how to add modification comments on the Data Entry
1. On the Data Entry Page, in the Comment section, enter or modify comments if any. Set
Underwriting Indicator to Y if necessary.
STEP RESULT: The Comment section is displayed.

NOTE: Refer to Comment Area for field descriptions.
Create a Policy Data Entry 35


Comment Area
This topic describes how to submit the proposal.
Enter Premium Payer Information has been finished.
Create a Policy Data Entry 36


1. On the Data Entry Page, click buttons to save, validate or submit the proposal, see the
descriptions in the table:
If you click Then
Validate (cid:129) The system saves the entered information and
performs validation checks on the UI fields. If any
check failed, an error message is displayed and you
need to make modification accordingly.
(cid:129) If all UI validation checks pass, the system checks the
Rule Management System (RMS)* at backend and
displays failed rules as outstanding issues. You can
click Outstanding Issues to view them.
(cid:129) The proposal status is not changed after validation.
Submit (cid:129) The system saves the entered information and
performs validation checks on the UI fields. If any
check failed, an error message is displayed and you
need to make modification accordingly.
(cid:129) If all UI validation checks pass, the system checks the
Rule Management System (RMS)* at backend and
displays failed rules as outstanding issues.
(cid:129) If the Verification stage is configured in workflow,
then the proposal status is changed to Waiting for
verification when submission is successful. If the
Verification stage is not configured in workflow,
then the proposal status is changed to Waiting for
underwriting.
Save The system saves the entered information and
returns to the work list directly without
validation checks.
The proposal status is set to Data Entry
In Progress.
Outstanding Issues Outstanding issues are displayed for review,
including:
(cid:129) Non-underwriting issues
(cid:129) Underwriting issues
(cid:129) Medical requirement
You can find out any possible data entry
errors and correct them accordingly.
NOTE: Before clicking Outstanding Issues to view
outstanding issues, you must click Validate first.
Cancel The system gives up all the information
entered after the last save action and returns
to the work list.
The proposal status is set to Waiting for
Data Entry.
NOTE: *Different rules for different organizations can be defined in RMS. The system will find
Create a Policy Data Entry 37


corresponding rules according to policy鈥檚 organization.
For example,
(cid:129) For organization 101, if BMI 鈮?23, the system will create an Outstanding UW Issues to tell user
that the BMI value is too high and more information about LA鈥檚 health is needed.
(cid:129) For organization 102, if BMI 鈮?25, the system will create an Outstanding UW Issues to tell user
that the BMI value is too high and more information about LA鈥檚 health is needed.
Verification
This topic explains related concepts about verification.
After detailed registration is complete, verification can be performed to check if there are any
errors during data entry. When incorrect information is found, the proposal can be send back to
data entry for modification.
The following flowchart shows the workflow of verifying a proposal.

Search Verification Task
This topic describes how to search out the proposal to be verified.
The proposal has been transferred to verification by workflow management system and the
proposal status is Waiting for Verification or Verification in Progress.
Create a Policy Verification 38


2. In the Task Classification pane, click Verification under PA Process.
STEP RESULT: The Verification Search Task page is displayed.

3. On the Search Task pane, set search criteria in the Verification Search Criteria section,

Create a Policy Verification 39


4. In the Search Result section, select the target proposal task, and you can choose to do:
To work on the proposal鈥檚 verification task. 1 Click Work On.
2 The Verification page is displayed, see Figure 62.
3 Go to Verify the Proposal.
details, refer to View Process.
STEP RESULT: The Verification page is displayed.

Create a Policy Verification 40


This topic describes how to verify the proposal information.
Search Verification Task has been finished.
1. On the Verification Page, verify the proposal information and enter the verification
comment in the Verification Comment textbox in the Comment section if necessary.
STEP RESULT: The Comment section is displayed.

NOTE: Refer to Verification Page for field descriptions.
Search Verification Task
Verification Page
This topic describes how to check the outstanding issues on the Outstanding Issues page.
Verify the Proposal has been finished.
1. On the Verification Page, click Outstanding Issues to check the outstanding issues.
STEP RESULT: The Outstanding Issues page is displayed.
Create a Policy Verification 41



2. On the Outstanding Issues page, you can proceed accordingly:
There are Non-UW issues. (cid:129) In the Non-UW Issues area, select the outstanding
issues and click Print or Batch Print to generate
query letters from outstanding Non-UW Issues. See
Figure 65.
(cid:129) Send the query letters to customer for confirmation.
See Figure 66.
(cid:129) Once a query letter is printed, a print record will be
displayed in the Letter List section, see Figure 67.
The letter is in Printed status and to be issued and
replied in Document Management module (see
Document Management User Manual).
(cid:129) Then go to Close Non-UW Issues.
There are no Non-UW issues. Click Submit directly on the Verification
page. Then go to Recheck the Proposal.
Add more outstanding Non-UW issues. On the Outstanding Issues page, in the
Manual Issues section, enter the issues and
comments, and click Add.
The added issue will be listed in the Manual
Issues section.
NOTE: An example of generating query letter is displayed.
Create a Policy Verification 42



An example of query letter generated is displayed as follows.
Create a Policy Verification 43



An example of query letters printed is displayed as follows.

Create a Policy Verification 44


After a reply on query letter is received from customer, close the Non-UW issues and update
proposal information. This topic describes how to close the Non-UW issues.
(cid:129) Check Outstanding Issues has been finished.
(cid:129) A reply on query letter is received from customer.
NOTE: If reply is not received, go to withdraw this proposal. For details, refer to Withdrawal.
1. On the Outstanding Issues page, in the Letter List section, enter a reply date and change
Letter Status from Printed to Replied and click Update Status.
STEP RESULT: The letter status is updated to Replied. See an example displayed as follows.

2. On the Outstanding Issues page, in the Non-UW Issues section (and Manual Issues area if
there are manual issues), change the status of outstanding issues from Pending to
Closed/Ignored, and then click Submit to close Non-UW issues.
STEP RESULT: The Non-UW issues are closed, back to the Verification page.
3. On the Verification page, click Submit to update the proposal.
Recheck the Proposal
Create a Policy Verification 45


Recheck the Proposal
This topic describes the results of recheck on the proposal information which is done by the
system automatically.
This task is triggered by clicking Submit on the Verification Page.
1. The system rechecks the proposal information and the results are described accordingly.
There are only underwriting issues. Workflow transfers the proposal to
underwriting module. The proposal status
will be changed to Waiting for
Underwriting.
There are no outstanding issues. The proposal is accepted automatically.
There are rejection issues. The system declines the proposal
Underwriting
This topic explains related concepts about underwriting.
The system checks the proposal information in auto-underwriting process. If there are any risks
that must be manually evaluated, the proposal will be sent to manual underwriting. Underwriters
will assess the risks and make appropriate decisions accordingly.
The following flowchart shows the workflow of underwriting.
Create a Policy Underwriting 46



During underwriting, if the current underwriter does not have the authority to underwrite the
proposal, or if the current underwriter wants senior underwriters to underwrite the proposal, the
proposal can be escalated to senior underwriters for approval. For more details, refer to eBaoTech
LifeSystem Configuration Guide.
The following flowchart shows the workflow of escalating underwriting.

Create a Policy Underwriting 47


This topic describes how to perform underwriting.
Workflow management system has transferred the proposal to underwriting and proposal status
is Waiting for Underwriting or Underwriting in Progress.
Generally speaking, you need to perform the following steps to perform underwriting for a life
policy.
New Business Underwriting Rules
Retrieve the Underwriting Task
This topic describes how to retrieve the new business underwriting task.
Workflow management system has transferred the proposal to underwriting and proposal status
is Waiting for Underwriting or Underwriting in Progress.
2. In the Task Classification pane, click Underwriting under PA Process.
STEP RESULT: The Underwriting Search Task page is displayed.

Create a Policy Underwriting 48


3. On the Search Task pane, set search criteria in the Underwriting Search Criteria section,

4. In the Search Result section, select the target underwriting task, and you can choose to do:
To work on the proposal鈥檚 underwriting task. 1 Click Work On.
2 The Underwriting Main Screen page is displayed, see

Proposal Back to Data Entry.
following process, refer to View Process.
STEP RESULT: The Underwriting Main Screen page is displayed.
Create a Policy Underwriting 49



This topic describes how to send the proposal back to Data Entry if necessary.
Retrieve the Underwriting Task has been finished.
Create a Policy Underwriting 50


1. On the Underwriting Main Screen Page, view the underwriting application information,
proposal basic information, and underwriting related information including risk
aggregation, underwriting history, declaration details, claim history, CS history, etc.
NOTE: On the Risk Aggregation page (see Figure 74), the system lists all the policies that are related to
the policyholder or life assured. For the policies that you have access to, you can click the hyperlink to
view the Common Query page (see Figure 75).

Create a Policy Underwriting 51



2. Decide whether the proposal information needs to be amended.
Proposal information needs amendment. Click Back to Data Entry on the
Underwriting Main Screen Page.
The proposal will roll back to data entry stage,
with proposal status changed to Waiting
for data entry.
No. Go to Dispose Outstanding UW Issues.
Retrieve the Underwriting Task
This topic describes how to dispose outstanding UW issues.
Send Proposal Back to Data Entry has been finished.
Create a Policy Underwriting 52


1. On the Underwriting Main Screen Page, click Outstanding Issues.
STEP RESULT: The Outstanding Issues page is displayed.

2. On the Outstanding Issues page, click UW Issues tab to view the underwriting issues in the
UW Issues section.
Create a Policy Underwriting 53


3. On the UW Issues tab page, if query letters need to be generated before you close or ignore
the outstanding issues, select the outstanding issues and click Print or Batch Print to
generate UW letters.
Click Print. A letter is generated in PDF. One new record
will be shown under the letter list with status
Printed. The user can update the status to
Replied directly in the same page.
Click Batch Print. A letter is generated and there is one new
record shown under the letter list with status
To be Printed.
NOTE: User can issue this letter after daily document generation batch or manually issue the letter in
Document Management. Then user needs to print the letter and reply the letter and the letter status will
be updated to Replied. For details, refer to Document Management User Manual.
STEP RESULT:
The letters are replied. You can close or ignore the outstanding
issues. Go to Step 4.
The letters are not replied. You can manually withdraw the proposal or
the system will withdraw the proposal
automatically after a predefined period. For
details, refer to Withdraw a Policy Ad hoc.
4. On the UW Issues tab page, close or ignore the issues by selecting Closed or Ignored from
the Status list. Then click Submit.
This topic describes how to update underwriting information on the Underwriting Main Screen
Dispose Outstanding UW Issues has been finished.
Create a Policy Underwriting 54


1. On the Underwriting Main Screen Page, in the Proposal Basic Information section,
update for Commencement Date, Risk Commencement Date, and Discount Type.
STEP RESULT: The Proposal Basic Information section is displayed.

2. On the Underwriting Main Screen Page, in the Underwriting Decision section, update for
Medical Exam Indicator, Standard Life Indicator and LIA. Also add non-standard
endorsement, condition and exclusion if neccessary.
STEP RESULT: The Underwriting Decision section is displayed.

Create a Policy Underwriting 55


(cid:129) Refer to Underwriting Decision Page for field descriptions.
(cid:129) If Standard Life Indicator is N, LIA information is required. To enter or update LIA information,
click the hyperlink in the LIA column.

The Update LIA Information page is displayed. Then follow the steps in Update LIA Informa-
tion to complete updating LIA information.
This topic describes how to select the main benefit to make benefit decision.
Update UW Information has been finished.
1. On the Underwriting Main Screen Page, in the Underwriting Decision section, select the
main benefit and click Make Benefit Decision (see Figure 80).
Create a Policy Underwriting 56



STEP RESULT: The Make Decision on Benefit page is displayed.

NOTE: Refer to Make Decision on Benefit Page for field descriptions.
Make Decision on Benefit Page
This topic describes how to make out the underwriting decision on the main benefit on the Make
Decision on Benefit page.
Make Benefit Decision has been finished.
1. On the Make Decision on Benefit Page, enter a decision code in the Underwriting
Decision field.
STEP RESULT: The Underwriting Decision section is displayed.
Create a Policy Underwriting 57



2. In the Underwriting Decision section, click Extra Loading, Lien or Restrict Cover to
enter Extra Loading, Lien, or Restrict Cover information according to the real situation.
a To enter Extra Loading information, click Extra Loading. The Extra Loading page is
displayed. Select one or multiple loading options and enter loading information in each
loading鈥檚 area. Then click Submit.
RESULT: The Extra Loading page is displayed.
Create a Policy Underwriting 58



NOTE: Refer to Extra Loading Page for field descriptions.
b To enter Lien information, click Lien and then Lien page is displayed. Enter the information
and then click Submit.
RESULT: The Lien page is displayed.
Create a Policy Underwriting 59



NOTE: Refer to Lien Information Page for field descriptions.
The coverage information may include Reduction in Sum Assured/Unit, Pre-benefit Period,
Coverage Term Type, Coverage Term, Premium Term Type, Premium Payment Term, MA Factor,
and MS Factor. Which information can be adjusted depends on the type of benefits proposed.
c To enter the restrict cover information, click Restrict Cover and the Restrict Cover page is
displayed. Enter the information and then click Submit.
RESULT: The Restrict Cover page is displayed.

NOTE: Refer to Restrict Cover Page for field descriptions.
3. On the Make Decision on Benefit Page, click Submit to go back to the Underwriting Main
Screen Page. Check that the Underwriting Status of the benefit is changed to
Underwriting Completed.
STEP RESULT: The Benefit Information section is displayed.

Extra Loading Page
Lien Information Page
Restrict Cover Page
Create a Policy Underwriting 60


This topic describes how to submit a facultative reinsurance application for the main benefit.
Make UW Decision has been finished.
1. According to real situation, decide whether facultative reinsurance is required for the
current quote.
Facultative reinsurance is required. Go to Step 2.
Not required. Go to Make Benefit Decisions for others.
2. On the Make Decision on Benefit Page, click Apply Fac.
STEP RESULT: The Enter or Amend Facultative Reinsurance Request page is displayed.

3. On the Enter or Amend Facultative Reinsurance Request page, click Add New Request to
enter request information in the displayed Fac Request textbox, and then click Submit.

STEP RESULT: The Request Status of the facultative reinsurance is changed to Waiting for
Confirm.
Create a Policy Underwriting 61



NOTE: Only one request can be added. You can change request information by clicking Change
Request or cancel a request by clicking Cancel Request.
4. In the Existing Request section, select the request and click Confirm to confirm it. Check
that the Request Status is changed to Confirmed.
STEP RESULT: The Request Status is changed to Confirmed.

5. Click Exit.
STEP RESULT: The Enter or Amend Facultative Reinsurance Request Page is closed.
NOTE: After the policy is issued, you can go to Reinsurance module to make a facultative
arrangement decision. For details about Facultative Arrangement, see Reinsurance User Manual.
This topic describes how to make benefit decisions for other benefits, riders, and waivers.
(cid:129) Submit a Facultative Reinsurance Application has been finished.
(cid:129) There are other benefits, riders or waivers in the same policy.
1. Go back to Make Benefit Decision to repeat the steps to make a decision for each of the
benefits, riders and waivers at a time.
NOTE: You can select multiple benefits and make a decision for them at once, but in this case,
Indexation Indicator, Extra Loading, Lien, Restrict Cover and Apply Fac will not be available on the
Make Decision on Benefit Page.
As a result, you are suggested to make decisions on benefits/riders/waivers one by one.
Create a Policy Underwriting 62


Enter UW Comments
Enter UW Comments
This topic describes how to enter UW comments.
Make Benefit Decisions for others has been finished.
1. On the Underwriting Main Screen Page, in the Underwriting Comments textbox, enter
the underwriting comments and click Submit.
STEP RESULT: The Underwriting Comments textbox is displayed.

Over-authority underwriting decision: The underwriting case goes beyond authority of the
current underwriter and needs to be escalated to a senior underwriter for decision. This topic
describes the process of escalating underwriting.
The underwriting case goes beyond the underwriter鈥檚 authority, submission is rejected and the
case needs to be escalated to a senior underwriter.
1. Escalate underwriting case.
a On the Underwriting Main Screen Page, the junior underwriter sets Manual Escalation
Indicator to Y and specifies a senior underwriter in the Underwriter Escalate To field.
RESULT: The Escalate Underwriting Case page is displayed.
Create a Policy Underwriting 63



b Click Submit.
STEP RESULT: The underwriting case is escalated to the senior underwriter.
2. The senior underwriter retrieves the proposal with escalated underwriting task.
a From the main menu, select New Business > New Business Work List.
b On the Task Classification pane, click Manual UW under PA Process.
c Enter a policy number or proposal number and click Search to view the proposal or select
the proposal in the Search Result section.
d Select the proposal and then click Work On.
3. The senior underwriter makes underwriting decisions and click Submit on the
Underwriting Main Screen Page. For the following process, refer to Perform Underwriting.
Escalate Underwriting Rules
Collection
Before the policy becomes in-force, the Total Inforcing Premium needs to be collected. It is one of
the mandatory conditions for policy enforcement (For all conditions of enforcing a policy, refer
to Inforce).
After a policy/quotation number has been generated during Registration, money can be collected
at any stage of a New Business proposal but must be done before Inforce.
NOTE: For details on New Business Collection, refer to Counter Collection for New Business in
Collection User Manual.
Inforce
This topic explains related concepts about inforcing a proposal.
Create a Policy Collection 64


An accepted or conditionally accepted proposal will take effect if it passes the required validation
check. The validation check will be triggered automatically after underwriting, consent or health
warranty update, waiver of due interest, or premium collection.
The following flowchart shows the workflow of inforcing a proposal.

Inforce a Proposal
This topic describes how to inforce a proposal.
(cid:129) The proposal status is Accepted or Conditionally Accepted.
(cid:129) Health warranty has not expired. For details about health warranty, refer to Update Health
Warranty Expiry Date.
(cid:129) Premium is fully collected if the benefit is not allowed to take effect without premium. For
details about premium collection, refer to Collection.
(cid:129) Customer鈥檚 consent is received for conditionally accepted cases. for details about consent,
refer to Update Consent for LCA.
(cid:129) No overdue premium interest or premium interest has been paid or waived.
Create a Policy Inforce 65


1. Enforcing process is triggered under any of the following conditions:
(cid:129) The Consent Received Indicator is updated to Y for conditionally accepted cases.
(cid:129) The health warranty expiry date is extended.
(cid:129) Direct Debit account is updated if renewal payment method is Direct Debit.
(cid:129) Underwriting is complete and proposal status is Accepted.
(cid:129) Amendment of the proposal is complete.
(cid:129) Overdue interest is being waived.
(cid:129) Payment collection is cancelled (due to dishonoured cheque, etc.) but balance of amount is
sufficient to re-inforce the proposal.
2. The system runs a batch job to check whether the following auto-enforcing criteria are
met. If all the criteria are met, the proposal will be in force. If not, the proposal status
remains unchanged.
(cid:129) The proposal status is Accepted or Conditionally Accepted.
(cid:129) Health warranty has not expired.
(cid:129) The Consent Given Indicator is Y.
(cid:129) For monthly payment frequency, the Direct Debit account number must be available.
(cid:129) Premium is fully paid with tolerance limit and debit agent account for short payment.
3. The system sets the Inforcing Date which is the Latest Date among the Consent Given Date,
Effective Date of Full Payment, Health Warranty Extended Date, Direct Debit Date, and LCA
Date.
4. The system updates the commencement date based on the inforcing date.
5. The system recalculates the age of the life assured based on the commencement date.
6. The system changes the commencement date.
The main benefit auto backdate indicator is Y, The system changes the commencement date
the main benefit First of month is N, and age to the DOB - 1.
increase occurs.
(cid:129) For single life assured case, the system changes the
commencement date to DOB of life assured - 1.
(cid:129) For multiple life assured case, the system changes the
commencement date to the earliest date of DOB of
life assured - 1.
The main benefit auto backdate indicator is N, The commencement date is the first day of
the main benefit First of month is Y. the month.
7. The system recalculates the proposal premium.
8. The system updates the proposal information.
9. The system generates fund transaction application for investment product.
10. The system updates and inserts fee records.
Create a Policy Inforce 66


11. The system refunds premium if any.
12. The system generated policy documents.
13. The system generates LCA if Generate LCA Indicator is Y. After generating LCA, the system
sets Generate LCA Indicator to N.
14. The system records the supervisor hierarchy of the service agent at present.
New Business Enforce Policy Rules
Dispatch Policies
This topic explains related concepts about dispatching policies.
After policies take effect, the insurance company will dispatch the policies to clients. At the same
time, the clients are required to sign receipts for the policies.
The following flowchart shows the workflow of dispatching policies to the clients.

This topic describes how to dispatch policies to the clients.
The proposal status is Inforce.
1. Print policy document ad-hoc to be dispatched or the system does a weekly batch job to
extract policies to be printed. For details, refer to Print Policy.
Create a Policy Dispatch Policies 67


2. Dispatch policy documents to client and enter the dispatch date. For details, refer to Enter
Dispatch Date.
3. The client receives the policy documents and assigns the acknowledgement letter.
4. After receiving the acknowledgement letter, the insurance company updates
acknowledgement details. For details, refer to Update Acknowledgement Details.
This topic describes how to print policy document ad-hoc to be dispatched.
The proposal status is Inforce.
1. From the main menu, select New Business > Print Policy Document > Ad hoc Print.
STEP RESULT: The Ad hoc Print Policy Document page is displayed.

2. Set search criteria and then click Search to search out the policies.
NOTE: Only the policies/proposals whose organizations that you have the access can be searched out.
3. In the Search Result section, select the policies and then click Print Policy to print them.
Create a Policy Dispatch Policies 68


In the new business stage, after a policy takes effect and the policy documents are printed, the
policy documents can be reprinted for the policyholder if required. This topic describes using LS
to regenerate/reprint policy documents.
(cid:129) The proposal status is Inforce.
(cid:129) The policy documents have been printed before.
1. From the main menu, select New Business > Print Policy Document > Reprint.
STEP RESULT: The Reprint Policy Document page is displayed.

2. On the Reprint Policy Document page, enter the policy number or proposal number, and
STEP RESULT: The policy information is displayed.

Create a Policy Dispatch Policies 69


3. Selet the documents, a print type, and enter the reason for reprinting. Then click Submit.
NOTE: For new business, the Re-print option is selected automatically and cannot be changed.
This topic describes how to enter the dispatch date after the policy documents have been
dispatched to clients.
The policy documents are printed out and dispatched to clients.
1. From the main menu, select New Business > Policy Document Acknowledgement >
Acknowledgement in Bulk.
STEP RESULT: The Bulk Confirm Policy page is displayed.

2. Set search criteria and then click Search.
STEP RESULT: The qualified policy records are displayed in the Search Result section.
NOTE: Only the policies/proposals whose organizations that you have the access can be
searched out.
3. Select the target policies to be dispatched, enter the dispatch date, and then click Submit.
Create a Policy Dispatch Policies 70


This topic describes how to update acknowledgement details after receiving the acknowledgement
letter.
The acknowledgement letter has been received.
1. From the main menu, select New Business > Policy Document Acknowledgement >
Acknowledgement by Individual.
STEP RESULT: The Individual Confirm Policy page is displayed.

2. Enter the policy number or proposal number and then click Submit.
NOTE: Only the policies/proposals whose organizations that you have the access can be searched out.
STEP RESULT: The Update Policy Acknowledgement page is displayed.

NOTE: Refer to Update Policy Acknowledgement Page for field descriptions.
3. On the Update Policy Acknowledgement page, update the acknowledgement details, and
then click Submit.
Create a Policy Dispatch Policies 71


Reversal and Withdrawal
This section is about reversal and withdrawal.
During new business proposal or even after policy issuance, users are allowed to modify or cancel
a proposal.
This section introduces how to modify or cancel New Business proposals at different stages.
Withdrawal
This topic explains what withdrawal is.
Insurer can withdraw proposals according to business rules either by online (Ad Hoc Withdrawal)
or by batch job (Auto Withdrawal). After the proposal is withdrawn, the system will generate a
withdrawn letter and refund the premium to the client.
The following flowchart shows the workflow of withdrawing a proposal.



Withdraw a Policy Ad hoc
This topic describes how to withdraw a policy ad hoc. Ad-hoc withdrawal is done manually by
using the Withdraw New Business menu.
(cid:129) The proposal status is not Withdrawn, Inforce, Postponed, Declined, or other
renewal policy status.
1. From the main menu, select New Business > Reversal and Withdrawal > Withdraw New
Business.
STEP RESULT: The Withdraw New Business page is displayed.
Reversal and Withdrawal Withdrawal 73



NOTE: Refer to Fields on Withdraw New Business Page for field descriptions.
2. On the Withdraw New Business page, enter the policy number or proposal number, and
then click Search to display the basic information of this proposal.
3. In the Withdrawal Reason list, select a withdrawal reason, and then click Submit.
About Auto Withdrawal
Fields on Withdraw New Business Page
Rules of New Business Withdrawal
Auto Withdrawal
This topic describes the process of auto withdrawal performed by the system with batch jobs.
(cid:129) The proposal status is not Withdrawn, Inforce, Postponed, Declined, or other renewal policy
status.
(cid:129) The proposals meet the predefined auto-withdrawal criteria predefined.
1. The system runs a daily batch job to withdraw the proposals.
2. The system updates proposal status to Withdrawn and sets the withdrawal reason.
3. The system cancels the waiver of overdue interest and miscellaneous fees if any and
updates the policy transaction history.
4. The system validates the medial fees.
5. The system checks whether refund is required.
NOTE: Refund is required when the proposal status is Withdrawn and the General Suspense Balance is
greater than zero. Then the system generates a refund fee record and a withdrawal letter with the refund.
Reversal and Withdrawal Withdrawal 74


New Business Amendment
This topic explains related concepts about new business amendment.
After underwriting but before in-force, users can still update proposal information through the
amendment function. After amendment, the proposal will be reassessed on risks.
The following flowchart shows the workflow of amending new business.

Amend New Business
This topic describes how to amend a New Business transaction.
(cid:129) The proposal status is Accepted, or Conditionally Accepted.
(cid:129) Proposal information amendment is required for various reasons by client, agent, hospital, or
clinic.
1. From the main menu, select New Business > Reversal and Withdrawal > Amend New
Business.
STEP RESULT: The Amend New Business page is displayed.
Reversal and Withdrawal New Business Amendment 75



2. On the Amend New Business page, enter the proposal number or policy number, and then
click Search to search out the target proposal.
STEP RESULT: A warning message is displayed: Do you wish to perform Amendment?
3. In the warning message, click Continue.
STEP RESULT: A message is displayed: Amendment Successfully. The proposal returns to Data
Entry stage.
4. From the main menu, select New Business > New Business Work List.
STEP RESULT: The Work List page is displayed.
5. On the Work List page, in the Task Classification pane, click Data Entry under PA Process.
In the Search Task pane, enter search criteria, and then click Search to search out the
proposal to be amended.
STEP RESULT: Matching results are displayed in the search result list.
6. In the search result list, double-click the target proposal.
STEP RESULT: The Data Entry page is displayed.
7. On the Data Entry page, amend the proposal information as needed, and then click
Amend New Business Rules
Policy Status Reverse
This topic explains related concepts about policy status reverse.
After a policy takes effect and the policy status becomes Inforce, if the client requests to change
proposal information or if any operation error is found, the insurance company needs to reverse
the inforce status for modification. The policy issued without premium cannot be reversed,
because the system will always refund the premium even if the premium has not been collected.
The following flowchart shows the workflow of reversing the Inforce status.
Reversal and Withdrawal Policy Status Reverse 76



Reverse Policy
This topic describes how to reverse the inforce status.
(cid:129) The policy status is Inforce.
(cid:129) The policy is not frozen by CS or claims.
1. From the main menu, select New Business > Reversal and Withdrawal > Reverse Policy.
STEP RESULT: The Reverse Policy page is displayed.

2. On the Reverse Policy page, enter the policy number or proposal number, and then click
STEP RESULT: The Change Policy Status of Inforce Policy page is displayed.
Reversal and Withdrawal Policy Status Reverse 77



3. On the Change Policy Status of Inforce Policy page, in the Reversal Application area, select
Waiting for Data Entry from the Proposal Status list, enter the reversal reason if
you want, and then click Submit.
STEP RESULT: The proposal will be sent to data entry and the proposal status will be changed to Waiting
for data entry.
NOTE: The system will transfer premium from premium income or respective account to New
Business suspense account.


Medical Billing Management
This section is about medical billing management.
LifeSystem provides functionalities for users to update, cancel or reverse medical billings.
This topic describes how to update medical billing.
(cid:129) Proposal number and policy number are generated successfully.
1. From the main menu, select New Business > Medical Billing > Update.
STEP RESULT: The Update Medical Billing page is displayed.

NOTE: Refer to Items for Medical Billing Area for field descriptions.
2. On the Update Medical Billing page, enter search criteria, and then click Search to search
out the target policy or proposal.
STEP RESULT: The related information of the matching result is displayed.
Medical Billing Management Update Medical Billing 79


3. In the Items for Medical Billing area, take action according to your purpose.
Add a medical billing 1 Click Add. Extra fields related to medical billing are displayed.
2 Enter the correct clinic code. The clinic name and clinic panel code are displayed
3 Enter other billing information, such as medical type, fee sum, and then click
Submit to save the medical billing information.
Delete a medical billing Select the target medical billing and then click Delete.
Edit a medical billing Modify the target medical billing information and then click
When medical billing record is submitted, you can cancel or reverse the medical billing record.
(cid:129) A medical billing is already created.
1. From the main menu, select New Business > Medical Billing > Cancel or Reverse.
STEP RESULT: The Cancel or Reverse Medical Billing page is displayed.

2. On the Cancel or Reverse Medical Billing page, enter search criteria, and then click Search
to search out the target medical billing record.
STEP RESULT: The related information of the matching result is displayed.
Medical Billing Management Cancel or Reverse Medical Billing 80


3. In the Items for Medical Billing area, select the medical billing record, and then click
Cancel/Reverse.
STEP RESULT: If the medical payment status is Pending Approval, Approved, Payment
Processed, or Payment Confirmed, the system reverses the medical billing record; If the
medical payment status is Pending Payment Requisition, the system deletes the medical
billing record and cancels the payment record from the system.


Task Management
This section is about task management.
Task Reassignment
This topic explains what task reassignment is.
You can reassign tasks with a reassignment strategy, that is, how the tasks will be reassigned,
through watch list. The watch list page looks the same as the work list page because they share the
same UIC components. The difference is that in the watch list page, the Work On button is
replaced by the Reassign button.
There are three reassignment strategies in system:
(cid:129) Pull: The tasks will be listed in sharing pool for any authorized user to claim them.
(cid:129) Auto balance push: Depending on user requirement, system will try to balance the workload
of participants on daily/monthly or other basis. Currently, auto balance solution is by random
in the group.
(cid:129) Least-number priority push: System will assign tasks to users with the least pending tasks to
make sure the shortest processing time.
Reassign Tasks
This topic describes how to reassign tasks.
1. From the main menu, select New Business > New Business Watch List.
STEP RESULT: The Watch List page is displayed.
Task Management Task Reassignment 82



2. On the Watch List page, in the Search Task pane, enter search criteria, and then click Search
to search out the target tasks.
3. In the search results, select the target results, and then click Reassign.
NOTE: You can press CTRL to select multiple tasks.
STEP RESULT: The Reassign page is displayed.

4. On the Reassign page, select a reassignment strategy from the Strategy list, select users
from the User list, and then click Submit.
NOTE: The system lists all accessible users in the user list according to the assignment strategy.
Task Management Task Reassignment 83


Unlock Claimed Task
This topic explains related concepts about unlocking claimed task.
A task is in either of the following two status:
(cid:129) Claimed: means that a user has already started to process the task, and the task cannot be
accessed by other users.
(cid:129) Ready: means that the task is still to be claimed, but it does not necessarily mean that it can be
accessed by any authorized users, because it is still possible that a ready case has already been
assigned to certain users.
Perform Unlock Claimed Task
This topic describes how to unlock a claimed task.
(cid:129) The task status is Claimed.
STEP RESULT: The Work List page is displayed.
2. On the Work List page, in the Search Task pane, enter search criteria, and then click Search.
STEP RESULT: Matching results are displayed in the search result list.
3. In the search result list, double-click the target task.
STEP RESULT: The corresponding task page is displayed.
4. On the task page, click Cancel.
The task status changes to Ready.
NOTE: Whether the ready task is put into the public work list or the work list of a certain user can be
configured in the rate table.


Advanced Functions
This section is about advanced functions.
Update Consent for LCA
This topic explains related concepts about updating consent for LCA.
For conditionally accepted cases, when the proposer consents to all the conditions and exclusions
in the Letter of Conditional Acceptance (LCA), the insurance company will update the consent in
the system.
The following flowchart shows the workflow of updating consent.

Perform Consent for LCA Updating
This topic describes how to update consent for LCA.
(cid:129) The proposal has been underwritten with a Conditionally Accepted decsion and a
LCA (Letter of Conditions on Acceptance) is generated.
(cid:129) The LCA document has been Printed, Issued and Replied (Refer to Document Management
User Manual for how to print/issue/reply a document).
(cid:129) The proposal status is Conditionally Accepted.
(cid:129) The Consent Given Indicator is N.
(cid:129) The proposal has been registered for not more than one year.
Advanced Functions Update Consent for LCA 85


(cid:129) Client consents to the underwriting decision.
1. From the main menu, select New Business > Advanced Functions > Update Consent for
LCA.
STEP RESULT: The Update Consent for LCA page is displayed.

2. On the Update Consent for LCA page, enter search criteria, e.g. the policy number or
proposal number, and then click Search.
STEP RESULT: The basic information of this proposal is displayed.
3. Update Consent Given Date, and set Consent Given Indicator to Y.
4. Update Re-underwriting Indicator and Re-underwriting Reason if applicable.
5. Click Submit.
STEP RESULT: If the Re-underwriting Indicator is Y, the proposal will be sent for underwriting. For
details, refer to Underwriting; If the Re-underwriting Indicator is N and the premium has been
collected, the proposal will be enforced. For details, refer to Inforce.
Update Consent for LCA Rules
Update Health Warranty Expiry Date
This topic explains related concepts about updating health warranty expiry date.
Health warranty refers to a certain period of time in which the underwriting decision results
remain valid. A policy will not take effect if health warranty has expired. If health warranty has
expired before a policy takes effect, insurer can ask the client to provide the latest health
declaration or to update health warranty directly.
The following flowchart shows the workflow of updating health warranty expiry date.
Advanced Functions Update Health Warranty Expiry Date 86



Perform Health Warranty Expiry Date Updating
This topic describes how to update the health warranty expiry date.
(cid:129) The proposal status is Conditionally Accepted or Accepted.
(cid:129) Proposal cannot be enforced because of expired health warranty.
1. From the main menu, select New Business > Advanced Functions > Update Health
Warranty Expiry Date.
STEP RESULT: The Update Health Warranty Expiry Date page is displayed.
2. On the Update Health Warranty Expiry Date page, enter the policy number or proposal
number, and then click Search.
3. Update the health warranty expiry date, and then click Submit.
Update Health Warranty Rules
LIA Information Management
This topic explains related concepts about LIA information management.
LIA is short for Life Insurance Association.
The following diagram shows how the LIA information is managed in LifeSystem.
Advanced Functions LIA Information Management 87



This topic describes how to upload LIA information.
(cid:129) LIA file has been received with records from other reporting insurance companies.
Upload/Download.
STEP RESULT: The Upload/Download LIA Data File page is displayed.

2. On the Upload/Download LIA Data File page, click Browse.
STEP RESULT: The Choose File to Upload dialog box is displayed.
3. In the Choose File to Upload dialog box, navigate to an LIA file on your local disk, and then
click Open.
STEP RESULT: The file path is displayed in the File Location box.
4. On the Upload/Download LIA Data File page, click Submit.
STEP RESULT: The system validates the uploaded file. If validation passes, the LIA information will be
successfully updated in the system.
Advanced Functions LIA Information Management 88


This topic describes how to download LIA information.
Upload/Download.
STEP RESULT: The Upload/Download LIA Data File page is displayed.

2. On the Upload/Download LIA Data File page, click Download.
STEP RESULT: The File Download dialog box is displayed.
3. In the File Download dialog box, click Open or Save.
STEP RESULT: The file is opened or saved to your local disk. See the sample as follows.
Advanced Functions LIA Information Management 89



4. Pass the LIA file downloaded to other insurers to share the LIA information.
This topic describes how to update LIA information.
(cid:129) During NB Underwriting, CS Underwriting or Claim Underwriting, LIA information needs
to be entered.
(cid:129) Party record already exists in the system.
Advanced Functions LIA Information Management 90


Update.
NOTE: If the Life Assured is a sub-standard life, the LIA information needs to be updated during NB
Underwriting, CS Underwriting and Claim Underwriting.
(cid:129) For updating LIA information during NB and CS Underwriting, see Underwriting.
(cid:129) For updating LIA information during Claim Underwriting, see Claim Underwriting in Claim User
Manual.
STEP RESULT: The Update LIA Information page is displayed.

NOTE: You can also enter the Update LIA Information page through New Business Underwriting,
CS Underwriting, or Claim Underwriting Main Screen.
2. On the Update LIA Information page, enter search criteria, and then click Search.
3. In the search results, click the radio button of the target record.
STEP RESULT: Related LIA information (if any) is displayed in the LIA Information area.
Advanced Functions LIA Information Management 91


4. In the LIA Information area, take action according to your purpose.
Add LIA record 1 Click Add. The Add/Edit LIA Information page is displayed.

2 On the Add/Edit LIA Information page, in the Underwriting Decision Code box, click
the magnifier icon to select an Underwriting Decision Code and click Add. One record
line is added below. Repeat this step to add more Underwriting Decision Codes if
necessary.
3 On the Add/Edit LIA Information page, in the Impairment Code box, click the
magnifier icon to select an Impairment Code and click Add. One record line is added
below. Repeat this step to add more Impairment Codes if necessary.
4 Click Submit.
Edit LIA record 1 In the LIA Information area, select the LIA record to be edited, and then click Edit. The
Add/Edit LIA Information page is displayed.
2 On the Add/Edit LIA Information page, modify the LIA record as needed, and then click
This topic describes how to query LIA information.
(cid:129) The LIA record already exists in the system.
Query.
STEP RESULT: The Query LIA Information page is displayed.
Advanced Functions LIA Information Management 92



2. On the Query LIA Information page, enter search criteria, and then click Search.
STEP RESULT: The target customer and related LIA information are displayed.
(cid:129) Only the policies/proposals whose organizations that you have access to can be searched out.
(cid:129) You have to input at least two search criteria to search out the target records.
3. Review the LIA information.
Waive Overdue Interest
This topic explains related concepts about waiving overdue interest.
If the client does not pay premium in due time, normally the insurance company requests the
client to pay the premium together with interest caused by overdue payment. In some cases, the
insurance company waives the interest so the customer only needs to pay the premium.
The following flowchart shows the workflow of waiving overdue interest.
Advanced Functions Waive Overdue Interest 93



Perform Waiving Overdue Interest
This topic describes how to waive overdue interest.
(cid:129) Overdue interest has been calculated. The proposal status should be Accepted or
1. From the main menu, select New Business > Advanced Functions > Waive Overdue
Interest.
STEP RESULT: The Waive Overdue Interest page is displayed.

Advanced Functions Waive Overdue Interest 94


2. On the Waive Overdue Interest page, enter a policy number or a proposal number, and
STEP RESULT: The basic information is displayed. If the proposal status is Accepted or
Conditionally Accepted, and the overdue interest amount is found, go to Step 3; Otherwise,
the request of waiving overdue interest is denied and the process is completed.
3. In the Basic Information area, enter the overdue interest amount to be waived in the Waive
Overdue Interest Amount box and enter reasons in the Waive Reason box, and then click
Waive Overdue Interest Rules
Anti-Money Laundry
This topic explains related concepts about anti-money laundry.
Anti-money-laundry (AML) is part of the LifeSystem risk management mechanism which
provides a blacklist to protect all business transactions from potential crimes that take form in
money-laundry.
If underwriting rules have been configured for AML blacklist, and policy PH or LA or Payer Info
5 basic info is the same as AML record, NB underwriting needs to be conducted for the policy.
This topic describes how to upload an AML list.
(cid:129) AML file has been received with records.
Laundry > Upload/Download.
STEP RESULT: The Upload/Download AML Data File page is displayed.

2. On the Upload/Download AML Data File page, click Browse.
STEP RESULT: The Choose File to Upload dialog box is displayed.
Advanced Functions Anti-Money Laundry 95


3. In the Choose File to Upload dialog box, navigate to an LIA file on your local disk, and then
click Open.
STEP RESULT: The file path is displayed in the File Location box.
4. On the Upload/Download AML Data File page, click Submit.
STEP RESULT: The system validates the uploaded file. If validation passes, the AML information will be
successfully updated in the system.
This topic describes how to download an AML list.
Laundry > Upload/Download.
STEP RESULT: The Upload/Download AML Data File page is displayed.

2. On the Upload/Download AML Data File page, click Download.
STEP RESULT: The File Download dialog box is displayed.
3. In the File Download dialog box, click Open or Save.
STEP RESULT: The file is opened or saved to your local disk. See the sample as follows.
Advanced Functions Anti-Money Laundry 96



4. Distribute the AML file.
This topic describes how to query an AML list.
Laundry > Query.
STEP RESULT: The Query AML Information page is displayed.
Advanced Functions Anti-Money Laundry 97



2. On the Query AML Information page, select an option from the Watch List Type list, enter
other search criteria as needed, and then click Search.
3. In the search results, take action according to your purpose.
Review the 1 Click the sequence number of the target record. The AML Information Details page is
AML
information

2 On the AML Information Details page, review the AML information.
Download the 1 Click Download Search Result. The File Download dialog box is displayed.
AML 2 In the File Download dialog box, click Open or Save. The file is opened or saved to your
information local disk.


Advanced Functions Anti-Money Laundry 99



---

# Appendix A: Field Descriptions

Appendix A: Field Descriptions
Table 1: Field Description of Register Initial Information Page
Proposal No. The unique number of each proposal. By default, two fields will be
displayed for Proposal Number. Enter the Proposal Prefix, proposal
number will be generated automatically according to proposal
number generation rules.
(cid:129) If the prefix is not required, then only one field will be displayed for Proposal
Number. You can manually entered proposal number or proposal number will
be set automatically as the policy number.
鈥?Proposal number cannot be duplicated.
鈥?Proposal number can be linked to organization.
NOTE: System will recognize the proposal/policy organization by prefix.
(cid:129) If the proposal does not have a prefix, the policy/proposal organization follows
the agent organization. User must have the access to the policy organization.
Sales Channel Sales channel type, automatically displayed after Agent Code is set.
Agent Code Enter the agent code or double-click this field to select a code from
(cid:129) Agent code must be valid.
(cid:129) Agent status must be active.
(cid:129) Agent must have valid qualification to sell the product
Main Benefit Enter the product code or double-click this field to select a code
from the drop-down list.
(cid:129) Product entered must be the main product.
(cid:129) Product Code must be valid.
(cid:129) Product must be on sale, means that product end date must be later than
submission date.
(cid:129) Agent entered must have valid qualification to sell this product.
(cid:129) If agent is 'Individual Agent' or 'Company Direct', agent branch must allowed to
sell this product.
(cid:129) If agent is not 'Individual Agent' or 'Company Direct', agent branch must have
agreement with insurance company to sell this product.
Appendix A: Field Descriptions Register Initial Information Page 100


Submission Date Entered manually by user or select from the calendar tab. The field is
subsequently used by system to pull the premium table for premium
calculation. Therefore, when a premium rate is revised, this date will
be used to determine whether "old" or "new" rates are used for
premium calculation.
Format: DD/MM/YYYY
By default, the submission date is set to the system date.
Submission date cannot be later than the system date.
Submission date cannot be earlier than proposal date.
Submission date cannot be later than the product withdrawal date.
Proposal Date Entered manually by user or selected from the calendar tab.
Format: DD/MM/YYYY
Proposal date must not be on or before current system date.
Proposal date must not be more than 12 months earlier than the
Proposal date cannot be earlier than the product launch date.
Policy Currency Default currency of the policy. All premiums will be transacted
based on policy currency. Select from the drop-down list. Default as
default currency defined by product according to agent branch.
Initial Premium Total initial premium for all benefits applied for in the proposal.
Enter the initial premium amount and select a premium currency.
The amount entered is based on the total initial premium written in
the physical proposal form. This field is used to inform the
Agent/Cashier of the minimum amount to collect before issuance of
Conditional Interim Cover Certificate (CICC) if applicable.
Add After all the mandatory information is entered, click Add to
generate the policy number, and the system allows you to add
another proposal submitted by the same agent.
Submit After all the mandatory information is entered, click Submit. Then
the proposal number and policy number are generated and
displayed on the top of the page. The proposal will be allocated to
data entry users.
Submit and Data Entry After all the mandatory information is entered, if you need to
perform data entry directly, click Submit and Data Entry. The Data
Entry page is displayed. For details about data entry, refer to Data
Entry.
Appendix A: Field Descriptions Register Initial Information Page 101


Print Receipt After all the mandatory information is entered, if you need to print
receipt, click Print Receipt and ALL the proposals submitted by the
current agent on the current date will be printed.
Search Search out the proposal/policy with the proposal status of
Waiting for data entry. Then the user can modify the
initial registration information if necessary.
Exit To exit the current page and back to the homepage.
(cid:129) Register Initial Information
Basic Information Area
Table 2: Field Description of Basic Information Area
Sales Channel Sales channel type, which is retrieved from initial registration and
cannot be modified.
Proposal No. Generated during initial registration and cannot be changed
manually.
Policy No. Generated during initial registration and cannot be changed
manually.
Appendix A: Field Descriptions Basic Information Area 102


Submission Date Submission date entered during initial registration by authorized
user. Submission date must meet the following rules:
(cid:129) Not later than the current system date
(cid:129) Not later than product withdraw date
(cid:129) Not earlier than the proposal date
Proposal Date Proposal date entered during initial registration and can be changed
manually. Proposal date must meet the following rules:
(cid:129) Not earlier than product launch date
(cid:129) Not later than registration date
(cid:129) Not more than 12 months earlier than the current system date
Registration Date Date of initial registration and cannot be changed manually.
Commencement Date Commencement Date is defaulted as Submission Date and can be
changed manually. Commencement date cannot be later than the
Commencement date can be backdated when the following
requirements are met:
(cid:129) The backdating indicator of the benefit is Y in product definition.
(cid:129) The backdating period defined in product is not exceeded.
NOTE: If the backdating days exceed 183, the system will calculate the overdue interest
for total enforcing premium.
Agent Code Selected during initial registration and can be changed manually.
Backdating Indicator Automatically set by system and cannot be manually changed.
(cid:129) If commencement date is in the future, backdating indicator is set to N.
(cid:129) If commencement date is earlier than the current system date, backdating
indicator is set to Y.
Introducer Scheme Introducer type
Introducer No. Introducer No. must be valid.
(cid:129) If Introducer Type is entered, Introducer No. must be entered.
(cid:129) If Introducer Type is 'S', then the length of Introducer No. must be 9.
Currency Policy currency is retrieved from initial registration and can be
changed manually. Double-click this field to select a currency type
Appendix A: Field Descriptions Basic Information Area 103


Origin Code Source of the policy, which indicates whether the policy is a clean
case, term renewal policy, converted from old system, or has been
done some alterations.
Enter a code or double-click this field to select a code from the list.
(cid:129) 0: New Business
(cid:129) 1: Opted Policy
(cid:129) 2: Converted Policy
(cid:129) 3: Continuation
(cid:129) 4: Term Renewal
(cid:129) 5: Altered Policy
(cid:129) 6: Others
(cid:129) 7: Conversion from Deposit - New Policy (Bonus Units)
(cid:129) 8: Conversion from Deposit - Existing Policy
(cid:129) 9: From Maturity Proceeds
Conversion Info Detailed conversion information. This button is enabled when
Origin Code is set to 2 (Converted Policy). Click this button to
display the Conversion Info page and enter the related information
as follows:
1 Enter the original policy number in the Policy to Be Converted field.
2 Select a benefit (under the original policy) from the Convertible Benefit
drop-down list. Only convertible benefits (according to product setup) will be
displayed in the drop-down list.
3 Select a conversion type (partial or full) from the Conversion Type drop-down
4 Enter the converted sum assured in the Converted Sum Assured field.
5 Click Add to add more converted information if any.
6 After all the required information is entered, click Submit.
The related rules are as follows:
(cid:129) The original policy status must be In-force.
(cid:129) The original policy must not be frozen
(cid:129) The total current sum assured must not be greater than the sum assured of the
original benefit.
Maturity Proceed Indicate whether maturity proceeds are to be retained (Y or N).
Retained Indicator Maturity proceeds on a to-be-matured policy can be used to pay for
the premium due on a new proposal.
Maturity proceeds will not be retained under the following
conditions:
(cid:129) When the policy is declined, withdrawn, or postponed by
policy-holder/company, the system will remove the retained request from the
existing policies which have not matured, and not automatically retain the
maturity proceeds, which will be recorded in the transaction history.
(cid:129) If underwriter imposes extra loading, premium increases, the premium to be
paid uses maturity proceeds, or there is balance in projected maturity proceeds,
the system will prompt user to change the amount of maturity proceeds to be
retained at Data Entry UI, Load Extra UI and Amendment UI when user clicks
Appendix A: Field Descriptions Basic Information Area 104


Maturity This button is enabled when Maturity Proceed Retained Indicator is
set to Y or Origin Code is set as 9. Click this button to display the
Maturity Proceeds Information page.
On the Maturity Proceeds Information page displayed, enter the
related information as follows:
1 Enter the retained policy number in the Policy to Be Retained field.
2 Select a retained indicator (partial or full) from the Retained Indicator
drop-down list.
3 Enter the retained amount in the Amount to Be Retained field. If Retained
Indicator is set to full, this field is disabled.
4 Click Add to add more maturity proceeds information if any.
5 After all the information is entered, click Submit. The system will update the
retained maturity amount for the existing policies. The system will not adjust the
amount but retain the amount as indicated. Refunds will be carried out by
respective functions when required.
The related rules are as follows:
(cid:129) The status of the retained policies must be In-force.
(cid:129) The maturity proceeds retained amount must not be greater than the maturity
proceeds or projected maturity value of the potential mature policy.
(cid:129) The projected maturity proceeds are not fully retained by any policy.
The system will not check for the health warranty date if Origin
Code is set to 9.
The health warranty check is applicable for policies which have
already indicated that maturity proceeds are to be retained for the
payment of enforcing amount and the retained policies will only
mature after 30 days from LCA date.
NOTE: LCA will expire 30 days from the date of issue if the proposal status is still
Accepted or Conditionally Accepted.
Discount Type Enter the discount type code or double-click this field to select a
If Discount Type is Staff, the system will validate whether both the
policyholder and the main insured are staff and save the result into
the non-underwriting issues.
Policy Dispatch Type Way of delivering policy documents to client.
Enter the dispatch type code or double-click this field and select a
(cid:129) H: Hand
(cid:129) M: Mail
Initial Premium Initial premium amount. It is entered during initial registration and
Amount can be changed manually.
Appendix A: Field Descriptions Basic Information Area 105


Campaign Type Initial premium amount. It is entered during initial registration and
can be changed manually.
Twinning Policy No. A proposal can be twinned to an existing policy (enforce policy or
registered proposal) or multiple proposals sold under a package.
The system will add zeros in front of the twining policy number if it
is less than eight digits. Twinning Policy Number should be a valid
policy number.
Worksite Code Front office code. Enter the worksite code or double-click this field
to select a code from the list.
Marketing Code Enter the marketing code or double-click this field to select a code
Fact Find Indicator Fact Find indicator for life products. Enter the indicator code or
(Life) double-click this field to select a code.
(cid:129) 1: Full Disclosure
(cid:129) 2: Partial Disclosure
(cid:129) 3: Product Advise Only
(cid:129) 4: No Disclosure
(cid:129) 5: Not Applicable
(cid:129) 6: Not Required
Fact Find Indicator Fact Find indicator for health products. Enter the fact find indicator
(Health) code or double-click this field to select a code.
(cid:129) 1: Full Disclosure
(cid:129) 2: Partial Disclosure
(cid:129) 3: Product Advise Only
(cid:129) 4: No Disclosure
(cid:129) 5: Not Applicable
(cid:129) 6: Not Required
Vesting Indicator Indicate whether the proposer will change to the life assured when
the life assured attains a certain age.
(cid:129) Age and term must be greater than vesting age(currently is 21 years old) if
Vesting Indicator is set as 'Y'.
(cid:129) Policy must be third party policy if vesting Indictor is set as 'Y'.
Appendix A: Field Descriptions Basic Information Area 106


Billing Dispatch Type Way of delivering billing to client, including SMS, email, mail, and
none.
1 Click the Billing Dispatch Type button and on the page displayed, select one or
more types.
2 Click Submit and the selected items are updated in the Billing Dispatch Type
(cid:129) Enter Basic Information
Proposer Information Page
Table 3: Field Description of Company Proposer Information Page
Company Name Company proposer name.
Fuzzy Search Company name supports fuzzy search. You can enter one or several
consecutive letters (case insensitive) of the company name to search
out the company name containing these letters.
Search If there is an existing company proposer, enter the ROC No. or
company name and then click Search. The target proposer record
will be displayed in the Existing Customer Information page. Select
it and click Submit. The detailed information will be displayed in
the Basic Information area of the Company Proposal Information
information about a proposer is submitted. This number cannot be
Appendix A: Field Descriptions Proposer Information Page 107


Registered Country Country where the company is registered. Enter the country code or
Office No. Office phone number of the proposer
Office Ext Office phone extension number of the proposer
Fax No. Fax number of the proposer
Contact Person Tel No. Phone number of contact person
(cid:129) There is no bankruptcy record and the status of the company proposer is not
(cid:129) There is no company proposer record sharing the same Company Name, Party
ID Type, and Party ID No.
If all the checks pass, the proposer record will be displayed in the
Proposer area of the Data Entry page and the insurance role will be
updated.
Appendix A: Field Descriptions Proposer Information Page 108


the address of the proposer. The Correspondence Address page is
(cid:129) Company Proposer Information Page
Table 4: Field Description of Individual Proposer Information Page
First Name First name of the individual proposer
Last Name Last name of the individual proposer
Appendix A: Field Descriptions Proposer Information Page 109


Search If there is an existing individual proposer, enter the party ID type
and party ID No., or enter the proposer name and then click Search.
The target proposer record will be displayed on the Existing
information will be displayed in the Basic Information area on the
Individual Proposal Information page.
Identifier Type Type of the identifier that identifies the individual proposer
information about a proposer is submitted. This number cannot be
Alias Alias of the individual proposer.
Courtesy Title Salutation of the individual proposer. Enter the title code or
(cid:129) MR
(cid:129) MS
Nationality Nationality of the proposer. Enter the nationality code or
Gender Gender of the individual proposer. Enter the gender code or
DOB Date of birth of the individual proposer. Format: DD/MM/YYYY
Occupation Occupation of the proposer. Enter the occupation code or
Marital Status Marital status of the individual proposer. Enter the marital status
code or double-click this field to select a code from the list. 1:
Married 2: Single 3: Divorced 4: Widowed 5: Separated 6: Other
For the existing individual proposer record, if Proof of Age is Y, you
cannot change it to N. Otherwise, an error message Existing
Customer Age Admitted will be displayed.
Spouse Child Indicator Whether the life assured is the spouse or child of the proposer.
Appendix A: Field Descriptions Proposer Information Page 110


Annual Income Annual income of the proposer. Annual income will be compared
with annual premium to ensure that the annual premium to annual
income of proposer ratio is not too high according to underwriting
rules.
Off-shore/External Indicate whether the proposer has an off-shore/external account.
Account
Permanent Resident Indicate whether the proposer is a permanent resident in the
Ind country of the insurance company.
Religion Religion of the proposer. Enter the race code or double-click this
Industry Industry in which the proposer works. Enter the industry code or
Home No. Home phone number of the proposer
Fax No. Fax number of the proposer
Handphone No. Mobile phone number of the proposer
Office No. Office phone number of the proposer
Office Ext Office phone extension number of the proposer
Appendix A: Field Descriptions Proposer Information Page 111


(cid:129) The status of individual proposer is Active.
(cid:129) The individual proposer does not have a bankruptcy record.
(cid:129) The age of the individual proposer is within the age limit defined by the benefit.
(cid:129) There is no existing proposer record sharing the same five basic attributes: name,
party ID type, party ID No., gender, and DOB.
If all the checks pass, the proposer record will be displayed in the
Proposer area of the Data Entry page.
NOTE: If two proposer records share some of the five attributes, a warning message An
existing party with similar party details found. Please
check for Inconsistent Person Record! will be displayed. You can
click Continue to confirm the record or modify the record.
Appendix A: Field Descriptions Proposer Information Page 112


the address of the proposer. The Correspondence Address page is
(cid:129) Individual Proposer Information Page
Appendix A: Field Descriptions Proposer Information Page 113


Life Assured Information Page
Table 5: Field Description of Life Assured Information Page
First Name First name of the life assured
Last Name Last name of the life assured
Search If there is an existing life assured record, enter the party ID type and
party ID No. or enter the life assured name and then click Search.
The target life assured record will be displayed on the Existing
information will be displayed in the Basic Information area on the
Life Assured Information page.
Identifier Type Type of the identifier that identifies the life assured
information about a life assured is submitted. This number cannot
be changed.
Relationship with Relationship of the life assured with the proposer. Enter the
Proposer relationship code or double-click this field to select a code from the
displayed as the life assured information.
If the proposer is a company, then Self is not allowed to be selected.
Alias Alias of the life assured
Courtesy Title Salutation of the life assured. Enter the title code or double-click this
field to select a code from the list, for example, Mr., Ms.
Gender Gender of the life assured. Enter the gender code or double-click
this field to select a code from the list.
DOB Date of birth of the life assured. Format: DD/MM/YYYY
Nationality Nationality of the life assured. Enter the nationality code or
Appendix A: Field Descriptions Life Assured Information Page 114


Marital Status Marital status of the individual proposer. Enter the marital status
(cid:129) 1: Married
(cid:129) 2: Single
(cid:129) 3: Divorced
(cid:129) 4: Widowed
(cid:129) 5: Separated
(cid:129) 6: Other
Number of Children Number of children of the life assured.
For the existing individual proposer record, if Proof of Age is Y, you
cannot change it to N. Otherwise, an error message Existing
Customer Age Admitted will be displayed.
Annual Income Annual income of the life assured.
Permanent Resident Indicate whether the proposer is a permanent resident in the
Ind country of the insurance company.
Religion Religion of the life assured. Enter the race code or double-click this
Occupation Occupation of the life assured. Enter the occupation code or
Industry Industry in which the life assured works. Enter the industry code or
Height (m) Height of the life assured in meters.
Weight (kg) Weight of the life assured in kilograms.
Smoking Indicator Indicate whether the life assured smokes or not.
(cid:129) N: non-smoking
(cid:129) Y: smoking
For the non-smoking life assured, a discount may be granted.
Preferred Life Indicator Indicate whether the life assured is a preferred insured or not.
Whether the life insured is preferred depends on his or her health
status or financial status. For the preferred insured, a discount may
be granted.
If Smoking Indicator is Y, Preferred Life Indicator must be N.
W means not applicable to the current policy.
Appendix A: Field Descriptions Life Assured Information Page 115


Medical Exam Indicate whether medical exam is performed or not.
(cid:129) Yes: medical exam performed
(cid:129) No: medical exam not performed
(cid:129) Paramedic: Indicate whether the Life Assured requires a paramedic or not.
Parent Cover Amount Aggregate face amount purchased to cover the parent.
Home No. Home phone number of the life assured.
Fax No. Fax number of the life assured.
Office No. Office phone number of the life assured.
Office Ext Office phone extension number of the life assured.
Handphone No. Mobile phone number of the life assured.
(cid:129) The status of the life assured must be Active.
(cid:129) The life assured does not have a bankruptcy record.
(cid:129) The age of the life assured is within the age limit defined in the plan code. During
proposal registration, the system date will be referred for age calculation as the
commencement date is not yet applicable.
(cid:129) There is no existing life assured record sharing the same five basic attributes:
name, party ID type, party ID No., gender, and DOB.
If all the checks pass, the life assured record will be displayed in the
Life Assured area on the Data Entry page.
NOTE: If two life assured records share some of the five attributes, a warning message
An existing party with similar party details found.
Please check for Inconsistent Person Record! will be displayed.
You can click Continue to confirm the record or modify the record.
Appendix A: Field Descriptions Life Assured Information Page 116


the life assured address. The Correspondence Address page is
(cid:129) Enter Life Assured Information
Appendix A: Field Descriptions Life Assured Information Page 117


Premium Payer Information Page
Table 6: Field Description of Company Premium Payer Information Page
Company Name Company payer name.
Fuzzy Search Company name supports fuzzy search. You can enter one or several
consecutive letters (case insensitive) of the company name to search
out the company name containing these letters.
Search If there is an existing company, enter the ROC No. or company
name and then click Search. The target company record will be
displayed in the Existing Customer Information page. Select it and
click Submit. The detailed information will be displayed in the Basic
Information area of the Company Premium Payer Information
information about a payer is submitted. This number cannot be
Relationship with Relationship of the premium payer with the proposer. Enter the
Proposer relationship code or double-click this field to select a code from the
displayed as the payer information.
If the payer is a company, then Self is not allowed to be selected.
Registered Country Country where the company is registered. Enter the country code or
Office No. Office phone number of the payer
Office Ext Office phone extension number of the payer
Fax No. Fax number of the payer
Contact Person Tel No. Phone number of contact person
Appendix A: Field Descriptions Premium Payer Information Page 118


(cid:129) There is no bankruptcy record and the status of the company payer is not
(cid:129) There is no company payer record sharing the same Company Name, Party ID
Type, and Party ID No.
If all the checks pass, the payer record will be displayed in the Payer
area of the Data Entry page and the insurance role will be updated.
the address of the payer. The Correspondence Address page is
Appendix A: Field Descriptions Premium Payer Information Page 119


(cid:129) Company Premium Payer Information Page
Table 7: Field Description of Individual Premium Payer Information Page
First Name First name of the individual premium payer
Last Name Last name of the individual premium payer
Search If there is an existing individual premium payer, enter the party ID
type and party ID No., or enter the individual premium payer name
The target individual premium payer record will be displayed on the
Existing Customer Information page. Select it and click Submit. The
detailed information will be displayed in the Basic Information area
on the Individual Premium Payer Information page.
Identifier Type Type of the identifier that identifies the individual premium payer
information about an individual premium payer is submitted. This
number cannot be changed.
Relationship with Relationship of the individual premium payer with the proposer.
Proposer Enter the relationship code or double-click this field to select a code
displayed as the individual premium payer information.
If the proposer is a company, then Self is not allowed to be selected.
Alias Alias of the individual premium payer.
Courtesy Title Salutation of the individual premium payer. Enter the title code or
(cid:129) MR
(cid:129) MS
Appendix A: Field Descriptions Premium Payer Information Page 120


Gender Gender of the individual premium payer. Enter the gender code or
DOB Date of birth of the individual premium payer. Format:
Marital Status Marital status of the individual premium payer. Enter the marital
status code or double-click this field to select a code from the list.
(cid:129) 1: Married
(cid:129) 2: Single
(cid:129) 3: Divorced
(cid:129) 4: Widowed
(cid:129) 5: Separated
(cid:129) 6: Other
For the existing individual premium payer record, if Proof of Age is
Y, you cannot change it to N. Otherwise, an error message
Existing Customer Age Admitted will be displayed.
Nationality Nationality of the individual premium payer. Enter the nationality
Annual Income Annual income of the individual premium payer.
Permanent Resident Indicate whether the individual premium payer is a permanent
Ind resident in the country of the insurance company.
Religion Religion of the individual premium payer. Enter the race code or
Occupation Occupation of the individual premium payer. Enter the occupation
Industry Industry in which the individual premium payer works. Enter the
industry code or double-click this field to select a code from the list.
Home No. Home phone number of the individual premium payer
Fax No. Fax number of the individual premium payer
Office No. Office phone number of the individual premium payer
Appendix A: Field Descriptions Premium Payer Information Page 121


Office Ext Office phone extension number of the individual premium payer
Handphone No. Mobile phone number of the individual premium payer
(cid:129) The status of individual premium payer is Active.
(cid:129) The individual premium payer does not have a bankruptcy record.
(cid:129) The age of the individual premium payer is within the age limit defined in the
plan code. During proposal registration, the system date will be referred for age
calculation as the commencement date is not yet applicable.
(cid:129) There is no existing individual premium payer record sharing the same five basic
attributes: name, party ID type, party ID No., gender, and DOB.
If all the checks pass, the individual premium payer record will be
displayed in the Individual Premium Payer area of the Data Entry
NOTE: If two individual premium payer records share some of the five attributes, a
warning message An existing party with similar party details
found. Please check for Inconsistent Person Record! will be
displayed. You can click Continue to confirm the record or modify the record.
Appendix A: Field Descriptions Premium Payer Information Page 122


the address of the individual premium payer. The Correspondence
Address page is displayed. Enter address information in the Address
Information area, and then click Apply. An address record number
will be generated and the address record will be displayed in the
(cid:129) Individual Premium Payer Information Page
Appendix A: Field Descriptions Premium Payer Information Page 123


Payment Method Information Page
Table 8: Field Description of Payment Method Information Page
Payment Method Enter the payment method code or double-click this field to select a
For different payment methods, you may need to enter extra
payment information. For example, for credit card payment method,
you need to enter the credit card type, credit card number and credit
card expiry date.
Payment methods supported are:
(cid:129) C: Cash
(cid:129) K: Cheque
(cid:129) DDA: Direct Debit
(cid:129) OA: CPF OA Fund
(cid:129) SRS: SRS Fund
(cid:129) ASA: ASPF-SA
(cid:129) SSS: SSS
(cid:129) SA: CPF SA Fund
(cid:129) MSS : CPF MSS Fund
(cid:129) MSPS : CPF MSPS Fund
(cid:129) MEDI: CPF MEDISSIVE Fund
(cid:129) CC: Credit Card
(cid:129) AOA: ASPF-OA
(cid:129) ASPFMSPS: ASPF-MSPS
Submit Click Submit. The system performs the following validation checks:
(cid:129) The payment method must be allowed by the payment method limit table.
(cid:129) The length and structure of bank account number must be valid for the selected
bank.
(cid:129) The payment method must be allowed for the selected currency.
(cid:129) The payment method must be allowed by the selected service branch.
(cid:129) The payment method and payment frequency must match.
If all the checks pass, the payment method record will be displayed
in the Payment Method area of the Data Entry page and the system
generates the renewal premium payment method.
The following fields are dynamically displayed when CC and Direct Debit are selected:
Appendix A: Field Descriptions Payment Method Information Page 124


Account Type There are two account types:
(cid:129) Credit Card
(cid:129) Direct Debit
This field is read-only and displayed when CC or DDA is selected in
Payment Method.
Account Holder Full Full name of the account holder which was used to open the bank
Name account.
Bank Headquarter Pre-configured in system.
Code
Bank Code Pre-configured in system.
Debit/Credit Three values in the drop-down list:
(cid:129) Debit
(cid:129) Credit
(cid:129) Both
Account Status Two values in the drop-down list:
(cid:129) Valid
(cid:129) Invalid
Authorization Status There're four authorization status:
(cid:129) Waiting for Authorization
(cid:129) Authorized
(cid:129) Rejected
(cid:129) Authorization in Progress
The default value in the drop-down list is configurable. It varies by
configuration data in a ratetable named rBankAuthorization (See
Bank Authorization in LifeSystem System Configuration Guide for
details):
1 If 'Need Authorization' is configured as 'N' or the data not configured, then the
default value is 'Authorized' and the field is read only, cannot be modified.
2 If 'Need Authorization' is configured as 'Y', then the default value is 'Waiting for
authorization', but user can manually modify the field to 'Authorized' or
'Rejected'.
NOTE: The field can only be set to 'Authorization in Progress' status by the System. If
user tries to modify the field to 'Authorization in Progress' online, then system pops up
an error message: User can't update the status to
'Authorization in Progress'.
Credit Card No. For Credit Card only.
Accepted format: XXXX-XXXX-XXXX-XXXX (0 <= X <= 9)
Appendix A: Field Descriptions Payment Method Information Page 125


Credit Card Type For Credit Card only.
Four types are supported:
(cid:129) Master Card
(cid:129) Visa Card
(cid:129) BCA
(cid:129) JCB
Credit Card Expiry For Credit Card only.
Date Month/Year when the credit card expires.
Format: mm/yy
This date should be later than the current system date, otherwise an
error message prompts, saying 鈥滳redit Card Expiry Date
should be greater than system date.鈥?
Account No. For Debit Card only.
Debit card's account number.
Bank Account City For Debit Card only.
The city where the debit card holder opened the account.
(cid:129) Enter Payment Method Information
Appendix A: Field Descriptions Payment Method Information Page 126


Benefit Information Page
Benefit Information Page of Traditional Products

Appendix A: Field Descriptions Benefit Information Page 127




Appendix A: Field Descriptions Benefit Information Page 128


Table 9: Field Description of Benefit Information Page (Traditional)
Appendix A: Field Descriptions Benefit Information Page 129


Appendix A: Field Descriptions Benefit Information Page 130


Cash Bonus Option Disposal option for cash bonus. Will be displayed if the product has
cash bonus.
Enter the option code or double-click this field to select a code from
(cid:129) 1: To receive SB/CB in cash
(cid:129) 2: To use SB/CB to pay premium
(cid:129) 3: To leave SB/CB on deposit with Company
(cid:129) 4: Option (3) for xx years thereafter Option (2).
(cid:129) 5: To use cash bonus to buy an additional paid-up sum assured
Otherwise, a prompt message Cash Bonus Option Options
Are XXX is displayed. You need to modify the value accordingly.
Indexation Type Enter the indexation type code or double-click this field to select a
code.
(cid:129) 1: CPI
(cid:129) 2: Dynamic Rate
Otherwise, a prompt message Indexation Type Options
Are XXX is displayed. You need to modify the value accordingly.
Indexation Calculation After the Indexation Type is entered, if only one corresponding
Basis indexation calculation basis option is defined, the Indexation
Calculation Basis is displayed automatically and cannot be
changed; if more than one indexation calculation basis option is
defined, you can select one from the drop-down list.
Survival Benefit Disposal option for survival benefit. Will be displayed if the product
Option selected has survival benefit.
Enter the option code or double-click this field to select a code from
(cid:129) 1: To receive SB/CB in cash
(cid:129) 2: To use SB/CB to pay premium
(cid:129) 3: To leave SB/CB on deposit with Company
(cid:129) 4: Option (3) for xx years thereafter Option (2).
(cid:129) 5: To use SB/CB to buy an additional paid-up sum assured
Save To save the current benefit information
Add Benefit To save the current benefit information and to add a new benefit
Cancel To cancel operation
Appendix A: Field Descriptions Benefit Information Page 131


Benefit Information Page for Investment Product

Appendix A: Field Descriptions Benefit Information Page 132


Table 10: Field Description of Benefit Information Page (Investment)
Appendix A: Field Descriptions Benefit Information Page 133


Premium Amount Premium amount must be within the limit defined in product
according to payment frequency and payment method.
Premium amount entered can be standard premium (before modal
factor) or the installment premium (after modal factor) according to
configuration at system level.
Appendix A: Field Descriptions Benefit Information Page 134


Use Investment This field will be displayed only if the product has allowed
Scheme investment scheme. Select one of the investment scheme, the funds
with pre-defined apportionment will be automatically displayed in
MA/MS Factor This field will only be displayed if minimum/maximum Sum
Assured calculation is related with MA/MS Factor.
Single Top up Amount Top up is the additional amount investment in the
investment-linked policy. If single top-up is allowed for this product,
you can enter the single top up amount. The single top up amount
must be greater than zero.
MS Factor This field will only be displayed if minimum/maximum Sum
Assured calculation is related with MS factor.
Top Up Amount If recurring top up is allowed for this product, you can enter the top
up amount.
(cid:129) The recurring top up amount must be greater than zero.
(cid:129) If the system parameter is defined as "input AF" (means the premium entered is
the installment premium, then the recurring top up input amount follows
premium payment frequency. For example, if the recurring top up is 100 and
payment frequency is monthly, system considers the 100 is monthly amount and
will calculate annual amount as 1200.
Investment Strategy To add Investment Strategy. Refer to Enter Investment Strategy.
Appendix A: Field Descriptions Benefit Information Page 135


Delete Investment If an investment strategy exists, you need to click this button and
Strategy then click Investment Strategy button if you want to change the
current strategy.
Enter Coupon Option Coupon is the dividend units declared by fund house for a specific
fund.
If the funds selected are defined with coupon, you need to click
Enter Coupon Option and select an option from the list.
Save To save the benefit information.
Add Benefit To save the current benefit information and to add a new benefit.
Benefit Information Page of Annuity Product

Table 11: Field Description of Benefit Information Page (Annuity)
Appendix A: Field Descriptions Benefit Information Page 136


Otherwise, a prompt message Year/Age of Coverage Term
Appendix A: Field Descriptions Benefit Information Page 137


Premium Amount Premium amount must be greater than zero.
Premium amount entered can be standard premium (before modal
factor) or the installment premium (after modal factor) according to
configuration at system level.
Type of Deferred Enter the type code or double-click this field to select a code from
Period for Annuity the list.
(cid:129) 1: Immediate
(cid:129) 2: Start from age at anniversary date
(cid:129) 3: Deferred for certain number of years
(cid:129) 4: Age of birthday
Otherwise, a prompt message Type of Deferred Period
for Annuity Options Are XXX is displayed. You need to
Deferred Period for The entered value must be allowed by product definition.
Annuity Otherwise, a prompt message Deferred Period for
Annuity Options Are XXX is displayed. You need to modify
Appendix A: Field Descriptions Benefit Information Page 138


Type of Annuity Enter the type code or double-click this field to select a code from
Installment Period the list.
(cid:129) 1: For a certain year
(cid:129) 2: Up to a certain age
(cid:129) 3: For whole life
Installment Period for The entered value must be allowed by product definition.
Annuity Otherwise, a prompt message Installment Period for
Annuity Options Are XXX is displayed. You need to modify
Guarantee Period Length of time that the insurer will pay out for, regardless of whether
the life assured survives the guarantee period or not. This field will
only be displayed if guarantee period is defined by product.
Installment Frequency Enter the frequency code or double-click this field to select a code
(cid:129) H: Half-Yearly
Annuity Payment Select a payment mode from the drop-down list.
Mode
Save To save the benefit record
Add Benefit To add a new benefit record
Cancel To cancel the operation
Appendix A: Field Descriptions Benefit Information Page 139


Benefit Information Page of Mortgage Product

Table 12: Field Description of Benefit Information Page (Mortgage)
Second Life Assured Select from the list.
If the benefit is joint life product, then Second Life Assured will be
Second Life Assured should not select the same person selected for
First Life Assured.
Appendix A: Field Descriptions Benefit Information Page 140


Appendix A: Field Descriptions Benefit Information Page 141


the method code or double-click this field to select a calculation.
Different input fields will be displayed according to different
calculation method selected:
Year from Start year for mortgage
Year to End year for mortgage
Interest Rate for Interest rate for mortgage. Whether the mortgage interest rate is
Mortgage required is defined by product (Mortgage Decreasing Term).
Add Click Add to add another mortgage interest rate record if any.
Delete Select a mortgage interest rate record and click Delete to delete the
record if required.
Manual Decreasing SA Indicate whether to manually decrease the sum assured. If you enter
Schedule Indicator Y, you need to arrange a schedule for sum assured decreasing by
setting Policy Year and the corresponding Decreasing SA.
Appendix A: Field Descriptions Benefit Information Page 142


Save After all the mandatory information is entered, click Save. The
(cid:129) The system validates the limits against the product setup. If validation failed, the
corresponding error message will be displayed. Validations including:
鈥?Allowed coverage term and premium term.
鈥?Max and Min age of Policy Holder, Life Assured or Joint life.
鈥?Max and Min Premium for one premium payment according to different
conditions, such as payment frequency and method.
鈥?Min Total Installment Premium for one policy.
鈥?Max and Min SA for one product according to different conditions such as
age, preferred life and so on.
鈥?Minimum investment premium for each fund.
(cid:129) The system calculates the premium and sum assured according to calculation
formulas defined by product.
Add Benefit To add a new benefit.
Appendix A: Field Descriptions Benefit Information Page 143


Benefit Information Page of Variable Annuity Product

Table 13: Field Description of Benefit Information Page (Variable Annuity)
Appendix A: Field Descriptions Benefit Information Page 144


Type of Coverage Type of benefit coverage period. Enter the type code or double-click
Period this field to select a code.
Year/Age of Coverage Length of benefit coverage corresponding to the Type of Coverage
Term Period selected. The entered value must be allowed by product
definition. Otherwise, a prompt message Year/Age of
Coverage Term Options Are XXX is displayed. You need to
Type of Premium Method for premium payment period. Enter the type code or
Payment Period double-click this field to select a code.
Year/Age of Premium Length of premium payment corresponding to the Type of Premium
Term Payment Period selected.The entered value must be allowed by
product definition. Otherwise, a prompt message Year/Age of
Premium Term Options Are XXX is displayed. You need to
Appendix A: Field Descriptions Benefit Information Page 145


Initial Premium Initial premium payment frequency. Enter the frequency code or
Frequency double-click this field to select a code.
Premium Amount (cid:129) Premium amount must be great than zero.
(cid:129) If product is defined as single premium, premium amount entered refers to
single premium before discount.
(cid:129) If product is defined as regular premium and standard premium rate is on a
yearly basis, premium amount entered refers to annual premium.
(cid:129) If product is defined as regular premium and standard premium rate is on a
monthly basis, premium amount entered refers to monthly premium.
Tariff Type This field will only be displayed if the tariff type is defined by
product
Appendix A: Field Descriptions Benefit Information Page 146


Type of Deferred Variable Annuity payment can be deferred for certain period. Client
Period for Variable can choose when to start his/her payment. Enter the type code or
Annuity double-click this field to select a code.
(cid:129) 1: Immediate
(cid:129) 2: Start from age at anniversary date
(cid:129) 3: Deferred for certain no. of years
(cid:129) 4: Age of birthday
Deferred Period for Length of deferred period corresponding to the Type of Deferred
Variable Annuity Period for Variable Annuity selected. The entered value must be
allowed by product definition. Otherwise, a prompt message
Deferred Period for Annuity Options Are XXX is
displayed. You need to modify the value accordingly.
Type of Variable Length type of variable annuity installment. Enter the code or
Annuity Installment double-click this field to select a code.
(cid:129) 1: For a certain year
(cid:129) 2: Up to a certain age
(cid:129) 3: For whole life
Installment Period for Length of variable annuity installment. It must be the same value as
Variable Annuity Year/Age of Premium Term. The entered value must be allowed by
product definition. Otherwise, a prompt message Installment
Period for Annuity Options Are XXX is displayed. You
Guarantee Period Length of time that the insurer will pay out for, regardless of whether
the life assured survives the guarantee period or not. This field will
only be displayed if guarantee period is defined by product.
Installment Frequency Installment frequency of the Variable Annuity. Enter the frequency
code or double-click this field to select a code.
(cid:129) 1: Yearly
(cid:129) 2: Half-Yearly
(cid:129) 3: Quarterly
(cid:129) 4: Monthly
(cid:129) 5: Single
Appendix A: Field Descriptions Benefit Information Page 147


Variable annuity Select a payment method from the drop-down list.
Payment Mode
GMxB Information Guarantee Minimum Benefit (GMxB) information, including:
(cid:129) GMDB: Guaranteed minimum death benefit
(cid:129) GMAB: Guaranteed minimum accumulation benefit
(cid:129) GMWB: Guaranteed minimum withdrawal benefit
(cid:129) GMIB: Guaranteed minimum income benefit
Only allowed GMxB (GMDB/GMAB/GMWB/GMIB) options will
be displayed. The user can choose whether to select the GMxB
option but cannot change the current status if the option is selected
by default according to definition.
Single Top up Amount If single top-up is allowed for this product, you can enter the single
top up amount. The single top up amount must be greater than zero.
Top up Amount If recurring top up is allowed for this product, you can enter the top
up amount.
(cid:129) The recurring top up amount must be greater than zero.
(cid:129) If the system parameter is defined as "input AF" (means the premium entered is
the installment premium, then the recurring top up input amount follows
premium payment frequency. For example, if the recurring top up is 100 and
payment frequency is monthly, system considers the 100 is monthly amount and
will calculate annual amount as 1200.
Appendix A: Field Descriptions Benefit Information Page 148


Investment Strategy To add Investment Strategy. Refer to Enter Investment Strategy.
Delete Investment To delete investment strategy.
Strategy
Enter Coupon Option If the funds selected are defined with coupon, you need to click
Enter Coupon Option and select an option from the list.
Save To save the current benefit information.
Add Benefit To save the current benefit information and to add a new benefit.
(cid:129) Modify Main Benefit Information
Investment Strategy Page
Table 14: Field Description of Investment Strategy Page
Filed Description
Basic Investment Basic investment premium is retrieved from the product data entry
Premium screen and cannot be edited.
Recurring Top Up Recurring top up is retrieved from data entry screen if the user has
input the amount. If not, the user can manually enter the amount if
necessary.
Investment Strategy Manually enter or double-Click the drop-down list to select an
Code investment strategy code
(cid:129) If the strategy is not a DCA plan or a self-defined strategy, the system will display
the fields fund, policy year from, policy year to, and premium apportionment %
accordingly. These fields are read only.
(cid:129) If the strategy is not a DCA plan but it is a self-defined strategy (Strategy Code is
7-Own Choose), the system will display the fields policy year from, policy year
to, fund, and premium apportionment % for user to input.
(cid:129) If the strategy is a DCA plan, the system will display the pre-defined strategy
information. If the strategy is defined as editable, the Edit button will be enabled.
User can amend the pre-defined strategy information.
At New Business, if the investment strategy code entered is 0, an
error message Investment strategy zero is not allowed in this UI will
be displayed.
Appendix A: Field Descriptions Investment Strategy Page 149


Filed Description
Investment Horizon Investment horizon refers to the period that you can stay invested
before you expect to cash out your investment.
The input value must be allowed according to the strategy selected.
(cid:129) If it is the self-defined strategy (Strategy Code is 7-Own Choose), there's no need
to enter the investment horizon.
(cid:129) If it is DCA strategy, investment horizon can be input as 0.
Fund Selected If it is the self-defined strategy (Strategy Code is 7-Own Choose), all
funds which are allowed by products will be displayed and the user
can select the funds used for the strategy.
Strategy Details The user can define the investment plan by entering the fund
apportionment according to different policy year. The user can click
Add Year to add new policy year range or Delete Year to remove the
policy year range.
(cid:129) The input value must not be greater than the policy term.
(cid:129) Policy Year From and Policy Year To must be continuous and in sequence.
(cid:129) Enter Investment Strategy
Waiver Benefit Information Page
Table 15: Field Description of Waiver Benefit Information Page
Benefit Type Waiver benefit selected. Cannot be modified.
Life Assured Life Assured of waiver benefit. Automatically displayed according to
different waiver types.
Waiver Benefit Benefit to be waived.
Coverage Type Enter the type code or double-click this field to select a code.
Otherwise, a prompt message Coverage Type Options Are XXX is
displayed. You need to modify the value accordingly.
Appendix A: Field Descriptions Waiver Benefit Information Page 150


Coverage Term The entered value must be allowed by product definition.
Otherwise, a prompt message Coverage Term Options Are
XXX is displayed. You need to modify the value accordingly (apply
to all Coverage Term):
Waiver/Rider coverage term cannot be greater than coverage term of
main benefit.
Premium Payment Enter the type code or double-click this field to select a code.
Type
Otherwise, a prompt message Premium Payment Type
Waiver/Rider premium payment term cannot be greater than
premium payment term of main benefit
Premium Payment The entered value must be allowed by product definition.
Term Otherwise, a prompt message Premium Payment Term
accordingly (apply to all Premium Payment Term):
Waiver/Rider premium payment term cannot be greater than
premium payment term of main benefit.
Payment Frequency Enter the frequency code or double-click this field to select a code
(cid:129) H: Half-Yearly
SA Waived of Waived Default as 0 and can be changed if SA waived is less than initial SA
Benefit of waived benefit. The entered SA waived of waived benefit cannot
exceed the initial SA of waived benefit.
Annual Benefit If annual benefit exists, it can be added to waiver initial SA
calculation (configuration required).
Editable if benefit needs Annual Benefit.
Appendix A: Field Descriptions Waiver Benefit Information Page 151


Initial SA of Waived Initial sum assured of the waived benefit attached, read only.
Benefit
Annual Amount Annual Premium amount to be waived for the waived benefit.
Waived Automatically calculated and cannot be modified.
Save After entering all the required waiver information, click Save.
System will validates waiver information against product definition,
such as age limit, premium/SA limit, allowed coverage and premium
payment term, etc. The system will calculate sum assured and
premium of the waiver benefit.
Cancel To cancel operation
(cid:129) Add Waiver
Beneficiary Page
Table 16: Field Description of Beneficiary Page
First Name First name of the beneficiary
Last Name Last name of the beneficiary
Search If there is an existing beneficiary record, enter the party ID type and
party ID No., or enter the beneficiary name and then click Search.
The target beneficiary record will be displayed in the Existing
information will be displayed in the Basic Information area of the
Beneficiary page.
Identifier Type Type of the identifier that identifies the beneficiary
information about a beneficiary is submitted. This number cannot
be changed.
Beneficiary Beneficiary's relationship with the proposer. Enter the relationship
Designation code or double-click this field to select a code from the list.
Share (%) Beneficiary's share percentage
Appendix A: Field Descriptions Beneficiary Page 152


Alias Alias of the beneficiary.
Courtesy Title Salutation of the beneficiary. Enter the title code or double-click this
Gender Gender of the beneficiary. Enter the gender code or double-click this
DOB Date of birth of the beneficiary. Format: DD/MM/YYYY
Add Other After information of a beneficiary is entered, click Add Other to add
another beneficiary if any.
Appendix A: Field Descriptions Beneficiary Page 153


the address of the beneficiary. The Correspondence Address page is
Appendix A: Field Descriptions Beneficiary Page 154


(cid:129) The status of beneficiary is Active.
(cid:129) There is no existing beneficiary record sharing the same five basic attributes:
name, party ID type, party ID No., gender, and DOB.
(cid:129) The share percentage of all beneficiaries must be 100%.
(cid:129) If all the checks pass, the beneficiary record will be displayed in the Beneficiary
area of the Data Entry page.
NOTE: If two beneficiary records share some of the five attributes, a warning message
An existing party with similar party details found.
Please check for Inconsistent Person Record! will be displayed.
You can click Continue to confirm the record or modify the record.
(cid:129) Enter Beneficiary Information
Trustee Information Page
Table 17: Field Description of Company Trustee Information Page
Company Name Company trustee name.
Search If there is an existing company trustee record, enter the ROC No. or
company name and then click Search. The target trustee record will
be displayed in the Existing Customer Information page. Select it
and click Submit. The detailed information will be displayed in the
Basic Information area of the Company Trustee Information page.
information about a trustee is submitted. This number cannot be
Appendix A: Field Descriptions Trustee Information Page 155


Registered Country Country where the trustee is registered. Enter the country code or
Office No. Office phone number of the trustee
Office Ext Office phone extension number of the trustee
Fax No. Fax number of the trustee
Contact Person Phone number of contact person
Telephone No.
(cid:129) There is no bankruptcy record and the status of the company trustee is not
(cid:129) There is no company trustee record sharing the same Company Name, Party ID
Type, and Party ID No.
If all the checks pass, the trustee record will be displayed in the
Trustee area of the Data Entry page and the insurance role will be
updated.
Appendix A: Field Descriptions Trustee Information Page 156


the address of the trustee. The Correspondence Address page is
(cid:129) Company Trustee Information Page
Table 18: Field Description of Individual Trustee Information Page
First Name First name of the individual trustee
Last Name Last name of the individual trustee
Appendix A: Field Descriptions Trustee Information Page 157


Search If there is an existing individual trustee record, enter the party ID
type and party ID No., or enter the trustee name and then click
Search.
The target trustee record will be displayed in the Existing Customer
Information page. Select it and click Submit. The detailed
information will be displayed in the Basic Information area of the
Individual Trustee Information page.
Identifier Type Type of the identifier that identifies the trustee
information about a trustee is submitted. This number cannot be
Alias Alias of the individual trustee.
Courtesy Title Salutation of the individual trustee. Enter the title code or
Gender Gender of the individual trustee. Enter the gender code or
DOB Date of birth of the individual trustee. Format: DD/MM/YYYY
Nationality Nationality of the individual trustee. Enter the nationality code or
Appendix A: Field Descriptions Trustee Information Page 158


(cid:129) The status of individual trustee is Active.
(cid:129) The individual trustee does not have a bankruptcy record of transferred status.
(cid:129) The trustee age (Age Next Birthday) must be greater than 21.
(cid:129) There is no existing trustee record sharing the same five basic attributes: name,
party ID type, party ID No., gender, and DOB.
If all the checks pass, the trustee record will be displayed in the
Trustee area of the Data Entry page and the insurance role will be
updated. System to create endorsement at point of policy
generation..
NOTE: If two trustee records share some of the five attributes, a warning message An
existing party with similar party details found. Please
check for Inconsistent Person Record! will be displayed. You can
click Continue to confirm the record or modify the record.
Appendix A: Field Descriptions Trustee Information Page 159


the address of the trustee. The Correspondence Address page is
(cid:129) Individual Trustee Information Page
Appendix A: Field Descriptions Trustee Information Page 160


Comment Area
Table 19: Field Description of Comment Area on Data Entry Page
Data Entry Comment Enter comments for data entry if any.
Verification Comment Comments entered during verification and cannot be modified here.
Underwriting Comments entered during underwriting and cannot be modified
Comment here.
Amendment in Comments entered during amendment and cannot be modified
Progress Comment here.
Pending Reason If you decide to suspend the proposal, enter the pending reason
code or double-click this field to select a code from the list, and then
click Save.
Underwriting (cid:129) If manual underwriting is required, set Underwriting Indicator to Y. The
proposal will be sent to the underwriting module after verification even if auto
underwriting passes. One UW issue 鈥淢anual UW is mandatory as advised鈥?will
be added to outstanding issues.
(cid:129) If Underwriting Indicator is set to N, the proposal will not be sent to the
underwriting module if it passes the auto underwriting.
(cid:129) Add Modification Comments
Appendix A: Field Descriptions Comment Area 161


Verification Page
Table 20: Field Description of Verification Page
Submit If no information needs to be updated, you can click Submit to
submit the proposal. The system checks whether there are
outstanding issues.
(cid:129) If there are outstanding non-underwriting issues, the proposal status will still be
(cid:129) If there are no outstanding non-underwriting issues but outstanding
underwriting issues, workflow will transfer the proposal to underwriting. The
proposal status will be changed to Waiting for underwriting.
(cid:129) If there are no outstanding issues, the proposal will be accepted automatically.
The policy/proposal status will be changed to Accepted.
(cid:129) If there are rejection issues, the system declines the proposal automatically. The
proposal status will be changed to Rejected.
Save To save the changes, click Save and the proposal status will be
Back to Data Entry If any data entry error is found, click Back to Data Entry. Workflow
will transfer the proposal to data entry for the data entry user to
modify information. The proposal status will be changed to
Waiting for underwriting.
Outstanding Issues View outstanding issues, including non-underwriting issues and
underwriting issues. You can also handle the non-underwriting
issues here.
Cancel To cancel the operation, click Cancel and the proposal status will be
(cid:129) Verify the Proposal
Underwriting Decision Page
Table 21: Field Description of Underwriting Decision Page
Endorsement code Click Add to add new endorsement code.
Some Endorsement code will be automatically added according to
predefined rules.
Appendix A: Field Descriptions Verification Page 162


Condition code Click Add to add new condition code. Select condition code from
Some condition code will be automatically added according to
predefined rules.
Exclusion code Click Add to add exclusion code. Select exclusion code from the
drop down list and then select benefit type and life assured
The same exclusion code can apply to one specific benefit or to all
the benefits under the policy.
Underwriting Enter the underwriting comments if any.
Comment
Pending Reason Double-click this field to select a pending reason if you want to
suspend the case.
Manual Escalation Indicate whether to send the proposal to senior underwriting.
Underwriting Escalate Underwriter to whom the proposal will be sent. This field is
To mandatory if Manual Escalation Indicator is Y.
Consent Given Indicate whether the client's consent has been received or not.
Generate LCA Indicate whether to generate Letter of Conditional Acceptance.
Update LCA Date Indicate whether to update the LCA date as per the date when
Indicator underwriter clicks Submit.
If Generate LCA Indicator is Y, the Update LCA Indicator must be
Y.
Special Comm Indicate whether there is a special commission.
(cid:129) Update UW Information
Appendix A: Field Descriptions Underwriting Decision Page 163


Make Decision on Benefit Page
Table 22: Field Description of Make Decision on Benefit Page
Underwriting Decision Double-click this field to select a decision from the displayed page:
(cid:129) 1: Accepted (only for New Business)
(cid:129) 2: Conditionally Accepted
(cid:129) 3: Postponed
(cid:129) 4: Declined
(cid:129) 5: Accepted with Standard Terms (only used for Customer Service
Underwriting). It means accepting the policy without any extra conditions.
(cid:129) 6: Accepted with Original Terms (only used for Customer Service
Underwriting). It means follow the previous decision.
(cid:129) 9: CS Rejection (only used for Customer Service Underwriting)
Auto-renewal Indicator The Auto-renewal Indicator is defaulted according to product setup.
If the product is the renewable product, the default value of
Auto-renewal Indicatoris Y; otherwise, it is set to N.
You can change the indicator to N if you don't want to grant auto
renewal for this proposal.
You cannot change the indicator to Y if product is not a renewable
Current Underwriter User name of the current underwriter.
Previous Underwriter User name of the previous underwriter if any.
Indexation Indicator (cid:129) For the non-indexation product, the indexation indicator is W and cannot be
changed to Y or N.
(cid:129) For the indexation product, the indexation indicator cannot be changed from N
to Y or from N/Y to W.
(cid:129) For the indexation product, if you change the indexation indicator from Y to N,
system will update the information entered in data entry with this value and
record the indexation suspend cause 6-Stop by UW Permanently.
Extra Loading Extra premium that the client may be required to pay when
underwriting decision is Accepted or Conditionally
Accepted, including health, occupation, residential, aviation,
avocation, and others.
This button is available when Underwriting Decision is set to
Accepted or Conditionally Accepted.
Lien This button is available when Underwriting Decision is set to
Preferred Life Indicator cannot be Y if Lien is applied.
Appendix A: Field Descriptions Make Decision on Benefit Page 164


Restrict Cover The coverage details can be adjusted if the original terms of the
proposal cannot be accepted.
This button is available when Underwriting Decision is set to
Apply Fac Submit request for facultative arrangement.
(cid:129) Make Benefit Decision
Extra Loading Page
Table 23: Field Description of Extra Loading Page
Loading Option Select loading options, including Health Loading, Occupation
Loading, Avocation Loading, Residential Loading, Aviation
Loading, and Other Loading. The dynamic fields specified in the
respective loading worksheet will be displayed below for user to
enter the related information.
Preferred Life Indicator cannot be Y if Health Loading is applied.
Loading Type Select form the list:
1 $ per 1000 sum assured
2 Rating by Age
3 Times of Annual Premium
4 Time of Insurance Charge
5 Manual Extra Premium
6 % EM or amount per 1000 SA
Different fields will be displayed according to different loading type
selected.
If it is health loading, only loading types which are allowed by the
product will be listed.
If it is other loading, all loading types will be displayed, but option 4-
Times of Insurance Charge is restricted for investment product with
insurance charge.
Duration Duration where the loading will be applied. Default as the premium
payment period of the benefit and cannot exceed the premium term
of benefit.
Appendix A: Field Descriptions Extra Loading Page 165


EM Value Extra Mortality value.
If loading type is selected as option 1, EM Value should not be 0 if
Amount is not manually entered.
If loading type is selected as option 6, EM Value should not be 0.
Amount Amount here is referring to the Extra Mortality Rate which can be
manually entered or automatically calculated after click Calculate
EM Rate if loading type is selected as option 1.
User can overwrite the value calculated by the system.
Times (Annual Displayed when loading type is selected as option 3 and 4.
Premium) Manually entered
Age Rated(year) Displayed when loading type is selected as option 2.
Manually entered
Life Extra Mortality Life extra mortality.
TPD Extra Morbidity Extra morbidity caused by third-party damage.
Dread Disease Extra Extra morbidity caused by dread disease.
Morbidity
Extra Premium Automatically calculated after click Calculate Extra Premium
Amount Amount. But if loading type is selected as option 5, then the extra
premium amount should be entered manually.
Reason Displayed if Other Loading is selected.
Free text.
Add Layer Two layers are applicable to Health Loading only. You can click Add
Layer to add layer 2.
Delete Layer You can click Delete Layer to delete an existing layer for Health
Loading.
Total Extra Premium Sum of all extra premium amounts of all types of loading applied.
Amount
Appendix A: Field Descriptions Extra Loading Page 166


Submit After mandatory information is entered, click Submit. The system
performs validation checks as follows:
(cid:129) For manual premium case (Premium Calculation method is manual premium),
if the loading type is Rated up by age, an error message Loading Type
Disallowed for Manually Quoted Premium cases will be
(cid:129) If the calculation is using EM Value and EM rate is not defined in the EM rate
table for the input EM value, error message Can鈥檛 find Rate will be
(cid:129) For unit-linked product, user should not enter the extra premium amount.
Otherwise, an error message Cannot input extra premium for
unit-linked product will be displayed.
(cid:129) If the loading type is option 2- Rating by Age and the premium rate is not defined
for the Entry Age + Age Rated entered, error message Can鈥檛 find Rate will
be displayed.
If all the checks are passed, the system will calculate and update the
related information.
Calculate Extra Click this button to calculate the extra premium amount.
Premium Amount If EM Value entered is more than 200, a message Do you want
to decline TPD will displayed and user must click OK to
continue.
Calculate EM Rate Click Calculate EM Rate, and the system will derive EM rate from
the EM rate table based on the input EM value.
(cid:129) Extra Loading Page
NOTE: Some fields, like EV Value, Times (Annual Premium) and Age Rated (year), are only visible
when specific loading type is selected.
Lien Information Page
Table 24: Field Description of Lien Information Page
Lien Type Double-click this field to select a lien type from the page displayed.
(cid:129) 1: Non-accidental death or TPD
(cid:129) 2: All death or TPD
EM Value Enter the Extra Mortality value.
Appendix A: Field Descriptions Lien Information Page 167


Lien Percentage/Factor (cid:129) Lien Percentage/Factor will be automatically displayed after EM value is entered.
System will check against product to determine which type of lien table to be
used. If the factor or percentage cannot be found, a message Lien
factor/percentage not available. Please enter the lien
factor/percentage will be displayed. User can modify the lien factor or
percentage displayed by the system.
(cid:129) For single premium, the factor input format must be 9.999 (three decimals).
Otherwise, an error message Invalid Lien Percentage / Factor
entered will be displayed.
(cid:129) For regular premium, the lien percentage must be an integer ranging from 1 to
100. Otherwise, an error message Invalid Lien Percentage /
Factor will be displayed.
Lien Term The lien term must be shorter than the premium payment term of
plan/benefit imposed and longer than zero. Otherwise, an error
message Invalid lien year value will be displayed.
For regular premium plan, Lien Term will be defaulted as premium
payment term minus 1.
Total Lien Amount The system will calculate and display the total lien amount after the
lien percentage/factor is entered.
Submit When all mandatory information is entered, click Submit. The
system proceeds as follows:
(cid:129) The system calculates the Reduced Sum Assured (RSA) values for lien 1 or 2.
Lien 1 or 2 is applicable to a main benefit which has no RSA values and excludes
joint-life policies.
Delete To delete the current lien information.
(cid:129) Lien Page
Restrict Cover Page
Table 25: Field Description of Restrict Cover Page
Coverage Term Type Double-click this field to select a coverage term type.
Coverage Term Enter the reduced coverage term.
Premium Term Type Double-click this field to select a premium term type.
Appendix A: Field Descriptions Restrict Cover Page 168


Premium Payment Enter the reduced premium payment term.
Term
Reduced SA/Unit Enter the reduced sum assured/unit, which cannot exceed the
original SA/unit.
Benefit Level Enter reduced benefit level, for example: 4 to 3.
Submit After adjusting the coverage information, click Submit. The system
performs the following checks:
(cid:129) If the coverage term type is changed, the system checks whether the coverage
term is also changed. If not, an error message Coverage Term Not
Changed will be displayed.
(cid:129) The system validates the coverage term type against product setup. If failed, an
error message Invalid Coverage term type will be displayed.
(cid:129) If the premium payment type is changed, the system checks whether the
premium payment term is also changed. If not, an error message Premium
Payment Term Not Changed will be displayed.
(cid:129) The system validates the premium payment type against product setup. If failed,
an error message Invalid Coverage term type will be displayed.
If all the checks are passed, the system updates the submitted
information and automatically generates different condition codes if
different information is updated for any benefits:
(cid:129) Change in sum assured, MA or MS factor: 0006
(cid:129) Change in coverage term or premium payment term: 0007
Delete Delete the existing restrict coverage information.
Clear Clear the entered restrict coverage information.
Cancel Cancel operation.
(cid:129) Restrict Cover Page
Update Policy Acknowledgement Page
Table 26: Field Description of Update Policy Acknowledgement Page
Dispatch Date Date when policy is dispatched. Format: DD/MM/YYYY
Appendix A: Field Descriptions Update Policy Acknowledgement Page 169


Dispatch Type In which way the policy is dispatch.
(cid:129) H: Hand
(cid:129) M: Mail
Service Branch Receive Date when the service branch receives the policy documents.
Date Format: DD/MM/YYYY
Agent Collection Date Date when the agent receives the policy documents. Format:
Reasons for Returning Reason why the policy documents are returned. Select from the
Print Policy Document drop-down list.
Acknowledgement Date when the client assigns the acknowledgement letter.
Date
Undelivered Indicator Indicate whether the policy documents are delivered to client or not.
Select from the drop-down list.
Reason for Reason why the policy documents are not delivered to client.
Non-Delivery of Policy
Non-Delivery Period during which the delivery failed.
Exclusion Start Date,
Non-Delivery
Exclusion End Date
(cid:129) Update Acknowledgement Details
Fields on Withdraw New Business Page
Table 27: Field Description of Withdraw New Business Page
Collect Medical Fee Indicate which party pays the medical fees. Select an option from
Option the drop-down list. Options are:
(cid:129) By Policy Holder
(cid:129) By Agent
(cid:129) By Company
Medical Fees Amount of medical fees. The field is mandatory if Policyholder
Pays Medical Fee Indicator is set to Yes.
Appendix A: Field Descriptions Fields on Withdraw New Business Page 170


Withdrawal Reason Select a reason from the drop-down list.
(cid:129) Withdraw New Business Page
Table 28: Field Description of Items for Medical Billing Area
Clinic Code Clinic code maintained in Party module. You must input the correct
clinic code manually.
Clinic Name Clinic name is automatically displayed by the system when relevant
clinic code is input.
Panel/Non Panel Automatically displayed by the system. Non Panel/Panel Clinic is
predefined in the Party module.
Create Clinic If the clinic does not exist in the system, you can click Create Clinic
to turn to Party Identification page. You can maintain the clinic
information. For details, refer to Maintain Third Parties in the
System Administration User Manual.
Medical Type Medical type is the abbreviation of medical test description that is
predefined in the Party module.
Invoice Number Receipt No. of medical exam
Fee Sum (cid:129) For panel clinic payment, Underwriting panel = Y, the system defaults agreed fee
as fee sum and does not allow any modification.
(cid:129) For non-panel clinic payment, Underwriting panel = N, the system allows you to
input the incurred fee sum. In addition, the system will also check whether the
Medical Type is included in the Clinic Medical Fee list. Otherwise, error
message will be displayed.
You can amend the fee sum as long as the relevant payment is not
paid. After the payment is paid and relevant payment record
generated, you cannot amend the fee sum any more.


Exam Date Exam date of the medical test. Exam date must be earlier than the
delete date of the medical type. Delete date is the date you delete a
medical type.
Disbursement Method Displayed from the drop-down list:
(cid:129) Cheque
(cid:129) Credit Agent's Commission
(cid:129) Debit Agent's Commission
(cid:129) Cash
(cid:129) Bank Transfer
(cid:129) When Disbursement Method = Cheque or Cash or Bank
Transfer and Payable To = Proposer, the user can requisi-tion
payment through Payment Requisition UI and then use
Authorise Payment UI to approve the payment.
(cid:129) When Disbursement Method = Debit/Credit Agent's
Commission, the relevant medical fee record will be generated.
(cid:129) When Disbursement Method = Cheque or Cash or Bank
Transfer and Payable to = Clinic, the system extracts the record
at month end via batch job. For details, refer to Batch Payment in
Payment User Manual.
For ad-hoc cheque requisition for medical fee payment to clinic, the
extraction will be triggered by cheque requisition action and the
total amount payable will be the consolidated amount. The
statement of account for the following month will exclude records
which have been paid under the ad-hoc cheque requisition.
Payable to Displayed from the drop-down list:
(cid:129) When you select disbursement type as Cheque or Cash or Bank Transfer,
you must select Clinic or Proposer from the Payable to drop-down list.
(cid:129) When disbursement type is Debit Agent's Commission or Credit
Agent's Commission, the system will display Agent automatically.
(cid:129) Update Medical Billing
NOTE: Create Clinic button is only visible after Add is clicked in the Items for Medical Billing area.
Appendix A: Field Descriptions Items for Medical Billing Area 172



---

# Appendix B: Rules

Appendix B: Rules
Register Initial Information Rules
This topic tells the rules in initial registration.
When you enter an agent code in the Agent Code filed on the Register Initial Information page:
(cid:129) Only the agent which has qualification on policy proposal date can issue policy.
(cid:129) If the entered proposal date is not between the agent sales qualification effective date and
expiry date, the system prompts alert: Service Agent has no permission to
sell this product.
(cid:129) If the agent does not have the qualification to sell this product, the system prompts alert:
Service Agent has no permission to sell this product.
(cid:129) For more details, refer to Maintain Producer Qualification in Sales Channel User Guide.
This topic tells the rules in data entry.
(cid:129) When you enter the search criteria to search out a target record in work list:
鈥?The search criterion Task Status has two options: Claimed and Ready.
Claimed A user has already started to process the task,
and the task cannot be accessed by other
users.
Ready The task is still to be claimed, but it does not
necessarily mean that it can be accessed by
any authorized users, because it is still
possible that a ready case has already been
assigned to certain users.
Appendix B: Rules Register Initial Information Rules 173


鈥?The search criterion Letter to be replied has two options: Yes and No. By default, No is
selected and thus the system only displays the tasks without outstanding letters.
The letters include: NB query letter, Medical check letter, CS query letter, and Claim
query letter.
When a letter is registered or scanned in Initial Registration, the status of the letter
will be changed to Replied. You can also reply the letter on the page where the letter
is generated.
If any of the above letters are not replied, the task cannot be submitted.
(cid:129) When you maintain the life assured information, please note that:
鈥?A proposal can have more than one life assured attached, which is defined by product.
If the product definition allows single life only, only one life assured record can be
added; otherwise, an error message 鈥淛oint Life or Multiple Lives not allowed鈥?will be
displayed when you click Add.
鈥?For a policy with insured category as Family Type, the number of life assured records
will not be checked.
鈥?For the joint-life policy, two different life assured records must be added; otherwise, an
error message: The 2 LA's records are the same. will be displayed if two
identical life assured records are created, or an error message: Please enter the
2nd Life Assured details. will be displayed if the details of the second life
assured are not entered.
(cid:129) When you click Save on the Benefit Information page:
The system will check the benefit information based on the product definition. For example:
payment method and Initial Premium Frequency should be aligned with the product
configuration Total Installment Premium Limit Table (refer to eBaoTech LifeSystem Product
Definition Guide LS 3.1.2.9), cover term, premium term, policyholder鈥檚 entry age, etc.
(cid:129) When you add a fund in the benefit information page for investment product, please note that
fund status must not be closed.
(cid:129) The system validates the combination of benefits, including Main versus Rider and Rider
versus Rider.
(cid:129) When you want to add beneficiary information, please note that the Trust Policy Indicator
in the Basic Information area must be Y; besides, the total percentage of all beneficiaries must
be 100%.
(cid:129) When you create more than one commission agent, the total percentage of all commission
agents must be 100%.
Appendix B: Rules New Business Data Entry Rules 174


The following table illustrates the types of insurance roles that may exist in a policy and the
corresponding payer/payee.
Existing NB Insurance Roles in a policy Payer/Payee
Payee(f
or
Payer(fo refund
r of
Policyh Premiu Life Benefici collecti premiu
older m Payer Assured ary Trustee Grantee on) m)
鈭?鈭?鈭?Premiu Policyho
鈭?鈭?鈭?鈭?Premiu Policyho
鈭?鈭?鈭?鈭?Premiu Policyho
鈭?鈭?鈭?鈭?鈭?Premiu Policyho
鈭?鈭?鈭?鈭?鈭?Premiu Policyho
鈭?鈭?鈭?鈭?鈭?鈭?Premiu Policyho
Appendix B: Rules Payer/Payee Rules for New Business 175


NOTE: For bankruptcy cases, if the bankruptcy status is Yes, the Disbursement Payee (on Payment
Requisition page) is set to Official Assignee by default, but finance user can change it.
New Business Underwriting Rules
This topic tells the rules in underwriting.
Risk aggregation is quite important for proposal, which will
be processed by the system automatically.
(cid:129) The aggregated risk per life will include the risk in the current proposal and any of the existing
valid policies, concurrent proposals (pending proposals) which has the life (for whom the risk
is aggregated) as either the proposer (if required) or the life assured.
(cid:129) Risk is aggregated based on aggregation risk type defined by the benefit and aggregation
formula accordingly. Currently the following aggregation risk types are predefined:
鈥?Death
鈥?Accidental Death
鈥?Accidental Death & Disability
鈥?DD Accelerated
Appendix B: Rules New Business Underwriting Rules 176


鈥?DD Additional
鈥?Hospital Cash
鈥?Hospitalization
鈥?TPD Accelerated
鈥?TPD Additional
鈥?Waive
(cid:129) The risk aggregation will be triggered under any of the following conditions:
鈥?Risk aggregation is triggered for the first time after the case has gone through
Underwriting Process Control (UPC). Subsequently, the risk aggregation can be
triggered when underwriter manually triggers the risk aggregation in the underwriting
UI.
鈥?Risk aggregation is to be triggered prior to routing the case back to the underwriting
work list.
鈥?For the CS application type, risk aggregation is to be triggered prior to routing the case
to the underwriting work list.
(cid:129) The procedure for risk aggregation is as follows:
a) The system retrieves the information on the current proposal, including the life assured,
proposer information, and the proposal details.
NOTE: The proposal details retrieved for risk aggregation include proposal
number/policy number, benefit number, product code, rider type, sum assured, annual
benefit, benefit term, form type, proposed life, joint life, and policy owner.
b) The system retrieves the party details for the life assured and proposer.
c) The system determines the risk for the life assured on the current proposal by
calculating the following: 1. Aggregated risk sum assured on the current proposal for the
life assured; 2. Per Life Limit on the current proposal for the life assured.
d) The system retrieves the in-force policies for the life assured.
e) The system determines the risk on the existing policies for the life assured by calculating
the following: 1. Aggregated risk sum assured on the existing policies for the life assured.
2. Per Life Limit on the existing policies for the life assured. 3. Total annual premium on
the existing policies for the life assured.
f) The system checks whether the current proposal is single life. If the proposal is not
single life, proceed to step g to determine the risk on the proposer; if it is single life,
proceed to step j.
g) The system determines the risk for the proposer on the current proposal by calculating
the following: 1. Aggregated risk sum assured on the current proposal for the life
assured. 2. Per Life Limit on the current proposal for the life assured.
h) The system retrieves the in-force policies for the proposer.
i) The system determines the risk for the proposer on the existing policies by calculating
the following: 1. Aggregated risk sum assured on the existing policies for the life assured.
2. Per Life Limit on the existing policies for the life assured.
Appendix B: Rules New Business Underwriting Rules 177


j) The system saves the aggregated risk information and the per life limit details as
determined in the above steps.
Issue status instructions:
Closed means that the issue has been handled. Ignored means that the underwriter does not think
the issue will bring impact to the policy. Both options will close outstanding issues.
When you can add non-standard endorsement, condition,
and exclusion,
(cid:129) The exclusions and endorsements will be printed on the policy documents.
(cid:129) A policy can have multiple endorsements, conditions, and exclusions.
If there are unclosed outstanding issues in underwriting,
A warning message will be displayed when you click Make Benefit Decision.
When you make underwriting decisions on benefits:
(cid:129) The system supports batch processing of the Accepted, Declined or Postponed benefits. If
you want to accept, decline or postpone all benefits, in the Underwriting Decision area of the
Underwriting Main Screen, select all benefits and click Make Benefit Decision. Then set
Underwriting Decision field to Accepted, Declined or Postponed. The decline or postpone
reason will only be captured on the first benefit. However, if you want to conditionally accept
all benefits, you must process them one by one.
(cid:129) When you need to update the existing underwriting decisions for all benefits to the same one,
if the existing underwriting decisions are different, you cannot select all of them to update
them simultaneously. Instead, you must update them one by one.
(cid:129) If the benefit underwriting decision is Accepted with exclusion, system will update the benefit
underwriting decision to Conditionally Accepted without any Extra Loading, Lien or Restrict
Cover.
When you click Submit on the Make Decision on Benefit
page, the system proceeds as follows:
(cid:129) The system recalculates the premium as the underwriter may have changed the following
information: Preferred Life Indicator, Smoker Indicator, Occupation Class, Accident Class,
and Occupation. The system updates the total enforcing premium amount required when the
recalculation is performed for any change of data which affects the premium. For the declined
or postponed benefits, the system will not recalculate premium, but generate declined or
postpone letters.
Appendix B: Rules New Business Underwriting Rules 178


(cid:129) The system performs validation checks.
If the Preferred Life Indicator is Y but the product parameter defined does not allow this
setting, an error message Preferred Life is Not allowed for <benefit
name>. will be displayed.
If the Preferred Life Indicator is Y and the product parameter defined allows this setting, the
system validates that the Smoker Indicator is not Y and the Underwriting Decision is
Accepted. If not, an error message Invalid indicator. Life Assured must be
non-smoker for preferred life product. will be displayed.
If Smoker Indicator is updated to N and Preferred Life Indicator is updated to Y, a warning
message Please change preferred life indicator to N. will be displayed.
If underwriter uses Restrict Cover to change coverage information, the system checks
whether loading or lien has been imposed. If yes, a warning Loading /Lien
information found. Extra premium will be re-computed. will be
displayed. Click Continue. The system will re-calculate the extra premium or lien based on the
reduced coverage.
(cid:129) The system updates the underwriting decisions.
For New Business, if Underwriting Decision is Conditionally Accepted at policy level, the
system does not display this underwriting decision to all the benefits as the underwriter can
impose different underwriting terms for each benefit.
For New Business, if Underwriting Decision is Accepted at policy level, the system displays
this underwriting decision to all the benefits attached to the main benefit upon the
underwriter completes the decision update.
For New Business, if Underwriting Decision is Declined or Postponed at policy level, the
system displays the underwriting decision to all the benefits attached to the main benefit. The
decline or postpone reason will only be captured once under the main benefit.
For Customer Service, the underwriting decision is made at benefit level.
(cid:129) The system updates the underwriting status to Underwriting Completed.
When you click Submit on the Underwriting Main Screen
page, the system proceeds as follows:
(cid:129) The system checks whether the underwriting status of all products is Underwriting
Completed and all letters have been returned and settled. If not, an error message Not all
products have been underwritten or not all letters have been
settled will be displayed.
(cid:129) If user amends the original Standard Life Indicator from N to Y, the system will delete the
substandard record but keep the information in underwriting history for enquiry purpose.
(cid:129) If Generate LCA Indicator is Y, the system will generate LCA, and set LCA Issue Date to the
current system date and set Health Warranty Expiry Date to LCA Issue Date + Validity Period.
For Annuity product and Jet Issuance product, no Health Warranty Expiry Date is required
and the system set Health Warranty Expiry Date to Null. However, the job schedule for LCA
expiration still applies.
Appendix B: Rules New Business Underwriting Rules 179


(cid:129) If Generate LCA Indicator is Y, the Update LCA Date Indicator must be Y. Otherwise, an
error message Update LCA Date IND Must be Y for re-generating LCA.
will be displayed.
(cid:129) If Update LCA Date Indicator is Y, the system will update the LCA Date as per the date when
underwriter clicks Submit. The Health Warranty Expiry Date will be reset for one month
validity again.
(cid:129) If Consent Given Indicator is Y, the system will regard the consent as having been received
and will not require further submission of consent from client.
(cid:129) For proposals which use maturity proceeds, no Health Warranty Expiry Date is required.
The system checks whether the proposal or policy鈥檚
underwriting limit is within the user鈥檚 underwriting
authority.
NOTE: Underwriting limit for proposal or policy refers to accumulated accidental or non-accidental
death and TPD sum assured of the products, disability benefit per month if any, product level if level
driven, medical status and extra mortality loaded if ever underwritten. Underwriting limit for a
proposal or policy is to be set based on the highest underwriting limit among all products under the
proposal or policy.
(cid:129) If yes, the system proceeds as follows:
For the accepted proposal, the system recalculates the total inforce premium amount,
standard premium/extra premium with the updated data, underwriting decision will be
applied immediately upon submission and the proposal will be transferred to enforcing
proposal workflow. For details, refer to Inforce.
For the conditionally accepted proposal, the system will generate LCA upon acceptance
(Generate LCA Indicator = Y) or conditionally acceptance. When the LCA is received and
confirmed, the consent information must be updated. For details, refer to Update Consent for
LCA.
For the declined or postponed proposal, the system will generate Decline or Postpone letter
and refund premium for payment.
(cid:129) If no, the system escalates this proposal to senior underwriters. The proposal status remains
Underwriting in Progress and the underwriting status will be changed to Escalated. The
Pending Reason will be updated to Escalated to next level. For details, refer to Escalate Under-
writing.
Escalate Underwriting Rules
This topic tells the rules in underwriting escalation.
When you click Submit:
Appendix B: Rules Escalate Underwriting Rules 180


(cid:129) If you do not have the authority to underwrite this proposal, the system escalates this proposal
to senior underwriters for underwriting. The proposal status will be change to Waiting for
Underwriting, the Pending Reason will be updated to Escalated to next level, and the
underwriting status will be changed to Escalated.
(cid:129) If the Manual Escalate Indicator is Y, you need to double-click the Underwriter Escalate To
field and select an underwriter from the displayed page. The system will escalate this proposal
to the specified senior underwriter for underwriting. The underwriting status will be changed
to Underwriting in progress. If the proposal or policy鈥檚 underwriting limit is beyond the
specified underwriter鈥檚 authority, an error message Underwriter's Authority
Limit Below Required underwriting level. Manual Escalation Not
allowed will be displayed when submitted. You can change Manual Escalate Indicator to
N or select another underwriter.
(cid:129) If you have the authority to underwrite this proposal, the system updates the underwriting
decision according to the decision you have made. The proposal can either be declined or
postponed, or it can be underwritten and then be sent for enforcement. For details about
proposal enforcement, refer to Inforce.
New Business Enforce Policy Rules
This topic tells the rules in inforce process.
When system checks the auto-inforcing criteria, the
following items should be noticed:
(cid:129) About health warranty expiry date: if the policy is not annuity policy or the product is not jet
issue, the system will validate that the Health Warranty Expiry Date is later than the current
system date. If Health Warranty Expiry Date is earlier than or equal to the current system date,
Health Warranty has expired, and a warning message Health Warranty is required will be
displayed on the update consent/health warranty UI, Cashiering UI, or waive overdue interest
UI for those policies which have completed underwriting. The policy cannot turn inforce
unless the Health Warranty Date is extended.
(cid:129) About Consent Given Indicator: For conditionally accepted cases, the system will validate that
Consent Given Indicator must be Y and Consent Given Date must be equal to or earlier than
Health Warranty Expiry Date. If not, a warning message Consent form is Required
will be displayed after underwriting is submitted.
(cid:129) About premium payment:
鈥?When payment method = cash/cheque/credit card/SSS/deferred benefit account:
(cid:129)If suspense premium - total enforcing premium 鈮?0, the system regards the premium as fully
paid and the case is deemed to have passed validation.
Appendix B: Rules New Business Enforce Policy Rules 181


(cid:129)If $1 > total enforcing premium - suspense premium > 0, the system regards the premium as
fully paid and the case is deemed to have passed validation. The system will insert a short
payment record as Company is waiving it. 鈥?1鈥?is set in the tolerance rate table.
(cid:129)If $25 鈮?total enforcing premium - suspense premium 鈮?$1 and proposal is not placed under
Company direct account, the system regards the premium as fully paid and the case is deemed
to have passed validation. The system will insert a fee record as debiting the shortfall amount
to agent commission account. 鈥?25鈥?and 鈥?鈥?are set in the tolerance rate table.
(cid:129)If validation fails and the case is triggered manually, a warning message short payment will be
(cid:129)If it is a foreign currency product, the foreign currency amount equivalent to 25 units or less
than 1 unit of the local currency should be used.
鈥?Rules on waiver of short payment of $25:
(cid:129)When the enforcing amount is less than $25, do not debit agent account. When the enforcing
amount is greater than $25 but the difference between the enforcing amount and the debit
agent account amount is less than $25, the debit agent account amount is set to the lower
amount, that is, the difference between the enforcing amount and the debit agent account
amount. Otherwise the debit agent account amount is set to $25.
When system updates the commencement date:
(cid:129) For backdating cases, the commencement date is as per user input.
(cid:129) For non-backdating cases, the commencement date is determined as follows:
鈥?For standard LCA with health warranty not expired, commencement date is the later
date between LCA date and effective date of full payment date.
鈥?For standard LCA with health warranty expired, commencement date is the latest date
among LCA date, effective date of full payment, and health warranty extended date.
鈥?For substandard LCA, commencement date is the latest date among consent given date,
effective date of full payment, and health warranty extended date.
When system recalculates the age of the life assured:
(cid:129) Age could be increased or decreased when there is any changed in commencement date.
(cid:129) Age will be increased when current age 鈥?original age > 0. The calculation of original age and
current age of life assured is as follows:
鈥?If LCA is not generated, original age is based on the proposal date and DOB of life
assured; current age is based on current commencement date and DOB of life assured.
Appendix B: Rules New Business Enforce Policy Rules 182


鈥?If LCA is generated, original age is based on underwriting complete date and DOB of
life assured; current age is based on current commencement date and DOB of life
assured.
When system calculates the proposal premium:
(cid:129) The sequence of premium calculation is as follows:
a) Gross amount (calculated by premium calculation of the benefit, including policy fee
and discounts like Large SA discount, No Smoking discount, etc.)
b) Discount for staff /staff family/agent/etc.
c) Total installment amount calculation.
d) Taxation calculation such as Service Tax, GST, Stamp Duty, etc.
e) Overdue interest.
f) Add Misc. fees.
(cid:129) Total in-forcing premium = 鈭?Total Amount to be Paid for one Policy of One Premium Due
* premium due times + total amount need to be paid for one policy of one premium due *
premium due times in arrears + overdue interest if any + miscellaneous fee if any + Tax if any).
(cid:129) Total amount need to be paid for one policy of one premium due = Gross premium of policy
without tax + 鈭?extra premium if premium due date is within the extra premium term + Tax
if any.
(cid:129) Gross premium of policy without tax = 鈭?total premium of benefit + 鈭?extra premium if
premium due date is within the extra premium term.
NOTE: System will sum up the premium for benefit with underwriting decision other than
declined and postponed and the benefit which is rider and is not paid by unit deduction.
(cid:129) For monthly payment which payment method is not under SSS, premium due times will be set
as 2 or 1 according to the configuration (system level parameter).
(cid:129) Premium due times in arrears = number of premiums payable between commencement date
and next due date according to the payment frequency - Premium due times. Where the
following conditions must be satisfied: Next due date > Issue date + 49 days.
(cid:129) Overdue interest if any: If the case is backdated for more than 183 days, overdue interest is
payable and system will calculate the amount to be payable as part of the enforcing amount.
This computed overdue interest is waived when 95% of the payable amount has been received
within 6 months of the backdated start date.
(cid:129) Miscellaneous fee if any: Miscellaneous fee can be updated by user in data entry UI or
amendment UI.
(cid:129) System will check for any change of the effective rate of taxes based on the effective date and
revise the new total enforcing amount before turning the proposal in force.
(cid:129) For benefit which is using premium for calculating the sum assured, system will re-calculate
the sum assured for the corresponding age if there is any change in age.
(cid:129) For proposal with manual premium indicator, only the standard premium rate does not need
to be calculated automatically as the amount is manually input by user.
Appendix B: Rules New Business Enforce Policy Rules 183


(cid:129) Calculate RSA Table: For benefit with Reducing Sum Assured (RSA), the system will calculate
the RSA table for the RSA terms. For manual premium case, system will not recalculate the
RSA but refer to the user input during data entry processing.
(cid:129) Commission entry: the system will generate agent commission entitlement for each benefit
attached in the policy. For any re-inforce policy, the system will generate new entry for
commission as the system has reversed commission entry previously created when the policy
status changed from inforce to non-inforce.
(cid:129) Reinsurance premium: The system will calculate the reinsurance premium amount based on
formula defined in Reinsurance module.
The proposal information the system updates includes:
(cid:129) Dates to be updated at benefit level and policy level:
鈥?Commencement date: based on calculation result
鈥?Risk commencement date: based on calculation result
鈥?Product Cover End date: commencement date + coverage period
鈥?Premium end date
鈥?Age of life assured for increased age proposal
鈥?Next due date: Commencement date + payment frequency* (premium due times +
premium due time in arrears), the payment frequency is by month.
(cid:129) Premiums to be updated:
鈥?Total in-forcing premium (policy level)
鈥?Standard premium (benefit level)
鈥?Extra premium (benefit level)
鈥?Total installment premium (benefit level)
鈥?Total installment premium (policy level)
(cid:129) Indexation information
鈥?The system saves the indexation information
鈥?For the product with indexation, the system creates a contract segment to record
indexation detailed information.
鈥?For the waiver product, if the waived product has indexation indicator, the system also
creates a contract segment.
(cid:129) The system updates the policy and benefit status to In-force and policy printing status to
Waiting for Printing.
(cid:129) The system updates the insurance role for Proposer to Policyholder.
(cid:129) If vesting endorsement codes 10 or 60 are attached, when policy turns in force, system will
create a vesting schedule. The initial setting includes:
鈥?Vesting Age, determined by Endorsement Code. The default value is 21.
Appendix B: Rules New Business Enforce Policy Rules 184


鈥?Vesting Status, upon inception, the system will set the status to waiting for effective. The
other two statuses are effective and cancel.
鈥?Vesting Date, which is equal to main benefit's life assured DOB plus vesting age.
When the system generates fund transaction application for
investment product:
(cid:129) Premium Allocation will check 鈥業nvestment Delay Option鈥?
a) If 鈥業nvestment Delay Option鈥?is 鈥楴o Delay鈥? then all premiums received, including target
premium (inforcing and renewal), Adhoc Top ups and Recurring Top Ups, will be
invested into target funds directly.
b) If 鈥業nvestment Delay Option鈥?is 鈥楴o investment during delay period鈥?and customer select
鈥楧irect鈥?in New Business, then all premiums received, including target premium
(inforcing and renewal), Adhoc Top ups and Recurring Top Ups, will be invested into
target funds directly.
c) If 鈥業nvestment Delay Option鈥?is 鈥楴o investment during delay period鈥?and customer select
鈥業ndirect鈥?in New Business, then all premiums received, including target premium
(inforcing and renewal), Adhoc Top ups and Recurring Top Ups, will not generate any
investment apply during delay period (collection date <= issue date +investment delay
days) and they will be invested into target funds after delay period (system date >issue
date +investment delay days).
d) If 鈥業nvestment Delay Option鈥?is 鈥業nvest to other funds during delay period鈥? then all
premiums received, including target premium (inforcing and renewal), Adhoc Top ups
and Recurring Top Ups, will be invested into mapping funds defined accordingly
during investment delay period (collection date <= issue date +investment delay days)
and they will be invested automatically into target funds after delay period (system date
>issue date +investment delay days).
(cid:129) 鈥業nvestment Delay Option鈥?and 鈥業nvestment Delay Days鈥?will be defined by product definition
(details refer to LifeSystem Product Definition Guide).
(cid:129) Mapping funds (normally money market fund) will be defined in table and can be different
according to different Product or Fund Currency or Target Funds (details refer to LifeSystem
Product Definition Guide).
(cid:129) There can be multiple mapping funds inside one policy. In this case, premiums will be invested
into both mapping funds according to fund apportionment of target funds.
(cid:129) If close fund is chosen, system will generate the pending transaction of the corresponding
money market fund. If the same money fund is selected for investment as well, system will
record the amount for purchase separately.
The system updates and inserts fee records.
(cid:129) Application of suspense to premium income
Appendix B: Rules New Business Enforce Policy Rules 185


鈥?Any premium amount received before policy turns inforce will be put into General
Suspense account. When the case turns in force, system will apply the premium from
the General Suspense account to premium income account. This includes arrears of
premium for backdated policies. For different fees will generate different fee records
respectively according to different fee types.
鈥?If the Advance Premium indicator is Y, system will automatically move any excess
payment to Advance Premium Account (APA) after using amount required to enforce
policy. Otherwise, system to automatically move any excess premium to general
suspense account for refund purpose.
鈥?For investment linked plans, details of the unallocated amount (while pending for fund
transaction) will be available for query. After the fund transaction, the information on
premium allocated, balance of units after the charges (Expense Fee, etc) will be available
for viewing.
(cid:129) Update and insert fee records, including premium income, overdue interest, service tax, GST,
miscellaneous fees, Debit agent commission, medical fees, stamp duty, HI policy fees, and
expenses.
(cid:129) Insert short payment records.
鈥?When payment method is cash/cheque/credit card, if $1 > in-forcing premium -
suspense premium > $0, system to insert short payment record as Company is waiving
it.
鈥?When payment method is cash/cheque/credit card, if $25 鈮?enforcing premium -
suspense premium 鈮?$1 and this proposal is not placed under Company direct
account, then system auto insert fee record as debiting the shortfall amount to agent
commission account.
When system checks if there is any premium to refund:
(cid:129) System checks whether the excess premium is being retained. If yes, no refund will be
triggered.
(cid:129) Unless otherwise specified by proposer, refund of premium paid using credit card will be
refunded to Proposer via cash/cheque.
(cid:129) Any excess premium less than $10 for monthly payment frequency plan will be used for
Renewal Premium.
(cid:129) For regular premium plan where payment frequency = monthly, if the excess premium is
sufficient to cover the next renewal premium, excess premium will not be refunded and policy
renewal will be triggered.
(cid:129) For single premium plan, the excess premium will be automatically refunded to the
policyholder.
Inforce a Proposal
Appendix B: Rules New Business Enforce Policy Rules 186


This topic tells the rules for dispatching policies.
(cid:129) When you search out policies, only the issued policies whose dispatch date is not entered can
be searched out.
(cid:129) When you click Submit on the Update Policy Acknowledgement page, the system performs
the following validation checks. If any check fails, the corresponding error message will be
鈥?The Dispatch Date must meet the following rules: policy issue date 鈮?dispatch date 鈮?
鈥?The Service Branch Receive Date must meet the following rules: dispatch date 鈮?service
branch receive date 鈮?current system date; service branch receive date 鈮?policy issue
date.
鈥?The DC Rep Collection Date must meet the following rules: dispatch date 鈮?DC Rep
Collection Date 鈮?current system date; DC Rep Collection Date 鈮?policy issue date.
鈥?If the Undelivered Indicator is Y, the Reasons for Returning Policy Document or the
Reason for Non-Delivery of Policy must be selected. If the Reasons for Returning
Policy Document or the Reason for Non-Delivery of Policy is selected, the
Undelivered Indicator must be Y.
鈥?If the Reason for Non-Delivery of Policy is selected, the Non-Delivery Exclusion Start
Date and Non-Delivery Exclusion End Date must be entered. If the Non-Delivery
Exclusion Start Date and Non-Delivery Exclusion End Date are entered, the Reason
for Non-Delivery of Policy must be selected.
鈥?The Non-Delivery Exclusion Start Date cannot be later than the Non-Delivery
Exclusion End Date.
Rules of New Business Withdrawal
This section lists the rules of ad hoc withdrawal and auto withdrawal.
Ad hoc withdrawal rules
When you click Submit, the system proceeds as follows:
Appendix B: Rules New Business Dispatch Policy Rules 187


(cid:129) The system updates the proposal status to Withdrawn and updates the withdrawal reason
according to user input.
(cid:129) The system cancels the waiver of overdue interest and miscellaneous fees if any and updates
the policy transaction history.
(cid:129) The system validates the medial fees.
鈥?If Policyholder Pays Medical Fee Indicator is No and Medical Fees is updated, upon
changing the proposal status to Withdrawn, the system will auto-debit the total
amount of medical fees incurred for the policy from the agent account.
鈥?If Policyholder Pays Medical Fee Indicator is No and Medical Fees is not updated, the
amount to be refunded equals the amount paid by proposer.
鈥?If Policyholder Pays Medical Fee Indicator is Yes, the system checks whether Medical
Fees is null. If it is null, a prompt message Medical Fee is required will be displayed. The
system also checks whether there is money in the suspense account. If not, an error
message Invalid indicator. No money in suspense account will be displayed.
鈥?System will deduct the medical fees from the general suspense account. If the amount
in general suspense account is greater than the medical fees or there are excess amount
after the deduction in the new business suspense account, the system will refund the
excess amount. If the amount in general suspense account is less than the medical fees,
system will deduct the medical fees from the general suspense account and debit agent's
account for the remaining medical fees.
(cid:129) After validating the medical fees, the system checks whether refund is required. A refund is
required when the proposal status is Withdrawn and the General Suspense Balance is
greater than zero.
(cid:129) If a refund is required, the system generates a refund fee record and a withdrawal letter with
the refund. A withdrawal letter will be generated after a withdrawal is successfully performed.
Auto withdrawal rules
When system runs a batch job to withdraw proposals,
(cid:129) If the proposal status is Accepted or Conditionally Accepted, the system will
automatically withdraw the policy when the date of the last LCA issued is more than 60
(configurable by system level parameter) days earlier than the system date.
(cid:129) If the proposal status is Underwriting in Progress or Amendment in Progress,
the system will automatically withdraw the policy when the registration date is more than 90
(configurable by system level parameter) days earlier than the system date or the date of the
last SLQ issued is more than 183 days earlier than the system date, whichever is earlier.
The system sets withdrawal reason as follows:
(cid:129) If proposal status is Accepted or Conditionally Accepted, the system sets the
withdrawal reason to Cancelled by company after acceptance.
(cid:129) If proposal status is not Accepted or Conditionally Accepted, the system sets the
withdrawal reason to Cancelled by company before acceptance.
When the system validates the medial fees,
Appendix B: Rules Rules of New Business Withdrawal 188


(cid:129) If Policyholder Pays Medical Fee Indicator is No and Medical Fees is updated, upon
changing the proposal status to Withdrawn, the system will auto-debit the total amount of
medical fees incurred for the policy from the DC Rep account.
(cid:129) If Policyholder Pays Medical Fee Indicator is No and Medical Fees is not updated, the
amount to be refunded equals the amount paid by proposer.
(cid:129) If Policyholder Pays Medical Fee Indicator is Yes, the system checks whether Medical Fees
is null. If it is null, a prompt message Medical Fee is required will be displayed. The
system also checks whether there is money in the suspense account. If not, an error message
Invalid indicator. No money in suspense account will be displayed.
(cid:129) System will deduct the medical fees from the general suspense account. If the amount in
general suspense account is greater than the medical fees or there are excess amount after the
deduction in the new business suspense account, the system will refund the excess amount. If
the amount in general suspense account is less than the medical fees, system will deduct the
medical fees from the general suspense account and debit agent's account for the remaining
medical fees.
Withdraw a Policy Ad hoc
About Auto Withdrawal
Amend New Business Rules
This section tells the rules of proposal amendment.
(cid:129) The proposal information that can be amended includes: Basic Information, Proposer, Life
Assured, Payment Method, Benefit Name, Beneficiary, Trustee, Commission, and Comment.
(cid:129) After the amended proposal information is submitted,
鈥?When verification and re-underwriting are needed, verify this proposal before
underwriting. For details, refer to Verification.
鈥?When verification is not required yet re-underwriting is required, underwrite this
proposal again. For details, refer to Underwriting.
鈥?When neither verification nor re-underwriting is required, enforce this proposal
directly. For details, refer to Inforce.
Amend New Business
This section tells the rules for cancelling/reversing medical billing records.
(cid:129) The medical billing records that can be searched out must have one of the medical payment
status listed below:
鈥?Pending Payment Requisition
Appendix B: Rules Amend New Business Rules 189


鈥?Pending Approval
鈥?Approved
鈥?Payment Processed
鈥?Payment Confirmed
(cid:129) Rules for medical billing reversal:
鈥?For medical transaction paid via Debit/Credit Agent's Commission, the reversal will
be done immediately.
鈥?For medical payments paid to the proposer directly, the reversal will be done
immediately. You can manually create a letter to inform the proposer.
鈥?For medical transaction paid to the clinic, the reversal will be done at the next available
extract for payment.
鈥?For medical transaction paid via cheque, the system will not process this record within
current month cheque composing. Instead, the cheque of this monthly batch will
remain un-reversed, and when the next month batch is triggered, the reversed medical
records of this month will be added into next cheque amount and monthly statement as
negative records.
Update Consent for LCA Rules
This section tells the rules in update consent.
(cid:129) On the Update Consent for LCA page, the default Consent Given Date is NULL. When you
update the consent given date, follow the rules described below:
鈥?current system date - 7 days 鈮?consent given date 鈮?current system date; LCA date 鈮?
consent given date
(cid:129) When you click Submit:
鈥?Interest will be charged for the policy that is backdated for more than 183 days. The
system will calculate the up-to-date total enforcing amount and display the amount. For
backdated cases, the system will calculate the number of installments required and
update the total enforcing amount.
鈥?The system will maintain the transaction details, including user ID, transaction date
and time, existing LCA date, consent given indicator, consent given date and health
warranty expiry date, into the log table for audit trail.
Perform Consent for LCA Updating
Appendix B: Rules Update Consent for LCA Rules 190


Update Health Warranty Rules
This section tells the rules in update health warranty.
(cid:129) When you update the health warranty expiry date, the health warranty expiry date must meet
the following rule:
鈥?current system date 鈮?health warranty expiry date 鈮?current system date + 30 days
(cid:129) When you click Submit:
鈥?Interest will be charged for the policy that is backdated for more than 183 days. The
system will calculate the up-to-date total enforcing amount and display the amount. For
backdated cases, the system will calculate the number of installments required and
update the total enforcing amount.
鈥?The system will maintain the transaction details, including user ID, transaction date
and time, existing LCA date, consent given indicator, consent given date and health
warranty expiry date, into the log table for audit trail.
Perform Health Warranty Expiry Date Updating
This section tells the rules for updating LIA Information.
Application date rules:
(cid:129) The Application Date is mandatory when you update or add LIA information from the Update
module.
(cid:129) If you enter this module by Underwriting Main Screen, and the application type is NB, the
application date is set the same as the policy鈥檚 application date; if the policy鈥檚 application date
is blank, the system will set the application date to the submission date.
(cid:129) If the application type is CS, and CS commencement date exists, the application date is set to
the CS commencement date; if CS commencement is blank, the application date is set to the
CS end date.
When user entered search criteria and clicks Search on the
Update LIA Information page:
(cid:129) System displays the insured鈥檚 details in the Customer List section.
Related rules are as follows:
Based on search criteria entered, system will search and display unique insured details from a
combination of the following:
Appendix B: Rules Update Health Warranty Rules 191


鈥?Existing party information
鈥?Uploaded LIA information
NOTE: In NB Underwriting, CS Underwriting and Claim Underwriting, the search criteria will be
disabled. System will display all the LIA records of the selected customer. User cannot search for other
customers in this interface; In update/query LIA, the search criteria are enabled and user can freely
search any customer in system.
Example - System Display Insured Details
E.g. User searches for First name = JOHATHAN and Last name = KING. System found existing
customer and also record in LIA information and the records have EXACT:
In this case, only one record will be displayed in the Customer List section.
(cid:129) System displays existing LIA information for the selected insured in the LIA Information
section. Related rules are as follows:
On selection of the insured from customer list, system will display LIA information for the
insured.
There are different rules for displaying LIA information entered by user and LIA information
uploaded from other reporting companies:
Appendix B: Rules Update LIA Information Rules 192


Table 29: Different Rules for Displaying Manual Entered LIA Information and
Uploaded LIA Information
LIA Records Source
LIA records created For LIA records which are created by user's company, LIA records
by user's company with the following details EXACTLY the same with the insured
will be displayed:
Selection radio button for such records are enabled. If user
modifies the record in this user interface, system will overwrite
the policy number in the LIA record. If user adds a new record,
the policy number of this new record will be current policy
LIA records uploaded For LIA records uploaded from other reporting companies, LIA
from external insurers records with the following details EXACTLY the same with the
insured will be displayed:
Selection radio button for such records are disabled which means
that user cannot modify the records from other companies.
When user completed LIA information entrance and click
Submit on the Add/Edit LIA Information page:
System updates the LIA information.
(cid:129) User can only update the LIA records whose company is current user鈥檚 company. The records
from other companies cannot be modified.
(cid:129) In NB, CS, system will display the previous policy number in read-only mode. If it is empty,
system will use current policy number by default. In claim and update LIA function, user can
input or modify policy number. In this case, if user entered the policy number, system will
validate if the insured is the insured of the policy number. If the insured is not the insured of
the policy or the policy number is not valid, system will prompt error message Invalid
policy number or the party is not the insured of the policy.
Appendix B: Rules Update LIA Information Rules 193


(cid:129) For newly created LIA records, system will allocate a sequence number. Sequence number will
start with YYYY year and following by a 6 digit sequence number. The format is like 2014
000001. Need an extension point to allow user to define other sequence logic.
(cid:129) Newly created records will have a default company code representing current user鈥檚 company.
In this release, we assume the company number is GE for baseline.
When user browsed a local LIA file and clicks Submit on the
Upload/Download LIA Data File page:
System validates file format and display results
(cid:129) System will validate file format of upload file is correct. System will validate file record by
record and an error message Notes: Line {line number} 鈥渰line content}鈥?
has error. Please check! will be displayed on top left of screen in red once an error
is found.
NOTE: See LIA Data File Format for more information on the LIA Data file's format.
(cid:129) Sequence no. + Company code will be the key to identify unique record. If duplicate records
exist, system will overwrite previous record with the newest one.
(cid:129) If NO errors are found, system will display Notes: File upload successful. on
top of screen in red.
(cid:129) Uploaded LIA records will be stored in system and can be queried and updated via 鈥淯pdate
LIA鈥?
When user clicks Download on the Upload/Download LIA
Data File page:
System will extract LIA data based on the following:
(cid:129) All records with predefined company code (such as = 16 or GE)
(cid:129) Previously extracted records need to be excluded.
(cid:129) System will generate file based on file format specified in LIA Data File Format.
When user entered search criteria and clicks Search on the
Query LIA Information page:
Rules are the same as that in System displays the insured鈥檚 details in the Customer List section.
Appendix B: Rules Update LIA Information Rules 194


Waive Overdue Interest Rules
This section tells the rules for waiving overdue interest.
(cid:129) Only when a) the product allows backdating, and b) the commencement date is more than 183
days earlier than the system date, the overdue interest will be generated.
(cid:129) When you click Submit, the system validates that user鈥檚 waiver authorized limit for overdue
interest set in the access matrix table is greater than or equal to the waived amount entered. If
not, an error message OD Interest amount to be waived is above authorized limit will be
鈥?Calculation of overdue interest amount
鈥?Total outstanding overdue interest = calculated overdue interest up to date - waived
overdue interest amount
鈥?The amount waived by user is considered waived permanently with no validity period
unless the proposal status is updated to withdrawal.
鈥?If the proposal status is updated to withdrawal, the system will delete the waived
overdue amount record and log it as transaction history.
鈥?After the deletion of waived overdue amount due to withdrawal status and the proposal
is re-open for processing, the system calculates the full overdue interest amount if any
and charges the full amount as part of the total inforcing amount.
鈥?Interest due is calculated from backdated start date to issue date, that is, up to the
transaction date of enforcement. This is still on a per annum per day basis.
(cid:129) After the system check passed, the system saves the entered information and records the
waived overdue interest amount. The amount will be deducted from the policy鈥檚 total
outstanding overdue interest amount.
(cid:129) The system will keep the transaction details, including User ID, Date, Time, overdue interest
calculated, overdue interest waived, transaction date, reason for waiving overdue interest and
user access level) in the log table for audit trail purpose.
(cid:129) The system will validate the total inforcing amount required for the proposal and inforce the
proposal if all inforcing criteria are met. For details, refer to Inforce.
Perform Waiving Overdue Interest
When user selected file to upload and clicks Submit on the
Upload/Download AML Data File page:
System validates file format and displays results:
Appendix B: Rules Waive Overdue Interest Rules 195


(cid:129) System will validate file format of upload file is correct. Refer to AML Data File Format for
details of file format.
(cid:129) If any of the record is not valid, the uploading of the whole document will be failed. System
will prompt an error message Notes: Line {line number}, {Watch List
Number} : {error field name 1}, {error field name 2}...{error
field name n} has error. will be prompted on top left of screen in red.
(cid:129) If NO errors are found, system will display a message Notes: File upload
successful. on top of screen in red and upload.
(cid:129) System will validate file as rules below:
鈥?If file existing watch list type is UN List, for UN List, system will use replacement. It
means system will delete all related existing UN List first, and upload file.
鈥?Other Watch List Types, system always upload file as incremental.
(cid:129) Uploaded AML records will be stored in system and can be queried via Query AML List.
When user clicks Download on the Upload/Download AML
Data File page:
System will extract AML data based on the following:
(cid:129) All records should be includes in download file.
(cid:129) Download file format is Excel.
(cid:129) System will generate file based on file format specified in Interface File Specification.
When user set search criteria and clicks Search on the Query
AML Information page:
When user keys in Watch List Type, Watch List Number, ID number, first name and last name to
search AML information:
(cid:129) The System uses fuzzy search function for First Name and Last Name.
(cid:129) The System lists all match records under search result, and only 10 records display each page.
(cid:129) The System only searches for existing records of AML information.
(cid:129) Search result will be sorted by Watch List Type.


New underwriting rule for blacklist matching:
In New Business Data Entry, System checks if the customer is similar or identical with any record
on the AML blacklist during New Business Proposal Rules Validation. If matching rules is
satisfied, system will generate one underwriting issue.
RMS rules are set up for AML blacklist matching:
(cid:129) During New Business rule validation, system will check all parties against the blacklist in
system. The matching rule is same as the current Duplicate Party Validation rule.
鈥?If the policyholder is in the blacklist, the system displays a message: There is
similar blacklist record for policy holder. Please
validate.
鈥?If the life assured is in the blacklist, the system displays a message: There is
similar blacklist record for insured. Please validate.
鈥?If the payer is in the blacklist, the system displays a message: There is similar
blacklist record for payer. Please validate.
鈥?For identical blacklist party, the system displays a message: There is an
identical blacklist record. Please validate.
Appendix B: Rules Anti-Money Laundry Rules 197



---

# Appendix C: File Formats

Appendix C: File Formats
Table 30: LIA Data File Format
S/N (Headline) Data Type Length Description
1 CutRunN Character 10 Sequence Number
2 CutComC Character 2 Company Code
Company code is configurable.
3 CutPreN Character 15 Courtesy Title
up to 15 characters.
4 CutFrstN Character 25 First Name
up to 25 characters.
5 CutMidN Character 30 Middle Name
For LIA upload file, exclude this field.
For LIA download file, set the field as
blank.
6 CutLstN Character 30 Last Name
up to 30 characters.
7 CutSex Character 1 Gender
Set "F" for female and "M" for male.
8 Cutddmmyy Character 8 Date of Birth
yy Format: DDMMYYYY
9 ID type Character 2 ID type
10 CutID Character 30 I.D. Card Number, Passport
11 CutDRef Character 20 Internal Code
1 Policy number
2 Add blank space to the RIGHT to fill up to
20 characters.
Appendix C: File Formats LIA Data File Format 198


S/N (Headline) Data Type Length Description
12 CutRes Character 10 Summary result code
1 Summary result values are configurable.
2 If more than 1 entry, use "," as separator.
3 Add blank space to the RIGHT to fill up to
10 characters.
13 CutReasC Character 30 Reason or cause
1 Reason or cause details are configurable.
2 If more than 1 entry, use "," as separator.
3 Add blank space to the RIGHT to fill up to
30 characters.
14 Cutddmmyy Character 8 Application signed date
yy
(cid:129) For LIA download file, specify the extract
entry date of LIA record.
(cid:129) For LIA upload file, map to entry date of
LIA record.
(cid:129) Format: DDMMYYYY
15 Cutmark Character 100 Remark
up to 100.
Table 31: AML Data File Format
1 Entry Date DD/MM/YY N/A Yes Date of Entry
YY
Appendix C: File Formats AML File Format 199


2 Watch List Character N/A Yes Type of AML
Type Only for 9 types as
following:
(cid:129) UN List
(cid:129) Thailand List
(cid:129) Bankruptcy
(cid:129) Internal MIB
(cid:129) K888
(cid:129) Group MRTA
(cid:129) Group TRT
(cid:129) Claim
(cid:129) Agent Blacklist
3 Watch List Character N/A No Sub type of watch list
Sub Type No validation for this field.
4 Watch List Character N/A Yes Number of Watch List
Number No format checking, but
the field cannot be null.
5 Identifier Character N/A Yes Identifier Type
Type Values are defined in code
table.
6 ID Number Character N/A Yes ID Number
Cannot be null.
7 Gender Character N/A No Gender
This field is not
(cid:129) F
(cid:129) M
Set "F" for female and "M"
for male.
8 Entity Title Character N/A No Courtesy Title
This field is not
9 Entity First Character N/A Yes First Name
Name This field cannot be null.
Appendix C: File Formats AML File Format 200


10 Entity Last Character N/A No Last Name
Name No Validation for this
11 DOB DD/MM/YY N/A No Date of Birth
YY This field is not
(cid:129) Buddhist year with
12 Number of Character N/A No Number of Disc
Disc No Validation for this
13 Underwritin Character N/A No Underwriting Decision
g Decision Code
Code This field is not
14 Impairment Character N/A No Impairment Code
Code This field is not
15 Remark Character N/A No Remark written by an
underwriter
No Validation for this
16 Remark2 Character N/A No Extend Field
No Validation for this
Appendix C: File Formats AML File Format 201
