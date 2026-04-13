# InsureMO V3 User Guide — Payment

## Metadata
| Field | Value |
|-------|-------|
| File | insuremo-v3-ug-payment.md |
| Source | 16_Payment_0.pdf |
| System | LifeSystem 3.8.1 |
| Version | V3 (legacy) |
| Date | 2015-04-30 |
| Category | Finance / Payment |
| Pages | 57 |

---

## 1. Purpose of This File

Answers questions about payment requisition, approval, batch payment, cheque printing, and DCA workflows in LifeSystem 3.8.1. Used for BSD writing when payment processing, disbursement authorization, and payment methods are needed.

---

## 2. Module Overview

```
Payment (LifeSystem 3.8.1)
│
├── 1. Payment Requisition
│   ├── Normal Payment Requisition
│   ├── Medical Payment Requisition
│   ├── Commission Payment Requisition
│   └── Tax Payment Requisition
│
├── 2. Payment Approval
│
├── 3. Batch Payment
│   ├── Before it can work
│   ├── How it works
│   └── Perform Batch Payment Rules
│
├── 4. Payment Authorization
│   ├── Perform Payment Authorization
│   └── Payment Authorization Rules
│
├── 5. Payment Details Change
│
├── 6. Cheque Printing
│   ├── Print Cheque Online
│   ├── Print Cheque By Batch
│   └── Cheques Printing Rules
│
├── 7. Non-Cheque Payment
│
├── 8. DCA Payment
│   ├── Make DCA Payment
│   └── DCA Payment Rules
│
├── 9. Payment Cancellation
│   ├── Cancel Batch Payment
│   └── Cancel Online Payment
│
├── Appendix: Field Description
│
└── Appendix: Rules
    ├── Payment Requisition Rules
    ├── Payment Authorization Rules
    ├── DCA Payment Rules
    ├── Cheques Printing Rules
    ├── Cancel Payment Rules
    └── Perform Batch Payment Rules
```

---

## 3. About Payment

Payment means the insurer refunds to the payee for business transactions such as surrender, Third Party Damage (TPD), medical billing through various disbursement methods. Payee includes policyholder, assignee, beneficiary, clinic, bank, government and so on.

The following diagram shows the workflow of payment.

**Table 1: Description of Payment Workflow**

| S/N | Description |
|-----|-------------|
| 1 | Payment requisition is the refund request sent to the insurer when a payment record is generated. The payment can either be directly refunded to the payee or be transferred to another policy or proposal. For detail, refer to section Payment Requisition. |
| 2 | For the transactions such as maturity, cash bonus, loan, refund of suspense, claim, annuity, and medical expenses, the payment need to be performed regularly and automatically by system through batch jobs. For details, refer to section Batch Payment. |
| 3 | Payment authorization is to decide whether to accept the payment or reject it. If authorized, the payment record is ready for cheque print. If rejected, the payment record status will be changed to Cancelled and a new payment record with status of Pending Requisition will be added. For details, refer to section Perform Payment Authorization. |
| 4 | The information of a payment such as the Disbursement Payee and Payment Bank can be changed if the payment is not paid. For details, refer to section Change Payment Details. |
| 5 | If the disbursement method of a payment is cheque and the payment record is authorized or the payment requisition is performed by a user with sufficient authority limit to bypass payment authorization, the payment is ready for cheque print. For details, refer to section Cheque Printing. |
| 6 | If the disbursement method of a payment is TT Manual cheque or Bank draft, and the payment record is authorized or the payment requisition is performed by a user with sufficient authority limit to bypass payment authorization, the payment record is ready for non-cheque payment. For details, refer to section Make Non-Cheque Payment. |
| 7 | If the disbursement method is direct credit, on scheduled date, the system extracts direct credit account (DCA) records and generates submission control reports. You need to download DCA files and send the tapes to bank for further process. For details, refer to section Make DCA Payment. |
| 8 | After a cheque payment has been authorized, for special reasons, such as spoilt cheque, payment details change, and void payment requisition, the client or bank may request to cancel the payment. For details, refer to Payment Cancellation. |

---

## 4. Payment Requisition

Payment requisition is the refund request sent to the insurer when a payment record is generated. The payment record is generated when an upstream NB, CS or payment item is processed. You can perform policy payment, suspense refund and other accounts payment. The payment can either be directly refunded to the payee or be transferred to another policy or proposal. Once the payee confirms the payment requisition, the payment records will be sent to the payment authorization process.

There are four types of payment requisition:

- Normal payment
- Medical payment
- Commission payment
- Tax payment

### 4.1 Normal Payment Requisition

**Workflow:** Payment Requisition → Normal Payment Requisition

**Steps:**

1. From the main menu, select Billing/Collection/Payment > Payment > Online Payment > Payment Requisition.
2. On the Payment Requisition page, select the payment requisition type Normal.
3. Enter the search criteria, for example the Policy Number, and click Search.

   **RESULT:** Records that match the search criteria are displayed.

4. Select a payment record by clicking the policy number.

   **RESULT:** The Perform Payment Requisition - Payment Selection page is displayed for the selected policy.

5. Select the target record(s) and click Calculate Total Payment to calculate the total payment amount.

   **RESULT:** The Perform Payment Requisition - Update page is displayed.

6. Choose the payment method and update the payment.

   **NOTE:** You have three choices to settle the payment:
   - Give the payment to the payee directly;
   - Or transfer the payment to another policy or proposal;
   - Or transfer the payment to a Customer Account through internal transference. For details, refer to Customer Account User Manual.

   a. In the Expenditure area, choose a payment method from the Disbursement Method drop-down list.

   **NOTE:**
   > To give the payment to the payee directly, choose one disbursement method from the following:
   > - Cash
   > - Cheque
   > - Direct Debit
   > - Bank Draft
   > - Telegraphic Transfer
   > - Manual cheque
   > - Money Order
   > - Cashier Order

   > Then continue with Step b, Step c, Step d, Step e and Step g to complete the payment.

   > To transfer the payment to a Customer Account, select Transfer to Customer Account, and then continue with Step b, Step c, Step d, Step e and Step g to complete the payment.

   > To transfer the payment to another policy or proposal, skip the current step and continue with Step f and Step g to complete the payment.

   b. Select a currency from the Payment Currency drop-down list.
   c. Enter the payment amount in Policy Amount.
   d. (Optionally) If the payment currency and the SI currency are different, enter the exchange rate.
   e. Click Add.

   **NOTE:** To delete a payment, select the payment and then click Del.

   **RESULT:** The payment details are displayed.

   f. In the Transfer area, enter the policy/proposal number, policy amount, foreign exchange rate and suspense type.
   g. Click Submit.

**RESULT:** The system checks whether requisition needs to be approved (which can be configured).

- If yes, go to the Approval process.
- If not, and you choose to pay the payee directly, the System checks whether the payment exceeds the authority limit.
- If yes, go to Perform Payment Authorization.
- If not, complete the following tasks according to different disbursement method you selected:
  - If you chose Cheque as disbursement method, go to Cheque Printing.
  - If you chose Direct Debit as disbursement method, go to Make DCA Payment.
  - If you chose other disbursement methods including Cash, Bank Draft, Telegraphic Transfer, Manual Cheque, Money Order or Cashier, go to Make Non-Cheque Payment.

---

### 4.2 Medical Payment Requisition

**Workflow:** Payment Requisition → Medical Payment Requisition

**Steps:**

1. From the main menu, select Billing/Collection/Payment > Payment > Online Payment > Payment Requisition.
2. On the Payment Requisition page, select the payment requisition type Medical Payment.
3. Enter the target invoice number in Invoice Number, and click Search.

   **RESULT:** Records that match the search criteria are displayed.

4. Select a payment record by clicking a hyper-link under Disbursement Payee.

   **RESULT:** The Perform Payment Requisition - Medical Payment Selection page is displayed.

5. Select the target record(s) and click Submit.

   **RESULT:** If payment is done, the System prompts a message box, saying "Perform allocation successfully."

6. Click OK to close the message box.

---

### 4.3 Commission Payment Requisition

**Workflow:** Payment Requisition → Commission Payment Requisition

**Steps:**

1. From the main menu, select Billing/Collection/Payment > Payment > Online Payment > Payment Requisition.
2. On the Payment Requisition page, select the payment requisition type Commission Payment.
3. Enter the search criteria, for example, an agent number in Agent No., and click Search.

   **RESULT:** The Perform Payment Requisition - Payment Selection page is displayed.

4. Select payment record(s) by selecting the check-box(es) ahead of each record line.
5. Select a payment method in Disbursement Method.

---

### 4.4 Tax Payment Requisition

**Workflow:** Payment Requisition → Tax Payment Requisition

**Steps:**

1. From the main menu, select Billing/Collection/Payment > Payment > Online Payment > Payment Requisition.
2. On the Payment Requisition page, select the payment requisition type Tax Payment.
3. Enter the search criteria, for example, the Payment Type, and click Search.

   **RESULT:** The Perform Payment Requisition - Payment Selection page is displayed.

4. Select payment record(s) by selecting the check-box(es) ahead of each record line.
5. For each payment record selected, specify a payee in Disbursement Payee.

---

## 5. Payment Approval

This topic explains how to approve payments.

When you need to approve or reject the payment that has completed the payment requisition process, do as follows:

1. From the main menu, select Billing/Collection/Payment > Payment > Online Payment > Approve Payment.
2. Search out the target payment record.
3. Check the payment information and make your decision:
   - Click Approve to accept the payment.
   - Click Reject to reject it.

---

## 6. Batch Payment

### 6.1 About Batch Payment

For the transactions such as maturity, cash bonus, loan, refund of suspense, claim, annuity, and medical expenses, the payment need to be performed regularly and automatically by system through batch jobs. This kind of payment is called batch payment.

The system extracts policies that fulfill the extraction criteria, creates batch payment records, and assigns a unique and sequential batch number to the records. A report listing the policies where batch payment records are created as well as exception cases will be generated. The batch payment records are then transferred to payment authorization process.

### 6.2 Before it can work

- Batch payment process, based on Customer Service rules, should have been completed
- Payment records with Fee Type 32 should have been generated, with the payee details and payment date (cheque date).
- Only Fee Type 32, Fee Status 0 (Waiting for Processing) is eligible for printing.
- Payment Date can be post dated based on the eligibility at the policy level.
- Report will be generated with details of records eligible for Batch Payments.
- Batch numbers should be generated for all eligible transactions as required.

### 6.3 How it works

1. System extracts a list of policies for which batch payments need to be made.
2. System updates the CB/SB account balance and payment information for payments to be made.
3. System generates the batch payment and exception cases report.

---

## 7. Payment Authorization

Payment authorization is to decide whether to accept the payment or reject it. If authorized, the payment record is ready for cheque print. If rejected, the payment record status will be changed to Cancelled and a new payment record with status of Pending Requisition will be added. Two types of payment records should undergo the payment authorization process: the payment records that exceed the authority limit in the Payment Requisition process and all batch payment records.

### 7.1 Perform Payment Authorization

**Prerequisites:** For batch payments, batch numbers must be assigned and the batch payment records must be created beforehand.

**Steps:**

1. Search the target payment record.

   a. From the main menu, select Billing/Collection/Payment > Payment > Online Payment > Payment Authorization.

   **RESULT:** The Payment Authorization page is displayed.

   b. Select a payment requisition type, set search criteria and then click Search.

2. Authorize the payment record.

   a. Select the payment record to be authorized or rejected.
   b. Select Authorize Payment and then click Submit to authorize the payment.
   c. Select Reject Payment, select a rejection reason, and then click Submit to reject the payment.

   **RESULT:** The system cancels the payment record. A message box is displayed, indicating the authorization is successful.

---

## 8. Payment Details Change

You can change the information of a payment such as the Disbursement Payee and Payment Bank if the payment is not paid. Only the information of non-cheque payment and batch payment can be changed.

### 8.1 Change Payment Details

**Prerequisites:** The payment is non-cheque payment and batch payment.

**Steps:**

1. Search the payment record and choose what kind of payment information to be changed.

   a. From the main menu, select Billing/Collection/Payment > Payment > Online Payment > Change Payment Details.

   **RESULT:** The Change Payment Details page is displayed.

   b. Select a change option, enter the search criteria and then click Search.

   **RESULT:** The target payment records are displayed.

2. Change and update the payment information.

   a. Click the policy number under the Search Results area to open the Change Payment Details – Payment Selection page.
   b. Select a payment record under the Payment Details area and then click Submit.
   c. To change the bank account, choose a new bank account from the Bank Account No. drop-down list and then click Submit.
   d. To change the disbursement payee, select a Party ID type and Party ID No. and then click Retrieve Party Details.
   e. Click the new payee name in the popup page and the new name will be filled in the Disbursement Payee field.

   **NOTE:** If no disbursement payee is found, the system will display a prompt message "No matching disbursement payee found! Create a new party?" Click OK to create a new one or Cancel to quit the operation.

3. Generate a report.

   **NOTE:** After the information of a payment is changed, the system generates a report to the third party through a nightly batch job.

---

## 9. Cheque Printing

If the disbursement method of a payment is cheque and the payment record is authorized or the payment requisition is performed by a user with sufficient authority limit to bypass payment authorization, the payment is ready for cheque print.

### 9.1 Print Cheque Online

**Prerequisites:**
- The payment requisition is performed by a user with sufficient authority limit to bypass payment authorization.
- The payment record is authorized.

**Steps:**

1. Search the payment records ready for cheque print.

   a. From the main menu, select Billing/Collection/Payment > Payment > Online Payment > Print Cheque.

   **RESULT:** The Print Cheque page is displayed.

2. Print the cheque.

   a. Select payment record for cheque printing.
   b. Select Print consolidated cheque if you want to lump the amount of all selected payment records into one cheque.

   **RESULT:** System will consolidate payment if payment records have the same cheque date, bank account and disbursement payee.

   c. Enter the starting cheque number in Starting cheque No. field.

   **RESULT:** The Ending cheques No. and Number of cheques to print fields will be auto-filled based on the number of selected payment records.

### 9.2 Print Cheque By Batch

**Steps:**

1. Search the batch payment cheque.

   a. From the main menu, select Billing/Collection/Payment > Payment > Batch Payment > Print Cheque.

   **RESULT:** Payment cheque records are listed in the Cheque Printing area.

2. Enter the cheque stock range in the Cheque Stock Range – Start textbox and select a bank account number from the Bank Account No. drop-down list.

   **NOTE:** For descriptions of the fields on this page, see Fields on Batch Cheque Printing – Search Page.

3. Print cheque.

   a. In the Cheque Printing area, select the payment records to be printed.

   **NOTE:** Select the check box before each record to select a payment record or select the check box at the header line to select all records.

   **RESULT:** The Batch Cheque Printing – Print page is displayed.
   c. Click Print.

   **RESULT:** The Batch Cheque Printing – Confirm page is displayed.
   d. Select the cheques to be printed and click Confirm.

   **RESULT:** The cheques are printed.
   e. Click Exit.

4. Perform posting to GL.

   **TUTORIAL INFORMATION:** For details, refer to section Perform Posting to GL User Manual.

---

## 10. Non-Cheque Payment

If the disbursement method of a payment is cash, TT manual cheque, or Bank draft, and the payment record is authorized or the payment requisition is performed by a user with sufficient authority limit to bypass payment authorization, the payment record is ready for non-cheque payment.

### 10.1 Make Non-Cheque Payment

**Prerequisites:**
- The payment requisition is performed by a user with sufficient authority limit to bypass payment authorization.
- The payment record is authorized.
- The disbursement method of a payment is TT Manual cheque or Bank draft.

**Steps:**

1. Search the payment records ready for non-cheque payment.

   a. From the main menu, select Billing/Collection/Payment > Payment > Online Payment > Non-cheque Payment.

   **RESULT:** The Non-cheque Payment page is displayed.

   **RESULT:** The target records are displayed.

2. Select the payment record and submit the payment.

   a. In the Non Cheque Payment area, select the payment record, and then enter the payment reference number and comment.

3. Perform posting to GL.

   **TUTORIAL INFORMATION:** For details, refer to section Posting to GL User Manual.

---

## 11. DCA Payment

If the disbursement method is direct credit or direct debit, on scheduled date, the system extracts direct credit account (DCA) records and generates submission control reports. Or user can manually perform bank transfer extraction to extract bank transfer file. The information will be saved. Then user can go to Download Direct Debit Bank File module to download the Direct credit file and send it to bank. After the bank processes the file and return the file, user can go to Upload Direct Debit Bank File module to upload the Direct Credit file. And then the system will verify the data.

### 11.1 Make DCA Payment

**Prerequisite:** The disbursement method is direct credit.

**Steps:**

1. Extract bank transfer file.

   a. From the main menu, select Collection/Billing/Payment > Billing > Electronic Collection > Bank Transfer > Bank Transfer Extraction.

   **RESULT:** The Bank Transfer Extraction page is displayed.

   b. Set search criteria and click Search.

   **RESULT:** The bank transfer record is displayed.
   c. Select it and click Submit.

2. Download direct credit extraction file.

   a. From the main menu, select Collection/Billing/Payment > Billing > Electronic Collection > Bank Transfer > Download Bank File.

   **RESULT:** The Perform Direct Debit Extraction - Download File page is displayed.

   b. Enter the generation date and bank code/name, and then click Download to download the direct credit extraction files.

3. Upload direct credit extraction file.

   a. After the file is processed and returned from the bank, go to Collection/Billing/Payment > Billing > Electronic Collection > Bank Transfer > Upload Bank File.

   **RESULT:** The Upload Direct Debit Bank File page is displayed.

   b. On the Upload Direct Debit Bank File page, enter the batch number and click Browse to localize and select the local-saved return file.

   **RESULT:** System captures the data on file and confirms the payment to client.

---

## 12. Payment Cancellation

After a cheque payment has been authorized, for special reasons, such as spoilt cheque, payment details change, and void payment requisition, the client or bank may request to cancel the payment.

### 12.1 Cancel Batch Payment

**Prerequisite:** The payment records to be cancelled already exist in the system.

**Steps:**

1. Search out the batch payments to be cancelled.

   a. From the main menu, select Billing/Collection/Payment > Payment > Batch Payment > Cancel Payment.

   **RESULT:** The Cancel Payment page is displayed.

   b. Set search criteria, and then click Search.

   **RESULT:** The qualified batch payment record is displayed.

2. Cancel batch payments.

   a. Select a cancellation type from the Cancellation Type drop-down list.
   b. Select the target batch payment record.

   **NOTE:** The reason for cancellation is automatically displayed.

   **RESULT:** The batch payments are cancelled.

**AFTER COMPLETING THIS TASK:**

The system checks the cancellation type:

| If… | Then… |
|-----|-------|
| The cancellation type is expiry | You can authorize the payment again. For details, refer to section Perform Payment Authorization. |
| The cancellation type is spoilt or internal error | You can print the cheque again. For details, refer to section Cheque Printing. |
| The cancellation type is void payments | You can perform payment requisition. For details, refer to section Payment Requisition. |

### 12.2 Cancel Online Payment

**Steps:**

1. Search out the payment records to be cancelled.

   a. From the main menu, select Billing/Collection/Payment > Payment > Online Payment > Cancel Payment.

   **RESULT:** The Cancel Payment page is displayed.

   b. Set search criteria, select a cancel reason from the Cancel Reason drop-down list, and click Search.

   **RESULT:** The target policy record is displayed.
   c. Under the Policy No. list, click the target record.

2. Cancel payment records.

   a. On the Cancel Payments – Update page, select the payment records to be cancelled.

   **RESULT:** The payment records are cancelled.

**AFTER COMPLETING THIS TASK:**

The system checks the cancellation type.

| If… | Then… |
|-----|-------|
| The cancel reason is void payment requisition | You can perform payment requisition. For details, refer to section Payment Cancellation. |
| The cancel reason is not void payment requisition | You can print the cheque. For details, refer to section Cheque Printing. |

---

## Appendix A: Field Description

### Fields on Batch Cheque Printing – Search Page

| Field | Description |
|-------|-------------|
| Cheque Stock Range-Start | The start of the cheque number which will be printed in the cheque. The cheque number range is bundled with a bank account and can be configured in the Finance module. |
| Group By Payee | If selected, payment records that have the same cheque date, bank account and disbursement payee are grouped. The grouped payments will be printed in one cheque. |
| Bank Account No. | The bank account of the insurer used to pay the payment. |
| Update | Used to confirm the bank account selection. |

---

## Appendix B: Rules

### B.1 Payment Requisition Rules

**When you select payment record to calculate the payment amount:**

- Payment records have the following payment types:
  - Policy Payment
  - Surrender
  - Loan
  - Maturity
  - Annuity
  - Medical Payment

- Suspense records have the following suspense types:
  - Renewal: All non CPF collection methods excluding premium voucher collection method renewal suspense
  - Policy Collection: All non CPF collection methods excluding premium voucher collection method policy collection suspense
  - General: All non CPF collection methods excluding premium voucher collection method general suspense

  The balance is consolidated based on the different suspense types.

- If you select more than one payment record, these payment records must belong to the same disbursement payee.
- The total payment amount of all the selected records must be greater than zero.

**When you enter the target policy number to which the payment is transferred:**

While its policyholder is different from that of the source policy, system will prompt message as a reminder. However, you can click OK to continue.

**When you click Submit to submit the payment:**

- The total payment amount for the selected disbursement methods must equal the total payment amount displayed in the Policy Basic Information area.
- For the payment transferred to another policy, the payment record will go to Posting to GL process.

**Payment types covered under Payment Requisition:**
- Normal Payment Requisition
- Medical Payment Requisition
- Commission Payment Requisition
- Tax Payment Requisition

---

### B.2 Payment Authorization Rules

1. When the payment amount is greater than your authorization limit, you can only view but cannot authorize or reject the records.
2. When the payment is authorized successfully, the authorization information is saved and the system checks the disbursement method:
   - If the disbursement is cheque, go to cheque print process. See Cheque Printing for details.
   - If it is TT, go to non-cheque payment process. See Make Non-Cheque Payment for details.
   - If it is DCA, go to DCA payment process. See Make DCA Payment for details.

---

### B.3 DCA Payment Rules

**Bank transfer file extraction rules:**

- Payment record exists.
- Bank account is valid.
- Not bank transfer suspended.
- Pay mode is bank transfer or credit card.

---

### B.4 Cheques Printing Rules

**Input Validation:**

When users select cheques to print, system validates the cheque number input by the user. The cheque number should be unique for the current cheque range. System will alert the user via error message if the cheque number input by the user has already been used within the cheque range.

Once users submit the cheque printing request, system validates if the selected payment records' branch payment bank accounts are the same. If not, a message is prompted to the user.

**Online Cheque Printing:**

For online cheques, the user must ensure that all the cheques are printed online. If any cheques are spoilt due to paper jammed, the user will need to cancel the cheques. The cheque record will be dropped into payable account and will appear in this print cheque UI if the filter is selected = Spoilt Cheque. The user does not need to go through the Perform Requisition and Authorise Payment process again.

**Batch Cheque Printing:**

- For annuity, maturity, cash bonus and survival benefit cases, the cheque date should be based on the payment due date if it is in the future. If the payment due date is in the past, the cheque date should be based on the current cheque printing date.
- For the ease of distribution, the remittance advice should be attached to the cheques printed.
- A batch cheque can be printed as an online cheque if the user desires.

**NOTE:**
- For Control purpose, the remittance advice generated online in PDF format. It cannot be saved locally.
- If the user has selected to print a few payment records or multiple policies payment records in a consolidated cheque, the remittance advice description will not be printed so that the user is aware that it is a consolidated cheque payment and a letter has to be prepared manually.
- If the payee is dead, the system prints payee's title with 'Estate of' in front of the Payee's name when printing the Remittance advice. If the Payee is still alive, the system needs not print the Payee title.
- When performing Cheque Printing, the system checks policy Organization ID against individual payment record.

---

### B.5 Cancel Payment Rules

When users enter search criteria, system validates if any payment records match search criteria. Payment Team users can only cancel payment records transacted on the same day (only applicable for payment status = Payment processed). Finance users can cancel payment records transacted on prior days. For the rest of the Payment Status such as Pending Payment Requisition, Pending Approval or Approved, users can process any day.

When selecting the cancellation reason from the drop-down list, users can select the following values:

- **Spoilt Cheque:** Only applicable for payment records with payment status = payment processed.
- **Change Payment Details:** Only applicable for payment records with payment status = Pending Approval, Approved or Payment Processed.
- **Void Payment Requisition:** Only applicable for payment records with payment status = Pending Approval, Approved or Payment Processed.

**NOTE:** If cancel reason is selected as void payment requisition, the search results will also display all the related payment records and internal transfer records (include offset from debts outstanding and transfer to suspense accounts). If users selects one payment record to cancel, by default the related payment records and internal transfer records will be selected.

**Payment Status Types:**

| Status | Description |
|--------|-------------|
| Pending Payment Requisition | Payment status before payment requisition is submitted. |
| Pending Approval | Payment status after payment requisition is submitted and awaiting approval. |
| Approved | Payment status after authorized signatory authorized the payment using the Authorise Payment UI. For disbursement method of cheque, this would be equivalent to the pending cheque printing stage. |
| Payment Processed | Payment status after a payment has been made. For disbursement method of cheque, this would be equivalent to the cheque printed stage. |
| Payment Confirmed | Payment status after a payment has been confirmed. For disbursement method of cheque, this would be equivalent to cheque has been cleared by bank. |
| Cancelled | Payment status tagged to a payment record that has been cancelled. A new payment record will be inserted. |

System will set the payment status of the cancelled payment record as Cancelled, then insert a new payment record with the appropriate payment status as specified in tables below.

**For Gross Payments > Payment authority limit of user who submitted payment requisition, upon payment cancellation, statuses are as below:**

| Payment Status | Disbursement Method | Cancel Payment Reason | Pending Payment Requisition | Pending Approval |
|----------------|--------------------|-----------------------|---------------------------|------------------|
| Cheque, Manual | Spoilt Cheque | N/A | N/A |
| Cheque, TT, Bank Draft, Deferred Benefit, CPF-MEPS | Change of Disbursement Payee Details | N/A | N/A |
| Cheque, TT, Bank Draft, Deferred Benefit, CPF-MEPS | Void Payment Requisition | N/A | Status = Pending Payment Requisition upon payment cancellation |

**For Gross Payment <= Payment authority limit of user who submitted the payment requisition, upon payment cancellation, statuses are as below:**

| Payment Status | Disbursement Method | Cancel Payment Reason | Pending Payment Requisition | Pending Approval |
|----------------|--------------------|-----------------------|---------------------------|------------------|
| Cheque, Manual | Spoilt Cheque | N/A | N/A |
| Cheque, TT, Bank Draft, Deferred Benefit, CPF-MEPS | Change of Disbursement Payee Details | N/A | N/A |
| Cheque, TT, Bank Draft, Deferred Benefit, CPF-MEPS | Void Payment Requisition | N/A | Status = Pending Payment Requisition upon payment collection |

**NOTE:**
- If the user chooses a cancellation reason that is not applicable for the payment record, system will prompt an error message when the user submits the cancellation.
- If accidentally unselected any related payment records or internal transfer records for cancellation when cancel reason is void payment requisition, system will prompt an error message when the user submits the cancellation.
- Medical Payment Status and Medical Payment Date in NB should be nullified if the medical payment record has been cancelled with reason of Void Payment Requisition.
- If claims payment records are cancelled and payment status reverts to Pending Payment Requisition, the user will have to go to claims benefit allocation UI to re-submit the benefit allocation.

**Expired Cheques:**
A list of expired cheques will be provided once a month by Finance. Expired cheques should be cancelled and monies are returned to the cheque printing pool. Users will then decide if they want to reissue cheques or to undo the previous transaction to cancel the payable.

**NOTE:** For expired cheques cancellation, the process is handled by finance. Finance will cancel the cheques and update the cancellation reason to expired cheque. The system will cancel the original payment record and insert a new one with payment status as Approved. Customer Service users will have to determine if they want to do a further cancellation (i.e. void payment requisition) or issue a new cheque.

---

### B.6 Perform Batch Payment Rules

The system schedules the following types of batch payment:

- Suspend Refund
- CB/SB Option 1
- CB Option 9
- GreatLink Withdrawals
- Medical Payment
- Maturity
- Annuity

#### B.6.1 Suspend Refund

**Extract Policies:** The system will schedule the following runs to extract policies for NB and CS batch suspense refund.

- For CS, when policies have been surrendered or matured and the Direct Debit tape has already been sent, the money deducted from Direct Debit account will subsequently drop into general suspense. A run needs to be scheduled just after the Renewal Batch Job Run in order to have batch refund of monies to PH.
- For CS, policies (with policy status = Lapsed) with total suspense balance >= $0 for >3 years will need to have monies refund to PH. A monthly run needs to be scheduled to batch refund monies.
- For NB, different runs are scheduled to extract policies for each of the following scenarios which require batch suspense refunds:
  - Declined
  - Postpone
  - Withdrawn (Ad Hoc)
  - Withdrawn (Auto)
  - CICC
  - LCA Expiry
  - Inforced with excess Monies
  - Money comes in after the case has been postponed
  - Money comes in after the case has been declined
  - Money comes in after the case has been withdrawn (ad hoc and auto)

**For the system batch suspense refund runs:**

- Pick up all policies where policy status = Terminated and reason = Surrendered or Matured.
- Pick up all policies with payment method = Direct Debit.
- System will exclude policies with foreign address.
- System will exclude policies with invalid address.
- System will exclude foreign currency policies.
- System will exclude policies with multiple payees.
- System checks if the Lock Refund Indicator is set. If it is set, then no refund will be made.
- System checks that the total amount to be refunded (general suspense + policy collection suspense + renewal suspense) >= $10, no refund will be made.

**For CS batch suspense refund (Lapsed policies):**

- Pick up all cases where policy status = Lapsed.
- System will exclude policies frozen by Claims.
- System checks if the refund indicator is set.
  - If it is set, then no refund will be made.
  - If the Lock Refund Indicator is not set, then system checks the last collection date which resulted in monies moving into suspense (whether it is into general, renewal, or policy collection suspense). System will then send the policy for auto-refund provided System Date - Collection Date > 3 years. That is, system will pick up all policies where total suspense has been outstanding for more than 3 calendar years. For example, if system runs on 31 Oct 2004, then system picks up all policies with Collection Date (into suspense account) < 31 Oct 2001.
  - System checks that the total amount to be refunded (general suspense + policy collection suspense + renewal suspense) > $0, no refund will be made.

**NOTE:**
- Payment requisition will be bypassed for NB/CS batch refund. The payment needs to go through payment authorization and cheque printing stages. The user can key in the batch number to locate a batch of payments.
- When considering all/any suspense amounts to refund, premium voucher suspense is not included.
- Refund of premium from MSS will go back to CPF Board. It will be longer for any refund back to Policyholder since there will not be anymore interest refund to policyholder.
- All batch suspense refund (NB or CS) will be dropped into the Finance cheque printing pool.

**Update suspense account balance and payment information:**
- System reduces the monies paid from all suspense accounts (general suspense + policy collection suspense + renewal suspense).

**Generate batch suspense refund report:**
- Any cancelled NB or CS suspense refunds cannot go through the batch refund process again. They will have to be handled through manual refunds. The same applies for rejected payments.
- All cases extracted via this case will be dropped into Finance Cheque Printing Pool. Users will authorise cases where cheques are to be printed and reject cases where cheques are not to be printed. Finance will print the cheques.

#### B.6.2 CB/SB Option 1

**Extraction Criteria:**
a) Policy status is = In force
b) Policy is not frozen by Claims
c) SB/CB Option 1
d) CB/SB account balance > $5 (for all currencies)
e) SB/CB payable due date <= System date + 7 working days

**Exception Cases:**
a) Foreign Currency Policies
b) Payee is a Bankrupt
c) Servicing Branch is not equal to Singapore
d) Estate (Death Claim)
e) Payee is Minor
f) Payee is a Trustee
g) Multiple Payee
h) Payee's Address is invalid
i) Payee's Address is a Foreign Address
j) Payee = Company or dummy NRIC

**The following types of cases are also reflected in the working report:**
a) Cases which fulfill extraction criteria in CB Option 9 and SB/CB due date < System date + 7 working days.
b) Cases where cheque collection has been made in the last 7 days.

**Disbursement Method:**
- **Cheque:** Cases where disbursement method at policy level is Cheque and Cases where disbursement method at policy level is Direct Credit but payment amount > SGD $30,000.
- **Direct Debit:** Cases where disbursement method at policy level is Direct Credit and Payment amount <= SGD $30,000, and the Direct Debit account Self-Account indicator = approved. If the Direct Debit account Self-Account indicator is not Approved, then use set the disbursement method to Cheque.
- **CPF-MEPs:** Cases where disbursement method at policy level is CPF-MEPs.

#### B.6.3 CB Option 9

**Extraction Criteria:** Extract Policies where:
a) Policy Status is In Force
b) Policy is not frozen by Claims
c) System date >= Next Withdraw Due Date
d) CB Option 9
e) Withdraw Schedule Status = Effective
f) CB account balance > $5 (for all currencies)

**Exception Cases:**
a) Foreign currency policies
b) Payee is Bankrupt
c) Servicing Branch is not equal to Singapore.
d) Estate (Death Claim)
e) Payee is Minor
f) Payee is a Trustee
g) Multiple Payee
h) Payee's Address is invalid
i) Payee's Address is a Foreign Address
j) Payee = Company or dummy NRIC

**NOTE:** If more than one exception reason exist, e.g. policy currency is foreign currency and Payee is a bankrupt, the record should be split into two if it is difficult to have one record. However, sorting is to be done by Policy Number so that all the exception reasons for the same policy are together.

**Payment Amount:** The refund amount = min (next withdraw amount, current CP deposit account value), using system date to calculate the CB deposit account value. If refund amount = 0, no need to refund.

**Update CB Option 9 information:**
- Update withdraw schedule as following even the refund amount = 0
  - Next withdraw due date = Original Next Withdraw Due Date + the month of withdraw frequency. The month of withdraw frequency value: yearly is 12, half yearly is 6, quarterly is 3, and monthly is 1.
  - Next Withdraw Amount: If the withdraw type is increasing by compound interest, using the following compound interest calculation method: P' = P * (1+I)^(t/365). P': new next withdraw amount; P: original next withdraw amount; I: compound interest rate in SB withdraw schedule; t: the number of days between the original next withdraw due date to new next withdraw due date. If the withdraw type is by level, the next withdraw amount is not changed.
  - Withdraw schedule status: If the next withdraw due date > withdraw end date, set the status to terminate.

**Batch rules for cases which fulfills extraction criteria in GreatLink Withdraw, is not an exception case and for LS system, CB due date = System date + 7 working days:**
a) By country
b) By Disbursement Method
   - Cheque
   - Direct Credit
   - CPF-MEPs
c) By Branch Payment Account

#### B.6.4 GreatLink Withdrawals

**Extraction Criteria:** Extract payable records > 0 where Payment Type = GreatLink Withdrawal

**Batch rules:**
a) By country
b) Branch of the user who has submitted the GreatLink withdrawal transaction.

**Type of batch:** BCP Batch

#### B.6.5 Medical Payment

**Batch Frequency:** Monthly

**NOTE:** Monthly batch frequency here means that the job is run at the end of the month, depending on when business is closed for the month.

**NOTE:** There is no indicator for closing business for the month, therefore, system should take end of the month as close of business month.

**Extraction Criteria:** Extract payable > 0 where:
- Payment Type = Medical payment
- Transaction date is within the month.
- Payment Amount: Medical payment amount based on a per clinic / hospital basis on consolidated basis.
- Disbursement Payee: Refer to Claim-TPA document
- Disbursement Method: Cheque

**Batch rules:**
- By Country

**Type of Batch:** Finance Batch

#### B.6.6 Maturity

Refer to Perform Maturity User Guide.

#### B.6.7 Annuity

Refer to Perform Annuity Installment User Guide.

#### Generate Batch Payment and Exception Cases Report

The system generates the following reports for the respective types of Batch Payment:

- Suspense Refund
- CB Option 1
- SB Option 1
- CB Option 9
- ILP Withdrawals
- Medical Payment
- Maturity
- Annuity

---

## Revision History

| Date | Version | Change | Reference |
|------|---------|--------|-----------|
| 2014/12/30 | 00 | Initial Release. Changes from LifeSystem 3.8 | |
| 2015/04/30 | V3 | Updated for LifeSystem 3.8.1 | 16_Payment_0.pdf |
