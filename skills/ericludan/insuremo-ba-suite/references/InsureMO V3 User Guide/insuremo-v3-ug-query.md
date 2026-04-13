# InsureMO Platform Guide — Query

**Source:** 23_Query_BL.pdf (44 pages)
**System:** LifeSystem 3.8.1
**Version:** V3
**Date:** 2015-04-30

---

## Table of Contents

1. About Query
2. Common Query
3. New Business Query
4. Investment Query
5. Payment Query
6. Claim Query
7. Reinsurance Query
8. Producer Query
9. Parties Query
10. Accounting Query
11. Common Query (for Producer)
12. Appendix: Field Description

---

## 1. About Query

The Query Module is a commonly used module that allows you to search and perform comprehensive query of information related to the policies, agents, claims, customer services, reinsurance, payments, accountings, etc.

---

## 2. Common Query

Common Query allows you to query information for a policy or party.

The information that you can query under Common Query includes:

- Policy Information
- Financial Information
- Party Information
- Benefit Information
- CS Information
- Loan/Deposit Information
- Underwriting Information
- Claim Information
- CPF Information
- Quick Links (provides a shortcut to access relevant commonly-used information)
- Document Information
- NBU Information

### Workflow

1. From the main menu, select **Query > Common Query**.
   **Result:** The Common Query page is displayed.

2. On the Common Query page, select a search type, enter the corresponding search criteria, and then click **Search**.

   **Notes:**
   - If you enter the policy number or proposal number as the search criteria, the policy or proposal must be under the organization which you have access to.
   - If you enter the party name, party ID number, date of birth, direct debit account number, credit card account, or agent code, system will search out the party first, and then displays only the policies or proposals under the organization which you have access to.
   - The search criterion Party Name is not case sensitive.
   - The procedures vary slightly with different search criteria selected.

3. On the Common Query page, you can click each item tab to view item detailed information.

4. Click **Policy Info** tab, the policy information is displayed on the Policy Info tab page.

5. Click the **Financial Info** tab to view the financial information.

6. Click the **Party Info** tab to view the party information. You can click each party name to view detailed information about this party.

   **NOTE:** If you click a party name, regardless of proposer name, life assured name, payer name or payee name, you can view the detailed information of this party.

7. Click the **Benefit Info** tab to view benefit information. Click a plan name to view detailed information of this benefit.

8. Click the **CS Info** tab to view the CS information if any.

9. Click the **Loan/Deposit** tab to view the detailed information if any.

10. Click the **Underwriting Info** tab to view the underwriting information. Click an underwriting sequence to view the detailed information.

    **NOTE:** The Underwriting Information Screen consists of the following tabs:
    - Click the **Policy UW** tab to view the underwriting-related information at policy level, at the point of underwriting.
    - Click the **Benefit UW** tab to view the underwriting-related information at benefit level, at the point of underwriting.
    - Click the **LA1 Info** tab to view the first Life Assured's information including LIA/ICD9 and extra loading information, at the point of underwriting.
    - Click the **LA2 Info** tab to view the second Life Assured's information under the same benefit including LIA/ICD9 and extra loading information, at the point of underwriting.
    - Click the **Comments** tab to view the comments made at different NBU stages.
    - Click the **Condition/Exclusion/Endorsement/RC/Lien Info** tab to view the condition, exclusion, endorsement, restricted cover and lien information.
    - Click the **F&R Arrangement Info** tab to view facultative or reinsurer information.

11. Click the **Claim Info** tab to view the claim information including case number, notification date, type of claim, event date, claim status, policy claim amount, and payment status if any. Click the policy number to view the detailed information.

12. Click the **CPF Info** tab to view the CPF information including CPF account number, cash amount, CPF amount, deduction amount, last deduction date, CPF suspense amount, and cash suspense amount if any.

13. Click the **Quick Links** tab to view the links related to this policy. You can click each link to view the detailed information if required.

    Available Quick Links:
    - **Policy Basic Information** – to view the details of information at policy level, e.g., basic policy information, maturity information, conversion information, endorsement and exclusion.
    - **Policy Payment Information** – to view the details of policy collection from policyholder and payment to policyholder.
    - **Policy Receivable and Payable Information** – to view the details of policy receivable and payable generated from various modules, e.g., NBU, CS and Claims.
    - **Survival Benefit Information** – to view the next and historical Survival Benefit allocation details.
    - **Bonus Information** – to view the next and historical bonus allocation details for reversionary bonus or cash bonus.
    - **Enquiry Notes** – to view notes created under the Manage Notes module and reply to the notes.
    - **Enquiry SLQ** – to view the SLQ information.
    - **Bucket Filling Information** – to view the Bucket Filling Information.
    - **Variable Annuity Information** – to view the variable annuity information.
    - **Regular Withdraw Plan Information** – to view the regular withdraw plan information.
    - **Fund Coupon Information** – to view the fund coupon information.

14. Click the **Document Info** tab to view the document information related to this policy.

15. Click **NB Info** tab to view new business transaction information.

### Field Description on the Policy Tab Page

| Field | Description |
|-------|-------------|
| Policy Year/Period | **Policy Year:** number of years from the policy in force until now. **Period:** means which period the premium has been paid under current year. For example: If the premium payment mode is quarterly. When Policy Year/Period field is displayed as 3/4, it means fourth installment premium of the third year has been paid. |

---

## 3. New Business Query

### Query Last Issued Policy Number

You can query the Last Number Issued Information. For example, the last numbers issued for Policy Number, Underwriting Panel Clinic Code and Proposal Number.

1. From the main menu, select **Query > New Business > Issued Policy Number**.
   **Result:** The Enquiry On Last Numbers Issued page is displayed.

2. On the Enquiry On Last Numbers Issued page, you can view the detailed information.

#### Field Description — Enquiry On Last Numbers Issued Page

| Field | Description |
|-------|-------------|
| Last Policy Number | The system will display the latest policy number among all the accessible organizations of the users. The last issued Policy Number is made up of 1 prefix digit + 8 digit running numbers + 1 check digit. |
| Last Proposal Number | The system will display the latest proposal number among all the accessible organizations of the users. The last issued Proposal Number by Proposal Prefix consists of: 3 character prefix (representing the service branch) + 5 digit running numbers + YY (year of the proposal). For example: Proposal Number: AAA1111YY (where AAA = Service Branch Prefix, 11111 = Proposal Serial Number, YY = Year of Proposal) |

### Query Outstanding Premium

You can query the outstanding premium for a proposal.

1. From the main menu, select **Query > New Business > Outstanding Premium**.
   **Result:** The Enquiry Screen to Compute Inforcing Premium page is displayed.

2. On the Enquiry Screen to Compute Inforcing Premium page, enter the Proposal Number or Policy Number, and then click **Search**.
   **Result:** The Policy information, Dates, Premium Information, and Items for Calculating information are displayed on the same page.

3. Enter the calculated date and click **Calculate**. Then system calculates and displays the total inforcing premium according to the calculated date you entered.

---

## 4. Investment Query

### Query Fund Price

1. From the main menu, select **Query > Investment > Fund Price**.
   **Result:** The Query Fund Price page is displayed.

2. On the Query Fund Price page, enter the search criteria, and then click **Search**.

3. View the detailed information of this fund price in the Search Result section.

### Query ILP Cash Flow

1. From the main menu, select **Query > Investment > ILP Cashflow**.
   **Result:** The Query ILP Cashflow page is displayed.

2. On the Query ILP Cashflow page, enter search criteria, and then click **Search**.
   **Result:** The matching records are displayed in the ILP Cash Flow section.

3. In the ILP Cash Flow section, view the detail information.

4. If you want to view fund detail information, in the Fund Code column, click a fund code.
   **Result:** The Query on ILP Cash Flow - by Fund page is displayed.

---

## 5. Payment Query

### Query Single Payment

This section describes how to query payment information.

1. From the main menu, select **Query > Payment > Single Payment**.
   **Result:** The Payment Query page is displayed.

2. On the Payment Query page, enter the search criteria, and then click **Search** to search out the payment records.

3. In the Policy Amount column, click a payment amount to view the detailed information of this payment.

### Query Cash Movement

This section describes how to query and download cash movement details.

1. From the main menu, select **Query > Payment > Cash Movement**.
   **Result:** The Cash Movement Query page is displayed.

2. On the Cash Movement Query page, enter the search criteria, and then click **Search**.
   **Result:** The cash movement details are displayed.

3. Click **Download Excel**. Then the system prompts message: Do you want to open or save this file? Click **Open** to open this XLS file directly or click **Save** to save it on the local disk.

---

## 6. Claim Query

This section describes how to query comprehensive information of a specified claim case.

1. From the main menu, select **Query > Claim**.
   **Result:** The Query Claim Case Detail Information page is displayed.

2. On the Query Claim Case Detail Information page, enter the search criteria, and then click **Search** to search out the target claim record.

3. In the Case No. section, click the case number to view the case information.
   **Result:** The Query Claim Case Detail Information page is displayed.

   **Notes:**
   - The page displayed varies with different case status.
   - You can click the buttons at the bottom of the page to view the relevant information.

4. Click the policy number in the left pane to view the policy basic information.
   **Result:** The Case Evaluation Detail - Policy page is displayed.

   **NOTE:** You can click Medical Claim Worksheet to view the relevant information.

5. Click the product in the left pane to view the detailed information of this product.
   **Result:** The Case Evaluation Detail page is displayed.

   **NOTE:** You can click ADL or Detail to view the relevant information.

---

## 7. Reinsurance Query

### Reinsurance Query by Treaty

1. From the main menu, select **Query > Reinsurance > By Treaty**.
   **Result:** The Query Reinsurance By Treaty page is displayed.

2. On the Query Reinsurance By Treaty page, enter the search criteria, and then click **Search**.
   **Result:** The matching results are displayed in the RI Treaty section.

3. In the Treaty ID column, click the treaty ID to view the detailed information.
   **Result:** The RI Treaty page is displayed.

### Reinsurance Query by Contract

1. From the main menu, select **Query > Reinsurance > By Contract**.
   **Result:** The Query Reinsurance By Contract page is displayed.

2. On the Query Reinsurance By Contract page, enter the search criteria, and then click **Search**.
   **Result:** The matching results are displayed in the RI Contract section.

   **NOTE:** Only the policies/proposals under the organization which you have access to will be displayed regardless of the search criteria entered.

3. In the Contract ID column, click the contract ID to view the detailed contract information.
   **Result:** The RI Contract page is displayed.

### Reinsurance Query by Policy

1. From the main menu, select **Query > Reinsurance > By Policy**.
   **Result:** The Query Reinsurance By Policy page is displayed.

2. On the Query Reinsurance By Policy page, enter the search criteria, and then click **Search**.

   **Notes:**
   - Only the policies under the organization which you have access to will be displayed regardless of the search criteria entered.
   - Only the product with risk type set up will be displayed.

3. Click the policy ID to view the detailed information of this Reinsurance policy.
   **Result:** The RI Policy page is displayed.

4. Click the Contract ID to view the reinsurance information under the contract.
   **Result:** The Contract information is displayed in the Reinsurer section.

---

## 8. Producer Query

This section allows:

- Life Planners to view online policy information but only for policies and proposals being serviced by them.
- Staff to view all online policy information for all the policies and proposals.

The information you can query includes:

- Query Current Policy Information.
- Query Underwriting Information.
- Query Quotation Information.
- Query BCP Information.

### Query Current Policy Information

This section allows you to view the policy information, financial information, party information, benefit information and annuity information of a policy.

1. From the main menu, select **Query > Producer**.
   **Result:** The Query Agent page is displayed.

2. On the Query Agent page, select **Policy Information**, enter the policy number, and then click **Search**.
   **Result:** The Common Query page is displayed.

3. On the Common Query page, view the policy information. You can click **Financial Info**, **Party Info**, **Benefit Info**, **Annuity Info** or **Policy Basic Info** tab to view the corresponding information.

### Query Underwriting Information

This section allows you to query underwriting information such as SLQ, underwriting information, benefit underwriting decision, benefit extra loading, condition, exclusion and amount to turn proposal into policy, etc.

1. From the main menu, select **Query > Producer**.
   **Result:** The Query Agent page is displayed.

2. On the Query Agent page, select **Underwriting Information**, enter policy number or proposal number, and then click **Search**.
   **Result:** The Underwriting Info page is displayed.

3. On the Underwriting Info page, you can view the underwriting information.

### Query Quotation Information

This section allows you to query information about financial position, surrender voucher and paid-up quotation.

1. From the main menu, select **Query > Producer**.
   **Result:** The Query Agent page is displayed.

2. On the Query Agent page, select **Quotation Information**, enter Policy No., Validate Date, and then select quotation items from the Quotation Items drop-down list.

   - If **Financial Position** is selected, click Search and then go to Step 3.
   - If **Surrender Voucher** is selected, click Search and then go to Step 4.
   - If **Paid up Quotation** is selected, click Search and then go to Step 5.
   **Result:** The corresponding quotation item page is displayed.

3. On the **Financial Position** page, do as follows:
   a. View the basic information and then click **Submit**.
   b. View the detail information of financial position.

4. On the **Reduce SA And Partial Surrender** page, do as follows:
   a. View the basic information and then click **Submit**.
   b. Enter comment and requirement in the box if necessary, and then click **Preview**.
      **Result:** The system will prompt a download dialog box.
      **NOTE:** You also can click **Print** to print file.
   c. On the download dialog box, click **Open** to open this PDF file, or click **Save** to save file on the computer.

5. On the **Policy Values** page, do as follows:
   a. In the Policy Plan Information section, select a policy plan, update the validation date and validity date if necessary, and then click **Submit**.
   b. View the policy values information, including policy basic information, deposit, suspense and debts information, surrender/paid up values, surrender bonus, loan, factor table, ETA, print option, letter content and letter information, and then click **Preview**.
      **Result:** The system will prompt a download dialog box.
      **NOTE:** You also can click **Print** to print file, or click **Process Immediately** to alert policy information. For more information, refer to Customer Service User Guide.
   c. On the download dialog box, click **Open** to open this PDF file, or click **Save** to save file on the computer.

### Query BCP Information

This section allows you to query BCP information.

1. From the main menu, select **Query > Producer**.
   **Result:** The Query Agent page is displayed.

2. On the Query Agent page, select **BCP Information**, and then enter the search criteria in the displayed fields.

   - If you select **Inforce** as Policy Status, fields Next Due Date From/To and Payment Method will be displayed. Enter next due date from/to and payment method.
   - If you select **Non-Inforce** as Policy Status, fields Status Date up to Last (No. of Days), Lapse Status and Terminated Reasons will be displayed. Enter status date up to last, lapse status and terminated reason.

3. Click **Search** to view the related records displayed.

---

## 9. Parties Query

This section tells how to search out parties through various criteria. After parties are created, you can search them out to view and amend their information.

### Query Agent Parties

This section describes how to search agent parties.

1. From the main menu, select **Query > Party > Agent Party**.
   **Result:** The Query Agent Party page is displayed.

2. Select **Search Agent Party**, enter the agent code, and then click **Search**.
   **Result:** The matching agent record is displayed.

### Query Insurer Related Parties

This section describes how to search insurer related parties and customers.

1. From the main menu, select **Query > Party > Insurer Related Party**.
   **Result:** The Query Insurer Related Party page is displayed.

2. Select **Search Individual Party** or **Search Organization Party**, enter corresponding search criteria, and then click **Search**.
   **Result:** The matching party record is displayed.

### Query Policy Related Parties

This section describes how to search the parties related to a certain policy.

1. From the main menu, select **Query > Party > Policy Related Party**.
   **Result:** The Query Policy Related Party page is displayed.

2. Select **Search Policy**, enter the policy number, and then click **Search**.
   **Result:** The party records related to the policy are displayed.

### Query Third Parties

This section describes how to search third parties.

1. From the main menu, select **Query > Party > Third Party**.
   **Result:** The Query Third Party page is displayed.

2. Select a third party type, such as **Search Doctor**, **Search Hospital/Clinic**, or **Search Reinsurer/Others**, set search criteria, and then click **Search**.

---

## 10. Accounting Query

### Query Financial Details by Product

Enquiry/Download of Financial Details by Product allows you to query and download financial details, for example, fee type, currency and amount by Product.

1. From the main menu, select **Query > Accounting > Financial Details by Product**.
   **Result:** The Enquiry/Download of Financial Details by Product page is displayed.

2. On the Enquiry/Download of Financial Details by Product page, enter the search criteria and then click **Download**.
   **Result:** System will prompt message: Do you want to open or save this file? Click **Open** to open this XLS file directly, or click **Save** to save it on the computer.

### Query Transaction

Transaction Query allows you to query and download all transaction history tables including Traditional and ILP transactions.

**NOTE:** For Traditional and ILP transactions, the query of transaction history will be for transactions with fee status as "1", "6" or "0" (for accrual transactions), including all posted and un-posted records, but excluding records which do not need to be posted.

1. From the main menu, select **Query > Accounting > Transaction**.
   **Result:** The Query Transaction page is displayed.

2. On the Query Transaction page, enter the search criteria, and then click **Search**.

3. In the Amount column, click the amount to view the detailed information of this transaction.

4. Click **Download** and then the system prompts message: Do you want to open or save this file? Click **Open** to open this XLS file directly or click **Save** to save it on the computer.

---

## 11. Common Query (for Producer)

This section allows you to search and query on:

- **Life Planner Information.** For example, Party Information, Contacts, Account, Comments, Roles and History.
- **Policy-related Information** for the policies that are serviced by the Life Planner. For example, Policy Information, Financial Information, Party Information, Benefit Information, CS Information, NBU Information, Loan/Deposit Information, Underwriting Information, Claim Information, CPF Information, Quick Links and Document Information.

### Workflow

1. From the main menu, select **Query > Common Query (for Producer)**.
   **Result:** The Common Query (for Producer) page is displayed.

2. On the Common Query (for Producer) page, enter **Agent Code**, and then click **Search**.
   **Result:** The matching records are displayed.

3. Click an agent code to query the agent information.
   **Result:** The Individual Customer Info page is displayed.

   **NOTE:** Click policy number to view policy information. For details, see Common Query.

4. On the Individual Customer Info page, view the party information. You also can click tab **Contact**, **Account**, **Comments**, **Roles** and **History** to view corresponding information.

---

## 12. Appendix: Field Description

### Field Description in New Business Query

**Table 1: Description of Fields on the Enquiry On Last Numbers Issued Page**

| Field | Description |
|-------|-------------|
| Last Policy Number | The system will display the latest policy number among all the accessible organizations of the users. The last issued Policy Number is made up of 1 prefix digit + 8 digit running numbers + 1 check digit. |
| Last Proposal Number | The system will display the latest proposal number among all the accessible organizations of the users. The last issued Proposal Number by Proposal Prefix consists of: 3 character prefix (representing the service branch) + 5 digit running numbers + YY (year of the proposal). For example: Proposal Number: AAA1111YY (where AAA = Service Branch Prefix, 11111 = Proposal Serial Number, YY = Year of Proposal) |

### Field Description in Common Query

**Table 2: Field Description on the Policy Tab Page**

| Field | Description |
|-------|-------------|
| Policy Year/Period | **Policy Year:** number of years from the policy in force until now. **Period:** means which period the premium has been paid under current year. For example: If the premium payment mode is quarterly. When Policy Year/Period field is displayed as 3/4, it means fourth installment premium of the third year has been paid. |

---

## Related Files

| File | Relationship |
|------|-------------|
| insuremo-v3-ug-nb.md | NB Query — outstanding premium context |
| insuremo-v3-ug-fund-admin.md | Fund price query |
| insuremo-v3-ug-reinsurance.md | RI Query |
| insuremo-v3-ug-loan-deposit.md | Loan/deposit query |
| insuremo-v3-ug-payment.md | Payment query |
