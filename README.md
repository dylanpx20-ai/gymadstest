# Gym Ads Test
Monte Carlo simulation of 600,000 marketing outcomes comparing Meta, Google Search, ChatGPT Ads, and Local SEO across three NYC CPC environments to optimize gym membership acquisition, CAC, and a $10K monthly budget.
# NYC Gym Marketing Budget Optimization — AI-Assisted Monte Carlo Simulation

A Python data science project demonstrating how AI-assisted Monte Carlo simulations can rapidly model thousands of potential business outcomes, evaluate marketing budget strategies, and support data-driven decisions under uncertainty.

This project simulates **600,000 possible monthly marketing outcomes** for a boutique gym in New York City, comparing customer acquisition performance across four budget allocation strategies and three advertising cost environments.

---

## What This Project Does

A boutique gym in a competitive NYC neighborhood has a fixed **$10,000 monthly marketing budget** to allocate across four acquisition channels:

- Meta Ads (Instagram / Facebook)
- Google Search Ads
- ChatGPT Ads
- Organic / Local SEO

The business question is simple:

**How should a small business allocate its marketing budget to maximize new paying customers while minimizing Customer Acquisition Cost (CAC)?**

Rather than relying on a single forecast, this project uses Monte Carlo simulation to evaluate thousands of possible outcomes under different advertising costs, conversion rates, and local market constraints.

Using AI-assisted Python development, the model runs 50,000 simulations for each of 12 strategy-environment combinations.

The full analysis completed in approximately **11.49 seconds in Google Colab**, demonstrating how computational simulation can support rapid business scenario analysis.

---

## Channels & Assumptions

The model uses synthetic but plausible assumptions for a competitive NYC neighborhood.

| Channel | Moderate CPC | Click-to-Lead CVR | Lead-to-Member Close Rate | Saturation Threshold |
|---|---:|---:|---:|---:|
| Meta Ads | $4.50 | 11% | 15% | $4,000 |
| Google Search | $12.00 | 13% | 30% | $3,000 |
| ChatGPT Ads | $7.50 | 12% | 27% | $2,000 |
| Organic / Local SEO | Fixed $1,500 | 10% | 33% | N/A |

Organic SEO generates a simulated pool of 300–700 monthly local visits when active.

The simulation incorporates several sources of uncertainty:

- **Log-Normal distributions** model CPC volatility while preventing negative advertising costs.
- **Beta distributions** model variation in lead conversion and membership close rates.
- **Poisson distributions** model fluctuations in paid website traffic.
- **Binomial distributions** model lead generation and paying member acquisition.
- **Nonlinear saturation penalties** increase effective CPC when spending exceeds local inventory thresholds.

The saturation model reflects the practical limitation that a small geographic audience cannot absorb unlimited advertising spend at constant efficiency.

All assumptions are illustrative and should be calibrated against actual campaign data before operational use.

---

## Budget Allocation Strategies

Four distinct monthly marketing strategies are evaluated.

| Channel | A: Meta-Heavy | B: High-Intent | C: Balanced | D: Paid-Only |
|---|---:|---:|---:|---:|
| Meta Ads | $6,500 | $1,500 | $3,500 | $4,500 |
| Google Search | $2,000 | $4,500 | $3,000 | $3,500 |
| ChatGPT Ads | $0 | $2,500 | $2,000 | $2,000 |
| Organic / SEO | $1,500 | $1,500 | $1,500 | $0 |
| **Total** | **$10,000** | **$10,000** | **$10,000** | **$10,000** |

Each strategy represents a different marketing philosophy.

| Strategy | Philosophy |
|---|---|
| A: Meta-Heavy | Prioritize social advertising and lead volume |
| B: High-Intent | Concentrate spending on search and conversational discovery |
| C: Balanced | Diversify acquisition across paid and organic channels |
| D: Paid-Only | Maximize paid advertising exposure without organic investment |

---

## CPC Market Environments

To evaluate performance under changing market conditions, the simulation tests three advertising cost environments.

| Channel | Conservative | Moderate | High CPC |
|---|---:|---:|---:|
| Meta Ads | $3.25 | $4.50 | $6.50 |
| Google Search | $9.00 | $12.00 | $17.00 |
| ChatGPT Ads | $5.00 | $7.50 | $11.00 |

These values represent the mean CPC assumptions used by the model.

| Environment | Interpretation |
|---|---|
| Conservative | Lower advertising costs and more efficient customer acquisition |
| Moderate | Baseline competitive NYC advertising conditions |
| High CPC | Increased competition, higher acquisition costs, and tighter marketing efficiency |

Each of the four strategies is tested in all three environments.

**4 strategies × 3 CPC environments × 50,000 iterations = 600,000 simulated monthly outcomes.**

---

## How AI & Monte Carlo Simulation Fit In

The central purpose of this project is to demonstrate how AI-assisted programming and statistical simulation can accelerate marketing decision analysis.

AI was used to assist with the development and organization of the Python simulation, including probabilistic modeling, scenario testing, statistical summaries, and visualizations.

NumPy performs the actual Monte Carlo calculations using vectorized numerical operations.

The workflow follows five steps:

1. **Define the business problem:** Optimize a fixed monthly marketing budget.
2. **Build probabilistic assumptions:** Model CPCs, conversion rates, and traffic as uncertain variables.
3. **Simulate possible outcomes:** Generate 50,000 monthly results per strategy-environment combination.
4. **Evaluate performance and risk:** Compare median memberships, CAC, downside outcomes, and target attainment.
5. **Translate results into decisions:** Identify allocations that perform consistently across market conditions.

Unlike a deterministic spreadsheet forecast, Monte Carlo simulation produces distributions of possible outcomes rather than a single predicted result.

This makes it possible to examine not only which strategy performs best, but also how reliably it performs under uncertainty.

**AI accelerates model development; Monte Carlo simulation quantifies uncertainty; business judgment interprets the results.**

---

## Key Results

The **Balanced Omnichannel strategy (Scenario C)** produced the strongest performance across all three CPC environments.

### Median New Paying Members

| Strategy | Conservative | Moderate | High CPC |
|---|---:|---:|---:|
| A: Meta-Heavy | 50 | 41 | 34 |
| B: High-Intent | 55 | 43 | 35 |
| **C: Balanced** | **62** | **49** | **39** |
| D: Paid-Only | 52 | 37 | 26 |

### Median Customer Acquisition Cost

| Strategy | Conservative | Moderate | High CPC |
|---|---:|---:|---:|
| A: Meta-Heavy | $200.00 | $243.90 | $294.12 |
| B: High-Intent | $181.82 | $232.56 | $285.71 |
| **C: Balanced** | **$161.29** | **$204.08** | **$256.41** |
| D: Paid-Only | $192.31 | $270.27 | $384.62 |

### Key Findings

- **Balanced wins in every CPC environment**, producing the highest median membership acquisition and lowest median CAC among the four tested strategies.
- In the Moderate environment, Balanced generates **49 median new members**, compared with 37 for Paid-Only — approximately 32% more.
- Balanced reduces median CAC by approximately **24.5%** compared with Paid-Only under Moderate CPC conditions.
- Under High CPC conditions, Balanced maintains a **65.98% probability of acquiring at least 35 new members**, compared with 18.04% for Paid-Only.
- Rising advertising costs reduce Balanced's median membership acquisition from 62 to 39, demonstrating the importance of evaluating downside risk.
- Organic/Local SEO contributes to the stronger performance of the diversified strategy under the model's assumptions.

The Balanced strategy also achieves the strongest cross-environment robustness ranking, averaging 50 median members and $207.26 median CAC across the three equally weighted CPC environments.

These cross-environment averages are descriptive comparisons, not probability-weighted forecasts of actual NYC market conditions.

See `RESULTS.md` for the complete analysis and business interpretation.

---

## Visualizations

Four visualizations illustrate the simulation's results.

### 1. Membership Acquisition Distributions

![Membership Acquisition Distributions](results/01_membership_distributions.png)

Overlapping probability density curves compare monthly membership acquisition across the four strategies under each CPC environment.

### 2. Customer Acquisition Cost Distributions

![Customer Acquisition Cost Distributions](results/02_cac_boxplots.png)

Boxplots illustrate the median, variability, and distribution of blended CAC across the simulated marketing strategies.

### 3. Median Membership Acquisition Heatmap

![Membership Heatmap](results/03_membership_heatmap.png)

A heatmap compares median monthly new members across all 12 strategy-environment combinations.

### 4. Median CAC Heatmap

![CAC Heatmap](results/04_cac_heatmap.png)

A heatmap highlights how acquisition costs change across budget allocations and advertising cost environments.

---

## Business Recommendation

Based on the simulated results, the recommended monthly allocation is:

| Marketing Channel | Monthly Budget | Allocation |
|---|---:|---:|
| Meta Ads | $3,500 | 35% |
| Google Search | $3,000 | 30% |
| ChatGPT Ads | $2,000 | 20% |
| Organic / Local SEO | $1,500 | 15% |
| **Total** | **$10,000** | **100%** |

This allocation offers the strongest modeled combination of membership growth, acquisition efficiency, and resilience to rising advertising costs.

The recommendation applies to the four tested strategies under the specified assumptions. It does not establish a globally optimal budget allocation.

Actual campaign data, local demand, member lifetime value, and operational capacity should be incorporated before making a real-world investment decision.

---

## How to Run

The simulation can be executed directly in Google Colab or locally using Python 3.

1. Open Google Colab or a Python environment.
2. Open the simulation script, `monte_carlo_simulation.py`.
3. Run the complete script.
4. Review the printed summary tables and strategy rankings.
5. Examine the four generated visualizations and exported CSV results.

The script requires no external datasets or CSV inputs.

Dependencies:

- `numpy`
- `pandas`
- `matplotlib`
- `seaborn`

The simulation uses a fixed random seed (`42`) for reproducibility.

### Generated Outputs

The script produces four PNG visualizations and four CSV result tables:

- `01_membership_distributions.png`
- `02_cac_boxplots.png`
- `03_membership_heatmap.png`
- `04_cac_heatmap.png`
- `nyc_gym_scenario_summary.csv`
- `nyc_gym_channel_results.csv`
- `nyc_gym_environment_winners.csv`
- `nyc_gym_robustness_ranking.csv`

---

## Tech Stack

| Tool | Role |
|---|---|
| Python 3 | Core programming language |
| NumPy | Vectorized Monte Carlo simulation and random sampling |
| pandas | Data aggregation, scenario comparisons, and CSV exports |
| Matplotlib | Statistical visualization and figure exports |
| Seaborn | KDE distributions, boxplots, and heatmaps |
| Google Colab | Development and execution environment |
| ChatGPT | AI-assisted simulation development and analytical workflow |

---

## Limitations

This is a synthetic scenario analysis, not a model trained on observed NYC gym advertising data.

The model assumes:

- CPC and conversion parameters are representative planning inputs.
- Local advertising saturation follows a predefined nonlinear penalty.
- Organic SEO has an established monthly traffic baseline.
- Acquisition from different channels is additive without cross-channel attribution overlap.
- All $10,000 of allocated marketing budget is included in blended CAC.
- Customer retention, lifetime value, staffing costs, and gym capacity are outside the model's scope.

ChatGPT Ads assumptions are hypothetical and are not presented as verified advertising benchmarks.

The simulation estimates outcomes conditional on these assumptions. It does not validate the assumptions themselves or guarantee future performance.

---

## Project Takeaway

This project demonstrates how **AI-assisted Monte Carlo simulation can turn a marketing budget question into a repeatable, quantitative decision-making framework**.

By simulating 600,000 possible monthly outcomes in approximately 11.49 seconds, the analysis shows how businesses can rapidly compare strategies, quantify downside risk, evaluate acquisition costs, and explore changing market conditions.

The broader lesson is that the value of simulation is not predicting one exact future outcome.

**It is understanding the range of possible outcomes before making a decision.**
