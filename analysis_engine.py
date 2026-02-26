#import config
import pandas as pd
import numpy as np
from openai import AzureOpenAI
from config_streamlit import client, AZURE_OPENAI_DEPLOYMENT,system_prompt,user_prompt,insight_system_prompt,insight_user_prompt2
def run_ai_cost_analysis(df):

  cols_to_drop = [
    "ner_rule",
    "reason",
    "last_known_cost_type_po_/_quote",
    "variance_from_last_known_lead_time_in_days"
    "predicted_lead_time_days_max",
    "item_mape_%",
    "predicted_cost_price_ner",
    "predicted_cost_price_ner"
    "variance_from_last_known_price_%"
    "number_of_records",
    "quote_valid_from",	
    "quote_valid_to",
    "po_age_months"
    ]

  df.drop(
      columns=[col for col in cols_to_drop if col in df.columns],
      inplace=True
  )
  # client = AzureOpenAI(
  #   api_key=aoi_api_key,
  #   api_version="2024-02-15-preview",
  #   azure_endpoint=aoi_api_url
  # )

  user_prompt1=f"""
  We have a pandas dataframe named `df`.
  Columns available:
  {list(df.columns)}
  """
  response = client.chat.completions.create(
      model=AZURE_OPENAI_DEPLOYMENT,  # This is your deployment name
      messages=[
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": user_prompt1+user_prompt}
      ],
      max_tokens=2000 
  )

  #print(response.choices[0].message.content)
  generated_code=response.choices[0].message.content
  execution_scope = {"df": df}
  #before_exec_vars = set(globals().keys())
  exec(generated_code, globals(), execution_scope)
  generated_dataframes = {
    name: obj
    for name, obj in execution_scope.items()
    if isinstance(obj, pd.DataFrame)
  }
  json_payload = {
    name: df.round(2).to_json(orient="records")
    for name, df in generated_dataframes.items()
  }
  dynamic_data_section = ""

  for name, json_data in json_payload.items():
      dynamic_data_section += f"\n{name}:\n{json_data}\n"

  insight_user_prompt1 = f"""
  Below are structured procurement analytics outputs generated from supplier cost estimation data.

  {dynamic_data_section}
  """
  response_insights = client.chat.completions.create(
    model=AZURE_OPENAI_DEPLOYMENT,
    messages=[
        {"role": "system", "content": insight_system_prompt},
        {"role": "user", "content": insight_user_prompt1+insight_user_prompt2}
    ]
  )

  final_insights = response_insights.choices[0].message.content

  print(final_insights)
  return final_insights



