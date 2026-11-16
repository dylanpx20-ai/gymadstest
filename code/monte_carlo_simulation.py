
# ============================================================
# NYC BOUTIQUE GYM — MARKETING MONTE CARLO SIMULATION
# 4 Budget Strategies x 3 CPC Environments x 50,000 Runs
# Total: 600,000 Simulated Monthly Outcomes
# ============================================================

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

START = time.perf_counter()

# ------------------------------------------------------------
# 1. GLOBAL SETTINGS
# ------------------------------------------------------------

SEED = 42
N = 50_000
BUDGET = 10_000
ORGANIC_COST = 1500
TARGET_MEMBERS = 35

rng = np.random.default_rng(SEED)

sns.set_theme(style="whitegrid", context="notebook")

# ------------------------------------------------------------
# 2. THREE CPC MARKET ENVIRONMENTS
# ------------------------------------------------------------

# Values are illustrative NYC market assumptions.
# Each value is the arithmetic mean of a Log-Normal CPC.
# Standard deviations scale with the mean CPC.

CPC_ENVIRONMENTS = {
    "Conservative": {
        "Meta": 3.25,
        "Google": 9.00,
        "ChatGPT": 5.00,
    },
    "Moderate": {
        "Meta": 4.50,
        "Google": 12.00,
        "ChatGPT": 7.50,
    },
    "High CPC": {
        "Meta": 6.50,
        "Google": 17.00,
        "ChatGPT": 11.00,
    },
}

# Baseline CPC coefficients of variation
CPC_CV = {
    "Meta": 1.20 / 4.50,
    "Google": 3.50 / 12.00,
    "ChatGPT": 2.50 / 7.50,
}

# ------------------------------------------------------------
# 3. CHANNEL FUNNEL AND SATURATION ASSUMPTIONS
# ------------------------------------------------------------

CHANNELS = {
    "Meta": {
        "lead_cvr": 0.11,
        "close_rate": 0.15,
        "saturation_threshold": 4000,
        "saturation_strength": 0.65,
    },
    "Google": {
        "lead_cvr": 0.13,
        "close_rate": 0.30,
        "saturation_threshold": 3000,
        "saturation_strength": 1.00,
    },
    "ChatGPT": {
        "lead_cvr": 0.12,
        "close_rate": 0.27,
        "saturation_threshold": 2000,
        "saturation_strength": 1.20,
    },
}

LEAD_CONCENTRATION = 100
CLOSE_CONCENTRATION = 80

# ------------------------------------------------------------
# 4. MARKETING BUDGET STRATEGIES
# ------------------------------------------------------------

SCENARIOS = {
    "A: Meta-Heavy": {
        "Meta": 6500,
        "Google": 2000,
        "ChatGPT": 0,
        "Organic": 1500,
    },
    "B: High-Intent": {
        "Meta": 1500,
        "Google": 4500,
        "ChatGPT": 2500,
        "Organic": 1500,
    },
    "C: Balanced": {
        "Meta": 3500,
        "Google": 3000,
        "ChatGPT": 2000,
        "Organic": 1500,
    },
    "D: Paid-Only": {
        "Meta": 4500,
        "Google": 3500,
        "ChatGPT": 2000,
        "Organic": 0,
    },
}

for name, allocation in SCENARIOS.items():
    assert sum(allocation.values()) == BUDGET, name
    assert allocation["Organic"] in (0, ORGANIC_COST)

# ------------------------------------------------------------
# 5. STATISTICAL SAMPLING FUNCTIONS
# ------------------------------------------------------------

def sample_lognormal(mean, cv, size):
    """Sample positive CPC values from a Log-Normal."""
    sigma2 = np.log1p(cv ** 2)
    sigma = np.sqrt(sigma2)
    mu = np.log(mean) - sigma2 / 2
    return rng.lognormal(mu, sigma, size)


def sample_beta(mean, concentration, size):
    """Sample conversion probabilities from a Beta."""
    alpha = mean * concentration
    beta = (1 - mean) * concentration
    return rng.beta(alpha, beta, size)


def saturation_multiplier(spend, threshold, strength):
    """
    Nonlinear CPC inflation above local inventory threshold.

    A 1-mile NYC audience cannot scale indefinitely at
    constant efficiency.

    The multiplier increases with spend above threshold.
    """
    excess_ratio = max(0, spend - threshold) / threshold
    return 1 + strength * excess_ratio ** 1.5


# ------------------------------------------------------------
# 6. SIMULATE PAID CHANNEL
# ------------------------------------------------------------

def simulate_paid(channel, spend, environment, n):

    if spend == 0:
        z = np.zeros(n, dtype=np.int32)
        return z, z.copy()

    p = CHANNELS[channel]

    mean_cpc = CPC_ENVIRONMENTS[environment][channel]
    cv = CPC_CV[channel]

    cpc = sample_lognormal(mean_cpc, cv, n)

    inflation = saturation_multiplier(
        spend,
        p["saturation_threshold"],
        p["saturation_strength"],
    )

    effective_cpc = cpc * inflation

    expected_clicks = spend / effective_cpc
    clicks = rng.poisson(expected_clicks)

    lead_prob = sample_beta(
        p["lead_cvr"],
        LEAD_CONCENTRATION,
        n,
    )

    close_prob = sample_beta(
        p["close_rate"],
        CLOSE_CONCENTRATION,
        n,
    )

    leads = rng.binomial(clicks, lead_prob)
    members = rng.binomial(leads, close_prob)

    return leads, members


# ------------------------------------------------------------
# 7. SIMULATE ORGANIC / LOCAL SEO
# ------------------------------------------------------------

def simulate_organic(spend, n):

    if spend == 0:
        z = np.zeros(n, dtype=np.int32)
        return z, z.copy()

    visits = rng.integers(300, 701, n)

    lead_prob = sample_beta(0.10, LEAD_CONCENTRATION, n)
    close_prob = sample_beta(0.33, CLOSE_CONCENTRATION, n)

    leads = rng.binomial(visits, lead_prob)
    members = rng.binomial(leads, close_prob)

    return leads, members


# ------------------------------------------------------------
# 8. RUN ALL 600,000 SIMULATIONS
# ------------------------------------------------------------

results = {}
summary_rows = []
channel_rows = []

for environment in CPC_ENVIRONMENTS:

    for scenario, allocation in SCENARIOS.items():

        total_leads = np.zeros(N, dtype=np.int32)
        total_members = np.zeros(N, dtype=np.int32)

        channel_members = {}

        for channel in CHANNELS:

            leads, members = simulate_paid(
                channel,
                allocation[channel],
                environment,
                N,
            )

            total_leads += leads
            total_members += members
            channel_members[channel] = members

        organic_leads, organic_members = simulate_organic(
            allocation["Organic"], N
        )

        total_leads += organic_leads
        total_members += organic_members
        channel_members["Organic"] = organic_members

        # Undefined CAC for zero-member outcomes.
        cac = np.divide(
            BUDGET,
            total_members.astype(float),
            out=np.full(N, np.nan),
            where=total_members > 0,
        )

        results[(environment, scenario)] = {
            "leads": total_leads,
            "members": total_members,
            "cac": cac,
        }

        summary_rows.append({
            "CPC Environment": environment,
            "Scenario": scenario,
            "Median Total Leads": np.median(total_leads),
            "Median New Members": np.median(total_members),
            "P10 New Members": np.percentile(total_members, 10),
            "P90 New Members": np.percentile(total_members, 90),
            "Median CAC ($)": np.nanmedian(cac),
            "Probability 35+ (%)":
                100 * np.mean(total_members >= TARGET_MEMBERS),
            "Zero-Member Risk (%)":
                100 * np.mean(total_members == 0),
        })

        for channel, members in channel_members.items():
            channel_rows.append({
                "CPC Environment": environment,
                "Scenario": scenario,
                "Channel": channel,
                "Spend ($)": allocation[channel],
                "Mean Members": np.mean(members),
                "Median Members": np.median(members),
            })

summary = pd.DataFrame(summary_rows)
channel_summary = pd.DataFrame(channel_rows)

env_order = list(CPC_ENVIRONMENTS)
scenario_order = list(SCENARIOS)

summary["CPC Environment"] = pd.Categorical(
    summary["CPC Environment"],
    categories=env_order,
    ordered=True,
)

summary["Scenario"] = pd.Categorical(
    summary["Scenario"],
    categories=scenario_order,
    ordered=True,
)

summary = summary.sort_values(
    ["CPC Environment", "Scenario"]
).reset_index(drop=True)

print("\n" + "=" * 90)
print("NYC BOUTIQUE GYM — 600,000 MONTE CARLO OUTCOMES")
print("=" * 90)

print(
    summary.to_string(
        index=False,
        float_format=lambda x: f"{x:,.2f}",
    )
)

# ------------------------------------------------------------
# 9. PREPARE HEATMAP DATA
# ------------------------------------------------------------

members_heatmap = summary.pivot(
    index="Scenario",
    columns="CPC Environment",
    values="Median New Members",
).reindex(index=scenario_order, columns=env_order)

cac_heatmap = summary.pivot(
    index="Scenario",
    columns="CPC Environment",
    values="Median CAC ($)",
).reindex(index=scenario_order, columns=env_order)

# ------------------------------------------------------------
# 10. VISUALIZATION 1 — MEMBERSHIP KDE
# ------------------------------------------------------------

palette = {
    "A: Meta-Heavy": "#E76F51",
    "B: High-Intent": "#457B9D",
    "C: Balanced": "#2A9D8F",
    "D: Paid-Only": "#9B5DE5",
}

fig1, axes = plt.subplots(
    1, 3, figsize=(19, 5.5),
    constrained_layout=True,
)

for ax, environment in zip(axes, env_order):

    for scenario in scenario_order:

        members = results[(environment, scenario)]["members"]

        # Sampling only affects KDE rendering speed.
        sample = rng.choice(
            members,
            size=min(3000, len(members)),
            replace=False,
        )

        sns.kdeplot(
            x=sample,
            ax=ax,
            label=scenario,
            color=palette[scenario],
            linewidth=2.2,
            cut=0,
            bw_adjust=1.1,
        )

    ax.axvline(
        TARGET_MEMBERS,
        color="black",
        linestyle="--",
        alpha=0.65,
        label="35-member target",
    )

    ax.set_title(environment, fontweight="bold")
    ax.set_xlabel("New Paying Members / Month")
    ax.set_ylabel("Probability Density")
    ax.grid(alpha=0.2)

axes[0].legend(fontsize=8)

fig1.suptitle(
    "Membership Acquisition Distributions by CPC Environment",
    fontsize=16,
    fontweight="bold",
)

fig1.savefig(
    "01_membership_distributions.png",
    dpi=180,
    bbox_inches="tight",
)

plt.show()

# ------------------------------------------------------------
# 11. VISUALIZATION 2 — CAC BOXPLOTS
# ------------------------------------------------------------

cac_plot_rows = []

for environment in env_order:
    for scenario in scenario_order:

        values = results[(environment, scenario)]["cac"]
        values = values[np.isfinite(values)]

        sample = rng.choice(
            values,
            size=min(2500, len(values)),
            replace=False,
        )

        cac_plot_rows.append(
            pd.DataFrame({
                "Environment": environment,
                "Scenario": scenario,
                "CAC": sample,
            })
        )

cac_plot = pd.concat(cac_plot_rows, ignore_index=True)

fig2, axes = plt.subplots(
    1, 3, figsize=(19, 5.5),
    constrained_layout=True,
)

for ax, environment in zip(axes, env_order):

    subset = cac_plot[
        cac_plot["Environment"] == environment
    ]

    sns.boxplot(
        data=subset,
        x="Scenario",
        y="CAC",
        order=scenario_order,
        hue="Scenario",
        palette=palette,
        legend=False,
        showfliers=False,
        ax=ax,
    )

    ax.set_title(environment, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Blended CAC ($)")
    ax.tick_params(axis="x", rotation=25)
    ax.grid(axis="y", alpha=0.2)

fig2.suptitle(
    "Customer Acquisition Cost by CPC Environment",
    fontsize=16,
    fontweight="bold",
)

fig2.savefig(
    "02_cac_boxplots.png",
    dpi=180,
    bbox_inches="tight",
)

plt.show()

# ------------------------------------------------------------
# 12. VISUALIZATION 3 — MEMBERSHIP HEATMAP
# ------------------------------------------------------------

fig3, ax = plt.subplots(figsize=(10, 5.5))

sns.heatmap(
    members_heatmap,
    annot=True,
    fmt=".0f",
    cmap="YlGnBu",
    linewidths=0.8,
    cbar_kws={"label": "Median New Members"},
    ax=ax,
)

ax.set_title(
    "Median Monthly New Members — Strategy vs. CPC",
    fontsize=15,
    fontweight="bold",
    pad=16,
)

ax.set_xlabel("CPC Environment")
ax.set_ylabel("Budget Strategy")
ax.tick_params(axis="y", rotation=0)

fig3.tight_layout()

fig3.savefig(
    "03_membership_heatmap.png",
    dpi=180,
    bbox_inches="tight",
)

plt.show()

# ------------------------------------------------------------
# 13. VISUALIZATION 4 — CAC HEATMAP
# ------------------------------------------------------------

fig4, ax = plt.subplots(figsize=(10, 5.5))

sns.heatmap(
    cac_heatmap,
    annot=True,
    fmt=".0f",
    cmap="YlOrRd",
    linewidths=0.8,
    cbar_kws={"label": "Median Blended CAC ($)"},
    ax=ax,
)

ax.set_title(
    "Median Customer Acquisition Cost — Strategy vs. CPC",
    fontsize=15,
    fontweight="bold",
    pad=16,
)

ax.set_xlabel("CPC Environment")
ax.set_ylabel("Budget Strategy")
ax.tick_params(axis="y", rotation=0)

fig4.tight_layout()

fig4.savefig(
    "04_cac_heatmap.png",
    dpi=180,
    bbox_inches="tight",
)

plt.show()

# ------------------------------------------------------------
# 14. STRATEGY RANKINGS BY CPC ENVIRONMENT
# ------------------------------------------------------------

print("\n" + "=" * 90)
print("WINNING STRATEGY BY CPC ENVIRONMENT")
print("=" * 90)

winners = []

for environment in env_order:

    subset = summary[
        summary["CPC Environment"] == environment
    ].copy()

    subset = subset.sort_values(
        ["Median New Members", "Median CAC ($)",
         "Probability 35+ (%)"],
        ascending=[False, True, False],
    )

    winner = subset.iloc[0]

    winners.append({
        "Environment": environment,
        "Winning Strategy": str(winner["Scenario"]),
        "Median Members": winner["Median New Members"],
        "Median CAC ($)": winner["Median CAC ($)"],
        "Probability 35+ (%)":
            winner["Probability 35+ (%)"],
    })

    print(f"\n{environment.upper()}")
    print(f"Best Strategy: {winner['Scenario']}")
    print(
        f"Median Members: "
        f"{winner['Median New Members']:.0f}"
    )
    print(
        f"Median CAC: "
        f"${winner['Median CAC ($)']:,.2f}"
    )
    print(
        f"Probability of 35+ Members: "
        f"{winner['Probability 35+ (%)']:.1f}%"
    )

winners_df = pd.DataFrame(winners)

# ------------------------------------------------------------
# 15. ROBUSTNESS ANALYSIS
# ------------------------------------------------------------

# Compare strategies on equally weighted CPC environments.
# Equal weighting is a planning assumption, not a forecast.

robustness = (
    summary.groupby("Scenario", observed=True)
    .agg(
        Average_Median_Members=("Median New Members", "mean"),
        Worst_Case_Median_Members=("Median New Members", "min"),
        Average_Median_CAC=("Median CAC ($)", "mean"),
        Average_Target_Probability=("Probability 35+ (%)", "mean"),
    )
    .sort_values(
        ["Average_Median_Members", "Average_Median_CAC"],
        ascending=[False, True],
    )
)

print("\n" + "=" * 90)
print("CROSS-ENVIRONMENT ROBUSTNESS RANKING")
print("=" * 90)

print(robustness.round(2).to_string())

robust_winner = robustness.index[0]

print(f"\nMost Robust Strategy: {robust_winner}")

print("\nRecommended Allocation:")
for channel, spend in SCENARIOS[robust_winner].items():
    print(f"  {channel:<12}: ${spend:,}")

# ------------------------------------------------------------
# 16. EXPORT ALL RESULTS
# ------------------------------------------------------------

summary.to_csv(
    "nyc_gym_scenario_summary.csv",
    index=False,
)

channel_summary.to_csv(
    "nyc_gym_channel_results.csv",
    index=False,
)

winners_df.to_csv(
    "nyc_gym_environment_winners.csv",
    index=False,
)

robustness.to_csv(
    "nyc_gym_robustness_ranking.csv",
)

print("\n" + "=" * 90)
print("GITHUB-READY FILES GENERATED")
print("=" * 90)

files = [
    "nyc_gym_scenario_summary.csv",
    "nyc_gym_channel_results.csv",
    "nyc_gym_environment_winners.csv",
    "nyc_gym_robustness_ranking.csv",
    "01_membership_distributions.png",
    "02_cac_boxplots.png",
    "03_membership_heatmap.png",
    "04_cac_heatmap.png",
]

for file in files:
    print(" -", file)

elapsed = time.perf_counter() - START

print(f"\nExecution Time: {elapsed:.2f} seconds")
print("Simulation Complete.")
