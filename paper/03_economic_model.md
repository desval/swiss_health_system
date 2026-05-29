# A Formal Model of the Swiss OKP with Risikoausgleich

## 1. Introduction

This chapter develops a partial equilibrium model of the Swiss mandatory health insurance market (OKP) that makes the role of the Risikoausgleich (RA) precise. The model has three elements: a population of heterogeneous individuals with observable and unobservable characteristics that determine their medical expenditures; a set of competing insurers who observe only the community-rated premium and bear the full distribution of realized costs; and a regulator who implements a transfer formula based on observable individual characteristics. The central object of analysis is the *loss ratio* — the ratio of realized claims costs to premium revenue — which governs insurer solvency. We derive analytical results characterizing how the precision of the RA formula affects the distribution of loss ratios and the required solvency buffer, and we trace through the implications of the three historical phases of the Swiss system.

---

## 2. Population and Individual Cost Model

### 2.1 Setup

Let there be a continuum of individuals indexed by i ∈ [0,1]. Each individual is characterized by a vector of observable characteristics:

> **x_i** = (a_i, s_i, h_i, **p_i**)

where:
- a_i ∈ {0,1,...,A} is age group (discretized into A+1 cells, e.g., five-year bands)
- s_i ∈ {0,1} is sex (0 = female, 1 = male, or vice versa)
- h_i ∈ {0,1} is a binary indicator for prior-year hospital or nursing home admission
- **p_i** = (p_{i,1},...,p_{i,M}) ∈ {0,1}^M is a vector of PCG group memberships (M = 22 in the Swiss system)

In addition, each individual has an unobservable characteristic ε_i drawn independently from a distribution F with mean zero and variance σ²_ε. The unobservable ε_i captures residual health status variation not summarized by **x_i**: chronic conditions not identified by pharmaceutical consumption, acute illness episodes, genetic predisposition, and behavioral factors.

### 2.2 Medical Expense

Annual individual medical expenditure c_i is determined by:

> c_i = **β**·**x_i** + ε_i                (1)

where **β** = (β_a, β_s, β_h, **β_p**) is the vector of cost parameters. In a linear cost model, each component of **x_i** contributes additively to expected costs. We assume:

- β_{a,k} > 0 for all age groups k, increasing in age (older individuals have higher expected costs)
- β_s reflects the sex differential (on average, women have higher costs in reproductive ages; men in older ages)
- β_h > 0 (prior hospitalization is strongly predictive of subsequent costs)
- β_{p,m} > 0 for all m = 1,...,M (PCG membership predicts higher pharmaceutical and overall costs)

The error term ε_i satisfies E[ε_i | **x_i**] = 0 (conditional mean independence: **x_i** is a sufficient statistic for the predictable component of costs). The variance σ²_ε is large relative to the variance of **β**·**x_i**: in empirical health cost models, individual-level R² is typically 5–30%, meaning the unpredictable residual accounts for 70–95% of total individual cost variance.

### 2.3 Observed Characteristics and Information Structure

The three phases of the Swiss Risikoausgleich differ in which elements of **x_i** are included in the formula:

| Phase | Observable characteristics included |
|-------|--------------------------------------|
| Phase 1 (1996–2011) | a_i, s_i |
| Phase 2 (2012–2019) | a_i, s_i, h_i |
| Phase 3 (2020–) | a_i, s_i, h_i, **p_i** |

Denote the information set available under phase φ as **x_i^(φ)**. The predicted cost under phase φ is:

> ĉ_i^(φ) = **β̂^(φ)**·**x_i^(φ)**

where **β̂^(φ)** is estimated by ordinary least squares on the national population (equivalently, it equals the cell-specific average cost across all enrollees in the relevant risk cell). Define the residual under phase φ:

> η_i^(φ) = c_i − ĉ_i^(φ) = (**β** − **β̂^(φ)**_extended)·**x_i** + ε_i

where **β̂^(φ)**_extended is the Phase-φ coefficient vector padded with zeros for characteristics not included in Phase φ. The variance of η_i^(φ) is decreasing in φ (each successive phase reduces the unexplained variance), and we denote it σ²_φ, with σ²_1 > σ²_2 > σ²_3.

---

## 3. Insurance Market and Community Rating

### 3.1 Insurer Structure

There are K insurers, indexed j = 1,...,K. Each insurer operates in the same canton (or equivalently, we analyze a single canton). Insurer j charges a monthly premium p_j per enrolled adult. Under community rating, p_j does not vary across individuals within insurer j: every adult enrollee in insurer j in the same premium region pays the same p_j.

Let N_j be the number of individuals enrolled with insurer j, and let ω_{ij} ∈ {0,1} denote individual i's enrollment with insurer j (Σ_j ω_{ij} = 1 for all i). The set of individuals enrolled with insurer j is J = {i : ω_{ij} = 1}.

### 3.2 Revenue

Total annual OKP premium revenue for insurer j:

> R_j = N_j · 12 · p_j

(The factor of 12 converts monthly premiums to annual revenue; we suppress it hereafter by treating p_j as an annual premium.)

Under premium approval, the BAG sets p_j ≈ c̄_j^e + κ_j, where c̄_j^e = E[c_i | i ∈ j] is the expected per-capita cost of insurer j's pool as estimated by the insurer, and κ_j is a reserve loading. In equilibrium — assuming actuarially accurate estimation — p_j = c̄_j^e + κ_j.

**Key observation**: if all insurers charge the same premium (p_j = p̄ for all j, i.e., perfect premium equalization across insurers), then each insurer's revenue is simply N_j · p̄, which does not depend on the riskiness of its pool. This case — relevant to the competitive equilibrium when premiums are fully comparable across insurers — is the natural benchmark for analyzing RA effects.

### 3.3 Total Cost and Loss Ratio

Insurer j's total realized cost in a given year:

> C_j = Σ_{i ∈ j} c_i = Σ_{i ∈ j} (**β**·**x_i** + ε_i)

The *loss ratio* of insurer j is:

> LR_j = C_j / R_j = (Σ_{i ∈ j} c_i) / (N_j · p_j)             (2)

In the absence of Risikoausgleich, the loss ratio directly governs solvency: LR_j > 1 implies claims exceed revenue in that year; sustained LR_j > 1 depletes reserves and eventually triggers regulatory intervention.

**Expected loss ratio without RA**: using c̄_j = E[c_i | i ∈ j] for the expected per-capita cost of insurer j's pool, and p_j = c̄_j + κ_j (accurate premium setting with loading κ_j):

> E[LR_j] = c̄_j / (c̄_j + κ_j) < 1

If insurer j's pool is representative of the population (c̄_j = c̄_system), then E[LR_j] = c̄ / (c̄ + κ) for all j. But if adverse selection concentrates high-risk individuals in certain insurers and low-premium insurers retain only healthy enrollees, then:
- For high-risk insurer j^H: c̄_{j^H} > c̄_system + κ_{j^H}, so E[LR_{j^H}] > 1 if the premium was set based on anticipated average costs.
- For low-risk insurer j^L: E[LR_{j^L}] << 1.

The expected loss ratio variance across insurers is:

> Var_j(E[LR_j]) ∝ Var_j(c̄_j)

i.e., the cross-insurer dispersion of loss ratios is determined by the dispersion of average costs across pools. Risk equalization works directly on this quantity.

---

## 4. Risikoausgleich Transfer Formula

### 4.1 Transfer Computation

Under phase φ, the RA transfer to insurer j is defined as the difference between the *expected cost of insurer j's actual pool* (computed using the phase-φ prediction model applied to insurer j's enrolled individuals) and the *expected cost of a pool of the same size at the population average risk*:

> T_j^(φ) = Ĉ_j^(φ) − N_j · c̄                (3)

where:
- Ĉ_j^(φ) = Σ_{i ∈ j} ĉ_i^(φ) = Σ_{i ∈ j} **β̂^(φ)**·**x_i^(φ)** is the total predicted cost of insurer j's pool under phase φ
- c̄ = (1/N) Σ_i c_i^e is the national average per-capita cost (where c_i^e = **β̂^(φ)**·**x_i^(φ)** at the population level, but in practice is taken as the average realized cost)

The transfer T_j^(φ) is positive for high-risk pools and negative for low-risk pools. By construction, Σ_j T_j^(φ) = 0 (the system is budget-neutral: total transfers sum to zero across all insurers).

### 4.2 Adjusted Revenue and Loss Ratio

After the RA transfer, insurer j's effective revenue is:

> R_j^*(φ) = R_j + T_j^(φ) = N_j · p_j + Ĉ_j^(φ) − N_j · c̄

The adjusted loss ratio is:

> LR_j^*(φ) = C_j / R_j^*(φ) = C_j / (N_j · p_j + T_j^(φ))             (4)

---

## 5. The Combined Ratio

### 5.1 Definition and Components

The *loss ratio* captures the claims side of insurer finances, but a complete picture of solvency requires accounting for operating expenses as well. The *combined ratio* (CR) is defined as:

> CR_j = LR_j + ER_j

where the *expense ratio* ER_j is the ratio of total administrative and processing costs to effective revenue. The CR is the standard measure of underwriting performance in insurance: CR_j < 1 implies that the insurer earns an underwriting profit (revenue covers both claims and expenses); CR_j > 1 implies an underwriting loss.

Operating expenses have two components that differ in how they interact with the RA:

**Fixed component (e_F · N_j)**: Costs that scale with the number of enrollees but not with their risk — member services, IT infrastructure, reserve management, actuarial and regulatory compliance. Let e_F denote the fixed administrative cost per enrollee per year (calibrated to approximately CHF 280 in the Swiss system, consistent with BAG reporting on administrative loadings).

**Variable component (e_V · C_j)**: Claims adjudication, prior-authorization review, coordination-of-care management, and quality monitoring. These costs scale with the volume and complexity of realized claims; let e_V denote the variable processing rate (approximately 2% of claims in the Swiss context).

Total administrative costs for insurer j:

> A_j = e_F · N_j + e_V · C_j

The expense ratio is then:

> ER_j^*(φ) = A_j / R_j^*(φ) = (e_F · N_j + e_V · C_j) / R_j^*(φ)

Substituting C_j = LR_j^*(φ) · R_j^*(φ):

> ER_j^*(φ) = e_F · N_j / R_j^*(φ) + e_V · LR_j^*(φ)

This decomposition reveals two channels through which the RA influences the expense ratio.

### 5.2 How Risikoausgleich Affects the Expense Ratio

**Channel 1 — Denominator effect on the fixed component**: The RA augments the effective revenue R_j^*(φ) of high-risk insurers and reduces it for low-risk insurers. For a high-risk insurer (T_j > 0), R_j^*(φ) = R_j + T_j > R_j, so:

> e_F · N_j / R_j^*(φ) < e_F · N_j / R_j

The same fixed overhead is spread over a larger revenue base, reducing the fixed-component expense ratio. This is a *double dividend* of the RA for high-risk pools: it directly reduces LR by augmenting revenue, and it indirectly reduces the ER by diluting the fixed cost loading.

For a low-risk insurer (T_j < 0), the opposite holds: the fixed-component expense ratio increases, because the same overhead is spread over a smaller revenue base.

**Channel 2 — Variable component scales with LR**: Since the variable component e_V · LR_j^*(φ) scales directly with the loss ratio, any improvement in LR from better RA also mechanically reduces the variable expense load. High-risk pools, whose LR falls most from RA, benefit disproportionately on this channel too.

**Net effect on the CR**: Combining the two channels, better RA (higher φ) reduces both LR and ER for high-risk pools and increases both for low-risk pools — the RA simultaneously equalizes claims exposure and administrative cost pressure across the insurer landscape. The combined ratio variance is:

> Var_j(CR_j^*) = Var_j(LR_j^*) + Var_j(ER_j^*) + 2 · Cov_j(LR_j^*, ER_j^*)

Since LR and ER move in the same direction for a given pool (both are increasing functions of the pool's risk relative to the formula's coverage), Cov_j(LR, ER) > 0. This means the CR SD exceeds the LR SD in the absence of RA. However, as RA quality improves, the covariance shrinks alongside the individual variances, so the CR benefits at least as much as the LR from successive RA reforms.

### 5.3 Premium Setting with Expense Loading

Under community rating with expense loading, the regulated premium must cover both expected claims and expected administrative costs:

> p_j = (c̄_j^e + e_F) / (1 − e_V)

In a fully community-rated system, p_j = p̄ for all j, where p̄ is set at the system-wide average:

> p̄ = (c̄ + e_F) / (1 − e_V)

Under this premium setting, the breakeven combined ratio at the system level is exactly 1.0 by construction. Departures of individual insurer CRs from 1.0 reflect risk-pool heterogeneity (driving LR dispersion) and the secondary expense ratio effects described above.

---

## 6. Analytical Results

### 6.1 Proposition 1: Perfect Risk Adjustment Equalizes Loss Ratios

**Proposition 1 (Perfect RA)**: Suppose β̂^(φ) = β (the formula perfectly predicts expected costs) and ε_i are i.i.d. across individuals. Then, for large N_j, the adjusted loss ratio converges:

> LR_j^*(φ) →^p 1   for all j as N_j → ∞

**Proof sketch**: Under perfect adjustment, T_j^(φ) = Σ_{i ∈ j} **β**·**x_i** − N_j · c̄. The adjusted revenue is R_j^*(φ) = N_j · p_j + Σ_{i ∈ j} **β**·**x_i** − N_j · c̄ = N_j · (p_j − c̄) + Σ_{i ∈ j} **β**·**x_i**. The realized cost is C_j = Σ_{i ∈ j} **β**·**x_i** + Σ_{i ∈ j} ε_i. By the law of large numbers, (1/N_j) Σ_{i ∈ j} ε_i → 0. The loss ratio becomes C_j / R_j^*(φ) → (Σ_{i ∈ j} **β**·**x_i**) / (Σ_{i ∈ j} **β**·**x_i** + N_j(p_j − c̄)), which equals 1 when p_j = c̄. □

The proposition confirms the intuition: if premiums are set at the system average and the RA formula perfectly predicts cost differences across pools, then each insurer recovers exactly its expected costs. The loss ratio variance is driven entirely by the unpredictable ε_i terms, which diversify away as pool size increases.

### 6.2 Proposition 2: Imperfect RA and Residual Loss Ratio Variance

**Proposition 2 (Imperfect RA)**: Suppose β̂^(φ) ≠ β (the formula uses an incomplete set of predictors, so ĉ_i^(φ) = **β̂^(φ)**·**x_i^(φ)** omits the components of **x_i** not included in phase φ). Define the omitted component as:

> δ_i^(φ) = (**β** − **β̂^(φ)**_extended)·**x_i** ≡ the "uncompensated cost" due to morbidity not captured in phase φ

Then the adjusted loss ratio for insurer j satisfies:

> Var_j(E[LR_j^*(φ)]) = Var_j( (1/N_j) Σ_{i ∈ j} δ_i^(φ) ) / (p_j)²

The variance of the adjusted loss ratio across insurers is proportional to the cross-insurer variance of the *average omitted cost* δ_i^(φ) in each pool. Specifically:

> Var_j(LR_j^*) = σ²_δ^(φ) · (1 + corr^(φ)_adverse) / p̄²

where σ²_δ^(φ) = Var(δ_i^(φ)) is the individual-level variance of the uncompensated cost under phase φ, and corr^(φ)_adverse measures the correlation between δ_i^(φ) and enrollment allocation (adverse selection loading: if high-δ individuals are concentrated in certain insurers, this amplifies loss ratio dispersion).

**Corollary (RA Phase Ordering)**: Since Phase 3 includes more predictors than Phase 2, which includes more than Phase 1:

> σ²_δ^(1) > σ²_δ^(2) > σ²_δ^(3)

and therefore:

> Var_j(LR_j^*(1)) > Var_j(LR_j^*(2)) > Var_j(LR_j^*(3))

Each successive RA reform reduces the variance of loss ratios across insurers by reducing the uncompensated cost variance. The proportional reduction in loss ratio variance as we move from Phase 1 to Phase 3 is bounded above by the improvement in R² of the cost prediction model (from ~10–15% in Phase 1 to ~25–35% in Phase 3), but is amplified if high-δ individuals are systematically concentrated in particular insurers.

### 6.3 Proposition 3: Solvency Buffer and Capital Requirements

**Proposition 3 (Solvency Capital)**: Define the solvency constraint for insurer j as the requirement that the probability of LR_j^*(φ) > 1 + τ does not exceed threshold α (a regulatory insolvency probability limit). The minimum required capital buffer κ_j^(φ) satisfies:

> κ_j^(φ) = z_α · σ_{LR}^(φ) · p̄

where z_α is the α-quantile of the standard normal distribution, σ_{LR}^(φ) is the standard deviation of the loss ratio under phase φ (for insurer j), and p̄ is the average premium.

**Implications**:
1. Under Phase 1 (high σ_{LR}^(1)), the required capital buffer is large, particularly for insurers with high-morbidity pools whose residual δ_i variance is large.
2. Under Phase 3 (low σ_{LR}^(3)), the required buffer is substantially lower for the same pool composition.
3. The reduction in required capital from Phase 1 to Phase 3 is:
   > Δκ_j = z_α · p̄ · (σ_{LR}^(1) − σ_{LR}^(3))

This reduction in capital requirements has a direct economic value: capital held as solvency buffer earns a below-market return (it must be held in highly liquid, low-yield instruments). Reducing the required buffer frees up capital for premium reductions or reserve distributions.

---

## 7. Adverse Selection Equilibrium

### 7.1 Insurer Incentives Without RA

Without Risikoausgleich, each insurer's expected profit per enrolled individual is:

> π_j = p_j − E[c_i | i ∈ j] = p_j − c̄_j

Assuming competition drives p_j toward an equilibrium premium that reflects the insurer's anticipated pool composition, each insurer has an incentive to enroll low-expected-cost individuals and deter high-expected-cost individuals. Denote the cost-type of individual i by τ_i = **β**·**x_i** (the predictable component). An insurer that can segment on τ_i — through plan design, network restrictions, or selective marketing — maximizes profit per member by attracting low-τ_i individuals.

**Selection index**: Following Van de Ven and Ellis (2000), define the selection profit margin for individual i under phase-φ RA as:

> m_i^(φ) = c̄_j^actual − ĉ_i^(φ)

where c̄_j^actual is the actual per-capita cost of insurer j's pool and ĉ_i^(φ) is what insurer j would receive as RA compensation for individual i. Individual i is "profitable" if m_i^(φ) < 0 (the RA compensates less than the actual cost differential) and "unprofitable" if m_i^(φ) > 0. The RA under phase φ neutralizes selection incentives for individuals whose cost is fully captured by the phase-φ predictors, but preserves incentives for the residual δ_i^(φ) component.

### 7.2 Equilibrium with Imperfect RA

With adverse selection and imperfect RA, the equilibrium allocation of individuals across insurers is characterized by sorting on δ_i^(φ) — the uncompensated cost component. In a competitive equilibrium with free insurer entry and no barriers to risk selection (e.g., no mandatory acceptance enforcement), high-δ_i individuals will be concentrated in a subset of "high-risk" insurers (those that attract them due to better service for chronically ill patients, or because other insurers successfully deter them), and low-δ_i individuals in "low-risk" insurers.

In this equilibrium, the cross-insurer variance of average δ_i^(φ) is not just σ²_δ^(φ) / N_j (the diversification term from Proposition 2) but also includes the systematic sorting component corr^(φ)_adverse. Better risk adjustment (lower σ²_δ^(φ)) reduces both the individual-level uncompensated variance and — by reducing the margin available from selection — the equilibrium degree of sorting.

---

## 8. Calibration to Swiss Data

### 8.1 Parameter Values

The following parameters are calibrated to publicly available Swiss data from the BAG and Santésuisse:

**Mean per-capita costs** (approximate annual figures, 2022):
- Population-wide average: CHF 4,800 per year
- Children (0–17): CHF 1,200
- Young adults (18–25): CHF 1,800
- Adults (26–64): CHF 3,800
- Elderly (65+): CHF 9,000

**Cost ratios by characteristic** (relative to adult baseline):
- Hospital admission in prior year: approximately 4× baseline cost in the following year
- PCG groups: range from 1.5× (mild conditions) to 6× (transplant, cancer on biologics)

**Variance decomposition**:
- Total individual cost variance: approximately CHF² 40,000,000 (standard deviation ~CHF 6,300)
- Predicted by Phase 1 (age/sex): approximately 12–15% of variance
- Predicted by Phase 2 (age/sex + hospital): approximately 20–22% of variance
- Predicted by Phase 3 (age/sex + hospital + PCG): approximately 28–33% of variance
- Residual (ε_i): approximately 67–72% in Phase 3

**PCG prevalence**: approximately 15–20% of the adult population is assigned to at least one PCG group; the largest groups are cardiovascular medications (~7%), diabetes (~4%), and respiratory disease (~3%).

### 8.2 Loss Ratio Implications

Under the calibration above, the cross-insurer standard deviation of loss ratios in Phase 1 (before RA) depends heavily on the degree of adverse selection. Under random pool assignment (no adverse selection), the loss ratio standard deviation for a pool of N = 30,000 individuals is approximately:

> σ_{LR}^random = σ_ε / (p̄ · √N) ≈ 6,300 / (4,800 · √30,000) ≈ 0.008

This is small by construction — diversification nearly eliminates idiosyncratic risk. The operative dispersion arises from the systematic component: if adverse selection concentrates individuals with average δ_i ≈ CHF 1,200 (one standard deviation of the uncompensated morbidity component) in certain insurers, the between-insurer loss ratio dispersion is approximately:

> σ_{LR}^systematic ≈ σ_δ / p̄ ≈ 1,200 / 4,800 = 0.25

This 25-percentage-point standard deviation in loss ratios represents a substantial solvency exposure. Insurers at the 95th percentile of the loss ratio distribution would face loss ratios of approximately 1.41 — implying that for every CHF 1.00 of premium revenue, they incur CHF 1.41 in claims, requiring a 41% capital buffer to survive a one-standard-deviation adverse realization.

Phase 3 reduces σ_δ by capturing approximately 60–70% of the systematic morbidity variation (the improvement from 15% to 30% R² corresponds to roughly this share of the systematic component). The loss ratio standard deviation under Phase 3 is approximately:

> σ_{LR}^Phase3 ≈ σ_δ^(3) / p̄ ≈ 0.30 × 1,200 / 4,800 = 0.075

This represents a reduction in loss ratio standard deviation from ~0.25 to ~0.075, a factor of three improvement. The required solvency buffer (at 95% confidence) falls from approximately CHF 1.41 per CHF 1.00 of premium to approximately CHF 1.12 — a substantial reduction in required capital.

### 8.3 Combined Ratio Implications

Including the expense ratio, the combined ratio adds a further dimension to the solvency picture. With calibrated parameters (e_F = CHF 280 per enrollee, e_V = 2% of claims) and a system-average premium that includes an administrative loading, the expected expense ratio at the system level is approximately 7.3% — i.e., CHF 7.30 per CHF 100 of premium covers administrative costs. The breakeven combined ratio is exactly 1.0 by construction of the premium.

The interaction between RA and the combined ratio has two important implications. First, the combined ratio *variance* across insurers exceeds the loss ratio variance in the absence of RA, because both components rise together for high-risk pools (positive LR–ER covariance). This means that ignoring the expense ratio understates the dispersion of financial outcomes before RA. Second, as RA quality improves, the reduction in CR variance is approximately proportional to the reduction in LR variance: both are driven by the same denominator equalization. The fixed expense component contributes a residual level to the CR (approximately 280/p̄ ≈ 5.4% of premium) that is approximately equal across all insurers regardless of phase, while the variable component tracks the LR improvement.

---

## 9. Discussion and Limitations

The model delivers three clear results. First, under perfect risk adjustment, loss ratios are equalized across insurers (Proposition 1). Second, imperfect adjustment leaves a residual loss ratio variance proportional to the unexplained cost variance (Proposition 2). Third, each successive RA reform reduces the required solvency buffer by reducing this residual variance (Proposition 3). These results hold under the assumption of a competitive market with no strategic insurer responses.

Several limitations of the model warrant acknowledgment.

**Endogeneity of cost reporting**: The RA formula under Phase 3 uses pharmaceutical consumption as a morbidity proxy. If insurers or providers respond to the formula by influencing PCG assignment (over-prescribing in PCG-eligible categories, or conversely under-reporting to manipulate competitor assessments), the formula no longer identifies genuine morbidity differences. The model treats **x_i** as exogenous, which is appropriate as a first-pass analysis but should be relaxed in a full strategic model.

**Dynamic adverse selection**: The model is static. In a dynamic setting, insurers learn which individuals have high δ_i and can design plan features to deter or attract them across enrollment periods. The RA formula's effectiveness may erode over time as insurers develop more refined selection tools — consistent with Beck et al.'s (2010) finding that the Phase 1 formula lost effectiveness over its 15-year lifespan.

**Premium heterogeneity**: The model assumes all insurers charge the same premium (p_j = p̄). In reality, premiums vary substantially across insurers within a canton. If healthier individuals choose lower-premium insurers, the premium itself becomes a selection mechanism, and the RA must account not only for risk differentials but also for premium differentials. This is the managed-care premium differentiation problem analyzed by Glazer and McGuire (2000), which is outside the scope of the current model.

**Non-linearity of costs**: The linear cost model c_i = **β**·**x_i** + ε_i is a convenient approximation, but healthcare costs are highly right-skewed. The top 1% of spenders account for approximately 30% of total OKP costs. A log-linear or two-part model (probability of any use × conditional cost) would be more realistic but would complicate the analytical derivation of loss ratio distributions. The simulation in Chapter 5 uses a more realistic cost distribution to address this limitation.
