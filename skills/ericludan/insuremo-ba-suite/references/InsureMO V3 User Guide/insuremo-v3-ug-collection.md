# InsureMO Platform Guide — Collection

## Metadata
| Field | Value |
|-------|-------|
| File | insuremo-v3-ug-collection.md |
| Source | 15_Collection_150605.pdf (78 pages) |
| System | LifeSystem 3.8.1 |
| Version | V3 (legacy) |
| Date | 2015-06-05 |
| Category | Billing / Collection |
| Pages | 78 |

---

## Table of Contents
1. [Purpose of This File](#1-purpose-of-this-file)
2. [Module Overview](#2-module-overview)
3. [Collection Workflow](#3-collection-workflow)
4. [Counter Collection](#4-counter-collection)
5. [Direct Debit Collection](#5-direct-debit-collection)
6. [Credit Card Collection](#6-credit-card-collection)
7. [Lock Box Collection](#7-lock-box-collection)
8. [Cancel Collection](#8-cancel-collection)
9. [Perform Waiver](#9-perform-waiver)
10. [Transfer and Apply Suspense to Other Account](#10-transfer-and-apply-suspense-to-other-account)
11. [Upload Batch Collection](#11-upload-batch-collection)
12. [Manage Unmatched Collection Records](#12-manage-unmatched-collection-records)
13. [Manage Cash Totalling](#13-manage-cash-totalling)
14. [Bank Account Authorization](#14-bank-account-authorization)
15. [Create or Modify Loan Repayment Schedule](#15-create-or-modify-loan-repayment-schedule)
16. [Update Premium Voucher Details](#16-update-premium-voucher-details)
17. [Lock and Unlock Suspense Refund](#17-lock-and-unlock-suspense-refund)
18. [Batch Functions](#18-batch-functions)
19. [Appendix A: Field Descriptions](#19-appendix-a-field-descriptions)
20. [Appendix B: Rules](#20-appendix-b-rules)
21. [Menu Navigation](#21-menu-navigation)
22. [INVARIANT Declarations](#22-invariant-declarations)

---

## 1. Purpose of This File

Answers questions about collection workflows and UI operations in LifeSystem 3.8.1. Used for BSD writing when collection-related UI screens, workflows, suspense account rules, batch jobs, and appendix rules are needed.

**Note:** This document is a comprehensive UI-reference guide with workflow diagrams, screen layouts, batch job descriptions, and detailed appendix rules. Supplement with `insuremo-v3-ug-renewal.md` for renewal billing rule details.

---

## 2. Module Overview

```
Collection (LifeSystem 3.8.1)
│
├── 1. Collection Workflow
├── 2. Counter Collection
│   ├── NB Collection
│   ├── CS Collection
│   ├── Misc Fee Collection
│   ├── Change Bank Account and Collection Date
│   └── Approve Collection
├── 3. Direct Debit Collection
│   ├── Bank Transfer Extraction
│   ├── Download Bank File
│   └── Upload Bank File
├── 4. Credit Card Collection
│   ├── Credit Card Extraction
│   ├── Download Bank File
│   └── Upload Bank File
├── 5. Lock Box Collection
│   └── Upload Lock-box and E-banking File
├── 6. Cancel Collection
├── 7. Perform Waiver
├── 8. Transfer and Apply Suspense to Other Account
├── 9. Upload Batch Collection
├── 10. Manage Unmatched Collection Records
├── 11. Manage Cash Totalling
├── 12. Bank Account Authorization
│   ├── Download Bank Authorization File
│   └── Upload Bank Authorization File
├── 13. Create or Modify Loan Repayment Schedule
├── 14. Update Premium Voucher Details
├── 15. Lock and Unlock Suspense Refund
└── Batch Functions
    ├── Reset Bank Account and Collection Date for Backdate
    ├── Credit Card Extraction
    ├── DDA Extraction
    └── Batch Generate Receipts
```

---

## 3. Collection Workflow

### 3.1 Main Collection Workflow

Collections are the money received from customers for business transactions attached to certain policy through various collection methods. Usually the policyholder determines a policy collection method when proposing, but insurer supports receiving collection by various methods. For example, customer proposes policy through Direct Debit, but pays cash for renewal premium later.

**Collection Workflow Table:**

| S/N | Description |
|-----|-------------|
| 1 | Counter Collection allows you to collect premium online for Traditional, investment linked and A&H Policies for insurance company. |
| 2 | On scheduled date, the system should generate Pre Direct Debit Notice and send it to Policyholder. So that Policyholder can deposit sufficient amount in the corresponding bank account beforehand. |
| 3 | On scheduled date, the system should generate Pre Credit Card Notice and send it to Policyholder. So that Policyholder can deposit sufficient amount in the corresponding bank account beforehand. |
| 4 | To perform lockbox collection, refer to section Lock Box Collection. |
| 5 | Cancel Collection allows you to cancel collections online for all types of collection methods (including dishonored cheque) for Traditional, investment linked and A&H Policies for insurance company. |
| 6 | Perform BCP Waiver allows you to waive interest for APL, policy loan and study loan, as well as to waive service tax, alteration/policy fee, switching fee, miscellaneous fee, overdue interest, stamp duty and benefit card. |
| 7 | Transfer and Apply Suspense into Other Account allows you to transfer monies between different suspense accounts (Policy Collection, Renewal and General) for insurance company. |
| 8 | Manage Cash Totaling allows you to perform cash totaling for the day for Traditional, investment linked and A&H Policies for insurance company. |
| 9 | Bank Account Authorization: When an account is created or modified, system generates a file which will be sent to bank offline by Back Office staff. After validating the account, the bank returns a file with confirmation result to insurer. The confirmed result will be uploaded to system by Back Office staff; the System then updates bank account's Authorization Status automatically. |

---

## 4. Counter Collection

Counter Collection allows you to collect premium online for Traditional, investment linked and A&H Policies for insurance company.

Receive Counter Collection allows for the update of collections via the counter or ad-hoc collection which needs to be made, for example, any non-cash entries such as amount from Deferred Benefit.

The collection methods available include cash, cheque, credit card, e-banking, lockbox, and DDA.

When you search for a specific policy to enter the collection details, the system will quote the default allocated amounts and populate the net amount payable. However, you can also overwrite the collection information as needed and submit the transaction. The system validates the payment and allocates the collection accordingly — for example, to premium, overdue premium, overdue interest, APL, policy loan, study loan, miscellaneous fees, APA, cash bonus account deposit, survival benefit deposit, suspense, etc. You can also choose to print receipts online from the system.

**Prerequisites:**
- The policy has been accepted.
- For bulk collection transactions, cashier has identified whether the bank account and collection date need to be changed. See Change Bank Account and Collection Date.

### 4.1 Counter Collection for New Business

1. Search out the policy whose premium is to be collected.
   a. From the main menu, select **Billing/Collection/Payment > Collection > Receive Counter Collection**.
   RESULT: The Receive Counter Collection - Search page is displayed.
   b. On the Receive Counter Collection page, select **NB Collection**, set the search criteria, and then click **Search**.
   RESULT: The qualified policy is displayed in the Search Results area.
   c. Click the hyperlink of the target policy.

2. On the Receive Counter Collection - NB Collection page, enter the collection details.
   a. View proposal/policy basic information which is automatically displayed in the Proposal/Policy Basic Information area.
   b. In the Receive Collection area, select a currency from the **Collection Currency** drop-down list and view the exchange rate that is automatically displayed in the **FOREX Rate** field.
   c. In the **Amount** textbox, enter the collection amount.
   d. In the **Collection Method** field, enter the collection method code, or double-click the field to select a code.
   e. Adjust Bank Account and Collection Date if necessary, or leave the default values unchanged.
   f. Set Bank Code, Cheque No., Bank Account, Cheque Due Date, Collection Date, and Source as required.
   g. Click **Add**.
   RESULT: The system conducts the conversion automatically and the collection record is listed below.
   h. Repeat Step b to Step g to add other collection records.

3. Allocate collection.
   a. Click **Allocate**.
   RESULT: The total amount collected is displayed in the **Amount Collected** field.
   b. For the payment method of C (cash) or K (cheque), enter the Temporary Receipt Number.

**Tutorial Information:** A dialog box is displayed, asking you whether to print receipt or not. Click OK if the receipt is required.

**Post-Allocation Checks:**
- The system checks whether collection needs to be approved (which can be configured).
  - If yes, go to the Collection Approval process.
  - If no, the system checks whether the collected premium is enough to make the policy in force.
    - If yes, the allocation is successful and the policy is in-force.
    - If no, the collected money will be allocated to suspense.

### 4.2 Counter Collection for Customer Service

1. From the main menu, select **Billing/Collection/Payment > Collection > Receive Counter Collection**.

2. On the Receive Counter Collection page, select **CS Collection**, set the search criteria and then click **Search**.
   RESULT: The selected policy is displayed in the Receive Counter Collection - CS Collection page.

3. In the Receive Collection area, enter the collection details.
   a. Specify Collection Currency from the drop-down list.
   b. Specify collection amount in the **Amount** textbox.
   c. Enter the Collection Method code or double-click the Collection Method to select a collection method from the Search Code page.
   RESULT: The selected method is loaded to the Collection Method field automatically.
   d. Enter Bank Code, Cheque No., Bank Account, Collection Date, Cheque Due Date, and Source as required.
   e. Click **Add** to add a new collection record to the list below.

4. Collection records.
   - All collection records are displayed in the Collection Records area.
   - Click **Policy Collection** to view the policy details.
   - Click **Premium** to view the premium details.
   - Click **Single Draw Next Installments**.

**Single Draw Next Installments:** You can trigger a single draw if collecting monies in advance for renewal premium or recurring top-ups. For single draw cases, you will need to perform the single draw before you carry out the Collection Allocation.

The single draw function is to be used for premiums collected with more than 30 days lead days. With the single draw, a billing record will be created and the amount collected will go to the Renewal Suspense. If no draw is done, the amount collected will go to General Suspense instead.

   a. Click **Single Draw Next Installments** to open the Extraction of Amount to Bill (Single)-Extraction page.
   b. Specify the **Extraction Date** (MMYYYY), the month in which you wish to create the billing record, via the Calendar control.
   c. Click **Submit** to submit the extraction request. Once successfully completed, the system should display a message **Extraction succeeded!**.
   d. Click **Back** to return.

5. Click **Allocate** to allocate the collection received.
   RESULT: The allocated amount will be displayed in the Collection Allocation area.

6. For the payment method of C (cash) or K (cheque), enter the Temporary Receipt Number.

7. Click **Submit**.
   RESULT: After checking the validity of the collection allocation details, the system will complete the allocation operation.

8. On the print receipt window displayed, click **OK** to print the receipt if the receipt is required.

### 4.3 Counter Collection for Miscellaneous Fee

Miscellaneous Fee Collection includes collections of stamp duty, service tax, overdue interest, etc.

1. From the main menu, select **Billing/Collection/Payment > Collection > Receive Counter Collection**.

2. On the Receive Counter Collection page, select **Misc Fee Collection**, set the search criteria and then click **Search**.
   RESULT: The qualified Policies are displayed in the search results area.

3. Click the hyperlink of the desired policy.
   NOTE: The policy basic information is read-only.
   RESULT: The related information is displayed on the Receive Counter Collection - Miscellaneous Collection page.

4. In the Receive Collection area, enter the collection details.
   a. Specify Collection Currency from the drop-down list, for example, SGD.
   b. Specify collection amount in the **Amount** textbox.
   c. Enter the Collection Method code or double-click the Collection Method to select a collection method from the Search Code page.
   NOTE: For bulk collection transactions, it is better to adjust the default settings in Change Bank Account and Collection Date to save efforts.
   RESULT: The selected method is loaded to the Collection Method field automatically.
   Once the Collection Method is selected, the system should display the default Bank Account and Collection Date. You can adjust the values via the drop-down list and calendar control as desired.
   d. Enter Bank Code, Cheque No., Bank Account, Cheque Due Date, and Source as needed, based on the collection method defined above.
   e. Click **Add** to add a new collection record to the list below.

5. In the Collection Allocation area, enter the amount collected for each collection type.

6. For the payment method of C (cash) or K (cheque), enter the Temporary Receipt Number.

7. Click **Submit**.
   RESULT: After checking the validity of the collection allocation details, the system will complete the allocation operation.

8. On the print receipt window displayed, click **OK** to print the receipt if the receipt is required.

### 4.4 Change Bank Account and Collection Date

This topic tells how to update the default bank account and collection date used for counter collection. This is applicable in situations to perform bulk collection transactions on behalf of another branch or collecting bank or when bulk backdated collections need to be made, so that you would not perform the update on a per-record basis. This function is for Traditional, investment linked and A&H Policies for insurance company.

1. From the main menu, select **Billing/Collection/Payment > Collection > Update Bank Account and Collection Date**.
   RESULT: The Update Bank Account and Collection Date page is displayed.

2. Select the required **Bank Account** from the drop-down list and adjust the **Collection Date** by using the Calendar Control.
   NOTE: Only cash accounts are available in Bank Account drop-down list.
   NOTE: The updated Collection Date will not be displayed on current page only if the collection method is selected, otherwise, it still displays the system date.

3. Click **Submit** to update the default settings.
   NOTE: A daily end-of-day job will reset the default bank account to the particular cashier's branch collection account, and the default collection date to the current system date.
   RESULT: Once submitting successfully, the system should display a message saying: **Update successfully!**

### 4.5 Approve Collection

When you need to approve or reject the collection that has gone through the main counter collection process, do as follows.

The Collection approval requirement is configured in the rate table. For detail information about the configuration, please refer to System Configuration Guide.

1. From the main menu, select **Billing/Collection/Payment > Collection > Approve Collection**.

2. Search out the target collection record.

3. Check the collection information and make your decision.
   - Click **Approve** to accept the collection.
   - Click **Reject** to reject it.

---

## 5. Direct Debit Collection

On scheduled date, the system should generate Pre Direct Debit Notice and sends it to Policyholder. So that Policyholder can deposit sufficient amount in the corresponding bank account beforehand. After a given period, the system should extract policies to perform calculation and calculate amount to bill. Or user can manually perform bank transfer extraction to extract bank transfer file. The information will be saved. Then user can go to Download Direct Debit Bank File module to download the Direct Debit file and send it to bank for the payment deduction. After the bank processes the file and returns the file, user can go to Upload Direct Debit Bank File module to upload the Direct Debit file. And then the system will verify the data.

**Prerequisites:**
- Bank Transfer Files' (both Transfer Generation File and Transfer Return File) formats have been defined in system. See Bank Transfer in LifeSystem System Configuration Guide for details.
- The direct debit card is in Authorized status. For details, see Bank Account Authorization.

### 5.1 Extract Bank Transfer File

1. From the main menu, select **Billing/Collection/Payment > Billing > Electronic Collection > Bank Transfer > Bank Transfer Extraction**.
   RESULT: The Bank Transfer Extraction page is displayed.

2. Set search criteria and click **Search**.
   NOTE: On the page displayed, select a bank and card type, select business types. You cannot select collection and payment business types at the same time.
   RESULT: The bank transfer record is displayed in the Search Result area.

3. Select the target record(s) and click **Submit**.

### 5.2 Download Direct Debit Extraction File

1. From the main menu, select **Billing/Collection/Payment > Billing > Electronic Collection > Bank Transfer > Download Bank File**.
   RESULT: The Download Bank File page is displayed.

2. Specify the **Generation Date** via calendar control and enter the **Bank Code**.

3. Click **Download** to download the file.
   NOTE: Then send the file to the bank.

### 5.3 Upload the Returned File

1. After the file is processed and returned from the bank, go to **Collection/Billing/Payment > Billing > Electronic Collection > Bank Transfer > Upload Bank File**.
   RESULT: The Upload Bank File page is displayed.

2. On the Upload Bank File page, enter the batch number and click **Browse** to localize and select the local-saved return file.
   RESULT: System captures the data on file and confirms the collection from client.

---

## 6. Credit Card Collection

**Prerequisites:**
- Bank Transfer Files' (both Transfer Generation File and Transfer Return File) formats have been defined in system. See Bank Transfer in LifeSystem System Configuration Guide for details.
- The direct debit card is in Authorized status. For details, see Bank Account Authorization.

### 6.1 Extract Bank Transfer File

1. From the main menu, select **Billing/Collection/Payment > Billing > Electronic Collection > Bank Transfer > Bank Transfer Extraction**.
   RESULT: The Bank Transfer Extraction page is displayed.

2. Set search criteria and click **Search**.
   NOTE: On the page displayed, select a bank and card type, select business types. You cannot select collection and payment business types at the same time.
   RESULT: The bank transfer record is displayed in the Search Result area.

3. Select the target record(s) and click **Submit**.

### 6.2 Download Credit Card Extraction File

1. From the main menu, select **Billing/Collection/Payment > Billing > Electronic Collection > Bank Transfer > Download Bank File**.
   RESULT: The Download Bank File page is displayed.

2. Specify the **Generation Date** via calendar control and enter the **Bank Code**.

3. Click **Download** to download the file.
   NOTE: Then send the file to the bank.

### 6.3 Upload the Returned File

1. After the file is processed and returned from the bank, go to **Collection/Billing/Payment > Billing > Electronic Collection > Bank Transfer > Upload Bank File**.
   RESULT: The Upload Bank File page is displayed.

2. On the Upload Bank File page, enter the batch number and click **Browse** to localize and select the local-saved return file.
   RESULT: System captures the data on file and confirms the collection from client.

---

## 7. Lock Box Collection

This section describes how LifeSystem processes the lockbox file from collecting banks by batch.

**Prerequisite:** The payment file from the bank is received.

After receiving the file from the bank, you should upload it to LifeSystem via Upload Lockbox and E-bank File.

1. From the main menu, select **Collection/Billing/Payment > Billing > Electronic Collection > Upload LockBox and Ebank File**.
   RESULT: The Upload Lockbox And E-Banking File page is displayed.

2. Select a file type from the **File Type** drop-down list and enter the batch number in the **Batch No.** textbox.

3. Click **Browse** to select the file you want to upload.

4. Click **Validate** to check the correctness of the Batch No., Source, and File format.
   RESULT: If the system validation is successfully, each transaction record is processed.
   - The system should update payable record status to reflect successful deductions.
   - The system tags the policy so that a receipt will be generated for the case at the end of the day.
   - System tags the policy for inclusion in the end-of-day suspense report if any monies have dropped into the respective suspense accounts (policy collection suspense, renewal suspense or general suspense).

5. Click **Submit**.

---

## 8. Cancel Collection

Cancel Collection allows you to cancel collections online for all types of collection methods (including dishonored cheque) for Traditional, ILP and A&H Policies for insurance company.

Cancel Collection is only for the collection records that have not been applied. Once the collection is applied, you need to enter the Reverse Inforce (for NBU inforce transaction) or Reverse Alteration (for renewal or CS transactions) to cancel the business activities, and the corresponding financial records will be reversed accordingly.

**Prerequisites:**
- The policy status is Inforce.
- The collection records have not been applied.
- The policy has collection records.

1. From the main menu, select **Billing/Collection/Payment > Collection > Cancel Collection**.
   RESULT: The Cancel Collection page is displayed.

2. Set the search criteria and click **Search**.
   RESULT: The qualified records are displayed in the search results section.

3. Click the hyperlink of the target policy to load the details.
   RESULT: The Cancel Collection - Update page is displayed. All collection records are displayed in the Cancel Collection section.

4. Click the checkbox next to the required collection records.

5. Specify the **Cancel Type** and **Cancel Reason** (if applicable).

6. Click **Submit** to submit the cancellation request.
   RESULT: The system should cancel the collection records based on the rules and display a message **Cancel collection is successful!**

**Cancel Type Options:**
- Incorrect Amount
- Cancellation of Application
- Dishonoured Cheque
- Others

**Cancel Reason Options:**
- Premium payment received
- Policy surrendered
- Policy lapsed
- Others (free text)

---

## 9. Perform Waiver

Perform Waiver allows you to waive interest for APL, policy loan and study loan, as well as to waive service tax, alteration/policy fee, switching fee, miscellaneous fee, overdue interest, stamp duty and benefit card. This function is for Traditional, ILP and A&H Policies for insurance company. Once a waiver amount has been submitted and confirmed, the system will create a collection record for the amount waived.

**Notes:**
- You should perform the waiver update only if you intend to waive the full amount.
- If you intend to perform partial waiver, you should wait till you have received the money (with partial interest) from the Policyholder/Life Planner, before you perform the waiver. When the money has been received, you can update the money received under Receive Counter Collection UI and then perform the waiver, or perform the partial waiver and then update the money received under Receive Counter Collection UI.

**Prerequisite:** There should be records under the policy to be performed.

1. From the main menu, select **Billing/Collection/Payment > Collection > Perform Waiver**.
   RESULT: The Perform Waiver page is displayed.

2. Set search criteria and click **Search**.
   RESULT: The qualified records are displayed in the search results section.

3. Click the hyperlink of the target policy.
   RESULT: The Perform Waiver - Update page is displayed. There are two areas on the page:
   - One is **Policy Information** area where you can get the basic data of the policy. It is read-only.
   - The other is **Transfer area** where you can perform the transfer.

4. Select the records need to be waived and enter the waiver amounts.

5. Click **Submit** to submit the waiver request.

---

## 10. Transfer and Apply Suspense to Other Account

Transfer and Apply Suspense into Other Account allows you to transfer monies between different suspense accounts (Policy Collection, Renewal and General) for insurance company. You can also transfer monies from/to suspense accounts to/from Advance Premium Account (APA), Policy Loan, Study Loan, Automatic Premium Loan (APL), Survival Benefit and Cash Bonus accounts.

**NOTE:** NB proposals do not have APA, Policy Loan, APL, Survival Benefit, Cash Bonus, etc and, therefore, NB proposals will not be handled under this function.

1. From the main menu, select **Billing/Collection/Payment > Collection > Transfer and Apply Suspense into Other Accounts**.
   RESULT: The Transfer and Suspense into Other Accounts page is displayed.

2. Set search criteria and click **Search**.
   RESULT: The qualified records are displayed in the search results section.

3. Click the hyperlink of the target policy.
   RESULT: The Perform Waiver - Update page is displayed.

4. Complete suspense transfer information on the details page.
   a. Pick a **Transfer Effective Date** using the calendar control.
   NOTE: By default, it is the current system date.
   b. Enter the amount to be transferred from the source account in **Bal Trf fm**.
   c. Enter the amount to be transferred to the target account in **Bal Trf to**.
   NOTE: The sum of Bal Trf to should be equal to Bal Trf fm.

5. Click **Submit** to submit the transfer request.

---

## 11. Upload Batch Collection

Uploading batch collection allows you to upload the returned file that may contain multiple collection records into system, in situation where returned file is the only requirement. This happens when insurer chooses to use the following 4 collection methods:
- Bank's Order
- Lock box
- Banking
- Cash

After uploading the returned file, system generates collection records for the matched collection and continues with the business transaction (e.g. policy issue, renew confirmation, loan repayment, CS inforce, Premium Allocation, etc).

**Prerequisites:**
- Policy status is Accepted or Inforced.
- The returned file must be in a defined format.

**Sample file format:**

```
"1", "0001391285", "Andy", "SGD", "2000.00", "description", "501-009492-201", "7339-OVERSEAS-CHINESE BANKING CORPORATION"
"2", "0001391285", "Hancel", "SGD", "6000.00", "description", "501-009492-202", "7339-OVERSEAS-CHINESE BANKING CORPORATION"
"3", "0001391285", "Kaity", "SGD", "5000.00", "description", "501-009492-203", "7339-OVERSEAS-CHINESE BANKING CORPORATION"
```

**Field Descriptions:**

| Field Name | Sample | Description |
|-----------|--------|-------------|
| Serial Number | "1" | Serial number of this collection, such as 1, 2, 3, etc. |
| Policy Number | "0001391285" | Policy number of this collection. |
| Account Owner Name | "Andy" | Owner name of the account to receive this collection. |
| Currency | "SGD" | Available currency codes, such as CNY, USD, and SGD. |
| Collection Amount | "2000.00" | Total amount of this collection. |
| Remark | "description" | Short description about this collection if you have any. |
| Bank Account Number | "501-009492-201" | Bank account number of collection owner. |
| Bank Name | "7339-OVERSEAS-CHINESE BANKING CORPORATION LTD(OCBC)" | Name of bank that owns the account. |
| Collection Method | "Cash" | Currently supports: Bank's Order, Lock box, Banking, Cash. Any other collection method will cause the record to be unmatched. |
| Collection Date | "18/04/2013" | The collection date. Format: DD/MM/YYYY. If the date filled does not comply with the real time, system will take the real time by default. |
| Collection Owner Name | "org-test24" | Short name or name of the collection owner, such as insurance company. |
| Receipt Number | "0001391285" | Receipt number of collection. |

1. Prepare the returned file of collection in a defined format (see sample above).

2. From the main menu, select **Billing/Collection/Payment > Collection > Batch Upload Collection**.
   RESULT: The Batch Upload Collection page is displayed.

3. Select the **bankCode** from the drop-down list.
   NOTE: The bank related information can be configured in Configuration Center > Finance Configuration > Bank > Maintain Bank Account.

4. Click **Browse** to select one returned file of collection that you have prepared.

5. Click **Submit** to upload the file into the system.

6. Check if the triggered batch is executed successfully after uploading collection:
   a. On the Batch Upload Collection page, click **Query Job Status**.
   RESULT: The User Job Monitor page is displayed.
   b. Input the Search Criteria and check the result.
   NOTE: The job status **Execute Success** indicates that this triggered batch is executed successfully.

---

## 12. Manage Unmatched Collection Records

Some of the uploading collection records are un-matched. In this case, user can re-match or remove it from the system, and also download a list of all un-matched collection records in an excel file.

**Prerequisite:** The un-matched collection records exist in system.

### 12.1 Re-match the Un-Matched Collection Records

1. From the main menu, select **Billing/Collection/Payment > Collection > Manage Unmatched Collection**.
   RESULT: It displays the Manage Unmatched Collection page.

2. Search out the un-matched collection records.

3. In **Collection Records** field, select **Match Record**.

4. Select the check-box before the record that you want to re-match.

5. In **Match to policy No.**, type in the policy number that you want to re-match collection for.

6. Click **Submit**.

### 12.2 Remove the Un-matched Collection Records

1. From the main menu, select **Billing/Collection/Payment > Collection > Manage Unmatched Collection**.

2. Search out the un-matched collection records.

3. In the **Collection Records** field, select **Remove Record**.

4. Select the check-box before the record that you want to remove.

5. Click **Submit**.

### 12.3 Download All of the Un-matched Collection Records

1. From the main menu, select **Billing/Collection/Payment > Collection > Manage Unmatched Collection**.

2. Click **Download**.

3. In the pop-up dialog window, click **Save**.

4. Specify the location and click **OK**.
   RESULT: All of the un-matched collection records are outputted into an excel file and saved under the location that you specified.

---

## 13. Manage Cash Totalling

Manage Cash Totaling allows you to perform cash totaling for the day for Traditional, ILP and A&H Policies for insurance company. The system will retrieve the collection summary records for each collection method for the current Cashier. Once the cash totalling has been submitted and confirmed, the system will commit all collection records for the day.

**Prerequisite:** There are collection records existing for the day.

1. From the main menu, select **Billing/Collection/Payment > Collection > Manage Cash Totalling**.
   RESULT: The Manage Cash Totalling - Summary page is displayed.

2. Set search criteria and click **Search**.
   RESULT: The summary records are displayed in the search results section. The total amount of all collections, belonging to the current cashier, under each collection method is summarized.

3. Click the hyperlink of certain collection method to view the collection details under that collection method.
   RESULT: The Manage Cash Totalling - Detail page pops up.
   NOTE: Click **Exit** to close the current page.

4. Click **Submit** to submit the cash totalling records.
   RESULT: A dialog box is displayed, requesting you to confirm clearing cash totalling.

5. Click **OK**.
   RESULT: After submitting the cash totalling records, the system should zeroize the collection records and display a message **cash totalling successfully**.

---

## 14. Bank Account Authorization

Below is the workflow of bank account authorization.

**Prerequisite:** N/A

1. After receiving the Bank Transfer Authorization Form, the Back Office staff enters or changes bank account information in the System.
   NOTE: The back office staff can enter bank account information in Maintain Party - Bank Account and NBU Data Entry - Select Payment Method; they can change bank account information in Maintain Party - Bank Account and CS Alteration - Change Payment Method.

2. The System checks whether the new added or modified bank account needs authorization or not.
   - If no, the System sets the bank account's Authorization Status to **Authorized**.
   - If yes, the System sets the bank account's Authorization Status to **Waiting for Authorization**.
   NOTE: For details about the Authorization Status field, refer to A.6 Payment Method Information Page in New Business User Manual.

3. On the scheduled date, the System starts a batch to extract all bank accounts in Waiting for Authorization status and sets all extracted bank accounts' Authorization Status to **Authorization In Progress**.

4. After batch extraction, the Back Office staff downloads the bank account authorization file online and sends it to bank for process.
   a. From the system main menu, select **Billing/Collection/Payment > Billing > Electronic Collection > Bank Transfer > Download Bank Authorization File**.
   RESULT: The Download Bank Authorization File page is displayed.
   b. Select a **Bank Code** and **Account Type** (Direct Debit or Credit Card), and click **Search**.
   RESULT: Records that match the search criteria are displayed in the Search Result area.
   c. Select the target record(s) and click **Download**.
   d. (Offline) The Back Office staff sends the authorization file to corresponding bank(s).

5. After bank(s) finishes processing the authorization file and returns the processed file, the Back Office staff uploads the authorization file online.
   a. From the system main menu, select **Billing/Collection/Payment > Billing > Electronic Collection > Bank Transfer > Upload Bank Authorization File**.
   RESULT: The Upload Bank Authorization File page is displayed.
   b. Select a **Bank Code** and **Account Type** (Direct Debit or Credit Card) and click **Search**.
   RESULT: Records that match the search criteria are displayed in the Search Result area.
   c. Select a target record.
   d. In the **Upload Information** area, click **Browse** to locate a returned authorization file on local disk and click **Upload**.
   RESULT: The authorization result is uploaded and waiting for further process by the System.

6. The System verifies authorization result in the uploaded authorization file.
   - If a bank account is authorized by the bank, the System sets the bank account's Authorization Status to **Authorized**.
   - If a bank account is not authorized by the bank, the System sets the bank account's Authorization Status to **Rejected**.
   Only bank accounts in **Authorized** status are accepted for Credit Card Collection or Direct Debit Collection. Bank accounts in **Rejected** status will cause collection failure.

### 14.1 Bank Account Authorization File Format

**Download bank file format — For Credit Card:**

| Field |
|-------|
| Credit Card Type |
| Credit Card No. |
| Expire Date |
| Account Holder's Full Name |
| Account holder's ID |
| Account holder's DOB |
| Account holder's mobile phone |
| Extraction date |

**Download bank file format — For Debit Card:**

| Field |
|-------|
| Account No. |
| Account Holder's Full Name |
| Account holder's ID |
| Account holder's DOB |
| Account holder's mobile phone |
| Extraction date |

**Upload bank file format — For Credit Card and Debit Card (both):**

| Field |
|-------|
| Account No. |
| Account holder full name |
| Validation result (Y, N) |
| Failure reason |

NOTE: Validation result Y means authorized, N means rejected.

---

## 15. Create or Modify Loan Repayment Schedule

User can create a new loan repayment schedule or modify an existing one. This is for the purpose of loan repayment by Direct Debit and Credit Card. User can edit the following repayment schedules for a specified policy:
- Policy loan repayment schedule
- APL repayment schedule

**Prerequisites:**
- The policy is inforce.
- User performed Apply Policy Loan to the policy. See Apply Policy Loan in Customer Service User Manual.
- Pay mode is DDA or Credit Card.

1. Search out the policy for whom the repayment schedule needs to be created or modified.
   a. From the main menu, select **Billing/Collection/Payment > Collection > Create or Modify Loan Repayment Schedule**.
   RESULT: The Create or Modify Loan Repayment Schedule page is displayed.
   b. Enter the target policy number and clicks **Search**.
   RESULT: The qualified policy is displayed in the Search Results area.

2. Select the target record and enter loan repayment schedule details for the policy, like **Repayment Start Date**, **Repayment Frequency** and **Repayment Amount**.

3. Click **Submit**.
   RESULT: System updates the Policy Loan or APL repayment schedule details for the specified policy.

---

## 16. Update Premium Voucher Details

This topic describes how to update premium voucher details. The user can key in the amount, the policy that the premium voucher used, as well as to view the current premium voucher balance.

**Prerequisites:**
- The product is applicable with premium voucher, and its percentage of sum assured of this product is defined.
- The premium voucher indicator is issued in NB.

1. From the main menu, select **Billing/Collection/Payment > Collection > Update Premium Voucher Details**.
   RESULT: The Update Premium Voucher Details page is displayed.

2. Enter the **Policy No.**, and click **Search**.
   RESULT: The target policy with **Available Premium Voucher Balance** amount is displayed.

3. Set **Premium Voucher Utilized** to Y, and then fill in the **Target Policy** and **Amount Utilized** information.
   NOTE: The amount of Amount Utilized should be less than Available Premium Voucher Balance.
   - Or Set **Premium Voucher Utilized** to N.

4. Click **Submit**.
   RESULT: Once submitting successfully, the system should display a message saying: **Update Premium Voucher successfully!**

---

## 17. Lock and Unlock Suspense Refund

This topic describes how to lock and unlock general suspense refunds for both online and batch, policy collection, and renewal suspense refunds (batch only).

1. From the main menu, select **Billing/Collection/Payment > Collection > Lock and Unlock Suspense Refund**.
   RESULT: The Lock and Unlock Suspense page is displayed.

2. Set the Search criteria and click **Search**.
   RESULT: The matched policy is displayed.

3. Click the hyperlink of the target policy to load the details.
   RESULT: The Lock and Unlock Suspense Refund - Update page is displayed.

4. Click the check box to lock or unlock the suspense refund. Make comments if necessary.

5. Click **Submit**.

---

## 18. Batch Functions

### 18.1 Reset Bank Account and Collection Date for Backdate

This is a daily batch job to reset the system default bank account and collection date for users who changed the default bank account and collection date by Update Bank Account and Collection Date.

**Prerequisite:** The Bank Account and Collection Date has been updated by the user.

**Result:** After executing this batch job, the system successfully resets the default bank account and collection date.

### 18.2 Credit Card Extraction

In this batch job, system will extract all the policies which need collection premium and the payment method is credit card (CC). The system extracts credit card deduction records and subsequently sent via files to the respective credit companies. It covers all traditional, ILP, and A&H policies.

**Prerequisites to compute the deduction amount:**
- Extracted amount to bill (Batch)
- Extracted amount to bill (Single)
- All policy alteration jobs which will trigger an online draw

**Prerequisite to execute loan repayment:**
- Extract Loan Repayment Amount

**Extraction criteria:**
- Policy payment method is credit card.
- Credit card deduction is not suspended.
- Policy status is inforce.
- Country of policy meets extraction criteria.
- Policy type meets extraction criteria.
- Credit card deduction date of policy meets extraction criteria.
- Policy is inforce and benefit premium status is regular.
- Policy is not frozen by Claims.
- For ILP policies, policy does not have Potential Lapse Date or Projected Lapse Date before next due date.
- For ILP policies, the premium holiday indicator is not set.
- The policy does not have premiums paid in advance (excluding premium in suspense).

**Batch Process:**
1. The batch job scheduler triggers a run for credit card extraction.
2. System extracts a list of policies which meet the extraction.
3. System retrieves and consolidates the amount to be included in the credit card deduction file for each extracted policy.
4. System generates the required credit card deduction files for the different acquiring banks in LifeSystem.

**After completing this task:** ISD user can download the credit card deduction files for transfer to the acquiring banks for processing.

### 18.3 DDA Extraction

This topic describes how LifeSystem extracts Direct Debit deduction records by batch. These records will be subsequently sent via tapes or other medium to the respective banks. It will cover the monthly Direct Debit deduction runs in LifeSystem. It covers all Traditional, ILP and A&H policies. The system extracts a list of policies for Direct Debit deductions, retrieves the amount to bill and creates the Direct Debit deduction file.

**Prerequisites to compute the deduction amount:**
- Extracted amount to bill (Batch)
- Extracted amount to bill (Single)
- All policy alteration jobs which will trigger an online draw

**Prerequisite to execute loan repayment:**
- Extract Loan Repayment Amount

**Additional prerequisite:**
- Generate Direct Debit Preliminary Report has been executed for the user to manually amend any records before creation of the deduction file.

**Extraction criteria:**
- Policy payment method is Direct Debit.
- Direct Debit deduction is not suspended.
- Policy status is inforce.
- Country of policy meets extraction criteria.
- Policy type meets extraction criteria.
- Credit card deduction date of policy meets extraction criteria.
- Policy is inforce and benefit premium status is regular.
- Policy is not frozen by Claims.
- Direct Debit deduction date of the policy does not meet extraction criteria.
- For ILP policies, policy does not have Potential Lapse Date or Projected Lapse Date before next due date.
- For ILP policies, the premium holiday indicator is not set.
- The policy does not have premiums paid in advance (excluding premium in suspense).

**Batch Process:**
1. The batch job scheduler triggers a run for Direct Debit extraction.
2. System extracts a list of policies which meet the extraction for inclusion the Direct Debit deduction file.
3. System retrieves and consolidates the amount to be included in the Direct Debit deduction file for each extracted policy.
4. System generates the required Direct Debit deduction files for the different acquiring banks in LifeSystem.

**After completing this task:** ISD user can download the Direct Debit extraction files and send to the bank.

### 18.4 Batch Generate Receipts

This topic describes how the system generates receipts by batch. It covers Traditional, ILP and A&H policies. The system extracts a list of policies for which receipts need to be printed and prints the receipts.

**Prerequisite:** Execute the following steps to receive collections before the associated receipts can be generated:
- Upload Lockbox file
- Upload Credit Card Deduction file

**Batch Process:**
1. The batch job scheduler triggers a run for the batch generation of receipts.
2. System extracts a list of policies for which receipts need to be printed.
   NOTE: If a receipt has already been printed for this policy, then the policy is not extracted.
3. System retrieves and consolidates the data to be printed in the receipt for each extracted policy.
4. System generates the receipts.

---

## 19. Appendix A: Field Descriptions

### Field Descriptions of Download/Upload Bank Authorization File Page

| Field | Description |
|-------|-------------|
| Bank Code/Name | Code or name of the bank. |
| Account Type | Account_type: 8-Credit Card; 2-Direct Debit |
| File Name | File name of the bank authorization file. For example: Bank_code+account_type+extract_date_list_id.txt |

---

## 20. Appendix B: Rules

### Counter Collection for New Business Rules

1. **Collection currency can be different from policy currency.** Multiple currency Over-the-Counter collection rules are as follows:
   - The collection amount user entered is in actual collection currency. System need to convert the collection amount online by using the real time transaction exchange rate.
   - System will check whether there is available transaction exchange rate with effective date the same as collection date. If yes, such rate record will be used to conduct conversion. If not, system will retrieve the latest updated one up to the collection date and display a dialog box for user to confirm. User can click OK to accept it and proceed with the collection, or click Cancel to quit.
     - Formula for currency conversion: Target currency's value = source currency's value * exchange rate
     - Exchange rate can have 8 decimals in the system. Every fund exchange to policy currency for the purpose of getting fund value will be rounded to 2 decimals.
     - Every collection/payment amount for fund will be rounded to 2 decimals. There is no rounding rule when converted to the base currency.
   - If conversion occurred between two foreign currencies, then two conversions are needed.
   - If the corresponding exchange rate is unable to be found out, an error message will be displayed.

2. **When you adjust the collection date:**
   - Forward dating of the collection date is not allowed.
   - Backdating of the collection date is allowed, but the number of days allowed for backdating must be within the user's authority.

3. **Pay source is a mandatory field for counter collection.** Each collection method has a default pay source. When the collection method is selected, the default pay source will be displayed automatically. The matrix between pay source and collection method is as follows:

| Collection Method | Pay Sources | Default Source |
|------------------|-------------|----------------|
| Cash | Cash | Cash |
| Cheque | Cheque | Cheque |
| Direct Debit | Direct Debit Auto Debit | Auto Debit |
| Bank's Order | LLG, RTGS | LLG |
| Lock Box | ATM, RTGS, Internet Banking, LLG, Phone Banking | ATM |
| E-banking | Internet Banking, Phone Banking | Internet Banking |
| Credit Card | Manually swipe, Auto debit | Manually swipe |
| Demand Draft | Manually swipe | Manually swipe |

4. **When you click Allocate:**
   - System allocates the amount collected based on default collection allocation rules and displays the results.
     - If the collected amount is not applied to the Total Inforcing Premium, the default rule is that the amount will be placed under General Suspense.
   - System computes and displays the overdue interest (to-date).
   - For bankruptcy cases, system will check the Bankruptcy Status (at Party level) and the Allow Premium Collection for Bankruptcy indicator to verify that premium can be collected.
     - If Bankruptcy Status (at Party level) = Y, Allow Premium Collection for Bankruptcy indicator = N, and collection method = Cash, NETS, Cheque, Cashier's Order, collection is not allowed.
   - When allocating monies to suspense, if the stamp duty indicator is '1' (Deduct from Suspense):
     - The system calculates the stamp duty amount based on the total collection amount.
     - The amount can be allocated = total collection amount – stamp duty.
     - The system adds the stamp duty suspense for this collection and displays it in UI.
     - The system creates the suspense record for stamp duty amount in t_cash when the collection is submitted.

5. **When you click OK to print receipt:**
   - The date printed on the receipts is the collection date and not the transaction date.

### Counter Collection for Customer Services Rules

1. When the collection method is selected, the system should display the default Bank Account and Collection Date. You can adjust the values via the drop-down list and calendar control as desired.
   NOTE: For bulk collection transactions, it is better to adjust the default settings in Change Bank Account and Collection Date to save efforts.

2. **When you click Allocate:**
   - The system will allocate the collection according to default rules, but you can change Amount Collected if necessary.
     - By default, monies collected are allocated by system in the following order. Each item must be collected fully before allocated to the next outstanding item. Existing suspense balance in the respective suspense type will be considered when allocating. For example, current outstanding policy collection is $100, existing policy collection suspense is $20, system will allocate only $80 to policy collection suspense and the surplus collected will be placed in the next item, that is, to APL if any outstanding APL, or if no APL then to renewal suspense, if no renewal premium is due, then to general suspense.
       a. Policy Collection Suspense (for payment of Admin fees, Miscellaneous Charge, Miscellaneous Interest, Overdue Interest, Stamp duty, Service Tax, Switching Fee - Units, Switching Fee)
       b. APL + APL Interest
       c. Renewal Suspense (for payment of Premium + Service Tax / GST / Stamp Duty where applicable)
       d. General Suspense
       e. APA
       f. Cash Bonus
       g. Survival Benefit
       h. Policy loan
   - The premium is applied and the due date is moved immediately if the policy meets the lead days criteria.
   - You can choose to allocate collected monies to the relevant suspense. For details, refer to Transfer and Apply Suspense to Other Account.
   - When allocating monies to suspense, if the stamp duty indicator is '1' (Deduct from Suspense):
     - The system calculates the stamp duty amount based on the total collection amount.
     - The amount can be allocated = total collection amount – stamp duty.
     - The system adds the stamp duty suspense for this collection and displays it in UI.
     - The system creates the suspense record for stamp duty amount in t_cash when the collection is submitted.

3. **When you click Submit**, the System checks whether all conditions for auto-reinstatement are met:
   a. Policy risk status is lapse
   b. Lapse reason is normal lapse
   c. The latest money received date <= policy lapse date + X days
   NOTE: The System uses the parameter pre-defined in product definition module.
   d. Receive amount >= Reinstatement amount
   If yes, the System automatically performs auto-reinstatement.

4. **When you click OK to print the receipt:**
   - The date printed on the receipts is the collection date and not the transaction date.

5. **Rules after collection:**
   - If monies have been applied successfully for investment linked policy, the system passes the Collection Date and Transaction Time to the ILP module for buying of units according to the 2 pm cut-off rules.
   - For policy loan that has been fully repaid, a letter will be printed to inform the Policyholder a certain number of days from the date of full repayment. This will be generated by a weekly batch job.
   - For insurance company, the system will generate a listing showing outstanding balance of APL and policy loan ≤ $30.
   - The system tags the policy for inclusion in the end-of-day suspense report if any monies have been dropped into the respective suspense accounts.
   - For each premium installment paid, the system will create a premium record to be passed to DCMS for payment of Life Planners' commission at the end of the day.

### Counter Collection for Miscellaneous Fee Rules

1. When you enter the amount collected for each collection type, the sum amounts in the Collection Allocation area must equal the Total Amount in the Receive Collection area.

2. When you click OK to print receipt:
   - The date printed on the receipts is the collection date and not the transaction date.

### Direct Debit Collection Rules

1. **Bank transfer file extraction rules:**
   - **New Business:**
     - Underwriting decision is Accepted or Conditionally Accepted.
     - Policy is not suspended.
   - **Force Billing:**
     NOTE: Force Billing allows user to manually schedule a Direct Debit/Direct Credit and Credit Card Deduction/Refund online for a specific policy on a specified extraction date. Refer to Perform Manual Extraction in Renewal Main Process User Manual.
     - Force billing record exists.
   - **Renew:**
     - ILP: Bank transfer due date < extraction date; Not bank transfer suspend.
     - Traditional: Billing extraction is finished; Billing due date <= extraction date + leading days
   - **Customer Service:**
     - Policy is suspended by customer service.
     - Customer service status is Approve.
   - **Loan Repayment:**
     - Loan repayment schedule batch has run.
     - Due date < deduction date (extraction date)

2. **When generating the bank file**, if the stamp duty indicator is '1' (Deduct from Suspense), the system calculates the stamp duty amount based on the recurring amount, and adds up into the collection amount. The stamp duty amount with fee type will be recorded in the bank file, so it can be deducted correctly when uploaded.

3. **For New Business cases:**
   - If the collected amount is not applied to the Total Inforcing Premium, the default rule is that the amount will be placed under General Suspense.

4. **For Renewal cases:**
   - When uploading the returned files to LifeSystem, system will apply the amount collected to the purpose of deduction. For example, if the record is created for the purpose of renewal, then the money will be applied to renewal premium when it is received.
   - If the amount deducted is not enough to move the due date, for example, due to CS item which causes a change to the premium due amount, the amount deducted will be placed in Renewal Suspense.

5. **When the system confirms the recurring amount:**
   - If the stamp duty indicator is '1' (Deduct from Suspense), the system generates the stamp duty based on the amount already saved in the extraction records, generates the fee record, and generates the cash for stamp duty and offset with the stamp duty AR.
   - If the stamp duty indicator is '2' (Not Deduct from Suspense), the system generates the stamp duty based on the collection amount, and does not deduct the suspense.

### Lock Box Collection Rules

1. **For New Business cases:**
   - If the collected amount is not applied to the Total Inforcing Premium, the default rule is that the amount will be placed under General Suspense.

2. **For renewal cases:**
   - When uploading the returned files to LifeSystem, system will apply the amount collected to Renewal premium if there is a renewal record.
   - If the amount deducted is not enough to move the due date, for example, due to CS item which causes a change to the premium due amount, the amount deducted will be placed in Renewal Suspense.

3. **When you click Submit:**
   - If the stamp duty indicator is '1' (Deduct from Suspense), the system generates the stamp duty based on the amount already saved in the extraction records, generates the fee record, and generates the cash for stamp duty and offset with the stamp duty AR.
   - If the stamp duty indicator is '2' (Not Deduct from Suspense), the system generates the stamp duty based on the collection amount, and does not deduct the suspense.

### Collection Cancel Rules

1. **When you enter the search criteria and click Search:**
   - The transaction period should not be more than one month.

2. **When you select the Cancel Type and Cancel Reason:**
   - If you select Incorrect Amount or Cancellation of Application from the Cancel Type drop-down list, you do not have to specify the cancel reason, as the Cancel Reason field cannot be modified. For Incorrect Amount or Cancellation of Application, no letter is generated to the policyholder.
   - If you select Others from the Cancel Reason drop-down list, there will be a blank space in the Dishonoured Cheque Notification Letter for you to write down the reason manually.
   - Incorrect Amount can be chosen for the Cancel Type field when an incorrect amount was entered, for example, $100 being wrongly entered as $1000.
   - Cancellation of Application can be chosen for the Cancel Type field when the collection was updated into the wrong policy, for example, $1000 being updated into Policy B instead of Policy A. After the collection has been successfully cancelled, the monies will sit in the General Suspense of Policy B.
     - For such a case, if Policy A is under the same legal owner as Policy B, the Cashier will need to inform the relevant users to perform an internal transfer of monies from Policy B General Suspense to Policy A General Suspense via the Perform Payment Requisition UI.
     - If Policy A is not under the same legal owner as Policy B, the Cashier will have to inform the relevant users to perform a workaround to make a payment out of Policy B (by cheque) and perform a new collection into Policy A via the Receive Counter Collection UI.

3. **When you click Submit:**
   - If a cheque is for multiple policies, dishonoring the cheque will reverse the transactions for each policy associated with that cheque. The Cashier will have to perform separate cancellation of collection for each of the affected policies.
   - If a cheque is one part of a multiple (part cash/part cheque) collection, the whole collection will be reversed. The cheque portion will be dishonored while the cash portion will be dropped into General Suspense.
   - Any cancellation of collection that was applied from APA will be placed into the APA account except when the benefit status = lapsed or terminated. For such instances, the APA amount will be placed into General Suspense.
   - If the cancellation of collection results in the reversal of a NB transaction (i.e., the policy turned inforce with collection of the inforcing premium), the system will automatically reverse the policy status and transactions, i.e., move back the due date and undo the inforcing of the policy.
   - If a CS application transaction has occurred (i.e., not included in the list of skipped transactions), the Cashier will need to inform the relevant CS users to perform undo of CS applications first, before returning to the Cancel Collection to perform an undo.
   - If there is a claim event with status not equal to Rejected or Cancelled, for major claims (for example, death and TPD), the Cashier will have to inform Claims users to perform a Cancel Claim first, before returning to the Cancel Collection UI to perform an undo. For minor claims (i.e., not death and TPD), the Cashier can choose to freeze the policy and collect the dishonored amount from the Policyholder. Once the dishonored amount is collected, the policy is unfrozen and no undone is required.
   - If a payment transaction has occurred, the Cashier will need to inform the relevant users to perform Cancel Payment via the Cancel Payment UI with the reason as "Void Payment Requisition". After which, the monies will sit in payable and no payment records will be available. The users will then have to manually perform a payment requisition via the Payment Requisition UI to pay out the monies into suspense.
   - If the stamp duty indicator is '2' (Not Deduct from Suspense), the record can be processed if there is only stamp duty is deducted from the suspense, and the system will generate the negative stamp duty after cancellation. For "bounced cheque" and "human error", the negative cash and negative stamp duty will be generated to cancel the whole collection. For "cancel application", the system will not cancel stamp duty.

### Perform Waiver Rules

When you select the records to be waived and enter the waiver amount on the Perform Waiver-Update page, please note:
- Waiver of overdue interest is not allowed.
- The waiver amount must be more than zero.
- For interest charging accounts, the waiver amount should be less than the sum of past interest and current interest.
- For non-interest charging accounts, the waiver amount should be less than the principal balance.
- The waiver amount should not exceed user's authorized limit.

When you click Submit, the system checks the validity of the data and prompts message **Perform waiver successfully!**
- You can select multiple records which require waiver, to be submitted in a single submission. Additionally, the waiver reason being specified for the single submission will be tied to all the records that are being waived in the single submission.
- You can waive either the partial amount or the full amount.
- For full waivers, the waiver amount (insurer payment record) would be performed and applied online immediately. It would not wait till the end-of-day waiver batch to trigger the waiver amount offsetting.
- For partial waivers, the waived amount will be placed in General Suspense for waivers pertaining to policy alterations.
- You will need to select the record to be waived before the Waiver Amount field will become updatable for you to enter the amount to be waived.
- If you select Others from the Waiver Reason drop-down list, the Reason Description field will become updatable for you to enter free text.
- The types of waiver include:
  - For renewal: overdue interest, stamp duty, service tax
  - For policy alteration: alteration/policy fee, switching fee, benefit card, policy loan, APL, study loan, overdue interest
  - For NB: miscellaneous fees (other than overdue interest)
- The conditions for waiver include:
  - For Interest charging accounts, the waived amount entered must be ≤ Past interest + Current interest.
  - For Non-Interest charging accounts, the waived amount entered must be ≤ Principal Balance.
  - For NB waiver of miscellaneous fees (other than overdue interest), the proposal status must be Accepted or Conditionally Accepted.
  - For CS waiver of overdue interest, the policy status must be Lapsed or Inforce.

### Transfer and Apply Suspense to Other Account Rules

When you transfer suspense to other accounts, please note the following rules:
- Each user will have an authorized limit for transfer of suspense.
- Transfer of suspense to/from Cash Bonus and Survival Benefit for CPF policies cannot be performed.
- When transferring suspense, distinction must be made between CPF and non-CPF balances.
- Transfer of suspense will always be from one to many accounts and not many to many accounts.
- If there is a lock on refund from General Suspense, then monies cannot be moved from General Suspense to other types of suspense, for example, Policy Collection and Renewal Suspense.
- If monies have been transferred to Renewal Suspense, the system will attempt to move the due date online via the Renewal Batch job.
- For display of interest bearing/charging account balances, the interest will be calculated up to the current system date and displayed as a total figure with the principal sum. This applies to accounts such as APA, APL, Policy Loan, Study Loan and Survival Benefit/Cash Bonus all options (except Option 1) that attract interest.
- For policy loan that has been fully repaid, a letter will be printed to inform the Policyholder a certain number of days from the date of full repayment. This will be generated by a weekly batch job.
- For insurance company, the system will generate a list showing outstanding balance of APL and policy loan ≤ $30.

### Manage Cash Totalling Rules

When you click OK:
- The system will generate the banking in slip number for each collection record.
- Once a group of collection records has been submitted for cash totalling during the day, the system will zeroize the records and you will not be able to view the records online anymore.
- However, you may generate a cash totalling report at any time during the day via the Report Module. The report will show the cumulative collection records which have been submitted from the start of the day until that point in time. At the end of the day, the same report can be generated to reflect all the collections done for the day.
- In eBaoTech LifeSystem, cash totalling is done by Cashier ID. For insurance company, Cashiers who are on-duty at Head Office for part of the day, before going to the service centers for back-up duty, must submit their cash totalling separately (i.e., clear their cash totalling for the Head Office collections, before proceeding to perform collections at the service centers, and vice versa).
- For example, if a Cashier performs collections at Head Office for part of the day, they should perform cash totalling and generate the cash totalling report, before proceeding to perform collections at the service centre. At the end of the day, the Cashier should perform a 2nd cash totalling and generate the cash totalling report, which will reflect their collections for the entire day.
- A batch job will also be executed at the end of the day to print the total collection for the day, i.e., the total amount would include the amounts collected by the Cashier at Head Office and at the service centre.
- For cancellation of collections:
  - If collection is cancelled within the same day, the system tracks it as an Internal Transfer and it will not be reflected in the end-of-the-day cash totalling report. For example, if there are a total of 10 transactions but 1 collection was cancelled on the same day, the report will reflect only 9 records.
  - If the cancellation of collection is done for a collection on the previous/past day, the system tracks it as an Internal Transfer and it will not be reflected in the end-of-the-day cash totalling report. For example, if there are a total of 10 transactions for the day but 1 collection was cancelled for the previous day, the report will reflect 10 records.

### Bank Account Authorization Rules

1. **Rules in downloading bank authorization file:**
   a. Extraction batch will extract all records with 'Authorization Status' = 'Waiting for authorization', including that of all individuals (inclusive of producers) and organizations (exclusive company organization).
   b. After extraction, system will generate one File Name including all extraction records. The extraction records' 'Authorization Status' will be updated from 'Waiting for authorization' to 'Authorization In Progress'.
   c. From download UI, user can enter the bank code and account type to perform search and find the File Name, system will validate if Bank code and card type is empty. If any of the field is empty, system will prompt error message 'Please select {Field Name}'.
   d. If validate passed, system will list all the files as generated by the extraction batch. If no file is found, the search result is empty.
   e. User can select a record to download, system will prompt dialog for users to select the destination to save the file. If no file is selected, system will prompt error message 'Please select a file'.

2. **Rules in uploading bank authorization file:**
   a. When user click search, system will validate if Bank code and card type is empty. If any of the field is empty, system will prompt error message 'Please select {Field Name}'.
   b. Only the files have been downloaded and not been uploaded will be search out. If no file is found, the search result is empty.
   c. User can select a record to upload, system will prompt dialog for users to select the destination to save the file. If no file is selected, system will prompt error message 'Please select a file'.
   d. System need check if the total record numbers in the upload file is same with download file, if not, the upload process ends and system need pop up error message: **'Upload unsuccessful, because the total numbers in this upload file is different with download file.'**
   e. If the total record numbers is same with download file, then system need match the records in upload file with download file (use File Name to match download file and upload file):
     - For records that are uploaded successfully: For the records in upload file and also in the download file (records successfully uploaded), system will update Authorization Status from 'Authorization in Progress' to 'Authorized' or 'Rejected'.
     - For records that failed to be uploaded: For the records in download file, but not in upload file (records not uploaded due to failure), system will update Authorization Status from 'Authorization in Progress' back to 'Waiting for Authorization'. (So these records can have chance to be extracted again by batch.)
     - For the records in upload file, but not in download file, system will not process these records.
   f. After upload completed, system will provide message for user to indicate the number of successful records and failed records.
     Example: Download file with 5 records (Account A, B, C, D, E); Upload file with 5 records (Account A: Authorized, Account B: Rejected, Account F, Account G, Account H).
     - System updates Account A → 'Authorized'.
     - System updates Account B → 'Rejected'.
     - System updates Account C, D, E from 'Authorization in Progress' → 'Waiting for Authorization'.
     - System takes no action for Account F, G, H.
     Frontend UI message: **"2 records are uploaded successful. 3 records are uploaded fail and still waiting for authorization."**

### Create or Modify Loan Repayment Schedule Rules

1. **Eligibility check imposed upon entry to this function:**
   - Policy status must be inforce.
   - There is an existing loan, or APL on the policy.
   - Policy payment method is bank transfer or credit card.
   - Loan account balance (policy loan, APL or study loan) must be > 0.
   - Cannot change repayment schedule if direct debit tape or credit card file has been sent to bank and has not come back (blackout period).

2. **System performs the following validation:**
   a. Loan repayment method will be set to be the same as policy payment method.
   b. Loan repayment start date:
     - For policies with non-regular premium status, system defaults to system date but this can be forward dated.
     - For policies with regular premium, system defaults to Next Due Date but this can be forward dated.

3. **System performs the following validation when Save information:**
   - Loan repayment start date is aligned with a premium due date (for regular premium benefit only).
   - Loan repayment start date is not less than policy commencement date.
   - Loan repayment start date is not greater than policy expiry date.
   - There is no check on loan repayment frequency. Loan repayment frequency for policy loan, APL can be different. Loan repayment schedule also need not follow the policy payment frequency.
   - Policy loan also applies to single premium policies. For single premium policies, loan repayment start date need not be aligned to a premium due date (since there is no due date for single premium policies).

### Update Premium Voucher Rules

1. **When you enter the search criteria and click Search**, the system will check if any records match the search criteria.
   - If policy does not have a premium voucher, system will prompt error message.
   - The system will show the record if exists.

2. The **Premium Voucher Utilized** indicator can be set to Y or N:
   - If premium voucher utilized indicator is Y, this figure is 0.
   - If premium voucher utilized indicator is N, this figure is calculated based on dollar per thousand of sum assured.
   NOTE: Product setup has catered for available premium voucher balance based on dollar per thousand of sum assured.

3. **If user selects to change premium voucher utilized indicator from N to Y**, the user needs to enter:
   - Target policy number
   - Amount of premium voucher utilized
   
   Upon user submitting the change, system performs the following validation checks:
   - Target policy number is valid. If not valid, system will prompt an error message.
   - Source policy status is inforce. If not inforce, system will prompt an error message.
   - Source policy has no APL balance. If APL balance exists, system will prompt an error message.
   - Source policy main benefit has no claim. If main benefit has a claim, system will prompt an error message.
   - Source policy premium benefit status is regular. If not regular, system will prompt an error message.
   - Source policy main benefit has not been converted to Reduced Paid-Up. If converted, system will prompt an error message.
   - Source policy main benefit has not been converted to ETA. If converted, system will prompt an error message.
   - Amount of premium voucher utilized (keyed in by user) is not greater than the available premium voucher balance. If greater, system will prompt an error message.

4. **If user selects to change premium voucher utilized indicator from Y to N:**
   - System will nullify the target policy number and amount of premium voucher utilized when user submits the change.
   NOTE: Upon modification, the system will auto update the information (fields for 'Available PV Amount' and 'PV utilized for Policy Number') to the PV information under Query Screen as well.

### Lock and Unlock Suspense Refund Rules

When you click Submit, system saves the lock and unlock suspense refund information:
- The lock applies to all monies that reside in a suspense account (i.e. there is no partial locking of monies within general suspense account allowed). If money was collected subsequently into a general suspense account, it will be locked as well.
- If the lock and unlock suspense refund indicator is checked:
  - Subsequent auto batch refund and manual refunds of monies in general suspense will be disallowed by the system.
  - Subsequent auto batch refunds of policy collection / renewal suspense will be disallowed by the system. Manual refund of policy collection suspense and renewal suspense will still be allowed.
- The Lock action will only lock refund of suspense. However, usage of the monies for application of premium or inforce of policy is not affected by the Lock.
- When the suspense refund is locked, the system will not allow the user to transfer monies from general suspense to other suspense (i.e. policy collection suspense and renewal suspense).

### Tolerance Rules

If the balance between actual amount and target amount is in the range of the tolerance limitation, the balance can be waived for customer.

Tolerance is triggered when the system performs the following functions:
- Collection of New Business inforce premium for all products
- Collection of renewal premium for all products, except for target ILP
- Bucket filling of target premium and regular top up premium for target ILP product

#### Tolerance for Bucket Filling

The tolerance amount for bucket filling is defined in the code table t_ilp_bucket_tolerance.

**Example for Bucket Filling Definition in Code Table:**

| Organization ID | Tolerance | Sales Channel ID |
|----------------|-----------|-----------------|
| 101 | 10 | 1 |
| 101 | 10 | 2 |
| 101 | 10 | 3 |
| 101 | 5 | 4 |
| 101 | 5 | 5 |
| 101 | 5 | 6 |

The related rules are as follows:
1. When the balance between actual target premium and target premium or actual regular top up and regular top up are in the range of tolerance limitation, the bucket filling due date can be moved.
2. The tolerance limitation definition is in base currency. Therefore, system will exchange between base currency and target currency if needed.
   - If the policy currency is the same as base currency, system directly compares the actual collected amount and target premium or regular top up, and checks whether the balance is in the range of tolerance in base/policy currency.
   - If the policy currency is different from base currency, system gets the tolerance in policy currency using the fixed exchange rate first and then compares the actual collected amount and target premium or regular top up, and checks whether the balance is in the range of tolerance in policy currency.

#### Tolerance for NB and Renewal

Tolerance amount for New Business and Renewal is defined in the rate table Tolerance. It is related to the following factors:
- Organization
- Sales channel
- Benefit type
- Application option

The related rules are as follows:
1. When the balance between actual collected premium and NB inforce premium or renewal premium is in the range of tolerance limitation, the proposal can be inforced or the due date can be moved.
2. The tolerance limitation definition is in base currency. Therefore, system will exchange between base currency and target currency if needed.
   - If the policy currency is the same as base currency, system directly compares the actual collected amount and New Business inforce premium or renewal premium, and checks whether the balance is in the range of tolerance in base/policy currency.
   - If the policy currency is different from base currency, system gets the tolerance in policy currency using the fixed exchange (buy) rate first and then compares the actual collected amount and New Business inforce premium or renewal premium, and checks whether the balance is in the range of tolerance in policy currency.

---

## 21. Menu Navigation

| Action | Path |
|--------|------|
| Counter Collection | Billing/Collection/Payment > Collection > Receive Counter Collection |
|
| Update Bank Account | Billing/Collection/Payment > Collection > Update Bank Account and Collection Date |
| Approve Collection | Billing/Collection/Payment > Collection > Approve Collection |
| Direct Debit Collection | Billing/Collection/Payment > Collection > Direct Debit Collection |
| Credit Card Collection | Billing/Collection/Payment > Collection > Credit Card Collection |
| Lock Box Collection | Billing/Collection/Payment > Collection > Lock Box Collection |
| Cancel Collection | Billing/Collection/Payment > Collection > Cancel Collection |
| Perform Waiver | Billing/Collection/Payment > Collection > Perform Waiver |
| Transfer Suspense | Billing/Collection/Payment > Collection > Transfer and Apply Suspense into Other Accounts |
| Batch Upload | Billing/Collection/Payment > Collection > Batch Upload Collection |
| Unmatched Collection | Billing/Collection/Payment > Collection > Manage Unmatched Collection |
| Cash Totalling | Billing/Collection/Payment > Collection > Manage Cash Totalling |
| Bank Auth Download | Billing/Collection/Payment > Billing > Electronic Collection > Bank Transfer > Download Bank Authorization File |
| Bank Auth Upload | Billing/Collection/Payment > Billing > Electronic Collection > Bank Transfer > Upload Bank Authorization File |
| Loan Repayment Schedule | Billing/Collection/Payment > Collection > Create or Modify Loan Repayment Schedule |
| Premium Voucher | Billing/Collection/Payment > Collection > Update Premium Voucher Details |
| Lock/Unlock Suspense Refund | Billing/Collection/Payment > Collection > Lock and Unlock Suspense Refund |

---

## 22. INVARIANT Declarations

**INVARIANT 1:** Collection amounts must be posted to the correct policy and billing records before the collection status is updated.
- Enforced at: Collection submission
- If violated: Policy billing records would be incorrect

**INVARIANT 2:** Cancelled collections must not generate payment requisitions; monies must remain in payable.
- Enforced at: Cancel Collection Page
- If violated: Duplicate payment could be issued

**INVARIANT 3:** Batch upload collection records are only processed after unmatched records are resolved.
- Enforced at: Batch Upload Collection Page
- If violated: Incorrect amounts posted to wrong policies

**INVARIANT 4:** Stamp duty is always calculated based on the total collection amount and the stamp duty indicator.
- Enforced at: Credit Card Collection submission
- If violated: Incorrect stamp duty collected or waived

**INVARIANT 5:** Bank account authorization status must be 'Authorized' before Direct Debit or Credit Card collection can proceed.
- Enforced at: Bank Transfer Extraction
- If violated: Collection failure; records not included in deduction file

**INVARIANT 6:** Sum of Bal Trf to must equal Bal Trf fm when transferring suspense between accounts.
- Enforced at: Transfer and Apply Suspense page
- If violated: System rejects submission

**INVARIANT 7:** Loan repayment start date for regular premium policies must be aligned with a premium due date.
- Enforced at: Create or Modify Loan Repayment Schedule
- If violated: System validation error on save

---

## 23. Related Files

| File | Relationship |
|------|-------------|
| insuremo-v3-ug-renewal.md | Renewal batch billing (related collection batch jobs) |
| ps-billing.md | Current version billing rules |
| 15_Collection_150605.pdf | Source PDF (78 pages) |
