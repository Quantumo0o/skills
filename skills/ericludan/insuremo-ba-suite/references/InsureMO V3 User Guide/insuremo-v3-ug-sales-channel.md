# InsureMO Platform Guide — Sales Channel

**Source:** 22_SalesChannel.pdf (60 pages)
**System:** LifeSystem 3.8.1
**Module:** Sales Channel and Commission
**Version:** V3 (legacy)

---

## Metadata

| Field | Value |
|-------|-------|
| File | insuremo-v3-ug-sales-channel.md |
| Source | 22_SalesChannel.pdf |
| System | LifeSystem 3.8.1 |
| Version | V3 (legacy) |
| Date | ~2015 |
| Category | Distribution / Sales Channel |
| Pages | 60 |

---

## 1. Purpose of This File

Answers questions about sales channel management, producer hierarchy, commission processing, compensation, and performance assessment in LifeSystem 3.8.1. Covers agents, brokers, bank channels, and internal sales forces. Used for BSD writing when commission rules, producer management, or sales channel workflows are needed.

---

## 2. Module Overview

```
Sales Channel (LifeSystem 3.8.1)
│
├── 1. Set Up Sales Channel
│   ├── Set Up Channel Organization
│   ├── Maintain Physical Location
│   ├── Manage Hierarchy
│   │   ├── Supervisory Relationship
│   │   └── Nurture Relationship
│   └── Manage Supervisory Hierarchy
│
├── 2. Manage Producer
│   ├── Transfer Producer
│   ├── Maintain Producer Qualification
│   ├── Modify Producer Position Status
│   ├── Modify Service Producer
│   ├── Modify Commission Producer
│   └── Modify Performance Producer
│
├── 3. Manage Performance
│   ├── Define Performance
│   └── Query Persistency
│
├── 4. Manage Compensation
│   ├── Define Compensation
│   ├── Adjust Compensation
│   ├── Aggregate Compensation
│   ├── Confirm Compensation
│   ├── Query Commission
│   ├── Query Compensation Status
│   ├── Download and Upload Compensation Tax File
│   └── Generate Compensation Statement
│
├── 5. Manage Assessment
│   ├── Define Assessment
│   ├── Evaluate Assessment
│   ├── Monitor Assessment
│   ├── Confirm Assessment
│   └── Promote or Demote Producer
│
└── 6. Sales Channel Batch Jobs
    ├── Production Generation Batch
    ├── Active Status Batch
    ├── Persistency Production Batch
    ├── Performance Calculation Batch
    └── Assessment Evaluation Batch
```

---

## 3. Sales Channel Management Process

The following table lists the recommended process of sales channel management.

| S/N | Process | Reference |
|-----|---------|-----------|
| 1 | Set up the organizations in sales channel. | Set Up Channel Organization |
| 2 | Set up physical location. | Define Physical Location |
| 3 | Set up producer (a person or organization involved in the policy sales, such as agent) with introducing relationship. | Maintain Sales Channel Related Parties |
| 4 | Add qualification for the producer. | Maintain Qualification |
| 5 | Define performance. | Define Performance |
| 6 | Define compensation. | Define Compensation |
| 7 | Define assessment. | Define Assessment |
| 8 | Build up supervisory hierarchy. | Manage Supervisory Hierarchy |
| 9 | Build up nurture relationship. | Maintain Nurture Relationship |
| 10 | Transfer producer. | Transfer Producer |
| 11 | Perform manual assessment adjustment (promotion/demotion). | Promote or Demote Producer |
| 12 | Manage the service producer. | Change Service Producer |
| 13 | Manage the performance producer. | Manage Performance Producer |
| 14 | Manage the commission producer. | Manage Commission Producer |
| 15 | Manage the producer status. | Maintain Position Status |
| 17 | Query commission. | Query Commission |
| 18 | System runs a daily batch job to calculate production for each benefit. | Production Generation Batch |
| 19 | System runs a monthly batch job to check producer's active status. | Active Status Batch |
| 20 | System runs a monthly batch job to calculate persistency related production. | Persistency Production Batch |
| 21 | System runs a daily batch job to calculate performance. | Performance Calculation Batch |
| 22 | Query persistency. | Query Persistency |
| 23 | Adjust compensation. | Adjust Compensation |
| 24 | Run compensation aggregation batch. | Aggregate Compensation |
| 25 | Query compensation. | Query Compensation Status |
| 26 | Download and upload tax. | Download and Upload Compensation Tax File |
| 27 | Run compensation confirmation batch. | Confirm Compensation |
| 28 | Generate compensation statement. | Generate Compensation Statement |
| 29 | Run assessment evaluation batch. | Evaluate Assessment |
| 30 | Monitor assessment. | Monitor Assessment |
| 31 | Run assessment confirmation. | Confirm Assessment |

---

## 4. Set Up Sales Channel

### 4.1 Set Up Channel Organization

This section describes how to set up the organizations in sales channel.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Channel Setup > Maintain Producer.
2. The Party Identification page is displayed. Select Organization from the Party Type drop-down list and select a channel organization from the Party Category drop-down list. Then click Create.
3. The channel organization maintenance page is displayed. Enter mandatory information and then click Apply or Submit.
4. Click other tabs to enter related information if any.
5. The end.

**Channel Organization Rules:**

1. When you create a channel organization, only active organizations are displayed in the parent organization drop-down list. Inactive organizations cannot be parent organizations.
2. When you change the status of a channel organization from active to inactive, this channel organization cannot be the parent organization of any organization.

---

### 4.2 Maintain Physical Location

This section describes how to define physical location of a sales channel.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Configuration Center > Sales Channel Configuration > Maintain Physical Location.
2. The Physical Location Management page is displayed. Click Create.
   - If you want to delete a physical location, search it out and click Delete. If the physical location is used by a producer, it cannot be deleted.
3. The Physical Location Maintenance page is displayed. Enter the location information and comments if any. Then click Submit.

**Rules:**
- The physical location must be unique.

---

### 4.3 Manage Supervisory Hierarchy

Hierarchy is the structure of specific channel in sales. It is much more related to sales structure rather than administrative structure. Supervisory hierarchy is a type of tied agent structure which is based on leadership of agent.

This section describes how to manage supervisory hierarchy of producers, including adding supervisory relationship and position.

**Prerequisites:** The producer has at least one position.

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Hierarchy > Supervisory Relationship.
2. The Supervisory Hierarchy page is displayed. Click Create.
3. The Supervisory Hierarchy Maintenance page is displayed. Enter the producer information and supervisory information and then click Submit.

**Table: Description of Fields in the Supervisory Hierarchy Maintenance Page**

| Field | Description |
|-------|-------------|
| Producer Code | Enter the producer code or double-click this field to select one. After the producer code is entered, all the hierarchy records of the producer will be displayed. |
| Producer Position | Select a position for the producer from the drop-down list. |
| Effective Date | The effective date must not be earlier than the current system date. |
| Supervisor Code | Enter the supervisor code or double-click this field to select one. After the supervisor code is entered, all the position records of the supervisor will be displayed. Select a proper supervisor position for the producer. The selected supervisor must meet the following requirements: The supervisor entered must have at least one management level position. The supervisor must be different from the producer entered previously. The hierarchy relationship between the producer and supervisor must be correct, that is, the position of the supervisor must be higher than the position of the producer. |

---

### 4.4 Change Nurture Relationship

Nurture relationship is used for some special bonus calculation and the belonging relationship after promotion and demotion.

Nurture relationship will be created and updated by system automatically as follows:
- When supervisory hierarchy is built, the supervisor will be the nurturer of the producer by default.
- When a producer is transferred, if the transferred producer's new leader is the nurturee of the transferred producer before change, system will update the transferred producer's nurturer as that leader's nurturer and the transferred producer's new leader will be his/her new nurturer. Other transferred producer's nurturees in the same level of this new leader will change also.
- When a producer is promoted from a low position to high position, his/her leader in original position will be the nurturer in new position.
- When a producer is demoted from a high position to low position, his/her new supervisor is his/her nurturer by default.

This section describes how to manually change the nurture relationship.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Hierarchy > Nurture Relationship.
2. The Nurture Relationship page is displayed. Click Create.
3. The Nurture Relationship Maintenance page is displayed. Enter the producer information and nurturer information. Then click Submit.

**Table: Description of Fields in the Nurture Relationship Maintenance Page**

| Field | Description |
|-------|-------------|
| Producer Code | Enter the producer code or double-click this field to select one. When the producer code is entered, all the position records of the producer will be displayed. Select a position. The producer code entered must have at least one position. |
| Nurturer Code | Enter the nurturer code or double-click this field to select one. When the nurturer code is entered, all the position records of the nurturer will be displayed. Select a position. The nurturer code entered must have at least one position. |
| Effective Date | Effective date must not be earlier than the system date. |

---

## 5. Manage Producer

### 5.1 Transfer Producer

This section describes how to transfer a producer.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Producer > Transfer Producer.
2. The Transfer Producer page is displayed. Enter the transfer information.

**Table: Description of Fields in the Producer Transference Page**

| Field | Description |
|-------|-------------|
| Producer | Enter the producer code or double-click this field to select one. The producer must meet the following requirements: The producer code must exist. The producer must be active. The producer must have at least one position. The producer position must be at direct agent level. When the producer code entered, system will display the agent's current information with his/her supervisor information as reference. |
| Transfer Reason | Select a reason from the drop-down list. |
| Transfer Date | Effective date of the transference |
| Policy Hierarchy | Options include Old Hierarchy and New Hierarchy. If New Hierarchy is selected, those mentioned old supervisors will not share the subsequent production of old policies, because the new supervisors in the new hierarchy will get these productions. If Old Hierarchy is selected, those mentioned old supervisors will share the subsequent production of old policies, but the new generated policies for those transferred producers will belong to the new supervisors in the new hierarchy. For old policies, the existing production still belongs to the old hierarchy. For new policies, the production belongs to the new hierarchy. |
| Leader Included | Indicate whether the leader is transferred with the transference. If the producer is at agent level, no matter whether Yes or No is selected, system will transfer the agent himself/herself. If the producer is at management level (which means there are some staff managed by the producer) and Yes is selected, system will transfer this producer with all his/her staff to the new supervisor. So the staff still report to this producer, but the producer will report to the new supervisor. If you do not want to transfer any of the staff with this transference, you need to transfer them out beforehand. If the producer is at management level and No is selected, system will transfer all his/her staff to the new leader except the producer himself/herself. After transference, there will be no staff under this producer. |
| Supervisor | Enter the supervisor code or double-click this field to select one. The supervisor must have a management level position. |
| Comments | Enter your comments if any. |

3. Click Submit. The system updates the hierarchy of the producer involved.

**Rules:**
- Nurturer is the same person as supervisor by default. If the transferred producer's new leader is the nurturee of the transferred producer before change, system will update the transferred producer's nurturer as that leader's nurturer and the transferred producer's new leader will be his/her new nurturer. Other transferred producer's nurturees on the same level of this new leader will change also.

---

### 5.2 Maintain Producer Qualification

This section describes how to maintain the qualification of sales channel.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Producer > Maintain Qualification.
2. The Maintain Producer Qualification page is displayed. Maintain qualification information as follows:
   - To add qualification information for one producer, click Create. Enter or modify the qualification information, including producer code, qualification type, effective date, and expiry date, and then click Submit.
   - To add qualification information for multiple producers, click Download to download the template as a CSV file, enter qualification information, and then click Upload to upload the file.
   - To modify an existing qualification record, search it out and click the producer code. Then modify the record.

**Qualification Overlap Rules:**
- If the qualification record with the same producer and qualification type already exists:
  - If the new and old qualification periods do not have any overlapped dates, system will generate a new qualification record.
  - If the new and old qualification periods have some overlapped dates, system will combine the old and new periods to get a longer period and update the old record.
  - If the new qualification period is in the old qualification period, no new record will be generated.

**Rules:**
- The expiry date is the date of invalidation for qualification. Therefore, the effective end date of qualification is expiry date - 1.

---

### 5.3 Modify Producer Position Status

This section describes how to maintain the position status of a producer.

**Prerequisites:**
- The producer has a position.
- The producer status is Inforce.

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Producer > Modify Producer Position Status.
2. The Producer Position Status Maintenance page is displayed. Enter the producer code, and the producer status is displayed. Change the position status from Inforce to Terminated, and enter the effective date. Then click Submit.

**Rules:**
- The position status can only be changed to Terminated.

---

### 5.4 Modify Service Producer

Service producer is the producer providing customer services.

This section describes how to change the service producer of policies.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Producer > Modify Service Producer.
2. The Modify Service Producer page is displayed. Set search criteria and click Search.
3. The qualified policy records are displayed. Select policies, enter the new service producer code and effective date, and then click Submit.

**Table: Description of Fields in the Service Producer Management Page**

| Field | Description |
|-------|-------------|
| Orphan Policy | The policy without a service producer or the service producer terminated will be treated as an orphan policy. You can assign a service producer to an orphan policy. |
| New Service Producer Code | New service producer must be in Inforce status. |
| Effective Date | Effective date must not be earlier than the current system date. |

---

### 5.5 Modify Commission Producer

Commission producer is the producer who enjoys the basic commission at benefit level. Commission can be split among different producers by different premium types, such as premium and top-up.

This section describes how to maintain the commission producer of benefit by batch or individually.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Producer > Modify Commission Producer.
2. The Modify Commission Producer page is displayed. Enter search criteria and click Search.
3. The qualified policy records are displayed. Decide whether to maintain the commission producer by batch or individually.
   - If you want to maintain the commission producer of benefit by batch, go to step 4.
   - If you want to maintain the commission producer of benefit individually, go to step 5.
4. Maintain commission producer of benefit by batch.
   a. From the search result, select more than one policy record and then click Maintain All Selected.
   b. The Maintain Policy Commission Producer page is displayed. Enter the new commission producer and then click Submit.
   - The new commission producer must be different from the current commission producer.
5. Maintain commission producer of benefit individually.
   a. From the search result, select a policy record and click Maintain One by One.
   b. The Commission Producer page is displayed. Edit the commission producer and percentage of the selected product. Then click Submit.
   - The total percentage must be 100%.
6. The end.

---

### 5.6 Modify Performance Producer

Performance producer is the producer who gets the production of issued benefits. Performance producer is the same person as the issue producer who issues benefits, but the performance producer can be changed if required.

This section describes how to transfer policies to a new performance producer.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Producer > Modify Performance Producer.
2. The Modify Performance Producer page is displayed. Set search criteria and click Search.
3. The qualified policy records are displayed. Select policies, enter the new performance producer code and effective date, and then click Submit.

**Table: Description of Fields in the Performance Producer Management Page**

| Field | Description |
|-------|-------------|
| New Performance Producer Code | The new performance producer must be different from the old performance producer. |
| With Existing Production | Whether the existing production belongs to the new performance producer. If Yes is selected, the old production of the existing policy will belong to the new hierarchy. If No is selected, the existing production will stay in the old hierarchy, but the new production after the change will belong to the new hierarchy. |
| Effective Date | Effective date must not be earlier than the current system date. |

---

## 6. Manage Performance

### 6.1 Define Performance

Performance refers to the defined production in specific period with predefined frequency and other related features.

This section describes how to define performance of sales channels.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Performance > Create or Modify.
2. The Create or Modify Performance page is displayed. To create a new performance definition, click Create. To modify an existing performance definition, search it out and click its performance code.
3. Enter performance definition information. You can define performance by production or by formula. Then click Submit.

**Table: Description of Fields in Performance Definition (By Production)**

| Field | Description |
|-------|-------------|
| Performance Code | Performance code is generated automatically after the Define Mode and Production is selected. |
| Define Mode | Select By Production from the drop-down list. |
| Production | Select a production from the drop-down list. |
| Inforce Status | Whether the performance is active or not |
| Frequency | Frequency of performance calculation. Select from the drop-down list. |
| Initial Calculation Date | Calculation start date |
| Name | Name of performance |
| Sequence | Sequence of performance calculation |
| Owner Position | Position of producer performance counted to. Select from the drop-down list. |
| Production Scope | Scope is a range definition of person involved in the performance contribution. Select from the drop-down list: Personal: producer; Team: producer in the same channel organization; Unit: team excluding the leader; Tree: producers who are under both the direct and indirect supervision of leader; Top down: producers under both direct and indirect supervision of leader, excluding leader; 1st Tier: producer team under direct supervision of leader excluding direct staff; 2nd Tier: producer team under the direct supervision of the leader's 1st Tier producer; Direct Group: direct tree, with direct or indirect producers, report to the leader |
| Calculate Period Type | Period definition in performance summation. Select from the drop-down list. |
| Calculate Period | Production calculation period |
| Owner Type | The relationship type of owner and downline. Select from the drop-down list. |
| Downline Position | Position of downline producer. Select from the drop-down list. |
| Downline Appointment Period Type | Type of downline appointment period. Select from the drop-down list. |
| Downline Appointment Period | Downline appointment period |
| Policy Year | Policy year of policy included |
| Payment Mode | Payment mode of policy |
| Policy Commencement Date | Date when policy takes effect |

**Table: Description of Fields in Performance Definition (By Formula)**

| Field | Description |
|-------|-------------|
| Performance Code | Performance code is generated automatically after the Define Mode is selected. |
| Define Mode | Select By Formula from the drop-down list. |
| Formula ID | Formula defined in FMS |
| Inforce Status | Whether the performance is active or not |
| Frequency | Frequency of performance calculation. Select from the drop-down list. |
| Initial Calculation Date | Calculation start date |
| Name | Name of performance |
| Sequence | Sequence of performance calculation |
| Owner Position | Position of producer performance counted to. Select from the drop-down list. |

---

### 6.2 Query Persistency

This section describes how to query persistency result for producer.

**Prerequisites:**
- Persistency batch and performance batch have run successfully.

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Performance > Query Persistency.
2. The Query Persistency page is displayed. Set search criteria and then click Search.
3. View persistency information in the Search Result area and then click Exit.

**Table: Description of Fields in the Persistency Query Page**

| Field | Description |
|-------|-------------|
| AAP | Actual Annualized Premium, a factor to calculate Sx persistency. It is a total actual payment of benefit premium in a certain year. |
| EAP | Expected Annualized Premium, a factor to calculate Sx persistency. It is a total annualized premium in certain year |
| ASAP | Actual Standardized Annualized Premium, a factor to calculate Kx persistency. It is an actual premium payment which is standardized and annualized in a certain period. |
| ESAP | Expected Standardized Annualized Premium, a factor to calculate Kx persistency. It is the total Standardized Annualized Premium in a certain period. |
| ACP | Actual Cumulative Premium, a factor to calculate Px persistency. It is the actual payment premium of cumulative premium in a certain period. |
| ECP | Expected Cumulative Premium, a factor to calculate Px persistency. It is the expected amount of cumulative premium in a certain period. |
| Sx | S1 premium persistency = AAP in year 1 / EAP in year 1 * 100%; S2 premium persistency = AAP in year 2 / EAP in year 2 * 100%; Sx rules: Policy will be considered only once at the month after it over the 1st anniversary date + grace period of premium for S1; Policy will be considered only once at the month after it over the 2nd anniversary date + grace period of premium for S2 |
| Kx | K1 premium persistency = ASAP in year 1 / ESAP in year 1 * 100%; K2 premium persistency = ASAP in year 2 / ESAP in year 2* 100%; Kx rules: Grace period of the premium payment will not be considered, which means at the end of the due date month, if the premium is paid, treat it as paid; if not, treat it as unpaid without the consideration of grace period. If the benefit does not have any short payment, Kx is considered as 100% with annualized amount for each month. If there's any short payment, the actual amount will use the actual payment of benefit divided by the annualized amount as expected. Kx will be calculated for policy during the corresponding year only, which means K1 is calculated in benefit's year1 only. Once the benefit goes to year 2, K1 will not be calculated. |
| Px | P1 premium persistency = ACP in year 1 / ECP in year 1 * 100%; P2 premium persistency = ACP in year 2 / ECP in year 2 * 100%; Px rules: ACP in year 1 will be the first year premium (FYP) which is actually paid, accumulated to the past 12 months in the point the persistency is calculated, that is, the accumulated FYP at the point of persistency calculation. ECP in year 1 will be the expected accumulated first year premium, that is, accumulated to the past 12 months at the point of persistency calculation. Grace period of the premium payment will not be considered, which means at the end of the due date month, if the premium is paid, treat it as paid; if not, treat it as unpaid. Px is the basis of persistency bonus calculation, promotion & contract maintenance, and other related bonus calculation. |

---

### 6.3 About Persistency

This section tells what persistency is, persistency calculation and the general rules related to persistency.

#### 6.3.1 Basic Knowledge of Persistency

- **Annualized Premium (AP):** installment premium (with or without extra premium, which can be configured by system parameter) multiply by mode of premium.
- **Spread Over Year:** the year of premium payment term for the difference of calculating standardized premium.
- **Cumulative Premium:** the accumulated premium rolling back to 12 months, which is count to specific year, at the point of specific year's persistency calculation.
- **Standardized Annualized Premium (SAP):** This definition is basically annualized premiums with reductions for product with premium terms less than Spread Over Year and less than the coverage term.
- **K1 Premium Persistency:** measures how much of expected first year premiums are actually collected from customers based on the Standardized Annualized Premium.
- **K2 Premium Persistency:** measures how much of expected second year premiums are actually collected from customers based on the Standardized Annualized Premium.
- **S1 Premium Persistency:** measures how much of expected first year premiums are actually collected from customers based on the Annualized Premium.
- **S2 Premium Persistency:** measures how much of expected second year premiums are actually collected from customers based on the Annualized Premium.
- **P1 Premium Persistency:** measures how much of expected first year premium are actually collected based on First Year Premium (FYP).
- **P2 Premium Persistency:** measures how much of expected second year premium are actually collected based on Second Year Premium (SYP).

#### 6.3.2 Persistency Calculation

- **Annualized Premium** = installment premium (with or without extra premium, which can be configured by system parameter) * mode of premium. Mode of premium is as follows:

| Payment Frequency | Mode of Premium |
|-------------------|-----------------|
| Yearly | 1 |
| Half-yearly | 2 |
| Quarterly | 4 |
| Monthly | 12 |

- **Spread Over Year** = 10 years for all the products
- **SAP:** If Premium Payment Term (PPT) >= spread over year, SAP = AP; if PPT < spread over year, SAP = (AP * PPT) / min (spread over year, CT)
- AAP, EAP, ASAP, ESAP, ACP & ECP are calculated on the monthly persistency batch job.
- The performance aggregation batch will check whether any production of persistency is calculated or not. If the production is generated already in the performance aggregation, system can calculate the persistency Kx, Px and Sx.
- The persistency bonus is based on Px in the compensation aggregation batch.

#### 6.3.3 Persistency General Rules

- The anniversary is based on the commence date rather than the issue date, so for back date policy, commencement will be considered.
- For direct agent, persistency is calculated based on the total amount of premium for all the issued policies; for supervisor, group persistency is calculated based on the total premium of all the team's policies (direct or indirect), and personal persistency is calculated based on all his/her personal policies.
- The period of persistency calculation will be from the start date of each calendar month to the last day of each calendar month.
- Any alternation that affects the premium will be considered in persistency calculation. Policy status change and policy transfer will also influence the persistency calculation.
- Persistency only considers policy's regular premium, target premium and recurring top-up amount. Single premium and adhoc top-up are not considered.
- The persistency calculation is product based for each producer, so there is no splitting of related productions of one product to different producers.
- The premium collected after new producer transfer belongs to the new producer.
- The actual payment must be less than or equal to the expected payment for each product.
- Tolerance of premium is not considered for each persistency, which means any tolerance amount will still be counted into actual and expected amount in persistency calculation.

---

## 7. Manage Compensation

### 7.1 Define Compensation

Compensation refers to the commission and bonus included in the payment calculation to producer.

This section describes how to define compensation.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Compensation > Create or Modify.
2. The Create or Modify Compensation page is displayed. To modify an existing compensation, search it out and click the compensation name. To add a new compensation, click Create.
3. The Compensation Maintenance page is displayed. Enter compensation information and then click Submit.

---

### 7.2 Compensation Calculation

#### 7.2.1 Agency Manager Direct Overriding

##### 1) Overriding for AM

Agent Manager (AM) only has direct agents. Therefore, the overriding for AM only includes the direct agents part.

**Productivity Overriding Bonus Rate:**

| Total number of "Qualified Cases" in past rolling 12 weeks (includes current week production) | Overriding Factor (% FYC) Payable |
|-------------------------------------------------------------------------------------------|-----------------------------------|
| < 12 | 10.0% |
| 12 – 19.99 | 12.5% |
| 20 – 39.99 | 15.0% |
| >= 40 | 17.5% |

Note: Qualified Cases include the cases produced by the AM as well.

| Total Annualized First Year Commission (AFYC) in past rolling 12 weeks (includes current week) | Overriding Factor (% FYC) Payable |
|----------------------------------------------------------------------------------------------------|-----------------------------------|
| < 15,000,000 | 10.0% |
| 15,000,000 – 29,999,999 | 12.5% |
| 30,000,000 – 54,999,999 | 15.0% |
| >= 55,000,000 | 17.5% |

Note: AFYC includes the AFYC produced by the AM as well.

| Agents recruited in the last rolling 12 weeks | Recruiting Target Factor |
|-----------------------------------------------|-------------------------|
| < 1 | 95% |
| 1 | 105% |
| >= 2 | 110% |

Note: last rolling back 12 weeks (3 months) under the team of AM.

##### 2) Overriding for SAM

Senior Agency Manager (SAM) has his own unit and AM, and also, SAM can have his direct agents. Thus the overriding for SAM is separated into two parts: direct agent part and direct team part.

**Productivity Overriding Rate:**

| Total number of "Qualified Cases" produced by the SAM's group in past rolling 12 weeks (including current week) | Overriding Factor (% FYC) Payable on current week production from SAM's direct agents | Overriding Factor (% FYC) Payable on current week production from all AM groups under the SAM |
|-------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| < 25 | 22.5% | 10.0% |
| 25 – 39.99 | 25.0% | 12.5% |
| 40 – 59.99 | 27.5% | 15.0% |
| >= 60 | 30.0% | 17.5% |

Note: SAM's direct agent and direct team have different productivity overriding rates, as shown above. SAM's own production is calculated in the direct agent part.

| Total Annualized First Year Commission (AFYC) produced by the SAM's group in past rolling 12 weeks (including current week) | Overriding Factor (% FYC) Payable on current week production from SAM's direct agents | Overriding Factor (% FYC) Payable on current week production from all AM groups under the SAM |
|--------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| < 35,000,000 | 22.5% | 10.0% |
| 35,000,000 – 54,999,999 | 25.0% | 12.5% |
| 55,000,000 – 84,999,999 | 27.5% | 15.0% |
| >= 85,000,000 | 30.0% | 17.5% |

Note: SAM's direct agent and direct team have different productivity overriding rates, as shown above. SAM's own production is calculated in the direct agent part.

| Agents recruited in the SAM's team the last rolling 12 weeks | Recruiting Target Factor |
|--------------------------------------------------------------|-------------------------|
| < 2 | 90% |
| 2 – 3 | 105% |
| >= 4 | 115% |

Note: last rolling back 12 weeks (3 months) under the team of SAM.

##### 3) Overriding for RAM

Regional Agency Manager (RAM) has his own SAM and AM and agents under the team, which is the direct team under the RAM. Meanwhile, RAM has his own AM team, which is the indirect team under the RAM. RAM also has his own agents, which is the direct agent. Thus, the overriding for RAM is separated into three parts.

**Productivity Overriding Rate:**

| Total number of "Qualified Cases" produced by the RAM's Group in past rolling 12 weeks (includes current week) | Overriding Factor (% FYC) Payable on current week production from RAM's direct agents | Overriding Factor (% FYC) Payable on current week production from all "Direct" AM groups under the RAM | Overriding Factor (% FYC) Payable on current week production from all Direct SAM groups under the RAM |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| < 50 | 32.5% | 20.0% | 7.5% |
| 50 – 74.99 | 35.0% | 22.5% | 10.0% |
| 75 – 104.99 | 37.5% | 25.0% | 12.5% |
| >= 105 | 42.5% | 27.5% | 15.0% |

Note: RAM's direct team, indirect team, and direct agent have different productivity overriding rates. RAM's own production is calculated in direct agent part.

| Total Annualized First Year Commission (AFYC) produced by the RAM's group in past rolling 12 weeks (includes current week) | Overriding Factor (% FYC) Payable on current week production from RAM's direct agents | Overriding Factor (% FYC) Payable on current week production from all "Direct" AM groups under the RAM | Overriding Factor (% FYC) Payable on current week production from all direct SAM groups under the RAM |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| < 90,000,000 | 32.5% | 20.0% | 7.5% |
| 90,000,000 – 119,999,999 | 35.0% | 22.5% | 10.0% |
| 120,000,000 – 149,999,999 | 37.5% | 25.0% | 12.5% |
| >= 150,000,000 | 42.5% | 27.5% | 15.0% |

Note: RAM's direct team, indirect team, and direct agent have different volume overriding rates. RAM's own production is calculated in direct agent part.

| Agents recruited in the SAM's team the last rolling 12 weeks | Recruiting Target Factor |
|--------------------------------------------------------------|-------------------------|
| < 3 | 90% |
| 3 – 4 | 105% |
| >= 5 | 115% |

Note: last rolling back 12 weeks (3 months) under the team of RAM.

##### 4) Agency Structure Rules

- Once the bonus is confirmed, the bonus factor will be locked on the policy (if the policy has the bonus factor, the following bonus calculation will use this factor. If the policy does not have the bonus factor, the bonus factor will be calculated and stored on the policy.)
- If the direct agents are promoted, the old policy's FYC/direct overriding will still count to old hierarchy with the same bonus factor.
- If the policy is assigned to a new agent, the old policy's case will still count to the old hierarchy. The renewal AM direct overriding will count to the new leader. If the leader is the same as the one before policy assignment, the direct overriding will be paid with the same factor. But if the leader is different, the direct overriding will be paid with the minimum factor: 40%.
- If the AM/SAM/RAM is demoted to a normal agent, then all the cases and overriding of the old policy of AM himself and previous direct agents will still count to the old hierarchy. User can use workaround to change to new hierarchy (transfer AM with policy in the same new unit after demotion)
- When there is policy transfer, the overriding depends on the transfer's date.
  - If payment is before policy transfer's date, overriding goes to AM.
  - If payment is after policy transfer's date, overriding goes to new AM.
- Agency structure rules:
  - The higher level cannot be attached to the lower lever department.
  - Super region is higher than region, region is higher than district, district is higher than unit.
  - Agent can be attached to any level department.

---

#### 7.2.2 New Agent Production Bonus

New agent production bonus = productivity bonus + volume bonus = FYC * productivity bonus rate + FYC * volume bonus rate

**Productivity Bonus:**

| Qualified Cases | Productivity Bonus Rate |
|-----------------|------------------------|
| < 3 | 0% |
| 3 – 3.99 | 10% |
| 4 – 4.99 | 15% |
| 5 – 6.99 | 20% |
| 7 – 8.99 | 30% |
| >= 9 | 35% |

**Volume Bonus:**

| Annualized First Year Commission | Volume Bonus Rate |
|----------------------------------|-------------------|
| < 4,000,000 | 0% |
| 4,000,000 – 6,499,999 | 10% |
| 6,500,000 – 8,999,999 | 15% |
| 9,000,000 – 11,999,999 | 20% |
| 12,000,000 – 14,999,999 | 30% |
| >= 15,000,000 | 35% |

**Rules:**
- Single premium commission is not qualified for this bonus. If the agent is inactive, the bonus will not be paid.
- Qualified case, AFYC are based on first 12 weeks. The payment productivity bonus and volume bonus are also based on first 12 weeks.
- If policy is assigned to another agent, new agent overriding on this policy will be stopped.
- When there is policy transfer, the overriding depends on the transfer date.
  - If payment is before policy transfer date, bonus goes to the original AM.

---

#### 7.2.3 Agent Referral Bonus

Agent referrer must produce at least one qualified case in the last rolling one month.

Recruiting bonus = referral bonus rate * FYC

- Currently, the referral bonus rate is set to 5%.
- Manager Level (RAM, SAM, and AM) is not allowed to be an introducer.
- If the rolling month has not reached one month, count the qualified case as one month. The rolling month is rolling from the end date of the last uncalculated month.
- If referee's policy is assigned to another agent, the bonus based on the assigned policy will be stopped.
- Single premium commission is not qualified for this bonus. If the agent is inactive, the bonus will not be paid.
- When there is policy transfer, the referral bonus depends on the transfer date.
  - If payment is before policy transfer date, bonus goes to original referral.

---

#### 7.2.4 Normal Production Bonus

Normal production bonus = productivity bonus + volume bonus = FYC * productivity bonus rate + FYC * volume bonus rate

**Productivity Bonus:**

| Total number of qualified cases in rolling 12 weeks (including current week) | Productivity Factor (% FYC) |
|------------------------------------------------------------------------------|----------------------------|
| < 3 | 0% |
| 3 – 3.99 | 10% |
| 4 – 4.99 | 15% |
| 5 – 6.99 | 20% |
| 7 – 8.99 | 30% |
| >= 9 | 35% |

**Volume Bonus:**

| Total Annualized First Year Commission (AFYC) in past rolling 12 weeks (including current week) | Volume Factor (% FYC) Payable |
|----------------------------------------------------------------------------------------------------|-------------------------------|
| < 4,000,000 | 0% |
| 4,000,000 – 6,499,999 | 10% |
| 6,500,000 – 8,999,999 | 15% |
| 9,000,000 – 11,999,999 | 20% |
| 12,000,000 – 14,999,999 | 30% |
| >= 15,000,000 | 35% |

**Rules:**
- The calculation of the AFYC for the past rolling 12 weeks is as follows:
  - If the policy issued is in yearly mode, then, the annual premium * first year commission rate is the AFYC for that policy.
  - If the policy issued is in other mode, (monthly, quarterly, half yearly), then, still no matter how many premium the client pays, system always uses the annual premium * first year commission rate to get the AFYC for that policy.
  - If the policy issued is in single mode, then the total premium * first year commission rate is used as the AFYC for that policy.
- Whether the case count is in rolling 12 weeks is based on the policy issue date (same as risk commencement date) and aggregation date, not policy commencement date. The system will calculate the 84 days period exactly from the closing (aggregation end) day. The result will only influence the current week payout.
- For the annual policy, the bonus will be paid only once. For other regular policies, the bonus factor will lock on the policy, which means the bonus based on the following renewal commission will be paid to the agent with the same factor.
- If the calculated bonus has not been confirmed after aggregation, this bonus factor will be recalculated in the next commission aggregation.
- If the agent is inactive, the bonus will not be paid. If the agent is still within his first 12 weeks (from his appointment date), then system will not calculate the weekly production bonus for that agent.
- If policy is assigned, the qualified case will still count to the old hierarchy, but the weekly production bonus based on assigned policy's FYC will be stopped.
- When there is policy transfer, the referral bonus depends on the transfer date.
  - If payment is before policy transfer date, bonus goes to AM.

---

#### 7.2.5 Year End Bonus

Year end bonus calculation will be triggered when the compensation aggregation period is over the end of calendar year. The following rules must be satisfied:
- 18 qualified cases in the calendar year
- Minimum P2 persistency of 75% from last 12 months premium collection (persistency requirement not required for 1st year producer)

**Year end bonus = FYC * Bonus Factor**

The producer appointment in the first year will have different sales targets as the first year may be an incomplete year:
- If the producer is recruited in Jan to March, the target will be 100%.
- If the producer is recruited in April to June, the target will be 75%.
- If the producer is recruited in July to September, the target will be 50%.
- If the producer is recruited in October to December, the target will be 25%.

---

#### 7.2.6 Persistency Bonus

The calculation of persistency is triggered on compensation aggregation and is based on producer level.

**Persistency Bonus = Sum of bonus factor * SYC**

- Bonus factor is based on the Px persistency
- Agent level only has agent persistency bonus, while other management levels have both persistency bonus and persistency overriding if they issue policies by themselves.

**Agent Persistency Bonus — Second Policy Year (payable monthly):**

| P2 | Bonus Factor (% SYC) |
|----|----------------------|
| < 75% | 0% |
| 75% – 79.99% | 5% |
| 80% – 84.99% | 15% |
| 85% – 89.99% | 25% |
| 90% – 94.99% | 35% |
| >= 95% | 45% |

**AM Persistency Overriding — Second Policy Year (payable monthly):**

| AM's total group P2 including personal sales | Persistency Overriding Factor (% SYC) |
|---------------------------------------------|---------------------------------------|
| < 75% | 0% |
| 75% – 79.99% | 10% |
| 80% – 84.99% | 15% |
| 85% – 89.99% | 20% |
| >= 90% | 25% |

**SAM Persistency Overriding — Second Policy Year (payable monthly):**

| Group P2 with personal | Factor for SAM's direct agent groups | Factor for direct AM groups |
|------------------------|--------------------------------------|----------------------------|
| < 75% | 0% | 0% |
| 75% – 79.99% | 15% | 10% |
| 80% – 84.99% | 25% | 15% |
| 85% – 89.99% | 35% | 20% |
| >= 90% | 45% | 25% |

**RAM Persistency Overriding — Second Policy Year (payable monthly):**

| Group P2 with personal | Direct agent factor | Direct AM groups factor | Direct SAM groups factor |
|------------------------|---------------------|-------------------------|-------------------------|
| < 75% | 0% | 0% | 0% |
| 75% – 79.99% | 25% | 15% | 5% |
| 80% – 84.99% | 35% | 20% | 10% |
| 85% – 89.99% | 45% | 25% | 15% |
| >= 90% | 55% | 30% | 20% |

---

#### 7.2.7 Development Allowance (payable monthly)

Development allowance is for partner only.

**Monthly Development Allowance (MDA) = base allowance * % of Achievement of year-to-date Sales Target**, or **Monthly Development Allowance (MDA) = base allowance * % of Achievement of current month Sales Target**

- Sales target varies with months and partners, for the checking of FYP.
- For the base allowance, minimum of MDA percentage and maximum of MDA percentage vary with partners and calendar years.

---

#### 7.2.8 Development Overriding (Payable Monthly)

Development overriding is for partner only.

In the first 12 months from the partner's appointment date:
**monthly overriding = A x B x 1.50 x FYC**

Starting from the 13th month from the partner's appointment date:
**monthly overriding = A x B x C x (FYC + SYC)**

Where:
- **A** refers to the following table:

| Factor A | Average Per month in net increase of agent manpower in partner's group from Jan 1st |
|----------|----------------------------------------------------------------------------------------|
| 15.0% | < 6 |
| 22.5% | 6 – 12 |
| 30.0% | 13 – 20 |
| 37.5% | 21 – 30 |
| 45.0% | >= 31 |

- **B** = current month agent activity ratio (active agents of all the team/inforce agents of all the team, including all the supervisors, but without the partner) of the partner's group
- **C** = current month P2 persistency ratio 12 months rolling
- **FYC** = current month total First Year Commission paid to the partner's group
- **SYC** = current month total Second Year Commission paid to the partner's group

---

#### 7.2.9 Annual Payment Bonus

- Only regular premium and target premium with annual payment are considered to contribute Annual Payment Bonus (APB) for extra payment to producer. Adhoc topup and recurring topup amount are not considered.
- For producer at agent level, **APB = basic commission for annual premium * APB rate for direct agent**
- For producer at manager level, **APB = self sales policies' basic commission for annual premium * APB rate for direct agent + all team's overriding bonus for annual premium * APB rate for manager**
- The overriding bonus is based on manager overriding for year 1 and persistency overriding bonus for year 2.
- APB rate is defined as follows:

**For agents (% commission):**

| Year | Annual | Semi-Annual | Quarterly | Monthly |
|------|--------|-------------|-----------|---------|
| 1 | 10% | 0% | 0% | 0% |
| 2 | 10% | 0% | 0% | 0% |

**For manager (% of overriding):**

| Year | Annual | Semi-Annual | Quarterly | Monthly |
|------|--------|-------------|-----------|---------|
| 1 | 5% | 0% | 0% | 0% |
| 2 | 5% | 0% | 0% | 0% |

- Manager will get two parts of the APB bonus, one is from their self policy sales which is based on basic commission, the other is from the whole team's performance which is based on overriding bonus.
- The payment frequency of the APB is based on the payment frequency of basic commission, manager overriding and persistency overriding. That means:
  - If a yearly payment regular premium is collected in the first year, APB of basic commission part and APB of manager overriding part are both paid weekly as basic commission and manager overriding are paid weekly.
  - If renew the premium on 2nd year, APB of basic commission part is paid weekly, while APB of persistency overriding is paid monthly as the persistency bonus is paid monthly.
- For basic commission, only the regular premium and target premium are considered for annual payment. The manager overriding and persistency overriding are based on the FYC/SYC of regular premium and target premium for annual payment only, while the bonus rates of overriding are based on all the existing policies, which means the overriding bonus rate does not need to be recalculated again for APB.

---

#### 7.2.10 Multiple Currency

If the policy currency is different from the base currency, system needs to convert the amount into base currency when calculating basic commission. Exchange rate will be on the system date when premium is applied. Other commission type will be calculated based on basic commission.

---

### 7.3 Adjust Compensation

After the compensation is defined, you can also adjust it if you want.

This section describes how to adjust compensation.

**Prerequisites:** Compensation is defined.

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Compensation > Adjust.
2. The Adjust Compensation page is displayed. If the compensation adjustment record already exists, set search criteria and then click Search to search it out; otherwise, click Create to create a new compensation adjustment record.
3. The Compensation Adjustment Maintenance page is displayed. Update the related information, and then click Submit.

**Table: Description of Fields in the Compensation Adjustment Maintenance Page**

| Field | Description |
|-------|-------------|
| Agent | Enter the agent code or double-click this field to select one. |
| Adjustment Level | Select a level from the drop-down list. If adjustment level is Producer, policy and benefit information is not mandatory. If adjustment level is Policy, policy information is mandatory. If adjustment level is Product, policy and benefit information is mandatory. |
| Policy No. | Policy number is mandatory if adjustment level is Policy or Product. |
| Benefit | Benefit is mandatory if adjustment level is Product. |
| Adjustment Item | Select an adjustment item from the drop-down list. |
| Adjustment Amount | The amount must be numeric. |
| Adjustment Reason | Select a reason from the drop-down list. |
| Tax Deduction Indicator | Used for tax calculation of adjustment. If Yes is selected, the adjustment needs to deduct tax in aggregation. If No is selected, the adjustment does not need to deduct tax. |
| Effective Date | Effective date of adjustment. This date must not be earlier than the last confirmed compensation end date. |

---

### 7.4 Aggregate Compensation

Aggregation is a step to sum up all the compensation with the calculated result for compensation in manual batch job. Compensation can be aggregated only after the previous aggregation has been confirmed. Compensation aggregation is a manual batch job to calculate and aggregate compensation for each producer.

This section describes how to aggregate compensation.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Compensation > Aggregate.
2. The Aggregate Compensation page is displayed. Enter the end date.
   - The start date is defaulted to the last end date of aggregation plus 1 day.
   - The end date must not be earlier than the start date.
   - The end date must not be earlier than the last confirmed aggregation date.
3. Click Submit.

**Compensation Aggregation Rules:**

1. When you click Submit, the system extracts the compensation records which meet the following criteria:
   - The status of basic commission and adjustment records is Waiting for issue.
   - The due date of compensation records which are earlier than or equal to the end date entered will be calculated.
   - System checks each compensation's frequency and due date based on the entered date. If any compensation covers more than one period by its frequency, system will calculate once for all in one aggregation, but generate a record for each period.
   - Compensation adjustment, basic commission and other compensation defined are added up together. It takes effect before the end date entered with status Waiting for issue for final compensation amount for each producer. If a record takes effect after the end date entered, it will not be extracted.
   - The total compensation is based on base currency.

---

### 7.5 Confirm Compensation

Compensation confirmation is a manual batch job to confirm the compensation amount before payment.

This section describes how to confirm compensation.

**Prerequisites:** Compensation has been aggregated successfully.

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Compensation > Confirm.
2. The aggregation record of compensation is displayed on the Confirm Compensation page. Click Submit.

**Compensation Confirmation Rules:**

1. When you click Submit:
   - The system retrieves qualified data that meets the following requirements:
     - Compensation status is Aggregated.
     - Compensation generation date is within the confirmation period.
   - The system confirms this compensation cycle.
     - The system updates the confirmed compensation status to Confirmed if confirmation is successful.
     - If any adjustment takes effect during the aggregation period which is not confirmed yet and an adjustment record is generated after this aggregation, system will remind user to run aggregation again to include this adjustment.
     - If Confirm Terminated Producer option is selected, system will confirm and prepare to pay terminated producer's compensation. If not, terminated producer only has the record of compensation but will not be paid.

---

### 7.6 Query Commission

Commission is the compensation at policy level. This section describes how to query commission.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Compensation > Query Commission.
2. The Query Commission page is displayed. Enter the search criteria and then click Search to search out the target agent commission records.
3. View commission information in the Search Result area. Click Download and the system will generate agent commission records by Excel.

**Commission Query Rules:**

1. Commission will generate only if TP (Non Allocation Charge of TP and Allocation Charge of TP) + STU fully filled for each installment period. But if TP and STU are deducted from UTU units, commission should not be generated for STU amount.

   1) **Commission generation rule for STU deducted from UTU:**
   - If UTU units are enough to cover TP + STU of one installment, system will deduct the UTU units to fill TP and STU. Commission of TP should be generated, while commission of STU should not be generated.
   - If UTU units are not enough to cover TP + STU of one installment, non-allocation charge will be deducted and commission of TP and STU will not be generated till premium comes in.

   2) **Commission generation rule when NAC is deducted:**
   Once premium is used to pay for the due dates which have the non-allocation charge deducted, system will check whether the premium has been fully paid.
   - If yes, system will generate the commission for TP and STU of the premium due.
   - Otherwise, system will not generate the commission of the premium due.

2. The commission calculation rules as follows:
   - The basic commission is calculated on benefit level. System will use Issue Date, which is benefit level information, to calculate the policy year (benefit year) of the benefit.
   - Basic commission = PC1*commission rate. PC1 is the total premium with extra premium. It includes the premium of all financial transactions, which means any change affecting the premium will be included.
   - Basic commission will be generated when the benefit is in Inforce status with the premium paid.
   - Basic commission rate is retrieved from the commission rate definition. The rider may have its own commission rate or follows the main benefit's commission rate.
   - The basic commission should be paid to the commission agent or the company that the commission agent belongs to.
   - Basic commission uses the base currency. The exchange rate on the date of basic commission generation is used to convert from policy currency to base currency.

---

### 7.7 Query Compensation Status

This section describes how to query compensation status.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Compensation > Query Compensation Status.
2. The Compensation Query page is displayed. Set search criteria and click Search.
3. View the compensation information.

---

### 7.8 Download and Upload Compensation Tax File

This section describes how to prepare data for tax calculation by downloading and uploading compensation data.

**Prerequisites:** Compensation has been aggregated.

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Compensation > Download and Upload Compensation Tax File.
2. The Download and Upload Compensation Tax File page is displayed. Download and upload compensation data.
   - In the Compensation File Download area, enter the start date and end date of compensation record, and then click Download to save the file.
   - In the Tax File Upload area, click Browse to select a file and then click Upload.

**Rules:**
- If you upload tax file twice in one period, the second file will replace the first one.

---

### 7.9 Generate Compensation Statement

This section describes how to generate compensation statement.

**Prerequisites:** Compensation aggregation has been confirmed.

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Compensation > Generate Compensation Statement.
2. The Generate Compensation Statement page is displayed. Set search criteria and click Search to search out the statement records.

**Rules:**
- Only the latest confirmed compensation for the specific producer will be displayed. When new compensation is confirmed, the existing result cannot be searched out again.
3. Select a statement record and click Download or Print to download or print the statement.

---

## 8. Manage Assessment

### 8.1 Define Assessment

Assessment refers to the rules used to check whether a producer is qualified for promotion, demotion or maintenance.

This section describes how to define assessment.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Assessment > Create or Modify.
2. The Create or Modify Assessment page is displayed. To modify existing assessment item, search it out and click its name. To add a new assessment item, click Create.
3. The Assessment Maintenance page is displayed. Enter assessment information and then click Submit.

---

### 8.2 Evaluate Assessment

Assessment evaluation is a manual batch job for the assessment checking for different levels of producer with the assessment frequency considered.

This section describes how to evaluate assessment.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Assessment > Evaluate.
2. The Evaluate Assessment page is displayed. Enter the end date and then click Submit.

**Table: Description of Fields in the Assessment Evaluation Page**

| Field | Description |
|-------|-------------|
| From | Start date of generating the assessment evaluation. Start date is the last end date of evaluation + 1 day. |
| To | End date of generating the assessment evaluation. End date must be later than start date. |

3. Click Batch Query to query batch status.

---

### 8.3 Assessment Evaluation Rules

#### 8.3.1 AM Maintenance Rules

If the active producer with Agency Manager (AM) level does not satisfy the following contract maintenance rules, the agency manager will be listed in the demotion list.

- The AM Validation Period is every 6 months with continues 12 months active status from AM position.
- AM must maintain a minimum total GROUP P2 persistency of 75%.
- Once the AM has been demoted, he/she has to remain as Agents for a minimum period of 6 months and fulfill all the promotion requirements before he/she can be promoted to AM again.

**AM Contract Maintenance Requirements:**

| Validation Period (from AM position start date to the generation date) | Minimum Manpower (Direct Agents under AM excluding the AM) | Minimum Activity Ratio (12 months average) | Minimum Total Team's Annualized First Year Commission (AFYC) in the last 12 months |
|---------------------------------------------------------------------|------------------------------------------------------|-------------------------------------------|------------------------------------------------------------------------------------|
| 6th month | 3 agents | 30% | 4500 |
| 12th month | 6 agents | 30% | 4500 |
| After 12th month | 6 agents, 2 new agents recruit every 6 months (new agent can be count to the total agent figure) | 30% | 4500 |

#### 8.3.2 AM Promotion Rules

For the active producer with Agency Manager (AM) level, the following rules need to be satisfied to promote the agency manager to senior agency manager:

- Minimum 6 months at AM position with continues active status in the previous 12 months from AM position start.
- Minimum total group production of 70 Qualified Cases.
- Total team's Annualized First Year Commission (AFYC) is more than 1200 in the last 12 months at AM position before the promotion.
- For promotion purpose, the mother AM can earned credits from production of new child AM group that was spin-off from the mother AM in the last 12 months to fulfill up to 50% of the qualified cases and AFYC requirements when child AM at AM position. This is only for promotion checking rules. Upon the mother AM promotion to SAM, AMs that were spin-off will automatically regroup under the new SAM, i.e., under their old mother.
- At least have 7 direct agents.
- Minimum average activity ratio (Average Activity Ratio = sum of total Number Active Producer in each month/ sum of total Number of manpower in each month) is 35% in the last 12 months (number of producer will calculate at the end of each month as the figure of that month)
- Minimum group P2 persistency of 75% from last 12 months premium collection.

#### 8.3.3 Agent Maintenance Rules

If the active producer doesn't satisfy the following contract maintenance rules, the active producer will be listed in the demotion list.

- Agent Validation Period is every 6 months with continues 12 months active status from appointment.
- An Agent must produce 3 qualified cases in each Validation Period.

#### 8.3.4 Agent Promotion Rules

Following rules need to be satisfied to promote agent to agency manager:

- Minimum 12 months at agent position with continues active status in the previous 12 months from appointment.
- Minimum personal production of 20 Qualified Cases.
- Total Annualized First Year Commission (AFYC) is more than 3000 in the last 12 months at agent position before the promotion.
- Minimum P2 persistency of 75% from last 12 months premium collection (persistency requirement not required for 1st year agent).

#### 8.3.5 RAM Maintenance Rules

If the active producer with Regional Agency Manager (RAM) level does not satisfy the following contract maintenance rules, the RAM will be listed in the demotion list.

- The RAM Validation Period is every 6 months with 12 months active status from RAM position.
- RAM must maintain a minimum total GROUP P2 persistency of 75%.
- Once the RAM has been demoted, he/she has to remain as SAM for a minimum period of 12 months and fulfill all the promotion requirements before he/she can be promoted to RAM again.

**RAM Contract Maintenance Requirements:**

| Validation Period (from RAM position start date to the generation date) | Minimum Group Manpower (include all direct & indirect agents under a SAM and AM) | Minimum Activity Ratio (12 months average) | Minimum Total Team's Annualized First Year Commission (AFYC) in the last 12 months |
|---------------------------------------------------------------------|------------------------------------------------------------------------|-------------------------------------------|------------------------------------------------------------------------------------|
| 6th month | 20 agents + 3 SAM | 30% | 32000 |
| 12th month | 24 agents + 4 SAM | 30% | 32000 |
| 18th month | 28 agents + 5 SAM | 30% | 34000 |
| 18th month & thereafter | direct/indirect | 30% | 34000 |
| - | Meanwhile, 4 new agents recruit every 6 months | - | - |

#### 8.3.6 SAM Maintenance Rules

If the active producer with Senior Agency Manager (SAM) level does not satisfy the following contract maintenance rules, the senior agency manager will be listed in the demotion list.

- The SAM Validation Period is every 6 months with continues 12 months active status from SAM position.
- SAM must maintain a minimum total GROUP P2 persistency of 75%.
- Once the SAM has been demoted, he/she has to remain as AM for a minimum period of 6 months and fulfill all the promotion requirements before he/she can be promoted to SAM again.

**SAM Contract Maintenance Requirements:**

| Validation Period (from SAM position start date to the generation date) | Minimum Group Manpower (include all direct & indirect agents under a AM) | Minimum Activity Ratio (12 months average) | Minimum Total Team's Annualized First Year Commission (AFYC) in the last 12 months |
|---------------------------------------------------------------------|---------------------------------------------------------------------|-------------------------------------------|------------------------------------------------------------------------------------|
| 6th month | 9 agents and 1 AM | 30% | 13000 |
| 12th month | 12 agents AND 1 AM | 30% | 13000 |
| 18th month | 2 AM & 15 agents | 30% | 14000 |
| 18th month & thereafter | 2 AM & 15 agents, Meanwhile, 3 new agents recruit every 6 months (new agent can be count to the total agent figure) | 30% | 14000 |

#### 8.3.7 SAM Promotion Rules

For the active producer with Senior Agency Manager (SAM) level, the following rules need to be satisfied to promote the senior agency manager to regional agency manager:

- Minimum 12 months as SAM position with continues 12 months active status from SAM position.
- Minimum total team production of 150 Qualified Cases.
- Total team Annualized First Year Commission (AFYC) of 27000 in the last 12 months before the promotion.
- For promotion purpose, the mother SAM can earned credits from production of new child SAM group that was spin-off from the mother SAM in the last 12 months to fulfill up to 50% of the qualified cases and AFYC requirements. Upon the mother SAM promotion to RAM, AMs that were spin-off will automatically regroup under the new RAM, i.e., under their old mother.
- Must have at least 16 direct and indirect agents and 2 AM in the last 12 months.
- Minimum average activity ratio (Average Activity Ratio = sum of total Number Active Producer in each month/ sum of total Number of manpower in each month) is 35% in the last 12 months (number of producer will calculate at the end of each month as the figure of that month).
- Must have minimum 1 AM team that fulfill the AM contract maintenance.
- Minimum group P2 persistency of 75% from last 12 months premium collection.

---

### 8.4 Monitor Assessment

This section describes how to monitoring assessment result.

**Prerequisites:**
- Rules of assessment have been defined.
- Assessment evaluation has run.

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Assessment > Monitor.
2. The Monitor Assessment page is displayed. Set search criteria and click Search to search out the assessment record.
3. View the assessment result of the producer.

---

### 8.5 Confirm Assessment

Assessment confirmation is a manual batch job to confirm the result of assessment to be correct.

This section describes how to confirm assessment.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Assessment > Confirm.
2. The Confirm Assessment page is displayed. Click Submit.

---

### 8.6 Promote or Demote Producer

This section describes how to promote (change from a lower position to a higher position) and/or demote (change from a higher position to a lower position) a producer.

**Prerequisites:** N/A

**Procedures:**

1. From the main menu, select Sales Channel and Commission > Assessment > Adjust Producer Position.
2. The Adjust Producer Position page is displayed. Enter the producer code, select a new position from the drop-down list, and then select a new agent organization.

**Table: Description of Fields in the Promotion & Demotion Page**

| Field | Description |
|-------|-------------|
| Producer Code | Enter the producer code or double-click this field to select one. The producer must meet the following requirements: The producer code must exist. The producer must have at least one position. |
| New Position | Select a position from the drop-down list. The new position must be different from the current position of agent. |
| Transfer Date | Effective date of the promotion or demotion. Transfer date must not be earlier than the system date. |
| New Supervisor Code | Enter the supervisor code or double-click this field to select one. |
| Comments | Enter your comments if any. |

3. Click Submit.

**Rules:**

For promotion, system will change the position first, and then verify the nurture relationship:
- His/her nurturee in the original position will report to him/her directly besides the nurture relationship.
- His/her leader in the original position will be nurtured in the new position.

**Promotion and Demotion Rules:**

**Relationship Change due to Promotion:**
- New supervisor is old supervisor's leader by default, but user can change it.
- The promoted producer's direct and indirect staff will go with him if the new position of promoted producer still allows managing his staff (check direct staff only). If not, these staff with their tree will report to the promoted producer's old supervisor.
- All nurturees of the promoted producer will report to him as staff with their tree automatically. If the nurturee is not allowed to report to the new position of promoted producer, they will keep in the old hierarchy.
- Nurturer will not be updated when promotion occurs.

**Relationship Change due to Demotion:**
- New supervisor is demoted producer's nurturer by default. If the nurturer does not exist or does not allow reporting to by demoted position, the demoted producer will be his old supervisor's direct producer at demoted position. User can change the default supervisor.
- Demoted producer's direct and indirect staff will keep their structures and report to him still. Only the tree that does not allow to report to him after demotion will report to the demoted producer's old supervisor.
- Nurturer will not be updated when demotion occurs.

---

## 9. Sales Channel Batch Jobs

### 9.1 Production Generation Batch

This section describes the batch job of calculating production for each benefit.

**Prerequisites:** Production calculation has been defined.

**Procedures:**

1. System calculates production for each benefit on sales agent directly.
2. System snapshoots current hierarchy for future use.
3. System records production details on producer with hierarchy date.

---

### 9.2 Active Status Batch

Active status is a kind of status of producer related to his/her performance based on specific rules.

System defines the producer as active if he/she issues one qualified case (QC) in a month. In this month, the producer is marked as active agent.

**Note:** QC = number of inforce policies * contribution rate. For single premium policy, the contribution rate is 0.15; for regular premium policy, the contribution rate is 1.

This section describes the batch job of checking the active status of producer.

**Prerequisites:** Active status has been defined.

**Procedures:**

1. On the last date of the month, the system tracks all the QCs for each producer with status Inforce and calculates the total number of QCs for each producer in current month.
   - If the total number of QCs for producer is less than one, system sets the active status of the corresponding producer to No in this month.
   - Otherwise, system sets the active status of the corresponding producer to Yes in this month.
2. The end.

---

### 9.3 Persistency Production Batch

This section describes the batch job of generating persistency related production.

**Prerequisites:** Production for persistency calculation has been defined.

**Procedures:**

1. On the last date of the month, the system tracks all the transactions for policy and calculates related production for persistency calculation.
2. System records persistency details for each producer.

---

### 9.4 Performance Calculation Batch

This section describes the batch job of calculating the performance for each benefit on producer level.

**Prerequisites:** The performance calculation has been defined.

**Procedures:**

1. System checks each due date of performance.
   - If any performance is on due date, go to step 2.
   - If no performance is on due date, the batch ends.
2. The system generates performance information for each producer.

---

## 10. INVARIANT Declarations

**INVARIANT 1:** Only active and licensed producers can submit new business applications.
- Enforced at: NB submission
- If violated: Unauthorized business submitted; compliance risk

**INVARIANT 2:** Commission is calculated as Premium × Commission Rate %.
- Enforced at: Commission calculation
- If violated: Incorrect commission paid; financial loss

**INVARIANT 3:** Persistency Rate = Policies in Force at Month 13 / Policies Issued at Month 0.
- Enforced at: Persistency Calculation Batch
- If violated: Incorrect persistency reported; wrong performance evaluation

**INVARIANT 4:** Confirmed compensation is locked and cannot be modified.
- Enforced at: Confirm Compensation
- If violated: Compensation amounts changed after payment authorization

**INVARIANT 5:** Basic commission is calculated at benefit level using Issue Date to determine policy year (benefit year).
- Enforced at: Commission generation
- If violated: Incorrect policy year used for commission rate; financial loss

**INV
**INVARIANT 5:** Basic commission is calculated at benefit level using Issue Date to determine policy year (benefit year).
- Enforced at: Commission generation
- If violated: Incorrect policy year used for commission rate; financial loss

**INVARIANT 6:** Producer active status is determined monthly: QC < 1 in a calendar month sets active status to No.
- Enforced at: Active Status Batch (last date of month)
- If violated: Incorrect producer activity status; performance evaluation affected

**INVARIANT 7:** Nurture relationship defaults to supervisory relationship; is updated automatically on transfer, promotion, and demotion.
- Enforced at: Transfer Producer, Promote or Demote Producer
- If violated: Incorrect bonus calculations that depend on nurture relationship

**INVARIANT 8:** Policy hierarchy (Old Hierarchy / New Hierarchy) determines which supervisor hierarchy shares production after a producer transfer.
- Enforced at: Transfer Producer
- If violated: Production credited to wrong hierarchy; commission paid to wrong producers

**INVARIANT 9:** AM/SAM/RAM must maintain minimum GROUP P2 persistency of 75% to avoid demotion listing.
- Enforced at: Assessment Evaluation Batch
- If violated: Producer not listed for demotion despite failing maintenance threshold

**INVARIANT 10:** Once confirmed, compensation records cannot be modified except through adjustment records with effective date after the last confirmed compensation end date.
- Enforced at: Confirm Compensation, Adjust Compensation
- If violated: Unauthorized changes to confirmed compensation; financial and compliance risk

---

## 11. Key Formulas

**Persistency Rate:**
`
Sx (S1/S2) = AAP / EAP * 100%
Kx (K1/K2) = ASAP / ESAP * 100%
Px (P1/P2) = ACP / ECP * 100%
`

**Annualized Premium (AP):**
`
AP = installment premium (with or without extra premium) * mode of premium
Mode of Premium: Yearly=1, Half-yearly=2, Quarterly=4, Monthly=12
`

**Standardized Annualized Premium (SAP):**
`
If PPT >= Spread Over Year (10): SAP = AP
If PPT < Spread Over Year (10): SAP = (AP * PPT) / min(Spread Over Year, CT)
`

**First Year Commission (FYC):**
`
FYC = PC1 * commission rate
PC1 = total premium with extra premium (all financial transactions affecting premium)
`

**Persistency Bonus:**
`
Persistency Bonus = Sum of (bonus factor * SYC)
Bonus factor based on Px persistency level
`

**New Agent Production Bonus:**
`
New agent production bonus = FYC * productivity bonus rate + FYC * volume bonus rate
`

**Normal Production Bonus:**
`
Normal production bonus = FYC * productivity bonus rate + FYC * volume bonus rate
`

**Year End Bonus:**
`
Year end bonus = FYC * Bonus Factor
Prerequisites: 18 qualified cases in calendar year AND P2 persistency >= 75%
`

**Monthly Development Allowance (MDA):**
`
MDA = base allowance * % of Achievement of year-to-date Sales Target
or
MDA = base allowance * % of Achievement of current month Sales Target
`

**Development Overriding (first 12 months):**
`
monthly overriding = A x B x 1.50 x FYC
`

**Development Overriding (from 13th month):**
`
monthly overriding = A x B x C x (FYC + SYC)
Where:
  A = net agent manpower increase factor (15% to 45%)
  B = current month agent activity ratio
  C = current month P2 persistency ratio (12 months rolling)
  FYC = current month total First Year Commission paid to partner's group
  SYC = current month total Second Year Commission paid to partner's group
`

**Annual Payment Bonus (APB) �� Agent:**
`
APB = basic commission for annual premium * APB rate for direct agent
`

**Annual Payment Bonus (APB) �� Manager:**
`
APB = self sales policies' basic commission for annual premium * APB rate for direct agent
    + all team's overriding bonus for annual premium * APB rate for manager
`

**Qualified Case (QC):**
`
QC = number of inforce policies * contribution rate
Single premium policy: contribution rate = 0.15
Regular premium policy: contribution rate = 1
`

**AFYC Calculation (Rolling 12 Weeks):**
`
Yearly mode policy: AFYC = annual premium * first year commission rate
Other mode (monthly/quarterly/half-yearly): AFYC = annual premium * first year commission rate
Single mode policy: AFYC = total premium * first year commission rate
`

---

## 12. Menu Navigation Table

| Action | Path |
|--------|------|
| Maintain Producer (Channel Organization) | Sales Channel and Commission > Channel Setup > Maintain Producer |
| Maintain Physical Location | Configuration Center > Sales Channel Configuration > Maintain Physical Location |
| Supervisory Relationship | Sales Channel and Commission > Hierarchy > Supervisory Relationship |
| Nurture Relationship | Sales Channel and Commission > Hierarchy > Nurture Relationship |
| Transfer Producer | Sales Channel and Commission > Producer > Transfer Producer |
| Maintain Qualification | Sales Channel and Commission > Producer > Maintain Qualification |
| Modify Producer Position Status | Sales Channel and Commission > Producer > Modify Producer Position Status |
| Modify Service Producer | Sales Channel and Commission > Producer > Modify Service Producer |
| Modify Commission Producer | Sales Channel and Commission > Producer > Modify Commission Producer |
| Modify Performance Producer | Sales Channel and Commission > Producer > Modify Performance Producer |
| Define Performance (Create or Modify) | Sales Channel and Commission > Performance > Create or Modify |
| Query Persistency | Sales Channel and Commission > Performance > Query Persistency |
| Define Compensation (Create or Modify) | Sales Channel and Commission > Compensation > Create or Modify |
| Adjust Compensation | Sales Channel and Commission > Compensation > Adjust |
| Aggregate Compensation | Sales Channel and Commission > Compensation > Aggregate |
| Confirm Compensation | Sales Channel and Commission > Compensation > Confirm |
| Query Commission | Sales Channel and Commission > Compensation > Query Commission |
| Query Compensation Status | Sales Channel and Commission > Compensation > Query Compensation Status |
| Download and Upload Compensation Tax File | Sales Channel and Commission > Compensation > Download and Upload Compensation Tax File |
| Generate Compensation Statement | Sales Channel and Commission > Compensation > Generate Compensation Statement |
| Create or Modify Assessment | Sales Channel and Commission > Assessment > Create or Modify |
| Evaluate Assessment | Sales Channel and Commission > Assessment > Evaluate |
| Monitor Assessment | Sales Channel and Commission > Assessment > Monitor |
| Confirm Assessment | Sales Channel and Commission > Assessment > Confirm |
| Adjust Producer Position (Promote/Demote) | Sales Channel and Commission > Assessment > Adjust Producer Position |

---

## 13. Related Files

| File | Relationship |
|------|-------------|
| insuremo-v3-ug-nb.md | NB �� producer linking to policies |
| ps-commission.md | Current version commission rules |
| ps-underwriting.md | UW �� producer licensing check |
