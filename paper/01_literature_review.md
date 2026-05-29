# Literature Review: Risk Equalization in Competitive Health Insurance Markets

## Introduction

The Risikoausgleich — Switzerland's risk equalization mechanism — operates at the intersection of three theoretical concerns: the design of regulated insurance markets, the welfare consequences of adverse selection, and the calibration of risk adjustment formulas under incomplete information. The five papers reviewed below collectively establish the theoretical foundations, empirical benchmarks, and welfare criteria against which the Swiss system can be evaluated. They are organized to move from general theory toward the specific Swiss context.

---

## 1. Van de Ven, W.P.M.M., & Ellis, R.P. (2000). "Risk Adjustment in Competitive Health Plan Markets." In A.J. Culyer & J.P. Newhouse (Eds.), *Handbook of Health Economics*, Vol. 1A, pp. 755–845. Elsevier.

### Motivation and Scope

This chapter is the foundational reference for risk adjustment theory in the context of regulated health insurance markets. Van de Ven and Ellis wrote it as the definitive treatment for the first edition of the *Handbook of Health Economics*, and it remains the standard starting point for any analysis of risk equalization design. The paper is not limited to a single country but draws on the experiences of the Netherlands, Germany, Switzerland, and the United States to develop a general framework.

### Methodology

The paper proceeds analytically. It begins by characterizing the equilibrium of a competitive health insurance market under community rating — the institutional constraint that prohibits risk-rated premiums — and derives the conditions under which adverse selection leads to market failure or inefficient sorting. It introduces the taxonomy of selection incentives (cream-skimming, lemon-dropping, and preferred-risk selection) that has since become standard in the literature. It then sets up the risk adjustment problem formally: given a regulator who observes a vector of individual characteristics **x**, what transfer formula minimizes residual selection incentives while respecting the information constraint?

### Main Finding

The paper shows that perfect risk adjustment — in the sense of fully eliminating selection incentives — requires predicting each individual's expected cost with zero error conditional on the observed characteristics. Since this is impossible in practice (individual cost is only partially predictable from observable risk factors), all practical risk adjustment formulas leave residual selection incentives. The paper introduces the concept of *predictive accuracy* — measured by the R² of the risk adjustment regression — as the key metric for evaluating how much of the selection problem a given formula resolves. It also demonstrates that higher R² does not necessarily imply better social welfare if the formula induces insurer moral hazard or gaming.

### Relevance to Risikoausgleich

This paper provides the conceptual vocabulary for evaluating all three phases of the Swiss Risikoausgleich. The transition from Phase 1 (age and sex only) to Phase 2 (plus hospital stays) to Phase 3 (plus PCG groups) can be directly interpreted as successive increases in the R² of the underlying prediction model. Van de Ven and Ellis's framework predicts that each increase in predictive accuracy reduces residual selection incentives — but also raises the question of whether the new predictors (hospital stays, pharmaceutical cost groups) are themselves subject to manipulation by insurers or enrollees.

---

## 2. Beck, K., Trottmann, M., & Zweifel, P. (2010). "Risk Adjustment in Health Insurance and Its Long-Term Effectiveness." *Journal of Health Economics*, 29(4), 489–498.

### Motivation and Scope

This is the most directly relevant empirical paper for the Swiss case. Beck, Trottmann, and Zweifel study the Swiss Risikoausgleich specifically, using data from the period prior to the 2012 reform. Their central question is whether the age-and-sex-based formula introduced in 1996 was achieving its intended purpose — equalizing loss ratios across insurers — and, if not, why it was failing.

### Methodology

The authors construct a panel of Swiss Krankenkassen covering 1996–2005 and estimate the relationship between insurer-level risk profiles and loss ratios, both before and after the application of the Risikoausgleich transfers. They measure the effectiveness of risk adjustment using two metrics: the reduction in cross-insurer variance of loss ratios attributable to the equalization transfer, and the correlation between a predicted cost index (based on the age-sex cells) and realized costs at the insurer level.

### Main Finding

The paper finds that the age-and-sex formula implemented in Phase 1 was substantially ineffective in the long run. While it reduced loss ratio variance in the early years after its introduction, its effectiveness declined over time as insurers learned to exploit the residual selection margins — in particular, by steering healthy enrollees toward low-premium high-deductible plans and deterring sick enrollees through service quality and network design. The paper estimates that only approximately 20–30% of the cross-insurer variation in expected costs was explained by the Phase 1 predictors, leaving the majority of the selection problem unresolved. This result provided much of the empirical motivation for the 2012 reform.

### Relevance to Risikoausgleich

Beck et al. (2010) establishes the empirical baseline against which the subsequent Swiss reforms should be evaluated. Their finding that Phase 1 predicted only 20–30% of cost variance aligns with Van de Ven and Ellis's theoretical prediction that low-R² formulas leave large residual selection incentives. The paper also raises a methodological concern that is directly relevant to any simulation of the Swiss system: insurer behavior is endogenous to the risk adjustment formula, so a static simulation that takes enrollment as given will overestimate the effectiveness of improved adjustment.

---

## 3. Schokkaert, E., & Van de Voorde, C. (2004). "Risk Adjustment and the Fear of Markets: The Case of Belgium." *Health Economics*, 13(9), 851–865.

### Motivation and Scope

Schokkaert and Van de Voorde use the Belgian health insurance system — which, like Switzerland, combines community rating with regulated insurer competition — to analyze the welfare consequences of partial risk adjustment. Their central contribution is to show that the welfare case for risk adjustment is more nuanced than a simple comparison between "adjustment present" and "adjustment absent." The degree, design, and completeness of the formula all matter.

### Methodology

The paper develops a formal model of a regulated insurance market with heterogeneous risk types. Individuals choose among competing insurers that offer differentiated quality; premiums are community-rated. The regulator implements a risk adjustment formula that correctly predicts a fraction θ ∈ [0,1] of expected cost differences. The authors derive equilibrium insurer strategies and welfare outcomes as a function of θ, and characterize the second-best optimal formula — which is not simply to maximize θ but to balance selection reduction against quality competition incentives.

### Main Finding

The paper's headline result is that *partial* risk adjustment — intermediate values of θ — can be welfare-inferior to both zero adjustment and full adjustment. When the formula is imperfect but large in scale, it may over-compensate certain risk groups while leaving others under-compensated, distorting the competitive equilibrium in ways that reduce quality competition without eliminating selection. The intuition is that an imperfect formula creates systematic transfer patterns that some insurers can exploit, while the market-discipline effect of allowing premium differentiation is already suppressed by community rating. Schokkaert and Van de Voorde call this the "fear of markets" problem: the reluctance to let competition operate is not matched by a sufficiently precise equalization instrument, leading to the worst of both worlds.

### Relevance to Risikoausgleich

This paper provides the welfare framework for evaluating Swiss reform sequencing. It implies that the gradual improvement of the Risikoausgleich formula — rather than a one-time move to a comprehensive morbidity-based system — may have passed through phases of reduced welfare during transitions. It also motivates the simulation design: comparing loss ratio distributions across phases is informative, but the full welfare comparison requires accounting for quality competition and insurer gaming, which are suppressed in a partial equilibrium model.

---

## 4. Glazer, J., & McGuire, T.G. (2000). "Optimal Risk Adjustment in Markets with Adverse Selection: An Application to Managed Care." *American Economic Review*, 90(4), 1055–1071.

### Motivation and Scope

Glazer and McGuire derive the optimal risk adjustment formula from first principles, treating the design of transfers as a mechanism design problem. Their paper is more theoretically abstract than the others reviewed here but provides the key normative benchmark: given a social planner who wants to eliminate adverse selection incentives while minimizing distortions in insurer behavior, what formula should be used? Their application to managed care markets in the United States is directly generalizable to the Swiss OKP context.

### Methodology

The model has two types of individuals (high-risk and low-risk), each with multiple medical conditions. Insurers observe a subset of individual characteristics and design benefit packages to attract preferred risks. The social planner designs a linear transfer formula based on observable characteristics to correct selection incentives. The key technical contribution is to show that the optimal formula is *not* necessarily the one that maximizes predictive accuracy (R²) of the cost regression. Instead, the optimal formula targets the *selection margin* — the services through which insurers can most effectively steer enrollment — and adjusts transfers specifically to neutralize these margins, even if this means under-predicting costs in other dimensions.

### Main Finding

The optimal risk adjustment formula under adverse selection should be proportional to the cross-price elasticity of demand for each service with respect to insurers' selective under-provision. In practice, this means that the formula should assign higher adjustment weights to services that are (a) high-cost, (b) inelastic in demand, and (c) easy for insurers to selectively exclude or discourage. Standard demographic or morbidity-based formulas — including PCG-based systems — are typically sub-optimal in this sense because they predict average costs rather than marginal selection incentives.

### Relevance to Risikoausgleich

Glazer and McGuire (2000) provides the theoretical benchmark for asking whether the Swiss PCG-based formula is "optimal." Their framework suggests it is not, in the strict sense: PCG groups predict past pharmaceutical costs and are therefore good proxies for expected future costs, but they do not directly neutralize selection margins on services that are under-provided to attract healthy enrollees. This is a recognized limitation of the Swiss system and motivates the ongoing debate about extending the Risikoausgleich to include diagnostic cost groups or episode-based payment adjustments.

---

## 5. Van de Ven, W.P.M.M., Beck, K., Buchner, F., Chernichovsky, D., Gardiol, L., Holly, A., Lamers, L.M., Schokkaert, E., Shmueli, A., Spycher, S., Van de Voorde, C., Van Vliet, R.C.J.A., Wasem, J., & Zmora, I. (2003). "Risk Adjustment and Risk Selection on the Sickfund Insurance Market in Five European Countries." *Health Policy*, 65(1), 75–98.

### Motivation and Scope

This large collaborative study — authored by the leading researchers on risk adjustment in Europe, including Swiss co-authors (Gardiol, Holly, Spycher) — provides the first systematic cross-national comparison of risk adjustment effectiveness in regulated health insurance markets. The five countries covered are Germany, Israel, Belgium, the Netherlands, and Switzerland. For each country, the authors measure the predictive accuracy of the formula in force at the time, quantify residual selection incentives, and characterize the strategic responses of insurers.

### Methodology

For each country, the study estimates a cost prediction regression using the risk adjustment variables embedded in the national formula (age, sex, disability status, pharmaceutical costs, prior hospitalizations, etc.) and computes the R² on a representative sample of insured individuals. It then estimates a "selection index" — the correlation between predicted insurer profit per enrollee and individual characteristics — which captures the degree to which the formula leaves unexploited arbitrage for selective insurers. Finally, it documents observed insurer strategies (product differentiation, marketing, service design) that exploit residual selection margins.

### Main Finding

The study finds large cross-country variation in the effectiveness of risk adjustment, with R² ranging from below 5% (Germany, age-sex only) to above 15% (Netherlands, which had already moved to a diagnosis-based system). Switzerland falls in the middle, with the Phase 1 formula explaining approximately 10–12% of individual cost variance. In all five countries, the authors document evidence of cream-skimming despite risk adjustment — suggesting that even the more sophisticated formulas leave economically significant selection opportunities. The Swiss findings specifically document that younger, healthier enrollees are systematically concentrated in certain insurers, consistent with strategic network design.

### Relevance to Risikoausgleich

This paper situates the Swiss system in international context and provides the external benchmark for the 10–12% R² of Phase 1. The subsequent Swiss reforms — moving to PCG-based adjustment with an estimated R² of 20–25% — remain below the Netherlands benchmark (which by 2003 had already reached 15% and has since moved much higher with diagnostic and episode-based adjustments). The Swiss system's improvement is real but places it in the lower tier of European systems by this metric. This comparative perspective motivates the simulation's sensitivity analysis: how much does loss ratio variance improve as R² increases from 10% to 25%, and what would full equalization at 50% R² imply for insurer solvency?

---

## Summary Table

| Paper | Year | Contribution | Key Metric | Relevance |
|-------|------|--------------|------------|-----------|
| Van de Ven & Ellis | 2000 | Theory: selection taxonomy + optimality of risk adjustment | R² of cost prediction | Conceptual framework for all phases |
| Beck, Trottmann & Zweifel | 2010 | Empirics: Swiss Phase 1 effectiveness | Loss ratio variance reduction | Direct baseline for Swiss simulation |
| Schokkaert & Van de Voorde | 2004 | Welfare: partial adjustment can be worse than none | Welfare under θ ∈ [0,1] | Caution about reform sequencing |
| Glazer & McGuire | 2000 | Theory: optimal formula targets selection margin, not average cost | Cross-price elasticity | Normative benchmark for PCG formula |
| Van de Ven et al. | 2003 | Comparative: R² and selection across 5 European systems | Selection index | International benchmark for Swiss R² |
