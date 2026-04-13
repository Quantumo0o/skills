# InsureMO Platform Guide — Fund Administration

> **Source:** 17_Fund_Administration_0.pdf (78 pages), LifeSystem 3.8.1
> **Updated:** Reflects full extraction including all batch jobs (pages 44–52) and Appendix A Rules (pages 54–78)

---

## Metadata

| Field | Value |
|-------|-------|
| File | insuremo-v3-ug-fund-admin.md |
| Source | 17_Fund_Administration_0.pdf |
| System | LifeSystem 3.8.1 |
| Version | V3 (legacy) |
| Date | 2015-04-27 |
| Category | Investment / Fund Administration |
| Pages | 78 |

---

## 1. Purpose of This File

Answers questions about ILP fund administration in LifeSystem 3.8.1. Covers NAV management, fund transactions, unit calculations, charge deductions, lock-in periods, fund switches, fund settlement, and all batch jobs. Critical reference for VUL and investment-linked product BSDs.

**Note:** This document is primarily a UI-reference guide. For detailed NAV calculation formulas and fund transaction rules, supplement with the current ps-fund-administration.md.

---

## 2. Module Overview

```
Fund Administration (LifeSystem 3.8.1)
│
├── 1. About Fund Administration
│
├── 2. Manage Fund Price
│   ├── Enter Fund Price
│   ├── Suspend Fund Price
│   └── Approve Fund Price
│
├── 3. Perform Fund Transaction
│   ├── Target Concept
│   ├── Deduct Charges
│   └── Lock In Period
│
├── 4. Adjust Unit
│   ├── Adjust Unit by Policy
│   └── Adjust Unit by Batch
│
├── 5. Calculate Gain and Loss
│
├── 6. Enter and Approve Fund Coupon Rate
│
├── 7. Automatic Switch
│
├── 8. Transfer from MF to CF
│
├── 9. Fund Settlement
│   ├── Enter Saving Account Rate
│   ├── Calculate Account Interest
│   └── Calculate Yearly Bonus
│
├── 10. Batch Jobs
│   ├── Guarantee Roll Up
│   ├── Guarantee Step Up
│   ├── Fund Coupon Allocation
│   ├── Fund Maturity
│   ├── Policy Loan Lapse
│   ├── ILP Policy Lapse Sell All Units
│   ├── Fund Coupon Alloc-Renew Status
│   ├── Insert Cash Flow Temp Table
│   └── Auto Switch ILP Strategy
│
└── Appendix A: Rules
    ├── Upload Fund Price Rules
    ├── Fund Transaction Rules
    ├── Allow/Not Allow Pending Transaction Rules
    ├── Logic Rules
    ├── Adjust Unit Rules
    ├── Automatic Switch Rules
    ├── Transfer from MF to CF Rules
    ├── Saving Account Rate Entry Rules
    ├── Guarantee Roll Up Rules
    ├── Guarantee Step Up Rules
    ├── Fund Coupon Allocation Rules
    ├── Fund Maturity Rules
    ├── Policy Loan Lapse Rules
    ├── Auto Switch ILP Strategy Rules
    └── ILP Premium Stream Configuration Rules
```

---

## 3. Key Concepts

### NAV (Net Asset Value)

NAV = Fund Value per Unit = Total Market Value of Fund Assets / Total Number of Units in Fund

**Key Rules:**
- NAV is calculated daily by the fund manager
- NAV is entered into the system by Operations
- NAV must be approved before transactions can use the new price
- NAV is used for all fund transactions: switch, top-up, partial withdrawal, surrender

### Unit Holdings

| Level | Description |
|-------|-------------|
| Policy Level | Total units held by the policy |
| Fund Level | Units allocated to each fund within the policy |
| Transaction Level | Units bought/sold per transaction |

### Fund Account Structure (ILP)

```
Policy Investment Account
  └── Fund Level Account (per fund)
        └── Unit Holdings (number of units)
              └── Unit Price (NAV at time of transaction)
```

---

## 4. Per-Process Sections

### Process 1: About Fund Administration

An insurance fund is a pool of assets held by the insurance company. Payments into the insurance fund include expense deductions, insurance charges, policy fee, rider premiums and other charges. Payments out of the insurance fund include claims for the Net Sum Assured for Death (& TPD) Benefit, rider benefit claims, commissions and expenses. A fund is managed in units.

Fund transaction is the process that the fund house purchases or sells fund units based on the request raised by customers. It needs to be performed after the request of transaction is applied, such as top up, partial withdraw, and fund switch.

#### Fund Transaction Management Workflow

| S/N | Description | Means |
|-----|-------------|-------|
| 1 | After obtaining the fund price, the finance personnel in the insurance company should manage the fund price for future fund transactions. For details, refer to Manage Fund Price. | Manual |
| 2 | On scheduled date, the system will perform fund transactions automatically. For details, refer to Perform Fund Transaction. | System Batch Job |
| 3 | On scheduled date, the system will deduct charges automatically according to the related rules. For details, refer to Deduct Charges. | System Batch Job |
| 4 | If there is an operation error and the number of units under the policy is wrong, unit adjustment is required for the particular policy. For details, refer to Adjust Unit. | Manual |
| 5 | If gain and loss calculation is required after unit adjustment, on scheduled date, the system will calculate gain and loss automatically. For details, refer to Calculate Gain and Loss. | System Batch Job |

---

### Process 2: Manage Fund Price

Fund price is the price used for buying and selling a fund. Normally the fund price is defined by the fund house and calculated based on the net asset value of the fund. After obtaining the fund price, the finance personnel in the insurance company should manage the fund price for future fund transactions.

**Workflow:**
1. After the fund manager issues the fund price, check whether the fund price is confirmed by the fund manager.
   - If the fund price is confirmed by the fund manager, go to Enter Fund Price.
   - If the fund price is not confirmed by the fund manager, go to Suspend Fund Price.
2. After fund prices are in status Entered, go to Approve Fund Price.
3. On the scheduled date, the system performs a batch job to confirm the fund price and changes the price status to Confirmed.

#### Enter Fund Price

**PREREQUISITE:** The fund price is confirmed by the fund manager.

**NOTE:** You can enter fund prices by either of the following ways:
- Manually enter fund prices entry by entry. See Step 2 for details.
- Batch upload fund prices with an excel file. See Step 3 for details.

1. From the main menu, select **Investment > Fund Price > Entry > New or Revise**.
   RESULT: The Batch Fund Price Entry page is displayed.

2. To manually enter fund prices:
   a. Set search criteria, and then click **Search**.
   b. Select the target fund records by selecting the checkboxes in the first column and enter a price in the Bid Price box.
      NOTE: If the price status is Approved or Confirmed, the Revise checkbox is available and you can revise the bid price as required.
      RESULT: Values in the Offer Price and Variance from Last Confirmed Price columns are calculated automatically. If there's no last confirmed price, the Variance from Last Confirmed Price field is blank.
   c. Click **Submit**.
      RESULT: The information is saved and the price status is changed to Entered.

3. To batch upload fund prices by an excel file:
   a. Click **Download Template** to download the Batch Upload Fund Prices excel template.
   b. Click **Save** and save the template to the local disk.
   c. Open the template file, update it with fund price information, and save the changes.
   d. Click **Upload**.
      RESULT: The Upload File page is displayed.
   e. Click **Browse** to locate the updated Fund Price Template file on your local disk.
   f. Click **Submit**.
      RESULT: If upload succeeds, a message is displayed. The information is saved and the price status is changed to Entered.

#### Suspend Fund Price

**PREREQUISITE:** The fund price is not confirmed by the fund manager.

1. Suspend Fund Prices:
   a. From the main menu, select **Investment > Fund Price > Entry > Suspend**.
      RESULT: The Batch Fund Price Suspend page is displayed.
   b. Set search criteria, and then click **Search**.
   c. Select the target fund records by selecting the check boxes under Option and select the corresponding Suspend checkbox.
   d. Click **Submit**.
      RESULT: The price status is changed to Suspended.

2. When the suspended fund price is confirmed by the fund manager, unsuspend the fund price:
   a. From the main menu, select **Investment > Fund Price > Entry > Unsuspend**.
      RESULT: The Batch Fund Price Unsuspend page is displayed.
   b. Set search criteria, and then click **Search**.
   c. Select the target fund records by selecting the checkboxes in the first column and enter a price in the Bid Price box.
      RESULT: Values in the Offer Price and Variance from Last Confirmed Price columns are calculated automatically. If there's no last confirmed price, the Variance from Last Confirmed Price field is blank.
   d. Clear the corresponding Suspend check box.
   e. Click **Submit**.
      RESULT: The information is saved and the price status is changed to Entered.

#### Approve Fund Price

**PREREQUISITE:** Fund prices are in status Entered.

1. From the main menu, select **Investment > Fund Price > Approve**.
   RESULT: The Batch Fund Price Approval page is displayed.

2. Set search criteria, and then click **Search**.
   RESULT: All fund records matching the search criteria are displayed.

3. Select the target fund records under the Option list and select the corresponding Approve checkboxes.

4. Click **Submit** to approve fund prices.
   - If you reject the fund price, select the target fund record under the Option list and click **Reject**. Then the fund manager needs to issue the fund price again.
   - If you click **Fund Price Validate**, a system message "A daily price update is expected for ******" is displayed, indicating which fund prices are not approved.
   RESULT: The price status is changed to Approved.

---

### Process 3: Perform Fund Transaction

Fund transaction batch job reads all records that are pending for fund transaction. This job will perform the normal validity checks.

If the price for the fund to be transacted is available, the records pending for fund transaction will be bought or sold depending on the following instructions in the records:
- Which Fund Type to transact
- Whether to 'buy' or to 'sell' (transact)
- Whether to transact (buy/sell) by units or by value
- Whether to use 'forward' or 'now' price
- Whether to use 'bid' or 'offer' price (price retrieved from Fund Price file)
- The effective date to use when reading the price for the fund

For backdating cases, the system will calculate the Profit / Loss (fluctuations) and create the relevant General Ledger 'Fee-Type' entries.

**PREREQUISITES:**
- Policy has pending transaction.
- Current or forward price is available based on the validity date of the transaction record.

**Processing Steps:**

1. On scheduled date, the system searches for pending transactions.
   - If no pending transactions exist, the processing is complete.
   - If pending transactions exist, proceed with the following steps.

2. The system determines the values for the fund transaction process based on the values in the records pending for fund transaction.

3. The system checks whether the current price (either 'Bid' or 'Offer' price as indicated in the records) is available based on the Validity Date.
   - If the current price is unavailable, Price Used Date is set to the date when the price is next available price from the Validity Date, and Price Used is set to the next available price from Validity Date. The process ends.
   - If the current price is available, Price Used Date is set to Validity Date, and Price Used is set to Price of Fund at Validity Date. Go to step 4.

4. The system processes transactions based on different alterations, such as top up, partial withdraw, fund switch, and full surrender.

5. The system generates transaction related letters and Investment Linked Product (ILP) letters, and performs charge deduction (refer to Deduct Charges for details). If there are exceptions, the system generates exception reports and ILP exception reports.

6. The finance personnel performs posting to GL.

#### Target Concept

Target concept is applied to investment product normally. It is a schedule to restrict client premium payment. Each installment payment determined by premium mode has its corresponding bucket.

Whenever money is collected from the client, bucket filling option is applied to determine the use of the money.

**Bucket filling options** to define whether the product has target concept and how to fill the bucket:
- **0: No target** — No target concept
- **1: Fill in all Past Buckets and Future Buckets as much as possible** — System fills in from the first unfilled bucket to future buckets until all buckets are filled up. The excess amount is applied to single top up.
- **2: Fill in all Past Buckets and Future Buckets for current policy year** — System fills in from the first unfilled bucket to future buckets during the current policy year. The excess amount is applied to single top up.

**Additional bucket filling options** to define whether to fill the bucket by proportion or fill premium first:
- **1: Filling by proportion** — System fills the buckets according to the proportion. Target premium is calculated according to its apportionment. The recurring top up plus target premium equals total invested amount.
- **Filling premium first** — System fills the target premium first and then recurring top up for each bucket.

#### Deduct Charges

The charges include cost of insurance, policy fee, fund management fee, guaranteed charge (for variable annuity), and expense charge (if it is defined to be deducted from funds). Charge deduction will be triggered on a specific time every day (daily batch job) and triggered by buy transaction.

**PREREQUISITES:**
- Policy is investment linked.
- Policy is not the issue without premium policy.
- Policy does not have any pending fund transaction if the parameter FND_CAN_PERFORM_WITH_PENDING_TRANS is N.
- If the parameter CHARGE_IN_ADVANCE_FLAG is N, system date ≥ charge due date; if the parameter CHARGE_IN_ADVANCE_FLAG is Y, system date ≥ charge due date – Price Waiting Days (defined in fund). Or system date ≥ [cash riders' due date + (grace period + additional grace period)].
- For the policy issued without premium, the policy is not in the issue without premium grace period.

At a specific time every day, the system starts a batch job to deduct charges automatically using the total investment value and calculate Potential Lapse Date (PLD) on the installment due date.

1. The system checks whether the selected policy meets the following conditions:
   - Charge due date > PDD
   - System date ≥ [cash riders' due date + (grace period + additional grace period)]
   - Cash rider's premium is not deducted yet (regardless of whether it is partial or full deduction)
   RESULT: If yes, go to step 2; if no, go to step 9.

2. The system checks whether PLD exists.
   RESULT: If yes and the lapse methodology is Deduct TIV Until Zero, the process ends; if yes and the lapse methodology is Calculate PLD, go to step 3. If no, go to step 9.

3. The system checks whether TIV is sufficient for prorated CRP between PDD and PLD.
   NOTE: Prorated CRP = (number of days to prorate)*(CRP per day) = (PLD – PDD)*(CRP/D)
   - Monthly frequency = 30 days
   - Quarterly frequency = 91 days
   - Half yearly frequency = 182 days
   - Yearly frequency = 365 days
   - Price used for all the variables will be the price as of PDD.
   RESULT: If yes, go to step 4. If no, go to step 5.

4. The system deducts TIV:
   - The system deducts prorated CRP for the period of PDD to PLD.
     NOTE: If the policy has more than one fund, deduction per fund = deduction amount*value of fund/TIV.
   - The system creates outstanding CRP for a period of PLD to the next PDD.
   - The system creates one record for each installment.
   RESULT: Go to step 6.

5. The system deducts all TIV:
   - The system deducts all TIV to settle prorated CRP.
   - The system creates Miscellaneous Debt for the outstanding CRP up to PLD.
   - The system creates Outstanding CRP for a period of PLD to the next PDD.
   RESULT: Go to step 6.

6. The system checks whether the total units are sufficient to cover CRP from PDD to the next installment due date.
   RESULT: If yes, go to step 7. If no, go to step 8.

7. The system deducts TIV and moves PDD:
   - For internal fund process, the system deducts TIV to settle CRP and moves PDD to the next installment due date; for external fund process, the system generates pending deduction records, waiting for external fund price to deduct TIV and to move PDD.
   RESULT: Go to step 9.

8. The system deducts all TIV and moves PDD:
   - For internal fund process, the system deducts all TIV to settle prorated CRP, creates Miscellaneous Debt up to (PDD+ next installment due date), and moves PDD to the next installment due date; for external fund process, the system generates pending deduction records, waiting for external fund price to move PDD.
   - The system cancels the related service tax of cash rider's premium.
   RESULT: Go to step 9.

9. The system checks whether the lapse methodology is Deduct TIV Until Zero and PLD exists.
   RESULT: If yes, the process ends. If no, go to step 10.

10. The system checks whether the charge due date is equal to PLD or the charge due date is later than system date.
    RESULT: If yes, the process ends. If no, go to step 11.

11. The system checks whether the policy's charge due date (with lowest frequency) is equal to one of installment due dates of the main benefit.
    NOTE: For single premium policy, PLD will be calculated at every deduction.
    RESULT: If yes, go to step 12. If no, go to step 13.

12. The system checks whether PLD is within the installment period.
    NOTE: PLD = charge due date + TIV/((COI+URP+PF)*n+Expense+CRP)*D
    - Monthly frequency = 30 days
    - Quarterly frequency = 91 days
    - Half yearly frequency = 182 days
    - Yearly frequency = 365 days
    - 'n' refers to the number of months in an installment period:
      - Monthly frequency = 1 month
      - Quarterly frequency = 3 months
      - Half yearly frequency = 6 months
      - Yearly frequency = 12 months
    - For policy with monthly payment frequency and charge due date > PDD, the system needs to calculate the TIV first before calculating the PLD.
    - Price used for all the variables will be the price as of charge due date.
    - If TIV is zero, the system sets PLD to be equal to charge due date.
    RESULT: If yes, the system sets the PLD and go to step 13. If no, go to step 16.

13. The system checks whether TIV is sufficient for prorated expense.
    NOTE: Prorated Expense = number of days to prorate * expense per date = (PLD - PDD) * (Expense/D)
    - Monthly frequency = 30 days
    - Quarterly frequency = 91 days
    - Half yearly frequency = 182 days
    - Yearly frequency = 365 days
    - Price used for all the variables will be the price as of PDD.
    RESULT: If yes, go to step 14. If no, go to step 15.

14. The system deducts TIV and generates outstanding expense:
    - For internal fund process, the system deducts prorated expense and creates outstanding expense for a period of PLD to the next PDD; for external fund process, the system generates pending deduction records.

15. The system deducts all TIV and generates outstanding expense:
    - For internal fund process, the system deducts all TIV to settle the prorated expense, creates Miscellaneous Debt for the prorated expense up to PLD, and creates outstanding expense for a period of PLD to the next PDD; for external fund process, the system generates pending deduction records.

16. The system checks whether TIV is sufficient for one installment expense.
    NOTE: TIV calculation:
    - Internal fund: TIV = total fund value
    - External fund: TIV = total fund value - pending withdraw/switch-out amount + pending buying/switch-in amount. (System uses the latest fund price to calculate total fund value.)
    - For estimation TIV calculation using the latest known price, a price factor is to be used to adjust the price for each fund: fund price * (1 + fund price factor)
    RESULT: If yes, go to step 17. If no, go to step 18.

17. For internal fund process, the system deducts expense to reduce TIV and shift the due date of expense; for external fund process, the system generates pending deduction records.

18. For internal fund process, the system deducts expense, generates Miscellaneous Debt and shift the due date of expense; for external fund process, the system generates pending deduction records.

19. The system checks whether PLD is within the charge period following the charge due date.
    RESULT: If yes, go to step 20. If no, go to step 23.

20. The system checks whether TIV is sufficient for prorated charge.
    NOTE: Prorated monthlyversary charge = (number of days to prorate)*(monthlyversary charge per day) = (PLD – MDD)*[(PF + IC + URP)/30]
    - PF: Policy Fee; IC: Insurance Charge; URP: Unit Deduction Rider
    - (PLD – MDD) refers to the number of days between MDD and PLD
    - Price used for the TIV and monthlyversary charge variables will be the price as of MDD
    RESULT: If yes, go to step 21. If no, go to step 22.

21. The system deducts TIV and moves charge due date:
    - For internal fund process, the system deducts prorated charge; for external fund process, the system generates pending deduction records.
    - The system moves charge due date to be equal to PLD.
    RESULT: Go to step 23.

22. The system deducts all TIV and moves charge due date:
    - For internal fund process, the system deducts all TIV to settle the prorated charge; for external fund process, the system generates pending deduction records.
    - The system creates Miscellaneous Debt for the outstanding charge up to PLD.
    - The system moves charge due date to be equal to PLD.
    RESULT: Go to step 23.

23. The system checks whether TIV is sufficient for one monthlyversary charge.
    NOTE: If the fund currency is different from the policy currency, the system will do as follows:
    - Exchange the value of each fund from the fund currency to the policy currency using the real time exchange rate on the system date.
    - Sum the value of each fund in policy currency of all the funds attached to the policy.
    - Regard the summed value of each fund in policy currency as the TIV of the policy.
    RESULT: If yes, go to step 24. If no, go to step 25.

24. The system deducts charge and moves charge due date:
    - The system reduces TIV to settle one monthlyversary charge.
      NOTE: One monthlyversary charge refers to total charge of PF, IC and URP for one deduction installment period. Deduction period is defined at product level.
    - The system moves charge due date by one charge period.
      NOTE: Charge period refers to one deduction installment period which is defined at product level.

25. The system deducts charge, generates Miscellaneous Debt and moves charge due date:
    - The system deducts all TIV to settle one charge period's charge.
    - The system generates Miscellaneous Debt up to charge due date + 1 charge period.
    - The system moves charge due date by one charge period.

**NOTE: Charge deduction rules:**
- For the charge deduction of Policy Fee (PF), Insurance Charge (IC) and Unit Deduction Rider (URP), the system should always deduct the PF first, then the IC and URP.
- All charges and TIV should be calculated at bid price.
- In the event that the fund price is higher than the charge deduction amount and the unit calculated after rounding is less than 0.01, no unit will be sold.

#### Lock In Period

Lock In Period process will be added inside Charge Deduction Batch after normal charges have been deducted. Lock In Period process is triggered if the premium is not paid by the customer after a certain period since policy issued. There are different steps in Lock In Period process:
1. Deduction due premium of TP/STU from UTU part of fund units
2. Convert premium frequency to monthly and deduct due premium (monthly) of TP/STU from UTU part of fund units
3. Deduct NAC (premium expense charge) from the fund units

- If "Lock In Period Option" is "Deduct TP/STU from UTU, then deduct non allocation charge", both two processes will be triggered in orders.
- If "Lock In Period Option" is "Deduct TP/STU from UTU only", then only "Deduction of TP/STU from UTU process" will be triggered.

NOTE: "Lock In Period Option" is defined in Product Definition stage. For more details, refer to Part 7. ILP Rules in Product Configuration Guide - LifeSystem 3.8.1.

**PREREQUISITES:**
- Lock In Period is applied.
- Using Target Premium Concept (Regular Premium Products).
- Additional Bucket Filling Option is Fill by the proportion of target premium and recurring top up.
- Lapse Method is Deduct TIV until zero.
- Apply Fund Premium Stream.

1. The system validates whether the policy matches the condition to kick off lock in period process:
   - Policy is Inforce.
   - The product has Lock In Period Option (Option is not 0-NA) and Bucket Filling Option = Fill by the proportion of target premium and recurring top up.
   - Policy is not frozen.
   - Policy is within the lock in period.
   - System date >= Premium next due date + Grace period of premium.
   - Premium filled for the current due date < Total requested amount (TP + STU) - Tolerance amount of renewal.

2. The system checks whether to deduct the unfilled TP and STU amount of the current due date from fund value of UTU:
   - Lock In Period Option is 1 or 2.
   - The fund value of UTU >= unfilled premium amount of current due date (including TP and STU).
   - The fund value of UTU = sum (no. of units of UTU for each fund * the latest known price).
   - No. of units of UTU should consider all other pending fund transactions.

3. If the validation passes, system generates pending selling application to deduct the unfilled TP and STU amount of the current due date from fund value of UTU:
   - Pending Amount = Unfilled premium amount of current due date
   - Transaction Date for selling: Premium current due date + Grace Period
   - Price Effective Date: follow T+N rules (T=Transaction Date)
   - Pending amount for each fund will be calculated by the ratio of each fund's UTU value

4. If the validation fails, system will automatically perform the following tasks:
   a. Update premium frequency to monthly and Premium due date will be updated accordingly.
   b. Premium will be refilled and Bucket filling information will be updated accordingly as well.

5. System will check whether to deduct 1 month's unfilled TP and STU amount of the current due date from fund value of UTU:
   - Lock In Period Option is 1 or 2.
   - The fund value of UTU >= 1 month's unfilled premium amount of current due date (including TP and STU).
   - The fund value of UTU = sum (no. of units of UTU for each fund * the latest known price).
   - No. of units of UTU should consider all other pending fund transactions.

6. If the validation passed, system will generate pending selling application to deduct the unfilled TP and STU amount of the current due date from fund value of UTU:
   - Pending Amount = Unfilled premium amount of current due date.
   - Transaction Date: Premium current due date + Grace Period.
   - Price Effective Date: follow T+N rules (T=Transaction Date).
   - Pending amount for each fund will be calculated by the ratio of each fund's UTU value.

7. If the validation fails, system will check whether to deduct non-allocation charge of unfilled TP for the current due date from the total fund value:
   - Lock In Period Option is 1.
   - The Total Investment Value >= Non-allocation Charge of unfilled TP for the current due date.
   - The Total Investment Value = sum (no. of units of each fund * the latest known price).
   - No. of units of each fund should consider all other pending fund transactions.

8. If the validation passed, system generates pending fund transaction to deduct the non-allocation charge of the un-filled premium of the current premium due:
   - Pending amount = Non-allocation charge rate * Unfilled TP amount of current due date.
   - Transaction Date:
     - For the first deduction will be Premium current due date + Grace Period.
     - For the following deduction will be Charge Due Date.
   - Pending amount for each fund will be calculated by the ratio of each fund's value (including TP, STU and UTU).

9. If the validation fails, process ends.

---

### Process 4: Adjust Unit

If there is an operation error and the number of units under the policy is wrong, unit adjustment is required for the particular policy. Batch unit adjustment is required if the fund price is wrongly declared. After the price is corrected, all the policies affected need to be adjusted.

**PREREQUISITE:** The current policy status is Inforce.

#### Adjust Unit by Policy

1. Search out the policy that requires unit adjustment:
   a. From the main menu, select **Investment > Adjust Unit**.
      RESULT: The Unit Adjustment page is displayed.

   Below are descriptions of fields on the Unit Adjustment page:

   | Field | Description |
   |-------|-------------|
   | Units to Adjust | Units to be adjusted to the current unit balance. For example, the value 20 indicates that the current unit balance will be added by 20 units; the value -20 indicates that the current unit balance will be reduced by 20 units. Current Unit Balance plus Units to Adjust cannot be smaller than 0. |
   | Gain & Loss Impact | If selected, the fund will affect gain and loss; if not selected, the fund will not affect gain and loss. |
   | Price Effective Date for Adjustment | Date when the adjustment takes effect. Price Effective Date for Adjustment cannot be later than Adjustment Date. |
   | Reason for Adjustment | Reason why the adjustment is made, for example, typo error. |

   b. Enter the policy number, and then click **Search**.
      RESULT: All the fund records under the policy are displayed in the Unit Adjustment area.

2. Adjust units:
   a. From the Option list, select the fund that requires unit adjustment.
   b. Set Units to Adjust, Gain & Loss Impact, Price Effective Date for Adjustment, and Reason for Adjustment.
   c. Click **Submit**.

3. The system updates the current units of the policy and generates the ILP fund application with a special service ID of Fund Unit Manual Adjustment.

4. The system checks the Gain & Loss Impact field:
   - If Gain & Loss Impact is selected, the system calculates gain and loss. For details, refer to Calculate Gain and Loss.
   - If Gain & Loss Impact is not selected, the processing is complete.

#### Adjust Unit by Batch

1. Download the batch unit adjustment report:
   a. From the main menu, select **Investment > Batch Correct Price**.
      RESULT: The Batch Unit Adjustment page is displayed.
   b. In the Download area, enter the Fund Code, Price Effective Date, Adjustment Date, and Transaction Date. Then click **Download Excel**.
      RESULT: The File Download dialog box is displayed.
   c. Click **Save** to save the batch unit adjustment report.

2. Update the batch unit adjustment report and save it as a .csv file.

3. Upload the updated batch unit adjustment report:
   a. In the Upload area, click **Browse** to select the updated batch unit adjustment report from your local PC.
   b. Click **Upload Excel**.
      RESULT: The report is uploaded and a file number is generated.

4. Verify the upload result:
   a. In the Upload Result area, enter the upload file number and click **Search** to verify the upload result.
   b. For the failed records, adjust units by policy. For details, refer to Adjust Unit by Policy.
   c. For the successful records, go to step 5.

5. The system updates the current units and generates daily report with the batch unit adjustment upload result.

6. The system checks the Gain/loss Indicator:
   - If Gain/loss Indicator is set to Y (gain and loss calculation required), the system calculates gain and loss. For details, refer to Calculate Gain and Loss.
   - If Gain/loss Indicator is set to N (no gain and loss), the processing is complete.

---

### Process 5: Calculate Gain and Loss

When a fund transaction is delayed or backdated, the Actual Transaction Date is different from the Price Effective Date. In this case, the insurer will still perform the fund transaction based on the Price Effective Date which is requested by customer. However, in the real market, only the price of the transaction date can be used. Therefore, the insurer will have loss if the price of the Date Requested by Customer is higher than the price of the Actual Transaction Date, and the insurer will have gain if the price of the Date Requested by Customer is lower than the price of the Actual Transaction Date.

**PREREQUISITES:**
- Gain & Loss Impact is selected, or
- Gain/loss Indicator is set to Y.

1. On the scheduled date, the system picks up the fund records that require gain and loss calculation.

2. The system calculates the gain and loss for the fund records:

   | Scenario | Gain and Loss |
   |----------|---------------|
   | Insert time ≤ price effective date and transaction date - price effective date ≤ 1 | N/A |
   | Insert time > price effective date | Units × (bid price of price effective date - bid price of transaction date) |
   | Insert time ≤ price effective date and transaction date - price effective date > 1 | Units × (bid price of price effective date - bid price of transaction date) |

3. The system updates the fund records.

4. The finance personnel performs posting to GL.

---

### Process 6: Enter and Approve Fund Coupon Rate

Coupon rate of a fund needs to be entered into the system and approved for allocation.

**PREREQUISITE:** You have the authority to perform coupon rate entry and approval.

1. Search out the funds that require coupon rate entry:
   a. From the main menu, select **Investment > Coupon Rate > Entry**.
      RESULT: The Fund Coupon Rate Entry page is displayed.
   b. In the Search Criteria area, set Coupon Rate Effective Date and enter the fund code range (Fund Code from and Fund Code to). Then click **Search**.
      RESULT: The fund records of the entered code range are displayed in the Fund Coupon Rate Entry area.

2. Perform fund coupon rate entry:
   a. Select target funds, enter the coupon rate, base unit, and select a coupon declaration type (By Amount or By Unit).
   b. Click **Submit**.
      RESULT: The system saves the coupon rate records with the status ENTERED.

3. Search out the fund coupon rate to be approved:
   a. From the main menu, select **Investment > Coupon Rate > Approve**.
      RESULT: The Fund Coupon Rate Approval page is displayed.
   b. In the Search Criteria area, set Coupon Rate Effective Date and enter the fund code range (Fund Code from and Fund Code to). Then click **Search**.
      RESULT: The fund coupon records of the entered code range are displayed in the Fund Coupon Rate Approval area.

4. Approve or reject the fund coupon rate:
   - To approve the fund coupon rate, click the target fund coupon record and the Approve field is enabled. Select the Approve checkbox and then click **Submit**. The fund coupon status is changed to APPROVED.
   - To reject the fund coupon rate, click the target fund coupon record and then click **Reject**. The fund coupon rate is rejected. You can go to the Fund Coupon Rate Entry page to change the coupon rate.

5. If you want to change the coupon rate after it is approved:
   a. Enter the Fund Coupon Rate Entry page and search out the target fund coupon record.
   b. Select the target fund coupon record. RESULT: The Revise field is enabled.
   c. Change the Coupon Rate, Base Unit, and Coupon Declaration Type if required, and then click the Revise checkbox.
   d. Enter the Fund Coupon Rate Approval page to approve the changed coupon rate.

---

### Process 7: Automatic Switch

The Automatic Switch batch job is used to automatically switch all money from mapping funds to the target funds after the policy passes Investment Delay Period (system date > issue date + investment delay days).

**PREREQUISITE:** N/A

1. System starts the automatic switch batch job to extract the policies to perform Auto Switch after Investment Delay Period.
2. System automatically switches the units from money market fund to target fund.

---

### Process 8: Transfer from MF to CF

The Transfer from MF to CF batch job is used to transfer the fund value from MF to CF after the subscription period of Close Fund is ended.

**PREREQUISITES:**
- User has logged on to the system.
- User has the appropriate privileges to invoke the function.
- System date reaches Start Date - Pre-invest days of the close fund.

1. System starts the Transfer from MF to CF batch job to generate pending fund transaction of switch from MF to CF.
2. After the price of CF is known, the system will run the fund transaction of the pending switch record. The money in MF will be transferred to CF.

---

### Process 9: Fund Settlement

Saving account is settled by guaranteed rate with yearly bonus upon regular settlement of saving account, policy surrender, and terminal claim. The system will accumulate the account interest and capitalize it on each settlement date. In addition, there is yearly bonus to be calculated to the saving account.

**PREREQUISITE:** The saving account is already set up.

1. Define the interest rates which are used in the saving account settlement. See Enter Saving Account Rate.
2. The system calculates the account interest. See Calculate Account Interest.
3. The system calculates the yearly bonus. See Calculate Yearly Bonus.

#### Enter Saving Account Rate

1. From the main menu, select **Investment > Savings Account Rate Entry**.
   RESULT: The Saving Account Rate Entry-Search page is displayed.

2. Select a Product Code which the saving account is attached to, the Saving Account and the Interest Rate Category, then click **Create**:
   - Select Guaranteed rate as the Interest Rate Category to modify the guaranteed rate.
   - Select Settlement rate and Bonus rate as the Interest Rate Category to set the settlement rate and bonus rate respectively.
   RESULT: The Saving Account Rate Entry-Create page is displayed.

3. On the Saving Account Rate Entry page, enter the Rate Effective Date and Interest Rate (%), click **Submit**.
   RESULT: The saving account rate has been defined successfully.

#### Calculate Account Interest

**Account with Yearly Rate, Simple Calculation and without Policy Loan:**
```
End value of account = start value of account * (1 + n/365 * i)
  + Σtop up k * (1 + nk/365 * i)
  + Σpremium k * (1 + nk/365 * i)
  + Σswitch-in k * (1 + nk/365 * i)
  - Σpartial withdraw k * (1 + nk/365 * i)
  - Σswitch-out k * (1 + nk/365 * i)
  - Σcharge deduction k * (1 + nk/365 * i)
```

**Account with Yearly Rate, Compound Calculation and without Policy Loan:**
```
End value of account = start value of account * (1 + i)^(n/365)
  + Σtop up k * (1 + i)^(nk/365)
  + Σpremium k * (1 + i)^(nk/365)
  + Σswitch-in k * (1 + i)^(nk/365)
  - Σpartial withdraw k * (1 + i)^(nk/365)
  - Σswitch-out k * (1 + i)^(nk/365)
  - Σcharge deduction k * (1 + i)^(nk/365)
```

**Account with Daily Rate, Compound Calculation and without Policy Loan:**
```
End value of account = start value of account * (1 + i)^n
  + Σtop up k * (1 + i)^nk
  + Σpremium k * (1 + i)^nk
  + Σswitch-in k * (1 + i)^nk
  - Σpartial withdraw k * (1 + i)^nk
  - Σswitch-out k * (1 + i)^nk
  - Σcharge deduction k * (1 + i)^nk
```

#### Calculate Yearly Bonus

**Variables:**
- Rate i: guaranteed rate
- Rate f: bonus rate
- Amount put in the account k
- Amount taken from the account k

**Bonus amount:**
```
Yearly bonus = start value of last year * [(1+i)(1+f)]^(n/365)
  + Σ amount put in the account k * [(1+i)(1+f)]^(nk/365)
  - Σ amount taken from the account k * [(1+i)(1+f)]^(nk/365)
  - start value of last year * (1+i)^(n/365)
  - Σ amount put in the account k * (1+i)^(nk/365)
  + Σ amount taken from the account k * (1+i)^(nk/365)
```

**Rules:**
- Yearly bonus will be calculated on each policy anniversary date on the basis of all account transactions happened in the last policy year. Bonus rate is declared on the start of each calendar year.
- If system cannot get the rate of the corresponding year, bonus calculation will fail until the rate is ready.
- The allocated bonus will be put back to the original account to increase the principal.
- Upon claim, send 80% bonus of current year to client on the latest declared rate.
- Upon policy surrender, abnormal settlement will not generate the bonus of that policy year.

---

## 10. Batch Jobs

### #### Guarantee Roll Up

The Guarantee Roll Up batch job is used to process VA policies with rollup guarantees. It will recalculate the guarantee amount with defined formulas.

**PREREQUISITES:**
- Charge Deduction batch will run prior to this batch job.
- The product has the guarantee with accumulation type rollup, which is defined in product definition. For details, refer to Parameter List in Product Business Rules.

1. The system starts the Guarantee Roll Up batch job to extract the policies to perform recalculation of the GMxB amount according to the roll up calculation rule.
2. The system updates the GMxB info and generates GMxB transaction info.
3. The system checks if GMxB is GMDB.
   RESULT: If yes, go to step 4; otherwise, the process is ended.
4. The system recalculates SA, and updates the policy information.

---

### #### Guarantee Step Up

The Guarantee Step Up batch job is used to process VA policies with step up/ratchet guarantees. It will recalculate the guarantee amount with defined formulas.

**PREREQUISITES:**
- Charge Deduction batch will run prior to this batch job.
- The product has the guarantee with accumulation type StepUp/Ratchet, which is defined in product definition. For details, refer to Parameter List in Product Business Rules.

1. The system starts the Guarantee Step Up batch job to extract the policies to perform recalculation of the GMxB amount according to the step up calculation rule.
2. The system updates the GMxB info and generates GMxB transaction info.
3. The system checks if GMxB is GMDB.
   RESULT: If yes, go to step 4; otherwise, the process is ended.
4. The system recalculates SA, and updates the policy information.

---

### #### Fund Coupon Allocation

The Fund Coupon Allocation batch job is used to allocate the coupon to the fund under each policy.

**PREREQUISITES:**
- Coupon rate is declared.
- System date >= coupon rate effective date.

1. System starts the Fund Coupon Allocation batch job to extract the policies and allocate the coupon to the fund under each policy.
2. System generates the payment record for those policies whose coupon disposal option is Pay Out.

---

### #### Fund Maturity

The Fund Maturity batch job is used to transfer the fund value from CF/OF to MF after the fund is matured.

**PREREQUISITES:**
- Fund is matured.
- System date reaches End date of the fund.

1. System starts the Fund Maturity batch job to extract the policies.
2. System generates pending selling fund transaction record from the specific fund for those extracted policies.

---

### #### Policy Loan Lapse

The Policy Loan Lapse batch job is used to lapse the policy when the TIV of the investment linked policy is less than policy loan account value.

**PREREQUISITES:**
- TIV <= Policy loan account value.

1. System starts the Policy Loan Lapse batch job to extract the policies.
2. System lapses the extracted policies.
3. System sells all units first and use the amount to repay the outstanding policy loan.

---

### #### ILP Policy Lapse Sell All Units

The ILP Policy Lapse Sell All Units batch job is a daily batch job. It is used to sell all fund units for policies which are lapsed after waiting days.

---

### #### Fund Coupon Alloc-Renew Status

The Fund Coupon Alloc-Renew Status batch job is used to update coupon-status to CONFIRMED in t_fund_coupon table.

---

### #### Insert Cash Flow Temp Table

The Insert Cash Flow Temp Table batch job is used to insert the value of t_ilp_cash_flow, which is the value of Adjustment Gain & Loss from the table t_fund_trans and t_fund_trans_apply with DISTRI_TYPE = 62.

---

### #### Auto Switch ILP Strategy

The Auto Switch ILP Strategy batch job will run daily (including weekend and public holiday). It will select all policies with policy anniversary date equals to the run date. The batch job will auto sell off all funds under that particular policy and reapportion all the funds according to the investment strategy tagged to the policy.

**PREREQUISITES:**
- Run after the Allocation/Encashment of units.
- Run after the Auto Change apportionment of Investment Strategy.
- Auto trigger daily batch job.

1. System starts the Auto Switch ILP Strategy batch job to perform Investment Strategy Switch:
   a. System extracts policies.
   b. System switches the funds according to the Investment Strategy Apportionment.

2. System performs Investment Strategy Cancellation:
   a. System selects policies.
   b. System will nullify the Investment Strategy for that policy.

3. System creates records for generation of Auto Switch Letter (Batch) and Cancel Investment Strategy letter.

---

## Appendix A: Rules

### Upload Fund Price Rules

This section contains rules in uploading fund prices by excel.

1. In the Excel, only Fund Code, Bid Price and Fund Effective Date are required. All other calculations please follow current system.

2. When user clicks Upload, the System checks whether inappropriate information is entered. If checks fail, error messages will be displayed on the screen.

| Condition | System Action |
|-----------|--------------|
| Only the fund which hasn't been priced for selected price effective date can be uploaded. | Upload Fail! Fund XX for Price Effective Date XX/XX/XXXX has been existing, please revise manually. |
| Fund Effective Date entered in the Excel cannot be later than system date minus one day. | Price Effective Date cannot be later than system date minus one day. |
| More than one record of the same fund code and price effective date exist in Excel, thus the Excel cannot be uploaded successfully. | Similar records exist! Please revise manually. |
| Fund code entered in the Excel doesn't exist in current system. | Fund Code entered doesn't exist! |
| Bid Price format should be XXXXXXXXXX.XX. | Upload Fail! Bid Price format is not correct! |
| Price Effective Date format should be DD/MM/YYYY. | Upload Fail! Price Effective Date format is not correct! |
| Price effective date is not a valid date (e.g., 02/13/2014). | Upload Fail! Price Effective Date is not a valid date! |
| User doesn't include all the necessary data in Excel. | Upload Fail! Lack of data! |
| The uploaded file is empty. | Uploaded File cannot be empty! |
| User doesn't select any file but clicks upload. | File does not exist! |
| File format is not XLS or XLSX. | System only supports XLS and XLSX file format, please select file again! |

3. After the Excel is successfully submitted, the fund prices' status will be changed to "Entered".

---

### Fund Transaction Rules

The records pending for fund transaction cover the following information:
- Application type, transaction application time
- Fund code, target fund code, fund name, fund currency
- Pending amount by policy currency, pending amount by fund currency, pending unit
- The Validity Date which is used to determine the Price Used Date. If a price for the Validity Date is not available, the system will get the forward price (next available price) following the Validity Date.

The system validates if current price of the Validity Date (either "Bid" or "Offer" price as indicated in the pending record) is available:
- If a price for the Validity Date is available, then:
  - Price Used Date = Validity Date
  - Price Used = Price of Fund at Validity Date
- Otherwise:
  - Price Used Date = Date where the price is Next Available from the Validity Date
  - Price Used = Next Available price from Validity Date

- Only if "Pending Transaction Allowed" is applied in system configuration, then the forward price will be available and Fund Transaction will be performed when fund price is available.
- T+N Rules will be applied if "Pending Transaction Allowed" is applied. Transaction price will use fund price at T+N days. T refers to the validity Date, N is Calendar Days or Working Days. T+N Rules are defined at fund level.

The system processes transactions based on different alterations:
- The system performs fund transactions in the order of the sequence of generation of pending fund transaction.
- The system calculates the number of units to be bought or sold and then updates the unit holding.
- If the fund price is higher than the value of Buy/Sell and the units calculated after rounding is less than 0.01, no units will be bought or sold.
- If it is a buying at offer price case, the system calculates and generates the record for Bid-Offer spread. Bid-Offer spread = (offer price used - bid price of the date) x units transacted.
- If it is a freelook, the system calculates the profit for the company if actual refund amount is less than the calculated refund amount, and creates related record of refund and the profit.
- If the transaction is generated by Lock In Period Process, system needs to update the premium filling information and move the premium due date or charge due date accordingly:
  a) After confirm pending selling application to deduct the unfilled TP and STU amount of the current due date from fund value of UTU, system will generate pending buying pending transaction to invest deduction amount into TP and STU fund units:
     - Pending Amount = Unfilled premium amount of current due date
     - Transaction Date for buying: Confirm Date of pending selling transaction
     - Price Effective Date: follow T+N rules (T=Transaction Date)
     - Pending amount for TP and STU will be calculated by TP/STU proportion
     - Pending amount for each fund will be calculated by fund proportion for TP and STU.
     - In case of fund price decrease and the fund value of UTU is insufficient to cover the deducted amount:
       - System will deduct the insufficient amount from the fund value of TP and STU in case the fund is the same as UTU.
       - If the fund value of TP and STU are still not sufficient to cover the deducted amount, the System will deduct which it can be deducted.
  b) After confirm pending buying application to deduct the unfilled TP and STU amount of the current due date from fund value of UTU, system will automatically fill up bucket filling information and move premium due date.
  c) After confirm pending selling application to deduct non-allocation charge, system will automatically fill up bucket filling information and move charge due date.
- In case that fund price decrease and total fund value are insufficient to cover the deducted amount, system will deduct the units to negative and also record insufficient amount as the debts on the policy.
- If the transaction is Increase/Decrease Premiums and Top-up:
  - The system re-calculates the sum assured for the main product (based on product definition) and updates the sum assured.
  - If the sum assured after recalculation is greater than the maximum sum assured or less than the minimum sum assured defined, the system updates the sum assured directly to the maximum sum assured or minimum sum assured.
- If transaction is for partial withdrawal:
  - The system re-calculates the sum assured for the main product (based on product definition).
  - If all the remaining units of the fund are not enough to fulfill the withdrawal amount request, the system changes the application status to Suspend and generates Exception Report.
- If transaction is for switch:
  - If switch is by value and the units are not sufficient to fulfill the amount, the system will auto switch all the units under that fund and transact the switch fee first and generate the related report.
  - If the switch fee is deducted from fund and the switch is by units, the system deducts the switch fee from switch-out fund, and uses the amount after deduction to buy the units for switch-in fund. The switch fee should be allocated for each switch-in fund by the switch in units apportionment if there is more than one switch-in fund for one switch-out fund. At the same time, the system generates the fee record for switch fee.
    NOTE: The number of switch times free of charge is defined by product parameter Times of Free Switch per Period. If the number is exceeded, switch fee is calculated by formula and the minimum switch fee is defined by product parameter Min Switch Fee Amount per Occurrence. Whether the switch fee is deducted from switch-in or out fund is defined by product parameter Fee Source.
    For example, switch 1000 units from Fund A to Fund B and 500 Units to Fund C, the switch fee is 25 for Fund A, the bid-price at the validity date of the switch is 2$, then the system should sell 1000 units and deduct the switch fee (25/1500*1000) from the value of 1000 units and buy the units for Fund C; the system should sell 500 units and deduct the switch fee (25/1500*500) from the value of 500 units and buy units for Fund B.
  - System also should transact the switch fee record.
  - If the switch is an auto switch, the system will sell all the units of each fund, and buy units based on the apportionment of investment strategy.
  - If the switch is an auto switch, any one of the generated transaction that cannot be transacted will cause rollback of all the transactions for the same auto switch application.
  - If the switch is by amount, the system sells the unit of the source fund according to the fund transaction application generated, deducts the switch fee if it is deducted from the fund and generates the fee record for switch fee, and then exchanges the amount available (amount applied-switch fee deducted) from source fund currency to target fund currency, using the real time exchange rate on the system date.
- If the switch fee is defined at product level in product definition:
  - Policy Holder will be allowed several free times for ad hoc fund switch per predefined period. Subsequent switches within period will be charged at switch fee respectively. Period and the switch fee amount are parameterized and defined at product definition.
  - The Switch fee cannot be amended by user.
  - Switch Fee will be applicable at policy level and one event will be considered as one switch.
  - Settlement for switch fee will be allowed by cash, cheque or unit deduction. For settlement by unit deduction, the switch fee amount will be inclusive of the units to be switched out from.
- If the switch fee is defined at fund level, to be deduct from the fund by percentage of the switch amount:
  - If Switch Fee Calculation Basis is per switch-in at fund level, then the switch fee should be calculated using the switch fee rate defined at Product-fund Level.
  - System should display the estimated switch fee value based on the switch fee rate defined under switch-in funds; switch fee amount of each fund = switch fee rate * switch amount; total switch fee = sum of switch fee amount of each fund.
  - In fund transaction, after system sells the switch-out funds, system will deduct the switch fee first and purchase switch-in funds.
- Switch fee deduction rules:
  - Switch fee calculation formula is defined in Formula instead of product definition. Please see FMS list in product definition for switch fee formula.
  - Switch fee deduct source is defined in product definition of ILP charge list. Deduction from switch-in fund or switch-out fund for both switch by amount and by unit.
  - If the fee source is deduction from switch-out fund, the switch fee will be deducted from switch-out fund according to calculation formula. System will generate one transaction for each fund switch. In fund transaction, after system sells the switch-out funds, system will deduct the switch fee first and purchase switch-in funds.
  - If the fee source is deduction from switch-in fund, all the amount or unit will be used for buying fund switched in. And the switch fee will be deducted from switch-in fund. There will be two fund transaction applications for each fund transaction: transaction application for switch and transaction application for switch charge from each switch-in fund.

---

### Allow/Not Allow Pending Transaction Rules

System supports both Pending Transaction Allowed and Pending Transaction Not Allowed process.
- If Pending Transaction Not Allowed, then alterations with Sell fund transaction and Switch fund transaction are not allowed to be performed before pending transactions are settled.
- If Pending Transaction Allowed, then alterations with Sell fund transactions and Switch fund transactions are allowed, and controls or calculations need to consider those pending transactions.

Take ILP Partial Surrender as an example:
- If Pending Transaction Not Allowed, then Partial Surrender cannot be performed.
- If Pending Transaction Allowed, then min/max Partial Surrender amount and Remaining amount after Partial Surrender need to consider pending transactions, for example, existing total fund value - pending withdraw/switch out amount + pending buying/switch in amount ≥ Min Remaining Amount.

For charge deduction batch:
- If Pending Transaction Not Allowed, then charge deduction and fund transaction will be performed at the same time when the fund price is available.
- If Pending Transaction Allowed, then pending transaction will be generated by charge deduction batch and fund transaction will be performed when the fund price is available.

T+N Rules are normally applied if Pending Transaction Allowed. Transaction price will use the fund price at T+N days.
- T refers to Valuation Date of transactions and normally it is equal to Customer Service validity date. For example, T for partial surrender is the Validity Date of Partial Surrender, while T for Fund Switch is the Validity Date of Fund Switch.
- Ad-hoc Single Top up uses the later one between Validity Date and Money Come In Date as the T date to apply T+N pricing rules.

For charge deduction, there are two options:
- T will be Charge Due Date
- T will be Charge Due Date - N

T can be calendar days or working days.
T+N Rules are defined at fund level. For example, Fund A is defined as T+3, while Fund B is defined as T=1. So for the same transaction, it is possible that some fund prices are available but others are not.

In case of Buying Transactions, those funds with fund price available will be transacted first and others will be performed until their fund prices are available. For example, investment of regular premium, single top up, etc.
In case of Selling Transaction, system will wait until all fund prices are available then the whole transaction will be performed together.

---

### Logic Rules

- As for policy in-force, no matter when the initial payment is collected, system regards the collection is on the policy commencement date and compulsory to fill in the first bucket. Then system checks the future filling option to settle the remaining money.
- After policy in-force, the collected money is first assigned to offset outstanding premium and operation fee such as cash rider premium, CS fee, and then the remaining fills in buckets.
- As for bucket filling, system checks the past buckets filling and then future bucket to settle the incoming money.
- Any excess money after bucket filling is regarded as ad hoc top-up and assigned to the accounts on the requested allocation rate at New Business stage (first follow New Business ad hoc top-up allocation, if not exist, follow regular premium allocation).
  - The customer service item ILP Ad-hoc Single Premium Top-up does not change the extra allocation fund, which means it follows New Business.
  - The customer service item ILP Change Premium Appointment changes the extra allocation, which means it will be followed by extra top-up allocation.
- For a specific bucket, if client requests for recurring top-up, the target premium will be satisfied first and then recurring top-up.
- Recurring top-up of past bucket will be ignored if additional bucket filling option is fill by sequence.
- System allows to fill partial installment bucket.
- **Tolerance for bucket filling:**
  - If tolerance is allowed (defined in the table t_ilp_bucket_tolerance), the bucket filling due date will be moved in any of the following conditions:
    - The difference between actual target premium and target premium is within the tolerance limit. The difference will be set as the target premium tolerance.
    - The difference between actual recurring top up and recurring top up is within the tolerance limit. The difference will be set as the recurring top up tolerance.
  - Parameter BUCKET_FILLING_TOLERANCE_OPTIONS is used to define the bucket filling rule for the bucket with tolerance.
    - After the bucket filling due date move with tolerance, if the value of BUCKET_FILLING_TOLERANCE_OPTIONS is Y, when there is new premium coming, the premium will be allocated for the bucket filling due date.
    - After the bucket filling due date move with tolerance, if the value of BUCKET_FILLING_TOLERANCE_OPTIONS is N, when there is new premium coming, the premium will be allocated to the tolerance first and then allocated for the bucket filling due date.

---

### Adjust Unit Rules

This section tells the rules in adjusting unit.

- When clicking Search on the Unit Adjustment page, the system does validation for the Policy No. entered in the search criteria:
  a) The system validates if the current policy status is Inforce. If not, the system gives an error message: "Policy status is not inforce."
  b) The system validates if the policy has been suspended by other transaction. If yes, the system gives an error message: "Policy xxx has been frozen. Please query by the policy number and check with CS or Claim."

- When users entered for Price Effective Date for Adjustment and move cursor to next on the Unit Adjustment page:
  The system validates this date should have confirmed fund price, otherwise, the system gives an error message: "Fund Code: xx on dd/mm/yyyy has no confirmed price."

- When clicking Submit on the Unit Adjustment page:
  a) The system validates if the Current Unit balance + Units to Adjust >= 0. Otherwise, the system gives an error message: "Current Unit Balance + Units to Adjust should be more than or equal to zero."
  b) The system validates the Price Effective Date for Adjustment cannot be later than Adjustment Date. Otherwise, the system gives an error message: "'Price Effective Date for Adjustment' cannot be later than 'Adjustment Date'."

---

### Automatic Switch Rules

This section tells the rules in automatic switch.

**Policy extraction conditions:**
- Policy status is in-force.
- Policy is not frozen by CS or Claim.
- System Date > Issue Date + Investment Delay Period.
- The policy has money to be invested in target fund but it is kept in mapping funds because of free look period.

**Switching rules:**
System will sell all money in mapping funds and invest into target funds:
a) If system is configured as "Allow pending fund transaction", then pending fund transaction records will be generated for selling and buying.
b) Fund Price date will apply T+N rule (transaction date + N days defined according to different fund).
c) If system is configured as "Apply Fund Premium Stream", then switched out money from different premium stream will be moved to target funds accordingly.

For example:

| Table 3: Before Automatic Switch | | |
| Money Market Fund | Regular Premium | 1000 | 01/01/2013 |
| | Ad-hoc Top Up | 5000 | 15/01/2013 |
| | Regular Top Up | 800 | 01/01/2013 |

| Table 4: After Automatic Switch | | |
| Fund A (Apportionment: 60%) | Regular Premium | 600 | 01/01/2013 |
| | Ad-hoc Top Up | 3000 | 15/01/2013 |
| | Regular Top Up | 480 | 01/01/2013 |
| Fund B (Apportionment: 40%) | Regular Premium | 400 | 01/01/2013 |
| | Ad-hoc Top Up | 2000 | 15/01/2013 |
| | Regular Top Up | 320 | 01/01/2013 |

---

### Transfer from MF to CF Rules

This section tells the rules in Transferring from MF to CF.

**PREREQUISITES:**
- Policy is without pending fund transactions.
- Policy is having investment to the Close Fund, and investment amount is put in the corresponding Money Fund currently.

**Transferring rules:**
System will validate with the following rules to proceed with the transferring:
a) The sum of the total investment amount in MF under the extracted policies which is intended to invest into close fund is more than the min investment amount of the close fund.
   NOTE: The system will use the original investment amount for validation, no matter whether price of MF goes down or not.
b) The sum of the total investment amount in MF under the extracted policies which is intended to invest into close fund is less than the min investment amount of the close fund.
   NOTE: If not, the system will extract the policies whose investment amount in MF is within the limit of Max investment amount.
c) If money from various policies come in on the same day for the same fund, which causes the maximum investment limit for the fund to be exceeded, money will be accepted in the following order (source of money): New premium; Top-up; Switch in amount.
d) Switch units = all units in the Money Fund which are intended to invest into Close Fund.
e) Apply date will use the date of fund start date - pre-invest days.

---

### Saving Account Rate Entry Rules

This section tells the rules in saving account rate entry.

**Rules for mandatory fields:**
The entered format of rate effective date is dependent on the rate category:
- If category = guaranteed rate, enter the date by format 'ddmmyyyy'.
- If category = settlement rate or special settlement rate, enter the date by format 'mmyyyy'.
- If category = bonus rate, enter the date by format 'yyyy'.

Enter the interest rate via percentage and round to 2 decimal digits.

**Rules for validation:**
The system performs the following check to validate the entered information; if fail to pass, it will pop up the error message.

| Condition | System Action |
|-----------|--------------|
| Mandatory fields are completely entered. | Error message: "Please enter the field." |
| Match the rate effective date with settlement frequency, when defining the settlement rate and special settlement rate. If settlement frequency = monthly, user can define the rate of each month. If settlement frequency = quarterly, user can only define the rate of Jan, Apr, Jul and Oct. | Error message: "The entered month should be Jan, Apr, Jul or Oct." |
| If settlement frequency = half yearly, user can only define the rate of Jan and Jul. | Error message: "The entered month should be Jan or Jul." |
| If settlement frequency = yearly, user can define the rate of Jan only. | Error message: "The entered month should be Jan." |
| The interest rate is unique in the system. | Error message: "There is the same record in the system, please check." |

---

### Guarantee Roll Up Rules

This section tells the rules in Guarantee Roll Up.

**PREREQUISITES:**
- The policy is VA policy with GMxB and accumulation type is Roll Up.
- Policy is not frozen, status is Inforce.
- Policy has no pending transactions.
- Policy is not within annuity payout period.
- Policy is not within withdrawal period if GMxB is GMWB.
- Batch processing date is >= policy anniversary date.
- Batch processing date is > the last capitalization date.

**GMxB calculation rules:**
Trigger: yearly, at each policy anniversary day till payout period start or Death Claim.

- If no any alterations:
  GMxB1 = GMxB0 * (1+i)
  GMxB2 = GMxB1 * (1+i)
  GMxB3 = GMxB2 * (1+i)
  ...
  ( *i is fixed rate defined in product)

- If Partial Withdraw:
  GMxB after withdrawal = GMxB (before withdrawal) * (1+i)^(d/365) - Withdraw Amount.
  And GMxB at policy anniversary date will be [GMxB (before withdrawal) * (1+i)^(d/365) - Withdraw Amount] * (1+i)^((365-d)/365).

- If Single Top Up:
  GMxB after Single Top Up = GMxB (before Single Top Up) * (1+i)^(d/365) + Single Top Up Amount.
  And GMxB at policy anniversary will be [GMxB (before Single Top Up) * (1+i)^(d/365) + Single Top Up Amount] * (1+i)^((365-d)/365).

---

### Guarantee Step Up Rules

This section tells the rules in Guarantee Step Up.

**PREREQUISITES:**
- The policy is VA policy with GMxB and accumulation type is Step Up/Ratchet.
- Policy is not frozen, status is Inforce.
- Policy has no pending transactions.
- Policy is not within annuity payout period.
- Policy is not within withdrawal period if GMxB is GMWB.
- Batch processing date is >= policy anniversary date.
- Batch processing date is > the last capitalization date.

**GMxB calculation rules:**
Trigger: each X policy year (X is defined in product definition), till payout period starts or Death Claim.

- If no any alterations:
  GMxBt = GMxB0 (0 < t < X-1)
  And at the Xth policy anniversary date:
  GMxBx = Max(TIV, GMxBx-1 * (1+i))
  ( *i is fixed rate defined in product)

- If Partial Withdraw:
  GMxB after withdrawal = TIV after withdrawal / TIV before withdrawal * GMDB before withdrawal.
  And GMxB at policy anniversary date will be GMxBt = Max(TIV, TIV after withdrawal / TIV before withdrawal * GMxB before withdrawal) * (1+i).

- If Single Top Up:
  GMxB after Single Top Up = GMxB before Single Top Up + Top Up Amount.
  And GMxB at t anniversary year will be GMxBt = Max(TIV, GMDB after Single Top Up * (1+i)).

---

### Fund Coupon Allocation Rules

This section tells the rules in Fund Coupon Allocation.

**PREREQUISITE:** Policy is having investment to the specific fund.

**Allocation rules:**
a) If the coupon disposal option is pay out and coupon rate is declared by unit: The amount to pay out for the policy = Fund Price * X * Total No of Units / Base Unit.
b) If the coupon disposal option is pay out and coupon rate is declared by amount: The amount to pay out for the policy = Y * Total No of Units / Base Unit.
c) If the coupon disposal option is reinvest and coupon rate is declared by units: The coupon units allocated = X * Total No of Units / Base Unit.
d) If the coupon disposal option is reinvest and coupon rate is declared by amount: The coupon units allocated = (Y * Total No of Units / Base Unit) / Fund Price.

NOTE: Fund Price will be the bid price as at coupon rate effective date. X: coupon rate of X units/Base units. Y: coupon rate of amount Y/Base units. Total No of units will be the exact no of units under the policy regardless of pending fund transaction. Close fund is always using the option of pay out.

---

### Fund Maturity Rules

This section tells the rules in Fund Maturity.

**PREREQUISITES:**
- Policy is un-frozen.
- Policy is having investment to the specific fund.
- Policy is without pending fund transactions for the specific fund.

**Generating pending selling fund transaction record rules:**
a) Switch units = all units in the specific fund.
b) Apply date will use the date of fund end date.

---

### Policy Loan Lapse Rules

This section tells the rules in Policy Loan Lapse.

**PREREQUISITES:**
- Policy is Inforce and un-frozen.
- Policy is an ILP, VUL or UL policy.
- There is no pending fund transaction under the policy.
- TIV <= Total policy loan account value.
- The latest known price will be used to calculate TIV.
- System date will be used to calculate total policy loan account values.

**Lapse rules:**
a) System sets the policy and benefit status to Lapse.
b) Lapse date = system date.
c) Lapse reason = Policy Loan Lapse.

---

### Auto Switch ILP Strategy Rules

This section tells the rules in Auto Switch ILP Strategy.

**Rules in policy extraction in Investment Strategy Switch:**
- If the strategy type is Normal:
  - Strategy Due Date must be equal to or before today's date.
  - Policy status is Inforce and not frozen.
  - Policy is an ILP policy.
  - Policy has a valid Investment Strategy code.
  - Policy has not any pending fund transaction.
- If the strategy type is DCA, system needs to validate the following extra information:
  - Strategy effective date < Strategy due date < Strategy end date.
  - Invest amount <= TIV.

**Rules in switching the funds:**
1. System creates pending transactions to sell all the funds under that particular policy and use a certain transaction code to show that it is an auto switch. Use the bid price of the anniversary date.
2. Strategy Due Date is derived based on the policy anniversary date and will be updated to next anniversary date later than current one.

**Rules in selecting policies in Investment Strategy Cancellation:**
- Strategy Due Date must be equal to or before today's date.
- Policy status is Lapsed and not frozen.
- Policy is an ILP policy.
- Policy has a valid Investment Strategy code.

**Rules in nullifying the investment strategy:**
- If the strategy type is normal, system updates strategy code to specify the cancelled status of strategy.
  If the strategy type is DCA, system sets the strategy status to inactive.
- System will not nullify the apportionment of the regular premium and recurring top up. Thus the apportionment of the regular premium and recurring top up premium will remain according to the strategy defined for that policy calendar year. Policy calendar year means policy year based on system date.

---

### ILP Premium Stream Configuration Rules

For ILP product regular premium stream, whether to continue regular premium stream or not can be configured through the system parameter 2062410001-INCR_WITH_INACTIVE_STREAM.

- If the parameter value is N, system will continue the regular premium stream.

For example: policy A, commencement date 2000-1-1, regular premium 10000:

1.
   a) 2000-11-1, system performs premium decrease from 2001-1-1 from 10000 to 8000.
   b) 2001-1-1, system performs renewal for the policy, renewal premium is 8000.
   c) System will deduct expense fee using the rate of second year.

2.
   a) 2001-10-1, system performs premium decrease from 2002-1-1 from 8000 to 13000.
   b) 2002-1-1, system performs renewal for the policy, renewal premium is 13000.
   c) For 8000 part, system will use third year's expense rate to deduct expense fee.
   For 2000 part, system will use second year's expense rate to deduct expense fee.
   For 3000 part, system will use first year's expense rate to deduct expense fee.

- If the parameter value is Y, system will not continue the regular premium stream.

For example: policy B, commencement date 2000-1-1, regular premium 10000:

1.
   a) 2000-11-1, system performs premium decrease from 2001-1-1 from 10000 to 8000.
   b) 2001-1-1, system performs renewal for the policy, renewal premium is 8000.
   c) System will deduct expense fee using the rate of second year.

2.
   a) 2001-10-1, system performs premium decrease from 2002-1-1 from 8000 to 13000.
   b) 2002-1-1, system performs renewal for the policy, renewal premium is 13000.
   c) For 8000 part, system will use third year's expense rate to deduct expense fee.
   For 5000 part, system will use first year's expense rate to deduct expense fee.

---

## INVARIANT Declarations

**INVARIANT 1:** Fund transactions are only processed using an approved NAV for the transaction date.
- Enforced at: Fund Transaction processing
- If violated: Transaction would use unapproved price; accounting error

**INVARIANT 2:** Units are always calculated as Transaction Amount divided by NAV.
- Enforced at: Fund Transaction unit calculation
- If violated: Incorrect number of units allocated

**INVARIANT 3:** Lock-in period restrictions are enforced at transaction time.
- Enforced at: Switch/Withdrawal during lock-in
- If violated: Premature withdrawal; higher charges not collected

**INVARIANT 4:** Gain/loss calculation uses average purchase price for units acquired at different NAVs.
- Enforced at: Calculate Gain and Loss
- If violated: Incorrect capital gain/loss reported

**INVARIANT 5:** Unit adjustments require authorization and are recorded in the audit log.
- Enforced at: Adjust Unit
- If violated: Unauthorized changes to unit holdings

**INVARIANT 6:** Coupon allocation uses bid price as at coupon rate effective date regardless of pending fund transactions.
- Enforced at: Fund Coupon Allocation
- If violated: Incorrect coupon amount allocated

**INVARIANT 7:** TIV for policy loan lapse is calculated using the latest known price; policy loan account value uses system date.
- Enforced at: Policy Loan Lapse batch
- If violated: Incorrect lapse trigger

---

## Field Reference Tables

### Unit Adjustment Page Fields

| Field Name | Mandatory | Description |
|---|---|---|
| Units to Adjust | Y | Units to be adjusted to the current unit balance. Positive value adds units; negative value reduces units. Current Unit Balance + Units to Adjust cannot be smaller than 0. |
| Gain & Loss Impact | N | If selected, the fund will affect gain and loss; if not selected, the fund will not affect gain and loss. |
| Price Effective Date for Adjustment | Y | Date when the adjustment takes effect. Cannot be later than Adjustment Date. Must have a confirmed fund price. |
| Reason for Adjustment | Y | Reason why the adjustment is made (e.g., typo error). |

### Fund Transaction Key Fields

| Field Name | Description |
|---|---|
| Fund Code | Fund identifier |
| Target Fund Code | Destination fund for switch transactions |
| Pending Amount (Policy Currency) | Transaction amount in policy's currency |
| Pending Amount (Fund Currency) | Transaction amount in fund's currency |
| Pending Unit | Number of units for the transaction |
| Validity Date | Date used to determine Price Used Date |
| Price Used Date | Actual date of the fund price used |
| Price Used | Fund price actually used for the transaction |
| Transaction Type | Buy / Sell |
| Transact By | Units / Value |
| Price Type | Bid / Offer |
| Price Mode | Forward / Now |

### Fund Coupon Rate Fields

| Field Name | Mandatory | Description |
|---|---|---|
| Coupon Rate Effective Date | Y | Date from which the coupon rate applies |
| Fund Code | Y | Fund identifier |
| Coupon Rate | Y | The declared coupon rate |
| Base Unit | Y | Base unit for coupon calculation |
| Coupon Declaration Type | Y | By Amount or By Unit |

### Saving Account Rate Fields

| Field Name | Mandatory | Description |
|---|---|---|
| Product Code | Y | Product code the saving account is attached to |
| Saving Account | Y | Saving account identifier |
| Interest Rate Category | Y | Guaranteed rate / Settlement rate / Bonus rate |
| Rate Effective Date | Y | Date from which the rate applies (format varies by category) |
| Interest Rate (%) | Y | Interest rate as percentage, rounded to 2 decimal digits |

---

## Config Gaps Commonly Encountered

| Config Item | Level | Notes |
|------------|-------|-------|
| NAV tolerance (%) | Global | Maximum deviation from previous NAV |
| Bid-offer spread | Fund / Product | Applied on every switch |
| Switching charge | Product | Per switch or annual limit |
| Lock-in period | Product / Fund | Years during which switch/withdrawal restricted |
| Minimum switch amount | Product | Below this amount, switch not permitted |
| Automatic switch schedule | Product | Pre-defined dates and funds |
| Saving account interest rate | Product | Rate for capital guarantee account |
| Yearly bonus rate | Product | Bonus declared annually |
| T+N pricing rules | Fund | Calendar days or working days |
| Pending Transaction Allowed | System | Controls forward pricing and pending transaction handling |
| BUCKET_FILLING_TOLERANCE_OPTIONS | Product | Controls bucket filling with tolerance |
| 2062410001-INCR_WITH_INACTIVE_STREAM | System | ILP premium stream continuation control |

---

## Menu Navigation Table

| Action | Path |
|---|---|
| Enter Fund Price | Investment > Fund Price > Entry > New or Revise |
| Suspend Fund Price | Investment > Fund Price > Entry > Suspend |
| Unsuspend Fund Price | Investment > Fund Price > Entry > Unsuspend |
| Approve Fund Price | Investment > Fund Price > Approve |
| Adjust Unit by Policy | Investment > Adjust Unit |
| Adjust Unit by Batch | Investment > Batch Correct Price |
| Enter Fund Coupon Rate | Investment > Coupon Rate > Entry |
| Approve Fund Coupon Rate | Investment > Coupon Rate > Approve |
| Saving Account Rate Entry | Investment > Savings Account Rate Entry |

---

## Related Files

| File | Relationship |
|------|-------------|
| ps-fund-administration.md | Current version fund administration |
| ps-investment.md | Current version investment rules |
| insuremo-v3-ug-nb.md | NB — ILP investment strategy setup |
| insuremo-v3-ug-loan-deposit.md | Loan and deposit accounts |
| insuremo-v3-ug-claims.md | Claims fund payouts |