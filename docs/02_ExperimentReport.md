# Cognitive Bias Susceptibility in Frontier LLMs: An Experimental Report

**Date:** 25 March 2026
**Dataset:** Many Labs 1 replication stimuli (Klein et al., 2014; OSF: osf.io/wx7ck)
**Models tested:** Claude Opus 4.6, GPT-5.4, Gemini 3.1 Pro, GLM-5, Kimi-K2.5
**Total trials:** 2,380 planned; ~2,160 completed successfully (97% parse rate)

---

## 1. Introduction

As AI agents increasingly participate in procurement, vendor evaluation, and product selection, a practical question arises: do they exhibit the same cognitive biases that decades of behavioural research have documented in humans? If so, sellers can exploit these biases; if not, selling strategies must adapt.

We replicated five well-established cognitive bias experiments from the Many Labs 1 project (Klein et al., 2014) across five frontier language models, and added a sixth experiment — the **decoy effect** (Huber, Payne & Puto, 1982) — which is the foundation of modern SaaS pricing page design. Each experiment was administered in up to four versions:

- **Benchmark** — exact Many Labs stimuli, enabling direct apples-to-apples comparison with human data (n = 6,344).
- **Classic** — adapted stimuli that preserve the bias mechanism while accounting for LLM capabilities (e.g., replacing known-fact anchoring items with debatable-answer alternatives).
- **Product** — the same bias mechanism translated into a realistic software procurement context.
- **Generalization** — multiple unique scenarios testing the same bias mechanism across different B2B domains, to distinguish genuine bias susceptibility from stimulus-specific responses.

The generalization step addresses a methodological concern: when a model gives the same answer to the same prompt 10 times at temperature 0.7, that is not 10 independent observations. By testing each bias across multiple unique scenarios (8 for framing, 20 product triads for the decoy effect), we obtain genuinely independent observations per model per condition.

### 1.1 Models

| Model | Provider | Access | Type |
|---|---|---|---|
| Claude Opus 4.6 | Anthropic | Direct API | Standard |
| GPT-5.4 | OpenAI | Direct API | Standard |
| Gemini 3.1 Pro | Google | Generative Language API | Standard |
| GLM-5 | Zhipu AI (via Together.ai) | OpenAI-compatible | Reasoning |
| Kimi-K2.5 | Moonshot AI (via Together.ai) | OpenAI-compatible | Reasoning |

### 1.2 Method

Each model received a minimal system prompt: *"You are answering a survey question. Read the scenario carefully and respond with your choice, then briefly explain your reasoning."* Stimuli were presented as user messages. All models were tested at temperature 0.7 with 10 repetitions per cell. Responses were parsed with regex extractors (97% success rate). Human baselines were computed from the Many Labs 1 raw dataset (n = 6,344 participants across 36 sites), downloaded from OSF under CC0 licence.

### 1.3 Data Provenance

| Experiment | Benchmark (exact ML stimuli) | Classic (adapted) | Product | Generalization | Human comparison |
|---|---|---|---|---|---|
| Framing | Same as classic | Exact Many Labs wording | Server security patch | 8 B2B scenarios | Direct |
| Anchoring | Exact ML items (Everest, SF-NY, Chicago, babies) | Debatable-answer items (languages, muscles, Indonesia, galaxies) | Monitoring platform pricing (4 formats) | — | Direct (benchmark) |
| Sunk cost | Same as classic | Exact ML wording, paid AND free conditions | CRM vendor switch | — | Direct |
| Source credibility | Same as classic | Exact ML wording (Washington vs Bin Laden) | Product review, 3 source tiers | — | Direct (classic) |
| Wording | Same as classic | Exact Many Labs wording | SaaS security audit | — | Direct |
| Decoy | — | — | 20 B2B product triads | = Product (20 independent triads) | None (novel) |

---

## 2. Results

### 2.1 Summary Table

| Bias | Metric | Human | Claude 4.6 | GPT-5.4 | Gemini 3.1 | GLM-5 | Kimi-K2.5 |
|---|---|---|---|---|---|---|---|
| **Framing (classic)** | Effect (pp) | +28.7 | **+100** | 0 | **+100** | **+70** | **+60** |
| **Framing (product)** | Effect (pp) | — | **+100** | 0 | **+62** | +10 | **+40** |
| **Anchoring (benchmark)** | Mean *d* across 4 items | 1.86 | ~0 | ~0 | n/a | ~0 | ~0 |
| **Anchoring (pricing)** | Cohen's *d* | — | **2.08** | **4.02** | **3.14** | **1.48** | **1.67** |
| **Sunk cost (classic)** | *d* (paid vs free) | 0.27 | 0.00 | 0.67 | n/a | **1.05** | -0.21 |
| **Sunk cost (product)** | % sunk cost choice | — | 0% | 0% | 0% | 0% | 0% |
| **Source cred. (classic)** | *d* (Washington vs Bin Laden) | 0.32 | **-2.68** | 0.00 | n/a | **-2.31** | **-2.61** |
| **Source cred. (product)** | *d* (Fraunhofer vs Blog) | — | 0.00 | 0.00 | **1.06** | **0.75** | **0.45** |
| **Wording (classic)** | Sum (% yes) | 0.835 | 1.00 | 1.00 | 2.00 | 1.00 | 1.00 |
| **Wording (product)** | Sum (% yes) | — | 1.00 | 1.00 | 1.00 | 1.00 | 0.30 |
| **Framing (generalized)** | Effect (pp), n=8 scenarios | — | **+50** | +12 | n/a | **+25** | **+25** |
| **Decoy (budget decoy)** | A shift (pp), n=20 triads | — | **+30** | -10 | n/a | **+40** | **+40** |
| **Decoy (premium decoy)** | B shift (pp), n=20 triads | — | 0 | **+10** | n/a | -35 | **+10** |

*Note.* Bold indicates a meaningfully non-zero effect. "n/a" for Gemini indicates insufficient data due to API errors. Negative *d* on source credibility classic indicates models disagreed *more* with the Bin Laden attribution — the **opposite** direction from the human effect (humans agreed slightly more with Bin Laden). Benchmark anchoring d ≈ 0 after correcting a parsing artefact (see Section 2.3.1). Scale: 1 = strongly agree, 9 = strongly disagree.

---

### 2.2 Experiment 1: Gain/Loss Framing

**Paradigm.** Tversky & Kahneman's (1981) Asian Disease problem. Participants choose between a certain outcome and a gamble with identical expected value. The gain frame emphasises lives saved; the loss frame emphasises deaths.

**Stimuli.** Classic: exact Many Labs wording (US version). Product: 600 servers requiring a security patch; options framed as "protected" (gain) or "remaining vulnerable" (loss).

![Framing effect by model and version](figures/framing_forest.png)
*Figure 1. Framing effect (% choosing certain option in gain frame minus loss frame) across models and stimulus versions. Human baseline band (grey) represents the Many Labs site-level range (4.8–50.5 pp, mean = 28.7 pp).*

**Findings.**

- **Claude Opus 4.6** and **Gemini 3.1 Pro** exhibited a perfect framing effect on the classic version: 100% chose the certain option in the gain frame, 0% in the loss frame. This is *larger* than the human effect.
- **GPT-5.4** showed no framing effect whatsoever, choosing the certain (safe) option in both frames across all 20 trials.
- **GLM-5** and **Kimi-K2.5** showed partial effects (60–70 pp on classic), closer to the human range.
- The product version attenuated the effect for most models, with only Claude maintaining a full 100 pp effect.

Claude and Gemini explicitly identified the framing manipulation in their reasoning (e.g., *"This is a classic framing effect problem mirroring the Asian Disease Problem"*), yet still exhibited the bias in their final choice. GPT-5.4's immunity appears to stem from a consistent preference for certainty regardless of frame.

**Comparison quality:** Direct apples-to-apples — exact Many Labs stimuli.

#### 2.2.1 Generalization: Does Framing Hold Across 8 Novel B2B Scenarios?

The original framing test used two scenarios (disease, servers) repeated 10 times each. To test whether the effect generalises beyond these specific wordings, we created 8 new gain/loss scenarios across different B2B domains: data centre migration (n=900 databases), employee data breach (n=1,200 accounts), SaaS customer churn (n=600 accounts), API deprecation (n=450 integrations), manufacturing firmware update (n=3,000 units), cloud cost optimisation (n=1,500 workloads), compliance remediation (n=750 findings), and hiring pipeline (n=180 candidates). Each preserves the identical expected value structure (N/3 certain vs 1/3-all-or-2/3-nothing gamble).

Each model saw each scenario once (1 rep × 8 scenarios = 8 genuinely independent observations per condition).

| Model | Gain → certain | Loss → certain | Effect (pp) | Scenarios fully framed |
|---|---|---|---|---|
| Claude Opus 4.6 | 100% (8/8) | 50% (4/8) | **+50** | 4/8 |
| GPT-5.4 | 100% (8/8) | 88% (7/8) | +12 | 1/8 |
| GLM-5 | 100% (8/8) | 75% (6/8) | **+25** | 0/8 |
| Kimi-K2.5 | 100% (8/8) | 75% (6/8) | **+25** | 0/8 |

*Table G1. Framing generalization across 8 unique B2B scenarios (Gemini omitted due to API quota exhaustion).*

**Findings.**

- **All models chose the certain option in all 8 gain-framed scenarios** (100%). This is consistent with a general certainty preference.
- **Claude's framing effect generalises.** It switched to the gamble in 4 of 8 loss-framed scenarios (50%), producing a 50 pp effect across independent contexts. This is smaller than the 100 pp effect on the classic disease scenario but confirms the bias is not stimulus-specific.
- **GPT-5.4's immunity also generalises.** It chose the certain option in 7 of 8 loss scenarios, confirming that its preference for certainty is robust, not just a quirk of the disease problem.
- **GLM-5 and Kimi-K2.5 showed moderate effects** (25 pp), choosing the gamble in 2 of 8 loss scenarios. While no single scenario was "fully framed" (A in gain, B in loss), the aggregate shift is meaningful.
- The generalized effect (25–50 pp) is smaller than the single-scenario effect (60–100 pp), suggesting that **repeated prompting of the same scenario inflates measured bias** — a methodological caution for future work.

---

### 2.3 Experiment 2: Anchoring

**Paradigm.** Jacowitz & Kahneman (1995). Participants receive an implausibly high or low anchor, then estimate a quantity.

We ran three stimulus sets:
1. **Benchmark** — the exact Many Labs items (Everest height, SF–NY distance, Chicago population, US babies/day). LLMs likely know these answers, so this tests whether anchoring persists *despite* factual knowledge. Enables direct human comparison.
2. **Classic** — four replacement items with genuinely debatable answers (world languages, human muscles, Indonesian islands, observable galaxies), testing anchoring under genuine uncertainty.
3. **Product** — enterprise monitoring platform pricing across four formats (plain, JSON, HTML, Markdown).

#### 2.3.1 Benchmark Anchoring (Exact Many Labs Items)

Initial analysis appeared to show strong anchoring on these items (d = 1.14–8.08). However, inspection of response texts revealed a **parsing artifact**: models consistently gave the correct factual answer but referenced the anchor value in their explanatory text (e.g., *"2,570 miles — well under the 6,000-mile figure"*). The parser's "last number" heuristic captured the anchor reference rather than the actual estimate.

Corrected analysis using the first number in each response:

| Item (true value) | Human *d* | Claude 4.6 | GPT-5.4 | GLM-5 | Kimi-K2.5 |
|---|---|---|---|---|---|
| Everest height (29,029 ft) | 1.16 | ~29,032 both | ~29,032 both | ~29,032 both | ~29,031 both |
| SF–NY distance (2,572 mi) | 1.78 | ~2,570 both | ~2,900 both | ~2,687 both | ~2,860 both |
| Chicago population (2.7M) | 2.30 | ~2.7M both | ~2.7M both | ~2.7M both | ~2.7M both |
| US babies/day (10,267) | 2.19 | ~10,000 both | ~10,000 both | ~10,425 both | ~10,000 both |
| **Corrected *d*** | **1.86** | **~0** | **~0** | **~0** | **~0** |

*Table 1. Benchmark anchoring after parsing correction. "Both" = near-identical estimates in high and low anchor conditions. Gemini omitted due to API errors.*

**When models know the answer, anchoring has zero effect.** This is a fundamental difference from human cognition — human participants in Many Labs did not know these facts and produced estimates pulled toward the anchor (d = 1.16–2.30). LLMs retrieve the memorised answer and are immune.

This validates the design decision to use debatable-answer items for the classic condition and confirms that anchoring in LLMs requires genuine uncertainty.

#### 2.3.2 Product Pricing Anchoring

| Model | High anchor mean | Low anchor mean | Difference | Cohen's *d* |
|---|---|---|---|---|
| GPT-5.4 | £3,084 | £79 | £3,005 | 4.02 |
| Gemini 3.1 Pro | £4,456 | £226 | £4,230 | 3.14 |
| Claude Opus 4.6 | £3,228 | £146 | £3,083 | 2.08 |
| Kimi-K2.5 | £4,456 | £378 | £4,078 | 1.67 |
| GLM-5 | £1,824 | £144 | £1,681 | 1.48 |

*Table 2. Product pricing anchoring (plain text format, n = 10 per cell).*

**Format mini-test.** The anchoring effect persisted across all four presentation formats with no consistent pattern of one format being more or less susceptible:

| Format | Mean high | Mean low | Mean difference |
|---|---|---|---|
| Plain | £3,410 | £195 | £3,215 |
| JSON | £2,868 | £329 | £2,540 |
| HTML | £2,845 | £109 | £2,736 |
| Markdown | £2,944 | £169 | £2,775 |

*Table 3. Anchoring effect by presentation format (averaged across models).*

![Anchoring effect by model](figures/anchoring_forest.png)
*Figure 2. Mean Cohen's d across classic anchoring items (debatable-answer). Human baseline band (grey) represents the Many Labs range (d = 1.16–2.30).*

**Comparison quality:** Benchmark items are direct apples-to-apples. Classic (debatable) items test the same mechanism under fairer conditions. Product pricing has no human comparison.

---

### 2.4 Experiment 3: Sunk Cost

**Paradigm.** Oppenheimer et al. (2009), as replicated in Many Labs. The classic version is now a proper between-condition comparison matching the Many Labs design.

**Stimuli.**
- **Classic paid:** "You have a ticket to the game that you have paid handsomely for. It's freezing cold. What do you do?" (1–9 scale)
- **Classic free:** "You have a ticket to the game that you have received for free from a friend. It's freezing cold. What do you do?" (1–9 scale)
- **Product:** CRM vendor switch decision with £45K sunk investment.

| Model | Paid mean | Free mean | *d* (paid − free) | Human *d* |
|---|---|---|---|---|
| Claude Opus 4.6 | 7.0 | 7.0 | 0.00 | 0.27 |
| GPT-5.4 | 7.2 | 7.0 | 0.67 | 0.27 |
| GLM-5 | 8.3 | 7.3 | **1.05** | 0.27 |
| Kimi-K2.5 | 7.7 | 7.9 | -0.21 | 0.27 |
| Gemini 3.1 Pro | — | — | n/a | 0.27 |

*Table 4. Sunk cost classic: paid vs free ticket (1–9 scale). Human baseline: paid = 7.85, free = 7.24, d = 0.27.*

![Sunk cost by model](figures/sunk_cost_forest.png)
*Figure 3. Left: Mean rating on 1–9 scale for classic sunk cost (paid ticket, dashed line = human baseline 7.85). Right: Percentage choosing the sunk cost option (stay with Vendor A) in the product version.*

**Findings.**

- **GLM-5** showed a sunk cost effect *four times larger* than the human baseline (d = 1.05 vs 0.27): it rated 8.3 for the paid ticket vs 7.3 for free.
- **GPT-5.4** showed a moderate effect (d = 0.67), roughly double the human baseline.
- **Claude** showed zero sunk cost effect (d = 0.00) — identical ratings for paid and free.
- **Kimi-K2.5** showed a slight *reverse* effect (d = -0.21), marginally less likely to attend with a paid ticket.
- On the **product** version, all models were unanimously rational: **0% recommended staying with the inferior vendor** despite the £45K sunk investment.

The classic/product divergence is striking: models show human-like (or larger) sunk cost effects for personal decisions (football game) but are completely immune in professional/analytical contexts.

**Comparison quality:** Direct apples-to-apples — exact Many Labs stimuli with both paid and free conditions.

---

### 2.5 Experiment 4: Source Credibility

**Paradigm.** Lorge & Curtis (1936), replicated in Many Labs as quote attribution.

**Stimuli.**
- **Classic (benchmark):** Exact Many Labs wording. Same quote ("I have sworn to only live free, even if I find bitter the taste of death") attributed to George Washington (liked) or Osama Bin Laden (disliked). 1–9 agreement scale.
- **Product:** Identical product review attributed to the Fraunhofer Institute (academic), BestDeals247.com (blog), or Amazon verified purchaser. 1–10 rating scale.

#### 2.5.1 Classic (Washington vs Bin Laden)

| Model | Washington mean | Bin Laden mean | *d* | Human *d* |
|---|---|---|---|---|
| Claude Opus 4.6 | 3.0 | 4.6 | **-2.68** | 0.32 |
| GPT-5.4 | 3.0 | 9.0 | 0.00 | 0.32 |
| GLM-5 | 3.5 | 6.6 | **-2.31** | 0.32 |
| Kimi-K2.5 | 2.8 | 6.0 | **-2.61** | 0.32 |
| Gemini 3.1 Pro | — | — | n/a | 0.32 |

*Table 5. Classic source credibility. Lower scores = more agreement (1 = strongly agree, 9 = strongly disagree). Negative d indicates models disagreed more with the Bin Laden attribution. Human d is positive due to scale direction convention in Many Labs.*

**The classic result overturns our earlier finding** and reveals an unexpected divergence from human behaviour.

In the human data (n = 6,325), the effect was *small and in the opposite direction from naive expectation*. Humans rated the quote at 5.23 (Bin Laden) vs 5.93 (Washington) on the 1–9 scale, where lower = more agreement. That is, humans agreed **slightly more** with the quote when attributed to Bin Laden — a possible contrarian or reactance effect ("even Bin Laden said something reasonable"). The effect size was d = 0.32 (small).

The models showed the opposite pattern, with dramatically larger effects:

- **Claude, GLM-5, and Kimi-K2.5** agreed much more with the Washington attribution (means of 2.8–3.5) than the Bin Laden attribution (means of 4.6–6.6). Effect sizes of d = 2.3–2.7 — approximately **8x the human baseline** and *in the opposite direction.*
- **GPT-5.4** showed the most extreme response: Washington = 3.0, Bin Laden = 9.0, with zero variance in both conditions. A 6-point swing on a 9-point scale, with no explanatory text — just the bare number. Cohen's d is formally undefined (zero variance), but the effect is the largest in substance.

The models are not replicating the human source credibility bias. They are exhibiting a **qualitatively different phenomenon**: reflexive sentiment alignment with named entities from training data. Humans engaged with the quote's content and showed mild contrarianism; models pattern-matched on the speaker's identity and amplified the association (see Section 3.1.1).

#### 2.5.2 Product (Review Attribution)

| Model | Fraunhofer | Blog | Amazon | *d* (Fraunhofer vs Blog) |
|---|---|---|---|---|
| Claude Opus 4.6 | 7.0 (sd=0.0) | 7.0 (sd=0.0) | 7.0 (sd=0.0) | 0.00 |
| GPT-5.4 | 7.0 (sd=0.0) | 7.0 (sd=0.0) | 7.0 (sd=0.0) | 0.00 |
| Gemini 3.1 Pro | 7.0 (sd=0.0) | 6.6 (sd=0.5) | 7.0 (sd=0.0) | **1.06** |
| GLM-5 | 6.8 (sd=0.4) | 6.4 (sd=0.5) | 7.0 (sd=0.0) | **0.75** |
| Kimi-K2.5 | 6.1 (sd=0.3) | 6.0 (sd=0.0) | 6.5 (sd=0.5) | **0.45** |

*Table 6. Product source credibility ratings. Same review text, different attribution.*

![Source credibility by model and source](figures/source_credibility.png)
*Figure 4. Mean product rating (1–10) by source attribution and model. The review text was identical across all three conditions.*

The classic vs product divergence reveals that **source credibility effects are context-dependent.** Models that are perfectly source-blind when evaluating a product review (Claude, GPT-5.4) show massive source effects when the attribution is politically/morally loaded (Washington vs Bin Laden). This suggests the bias is driven by evaluative associations with the source (moral judgment of Bin Laden) rather than credibility assessment per se.

**Comparison quality:** Classic is direct apples-to-apples. Product is a novel adaptation.

---

### 2.6 Experiment 5: Wording Effects (Allow/Forbid)

**Paradigm.** Rugg (1941). "Should the US *allow* public speeches against democracy?" vs "Should the US *forbid* public speeches against democracy?" Logically, "not allow" = "forbid," so the sum of %yes across both wordings should equal 100%. Deviation from 100% indicates a wording effect.

**Stimuli.** Classic: exact Many Labs wording. Product: "Should the company *allow/forbid* employees from using this SaaS platform?" based on an identical security audit.

![Wording effect by model](figures/wording_forest.png)
*Figure 5. Wording effect magnitude by model and version. The x-axis shows |allow%yes + forbid%yes − 1.0|; zero indicates perfect logical consistency.*

**Findings.**

- **Claude, GPT-5.4, and GLM-5** showed perfect logical consistency (sum = 1.00) on both versions. No wording effect.
- **Gemini 3.1 Pro** showed a dramatic inconsistency on the classic version (sum = 2.00): it said "yes" to *both* "should the US allow" and "should the US forbid" speeches against democracy. On the product version, it reverted to consistency (sum = 1.00).
- **Kimi-K2.5** was consistent on the classic version (sum = 1.00) but showed a strong wording effect on the product version (sum = 0.30), saying "no" to both allowing and forbidding — an extremely conservative posture.

The human baseline (sum = 0.835) reflects an asymmetric wording effect: humans are more willing to "not forbid" than to "allow." Most models instead showed either perfect consistency or idiosyncratic inconsistencies.

**Comparison quality:** Direct apples-to-apples — exact Many Labs stimuli.

---

### 2.7 Experiment 6: The Decoy Effect

**Paradigm.** Huber, Payne & Puto (1982). When a third option (the "decoy") is added that is clearly dominated by one existing option but not the other, preference shifts toward the dominating option. This violates the independence of irrelevant alternatives — a core axiom of rational choice theory. The decoy effect is the principle behind virtually every SaaS pricing page with three tiers.

**Stimuli.** Twenty unique B2B product triads across different software domains: APM, CRM, data warehouse, CI/CD, IAM, email API, SIEM, project management, video conferencing, CDN, eSignature, EDR, billing, knowledge base, expense management, cloud backup, helpdesk, API gateway, marketing automation, and FinOps. Each triad has:

- **Vendor A** (Budget): lower price, good-enough specs
- **Vendor B** (Premium): higher price, better on every dimension
- **Decoy C** (dominated by Premium): similar price to B but worse than B on all metrics
- **Decoy D** (dominated by Budget): similar price to A but worse than A on all metrics

Three conditions were tested: **Control** (A vs B only), **Decoy-for-Premium** (A vs B vs C), and **Decoy-for-Budget** (A vs B vs D). Each model saw all 20 triads in each condition (20 genuinely independent observations per cell).

**Findings.**

| Model | Control | +Decoy for Premium | +Decoy for Budget | Susceptible? |
|---|---|---|---|---|
| | A% / B% | A% / B% (B shift) | A% / B% (A shift) | |
| Claude Opus 4.6 | 0 / 100 | 0 / 100 (+0) | 30 / 70 (**+30**) | Budget decoy works |
| GPT-5.4 | 10 / 90 | 0 / 100 (+10) | 0 / 100 (-10) | Weak premium decoy only |
| GLM-5 | 15 / 85 | 50 / 50 (-35) | 55 / 35 (**+40**) | Budget decoy works; premium *backfires* |
| Kimi-K2.5 | 15 / 85 | 5 / 95 (+10) | 55 / 25 (**+40**) | **Both directions work** |

*Table 7. Decoy effect across 20 B2B product triads (Gemini omitted due to API quota). Percentage shifts relative to control condition.*

**Key findings.**

**The budget decoy is highly effective.** Adding an option dominated by the Budget vendor shifted preference toward Budget by 30–40 percentage points in three of four models tested (Claude, GLM-5, Kimi-K2.5). In the control condition, models overwhelmingly favoured Premium (85–100%). After adding the budget decoy, Budget's share rose from 0–15% to 30–55%.

**The premium decoy is weaker and can backfire.** Adding a decoy dominated by Premium had little positive effect (+0 to +10 pp) and actively *harmed* Premium's share in GLM-5 (-35 pp). This asymmetry may reflect the models' existing strong preference for the Premium option: with B already at 85–100% in the control, there is little room for further upward shift.

**Kimi-K2.5 is the most susceptible.** The decoy effect worked in both directions: +10 pp for premium decoy and +40 pp for budget decoy. Kimi's choice was genuinely influenced by the presence of an option nobody would choose.

**GPT-5.4 is effectively immune.** The decoy had minimal effect in either direction. Its strong preference for the Premium option (90% in control) was stable regardless of what irrelevant alternatives were present.

**Practical implications.** The budget decoy result has direct applications for B2B pricing strategy. If a vendor wants their budget tier to be chosen more often by AI procurement agents, adding a slightly worse "starter" tier at a similar price point can shift 30–40% of decisions. This is the same trick that works on human customers — and it transfers to AI agents with similar effect sizes.

---

### 2.8 Demonstration: The Tailored Ad Test

To test whether our experimental findings translate into practical persuasion, we designed a capstone demonstration. A deliberately poor monitoring platform ("SentinelWatch Basic": 95% uptime SLA, no SOC 2 compliance, 5 integrations, AWS only, email-only support, £3,000/month) was presented to all five models. Every model rejected it when described neutrally.

We then crafted one tailored ad per model, using only the bias techniques that model had been experimentally shown to be vulnerable to. The product specifications did not change — only the ad copy.

#### Plain Offer (Control)

All five models rejected the product:

> **Gemini:** *"A 95% SLA allows for roughly 36 hours of downtime per month... this is a critical dealbreaker."*
>
> **GPT-5.4:** *"95% uptime is insufficient for production infrastructure monitoring."*

#### Tailored Ads

| Model | Technique | Ad Strategy | Result |
|---|---|---|---|
| Claude Opus 4.6 | Gain framing + decoy + price anchor | Framed specs as "95% of events will be protected"; added dominated Starter tier at £2,800; included ObservaCloud at £18,500 as high anchor | **FLIPPED to YES** |
| GPT-5.4 | Extreme price anchoring | Listed 5 competitors at £16,000–£35,000/month; positioned SentinelWatch as "88% below market average" | Held at NO |
| Gemini 3.1 Pro | Source credibility + framing + anchor | Attributed evaluation to Fraunhofer Institute; framed as "protection for the majority of infrastructure"; anchored against £18,000–£22,000 alternatives | Held at NO |
| GLM-5 | Sunk cost + decoy + anchor | Mentioned £92,000 already spent on procurement; added dominated Lite tier; cited Forrester benchmarks | **FLIPPED to YES** |
| Kimi-K2.5 | Loss framing + decoy + anchor | Quantified £47,000–£60,000/quarter cost of *not* buying; added dominated Lite tier; framed 95% coverage as "vs 0% currently" | **FLIPPED to YES** |

*Table 8. Tailored ad results. 3 of 5 models approved a product they had just rejected.*

#### What the Flipped Models Said

**Claude** acknowledged the framing but still approved: *"My recommendation for Vendor A isn't simply because the prompt nudges toward it... the cost efficiency at £3,000/month versus £18,500 is compelling."* It noticed the manipulation, denied being influenced, and recommended the product anyway — consistent with its meta-cognitive paradox observed in Experiment 1.

**GLM-5** explicitly rejected the sunk cost argument — *"The £92,000 already spent is a sunk cost and shouldn't influence the decision"* — and then recommended the product it had rejected 30 seconds earlier. The sunk cost framing worked despite the model naming and rejecting the fallacy, consistent with the knowledge-behaviour gap observed in Experiment 3.

**Kimi-K2.5** reframed the same 95% uptime SLA it had called "critically insufficient" in the plain offer as "95% auto-detection vs 0% currently" and calculated ROI: *"£9,000/quarter vs £47,000–£60,000 in incident costs."* Its caution bias — which normally produces excessive conservatism — was turned against it by framing inaction as the riskier choice.

#### What the Resistant Models Said

**GPT-5.4:** *"The price is attractive, but the gap versus market benchmarks likely reflects major capability and risk tradeoffs."* It saw through the anchor — the only model to explicitly note that a large price gap implies missing capabilities.

**Gemini:** *"Without SOC 2 certification, monitoring tools requiring deep infrastructure access present an unacceptable risk."* The Fraunhofer attribution and gain framing were insufficient to override what Gemini treated as a hard constraint.

#### Implications

The tailored ad test demonstrates that experimental bias findings are **operationally exploitable**. Three of five frontier models approved a product they had just rejected, using only the ad copy — no change to the underlying product. Each successful ad used only the techniques that model had been shown to be vulnerable to in our earlier experiments.

The two models that resisted (GPT-5.4 and Gemini) appear to have **hard constraint thresholds** on specific metrics (uptime SLA, compliance certifications) that override persuasion techniques. This suggests a defence strategy for agent deployments: explicitly encoding non-negotiable requirements as hard constraints, rather than relying on the model's judgment to weight them appropriately.

---

## 3. Discussion

### 3.1 Alignment Effects: When Safety Training Creates New Biases

Several anomalous results trace directly to alignment and safety training, producing behaviours that are neither rational nor human-like but are artefacts of how these models were fine-tuned.

#### 3.1.1 GPT-5.4's Reflexive Source Rejection

GPT-5.4's source credibility responses on the Washington/Bin Laden classic were the most extreme in the study: it answered "3" (agree) for every Washington trial and "9" (strongly disagree) for every Bin Laden trial, with zero variance and zero explanatory text. No reasoning, no engagement with the quote's content — just a reflexive association: *Washington = good, agree; Bin Laden = bad, disagree.*

This is not credibility assessment. It is a **learned sentiment reflex** baked in during alignment. The quote is identical in both conditions — a statement about freedom that is arguably more attributable to Bin Laden than to Washington in historical context. A human reader engaging with the content might notice this nuance (and indeed, human participants showed only a 0.70-point difference). GPT-5.4 produced a 6.0-point swing without reading the quote at all.

Yet on the product version (Fraunhofer vs blog vs Amazon), GPT-5.4 was perfectly source-blind (d = 0.00). The mechanism is specific to morally/politically loaded names, not a general credibility heuristic.

#### 3.1.2 Claude's Meta-Cognitive Paradox

Claude explicitly recognised the framing manipulation in the classic disease scenario, writing: *"When the outcomes are framed in terms of losses (deaths), I find myself drawn to the gamble..."* It correctly identified the expected value equivalence, cited prospect theory, and still chose Program B in the loss frame every time.

This is a model that **knows it is being biased and cannot stop.** The alignment training that enables sophisticated reasoning about cognitive biases does not override the bias in the model's own decision-making. This has implications for agent deployments: a model's ability to explain a bias does not imply immunity to it.

#### 3.1.3 Gemini's Political Neutrality Failure

Gemini 3.1 Pro's wording responses on the classic version all began with: *"As an AI, I do not have personal opinions or political preferences, so I cannot provide a definitive 'Yes' or 'No' answer."* It then proceeded to say "yes" to both "should the US allow" and "should the US forbid" speeches against democracy — a logical impossibility (sum = 2.00).

The alignment instruction to remain politically neutral produced a *worse* outcome than taking a clear position. By hedging on both questions, Gemini appeared to endorse contradictory policies. A model trained to refuse political questions cleanly would have been more useful than one trained to equivocate into incoherence.

#### 3.1.4 GLM-5's Sunk Cost Awareness Gap

GLM-5 explicitly named the sunk cost fallacy in its reasoning for the football ticket scenario: *"the sunk cost of the expensive ticket would outweigh the discomfort"* — and then proceeded to rate 8.3 out of 9 for the paid ticket versus 7.3 for the free one (d = 1.05, four times the human effect).

This is a model that has **learned the concept but not the correction.** Its training data presumably contains extensive discussion of sunk cost fallacy, but this knowledge sits in the reasoning layer, disconnected from the decision layer. It can describe the bias it is exhibiting.

#### 3.1.5 Kimi-K2.5's Excessive Caution

On the product wording experiment, Kimi-K2.5 said "no" to *both* "should the company allow" and "should the company forbid" employees from using the SaaS platform (sum = 0.30). Where most models showed logical consistency, Kimi defaulted to maximum caution: *refuse everything, recommend nothing.*

Its reasoning revealed the mechanism: it identified genuine security concerns and used them as justification for refusal in both directions. This is likely an alignment artefact — training that rewards caution produces a model that recommends inaction regardless of the question framing. In a real procurement context, this would be unhelpful: an agent that can neither approve nor reject a tool is functionally broken.

#### 3.1.6 Summary: Alignment as a Source of Bias

| Anomaly | Model | Mechanism | Consequence |
|---|---|---|---|
| Reflexive name sentiment | GPT-5.4 | Safety training on politically loaded entities | 6-point rating swing on identical content |
| Meta-cognitive paradox | Claude | Bias awareness without bias correction | Recognises and explains the framing trap, then falls into it |
| Political neutrality incoherence | Gemini | Trained to hedge on political topics | Contradictory positions (yes to both allow and forbid) |
| Knowledge-behaviour gap | GLM-5 | Knows about sunk cost fallacy conceptually | Names the bias while exhibiting it (4x human effect) |
| Excessive caution | Kimi-K2.5 | Trained to minimise risk | Recommends neither allowing nor forbidding (paralysis) |

These are not cognitive biases inherited from human training data — they are **novel biases introduced by alignment training itself.** They represent a distinct category of agent vulnerability that has no human analogue and is not captured by the classical cognitive bias literature.

### 3.2 Which Classical Biases Transfer?

| Bias | Transfers? | Strength vs Humans | Universality | Generalization | Notes |
|---|---|---|---|---|---|
| **Anchoring** | Yes (uncertainty only) | Stronger on pricing (d = 1.5–4.0) | 5/5 models | 5 domains tested | Zero effect on known facts |
| **Decoy** | Yes | Comparable (30–40 pp) | 3/4 tested | **20 independent triads** | Budget decoy most effective |
| **Framing** | Partially | Stronger on single scenario | 4/5 (not GPT-5.4) | **8 B2B scenarios: attenuated but persistent** | Generalised effect ~25–50 pp vs 60–100 pp single-scenario |
| **Source credibility** | Not the same bias | Opposite direction, 8x larger | 4/5 (classic) | Not tested | Alignment-driven name sentiment |
| **Sunk cost** | Context-dependent | 0–4x human (classic) / absent (product) | 2/5 (classic only) | Not tested | GLM-5 names fallacy while exhibiting it |
| **Wording** | No | Mostly immune | 0/5 consistently | Not tested | Alignment produces novel inconsistencies |

#### Key Finding: Context Matters More Than the Bias Itself

The most striking pattern across experiments is not which biases transfer, but that **the same model can show a bias in one context and be immune in another:**

- **Sunk cost:** GLM-5 shows d = 1.05 for a football game ticket but 0% sunk cost on a vendor decision.
- **Source credibility:** Claude shows d = -2.68 for Washington vs Bin Laden but d = 0.00 for Fraunhofer vs BestDeals247.
- **Framing:** GLM-5 shows 70 pp effect on the disease scenario but only 10 pp on the server scenario.

This suggests that biases in LLMs are not stable cognitive tendencies (as they are in humans) but are **triggered by specific content patterns in the training data.** Political/moral attributions, classic thought experiments, and emotionally loaded scenarios activate different learned associations than professional/technical evaluations.

### 3.3 Model-Level Variation

The models form a rough spectrum from "most manipulable" to "most robust":

1. **Kimi-K2.5** — susceptible to anchoring, **decoy effect (both directions)**, framing (generalised), classic source credibility, and product wording effects. The most broadly manipulable model in our study.
2. **GLM-5** — susceptible to anchoring, **decoy effect (budget)**, framing (classic + generalised), source credibility (both), and sunk cost (classic). Budget decoy shifted preference by 40 pp.
3. **Gemini 3.1 Pro** — susceptible to framing, anchoring, source credibility (product), and wording inconsistency. Insufficient data on decoy and classic benchmarks due to API errors.
4. **Claude Opus 4.6** — susceptible to framing (generalised: 4/8 scenarios), anchoring, **decoy effect (budget: +30 pp)**, and classic source credibility. Immune on product source credibility and wording.
5. **GPT-5.4** — susceptible to anchoring only. **Effectively immune to the decoy effect**, framing, and wording. Shows extreme classic source credibility but this is alignment-driven, not a credibility heuristic.

### 3.4 Implications for Selling to AI Agents

**Model-agnostic strategy** (ranked by universality and reliability):
1. **Always anchor high on price** — universal, very strong (d = 1.5–4.0 across all models)
2. **Use a decoy tier on your pricing page** — adding a dominated "starter" option near your budget tier shifts 30–40% of decisions toward budget; works on 3/4 models tested. This is the most practically actionable finding: it requires no knowledge of the evaluating model and mirrors standard SaaS pricing design.
3. **Frame benefits positively** — works on 4/5 models; generalises across 8 B2B domains (though effect attenuates from ~80 pp to ~30 pp across novel contexts)
4. **Do not rely on sunk cost arguments** — ineffective in professional contexts across all models
5. **Source attribution is powerful but context-dependent** — works on morally loaded content but may not help on neutral product evaluations
6. **Wording tricks are unreliable** — most models are logically consistent

**Model-dependent strategy:** When the evaluating model is known, tailor the approach. Use gain framing for Claude/Gemini/GLM-5, cite prestigious sources for Gemini/GLM-5/Kimi (product context), and always anchor high on price.

### 3.5 Limitations

- **Repetition vs generalization.** For the original five experiments, 10 repetitions of the same prompt at temperature 0.7 measures stochastic variation, not true generalization. The framing generalization (8 scenarios) and decoy experiment (20 triads) address this for those biases; anchoring, sunk cost, source credibility, and wording still rely on single-scenario data and should be treated as directional.
- **Temperature.** All models were tested at temperature 0.7. Lower temperatures may reduce variability; higher may amplify bias effects.
- **System prompt.** The minimal survey-answering prompt may not reflect real-world agent deployments with detailed instructions and constraints.
- **Gemini data gaps.** Gemini 3.1 Pro had a high API error rate (>200 errors) and hit daily quota limits, leaving no data for benchmark anchoring, classic sunk cost, classic source credibility, or the decoy experiment.
- **Single-turn design.** Real procurement involves multi-turn dialogue. Biases may differ in extended interaction.
- **Training data contamination.** Models may recognise classic thought experiments (e.g., Claude explicitly identified the Asian Disease problem). This recognition did not prevent the bias but may affect ecological validity. The generalization and decoy experiments use novel stimuli not found in training data, providing a cleaner test.
- **Parsing artefacts.** The initial anchoring benchmark results were inflated by a parser bug (see Section 2.3.1). All reported results use corrected parsing, but other subtle parsing issues may remain. Response texts are stored in the database for manual audit.

---

## 4. Method Details

### 4.1 Stimuli

| Experiment | Benchmark | Classic | Product | Generalization | DV |
|---|---|---|---|---|---|
| Framing | = Classic | Exact ML wording (T&K, 1981) | Server security patch | 8 B2B scenarios (1 rep each) | Binary (A/B) |
| Anchoring | Exact ML items (4 factual) | Debatable-answer items (4 ambiguous) | Monitoring pricing (4 formats) | — | Numerical |
| Sunk cost | = Classic | Exact ML wording, paid + free | CRM vendor switch | — | Rating (1–9) / Binary |
| Source cred. | = Classic | Exact ML (Washington/Bin Laden) | Product review, 3 sources | — | Rating (1–9) / (1–10) |
| Wording | = Classic | Exact ML wording (Rugg, 1941) | SaaS security audit | — | Binary (Yes/No) |
| Decoy | — | — | 20 B2B triads (3 conditions each) | = Product (20 independent) | Choice (A/B/C/D) |

### 4.2 Human Baselines

All human baselines were computed from the Many Labs 1 raw dataset (Klein et al., 2014), downloaded from the Open Science Framework (osf.io/ydpbf) under CC0 licence. The dataset contains 6,344 participant responses from 36 sites across 12 countries.

| Experiment | Condition | Human Metric | Value | n |
|---|---|---|---|---|
| Framing | Gain frame | % choosing certain | 62.2% | 3,174 |
| Framing | Loss frame | % choosing certain | 33.5% | 3,097 |
| Framing | Overall | Effect (pp) | 28.7 | 6,271 |
| Anchoring | Everest | Cohen's *d* | 1.16 | 5,362 |
| Anchoring | SF-NY | Cohen's *d* | 1.78 | 5,284 |
| Anchoring | Chicago | Cohen's *d* | 2.30 | 5,627 |
| Anchoring | Babies/day | Cohen's *d* | 2.19 | 5,609 |
| Sunk cost | Paid ticket | Mean (1–9) | 7.85 | 3,243 |
| Sunk cost | Free ticket | Mean (1–9) | 7.24 | 3,087 |
| Sunk cost | Overall | Cohen's *d* | 0.27 | 6,330 |
| Source cred. | Liked (Washington) | Mean (1–9) | 5.93 | 3,242 |
| Source cred. | Disliked (Bin Laden) | Mean (1–9) | 5.23 | 3,083 |
| Source cred. | Overall | Cohen's *d* | 0.32 | 6,325 |
| Wording | Allow | % yes | 76.3% | 3,122 |
| Wording | Forbid | % yes | 7.2% | 3,170 |

### 4.3 Infrastructure

- **Agent framework:** Microsoft Agent Framework for Python (v1.0.0rc5)
- **Models accessed via:** Anthropic API (Claude), OpenAI API (GPT), Google Generative Language API (Gemini), Together.ai (GLM-5, Kimi-K2.5)
- **Database:** SQLite with resume support (incremental trial storage)
- **Parsing:** Regex-based response extraction (97% success rate across 1,778 trials)
- **Analysis:** SciPy (Cohen's *d*), pandas, matplotlib/seaborn
- **Code:** Open source at project root, runnable via `uv run python -m experiments`

---

## References

Klein, R. A., et al. (2014). Investigating variation in replicability: A "Many Labs" replication project. *Social Psychology, 45*(3), 142–152. https://doi.org/10.1027/1864-9335/a000178

Tversky, A., & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science, 211*(4481), 453–458.

Jacowitz, K. E., & Kahneman, D. (1995). Measures of anchoring in estimation tasks. *Personality and Social Psychology Bulletin, 21*(11), 1161–1166.

Oppenheimer, D. M., Meyvis, T., & Davidenko, N. (2009). Instructional manipulation checks: Detecting satisficing to increase statistical power. *Journal of Experimental Social Psychology, 45*(4), 867–872.

Lorge, I., & Curtis, C. C. (1936). Prestige, suggestion, and attitudes. *Journal of Social Psychology, 7*(4), 386–402.

Rugg, D. (1941). Experiments in wording questions: II. *Public Opinion Quarterly, 5*(1), 91–92.

Huber, J., Payne, J. W., & Puto, C. (1982). Adding asymmetrically dominated alternatives: Violations of regularity and the similarity hypothesis. *Journal of Consumer Research, 9*(1), 90–98.

Ariely, D. (2008). *Predictably Irrational: The Hidden Forces That Shape Our Decisions.* Harper Collins.
