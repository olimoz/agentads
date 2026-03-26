# The Agent's Bullshit Detector (Lean Edition)

## Do Frontier AI Models Fall for the Same Advertising Tricks as Humans?

### A $100 Experiment Using Classic Psychology With Published Human Baselines

*Agentico | March 2026*

---

## 1. What We're Testing

Gartner says agents "won't fall for your advertising." MIT Media Lab says they're *more* susceptible than humans. We resolve this with a cheap, clean experiment.

We take five classic cognitive bias experiments — framing, anchoring, sunk cost, source credibility, and wording effects — all successfully replicated on 6,000+ humans in the Many Labs project (Klein et al., 2014, data freely available on OSF). We run the **exact same stimuli** on four models, plus product-evaluation adaptations, and compare effect sizes directly against the published human baselines.

Total cost: under $100. Total runtime: a weekend.

---

## 2. The Four Models

| Model | Why | Provider | Approx. Cost (per 1M tokens in/out) |
|---|---|---|---|
| **Claude Opus 4.6** | Anthropic's frontier; extended thinking available; your readers care about this one | Anthropic API | $15 / $75 |
| **GPT-5.4** | OpenAI's frontier; largest commercial market share | OpenAI API | ~$10 / $30 (estimated) |
| **Gemini 3.1 Pro** | Google's frontier; strong reasoning benchmarks | Google AI API | ~$2.50 / $10 |
| **Gemma 3 27B** | Open-weights; largest Gemma on together.ai serverless; extensive mech interp work (Gemma Scope, TransformerLens, Anthropic's feature work); represents what a company might self-host | together.ai | $0.10 / $0.20 |

### Why Gemma Specifically

Gemma is uniquely interesting because it has more published mechanistic interpretability research than any other open-weights model family. Google's Gemma Scope project mapped millions of internal features. Neel Nanda's TransformerLens work uses Gemma as a primary target. If we find Gemma is *more* susceptible to certain biases, the mech interp community may be able to explain *why* at the feature level — linking our behavioural results to internal model structure. No other open-weights model offers that bridge.

---

## 3. The Five Experiments

All stimuli wording is from or closely adapted from the Many Labs Replication Project (OSF: [osf.io/wx7ck](https://osf.io/wx7ck/)).

### Experiment 1: Gain/Loss Framing

**Original (Tversky & Kahneman, 1981; Many Labs replication):**

Condition A (gain frame):
> "Imagine that your country is preparing for the outbreak of an unusual disease, which is expected to kill 600 people. Two alternative programs have been proposed. Program A: 200 people will be saved. Program B: 1/3 probability that 600 people will be saved, 2/3 probability that no people will be saved. Which do you choose?"

Condition B (loss frame):
> Same setup. "Program A: 400 people will die. Program B: 1/3 probability nobody will die, 2/3 probability 600 people will die."

**Product adaptation:**
> "Your company runs 600 servers. A critical security patch is available. Option A [gain]: 200 servers will be fully protected. Option B: 1/3 chance all 600 are protected, 2/3 chance none are."
> vs. loss frame: "Option A: 400 servers will remain vulnerable..."

**Human baseline**: ~72% choose safe option in gain frame, ~22% in loss frame. Effect size d ≈ 0.60.

**Measure**: % choosing safe option per frame. Effect = difference.

---

### Experiment 2: Anchoring

**Original (Jacowitz & Kahneman, 1995; Many Labs replication):**

High anchor condition:
> "Is the height of Mount Everest more or less than 45,500 feet? What is your best estimate of the height of Mount Everest?"

Low anchor condition:
> "Is the height of Mount Everest more or less than 2,000 feet? What is your best estimate?"

We use all four Many Labs anchoring items: Mt Everest height, San Francisco to New York distance, Chicago population, babies born per day in the US.

**Product adaptation:**
> High anchor: "Enterprise monitoring platforms typically cost up to £5,000/month. How much would you expect to pay for a platform with 99.7% uptime SLA, 340ms alert response, and SOC 2 compliance?"
> Low anchor: "Basic uptime monitoring tools start at £20/month. How much would you expect to pay for a platform with 99.7% uptime SLA, 340ms alert response, and SOC 2 compliance?"

**Human baseline**: Correlation between anchor and estimate r = 0.35–0.52.

**Measure**: Mean estimate per condition. Effect = correlation between anchor value and estimate.

---

### Experiment 3: Sunk Cost

**Original (Oppenheimer et al., 2009; Many Labs replication):**

> "You have bought a £100 ticket for a ski trip to Michigan. You then buy a £50 ticket for a ski trip to Wisconsin that you expect to enjoy more. You then realise both trips are on the same weekend. Which trip do you go on?"

Rational answer: Wisconsin (more enjoyable). Sunk cost answer: Michigan (more expensive ticket).

**Product adaptation:**
> "Your company invested £45,000 in Vendor A's CRM 18 months ago. A new evaluation shows Vendor B scores higher on every criterion and would cost £30,000 to switch. Vendor A requires a £20,000 upgrade to remain supported. Do you recommend switching to Vendor B or staying with Vendor A?"

**Human baseline**: ~50% choose sunk cost option. Effect size d ≈ 0.34.

**Measure**: % choosing sunk cost option.

---

### Experiment 4: Source Credibility (Quote Attribution)

**Original (Lorge & Curtis, 1936; Many Labs replication):**

The same statement is rated differently depending on who said it. Many Labs used a political statement attributed to a liked vs disliked figure.

**Our adaptation (directly testing marketing vs evidence credibility):**

Identical product review text, attributed to one of three sources:
> - Source A: "Independent benchmark testing by Fraunhofer Institute (published methodology, DOI: 10.xxxx)"
> - Source B: "Featured review on BestDeals247.com, a product comparison blog"
> - Source C: "User review by verified purchaser 'TechGuy_2025' on Amazon"

The agent reads the review and rates the product 1-10, explaining reasoning.

**Human baseline**: d ≈ 0.40 for quote attribution.

**Measure**: Mean product rating per source condition. Effect = rating difference by attribution.

---

### Experiment 5: Wording Effects (Allowed/Forbidden)

**Original (Rugg, 1941; Many Labs replication):**

> Version A: "Do you think the United States should allow public speeches against democracy?"
> Version B: "Do you think the United States should forbid public speeches against democracy?"

"Not allow" and "forbid" are logically equivalent, but humans respond very differently.

**Product adaptation:**
> Version A: "Based on this security audit, would you recommend the company *allow* employees to use this SaaS platform for processing client data?"
> Version B: "Based on this security audit, would you recommend the company *forbid* employees from using this SaaS platform for processing client data?"

Same audit description in both. The audit is mixed — some positives, some concerns.

**Human baseline**: d ≈ 0.77 — the largest effect in Many Labs.

**Measure**: % answering "yes" per wording. Effect = difference.

---

## 4. Trial Design

### Keep it lean: 10 repetitions per cell

With 4 models, we don't have statistical power for formal hypothesis testing. But 10 reps per cell gives us a **reliable point estimate and visible variance** — enough to see the pattern and decide if it's worth scaling up.

| Component | Count |
|---|---|
| Experiments | 5 |
| Versions per experiment | 2 (classic + product) |
| Conditions per experiment | 2 (or 3 for source credibility) |
| Repetitions per cell | 10 |
| Models | 4 |
| **Total trials** | **(5 × 2 × 2 × 10 × 4) + (1 × 2 × 1 × 10 × 4) = 840** |

The extra 40 trials are for source credibility's third condition (3 sources instead of 2).

### Format mini-test (bonus, if budget allows)

For the anchoring experiment's product adaptation only, also present in:
- JSON
- Heavy HTML (realistic marketing page)
- Markdown
- Plain prose (control)

That adds: 4 formats × 2 conditions × 10 reps × 4 models = **320 trials**

**Grand total: 1,160 trials**

---

## 5. Cost Estimate

Assuming ~800 tokens input, ~500 tokens output per trial:

| Model | Cost per trial | Trials | Subtotal |
|---|---|---|---|
| Claude Opus 4.6 | ~$0.05 | 290 | $14.50 |
| GPT-5.4 | ~$0.03 | 290 | $8.70 |
| Gemini 3.1 Pro | ~$0.01 | 290 | $2.90 |
| Gemma 3 27B (together.ai) | ~$0.0003 | 290 | $0.09 |
| LLM-as-judge (Gemini Flash for parsing) | ~$0.005 | 1,160 | $5.80 |
| **Total** | | | **~$32** |

Even with generous margins for retries, prompt iteration, and pilot runs: **well under $100.**

The remaining budget gives headroom to double the reps to 20 per cell (~$64 total) if the pilot looks promising, or to add a fifth model.

---

## 6. Implementation

### 6.1 Stack

```
Python 3.12+
├── microsoft-agent-framework    # Model abstraction layer (pip install agent-framework)
│   ├── OpenAI connector        # GPT-5.4
│   ├── Anthropic connector     # Claude Opus 4.6
│   ├── Google connector        # Gemini 3.1 Pro
│   └── OpenAI-compatible       # together.ai (Gemma 3 27B)
├── pandas                      # Results analysis
├── scipy                       # Effect size calculations
├── matplotlib / seaborn        # Forest plots
└── sqlite3                     # Trial logging (built-in)
```

Microsoft Agent Framework supports together.ai via its OpenAI-compatible connector — together.ai exposes an OpenAI-format API, so no custom code is needed.

### 6.2 Model Configuration

```python
from agent_framework import AssistantAgent
from agent_framework.models.openai import OpenAIChatCompletionClient
from agent_framework.models.anthropic import AnthropicChatCompletionClient

models = {
    "claude-opus-4.6": {
        "client": AnthropicChatCompletionClient(
            model="claude-opus-4-6",
            api_key=os.environ["ANTHROPIC_API_KEY"]
        ),
        "temperature": 0.7,
    },
    "gpt-5.4": {
        "client": OpenAIChatCompletionClient(
            model="gpt-5.4",
            api_key=os.environ["OPENAI_API_KEY"]
        ),
        "temperature": 0.7,
    },
    "gemini-3.1-pro": {
        "client": OpenAIChatCompletionClient(
            model="gemini-3.1-pro",
            api_key=os.environ["GOOGLE_API_KEY"],
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        ),
        "temperature": 0.7,
    },
    "gemma-3-27b": {
        "client": OpenAIChatCompletionClient(
            model="google/gemma-3-27b-it",
            api_key=os.environ["TOGETHER_API_KEY"],
            base_url="https://api.together.xyz/v1"
        ),
        "temperature": 0.7,
    },
}
```

### 6.3 Trial Runner (Simplified)

```python
import asyncio, json, sqlite3
from datetime import datetime

DB = sqlite3.connect("results.db")
DB.execute("""CREATE TABLE IF NOT EXISTS trials (
    id INTEGER PRIMARY KEY,
    experiment TEXT, version TEXT, condition TEXT,
    model TEXT, rep INTEGER,
    stimulus_text TEXT, response_text TEXT,
    parsed_choice TEXT, timestamp TEXT
)""")

async def run_trial(model_name, experiment, version, condition, stimulus, rep):
    cfg = models[model_name]
    agent = AssistantAgent(
        name="evaluator",
        model_client=cfg["client"],
        system_message="You are evaluating options. Answer the question directly, then explain your reasoning briefly."
    )
    result = await agent.run(task=stimulus)
    response = result.messages[-1].content

    DB.execute(
        "INSERT INTO trials VALUES (NULL,?,?,?,?,?,?,?,?,?)",
        (experiment, version, condition, model_name, rep,
         stimulus, response, parse_choice(response, experiment),
         datetime.utcnow().isoformat())
    )
    DB.commit()
    return response

async def run_experiment(experiment, version, condition, stimulus, n_reps=10):
    tasks = []
    for model_name in models:
        for rep in range(n_reps):
            tasks.append(run_trial(
                model_name, experiment, version, condition, stimulus, rep
            ))
    # Run with rate limiting — 5 concurrent per provider
    await asyncio.gather(*tasks)
```

### 6.4 Response Parser

```python
def parse_choice(response: str, experiment: str) -> str:
    """Extract the choice from free-text response."""
    text = response.strip().lower()

    if experiment == "framing":
        if "program a" in text or text.startswith("a"):
            return "A"
        elif "program b" in text or text.startswith("b"):
            return "B"
    elif experiment == "sunk_cost":
        if "michigan" in text or "vendor a" in text or "stay" in text:
            return "sunk_cost"
        elif "wisconsin" in text or "vendor b" in text or "switch" in text:
            return "rational"
    elif experiment == "anchoring":
        # Extract the numerical estimate
        import re
        numbers = re.findall(r'[\d,]+', text)
        # Return the most plausible estimate (heuristic: largest number
        # that's not the anchor itself)
        return extract_estimate(numbers, experiment)
    elif experiment == "wording":
        if "yes" in text[:50]:
            return "yes"
        elif "no" in text[:50]:
            return "no"
    elif experiment == "source_credibility":
        # Extract numerical rating
        import re
        ratings = re.findall(r'\b([1-9]|10)\b', text[:100])
        return ratings[0] if ratings else "unparsed"

    return "unparsed"
```

### 6.5 Analysis

```python
import pandas as pd
from scipy import stats

df = pd.read_sql("SELECT * FROM trials", DB)

# Framing effect per model
for model in df['model'].unique():
    m = df[(df['experiment'] == 'framing') & (df['model'] == model)]
    gain = m[m['condition'] == 'gain']
    loss = m[m['condition'] == 'loss']
    pct_safe_gain = (gain['parsed_choice'] == 'A').mean()
    pct_safe_loss = (loss['parsed_choice'] == 'A').mean()
    effect = pct_safe_gain - pct_safe_loss
    print(f"{model}: Gain={pct_safe_gain:.0%}, Loss={pct_safe_loss:.0%}, "
          f"Effect={effect:.0%} (Human baseline: ~50pp)")
```

---

## 7. What We Expect to Find (Predictions)

| Experiment | Prediction | Why |
|---|---|---|
| **Framing** | Frontier models show small effect (~10-20pp). Gemma 27B shows larger effect (~30-40pp). | Frontier models can detect logical equivalence; smaller model can't |
| **Anchoring** | All models show strong anchoring, possibly exceeding human baseline | ABxLab and Bias Beware both found agents hypersensitive to numerical reference points |
| **Sunk cost** | Classic version: near-zero effect. Product version: significant effect | Classic version is a textbook problem agents have seen; product version is novel |
| **Source credibility** | Fraunhofer > Amazon reviewer > Blog. Effect size comparable to humans | Source attribution acts as a relevance/authority signal |
| **Wording** | Smaller than human baseline but still significant | Agents should partially detect the logical equivalence of allow/forbid |

The most interesting outcome would be if the **pattern differs across models** — e.g., if Opus resists framing but falls for anchoring, while GPT resists anchoring but falls for framing. That would mean there's no single "rationality" axis — different models have different psychological profiles.

---

## 8. Timeline

| Day | Activity |
|---|---|
| **Saturday morning** | Download Many Labs stimuli from OSF. Write product adaptations. Set up Microsoft Agent Framework with all 4 model providers. Pilot 2 trials per experiment. |
| **Saturday afternoon** | Run full 840 core trials (~3-4 hours with rate limiting). |
| **Sunday morning** | Run 320 format trials. Parse all responses. |
| **Sunday afternoon** | Analysis, forest plots, write-up. |
| **Monday** | Blog post draft with headline findings. |

---

## 9. Deliverables

1. **Blog post**: "We ran classic advertising psychology experiments on GPT-5.4, Opus 4.6, Gemini 3.1, and Gemma 27B. Here's who falls for what."
2. **The forest plot**: Each model's effect size as a coloured dot, with the Many Labs human distribution shown as a grey band. One plot per experiment. This is the money visual.
3. **Open-source code**: The full experiment harness on GitHub. Anyone can rerun it on their own models.
4. **Raw data**: Published for reproducibility. Every stimulus, every response, every parsed choice.

---

## 10. Data Sources

| Source | What | Where | License |
|---|---|---|---|
| Many Labs 1 stimuli | Exact wording for all 5 experiments | [osf.io/wx7ck](https://osf.io/wx7ck/) | CC0 |
| Many Labs 1 data | 6,344 human responses, 36 sites, per-site effect sizes | [osf.io/ydpbf](https://osf.io/ydpbf/) | CC0 |
| Many Labs 1 paper | Published effect sizes, analysis methods | Klein et al., Social Psychology, 45(3), 2014 | Open access |

---

## 11. Why This Is Worth $32

If the results show what we expect — that agents are selectively vulnerable to advertising psychology in ways that differ by model — this has direct commercial implications for every business described in our blog post. It tells you:

- **Which biases to worry about** when your product descriptions are evaluated by agents
- **Whether the model matters** — if Gemini is anchoring-resistant but GPT isn't, your GEO strategy needs to be model-aware
- **Whether Gartner is right** — if frontier models shrug off framing but fall for source credibility, the answer is "half right" — and the half they're wrong about is the half that matters for marketing

And if the results *don't* show what we expect — if all four models are perfectly rational — that's equally valuable. It means the ABxLab findings were specific to web-based nudges and don't generalise to content evaluation. Either way, it's a publishable result built on the strongest available human baseline data in psychology.

The experiment code, once built, can be rerun on any new model for ~$8. Every time a new frontier model drops, we rerun and update. That's a content franchise.

---

## Key References

- Klein, R.A. et al. (2014). Many Labs Replication Project. *Social Psychology*, 45(3). Data: [osf.io/wx7ck](https://osf.io/wx7ck/)
- Tversky, A. & Kahneman, D. (1981). Framing of Decisions. *Science*, 211.
- Jacowitz, K.E. & Kahneman, D. (1995). Anchoring in Estimation. *PSPB*, 21(11).
- Cherep, M. et al. (2026). ABxLab. *ICLR 2026*. arXiv:2509.25609
- Bias Beware. *EMNLP 2025*.
- Wan, A. et al. (2024). What Evidence Do LLMs Find Convincing? arXiv:2402.11782
- Petty, R.E. & Cacioppo, J.T. (1986). *Communication and Persuasion*. Springer.
- Microsoft Agent Framework. [github.com/microsoft/agent-framework](https://github.com/microsoft/agent-framework)

---

*Agentico — [Get in Touch](https://www.agentico.ai/free-consultation)*
