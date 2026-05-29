# Questions and Analytical Notes

This chapter collects conceptual questions about the Swiss OKP system and the Risikoausgleich, with detailed answers. Each question is addressed in the context of the formal model (Chapter 3) and the simulation (Chapter 5). New questions should be added here as they arise.

---

## Q1. Is the Risikoausgleich designed to prevent selection of profitable customers — or to make all customers equally unprofitable?

**Short answer:** Neither exactly. The RA is designed to make all customers *equally* profitable — specifically, to drive the expected profit margin on every individual toward zero, regardless of their health status. It does not make profitable customers unprofitable; it eliminates the distinction between the two.

---

**The problem without RA**

Under community rating, all adults in the same premium region pay the same monthly premium p̄, regardless of how much they are expected to cost the insurer. This creates a simple profitability calculation for the insurer:

> expected profit per individual i = p̄ − E[c_i | **x_i**]

An individual whose expected cost is below the system average (E[c_i] < p̄) generates a positive expected profit — they are a "profitable customer." An individual whose expected cost is above the system average (E[c_i] > p̄) generates an expected loss — they are an "unprofitable customer."

The premium is set at the system-wide average cost, so profitable and unprofitable customers balance out *across the whole market*. But they do not balance out for any individual insurer whose pool is not representative. An insurer that manages to attract only low-expected-cost individuals earns systematic profits; an insurer that ends up with a high-expected-cost pool sustains systematic losses. The incentive to select profitable customers — sometimes called *cream-skimming* — is therefore a direct consequence of community rating without risk equalization.

---

**What the RA does to the profitability calculation**

The RA adds a transfer to the insurer's revenue that depends on the predicted cost of each enrolled individual. For individual i enrolled with insurer j, the per-capita RA compensation under phase φ is:

> t_i^(φ) = ĉ_i^(φ) − c̄^(φ)

where ĉ_i^(φ) is the predicted cost for individual i under the phase-φ formula and c̄^(φ) is the system-wide average predicted cost. The effective revenue attributed to individual i is then:

> r_i^(φ) = p̄ + t_i^(φ) = p̄ + ĉ_i^(φ) − c̄^(φ)

The expected profit from enrolling individual i becomes:

> E[profit per i] = r_i^(φ) − E[c_i] = p̄ + ĉ_i^(φ) − c̄^(φ) − E[c_i]

Under perfect risk adjustment (ĉ_i^(φ) = E[c_i] and c̄^(φ) = p̄), this simplifies to:

> E[profit per i] = p̄ + E[c_i] − p̄ − E[c_i] = 0

Every individual generates zero expected profit, regardless of their health status. The distinction between profitable and unprofitable customers has been completely eliminated. Enrolling a diabetic patient or a post-transplant patient generates the same expected profit as enrolling a healthy young adult — zero — because the RA exactly compensates for the cost difference.

---

**The key implication: RA targets the selection margin, not the absolute profit level**

The RA does not make previously-profitable customers unprofitable. A healthy young adult who previously generated a large profit surplus for a low-risk insurer now generates zero expected profit — but so does the previously-unprofitable sick elderly patient. Both are equalized at zero. The previously-profitable individual has their "premium surplus" effectively redirected: the insurer pays it into the RA pool as a negative transfer for that individual's below-average predicted cost, and that money flows to insurers with above-average predicted cost pools.

This is the mechanism by which the RA achieves its goal: not by punishing the profitable customers, but by ensuring that the revenue attributed to any individual tracks their expected cost closely enough that no individual is systematically more attractive than another. A perfectly calibrated RA makes cherry-picking a financially neutral activity — there is nothing to be gained by selecting low-risk individuals because the RA would require a corresponding reduction in transfer income.

---

**Why imperfect RA still leaves some selection incentives**

In practice, ĉ_i^(φ) ≠ E[c_i] because the formula omits some predictive characteristics. Define the residual selection profit margin for individual i under phase φ as:

> m_i^(φ) = ĉ_i^(φ) − E[c_i] = −δ_i^(φ)

where δ_i^(φ) = E[c_i] − ĉ_i^(φ) is the uncompensated cost component (see Appendix A.6). An individual with positive δ_i^(φ) (their true expected cost exceeds the formula's prediction) remains unprofitable: the insurer is not fully compensated for their expected cost. An individual with negative δ_i^(φ) (their true expected cost is below the formula's prediction) remains profitable: the insurer receives more in RA transfer than the individual is expected to cost.

The magnitude of these residual selection margins is directly proportional to the uncompensated cost variance σ²_δ^(φ). As discussed in Section 6.2 of Chapter 3, each successive RA phase reduces σ²_δ^(φ) — but never to zero. Some individuals will always have expected costs that the formula over- or under-predicts, and those prediction errors define the residual population of profitable and unprofitable customers.

---

**Practical implications for Swiss insurers**

Under Phase 3 (PCG-based RA), the residual selection margins are substantially smaller than under Phase 1. The profitable/unprofitable distinction has been largely — but not completely — neutralized. The remaining profitable customers are those whose expected costs are systematically below their PCG-predicted level (e.g., individuals assigned to a PCG group who manage their condition with low pharmaceutical consumption and few hospitalizations). The remaining unprofitable customers are those whose expected costs exceed their PCG-predicted level (e.g., rare disease patients not captured in any PCG group, or patients with complex multimorbidity spanning multiple PCG groups where the formula under-predicts total costs).

This residual structure explains why Swiss insurers continue to invest in plan design and service network optimization that — intentionally or not — tends to deter the high-δ_i individuals. It is not that the RA has failed; it is that no formula based on observable proxies can perfectly predict individual costs, and the residual unpredictability always leaves some selection margin for insurers to exploit.

---

**Summary**

| Scenario | Profitable customers? | Unprofitable customers? | Selection incentive? |
|----------|----------------------|------------------------|----------------------|
| No RA | Yes (low-cost individuals) | Yes (high-cost individuals) | Strong |
| Perfect RA | None *in expectation* | None *in expectation* | None *in expectation* |
| Imperfect RA (Phase 1) | Yes (low-δ individuals) | Yes (high-δ individuals) | Moderate–strong |
| Imperfect RA (Phase 3) | Yes, but smaller margin | Yes, but smaller margin | Weak–moderate |

The RA does not destroy the concept of a profitable customer — it destroys it *in expectation* only. Realized costs deviate from expected costs in every year due to the individual noise term ε_i, so some individuals will always be profitable or loss-making ex-post, purely from random variation. What perfect RA eliminates is *systematic* profitability: the ability to predict in advance, based on observable characteristics, which individuals will be profitable to enroll. An insurer can no longer look at a healthy 30-year-old and know they will generate a surplus — the RA transfer removes that surplus in expectation. But they cannot know whether that individual will happen to have an expensive year regardless. Imperfect RA (all real phases) additionally leaves residual *systematic* profitability among individuals with large uncompensated cost components δ_i. The historical progression from Phase 1 to Phase 3 progressively eliminates the systematic part, while the unsystematic (noise-driven) part is irreducible.

---

---

## Q2. To find profitable customers, do insurers need to identify characteristics that end up in the RA model's error term and predict lower realized costs?

**Short answer:** Yes. Under imperfect RA, a profitable customer is precisely one whose true expected cost falls below the formula's prediction — meaning the insurer is over-compensated for them. Finding profitable customers therefore means finding characteristics that predict lower costs *within* the RA cells the formula already defines. This is called within-cell selection.

---

**The formal condition for profitability**

Recall from Q1 that the expected profit from enrolling individual i is:

> E[profit per i] = −δ_i^(φ) = ĉ_i^(φ) − E[c_i]

Individual i is profitable if and only if δ_i^(φ) < 0 — that is, if the formula *over-predicts* their expected cost. The insurer receives more in RA transfer than the individual is expected to cost. Conversely, an individual is unprofitable when δ_i^(φ) > 0: the formula under-predicts their cost, and the RA transfer falls short of covering expected claims.

This means profitable customers are not simply low-cost individuals — they are individuals whose true expected cost is low *relative to what the formula assumes for people who look like them*. An elderly patient could be profitable if the elderly-cell average in the formula exceeds their personal expected cost. A PCG-positive patient could be profitable if their drug-class average overstates their actual chronic disease burden.

---

**Within-cell selection**

The key insight is that an insurer does not need to find characteristics the RA formula ignores entirely. It needs to find characteristics that predict cost *below the cell mean* — within the groups the formula already uses. This is called **within-cell selection**.

Each RA risk cell is defined by a combination of observable characteristics — age, sex, hospitalization, PCG membership — and is compensated at the *average cost* for everyone in that cell. But within each cell there is always residual cost variation. Some individuals cost far less than the cell average; others far more. The formula cannot distinguish them because it only observes the cell-defining characteristics.

An insurer that can identify the low-cost members within each cell — and attract them preferentially — earns the difference between the cell-average RA compensation and the individual's actual lower expected cost. It is over-compensated on a systematic basis without ever needing to refuse enrollment or engage in overt discrimination.

---

**Concrete examples across phases**

**Phase 1 (age/sex only):** The elderly risk cell (say, age 65–70) is compensated at the average cost of all 65–70 year-olds — a mix of healthy retirees and patients with multiple chronic conditions. An insurer that attracts the healthy end of this group through active-lifestyle marketing (gym membership discounts, hiking club partnerships, sports facility networks) is over-compensated for every healthy 68-year-old it enrolls, because the RA treats them identically to a 68-year-old with diabetes, COPD, and heart failure.

**Phase 2 (age/sex + hospitalization):** Adding the hospital stay indicator creates finer cells — the formula now distinguishes recently hospitalized from non-hospitalized individuals. But within the "recently hospitalized" cell, there is still wide variation: a patient hospitalized for an elective knee replacement has a very different cost trajectory than one hospitalized for a first acute myocardial infarction. An insurer with a network that appeals to elective-surgery patients (high quality orthopedic care, fast access) will over-represent the low-cost end of the hospitalized cell.

**Phase 3 (PCG groups):** The cardiovascular PCG group is compensated at the average cost of all patients on cardiovascular medication. But within that group, a 55-year-old recently started on a preventive statin costs far less than a 72-year-old with advanced heart failure on multiple agents. If an insurer's network, plan design, or communication style appeals more to the "well-managed, low-severity" end of each PCG group, it systematically attracts the profitable within-group members. No explicit selection is required — the structure of the formula does the work.

---

**Implications for formula design**

This logic implies that adding more risk cells — improving average R² — does not fully solve the selection problem as long as within-cell cost variation remains large and predictable from non-formula characteristics. Each new cell the formula creates is a new arena for within-cell selection.

The Glazer and McGuire (2000) framework addresses this directly: the optimal RA formula should not maximize aggregate predictive accuracy but should specifically target the *margins on which selection is easiest*. In practice this means assigning higher adjustment weights to services and conditions where (a) within-cell cost variation is large, (b) that variation is predictable from characteristics the insurer can observe but the regulator cannot include in the formula, and (c) the insurer can realistically act on that information through plan design or network choices.

Under this criterion, the Swiss PCG formula — which assigns a single average cost increment per PCG group regardless of severity — is known to leave large within-group selection margins, particularly for PCG groups that span wide severity ranges (cardiovascular, respiratory, musculoskeletal). Proposals to introduce severity sub-groups within PCG classes, or to transition to ACG-style episode-based adjustment, are direct responses to this within-cell selection vulnerability.

---

**The information asymmetry at the heart of selection**

The selection problem is ultimately an information problem. The RA formula is based on characteristics the regulator can observe and verify from administrative data — age, sex, hospitalizations, drug prescriptions. The insurer observes or can infer additional characteristics — lifestyle, social network, health literacy, adherence behavior, employer type, neighborhood — that predict costs within the formula's cells but are outside the regulator's information set.

Selection does not require the insurer to explicitly measure or record these characteristics. Any marketing channel, network design, service offering, or plan feature that correlates with the within-cell cost dimension will produce selection as a side effect. The insurer that builds a network of sports medicine specialists and wellness centers will attract low-cost individuals from every RA cell without ever asking about their health status — and will be systematically over-compensated by a formula that cannot see what kind of person within each cell it has attracted.

*Further questions to be added.*
