"""
Swiss OKP Risk Equalization Simulation
=======================================
Simulates the Swiss mandatory health insurance market under three phases of
the Risikoausgleich (RA) formula to illustrate the model in paper/03_economic_model.md.

Phases:
  Phase 1 (1996-2011): age + sex cells only
  Phase 2 (2012-2019): age + sex + prior hospital admission
  Phase 3 (2020-):     age + sex + prior hospital + PCG groups (22 groups)

Outputs:
  output/figures/f01_loss_ratio_distribution.png
  output/figures/f02_solvency_gap_by_phase.png
  output/figures/f03_sensitivity_adverse_selection.png
  output/figures/f04_combined_ratio_distribution.png
  output/figures/f05_combined_ratio_decomposition.png
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import os

# ── reproducibility ──────────────────────────────────────────────────────────
RNG = np.random.default_rng(42)

# ── output directory ─────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "output", "figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 1. POPULATION GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_population(n: int = 10_000) -> pd.DataFrame:
    """
    Draw a synthetic Swiss-like insured population.

    Age distribution is calibrated to the 2022 Swiss resident population
    (approx. shares by decade). PCG prevalence and hospitalization rates
    are calibrated to Swiss BAG statistics.
    """
    age_group_probs = [0.16, 0.09, 0.52, 0.23]
    age_group = RNG.choice([0, 1, 2, 3], size=n, p=age_group_probs)
    sex = RNG.integers(0, 2, size=n)

    hosp_prob_by_age = {0: 0.05, 1: 0.06, 2: 0.10, 3: 0.25}
    hosp = np.array([RNG.binomial(1, hosp_prob_by_age[a]) for a in age_group])

    pcg_prevalence = np.concatenate([
        RNG.uniform(0.03, 0.07, size=7),
        RNG.uniform(0.005, 0.02, size=15)
    ])
    pcg = np.zeros((n, 22), dtype=int)
    for m in range(22):
        base_prob = pcg_prevalence[m]
        age_multiplier = np.array([0.2, 0.3, 0.8, 2.5])[age_group]
        hosp_multiplier = 1 + 1.5 * hosp
        prob = np.clip(base_prob * age_multiplier * hosp_multiplier, 0, 0.95)
        pcg[:, m] = RNG.binomial(1, prob)

    pop = pd.DataFrame({"age_group": age_group, "sex": sex, "hosp": hosp})
    for m in range(22):
        pop[f"pcg_{m}"] = pcg[:, m]
    return pop


# ═══════════════════════════════════════════════════════════════════════════════
# 2. COST MODEL
# ═══════════════════════════════════════════════════════════════════════════════

BASE_COST = 3_800.0

BETA_AGE = {0: 1_200 - BASE_COST,
            1: 1_800 - BASE_COST,
            2: 0.0,
            3: 9_000 - BASE_COST}

BETA_SEX    = 200.0
BETA_HOSP   = 12_000.0

PCG_COST_EFFECTS = np.array([
    6_000, 5_500, 4_800, 4_200, 3_800, 3_500, 3_200,
    8_000, 9_500, 12_000, 15_000,
    2_500, 2_200, 2_000, 1_800, 1_600, 1_500, 1_400,
    1_200, 1_100, 1_000, 900
])

SIGMA_EPSILON = 5_500.0

# ── expense parameters (calibrated to Swiss BAG administrative cost data) ─────
# Fixed component: member services, IT, reserve management, regulatory compliance
ADMIN_FIXED_PER_ENROLLEE = 280.0   # CHF/year per enrollee, independent of risk

# Variable component: claims adjudication, authorisation, quality review
# Scales with realized claims volume; captures the higher processing burden
# of complex, high-cost cases (e.g. PCG patients, post-hospitalisation care).
ADMIN_VARIABLE_RATE = 0.02         # 2% of realized claims

# Premium is set to cover expected claims PLUS expected admin (community rating
# means the loading is the same proportion for all enrollees).
# At system averages: admin = 280 + 0.02 * 4800 = 376 CHF/year ≈ 7.3% loading.
ADMIN_RATE = (ADMIN_FIXED_PER_ENROLLEE + ADMIN_VARIABLE_RATE * BASE_COST) / BASE_COST


def compute_true_cost(pop: pd.DataFrame):
    n = len(pop)
    expected = np.full(n, BASE_COST)
    for ag, beta_ag in BETA_AGE.items():
        expected += (pop["age_group"] == ag).values * beta_ag
    expected += pop["sex"].values * BETA_SEX
    expected += pop["hosp"].values * BETA_HOSP
    for m in range(22):
        expected += pop[f"pcg_{m}"].values * PCG_COST_EFFECTS[m]

    log_sigma = np.log(1 + (SIGMA_EPSILON / expected) ** 2) ** 0.5
    log_mu = -0.5 * log_sigma ** 2
    noise_multiplier = RNG.lognormal(log_mu, log_sigma, size=n)
    realized = np.maximum(expected * noise_multiplier, 0)
    return expected, realized


# ═══════════════════════════════════════════════════════════════════════════════
# 3. RISK ADJUSTMENT PREDICTION
# ═══════════════════════════════════════════════════════════════════════════════

def predict_cost_phase1(pop, realized):
    predicted = np.zeros(len(pop))
    for ag in range(4):
        for sx in range(2):
            mask = (pop["age_group"] == ag) & (pop["sex"] == sx)
            if mask.sum() > 0:
                predicted[mask] = realized[mask].mean()
    return predicted


def predict_cost_phase2(pop, realized):
    predicted = np.zeros(len(pop))
    for ag in range(4):
        for sx in range(2):
            for h in range(2):
                mask = (pop["age_group"] == ag) & (pop["sex"] == sx) & (pop["hosp"] == h)
                if mask.sum() > 0:
                    predicted[mask] = realized[mask].mean()
    return predicted


def predict_cost_phase3(pop, realized):
    feature_cols = ["age_group", "sex", "hosp"] + [f"pcg_{m}" for m in range(22)]
    X = pop[feature_cols].copy()
    X = pd.get_dummies(X, columns=["age_group"], drop_first=False).astype(float)
    X.insert(0, "const", 1.0)
    X_mat = X.values
    beta, _, _, _ = np.linalg.lstsq(X_mat, realized, rcond=None)
    return np.maximum(X_mat @ beta, 0)


# ═══════════════════════════════════════════════════════════════════════════════
# 4. INSURER ENROLLMENT (WITH OPTIONAL ADVERSE SELECTION)
# ═══════════════════════════════════════════════════════════════════════════════

def assign_to_insurers(pop, expected_cost, k=10, adverse_selection_strength=0.0):
    n = len(pop)
    if adverse_selection_strength == 0:
        return RNG.integers(0, k, size=n)
    rank = stats.rankdata(expected_cost) / n
    sort_score = (1 - adverse_selection_strength) * RNG.uniform(0, 1, n) + \
                 adverse_selection_strength * rank
    assignment = np.digitize(sort_score, bins=np.linspace(0, 1, k + 1)[1:-1])
    return assignment.astype(int)


# ═══════════════════════════════════════════════════════════════════════════════
# 5. LOSS RATIO, EXPENSE RATIO, AND COMBINED RATIO
# ═══════════════════════════════════════════════════════════════════════════════

def compute_ratios(pop, realized_cost, predicted_cost, assignment, k=10):
    """
    For each insurer j compute:
      - LR*  : loss ratio after Risikoausgleich  = claims / RA-adjusted revenue
      - ER*  : expense ratio after RA            = admin costs / RA-adjusted revenue
      - CR*  : combined ratio after RA           = LR* + ER*

    The premium is loaded to cover both expected claims and expected admin
    (community rating: same loading for everyone). The RA transfer is applied
    only to the claims-coverage part of revenue; admin revenue is proportional
    to pool size regardless of risk composition.

    Expense structure:
      admin_j = ADMIN_FIXED_PER_ENROLLEE * N_j        (fixed: does not vary with risk)
              + ADMIN_VARIABLE_RATE       * C_j        (variable: scales with claims)
    """
    system_avg_cost      = realized_cost.mean()
    system_avg_predicted = predicted_cost.mean()

    # Premium covers expected claims + expected admin loading
    premium = system_avg_cost * (1 + ADMIN_RATE)

    results = []
    for j in range(k):
        mask = assignment == j
        n_j = mask.sum()
        if n_j == 0:
            continue

        c_j     = realized_cost[mask].sum()    # total realized claims
        pred_j  = predicted_cost[mask].sum()   # total predicted claims (RA base)

        # Revenue: flat premium × pool size (community rating)
        revenue_j = n_j * premium

        # RA transfer on the claims side only
        ra_transfer = pred_j - n_j * system_avg_predicted
        revenue_adj = revenue_j + ra_transfer   # RA-adjusted revenue

        # Admin costs
        admin_j = ADMIN_FIXED_PER_ENROLLEE * n_j + ADMIN_VARIABLE_RATE * c_j

        # Ratios
        lr = c_j     / revenue_adj if revenue_adj > 0 else np.nan
        er = admin_j / revenue_adj if revenue_adj > 0 else np.nan
        cr = lr + er

        results.append({
            "insurer":                 j,
            "n_enrollees":             n_j,
            "avg_realized_cost":       c_j / n_j,
            "avg_predicted_cost":      pred_j / n_j,
            "ra_transfer_per_capita":  ra_transfer / n_j,
            "lr":                      lr,
            "er":                      er,
            "cr":                      cr,
        })

    return pd.DataFrame(results)


# ═══════════════════════════════════════════════════════════════════════════════
# 6. FULL SIMULATION RUN
# ═══════════════════════════════════════════════════════════════════════════════

def run_simulation(n=10_000, k=10, adverse_selection_strength=0.5, n_sim=200):
    """
    Run n_sim Monte Carlo replications.
    Returns dict {phase: {"lr": (n_sim, k), "er": (n_sim, k), "cr": (n_sim, k)}}.
    """
    store = {phase: {"lr": [], "er": [], "cr": []} for phase in ["no_ra", 1, 2, 3]}

    def pad(arr, length):
        padded = np.full(length, np.nan)
        padded[:len(arr)] = arr
        return padded

    for _ in range(n_sim):
        pop = generate_population(n)
        expected_cost, realized_cost = compute_true_cost(pop)
        assignment = assign_to_insurers(pop, expected_cost, k, adverse_selection_strength)

        pred_p1   = predict_cost_phase1(pop, realized_cost)
        pred_p2   = predict_cost_phase2(pop, realized_cost)
        pred_p3   = predict_cost_phase3(pop, realized_cost)
        pred_none = np.full(n, realized_cost.mean())   # no RA: flat prediction

        for phase, pred in [("no_ra", pred_none), (1, pred_p1), (2, pred_p2), (3, pred_p3)]:
            df = compute_ratios(pop, realized_cost, pred, assignment, k)
            store[phase]["lr"].append(pad(df["lr"].values, k))
            store[phase]["er"].append(pad(df["er"].values, k))
            store[phase]["cr"].append(pad(df["cr"].values, k))

    return {
        phase: {metric: np.array(vals) for metric, vals in metrics.items()}
        for phase, metrics in store.items()
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 7. FIGURES
# ═══════════════════════════════════════════════════════════════════════════════

PHASE_LABELS = {
    "no_ra": "No RA",
    1: "Phase 1 (age/sex)",
    2: "Phase 2 (+hospital)",
    3: "Phase 3 (+PCG)",
}
PHASE_COLORS = {
    "no_ra": "#d62728",
    1: "#ff7f0e",
    2: "#1f77b4",
    3: "#2ca02c",
}


def _flat(results, phase, metric, clip_center=1.0, clip_radius=1.0):
    """Flatten, remove NaN, and clip outliers for a given phase/metric."""
    arr = results[phase][metric].flatten()
    arr = arr[~np.isnan(arr)]
    arr = arr[np.abs(arr - clip_center) < clip_radius]
    return arr


def figure_loss_ratio_distribution(results, output_path):
    """Figure 1: Distribution of loss ratios by phase."""
    phases = ["no_ra", 1, 2, 3]
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    axes = axes.flatten()

    for ax, phase in zip(axes, phases):
        lr = _flat(results, phase, "lr")
        ax.hist(lr, bins=50, color=PHASE_COLORS[phase], alpha=0.7,
                edgecolor="white", linewidth=0.4)
        ax.axvline(1.0, color="black", linewidth=1.2, linestyle="--")
        ax.set_title(PHASE_LABELS[phase], fontsize=13, fontweight="bold")
        ax.set_xlabel("Loss Ratio", fontsize=11)
        ax.set_ylabel("Frequency", fontsize=11)
        sd = lr.std()
        pct = 100 * (lr > 1.0).mean()
        ax.text(0.97, 0.93, f"SD = {sd:.3f}\n> 1.00: {pct:.1f}%",
                transform=ax.transAxes, ha="right", va="top", fontsize=10,
                bbox=dict(facecolor="white", edgecolor="grey", alpha=0.8, boxstyle="round"))

    fig.suptitle(
        "Distribution of Insurer Loss Ratios by Risikoausgleich Phase\n"
        "(N = 10,000, K = 10 insurers, 200 simulations, moderate adverse selection)",
        fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def figure_solvency_gap(results, output_path):
    """Figure 2: Solvency gap curves and loss ratio SD by phase."""
    phases = ["no_ra", 1, 2, 3]
    thresholds = np.linspace(0.90, 1.40, 100)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    ax = axes[0]
    for phase in phases:
        lr = _flat(results, phase, "lr")
        gap = [100 * (lr > t).mean() for t in thresholds]
        ax.plot(thresholds, gap, label=PHASE_LABELS[phase],
                color=PHASE_COLORS[phase], linewidth=2)
    ax.axvline(1.0, color="grey", linewidth=1, linestyle=":")
    ax.set_xlabel("Loss Ratio Threshold", fontsize=12)
    ax.set_ylabel("% of Insurers Exceeding Threshold", fontsize=12)
    ax.set_title("A. Solvency Gap by RA Phase", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)
    ax.set_xlim(0.90, 1.40)

    ax2 = axes[1]
    phase_names = [PHASE_LABELS[p] for p in phases]
    sds = [_flat(results, p, "lr").std() for p in phases]
    bars = ax2.bar(phase_names, sds, color=[PHASE_COLORS[p] for p in phases],
                   alpha=0.8, edgecolor="grey")
    ax2.set_ylabel("Standard Deviation of Loss Ratio", fontsize=12)
    ax2.set_title("B. Loss Ratio Dispersion by RA Phase", fontsize=13, fontweight="bold")
    ax2.set_ylim(0, max(sds) * 1.3)
    sd_no_ra = sds[0]
    for bar, sd, i in zip(bars, sds, range(len(sds))):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.003,
                 f"{sd:.3f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
        if i > 0:
            reduction = 100 * (sd_no_ra - sd) / sd_no_ra
            ax2.text(i, sd / 2, f"-{reduction:.0f}%\nvs. No RA",
                     ha="center", va="center", fontsize=9, color="white", fontweight="bold")

    fig.suptitle("Solvency Analysis: Effect of Risikoausgleich Phases\n"
                 "(200 Monte Carlo replications, K = 10 insurers per replication)", fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def figure_sensitivity_adverse_selection(output_path):
    """Figure 3: Loss ratio SD vs adverse selection intensity, Phase 1 vs Phase 3."""
    strengths = np.linspace(0, 1, 11)
    n_sim_s = 100
    results_by_strength = {1: [], 3: []}

    for strength in strengths:
        res = run_simulation(n=10_000, k=10,
                             adverse_selection_strength=float(strength),
                             n_sim=n_sim_s)
        for phase in [1, 3]:
            results_by_strength[phase].append(_flat(res, phase, "lr").std())

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(strengths, results_by_strength[1], "o-", color=PHASE_COLORS[1],
            label="Phase 1 (age/sex)", linewidth=2, markersize=5)
    ax.plot(strengths, results_by_strength[3], "s-", color=PHASE_COLORS[3],
            label="Phase 3 (+PCG)", linewidth=2, markersize=5)
    ax.fill_between(strengths, results_by_strength[1], results_by_strength[3],
                    alpha=0.15, color="purple", label="RA benefit (Phase 3 vs Phase 1)")
    ax.set_xlabel("Adverse Selection Strength (0 = random, 1 = full sorting)", fontsize=12)
    ax.set_ylabel("Standard Deviation of Loss Ratio", fontsize=12)
    ax.set_title("Loss Ratio Dispersion vs. Adverse Selection Intensity\n"
                 "Phase 1 vs. Phase 3, 100 simulations each", fontsize=12)
    ax.legend(fontsize=11)
    ax.set_xlim(0, 1)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def figure_combined_ratio_distribution(results, output_path):
    """
    Figure 4: Combined ratio distributions by phase (2×2 grid).
    The breakeven combined ratio is 1.0; the vertical line marks this threshold.
    """
    phases = ["no_ra", 1, 2, 3]
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    axes = axes.flatten()

    for ax, phase in zip(axes, phases):
        cr = _flat(results, phase, "cr", clip_center=1.1, clip_radius=1.2)
        ax.hist(cr, bins=50, color=PHASE_COLORS[phase], alpha=0.7,
                edgecolor="white", linewidth=0.4)
        ax.axvline(1.0, color="black", linewidth=1.2, linestyle="--", label="CR = 1.0")
        ax.set_title(PHASE_LABELS[phase], fontsize=13, fontweight="bold")
        ax.set_xlabel("Combined Ratio", fontsize=11)
        ax.set_ylabel("Frequency", fontsize=11)
        sd = cr.std()
        pct = 100 * (cr > 1.0).mean()
        ax.text(0.97, 0.93, f"SD = {sd:.3f}\n> 1.00: {pct:.1f}%",
                transform=ax.transAxes, ha="right", va="top", fontsize=10,
                bbox=dict(facecolor="white", edgecolor="grey", alpha=0.8, boxstyle="round"))

    fig.suptitle(
        "Distribution of Insurer Combined Ratios (LR + ER) by Risikoausgleich Phase\n"
        "(N = 10,000, K = 10 insurers, 200 simulations, moderate adverse selection)\n"
        "Combined ratio > 1.0 implies underwriting loss",
        fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def figure_combined_ratio_decomposition(results, output_path):
    """
    Figure 5: Stacked bar chart decomposing mean combined ratio into LR and ER
    components across phases, with SD whiskers on the combined ratio.
    Shows how RA reduces both components, with LR driving most of the improvement.
    """
    phases = ["no_ra", 1, 2, 3]
    phase_names = [PHASE_LABELS[p] for p in phases]

    mean_lr, mean_er, mean_cr, sd_cr = [], [], [], []
    for phase in phases:
        lr = _flat(results, phase, "lr", clip_center=1.1, clip_radius=1.2)
        er = _flat(results, phase, "er", clip_center=0.08, clip_radius=0.3)
        cr = _flat(results, phase, "cr", clip_center=1.1, clip_radius=1.2)
        mean_lr.append(lr.mean())
        mean_er.append(er.mean())
        mean_cr.append(cr.mean())
        sd_cr.append(cr.std())

    x = np.arange(len(phases))
    width = 0.55

    fig, ax = plt.subplots(figsize=(10, 6))

    bars_lr = ax.bar(x, mean_lr, width, label="Loss Ratio (LR)",
                     color="#4c72b0", alpha=0.85, edgecolor="white")
    bars_er = ax.bar(x, mean_er, width, bottom=mean_lr, label="Expense Ratio (ER)",
                     color="#dd8452", alpha=0.85, edgecolor="white")

    # SD whiskers on the combined ratio total
    ax.errorbar(x, mean_cr, yerr=sd_cr, fmt="none", color="black",
                capsize=6, linewidth=1.5, label="SD of Combined Ratio")

    ax.axhline(1.0, color="black", linewidth=1.2, linestyle="--", label="Breakeven (CR = 1.0)")
    ax.set_xticks(x)
    ax.set_xticklabels(phase_names, fontsize=11)
    ax.set_ylabel("Ratio Value", fontsize=12)
    ax.set_title("Combined Ratio Decomposition by Risikoausgleich Phase\n"
                 "Mean LR and ER with combined ratio standard deviation",
                 fontsize=13, fontweight="bold")
    ax.legend(fontsize=10, loc="upper right")
    ax.set_ylim(0, max(mean_cr) + max(sd_cr) + 0.15)

    # Label total CR on each bar
    for xi, cr_val, sd_val in zip(x, mean_cr, sd_cr):
        ax.text(xi, cr_val + sd_val + 0.01, f"CR={cr_val:.3f}",
                ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# 8. SUMMARY STATISTICS PRINTOUT
# ═══════════════════════════════════════════════════════════════════════════════

def print_summary(results):
    """Print compact summary tables for LR, ER, and CR by phase."""

    for metric, label, center in [("lr", "Loss Ratio (LR)", 1.0),
                                   ("er", "Expense Ratio (ER)", 0.08),
                                   ("cr", "Combined Ratio (CR)", 1.1)]:
        print(f"\n{'=' * 70}")
        print(f"SIMULATION SUMMARY: {label} Statistics by RA Phase")
        print(f"{'=' * 70}")
        header = f"{'Phase':<22} {'Mean':>8} {'SD':>8} {'P5':>8} {'P95':>8} {'%>1.00':>8}"
        print(header)
        print("-" * 70)
        for phase in ["no_ra", 1, 2, 3]:
            arr = _flat(results, phase, metric, clip_center=center, clip_radius=1.5)
            pct_above1 = 100 * (arr > 1.0).mean()
            print(f"{PHASE_LABELS[phase]:<22}"
                  f" {arr.mean():>8.4f}"
                  f" {arr.std():>8.4f}"
                  f" {np.percentile(arr, 5):>8.4f}"
                  f" {np.percentile(arr, 95):>8.4f}"
                  f" {pct_above1:>7.1f}%")
        print("=" * 70)

    # R² comparison
    print("\nR2 of cost prediction model (estimated from one replication):")
    pop_demo = generate_population(50_000)
    _, realized_demo = compute_true_cost(pop_demo)
    for lbl, pred_fn in [("Phase 1", predict_cost_phase1),
                          ("Phase 2", predict_cost_phase2),
                          ("Phase 3", predict_cost_phase3)]:
        pred = pred_fn(pop_demo, realized_demo)
        ss_res = np.sum((realized_demo - pred) ** 2)
        ss_tot = np.sum((realized_demo - realized_demo.mean()) ** 2)
        r2 = 1 - ss_res / ss_tot
        print(f"  {lbl}: R2 = {r2:.4f} ({100 * r2:.1f}%)")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# 9. MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Running Swiss OKP Risk Equalization Simulation...")
    print("  Population size: 10,000 | Insurers: 10 | Simulations: 200")
    print("  Adverse selection strength: 0.50 (moderate sorting)")

    results = run_simulation(n=10_000, k=10, adverse_selection_strength=0.5, n_sim=200)

    print_summary(results)

    figure_loss_ratio_distribution(
        results, os.path.join(OUTPUT_DIR, "f01_loss_ratio_distribution.png"))

    figure_solvency_gap(
        results, os.path.join(OUTPUT_DIR, "f02_solvency_gap_by_phase.png"))

    print("\nRunning sensitivity analysis (adverse selection strength 0 to 1)...")
    figure_sensitivity_adverse_selection(
        os.path.join(OUTPUT_DIR, "f03_sensitivity_adverse_selection.png"))

    figure_combined_ratio_distribution(
        results, os.path.join(OUTPUT_DIR, "f04_combined_ratio_distribution.png"))

    figure_combined_ratio_decomposition(
        results, os.path.join(OUTPUT_DIR, "f05_combined_ratio_decomposition.png"))

    print("\nAll figures saved to output/figures/")
