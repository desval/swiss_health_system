# Appendix A: Key Performance Indicators

This appendix defines the quantitative metrics used throughout the model, simulation, and summary chapters. For each KPI, the definition is given first in formal notation, then in plain language, followed by the Swiss-specific interpretation and the benchmark value or threshold relevant to this analysis.

---

## A.1 Loss Ratio (LR)

**Definition:**

> LR_j = C_j / R_j*

where C_j is insurer j's total realized claims expenditure and R_j* is effective revenue after the Risikoausgleich transfer.

**Plain language:** For every franc of effective revenue, how many francs did the insurer pay out in claims? A loss ratio of 0.90 means 90 cents in claims per franc of revenue; a ratio of 1.10 means 10 cents in losses per franc of revenue.

**Interpretation:** The loss ratio is the primary measure of underwriting performance on the claims side. It reflects three factors: (1) the riskiness of the insurer's enrolled population, (2) the precision of the Risikoausgleich formula in compensating for that risk, and (3) random claims volatility. In expectation, a perfectly equalized market would have LR_j = 1 − e_V · LR_j (net of variable admin), i.e., LR slightly below 1.0 to leave room for the variable expense loading.

**Threshold:** LR > 1.0 indicates that claims alone exceed revenue. Sustained LR > 1.0 depletes reserves and triggers regulatory intervention under FINMA solvency rules.

**Simulation benchmark:** Under Phase 3 and moderate adverse selection, the cross-insurer standard deviation of LR is approximately 0.127, compared to 0.395 under Phase 1 (age/sex only).

---

## A.2 Expense Ratio (ER)

**Definition:**

> ER_j = A_j / R_j*

where A_j = e_F · N_j + e_V · C_j is total administrative cost, decomposed into:
- **Fixed component** e_F · N_j: overhead proportional to pool size (IT, member services, regulatory compliance, reserve management). Calibrated to CHF 280 per enrollee per year in the Swiss context.
- **Variable component** e_V · C_j: claims processing costs proportional to realized claims volume (adjudication, authorization, care coordination). Calibrated to approximately 2% of claims.

**Plain language:** For every franc of effective revenue, how many francs were spent on administration? An expense ratio of 0.07 means 7 cents in admin per franc of revenue.

**Interpretation:** Unlike the loss ratio, the expense ratio is not directly targeted by the Risikoausgleich — the RA does not compensate for administrative cost differences. However, the RA affects the ER indirectly through two channels: (1) the denominator effect on the fixed component (a high-risk insurer receiving a positive RA transfer has higher effective revenue, so the same fixed overhead represents a smaller share), and (2) the variable component tracking the loss ratio improvement (lower LR after RA → lower variable processing costs as a share of revenue).

**Threshold:** There is no single regulatory threshold for the expense ratio in Swiss OKP, but the BAG reviews administrative cost levels in the context of premium approval. The Swiss legal framework does not set an explicit cap, but administrative loadings above approximately 10% of premiums attract regulatory scrutiny.

**Simulation benchmark:** Mean ER across phases ranges from approximately 4.9% (no RA) to 6.5% (Phase 3). The increase in mean ER from Phase 1 to Phase 3 reflects the redistribution of fixed overhead burden: as RA transfers grow in magnitude, low-risk pools pay larger contributions, shrinking their RA-adjusted revenue base and raising their expense ratio — while high-risk pools see the reverse.

---

## A.3 Combined Ratio (CR)

**Definition:**

> CR_j = LR_j + ER_j = (C_j + A_j) / R_j*

**Plain language:** For every franc of effective revenue, how many francs were spent in total (claims plus administration)? A combined ratio of 1.05 means the insurer spent CHF 1.05 for every CHF 1.00 it received — a 5-cent underwriting loss per franc of revenue.

**Interpretation:** The combined ratio is the standard insurance metric for overall underwriting performance. It integrates both sides of insurer finances and is the appropriate metric for assessing solvency risk, capital requirements, and competitive viability. The premium in the Swiss OKP system is set precisely to make the expected combined ratio equal to 1.0 at the system level — meaning individual insurers can be above or below 1.0 depending on risk-pool composition and RA precision.

**Threshold:**
- CR < 1.0: underwriting profit — revenue exceeds total costs; insurer can build reserves
- CR = 1.0: breakeven — revenue exactly covers claims and admin; no underwriting profit or loss
- CR > 1.0: underwriting loss — insurer must draw on reserves or raise capital

In the OKP context, sustained CR > 1.0 implies that the insurer cannot cover its costs from premium revenue alone. Given the prohibition on cross-subsidization from supplementary insurance, this directly threatens OKP operations.

**Simulation benchmark:**

| Phase | Mean CR | SD of CR | % Insurers with CR > 1.0 |
|-------|---------|----------|--------------------------|
| No RA | ~0.885 | 0.634 | 44.3% |
| Phase 1 (age/sex) | ~0.919 | 0.387 | 41.1% |
| Phase 2 (+hospital) | ~0.887 | 0.197 | 35.8% |
| Phase 3 (+PCG) | ~0.921 | 0.098 | 9.3% |

---

## A.4 Risikoausgleich Transfer (T_j)

**Definition:**

> T_j^(φ) = Ĉ_j^(φ) − N_j · c̄

where Ĉ_j^(φ) = Σ_{i ∈ j} ĉ_i^(φ) is the sum of predicted costs for insurer j's enrollees under phase φ, and c̄ is the system-wide average predicted cost per enrollee.

**Plain language:** How much does the RA system pay to (or collect from) insurer j, based on the predicted riskiness of its pool relative to the system average? A positive transfer means the insurer's pool is predicted to be more expensive than average; it receives compensation. A negative transfer means its pool is cheaper than average; it contributes to the fund.

**Properties:**
- Σ_j T_j^(φ) = 0 for all φ: the system is budget-neutral across all insurers
- T_j^(φ) = 0 for all j when all insurer pools have identical predicted risk composition
- T_j^(φ) increases in magnitude as pool heterogeneity increases (more adverse selection → larger transfers needed)

**Swiss context:** The RA transfers in Switzerland are administered annually by the *Gemeinsame Einrichtung KVG* (Common Institution under the KVG). In 2022, the total volume of RA transfers across all Krankenkassen was approximately CHF 10 billion — roughly one third of total OKP premium revenue — illustrating the scale of redistribution required to sustain community rating in a market with substantial risk heterogeneity.

---

## A.5 Predictive R² of the Risk Adjustment Formula

**Definition:**

> R²^(φ) = 1 − Var(c_i − ĉ_i^(φ)) / Var(c_i)

The proportion of total individual cost variance explained by the phase-φ prediction formula, measured at the individual level.

**Plain language:** Of all the variation in individual annual healthcare costs, what fraction can be predicted from the characteristics included in the RA formula? The remainder (1 − R²) is unpredictable noise plus systematic variation the formula misses.

**Interpretation:** R² is the single most important summary statistic for evaluating RA formula quality. All else equal, higher R² means lower residual adverse selection incentives, lower cross-insurer loss ratio variance, and lower required capital buffers. It is the key metric used in comparative analyses of European risk adjustment systems (Van de Ven et al., 2003).

**Benchmarks:**

| System / Phase | Approximate R² |
|----------------|---------------|
| Swiss Phase 1 (age/sex) | 10–15% |
| Swiss Phase 2 (+hospital) | 20–22% |
| Swiss Phase 3 (+PCG) | 28–33% |
| Netherlands (ACG-based, early 2000s) | ~15–20% |
| Netherlands (current, full morbidity) | ~35–45% |
| Simulation Phase 1 | ~35% |
| Simulation Phase 2 | ~62% |
| Simulation Phase 3 | ~76% |

*Note: simulation R² values exceed real-world benchmarks because the simulated data are generated from the same parametric model used for prediction. The relative improvement across phases is the relevant comparison.*

**Limitation:** R² measures average predictive accuracy and does not capture where in the cost distribution the formula fails. A formula with high aggregate R² can still leave large selection margins in specific high-cost sub-populations (e.g., rare disease patients) if it under-compensates extreme values. This is the Glazer-McGuire critique of standard demographic and morbidity-based adjustment formulas.

---

## A.6 Uncompensated Cost Variance

**Definition:**

> σ²_δ^(φ) = Var(c_i − ĉ_i^(φ))

The variance of the gap between an individual's actual expected cost and the predicted cost under phase φ. This is the component of individual cost variation that the RA formula fails to capture and therefore cannot compensate.

**Plain language:** How much does the formula's prediction miss, on average? A large uncompensated variance means the formula leaves a wide range of "free" risk that insurers can exploit through selective enrollment.

**Relationship to R²:** σ²_δ^(φ) = (1 − R²^(φ)) · Var(c_i). A phase with R² = 30% has an uncompensated variance equal to 70% of total individual cost variance.

**Relationship to loss ratio variance:** Under Proposition 2 (Chapter 3), the cross-insurer variance of expected loss ratios is proportional to σ²_δ^(φ) and to the degree of adverse selection. Reducing σ²_δ is therefore the direct mechanism through which RA reforms reduce financial risk dispersion across insurers.

---

## A.7 Solvency Capital Buffer (κ)

**Definition:**

> κ_j^(φ) = z_α · σ_{CR}^(φ) · p̄

The minimum capital reserve insurer j must hold to ensure the probability of combined ratio exceeding 1.0 + τ does not exceed the regulatory tolerance α, where z_α is the α-quantile of the standard normal distribution, σ_{CR}^(φ) is the combined ratio standard deviation under phase φ, and p̄ is the average premium.

**Plain language:** How large a financial cushion must an insurer maintain to survive an adverse year without insolvency? The larger the combined ratio variance, the larger the required buffer.

**Relationship to RA phases:** Since σ_{CR}^(φ) decreases monotonically across phases (Section 5, Chapter 3), the required capital buffer shrinks with each RA reform. The reduction in required capital is proportional to the reduction in combined ratio standard deviation:

> Δκ_j = z_α · p̄ · (σ_{CR}^(1) − σ_{CR}^(3)) ≈ z_α · p̄ · (0.387 − 0.098) = z_α · p̄ · 0.289

At α = 5% (z_α = 1.645) and p̄ = CHF 5,150 (claims + admin), this implies a reduction in required capital per-enrollee of approximately CHF 2,450 — a substantial release of capital that can be redeployed toward premium reduction or service investment.
