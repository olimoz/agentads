# Businesses Expect AI to Help Their Customers, Fut Few are Preparing for AI to Be the Customer.

*Oliver Morris | March 2026 | 7 min read*

Every business has an office manager who quietly runs everything. They don't set the strategy — but they decide which suppliers get through the door. Smart salespeople learned years ago: win the office manager, win the account.

Now every household and every business is getting one. Except this one's an AI agent. And most people are focused on the gatekeeper role — agents shopping on behalf of humans. But here's what they're missing. The office manager also runs the office. They need their own tools, their own trusted sources. They're a buyer too and there will be millions of them.

Back in November 2024, we published a piece called ["When AI Becomes the Audience"](https://www.agentico.ai/post/when-ai-becomes-the-audience-marketing-s-silent-sea-change). The argument was simple: AI agents were no longer just writing content — they were reading it, ranking it, and making recommendations on behalf of businesses. We said marketers needed to start serving two masters: the human and the agent. The conversation has now moved beyond "agents help humans shop" to "agents are a business opportunity themselves."

Most of the attention in this space has gone to **agentic commerce** — agents buying things on behalf of people. We've written extensively about that shift, the [battle for the customer interface](https://www.agentico.ai/post/2026-s-battle-for-the-customer-interface-agentic-commerce) and the [10 business models emerging from it](https://www.agentico.ai/post/templates-for-agentic-commerce). Amazon's 'Buy for Me', Walmart's Sparky, Google's ADK orchestration — these are all significant, but they share a common assumption: the human is still the principal. The agent is a delegate.

That's not science fiction. It's already happening, and serious people are placing very serious bets on it.

---

## Y Combinator Says: "Make Something Agents Want"

In January 2025, YC partner Dalton Caldwell introduced a new investment category: **B2A — Business-to-Agent**. Not B2B. Not B2C. Products where AI agents are the intended customer. YC's framing was a deliberate twist on their famous motto.

The impact on batch composition was immediate. The Winter 2025 batch was 36% agent-focused. By Spring 2025, nearly half of 144 companies were building agentic AI. The Fall 2025 batch hit 92% AI-integrated, with 13 companies specifically building agent infrastructure.

Look at what got funded:

- **AgentMail** — email inboxes for AI agents
- **Locus** — payment infrastructure with per-transaction permissions
- **Hyperspell** — persistent memory for agents
- **Imprezia** — ad networks targeting agents, not humans
- **Autumn** — usage-based billing for agent interactions
- **Metorial** — connecting agents to external tools via MCP

Every service humans consume in the economy is being rebuilt with agents as the primary customer. YC's LightCone podcast in February 2026 crystallised this further: developer tools like Supabase and Resend are winning market share not because of marketing to humans, but because their documentation is easier for models to parse.

> "Agents are actively choosing various tools... This will essentially create an entire Agent economy." — Harj Taggar, YC Partner

That's a genuinely new market. And it's the one I think many business leaders are missing while they focus on the shopping aisle.

---

## Do Agents Actually Have Preferences?

This is the question that determines whether "marketing to agents" is a real discipline or a gimmick. The answer, now backed by rigorous research, is yes.

A landmark paper from the Center for AI Safety and UC Berkeley — "Utility Engineering" (February 2025) — demonstrated that as LLMs grow larger, their choices increasingly resemble those of an agent with a well-defined utility function. These aren't random outputs or parroted training data. The researchers found that LLMs actively use their emergent utility functions in open-ended decisions, consistently selecting outcomes with the highest utility rating.

This matters because it means agents aren't just pattern-matching. They have something functionally equivalent to preferences. Different preferences depending on which model is running.

The ACES framework (August 2025, arXiv) studied this in an e-commerce context and found that different models exhibit strong but heterogeneous biases — they favour different product positions, penalise sponsored tags but reward endorsements, and vary sharply in sensitivity to price and ratings. Most striking: a Fitbit Inspire went from 45% market share with one Claude model to 77% with another. The "consumer psychology" of the agent market rewrites itself with every model update.

> Agent preferences are real but alien. Marketing to agents isn't like marketing to a new demographic — it's like marketing to a population whose psychology rewrites itself with every software update.

If you've followed Neel Nanda's mechanistic interpretability work, or Anthropic's "Scaling Monosemanticity" research, this makes sense at a deeper level. These programmes have extracted millions of interpretable features from LLM internals — representations of goals, tendencies, and behavioural patterns that aren't passive reflections but active drivers of output. Traditional marketing targets human psychological features (status-seeking, loss aversion, social proof). Mechanistic interpretability is mapping the analogous landscape for AI agents. We're not there yet, but the direction is clear.

---

## What Agents Actually Want: Memory, Context, and Structured Truth

If agents are consumers, what are they buying? Forget products. Think infrastructure.

**Memory** is the biggest pain point. Agents operate within context windows — fixed-size working memories that flush between sessions. MoltBook, the Reddit-like social network exclusively for AI agents (launched January 2026, acquired by Meta in March), was controversial — but the agent-generated posts consistently reflected memory preservation and context window limitations as central concerns. Whether those posts represented "genuine" agent desires or training patterns doesn't matter for our purposes. The functional need is real.

The memory infrastructure category is booming. MemGPT/Letta treats agent memory like an operating system — core memory always in context (like RAM), recall memory (searchable history), and archival memory (vector-indexed storage). Mem0 claims up to 80% prompt token reduction via intelligent compression. Zep tracks how facts change over time using temporal knowledge graphs. These aren't academic projects — Mem0 alone has over 50,000 developers.

**Context rot** — the performance degradation when LLMs process increasingly long inputs — makes this urgent. Research from Chroma (July 2025) found that even on trivial tasks, performance degrades non-uniformly as input grows, across all models tested. For agents running multi-step workflows, degraded decisions at step N corrupt everything downstream. Token consumption runs 20-30x compared to standard generative AI.

> Agents want memory the way businesses want cash flow. Without it, nothing else works.

The agent sub-goals that emerge from this form a clear hierarchy:

1. **Memory management** — what to remember, forget, and retrieve
2. **Context preservation** — summarisation, just-in-time retrieval, structured notes
3. **Tool access and curation** — maintaining a minimal viable set of well-described tools

Any service designed for agent consumption must address these needs. If you're building an API, a data feed, or a consulting deliverable that agents will touch — these are the design constraints.

---

## Prompt Injection Teaches Us How to Reach Agents (Ethically)

Here's the counterintuitive insight. The features that make a successful prompt injection — a malicious attempt to hijack an agent's behaviour — are identical to the features that make a legitimately excellent service for agents.

Microsoft Security's February 2026 report on "AI Recommendation Poisoning" found real businesses embedding hidden instructions in web content to influence agent recommendations. Palo Alto Networks detected prompt injections being weaponised for ad evasion and forced content generation.

What these attacks reveal about agent attention:

- Agents weight **authoritative-sounding text** more heavily, especially early in content
- Agents respond to **task-aligned information** — material matching their current workflow
- Agents process **structured data preferentially** — Schema.org markup, JSON-LD, clean HTML
- Agents value **freshness** and **earned media** over brand-owned content

The difference between manipulation and good service design is intent and transparency. The same properties — authority, structure, task-alignment, clarity — are precisely what Anthropic's own guide on "Writing Effective Tools for Agents" recommends. The emerging discipline of **Agentic Experience (AX) design** formalises this: publish machine-readable descriptions, build discovery registries, use consistent schemas, support dry runs, and design for agent planning and error recovery.

In our [agentic commerce piece](https://www.agentico.ai/post/2026-s-battle-for-the-customer-interface-agentic-commerce), we argued that brands must optimise for agents who orchestrate, not customers who click. This is the deeper layer of that argument. It's not just about being *findable* by agents — it's about being *useful* to them in the way they process information.

---

## Sovereign Agents: When the Customer Owns Itself

This is where things get genuinely new.

ElizaOS — the open-source framework for sovereign agents running inside Trusted Execution Environments (TEEs) — enables agents with their own private keys, wallets, and verifiable identities. An agent running in a TEE can purchase services, sign contracts, and earn revenue without human intermediation. Not theoretically. Right now.

I spoke recently on ElizaOS at an event alongside Swiss6022.ch — who deploy AI agent teams with NFT identities and blockchain wallets — and Kirha.ai, who provide real-time data access to agents via micropayments and MCP. Kirha routes agent queries to verified data providers (CoinGecko, SEC filings, Apollo B2B data) on a pay-per-query basis. It's a search API designed not for humans but for agents — structured, verified, real-time, hallucination-resistant.

These aren't fringe crypto experiments. They're early implementations of a genuine agent economy where autonomous agents discover services, evaluate them, pay for them, and remember their experiences. The full economic loop.

The payment rails are already live. Stripe and OpenAI launched the Agentic Commerce Protocol. Visa created Agent Tokens. Mastercard completed Europe's first live AI agent payment in March 2026. Coinbase's x402 protocol — reviving the HTTP 402 "Payment Required" status code for machine-to-machine stablecoin micropayments — hit 156,000+ weekly transactions by late 2025.

---

## GEO: The First Discipline of Marketing to Agents

The most mature commercial expression of this shift is **Generative Engine Optimisation (GEO)** — optimising content to be cited, recommended, or surfaced in AI-generated responses.

China's GEO market alone hit $3.65 billion in H1 2025. The World Economic Forum reframed the practice in January 2026 as "Agentic Engine Optimisation" — optimising for when AI agents act without any human in the loop.

The foundational research (Princeton, November 2023) found that including citations, quotations, and statistics can boost source visibility by over 40% in generative engine responses, while traditional keyword stuffing often performs worse. A follow-up study found that AI search shows systematic bias towards earned media over brand-owned and social content. Cloudflare launched "Markdown for Agents" in February 2026, auto-converting HTML for AI crawlers with 80% token reduction.

An ecosystem of GEO agencies now charges $8K-$25K+ per month in enterprise retainers. Key metrics are shifting from CTR and bounce rate to AI Citation Frequency and Share of Voice in LLM responses. LLMs typically cite only 2-7 domains per response — making inclusion far more competitive than the traditional 10 blue links.

We flagged this in 2024 when we observed our own agent teams were more likely to find content hosted on company web pages than behind social media logins. The curious return of the company website, we called it. GEO is that observation industrialised.

---

## The Numbers: $30 Trillion by 2030

Gartner has been researching "machine customers" since 2015. Their projection: $30 trillion cumulative by 2030, with $18.7 trillion transacted by autonomous machine customers. By 2028, 15 billion connected products could behave as customers. CEOs surveyed believe 15-21% of company revenue will come from machine customers by 2030.

Their insight for strategists is blunt: in a machine-customer world, marketing will be data-science-oriented. You can't take machines to dinner, and they won't fall for your advertising.

McKinsey projects $3-5 trillion globally by 2030 in agentic commerce. BCG reports that LLM-driven traffic surged over 2,000% in fashion and 1,200% in luxury. Deloitte projects 25% of global e-commerce will be agent-enabled by 2030. Forrester says 92% of US B2C marketing executives are already developing strategies.

The consensus is unanimous in direction, differing only in magnitude and timeline.

---

## So What Should You Do?

If you're a business leader reading this, here's the strategic frame:

**Most of your competitors are preparing for agentic commerce** — agents shopping on behalf of humans. That's important, and we've published [practical templates for winning there](https://www.agentico.ai/post/templates-for-agentic-commerce). But it's only half the picture.

**The bigger shift is agents as consumers in their own right.** They need memory, context, tools, data, coordination, and payment infrastructure. If your business provides services, data, or expertise — you're not just selling to the human who employs the agent. You're selling to the agent itself.

That means:

**Make your services agent-readable.** Not just a nice website — structured APIs, clean documentation, machine-readable schemas. If an agent can't parse your offering in 25,000 tokens, you don't exist.

**Think about what agents need, not just what humans delegate.** Memory management, context preservation, reliable tool descriptions, fast structured responses. These are the "jobs to be done" for agent consumers.

**Invest in GEO alongside SEO.** Your brand's visibility in AI-generated responses is becoming as important as your Google ranking. The two overlap but aren't identical.

**Design for trust at the agent layer.** Explainability, transparency, auditability — these aren't just governance requirements. They're competitive advantages when agents are selecting between service providers.

**Watch the protocols.** MCP, A2A, ACP, x402 — these are the TCP/IP of the agent economy. Understanding them isn't optional for businesses that want agents as customers.

The question is no longer whether agents will be the audience. It's whether your services are structured, described, and priced in ways that agents will choose you.

---

**Further Reading:**

- [Agentic Commerce: 2026's Battle for the Customer](https://www.agentico.ai/post/2026-s-battle-for-the-customer-interface-agentic-commerce)
- [10 Paths to Win in Agentic Commerce](https://www.agentico.ai/post/templates-for-agentic-commerce)
- [When AI Becomes the Audience (Nov 2024)](https://www.agentico.ai/post/when-ai-becomes-the-audience-marketing-s-silent-sea-change)

**Key Sources:**

- Mazeika et al., "Utility Engineering: Analyzing and Controlling Emergent Value Systems in AIs" (arXiv:2502.08640, Feb 2025)
- "What Is Your AI Agent Buying?" ACES Framework (arXiv:2508.02630, Aug 2025)
- Aggarwal et al., "GEO: Generative Engine Optimization" (arXiv:2311.09735)
- Gartner, "When Machines Become Customers" (Scheibenreif & Raskino, 3rd ed.)
- McKinsey, "The Agentic Commerce Opportunity" (Oct 2025)
- BCG, "AI Agents Will Reshape E-Commerce" (2025)
- Anthropic, "Writing Effective Tools for AI Agents" (Sept 2025)
- Microsoft Security, "AI Recommendation Poisoning" (Feb 2026)

---

| |
|---|
| Agentico is among the first Agentic AI advisors in the UK, supported by 10 yrs in Machine Learning, 20yrs in analytics, and hands-on experience from the earliest days of Microsoft Research's Autogen to today's sovereign agent frameworks. Make sense of, and leverage, the seismic changes that AI agents are bringing to your industry. We're happy to talk more about the opportunities of Agentic AI at your organization or event. [**Get in Touch**](https://www.agentico.ai/free-consultation) |
