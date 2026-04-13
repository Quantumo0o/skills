# InsureMO V3 User Guide — ProductFactory System Configuration Guide

## Metadata
| Field | Value |
|-------|-------|
| File | insuremo-v3-pf-system-config.md |
| Source | eBaoTech_LifeProductFactory_System_Configuration_Guide_0.pdf |
| System | LifeProductFactory 3.8 |
| Version | V3 (legacy) |
| Date | 2014-07 |
| Category | System Administration / Access Control |
| Pages | 24 |

## 1. Purpose of This File

Answers questions about system administration, access control, and role configuration in LifeProductFactory 3.8. Covers organization hierarchy, user management, role types (Operation/Limitation/Accessible Organization), and access control rules. **Note:** This is the System Configuration Guide (separate from the Product Configuration Guide). This is primarily relevant for system administrators and implementation consultants setting up a new organization.

---

## 2. Organization Structure

### Organization Hierarchy
- LifeProductFactory supports **unlimited levels** of organization
- Level 1 = Head office
- Level 2 = Company/Carrier (mapped to financial data and reporting)
- Lower levels = branches organized by: Line of Business / Carrier / Region / Country

### Organization by Line of Business Example
```
Head Office (Level 1)
  └── Company A (Level 2)
        ├── Health Company (Level 3)
        │     └── Regional branches
        └── Life Company (Level 3)
              └── Regional branches
```

### Organization by Carrier Example
```
Head Office
  └── Company B
        ├── Universal America
        └── Company Group
```

---

## 3. Access Control Model

### Three Types of Roles

| Role Type | Defines | Editable |
|-----------|--------|----------|
| **Operation Role** | Menus/modules user can access | NO (predefined) |
| **Limitation Role** | What user can do within operation role | Partially |
| **Accessible Organization Role** | Organizations user can access | NO (each org = one role) |

### Product Definition Limit Roles (a Limitation Role type)

| Role | What user can do |
|------|----------------|
| View Product | View product information only |
| Create Product | Create new product in product definition |
| Edit Product | Edit product if Editable indicator = Yes |
| Editable Product | Edit product even if Editable indicator = No |

### Accessible Organization Rules
- Once an organization is assigned to a user, the user can access:
  - That organization
  - All branches under that organization
  - All departments under those organizations and branches
  - All users associated with those organizations/branches/departments

**Note:** Organization access control applies to policy/proposal transactions. It does NOT apply to Party and Claims.

### Menus Restricted by Organization Access
When a user has limited organization access, they can only search policies/proposals under their accessible organizations via:
- Query > Common Query
- Query > New Business
- Query > Payment > Single Payment
- Query > Reinsurance
- NB menus (Reversal, Medical Billing, Print Policy, Policy Confirmation, Advanced Function)
- CS menus (Registration, Entry, UW, Confirmation, Approval, Cancellation, Ad hoc, Advanced Adjustment)
- Image Management (Query, Delete)
- Communication > Document (all functions)

---

## 4. User Creation Process

### Standard User
1. Create individual party: Party Management > Maintain Party
2. Click Maintain User to create user for the party
3. Assign roles to the user

### Agent User
1. Create agent: Sales Channel and Commission > Producer > Maintain Producer
2. Click Maintain User to create the agent user
3. Assign roles to the user

---

## 5. Profile Management

### User Profile
A profile = collection of rights (operation role + limitation role + accessible organization role) assigned to an organization.

### Profile Assignment Flow
```
Step 01: Create profile (System Administration > Profile Management)
         → Select organization for the profile
Step 02: Assign rights to the profile (operation + limitation + accessible org roles)
Step 03: Assign profile to organization
         → One profile → one or multiple orgs: Allocate Role to Organization
         → Multiple profiles → one org: Allocate Organization to Role
Step 04: Assign profile to user
         → One profile → one or multiple users: Profile/Role Authorization
         → Multiple profiles → one user: User Management
```

---

## 6. Role Assignment

### Operation Role Assignment
- Assign to organization first, then to user
- **Super Admin:** Can assign role to any organization
- **Admin:** Can only assign role to lower organizations

### Limitation Role Assignment
Organization-related limitation roles include:
- BCP APL, PL and Suspense Adjustment Limit
- BCP Backdating Limit
- Change Payment Details
- BCP Requisition for Payment
- BCP Waiver of Interest Limit
- Financial Adjustment
- BCP Cancel Cheque
- GP_Collbank and GP_Paybank
- Document Management Limit
- **Underwriting Authority** (not org-related — but needs updated raUWCategory and raUWLevel rate tables)

---

## 7. Access Control Rules

### Profile Rules
1. Super Admin + Admin of the profile's organization can delete/modify the profile
2. If profile's organization = current user's organization: current user can delete/modify it
3. If profile's organization is same level as current user's org: upper org can cancel assignment
4. If profile's organization is lower level than current user's org: current user cannot modify/delete/assign rights to it
5. Only rights that the Admin's organization has can be assigned to the profile
6. Only Super Admin can modify a profile that is assigned to an org where the Admin has no rights

### Rights Assignment Rules
1. Rights must be assigned to the **organization first**, then to the **user**
2. **Super Admin:** Can assign rights to any org and any user
3. **Admin:** Can only assign rights to lower organizations
4. If Admin's org doesn't have certain rights: Admin cannot see whether target org already has those rights

### Note on Visible vs Actual Rights
> "If the organization of the current Admin does not have certain rights, the Admin will not know whether the organization he/she wants to assign rights to are already assigned with these rights by another Admin or not."

---

## 8. New Organization Configuration Checklist

When a new branch is added:

### Step 1: Create Organization, Department, User
- Create new organization
- Create departments under the new organization
- Create users under the new departments

### Step 2: Assign Roles
1. **Operation Roles** — Enable system access
2. **Limitation Roles** — Enable org-specific limitations (BCP adjustment, backdating, payment changes, etc.)
3. **Accessible Organization Roles:**
   - For **existing users:** Assign new org to their profile
   - For **new users:** Assign accessible org roles directly

---

## 9. Menu Paths Reference

| Action | Path |
|--------|------|
| Create org/dept/user | Party Management > Maintain Party |
| Create agent user | Sales Channel and Commission > Producer > Maintain Producer |
| Create profile | System Administration > Profile Management |
| Assign profile to org | System Administration > Organization Authority Management > Allocate Role to Organization |
| Assign org to profile | System Administration > Organization Authority Management > Allocate Organization to Role |
| Assign role to user | System Administration > Profile/Role Authorization |
| Assign user to role | System Administration > User Management |

---

## 10. Related Files

| File | Relationship |
|------|-------------|
| insuremo-v3-ug-nb.md | NB — user access to NB functions |
| ps-claims.md | Claims — NOT subject to org access control |
