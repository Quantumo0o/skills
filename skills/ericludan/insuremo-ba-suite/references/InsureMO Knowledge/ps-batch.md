| # | Batch Job |
|---|-------------|
| 1 | Auto Convert Payment Frequency  |
| 2 | Auto Cancel Premium Holidayv0.1 |
| 3 | Auto Premium Holidayv0.2 |
| 4 | Auto Suspense Refund |
| 5 | Cpf Projection Send |
| 6 | Cpfb Projection Request |
| 7 | Cs Auto Inforce Jobv0.1 |
| 8 | Cancel Cb Sb Payment |
| 9 | Cb Sb Opt1 Batch Payment |
| 10 | Change Policy Hps Exemption Job |
| 11 | Claim Installment Payment |
| 12 | Deposit And Loan Account Interest Settlement And Capitalize |
| 13 | Extract Cross Age Job |
| 14 | Fund Dividend Allocation & Confirmation |
| 15 | Fund Transaction Job-Enhancement |
| 16 | Ilp Lapse Rider |
| 17 | Loyalty Bonus Allocation |
| 18 | Maturity Letter Job |
| 19 | Maturity Notice Job |
| 20 | Maturity Auto Pay Out |
| 21 | Pay Maturity |
| 22 | Policy Auto Surrender |
| 23 | Policy Maintenance Fee Refund Allocation |
| 24 | Power Up Bonus Allocation |
| 25 | Rsp Renew Confirmation |
| 26 | Rsp Renew Extraction |
| 27 | Regular Withdrawv0.1 |

---

# Batch Jobs Knowledge Base

Generated from Gemini Batch Guide PDFs (27 files)

---

## Auto Convert Payment Frequency 

### Description
From Xth Policy Anniversary onwards, premium on specific rider shall be paid annually. The basic plan will be fully paid, while the rider is regular premium and payment frequency will be automatically changed to annually from start of (X+1)th policy year.

### Acronyms
| Term | Description |
|------|------------|
| NDD | Next Due Date |

### Prerequisites
- • Policy is inforce.
- • The main benefit's premium status is fully paid.
- • If the policy has other optional riders and riders' status is inforced, the premium status
- • The new payment frequency is pre-defined on product configuration and new rate
- • Months between premium next due date and commencement date is equal to Policy

### Procedures
- • Updates the rider's payment frequency to new payment frequency.
- • If the rider is a parent benefit which has other optional riders under it and rider status
- • For main benefit and other optional riders, system doesn't update the payment
- • Updates the rider's payment frequency to policy level's payment frequency, display
- • Updates the rider's installment premium and outstanding premium based on new
- • If there're pending billing records, system cancels the original billing records and

### Configuration
Main Product Code Rider Code Policy Month Effective Date New Pay Mode Living ‘2000-01-01... LivingXcite Enhancer 180 2099-01-01 Y • Policy month is calculated based on new premium date and commencement date • Effective Date is validated based on commencement date

## Auto Cancel Premium Holidayv0.1

### Description
This document describes the daily batch job to auto cancel premium holiday for eligible policies.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |

### Prerequisites
- • Policy status is Inforce
- • Policy Premium Status is Regular
- • Policy is an ILP policy
- • Policy does not have Potential Lapse Date
- • Policy does not have miscellaneous debts
- • The Premium Holiday status is Yes
- • System Date >= Premium Holiday End Date
- • Policy is not suspended by other transactions

### Configuration
NA

### User Cases
- • Preconditions:
- • Process date & expected results:

## Auto Premium Holidayv0.2

### Description
This document describes the daily batch job that verifies whether the policy is eligible to auto set premium Holiday. If yes, deduct premium holiday charge if any and set premium holiday indicator as Yes with start date and end date. Otherwise, set PLD at end of grace period.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |
| APH | Auto premium holiday |
| PH | Premium holiday |

### Prerequisites
- • Policy is inforce.
- • Policy is not frozen.
- • The main product is an ILP product and is allowed to process APH in product
- • Premium Status is Regular.
- • Policy doesn’t have Potential Lapse Date.
- • System Date>= Premium Due Date + Grace Period (including Additional Grace
- - When the account value is sufficient to cover the premium holiday charge from
- • Deduct the premium holiday charge from premium due date to charge due
- • If the Allowed Premium Holiday Months are not enough to cover a whole
- - When the account value is insufficient to cover the premium holiday charge, system

### Configuration
NA

### User Cases
- • Preconditions:
- • Process date & expected results:

## Auto Suspense Refund

### Description
Under some business scenarios, insurer may require to auto refund the balance remain within the policy suspense account (such as for terminate/lapsed policies). Gemini provide a series batch jobs offer this auto suspense refund functionalities for different type’s policies. This document describes the logic for those batch jobs, including (1) FN DwP Suspense Refund It is the batch job use to auto refund the suspense for withdrawn, postponed or declined proposals. (2) FN In Force Suspense Refund If the initial premium collected is over paid than inforcing premium required (e.g. due to UW down sell decision), this batch job will auto refund the general suspense balance after policy taking inforce. (3) FN Termination Suspense Refund It is the batch job use to auto refund the suspense for terminated policies. (4) FN Lapse Suspense Refund It is the batch job use to auto refund the suspense for lapsed policies.

### Acronyms
| Term | Description |
|------|------------|
| Step | 1: System extract the policies fulfill batch criteria. |
| <Confidential> | eBaoTech Corporation Page 6 of 10 |
| Step | 2: Process the policies within the batch job, generate refund payment record (F32) based |
| on | the batch logic. |
| Process | ends. |
| Remark: | After the payment record is generated, it will follow the remaining payment process to |
| perform | the real payout based on the disbursement method. (Refer to User Guide of Payment |
| Module | for more details. |
| Basic | Information |
| Job | Name FN DwP Suspense Refund |
| proposals | (if there is any misllesous money comes in and put into the suspense of the policy). |
| Depend | Job The batch job should be triggered after following job finished: |
| Name | - Claim Installment Payment |
| Batch | Logic |

### Configuration
NA

## Cpf Projection Send

### Description
This document describes how to extract the projection request records and generate projection file for main shield policies and send to CPFB.

### Acronyms
| Term | Description |
|------|------------|
| CPFB | Central Provident Fund Board |

### Prerequisites
- • Projection request records of NBU, CS and premium renewal has been generated by batch

### Business Rules
| Rule | Description |
|------|-------------|
| BR_001: Specification
of projection | 1. Header Record |
| BR_002: File name
convention | PMIW043_PMIW043F.TXT for every time |
| File name format: PMIW043_PMIW043F_ CHKSM _YYYYMMDD.TXT
Refer to BR_004 for the checksum file generation logic, Downstream will
validate the data file based on the checksum logic.: Checksum
data file |  |
| BR_004: CheckSum
logic |  |

### Configuration
NA

### User Cases
- • Preconditions:
- • Process date & expected results:

## Cpfb Projection Request

### Description
This document describes following batch PolicyCpfRequestExtractBatch to generate CPFB projection transaction records.

### Acronyms
| Term | Description |
|------|------------|
| CPFB | Central Provident Fund Board |
| Shield | main policy The policy with the main product as a Shield main product. |

### Configuration
NA

### User Cases
- • Preconditions:
- • Process date & expected results:

## Cs Auto Inforce Jobv0.1

### Description
This document describes the daily batch job to auto inforce CS alteration for eligible transactions.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |

### Prerequisites
- • The application status is Approved.
- • Sufficient collection is received for the policy alteration.

### Configuration
NA

### User Cases
- • Preconditions:
- • Process date & expected results:

## Cancel Cb Sb Payment

### Description
This document describes the daily batch job for Cancel Cb sb payment.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |

### Business Rules
| Rule | Description |
|------|-------------|
| BR_001 |  |

### Configuration
NA

### User Cases
- • Preconditions:
- • Process date & expected results:

## Cb Sb Opt1 Batch Payment

### Description
This document describes the daily batch job for Cb sb opt1 Batch payment.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |

### Procedures
- 7 Business Rules for detail rules.

### Business Rules
| Rule | Description |
|------|-------------|
| BR_001: Payment Amount | Payment amount after batch ‘'Cb sb opt1 Batch payment', refer
to CB/SB allocation amount. |

### Configuration
NA

### User Cases
- • Preconditions:
- • Process date & expected results:

## Change Policy Hps Exemption Job

### Description
This document describes batch job process to change policy HPS exemption after HPS exemption file upload and check passed.

### Acronyms
| Term | Description |
|------|------------|
| PDD | Policy Due Date |
| CS | Customer Service |

### Prerequisites
- • HPS exemption file is uploaded to core system successfully.
- • Exist HPS approved status is uploaded.

### User Cases
- • Preconditions:
- • Process date & expected results:

## Claim Installment Payment

### Description
This document describes the daily batch job to generate the claim installment payment payable record and actual payment record.

### Prerequisites
- • Claim installment plan has been made and batch process date ≥ installment due date

### Configuration
NA

### User Cases
- • Preconditions:
- • Process date & expected results:

## Deposit And Loan Account Interest Settlement And Capitalize

### Description
This document describes the daily batch job to extract policy with account(Deposit or Loan) to settle interest and/or capitalize interest balance to principle per configuration.

### Acronyms
| Term | Description |
|------|------------|
| CB | Cash Bonus |
| SB | Survival Benefit |
| APA | Advanced Premium Account |
| PL | Policy Loan |
| APL | Automatic Policy Loan |

### Prerequisites
- 1 The policy is in force
- 2 This policy is not frozen
- 3 There is at least one in force product with deposit account type of CB, SB, APA (Refer to
- 4 The current deposit account value plus interest (Deposit account value = deposit
- 5 There is at least one policy anniversary date (Refer to Account Capitalization frequency,

### Configuration
t_policy_account_type 1) Deposit Account Type: Cash Bonus, Survival Benefit or APA 2) Loan Account Type: APL or PL 3) Interest Calculation Type: 2 - Simple or 1 - Compound 4) Interest Calculation/Posting Frequency: 5 - Daily, 4 - Monthly, 3 - Quarterly, 2 - Half- Yearly and 1 - Yearly 5) Account Capitalization Frequency: 5 - Daily, 4 - Monthly, 3 - Quarterly, 2 - Half- Yearly and 1 - Yearly 6) Interest Calculation/Posting Due Type: Calendar End, Policy Due a. 1 - Calendar End: Due date to align to Calendar date b. 2 - Policy Due: Due date to align to policy date, based on policy commencement date 7) Account Capitalization Due Type: Calendar End, Policy Due a. 1 - Calendar End: Due date to align to Calendar date b. 2 - Policy Due: Due date to align to policy date, based on policy commencement date 8) Interest Rate Type: 1 - Creation Date, 2 - Due Date <Confidential> eBaoTech Corporation Page 8 of 10 Gemini<Title> a. 1 - Creation Date:System will use the appropriate interest rate based on the account’s creation date b. 2 - Due Date: System will check if there is a change in interest rate between the start date and end date, system will use the appropriate interest rate based on its effective date Account Interest Capitalization Capitalization Interest Interest Interest Type Calculation Frequency Due Type Frequency Due Rate Type Type Type 21_APA 2 - Simple 1 - Yearly 2 - Policy Due 4 - Monthly 2 - Policy 2 - Policy Due Due 22_Cash 2 - Simple 1 - Yearly 2 - Policy Due 4 - Monthly 2 - Policy 2 - Policy Bonus Due Due 23_Survival 2 - Simple 1 - Yearly 2 - Policy Due 4 - Monthly 2 - Policy 2 - Policy Benefit Due Due 51_Policy 2 - Simple 1 - Yearly 2 - Policy Due 4 - Monthly 2 - Policy 2 - Policy Loan Due Due 53_APL 2 - Simple 1 - Yearly 2 - Policy Due 4 - Monthly 2 - Policy 2 - Policy Due Due Rate Type Rate Effective Product Currency Rate(%) Date APA 2024-08-01 5 CB 2024-08-01 4 SB 2024-08-01 3 PL 2024-08-01 2 APL 2024-08-01 2

## Extract Cross Age Job

### Description
This document describes the daily batch job for Extract Cross Age Job.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |

### Procedures
- • Cross_Age1: life assured’s system time age
- o Calculate life assured age based on current system time.
- • Cross_Age2: life assured’s system time age after one month
- o Calculate life assured age based on current system time+ 1 month.

### Configuration
NA

## Fund Dividend Allocation & Confirmation

### Description
For unit linked product, the fund house may declare fund dividend that need to be allocated to all policies that own this fund and entitle to receive this dividend. This document describes the following batch job that use to process the fund dividend within the system. (1) Fund Dividend Allocation: Calculate the distribute the dividend on policy & fund. (2) Fund Dividend Confirmation: Confirm the dividend record after all policies entitle the dividend has completed. Remark: (allocation additional unit) is not covered. Feature User Guide Fund Dividend Rate Investment User Guide Entry/Revise/Approve/Query Fund Dividend Disposal Option New Business User Guide: Initial capture of customer’s choice on the fund dividend disposal option. Customer Service User Guide: (1) Change of the disposal option. (2) Capture the disposal option when additional fund added through CS change.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| CS | Customer Service |
| Record | Date An investor must be a unitholder on this date in order to be entitled dividend |
| Ex | Date Date where an investor can sell/redeem units based on the ex-dividend |
| price/NAV | and will be entitled to the dividend payment that is captured on the |
| record | date. (Record date + 1 Business Day) |
| Payment | Date The investor receives the cash payment arising from dividends as captured |
| on | the Record Date. (The date where system run the dividend allocation) |
| Reinvest | Date The price use to unitize policyholder’s dividend reinvestment. |
| (Payment | Date + 1 business day). |
| Dividend | Rate The dividend rate declares by Fund Manager. |
| FX | Foreign exchange |
| <Confidential> | eBaoTech Corporation Page 6 of 10 |
| CPF | Central Provident Fund (of Singapore) |
| In | the system, it refer to a special payment method within the system that use |

### Configuration
NA

### User Cases
- 2024; Fund Currency= SGD, Policy Currency = SGD, Dividend Rate= 0.054 SGD/ 1 Unit
- 2024; Fund Currency= USD, Policy Currency = SGD, Dividend Rate= 0.054 USD/ 1 Unit
- 05 Jan 2024 Dividend Allocation Coupon/Dividend 77.14(1000*0.054*1.428571)

## Fund Transaction Job-Enhancement

### Description
This is the daily batch job that reads all records that are pending for fund transaction daily to perform the normal validity checks. If the price for the fund to be transacted is available, the records pending for fund transaction will be bought or sold depending on the following instructions in the records: • Which Fund Type to transact • Whether to ‘buy’ or to ‘sell’ (transact) • Whether to transact (buy/sell) by units or by value • Whether to use ‘bid’ or ‘offer’ price (price retrieved from Fund Price file) • The effective date to use when reading the price for the fund

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |

### Prerequisites
- • Policy status is not applicant status (inforce/lapse/terminate).
- • Policy has a pending transaction.
- • Price is available based on the validity date of the transaction record.
- • Policy is not frozen.
- • Other Policy Alteration transaction that has fund transaction applications should be

### Configuration
IUA and AUA, another one is RPA and TPA. When defines fund factor ratio, the RPA should be mapped to IUA, the TPA should be mapped to AUA. Product info > Servicing Rules > ILP rules Product info > Servicing Rules > ILP rules Product_id Premium_Year Distri_type Sub_account Trans_month Effective_period FF_rate 5 D512-Start- RPA 1 1900-01-01 .. 0.8103 up Bonus 2024-12-31 5 D512-Start- RPA 1 2025-01-01 .. 0.8104 up Bonus 2999-12-31 5 D513- RPA 1 1900-01-01 .. 0.8103 Power-up 2999-12-31 Bonus 5 D514- RPA 1 1900-01-01 .. 0.8103 Loyalty 2999-12-31 Bonus 5 D515-Large RPA 1 1900-01-01 .. 0.8103 Sum Bonus 2999-12-31 <Confidential> eBaoTech Corporation Page 17 of 19 Gemini<Title> 5 D518- RPA 1 1900-01-01 .. 0 Account 2999-12-31 Maintenance Fee 5 D8-Partial RPA 1 1900-01-01 .. 0.8103 Withdraw 2999-12-31 5 D1-Net RPA 1 1900-01-01 .. 0.8103 Investment 2999-12-31 Premium 5 D17-Free RPA 1 1900-01-01 .. 0.8103 Look 2999-12-31 Withdrawal

### User Cases
- • Preconditions:
- • Process date & expected results:
- 2022-11- NB in force for ILP
- 28 policy
- 2022-11- Edit and confirm
- 30 Fund price
- 2022-11- Policy Fund Transaction record (buy) is confirmed, policy units
- 30 Transaction batch are updated
- 2022-11- Charge Deduction
- 30 Batch
- 2022-11- Policy Fund Transaction record (sell) is confirmed, policy units
- 30 Transaction batch are updated
- • Preconditions:
- • Process date & expected results:
- 2022-11- Apply for ILP Full
- 28 Surrender in CS
- 2022-11- Edit and confirm
- 28 Fund price
- 2022-11- Policy Fund Transaction record (sell) is confirmed, policy units
- 28 Transaction batch are updated

## Ilp Lapse Rider

### Description
This document describes the daily batch job to lapse unit deduct rider for level COI product.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |
| RSP | Regular single top up |

### Prerequisites
- • Level Pay COI Product indicator(ILP rules) of main product is Y.
- • Policy is inforce.
- • Policy is not frozen.
- • Policy has no any pending fund transaction record.
- • Policy has UDR and it has PLD existed.

### Procedures
- • If the system date is earlier than PLD. Process ends.
- • If the system date equals or is later than PLD. System will lapse the rider and

### Configuration
Eligibility criteria for ILP lapse rider is configured in ILP rules: • Level Pay COI Product = Y.

### User Cases
- • Preconditions:
- • Process date & expected results:
- 2024-10-16 Run batch ILP lapse rider No changes
- 2024-10-17 Run batch ILP lapse rider

## Loyalty Bonus Allocation

### Description
This document describes the daily batch job for Loyalty Bonus Allocation.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |

### Prerequisites
- • Bonus Type=Loyalty Bonus
- • Bonus allocation schedule defined
- • Bonus rate and Bonus calculation formula defined
- • Policy is inforce
- • Policy is not frozen
- • Current system date >= Bonus Due Date

### Configuration
Configuration example Loyalty Bonus: Starting from the first Policy month after the end of MIP and while the Policy is in force, the Policyholder will receive the Loyalty Bonus every month throughout the Policy Term, subject to the eligibility criteria. Bonus Allocation Schedule Configuration Bonus Name Minimum Minimum Minimum Bonus Start Bonus End Bonus Allot Investment Investment Investment Allot Period Allot Period Schedule Period Period Period (High) Type (Low) Loyalty Bonus Year 15 15 180 month 1187 month Monthiversary every 1 month Loyalty Bonus Year 20 20 240 month 1187 month Monthiversary every 1 month Loyalty Bonus Year 25 25 300 month 1187 month Monthiversary every 1 month Loyalty Bonus Year 30 30 360 month 1187 month Monthiversary every 1 month

## Maturity Letter Job

### Description
This document describes the daily batch job for Maturity Letter Job.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |
| APA | Advance Premium Account |
| APL | Automatic Premium Loan |

### Procedures
- 5. <maturity benefit amount> is total amount of guaranteed Maturity Benefit, Terminal
- 4. <maturity benefit amount> is total amount of guaranteed MB, RB, TB and adjusted amount.
- 5. <Excess payment> is total amount of general/PS/renew suspense and APA balance.
- 6. <Net maturity proceeds> is the actual amount of payment.

### Configuration
PS_PREMATURITY_ILP. <Confidential> eBaoTech Corporation Page 9 of 10 L M e t a t u r it y t e r _ .x ls x Gemini<Title> <Confidential> eBaoTech Corporation Page 10 of 10

## Maturity Notice Job

### Description
This document describes the daily batch job for Maturity Notice Job.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |
| APA | Advance Premium Account |
| APL | Automatic Premium Loan |

### Prerequisites
- • The products of policy cover the maturity benefit
- • The policies will be due for maturity X months later after the batch job starts
- • The policy status must be inforced
- • Batch Process Period from expiry date – XX days until maturity payment process

### Procedures
- o After performing maturity extraction batch, system extracts and stores the
- o For all maturating policies, system extracts the balance per policy and

### Configuration
Maturity Notice, Advance days is 180 day NA

### User Cases
- • Preconditions:
- • Process date & expected results:

## Maturity Auto Pay Out

### Description
This document describes the daily batch job for Maturity Auto Pay out.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |
| APA | Advance Premium Account |
| APL | Automatic Premium Loan |

### Procedures
- • Maturity payable records offset and generate actual payment record
- • The payment method is defaulted as Policy disbursement method
- • The fee status of payment records is Waiting for Authorization (Temperate fee status)
- • System assigns and generates a unique and sequential batch number to the maturity

### Configuration
NA

## Pay Maturity

### Description
This document describes the daily batch job for Pay Maturity.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |
| APA | Advance Premium Account |
| APL | Automatic Premium Loan |

### Procedures
- • For all maturating policies, system re-extracts the latest balance of policy (refer to
- • System generates the net maturity amount payable and adjustment amount payable
- • The payment method is defaulted as Policy disbursement method
- • If the calculated net amount is less 0, system won’t generate the MB payment records
- • The fee status of payment records is Waiting for Authorization (Temperate fee status)
- • System updates the benefit status to be terminated and record the termination reason
- • If the mature benefit is main benefit, system updates the policy status to be terminated
- • System assigns and generates a unique and sequential batch number to the maturity

### Configuration
Maturity Extraction, Advance days is 1 day NA <Confidential> eBaoTech Corporation Page 8 of 10 Gemini<Title>

### User Cases
- • Preconditions
- • Expected Results
- • Preconditions
- • Expected Results
- • Preconditions
- • Expected Results
- • Preconditions
- • Expected Results
- • Preconditions
- • Expected Results

## Policy Auto Surrender

### Description
This document describes the daily batch job to auto surrender eligible policies.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |

### Prerequisites
- • Product auto surrender indicator is ‘Yes’ as defined in product definition ->CS rules
- ->surrender rules
- • Batch process date ≥ lapse date + xx days (system parameter) refer to reinstatement

### Business Rules
| Rule | Description |
|------|-------------|
| BR_001: Auto surrender rules | Upon auto surrender, system update policy information as below:
1. Set policy status to ‘terminated’, termination reason is
‘auto surrender’, termination date = lapse date
2. If there are any units left on policy ILP account, system
generate selling transaction to sell all units, price effective
date set as lapse date + 1.
3. Calculate all benefits net surrender value, using lapse
date as valuation date. If there is any net surrender value,
generate surrender amount to be refunded to customer.
Net surrender value = gross surrender value – policy
debts. |

### Configuration
NA

### User Cases
- • Preconditions:
- • Process date & expected results:

## Policy Maintenance Fee Refund Allocation

### Description
This document describes the daily batch job to calculate and allocate policy maintenance fee refund.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |
| APH | Auto premium holiday |
| PH | Premium holiday |

### Prerequisites
- • Policy Maintenance Fee Refund is defined for the product
- • Policy is inforce
- • Policy is not frozen
- • Current system date >= Bonus Due Date

### Configuration
Eligibility criteria for the Policy Maintenance Fee Refund is configured in the calculation formula such as: • All Regular Premiums payable for the first 3 Policy Years have been fully paid when due; and • Premium Holiday has not been taken during the first 3 Policy Years; and • Regular Premium has not been reduced during the first 3 Policy Years; and • After making Partial Withdrawals during the Premium Payment Term, the remaining value in the Accumulation Units Account shall not fall below 18 months of the monthly Regular Premium committed at Policy issuance.

### User Cases
- • Preconditions:
- • Process date & expected results:
- 2024-10-16 No changes
- 2024-10-17

## Power Up Bonus Allocation

### Description
This document describes the daily batch job to calculate and allocate power up bonus.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |
| APH | Auto premium holiday |
| PH | Premium holiday |

### Prerequisites
- • Power-up Bonus is defined for the product
- • Policy is inforce
- • Policy is not frozen
- • Current system date >= Bonus Due Date

### Configuration
Eligibility criteria for the Power-up Bonus is configured in the calculation formula such as: • The Policyholder has made a Partial Withdrawal from the Regular Premium account; or • The Policyholder has been on Premium Holiday; or • The Policyholder has reduced the Regular Premium.

### User Cases
- • Preconditions:
- • Process date & expected results:
- 2024-10-16 Run batch power up bonus allocation No changes
- 2024-10-17 Run batch power up bonus allocation

## Rsp Renew Confirmation

### Description
This document describes the daily batch job to applied RSP and move RSP due date for eligible polices.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |
| APH | Auto premium holiday |
| PH | Premium holiday |

### Prerequisites
- • Main benefit status is inforce.
- • Policy is not frozen by claim or CS.
- • RSP bill record status is not payment confirmed.

### User Cases
- • Preconditions:
- • Process date & expected results:
- 2024-10-17 Collect inforcing premium Policy status=Inforce
- 2024-10-17 Run RSP renew extraction batch Bill record created
- 2024-10-20 Collect RSP renew premium Money collected into renew suspense
- 2024-10-20 Run RSP renew confirm batch
- • Preconditions:
- • Process date & expected results:
- 2024-09-17 Run RSP renew extraction batch Bill record created
- 2024-11-15 suspense>=1 installment RSP
- 2024-11-15 Run RSP renew confirm batch
- • Preconditions:
- • Process date & expected results:
- 2024-09-17 Run RSP renew extraction batch Bill record created
- 2024-11-15 Run RSP renew confirm batch No change.
- 2024-11-16 Run RSP renew confirm batch RSP due date moves to 2025-
- 01-17
- • Preconditions:
- • Process date & expected results:
- 2024-09-17 Run RSP renew extraction batch Giro payment file is generated and uploaded.
- 2024-09-19 Run RSP renew confirm batch No change.
- 2024-19-20

## Rsp Renew Extraction

### Description
This document describes the daily batch job that verifies whether the policy is eligible to extract the due for recurring single premium. This is a daily batch to calculate the premium amount to bill and then create a billing record for the calculated amount.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |
| APH | Auto premium holiday |
| PH | Premium holiday |

### Prerequisites
- • Main benefit status is inforce.
- • Policy is not frozen by claim or CS.
- • Policy is not in premium holiday period.
- • RSP Plan status is active.
- • RSP End Date is not earlier the RSP Due Date
- • System Date>= RSP Due Date – 30 days(extraction_leading_days).

### Configuration
30 (days) is configured in existing parameter extraction_leading_days the same as renew premium extraction.

### User Cases
- • Preconditions:
- • Process date & expected results:
- 2024-10-17 Collect inforcing premium Policy status=Inforce
- 2024-10-17 Run RSP renew extraction batch Bill record created
- • Preconditions:
- • Process date & expected results:
- 2022-10-17 Collect inforcing premium Policy status=Inforce
- 2024-08-10
- 2024-09-17 Run RSP renew extraction batch Bill record created

## Regular Withdrawv0.1

### Description
This document describes the daily batch job that verifies whether the policy is eligible to auto set premium Holiday. If yes, deduct premium holiday charge if any and set premium holiday indicator as Yes with start date and end date. Otherwise, set PLD at end of grace period.

### Acronyms
| Term | Description |
|------|------------|
| ILP | Investment Linked Product |
| TIV | Total Investment Value |
| PF | Policy Fee |
| COI | Cost of Insurance |
| UDR | Unit Deduct Rider |
| URP | Unit Deduct Rider Premium |
| CRP | Cash Rider Premium |
| NLG | period Non Lapse Guaranteed period |
| PDD | Policy Due Date |
| MDD | Monthly Charge Due Date |
| PLD | Potential Lapse Date |
| MIP | Minimum Investment Period |
| CS | Customer Service |

### Prerequisites
- • Policy status is inforce.
- • The policy is not frozen by other transactions.
- • There is an active regular withdraw plan under the policy.
- • System date >= Regular Withdraw Due Date.
- • Regular withdraw amount< Total Account Value- Minimum Holding Amount- Pending

### Procedures
- • If the account value is sufficient, generate pending fund transactions. Refer to rules
- • If the account value is not sufficient, system should cancel the future withdraw

### Configuration
NA

### User Cases
- • Preconditions:
- • Process date & expected results:

