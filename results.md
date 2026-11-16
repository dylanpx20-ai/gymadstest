# Results & Key Takeaways

## NYC Gym Marketing Budget — GPT-6 Assisted Monte Carlo Simulation

This project used **OpenAI's GPT-6 to assist in developing a Python Monte Carlo simulation that evaluated 600,000 potential monthly marketing outcomes in just 11.49 seconds**. The simulation compared four marketing budget strategies across three CPC environments (Conservative, Moderate, and High) to determine which allocation of a $10,000 monthly budget would maximize new paying gym members while minimizing Customer Acquisition Cost (CAC).

## Simulation Summary Results

The table below summarizes the results of **50,000 simulations per strategy-environment combination**, including median leads, median new paying members, downside and upside outcomes (10th and 90th percentiles), median CAC, and the probability of acquiring at least 35 new members in a month.

| CPC Environment | Strategy | Median Leads | Median Members | P10 Members | P90 Members | Median CAC | P(35+ Members) |
|---|---|---:|---:|---:|---:|---:|---:|
| Conservative | A: Meta-Heavy | 249 | 50 | 33 | 75 | $200.00 | 87.74% |
| Conservative | B: High-Intent | 211 | 55 | 38 | 76 | $181.82 | 94.63% |
| Conservative | **C: Balanced** | **270** | **62** | **44** | **86** | **$161.29** | **98.07%** |
| Conservative | D: Paid-Only | 254 | 52 | 34 | 76 | $192.31 | 89.39% |
| Moderate | A: Meta-Heavy | 196 | 41 | 27 | 61 | $243.90 | 71.10% |
| Moderate | B: High-Intent | 164 | 43 | 30 | 61 | $232.56 | 78.73% |
| Moderate | **C: Balanced** | **208** | **49** | **34** | **69** | **$204.08** | **89.21%** |
| Moderate | D: Paid-Only | 182 | 37 | 24 | 55 | $270.27 | 58.38% |
| High CPC | A: Meta-Heavy | 152 | 34 | 21 | 50 | $294.12 | 47.26% |
| High CPC | B: High-Intent | 129 | 35 | 23 | 50 | $285.71 | 51.50% |
| High CPC | **C: Balanced** | **159** | **39** | **26** | **55** | **$256.41** | **65.98%** |
| High CPC | D: Paid-Only | 126 | 26 | 16 | 39 | $384.62 | 18.04% |

*P10 and P90 represent the 10th and 90th percentiles of simulated monthly membership outcomes. CAC is calculated using the full $10,000 monthly marketing budget.*

## Cross-Environment Robustness

To evaluate which strategy performed most consistently, the model compared outcomes across all three CPC environments, weighting each environment equally.

| Strategy | Average Median Members | Worst-Case Median Members | Average Median CAC | Average P(35+ Members) |
|---|---:|---:|---:|---:|
| **C: Balanced** | **50.00** | **39** | **$207.26** | **84.42%** |
| B: High-Intent | 44.33 | 35 | $233.36 | 74.96% |
| A: Meta-Heavy | 41.67 | 34 | $246.01 | 68.70% |
| D: Paid-Only | 38.33 | 26 | $282.40 | 55.27% |

The **Balanced Omnichannel strategy ranked first across all three environments**, achieving the highest median membership acquisition, lowest median CAC, and strongest probability of reaching the monthly acquisition target.

These averages represent equally weighted scenario comparisons, not a probability-weighted forecast of actual market conditions.

## Key Findings

Under Moderate CPC conditions, the Balanced strategy generated a median of **49 new paying members at a $204.08 CAC**, compared with 37 members at $270.27 CAC for Paid-Only. This represents approximately **32% more members and a 24.5% reduction in median acquisition cost** using the same $10,000 budget. Balanced also maintained the highest probability of acquiring 35 or more members, reaching 89.21% in the Moderate environment.

Rising advertising costs substantially affected every strategy. Balanced declined from 62 median new members under Conservative CPC conditions to 39 under High CPC conditions. However, it remained the strongest performer, maintaining a **65.98% probability of acquiring at least 35 new members** even in the most expensive environment. Its 10th-percentile outcome under High CPC conditions was 26 members, illustrating that meaningful downside risk remains even for the winning strategy.

## Recommended Marketing Allocation

Based on the simulated results, the recommended $10,000 monthly allocation is:

| Channel | Monthly Budget | Allocation |
|---|---:|---:|
| Meta Ads | $3,500 | 35% |
| Google Search Ads | $3,000 | 30% |
| ChatGPT Ads | $2,000 | 20% |
| Organic / Local SEO | $1,500 | 15% |
| **Total** | **$10,000** | **100%** |

This allocation produced the strongest combination of acquisition volume, cost efficiency, and resilience among the four tested strategies.

## Why This Matters

The most compelling takeaway is the **speed and accessibility of AI-assisted statistical modeling**. With GPT-6 assisting in the development of the Python code, probabilistic assumptions, scenario design, and visualizations, the project evaluated **600,000 simulated marketing outcomes in approximately 11 seconds**. NumPy performed the underlying computations, allowing a complex marketing decision to be analyzed rapidly without external datasets.

Instead of relying on a single forecast or committing thousands of dollars based solely on intuition, businesses can use Monte Carlo simulations to compare strategies, quantify downside risk, and test how changing market conditions might affect performance. The results demonstrate how **AI-assisted development and statistical simulation can work together to make sophisticated business analysis faster and more accessible**.

The simulation uses synthetic assumptions, including hypothetical ChatGPT Ads performance and modeled NYC advertising saturation. Therefore, the findings should be interpreted as scenario-based decision support rather than validated predictions of real campaign performance.

**The goal isn't to predict the future perfectly — it's to understand the range of possible outcomes and make better-informed decisions before investing real money.**
