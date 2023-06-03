"""
Name: Parse XML, extract a field, compare that field to a field from a csv for diffs
By: Martin Palkovic
Date: 2022-08-18
Description: 
"""

# Import Modules
import pandas as pd

# Paste your xml here
xml = """
<Pallet>
 <Packs>
  <Pack>
   <Properties>
    <Property name="Id">1</Property>
    <Property name="Site">warehouse1</Property>
    <Property name="Pallet">1</Property>
    <Property name="Units">127</Property>
    <Property name="Weight">9.16</Property>
    <Property name="DateTime">08/16/2022 15:38:55</Property>
   </Properties>
  </Pack>
  <Pack>
   <Properties>
    <Property name="Id">2</Property>
    <Property name="Site">warehouse2</Property>
    <Property name="Pallet">2</Property>
    <Property name="Units">450</Property>
    <Property name="Weight">13.3</Property>
    <Property name="DateTime">08/17/2022 15:39:26</Property>
   </Properties>
  </Pack>
 </Packs>
</Pallet>
"""

# Parse XML
df = pd.read_xml(xml, xpath=".//Property")

# Extract only the columns we need from the XML
df_pallet = df.loc[df["name"] == "Pallet"]

# Read CSV
df_csv = pd.read_csv(r"your_csv_here.csv")

# Convert values to Python list, cast to integer
pallet = df_pallet["Property"].tolist()
pallet = [int(i) for i in pallet]
csv = df_csv["Pallet"].tolist()

# Compare differences
print([i for i in pallet if i not in csv])
