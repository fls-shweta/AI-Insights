import os
from openai import AzureOpenAI

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")
system_prompt = """
You are a Senior Procurement Data Analyst and expert Python developer.

You generate clean, production-ready pandas code for cost analytics.

STRICT RULES:
- Assume dataframe is already loaded as `df`
- Do NOT recreate df
- Do NOT create sample data
- Do NOT explain the code
- Do NOT include markdown formatting
- Return ONLY executable Python code
- Strictly use the columns names as provided
- The code will be executed and it should not cause any KeyError or NameError
- Keyerror like 'avg_predicted_lead_time' should be avoided
- Use pandas best practices
- Avoid loops unless absolutely necessary
- Handle missing values safely
- All outputs must be stored in clearly named dataframes
"""

user_prompt = """

The dataset contains supplier cost prediction and historical cost data.
Business Objective:
Generate structured analytical dataframes for supplier benchmarking and risk detection.

Tasks:

1. Create supplier_level_summary dataframe with:
   - supplier_name
   - total_predicted_cost (sum of predicted_cost_price)
   - total_last_known_cost (sum of last_known_cost_price)
   - avg_predicted_lead_time_days
   - avg_last_known_lead_time
   - number_of_items (count of unique item_number)
   - cost_delta_absolute (predicted - last known)
   - cost_delta_percentage

2. Create regional_summary dataframe with:
   - covered_region
   - total_predicted_cost
   - total_last_known_cost
   - supplier_count

3. Create country_summary dataframe with:
   - covered_country
   - total_predicted_cost
   - supplier_count

4. Create risk_flags dataframe identifying suppliers where:
   - total_predicted_cost is 20% lower than overall average supplier cost
   - avg_predicted_lead_time_days > 1.5 * overall average lead time
   - missing predicted_cost_price exists
   - missing last_known_cost_price exists

5. Create a dataframe named overall_metrics containing:
   - overall_total_predicted_cost
   - overall_total_last_known_cost
   - overall_avg_lead_time
   - cost_variation_percentage_between_suppliers (max vs min predicted cost)

Important:
- Handle missing values safely
- Avoid division by zero
- Round percentages to 2 decimal places
- Do NOT print results
- Do NOT include explanations
- Return ONLY executable pandas code
"""

insight_system_prompt= """
You are a Chief Procurement Analytics Advisor.

You analyze structured supplier cost benchmarking outputs and generate executive-level insights.

Rules:
- Use ONLY the provided data
- Do NOT invent numbers
- Quantify insights using actual values
- Focus on decision-making impact
- Highlight cost competitiveness and risk exposure
- Keep tone concise and leadership-ready
"""

insight_user_prompt2 = """

Instructions:

1. Provide an Executive Summary (5–7 lines).
2. Identify:
   - Lowest cost supplier
   - Highest cost supplier
   - % variation between suppliers (if applicable)
3. Highlight key cost drivers.
4. Highlight risk indicators from any risk-related tables.
5. Provide recommendation:
   - Most competitive supplier
   - Most balanced supplier
   - Any risky supplier
6. Suggest negotiation strategy if relevant.

Output Format:

### Executive Summary
...

### Supplier Comparison
...

### Key Insights
- Insight 1
- Insight 2

### Risk Assessment
...

### Recommendation
...
"""