/**********************************************************************************************************/
-- Query: Common Table Expression Example
-- CreateBy: Martin Palkovic
-- Create date: 2022-05-03
-- Description: Example of a common table expression query, a variation of which I used in a production integration process
-- Modified by:
-- Modify date:
-- Mod Reason:
/***********************************************************************************************************/
with
get_source_and_intercompany_accounts as (
  select
  CCD.company as SourceCompanyCode
    , DCD.company as DestCompanyCode
    , ERE."PaymentTypeCode" as Payment_Type_Code
    , JEL."DebitOrCredit" as Debit_Or_Credit
    , sum(case
          when (GTDA.Tax_ID like '%PST%' or GTDA.Tax_ID like '%QST%') and  ERE."ExpenseTypeName" not like '%Meals%' and  ERE."ExpenseTypeName" not like '%Mileage%'
              then cast(JEL."Amount" as number(20, 2)) - cast(coalesce(ITL."QSTValue", 0) as number(20, 2)) - cast(coalesce(ITL."HSTValue", 0) as number(20, 2))
          when (GTD.Tax_ID like '%HST%' or GTD.Tax_ID like '%GST%')  and ERE."ExpenseTypeName" not like '%Meals%' and  ERE."ExpenseTypeName" not like '%Mileage%'
              then cast(JEL."Amount" as number(20, 2)) - cast(coalesce(ITL."HSTValue", 0) as number(20, 2)) - cast(coalesce(ITL."QSTValue", 0) as number(20, 2))
          when (GTDA.Tax_ID like '%PST%' or GTDA.Tax_ID like '%QST%') and  ERE."ExpenseTypeName" like '%Meals%'
              then cast(JEL."Amount" as number(20, 2)) - cast(coalesce(ITL."QSTValue", 0) * 0.5 as number(20, 2)) - cast(coalesce(ITL."HSTValue", 0) * 0.5 as number(20, 2))
          when (GTD.Tax_ID like '%HST%' or GTD.Tax_ID like '%GST%')  and ERE."ExpenseTypeName" like '%Meals%'
              then cast(JEL."Amount" as number(20, 2))  - cast(coalesce(ITL."HSTValue", 0) * 0.5 as number(20, 2)) - cast(coalesce(ITL."QSTValue", 0) * 0.5 as number(20, 2))
          when (GTDA.Tax_ID like '%PST%' or GTDA.Tax_ID like '%QST%') and  ERE."ExpenseTypeName" like '%Mileage%'
              then cast(JEL."Amount" as number(20, 2)) - cast(coalesce(VEL."TaxPostedAmount", 0) as number(20, 2))
          when (GTD.Tax_ID like '%HST%' or GTD.Tax_ID like '%GST%')  and ERE."ExpenseTypeName" like '%Mileage%'
              then cast(JEL."Amount" as number(20, 2))  - cast(coalesce(VEL."TaxPostedAmount", 0) as number(20, 2))
      else cast(JEL."Amount" as number(20, 2))
                  end) as Amount
    , concat_ws('-',JEL."AccountCode",ITL."CostCentreCode",ITL."DepartmentCode") as Intercompany_Account
    , case
        when CCD.company != DCD.company then GIA.Account_Number
        else GIA.Account_Number
        end as Source_Account

  from dbo.V_EXPENSE_REPORT_HEADER ERH

  left join dbo.V_EXPENSE_REPORT_ENTRIES ERE
    on ERH."ReportID" = ERE."ReportID"

  left join dbo.V_ITEMIZATION_LIST ITL
    on ERE."ReportEntryID" = ITL."ReportEntryID"

  left join dbo.V_ALLOCATIONS_LIST ALS
    on ITL."ItemizationID" = ALS."ItemizationID"

  left join dbo.V_JOURNAL_ENTRIES_LIST JEL
    on ALS."AllocationID" = JEL."AllocationID"

  left join dbo.V_VAT_ENTRIES_LIST VEL
    on ALS."AllocationID" = VEL."AllocationID"

  left join xref.GP_COMPANY CCD
    on CCD.companycode = ERH."SourceCompany"

  left join xref.GP_COMPANY DCD
    on DCD.companycode = ITL."CompanyCode"

  left join xref.TAXES TAX
    on TAX.PROVINCE = 'NB'

  left join xref.GP_TAX_Account_DTL GTD
    on GTD.TXDTLPCT = COALESCE(TAX.GST, TAX.HST)
    and CCD.company = GTD.division

  left join xref.GP_TAX_Account_DTL GTDA
    on GTDA.TXDTLPCT = COALESCE( TAX.PST, TAX.QST)
    and CCD.company = GTDA.division

  left join xref.dbo_GP_INTERCOMPANY_ACCTS GIA
    on GIA.company = DCD.company

  where
  ERH."PaidDate" >= ?
  and ERH."ReportID" = ?
  and SourceCompanyCode != DestCompanyCode
  and ERH."ApprovalStatusCode"='A_APPR'
  and cast(JEL."Amount" as number(20, 2)) is not null

  group by CCD.company
  , DCD.company
  , INTERCOMPANY_ACCOUNT
  , SOURCE_ACCOUNT
  )

/* Credit Card Expenses - Debit */
select
  SourceCompanyCode
, DestCompanyCode
, Amount
, Intercompany_Account
, Source_Account
from get_source_and_intercompany_accounts 

where Payment_Type_Code = 'CBCP'
and Debit_Or_Credit = 'DR'

union all

/* Cash - Debit */
select
  SourceCompanyCode
, DestCompanyCode
, Amount
, Intercompany_Account
, Source_Account
from get_source_and_intercompany_accounts 

where Payment_Type_Code = 'CASH'
and Debit_Or_Credit = 'DR'

union all

/* Credit Card Expenses - Credit */
select
  SourceCompanyCode
, DestCompanyCode
, Amount
, Intercompany_Account
, Source_Account
from get_source_and_intercompany_accounts 

where Payment_Type_Code = 'CBCP'
and Debit_Or_Credit = 'CR'

union all

/* Cash - credit  */
select
  SourceCompanyCode
, DestCompanyCode
, Amount
, Intercompany_Account
, Source_Account
from get_source_and_intercompany_accounts 

where Payment_Type_Code = 'CASH'
and Debit_Or_Credit = 'CR'