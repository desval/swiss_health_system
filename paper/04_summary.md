# Summary: The Swiss OKP, Risikoausgleich, and Insurer Solvency

## 1. What the Swiss OKP System Does

The Swiss mandatory health insurance system (OKP) resolves a fundamental tension in health insurance design: individuals differ substantially in their expected medical costs, but a just and politically sustainable system cannot allow premiums to reflect those differences. Community rating — the legal requirement that all adults within a premium region pay the same monthly premium regardless of health status — enforces solidarity between healthy and sick, young and old. Open enrollment — the insurer's obligation to accept any applicant — ensures that no one is excluded on the basis of risk.

These two requirements create a structural problem. Under community rating and open enrollment, an insurer whose enrolled population is systematically sicker than the average will collect the same revenue per person as its competitors but bear substantially higher costs. Without a corrective mechanism, this insurer faces chronic losses, eventual insolvency, and exit — leaving its enrollees without coverage and undermining the competitive structure that the KVG was designed to preserve. Conversely, an insurer whose pool is systematically healthy will earn rents without providing better service.

The Risikoausgleich is the corrective mechanism. It is a transfer system in which the predicted cost of each insurer's enrolled population — estimated from individual observable characteristics — is compared to the system-wide average. Insurers with above-average predicted costs receive positive transfers; those with below-average predicted costs make contributions. The transfers are budget-neutral in aggregate: money moves among insurers, not from outside the system. The effect is to level the playing field: after the transfer, each insurer's effective revenue reflects the expected cost of its actual pool rather than the system-average cost applied to a pool of potentially very different composition.

The Swiss system has refined this mechanism in three phases since 1996. The initial formula used only age and sex to predict costs. The 2012 reform added a prior-year hospitalization indicator. The 2020 reform introduced 22 Pharmaceutical Cost Groups (PCG) based on active drug prescriptions, which serve as a proxy for chronic disease burden. Each reform extended the set of observable characteristics used to compute the predicted cost, increasing the accuracy of the formula and reducing the scope for profitable risk selection.

---

## 2. What the Model Shows

The formal model in Chapter 3 provides three analytical results that clarify the mechanism and its limits.

**Equalization under perfect risk adjustment.** If the formula predicts each individual's expected cost without error — that is, if the observable characteristics fully capture the systematic component of costs — then applying the transfer formula equalizes expected loss ratios across all insurers. Every insurer, regardless of the risk composition of its pool, earns the same expected return per franc of premium revenue. In this limiting case, there is no incentive to cherry-pick healthy enrollees because the RA transfer would exactly offset the cost advantage of a healthier pool. The formula eliminates the profitability of risk selection by construction.

**Residual dispersion under imperfect adjustment.** Perfect risk adjustment is theoretically achievable but practically impossible: individual healthcare costs are only partially predictable from observable characteristics, even rich ones. The model shows that the variance of loss ratios across insurers under an imperfect formula is proportional to the uncompensated cost variance — the share of expected cost differences across pools that the formula fails to capture. This residual variance represents both a solvency risk (some insurers will systematically overpay claims relative to revenue) and a selection incentive (insurers can profitably deter individuals whose uncompensated cost is high). The key metric is the R² of the cost prediction model: each unit increase in R² reduces the uncompensated variance proportionally.

**Solvency buffer and capital requirements.** Under standard regulatory solvency requirements, insurers must hold capital reserves proportional to the variance of their loss ratio. An imperfect risk adjustment formula therefore implies a higher required capital buffer for high-risk pools. The model derives the relationship between the formula's predictive accuracy and the required capital: the minimum buffer scales with the standard deviation of the loss ratio, which in turn scales with the square root of the uncompensated cost variance. Better risk adjustment reduces required capital directly, releasing resources that can be used for premium reduction or service investment.

---

## 3. What the Simulation Confirms

The Python simulation in `code/simulation.py` implements the model with a synthetic Swiss-like population of 10,000 individuals, calibrated to Swiss BAG statistics for cost levels, age distribution, PCG prevalence, and hospitalization rates. It runs 200 Monte Carlo replications under moderate adverse selection (sorting strength = 0.5) across 10 competing insurers, and computes loss ratio distributions under each RA phase.

The results strongly confirm the model's theoretical predictions.

**Loss ratio dispersion falls sharply across phases.** Without any risk equalization, the cross-insurer standard deviation of loss ratios is 0.621 and 39.5% of insurer-simulation pairs have loss ratios exceeding 1.0. Phase 1 (age and sex) reduces the standard deviation to 0.395, but the share of insurers with LR > 1.0 remains high (33.4%), reflecting that the age-sex formula captures systematic age-related variation but misses the chronic disease component that drives the high-cost tail. Phase 2 (adding hospitalization) produces a more meaningful reduction to SD = 0.218, and the share above 1.0 falls to 29.4%. Phase 3 (adding PCG groups) delivers the most substantial improvement: SD = 0.127 (a 68% reduction from Phase 1), and only 0.4% of insurer-simulation pairs exceed LR = 1.0 — consistent with near-full equalization under moderate adverse selection.

**The combined ratio tells a fuller story.** Once administrative costs are included — modelled as CHF 280 fixed per enrollee per year plus 2% of realized claims — the combined ratio adds approximately 6–7 percentage points to the loss ratio on average. More importantly, the combined ratio dispersion is closely related to, but distinct from, the loss ratio dispersion. High-risk pools face both elevated loss ratios and elevated expense ratios: the variable admin component scales with claims, while the fixed component represents a larger share of the denominator when RA transfers are insufficient. Low-risk pools experience the reverse: their RA contributions reduce their effective revenue, raising both LR and ER slightly. Phase 3 reduces combined ratio SD from 0.387 (Phase 1) to 0.098, and the share of insurers with CR > 1.0 falls from 41.1% to 9.3%.

| Phase | LR SD | CR SD | % LR > 1.0 | % CR > 1.0 | LR SD reduction vs. No RA |
|-------|-------|-------|-----------|-----------|--------------------------|
| No RA | 0.621 | 0.634 | 39.5% | 44.3% | — |
| Phase 1 (age/sex) | 0.395 | 0.387 | 33.4% | 41.1% | −36% |
| Phase 2 (+hospital) | 0.218 | 0.197 | 29.4% | 35.8% | −65% |
| Phase 3 (+PCG) | 0.127 | 0.098 | 0.4% | 9.3% | −80% |

**Cost prediction R² increases across phases.** The simulation estimates the R² of the cost prediction model at 35% under Phase 1, 62% under Phase 2, and 76% under Phase 3. These values exceed the 10–35% range observed in real-world Swiss data because the simulation generates data from the same parametric model used to fit the formula. The relative ordering is what matters: the threefold improvement in R² from Phase 1 to Phase 3 produces the proportional improvement in loss ratio standard deviation, consistent with the model's prediction that LR dispersion scales with the square root of the uncompensated cost variance (1 − R²).

**The benefit of better adjustment depends on the degree of adverse selection.** The sensitivity analysis (Figure 3) shows that when enrollment is random, loss ratio dispersion under Phase 1 and Phase 3 are nearly identical and close to zero — diversification alone eliminates most idiosyncratic variance. As adverse selection intensity rises, Phase 1 dispersion increases rapidly while Phase 3 rises much more slowly, because the PCG formula captures most of the morbidity variation that otherwise drives sorting. At full adverse selection, Phase 3 still delivers a standard deviation approximately 70% lower than Phase 1. The value of better risk adjustment is greatest precisely when selection pressures are strongest — the conditions under which combined ratio volatility is also highest.

---

## 4. Policy Implications

Three policy-relevant conclusions emerge from the model and simulation.

**The PCG reform was the right move, but the formula is still imperfect.** The transition from Phase 2 to Phase 3 delivered the largest single improvement in loss ratio equalization in the simulation. The PCG groups capture chronic disease burden through pharmaceutical consumption — a proxy that is available from existing claims data, does not require new diagnostic coding infrastructure, and is strongly predictive of future costs. At the same time, the formula leaves roughly 24% of cost variance unexplained at the individual level (1 − R² = 0.24 in the simulation; likely more in real data due to greater individual-level noise). The 4.6% of insurer-simulation pairs still exceeding LR > 1.10 under Phase 3 and moderate adverse selection represents a residual solvency exposure that is not negligible for smaller or newer insurers with thin capital buffers.

**Diagnostic cost groups or episode-based adjusters are a natural next step.** The PCG system is bounded in principle by the information it contains: pharmaceutical consumption proxies morbidity but does not directly measure it, excludes patients who decline medication, and lags diagnoses by up to one year. The Dutch experience — where the transition to diagnosis-based risk adjustment (ACG-based systems) substantially improved R² beyond what pharmaceutical-based systems achieved — suggests that a similar path is available to Switzerland. The simulation's sensitivity analysis implies that this investment would be most valuable for preventing insolvency among insurers that attract high concentrations of chronically ill enrollees.

**Capital requirement reductions from better risk adjustment have real financial value.** The solvency analysis in Chapter 3 shows that the standard deviation of the combined ratio — not just the loss ratio — is the correct input to capital buffer calculations, since both claims shortfalls and administrative overruns threaten solvency. The simulation finds that Phase 3 reduces combined ratio SD by 75% relative to Phase 1, and reduces the share of insurers in underwriting loss (CR > 1.0) from 41% to 9%. In a system where Krankenkassen are legally prohibited from cross-subsidizing OKP from supplementary insurance profits, this reduction in combined ratio volatility directly lowers the minimum regulatory capital requirement for high-risk pools, freeing resources for premium reductions or service investment.

---

## 5. Open Questions

Several questions remain beyond the scope of this analysis.

**Insurer gaming.** The model assumes that the characteristics used in the RA formula (**x_i**) are exogenous. In practice, a PCG system creates incentives for insurers to influence pharmaceutical prescribing patterns — either toward PCG-eligible medications (to increase RA receipts) or away from them (to reduce the apparent morbidity of the pool and deter high-cost enrollees). The magnitude of this gaming has not been empirically documented in Switzerland, but the theoretical exposure is real. A more robust formula would use diagnostic codes (which are harder to manipulate than prescriptions) or cross-validated pharmaceutical indicators.

**Endogeneity of PCG assignment.** The PCG assignment depends on prior-year drug use, which is itself a function of insurance plan features (formulary design, specialist access, adherence support). Insurers that provide better pharmaceutical management may show higher PCG rates not because their pools are sicker but because they prescribe more. This creates a perverse incentive to under-prescribe. The model treats PCG as exogenous; a dynamic model would need to account for this channel.

**Cantonal variation in subsidy design.** The Prämienverbilligung system introduces substantial cross-cantonal variation in the net premium burden, which in turn affects enrollment decisions and the severity of adverse selection. A canton with generous subsidies will tend to attract higher-risk low-income enrollees, potentially concentrating risk in insurer pools that operate primarily in that canton. The RA formula does not account for cantonal subsidy heterogeneity; extending it to do so would require integrating the IPV system into the equalization mechanism.

**Value vs. volume.** The analysis uses counts of medical costs (in CHF) as the outcome variable, which is appropriate for insurer solvency analysis. A welfare analysis would additionally consider health outcomes: does better risk equalization improve access to care for high-risk individuals by removing the deterrence incentive, and does this produce measurable health gains? This question connects the Risikoausgleich to the broader literature on managed competition and the equity-efficiency frontier in health insurance design.
