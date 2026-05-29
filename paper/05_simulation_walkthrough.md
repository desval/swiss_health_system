# Simulation Walkthrough: Mechanics and Interpretation

This chapter describes the logic of the Python simulation (`code/simulation.py`) in plain language. It is intended to bridge the formal model in Chapter 3 and the quantitative results reported in Chapter 6. A reader who wants to understand why the simulation produces the numbers it does — rather than just what those numbers are — should read this chapter first.

---

## Step 1: Generate a Synthetic Population

The simulation draws 10,000 individuals, each assigned four types of characteristics:

- **Age group**: one of four categories (child, young adult, adult, elderly), sampled with probabilities calibrated to the 2022 Swiss resident population.
- **Sex**: binary, drawn with equal probability.
- **Prior-year hospital admission**: binary, drawn with age-group-specific probabilities (5% for children, 25% for the elderly).
- **PCG memberships**: 22 binary indicators, one per Pharmaceutical Cost Group. Prevalence is calibrated to Swiss BAG statistics and increases with age and hospitalization status — older, recently hospitalized individuals are more likely to be in a PCG group.

These characteristics are the only things the risk adjustment formula can see. They are the *observable* part of each individual's health status.

---

## Step 2: Draw Realized Costs

Each individual's annual cost is computed in two parts.

The first part is the *expected cost* — the systematic, predictable component that the formula is trying to capture:

```
expected_cost_i = base_cost
                + age_effect
                + sex_effect
                + hospital_effect       (large: ~CHF 12,000)
                + sum of PCG effects    (CHF 900–15,000 per active group)
```

The base cost is CHF 3,800 (calibrated to the Swiss adult average). Hospitalization adds a large increment because prior admission is strongly predictive of future costs. PCG groups add smaller but still substantial increments depending on the therapeutic class.

The second part is *noise* — the unpredictable residual that even a perfect formula cannot anticipate. This is drawn from a log-normal distribution with mean one, so it multiplies the expected cost by a random factor centered on 1.0 but with a standard deviation of roughly CHF 5,500. The log-normal shape captures the right-skewed nature of healthcare costs: most individuals cost close to their expected value, but a small fraction have very high draws.

*Realized cost = expected cost × noise draw.*

The key point: the formula compensates insurers for the expected cost, but they bear the full realized cost including the noise. Even under perfect risk adjustment, loss ratios will not be exactly 1.0 — the noise term creates unavoidable residual variance that diversifies away only as pool size grows.

---

## Step 3: Assign Individuals to Insurers

This is where adverse selection enters the model. Each individual is assigned to one of 10 insurers using a score that mixes random assignment with cost-based sorting:

```
sort_score_i = (1 − λ) × uniform_random + λ × rank_by_expected_cost
```

where λ ∈ [0, 1] is the *adverse selection strength*.

- **λ = 0 (no selection)**: assignment is purely random. Every insurer receives a statistically representative cross-section of the population. Expected costs differ across insurers only due to random sampling — the law of large numbers ensures these differences are small.
- **λ = 1 (full sorting)**: individuals sort perfectly by expected cost. The cheapest 10% of the population go to insurer 1, the most expensive 10% go to insurer 10. Each insurer's pool is homogeneous in expected cost but very different from the others.
- **λ = 0.5 (moderate sorting, the default)**: a mix. Healthier individuals are more likely to end up in lower-cost insurers, but the sorting is imperfect — there is still substantial mixing.

This parameter captures, in a stylized way, the combined effect of several real-world mechanisms: insurers designing networks or benefit structures to deter sick enrollees, healthy individuals seeking lower-premium plans, and the limited enforcement of the open enrollment obligation.

---

## Step 4: Compute the Risikoausgleich Transfer

For each insurer j, the RA transfer is computed in three sub-steps.

**Predict the cost of insurer j's actual pool.** Apply the phase-specific formula to each enrolled individual and sum:

```
predicted_pool_cost_j = sum over i in j of: predicted_cost(x_i)
```

The predicted cost uses only the characteristics included in the relevant phase:
- Phase 1: age and sex → cell average costs by age × sex combination
- Phase 2: age, sex, and hospital admission → cell averages by age × sex × hospital
- Phase 3: OLS regression on age, sex, hospital, and all 22 PCG indicators

**Compute what the pool "should" cost at system average risk.**

```
neutral_cost_j = N_j × system_avg_predicted_cost
```

This is what insurer j would be predicted to spend if its enrollees were exactly average in risk composition.

**The transfer is the difference:**

```
T_j = predicted_pool_cost_j − neutral_cost_j
```

If insurer j's pool is predicted to be more expensive than average, T_j > 0: it receives a transfer. If cheaper than average, T_j < 0: it contributes to the pool. By construction, transfers sum to zero across all insurers.

---

## Step 5: Compute Loss Ratio, Expense Ratio, and Combined Ratio

All insurers charge the same flat premium, set to cover both expected claims and expected administrative costs (community rating). The premium includes a loading of approximately 7.3% above expected claims costs.

**Loss ratio (LR):**

```
LR_j = realized_cost_j / RA-adjusted_revenue_j
```

The RA transfer enters the denominator — it augments effective revenue for sick pools and reduces it for healthy pools, pushing all loss ratios toward 1.0.

**Expense ratio (ER):**

Administrative costs have two parts:
- Fixed: CHF 280 per enrollee per year (IT, member services, regulation) — independent of risk
- Variable: 2% of realized claims (adjudication, authorisation, care coordination) — scales with cost volume

```
admin_j = 280 × N_j + 0.02 × realized_cost_j
ER_j    = admin_j / RA-adjusted_revenue_j
```

**Combined ratio (CR):**

```
CR_j = LR_j + ER_j = (realized_cost_j + admin_j) / RA-adjusted_revenue_j
```

The breakeven point is CR = 1.0 (revenue covers claims and admin exactly). CR > 1.0 implies an underwriting loss.

The RA influences the expense ratio through the same denominator mechanism as the loss ratio: for a high-risk pool that receives a positive RA transfer, both LR and ER fall because the same admin cost is spread over a larger effective revenue base. For a low-risk pool that pays into the RA, both rise. This means RA has a *double benefit* for high-risk pools — it relieves both the claims burden and the administrative cost pressure simultaneously.

---

## How RA Influences the Results: The Key Mechanism

The intuition is straightforward once the steps above are clear.

**Without RA**, insurer revenue is the same per head regardless of pool composition. An insurer that attracts sicker enrollees will have higher realized costs but the same revenue — its loss ratio exceeds 1.0. At the same time, because variable admin costs scale with claims, its expense ratio also rises, compounding the combined ratio above 1.0.

**With perfect RA**, the denominator is exactly adjusted to match each insurer's predicted costs. The only remaining loss ratio variance is the unpredictable individual noise ε_i, which diversifies away as pool size grows. The expense ratio also equalizes: the fixed admin per-head cost becomes the same fraction of revenue for all pools once revenues are equalized; and the variable processing cost tracks the equalized loss ratio.

**With imperfect RA** (the realistic case), the uncompensated cost component — morbidity variation not captured by the formula — still drives loss ratio dispersion. This uncompensated component affects both LR and ER: high-uncompensated-cost insurers have high LR (claims exceed RA-adjusted revenue) and high ER (variable processing cost scales with high claims; and the RA transfer, being too small, leaves the fixed admin as a high share of the under-augmented denominator).

Each successive RA phase reduces the uncompensated component:
- Phase 1 misses the morbidity signal: a 65-year-old with five chronic conditions and a healthy 65-year-old receive the same RA compensation.
- Phase 2 adds hospitalization — a strong but lagged and binary morbidity signal.
- Phase 3 adds PCG groups, directly capturing chronic disease burden through drug consumption.

The simulation quantifies this improvement. **Loss ratio SD** falls from 0.395 (Phase 1) to 0.218 (Phase 2) to 0.127 (Phase 3). **Combined ratio SD** follows a similar path: from 0.387 to 0.197 to 0.098. The share of insurers facing combined ratios above 1.0 falls from 41.1% (Phase 1) to 9.3% (Phase 3) — the most direct measure of underwriting loss risk across the market.

One nuance worth noting: the mean expense ratio increases slightly across phases (from ~5.3% under Phase 1 to ~6.5% under Phase 3). This is not a sign of higher costs, but of a denominator effect in low-risk pools. As RA phases improve, the transfers grow in magnitude — meaning low-risk pools pay larger contributions, shrinking their RA-adjusted revenue. Their fixed admin cost therefore represents a larger share of a smaller base. This redistribution of the expense ratio burden from high-risk to low-risk pools is an inherent feature of any transfer system, and it is fully offset by the corresponding reduction in their loss ratio.

---

## What the Simulation Does Not Capture

Three important real-world features are absent from the simulation and should be kept in mind when interpreting the numbers.

**Insurer response.** The simulation takes enrollment as given: once individuals are assigned to insurers, they stay there. In reality, insurers react to the RA formula by adjusting plan design, marketing, and service offerings to attract or deter specific risk types. A richer model would make assignment endogenous to the formula — meaning that a better formula not only reduces loss ratio dispersion for a given allocation but also changes the equilibrium allocation itself.

**Formula gaming.** The simulation assumes that PCG membership (**p_i**) is exogenous. In practice, an insurer might influence whether its enrollees are classified into PCG groups — for example, by prescribing or not prescribing drugs in PCG-eligible categories. Since PCG membership drives RA receipts, there is a financial incentive to inflate it. This is a recognized concern with pharmaceutical-based risk adjustment formulas and is outside the scope of the current model.

**Dynamic adverse selection.** The simulation is static: the population is drawn once, assigned once, and costs are realized once. In a dynamic setting, insurer strategies evolve over time as they learn which individual characteristics predict high uncompensated costs, and individuals update their plan choices as their health status changes. The erosion of Phase 1's effectiveness documented by Beck et al. (2010) — where the formula was effective initially but lost predictive power over time as insurers optimized against it — is a dynamic effect that a one-period simulation cannot capture.
