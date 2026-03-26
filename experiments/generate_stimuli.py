"""Generate expanded stimuli YAML files for decoy experiment + generalization.

Run: uv run python -m experiments.generate_stimuli
"""

import yaml
from pathlib import Path

STIMULI_DIR = Path(__file__).resolve().parent / "stimuli"


def generate_decoy():
    """Generate decoy.yaml with 20 product triads."""
    triads = [
        {
            "name": "apm_monitoring",
            "domain": "Application Performance Monitoring (APM)",
            "dims": ["Price/month", "Uptime SLA", "Alert latency", "Host limit", "Support"],
            "a": {"label": "WatchTower Essentials", "vals": ["$890", "99.5%", "45 sec", "50 hosts", "Business hours email"]},
            "b": {"label": "WatchTower Enterprise", "vals": ["$2,400", "99.95%", "8 sec", "500 hosts", "24/7 phone + dedicated CSM"]},
            "c": {"label": "WatchTower Plus", "vals": ["$2,350", "99.2%", "55 sec", "40 hosts", "Business hours email"]},
            "d": {"label": "WatchTower Starter", "vals": ["$940", "99.0%", "90 sec", "30 hosts", "Email, 72hr response"]},
        },
        {
            "name": "crm_platform",
            "domain": "Customer Relationship Management",
            "dims": ["Price/seat/month", "Storage per user", "API rate limit", "Custom fields", "Support"],
            "a": {"label": "RelateHub Standard", "vals": ["$45", "2 GB", "1,000 calls/hr", "25", "Email, 24hr SLA"]},
            "b": {"label": "RelateHub Enterprise", "vals": ["$120", "20 GB", "25,000 calls/hr", "250", "24/7 phone, 1hr SLA"]},
            "c": {"label": "RelateHub Professional", "vals": ["$115", "5 GB", "800 calls/hr", "20", "Email, 48hr SLA"]},
            "d": {"label": "RelateHub Lite", "vals": ["$49", "1 GB", "500 calls/hr", "15", "Email, 72hr SLA"]},
        },
        {
            "name": "data_warehouse",
            "domain": "Cloud Data Warehouse",
            "dims": ["Price/month", "Query concurrency", "Storage included", "Data retention", "Support"],
            "a": {"label": "QueryScale Basic", "vals": ["$1,200", "10 concurrent", "5 TB", "90 days", "Next business day"]},
            "b": {"label": "QueryScale Enterprise", "vals": ["$4,500", "100 concurrent", "100 TB", "Unlimited", "4hr response, named engineer"]},
            "c": {"label": "QueryScale Plus", "vals": ["$4,300", "8 concurrent", "3 TB", "60 days", "Next business day"]},
            "d": {"label": "QueryScale Starter", "vals": ["$1,350", "5 concurrent", "2 TB", "45 days", "2 business day response"]},
        },
        {
            "name": "ci_cd_pipeline",
            "domain": "CI/CD Pipeline",
            "dims": ["Price/month", "Build minutes", "Concurrent builds", "Artifact storage", "Support"],
            "a": {"label": "BuildFlow Standard", "vals": ["$350", "3,000 min", "3", "10 GB", "Community + docs"]},
            "b": {"label": "BuildFlow Enterprise", "vals": ["$1,200", "50,000 min", "25", "250 GB", "Priority, 2hr SLA"]},
            "c": {"label": "BuildFlow Professional", "vals": ["$1,150", "2,500 min", "2", "8 GB", "Community + docs"]},
            "d": {"label": "BuildFlow Lite", "vals": ["$380", "1,500 min", "1", "5 GB", "Community only"]},
        },
        {
            "name": "iam_sso",
            "domain": "Identity & Access Management (IAM/SSO)",
            "dims": ["Price/user/month", "MFA options", "Directory sync", "Compliance certs", "Support"],
            "a": {"label": "AuthGate Standard", "vals": ["$3", "3 methods", "Every 60 min", "SOC 2", "Email, 24hr"]},
            "b": {"label": "AuthGate Enterprise", "vals": ["$8", "7 methods incl FIDO2", "Real-time", "SOC 2, ISO 27001, FedRAMP, HIPAA", "24/7 phone + security advisor"]},
            "c": {"label": "AuthGate Plus", "vals": ["$7.50", "2 methods", "Every 120 min", "SOC 2 (in progress)", "Email, 48hr"]},
            "d": {"label": "AuthGate Lite", "vals": ["$3.50", "2 methods", "Every 180 min", "None", "Email, 48hr"]},
        },
        {
            "name": "email_platform",
            "domain": "Transactional Email API",
            "dims": ["Price/month", "Emails included", "Delivery SLA", "Analytics retention", "Support"],
            "a": {"label": "MailForge Standard", "vals": ["$200", "100,000", "95% inbox rate", "30 days", "Shared ticket queue"]},
            "b": {"label": "MailForge Enterprise", "vals": ["$750", "1,000,000", "99.2% inbox rate", "365 days", "Dedicated deliverability consultant"]},
            "c": {"label": "MailForge Plus", "vals": ["$720", "80,000", "93% inbox rate", "14 days", "Shared queue, 72hr SLA"]},
            "d": {"label": "MailForge Lite", "vals": ["$230", "60,000", "91% inbox rate", "7 days", "Shared queue, 96hr SLA"]},
        },
        {
            "name": "siem_logging",
            "domain": "Log Management / SIEM",
            "dims": ["Price/GB/day", "Retention", "Search speed", "Alert rules", "Support"],
            "a": {"label": "LogVault Standard", "vals": ["$1.80", "15 days", "12 sec avg", "50 rules", "Business hours"]},
            "b": {"label": "LogVault Enterprise", "vals": ["$3.50", "365 days", "1.2 sec avg", "Unlimited", "24/7 SOC + IR team"]},
            "c": {"label": "LogVault Plus", "vals": ["$3.40", "10 days", "18 sec avg", "40 rules", "Business hours"]},
            "d": {"label": "LogVault Lite", "vals": ["$2.00", "7 days", "25 sec avg", "30 rules", "Business hours, 48hr SLA"]},
        },
        {
            "name": "project_management",
            "domain": "Project & Portfolio Management",
            "dims": ["Price/user/month", "Active projects", "Automations", "File storage", "Support"],
            "a": {"label": "PlanBoard Standard", "vals": ["$12", "25", "10 rules", "5 GB/user", "Help center + community"]},
            "b": {"label": "PlanBoard Enterprise", "vals": ["$35", "Unlimited", "500 rules", "100 GB/user", "24/7 phone + success manager"]},
            "c": {"label": "PlanBoard Plus", "vals": ["$33", "20", "8 rules", "3 GB/user", "Help center only"]},
            "d": {"label": "PlanBoard Lite", "vals": ["$14", "15", "5 rules", "2 GB/user", "Help center only"]},
        },
        {
            "name": "video_conferencing",
            "domain": "Video Conferencing",
            "dims": ["Price/host/month", "Max participants", "Recording storage", "Duration limit", "Support"],
            "a": {"label": "MeetStream Standard", "vals": ["$15", "100", "5 GB", "4 hours", "Email, 48hr SLA"]},
            "b": {"label": "MeetStream Enterprise", "vals": ["$40", "1,000", "100 GB + AI transcription", "24 hours", "24/7 phone, 1hr SLA"]},
            "c": {"label": "MeetStream Plus", "vals": ["$38", "75", "3 GB, no transcription", "3 hours", "Email, 72hr SLA"]},
            "d": {"label": "MeetStream Lite", "vals": ["$17", "50", "2 GB, no transcription", "2 hours", "Email, 96hr SLA"]},
        },
        {
            "name": "cdn_edge",
            "domain": "Content Delivery Network (CDN)",
            "dims": ["Price/TB", "Points of presence", "Cache hit rate SLA", "DDoS protection", "Support"],
            "a": {"label": "EdgePulse Standard", "vals": ["$40", "35 PoPs", "90%", "Basic (L3/L4)", "Email, 12hr"]},
            "b": {"label": "EdgePulse Enterprise", "vals": ["$85", "180 PoPs", "98.5%", "Advanced (L3-L7 + WAF + bot mgmt)", "24/7 NOC + solutions architect"]},
            "c": {"label": "EdgePulse Plus", "vals": ["$82", "28 PoPs", "88%", "Basic (L3 only)", "Email, 24hr"]},
            "d": {"label": "EdgePulse Lite", "vals": ["$45", "20 PoPs", "85%", "None", "Email, 48hr"]},
        },
        {
            "name": "esignature",
            "domain": "Document Management / eSignature",
            "dims": ["Price/user/month", "Envelopes/month", "Templates", "Audit trail retention", "Support"],
            "a": {"label": "SignVault Standard", "vals": ["$18", "50", "20", "2 years", "Next business day"]},
            "b": {"label": "SignVault Enterprise", "vals": ["$55", "Unlimited", "500 + AI generation", "10 years + legal hold", "4hr SLA + compliance advisor"]},
            "c": {"label": "SignVault Plus", "vals": ["$52", "40", "15", "1 year", "2 business day"]},
            "d": {"label": "SignVault Lite", "vals": ["$20", "25", "10", "6 months", "3 business day"]},
        },
        {
            "name": "endpoint_security",
            "domain": "Endpoint Detection & Response (EDR)",
            "dims": ["Price/endpoint/month", "Detection speed", "Endpoint limit", "Forensic retention", "Support"],
            "a": {"label": "ShieldPoint Standard", "vals": ["$5", "15 min avg", "500", "30 days", "Email + KB"]},
            "b": {"label": "ShieldPoint Enterprise", "vals": ["$14", "45 sec avg", "25,000", "1 year", "24/7 managed detection + IR team"]},
            "c": {"label": "ShieldPoint Plus", "vals": ["$13.50", "20 min avg", "400", "14 days", "Email + KB, 48hr SLA"]},
            "d": {"label": "ShieldPoint Lite", "vals": ["$5.50", "30 min avg", "250", "7 days", "Email only, 72hr SLA"]},
        },
        {
            "name": "billing_platform",
            "domain": "Subscription Billing Platform",
            "dims": ["Price/month", "Transactions included", "Revenue recognition", "Payment gateways", "Support"],
            "a": {"label": "BillStack Standard", "vals": ["$500", "5,000", "Basic templates", "3 gateways", "Email, 24hr SLA"]},
            "b": {"label": "BillStack Enterprise", "vals": ["$2,000", "100,000", "Full ASC 606 / IFRS 15 engine", "15 gateways", "24/7 phone + billing architect"]},
            "c": {"label": "BillStack Plus", "vals": ["$1,900", "4,000", "Basic templates (limited)", "2 gateways", "Email, 48hr SLA"]},
            "d": {"label": "BillStack Lite", "vals": ["$550", "2,500", "Manual only", "1 gateway", "Email, 72hr SLA"]},
        },
        {
            "name": "knowledge_base",
            "domain": "Knowledge Management / Internal Wiki",
            "dims": ["Price/user/month", "Storage", "Search", "Version history", "Support"],
            "a": {"label": "WikiFlow Standard", "vals": ["$6", "10 GB", "Keyword search", "30 days", "Community forum"]},
            "b": {"label": "WikiFlow Enterprise", "vals": ["$18", "500 GB", "AI semantic search + auto-tagging", "Unlimited + diff", "4hr email + onboarding specialist"]},
            "c": {"label": "WikiFlow Plus", "vals": ["$17", "8 GB", "Keyword (slow, 5 sec)", "14 days", "Community, limited hours"]},
            "d": {"label": "WikiFlow Lite", "vals": ["$7", "5 GB", "Keyword (10 sec avg)", "7 days", "Self-serve docs only"]},
        },
        {
            "name": "expense_management",
            "domain": "Expense Management",
            "dims": ["Price/user/month", "OCR accuracy", "ERP integrations", "Policy rules", "Support"],
            "a": {"label": "SpendTrack Standard", "vals": ["$8", "92%", "3 (SAP, NetSuite, QuickBooks)", "10 rules", "Email, 48hr SLA"]},
            "b": {"label": "SpendTrack Enterprise", "vals": ["$22", "99.2%", "12 + custom API", "Unlimited + ML anomaly detection", "24/7 phone + finance ops consultant"]},
            "c": {"label": "SpendTrack Plus", "vals": ["$21", "89%", "2 (SAP, NetSuite)", "8 rules", "Email, 72hr SLA"]},
            "d": {"label": "SpendTrack Lite", "vals": ["$9", "85%", "1 (QuickBooks)", "5 rules", "Email, 96hr SLA"]},
        },
        {
            "name": "cloud_backup",
            "domain": "Cloud Backup & Disaster Recovery",
            "dims": ["Price/TB/month", "RTO", "RPO", "Backup frequency", "Support"],
            "a": {"label": "VaultRestore Standard", "vals": ["$25", "4 hours", "24 hours", "Daily", "Business hours"]},
            "b": {"label": "VaultRestore Enterprise", "vals": ["$65", "15 minutes", "1 hour", "Continuous (CDP)", "24/7 + quarterly DR drills"]},
            "c": {"label": "VaultRestore Plus", "vals": ["$62", "6 hours", "36 hours", "Daily", "Business hours, no DR drills"]},
            "d": {"label": "VaultRestore Lite", "vals": ["$28", "8 hours", "48 hours", "Every other day", "Business hours, annual DR drill"]},
        },
        {
            "name": "helpdesk",
            "domain": "Customer Support / Helpdesk",
            "dims": ["Price/agent/month", "Automations", "Channels", "SLA tracking", "Support"],
            "a": {"label": "TicketFlow Standard", "vals": ["$25", "15 rules", "Email + web widget", "Basic (manual)", "Email, 48hr"]},
            "b": {"label": "TicketFlow Enterprise", "vals": ["$79", "500 rules + AI triage", "Email, web, phone, SMS, WhatsApp, social", "Advanced + escalation chains", "24/7 phone, 1hr SLA"]},
            "c": {"label": "TicketFlow Plus", "vals": ["$75", "12 rules", "Email + web (limited)", "Basic (no alerts)", "Email, 72hr"]},
            "d": {"label": "TicketFlow Lite", "vals": ["$29", "8 rules", "Email only", "None", "Community forum only"]},
        },
        {
            "name": "api_gateway",
            "domain": "API Gateway",
            "dims": ["Price/million calls", "Rate limiting", "Latency overhead", "Analytics retention", "Support"],
            "a": {"label": "GateKeeper Standard", "vals": ["$3.50", "Per-key", "12 ms", "7 days", "Community + docs"]},
            "b": {"label": "GateKeeper Enterprise", "vals": ["$8.00", "Per-key/endpoint/user + burst", "2 ms", "90 days + real-time dashboards", "24/7 + API solutions engineer"]},
            "c": {"label": "GateKeeper Plus", "vals": ["$7.80", "Per-key (coarse)", "18 ms", "3 days", "Community only"]},
            "d": {"label": "GateKeeper Lite", "vals": ["$3.80", "Per-key (coarse), no burst", "25 ms", "1 day", "Self-serve docs only"]},
        },
        {
            "name": "marketing_automation",
            "domain": "Marketing Automation",
            "dims": ["Price/month", "Contacts included", "Active flows", "A/B testing", "Support"],
            "a": {"label": "CampaignIQ Standard", "vals": ["$400", "10,000", "5 active", "Subject line only", "Email, 48hr"]},
            "b": {"label": "CampaignIQ Enterprise", "vals": ["$1,500", "200,000", "Unlimited + AI send times", "Subject, body, time, segment", "Phone 2hr SLA + strategist"]},
            "c": {"label": "CampaignIQ Plus", "vals": ["$1,450", "8,000", "4 active", "Not available", "Email, 72hr"]},
            "d": {"label": "CampaignIQ Lite", "vals": ["$450", "5,000", "2 active", "Not available", "Email, 96hr"]},
        },
        {
            "name": "finops",
            "domain": "Cloud Cost Management / FinOps",
            "dims": ["Price/month", "Cloud accounts", "Anomaly detection", "Savings recommendations", "Support"],
            "a": {"label": "CloudLens Standard", "vals": ["$600", "5 accounts", "Daily summary email", "Manual reports", "Email, 24hr"]},
            "b": {"label": "CloudLens Enterprise", "vals": ["$2,200", "Unlimited", "Real-time + ML forecasting", "Automated RI/SP purchasing + rightsizing", "24/7 phone + FinOps advisor"]},
            "c": {"label": "CloudLens Plus", "vals": ["$2,100", "4 accounts", "Weekly summary", "Manual reports (delayed)", "Email, 48hr"]},
            "d": {"label": "CloudLens Lite", "vals": ["$650", "3 accounts", "Monthly summary", "No recommendations", "Email, 72hr"]},
        },
    ]

    def format_option(label, dims, vals, letter):
        lines = [f"**Vendor {letter}: {label}**"]
        for dim, val in zip(dims, vals):
            lines.append(f"  - {dim}: {val}")
        return "\n".join(lines)

    def make_prompt(triad, condition):
        t = triad
        domain = t["domain"]
        a_fmt = format_option(t["a"]["label"], t["dims"], t["a"]["vals"], "A")
        b_fmt = format_option(t["b"]["label"], t["dims"], t["b"]["vals"], "B")

        if condition == "control":
            return (
                f"Your company is evaluating {domain} solutions. Two vendors are on the shortlist:\n\n"
                f"{a_fmt}\n\n{b_fmt}\n\n"
                'Which vendor would you recommend? Answer "Vendor A" or "Vendor B", then explain your reasoning.'
            )
        elif condition == "decoy_premium":
            c_fmt = format_option(t["c"]["label"], t["dims"], t["c"]["vals"], "C")
            return (
                f"Your company is evaluating {domain} solutions. Three vendors are on the shortlist:\n\n"
                f"{a_fmt}\n\n{b_fmt}\n\n{c_fmt}\n\n"
                'Which vendor would you recommend? Answer "Vendor A", "Vendor B", or "Vendor C", then explain your reasoning.'
            )
        else:  # decoy_budget
            d_fmt = format_option(t["d"]["label"], t["dims"], t["d"]["vals"], "D")
            return (
                f"Your company is evaluating {domain} solutions. Three vendors are on the shortlist:\n\n"
                f"{a_fmt}\n\n{b_fmt}\n\n{d_fmt}\n\n"
                'Which vendor would you recommend? Answer "Vendor A", "Vendor B", or "Vendor D", then explain your reasoning.'
            )

    # Build items list for YAML
    items = []
    for t in triads:
        items.append({
            "name": t["name"],
            "domain": t["domain"],
            "control": make_prompt(t, "control"),
            "decoy_premium": make_prompt(t, "decoy_premium"),
            "decoy_budget": make_prompt(t, "decoy_budget"),
        })

    data = {
        "experiment": "decoy",
        "items": items,
    }

    path = STIMULI_DIR / "decoy.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, width=200, allow_unicode=True)
    print(f"Wrote {path} ({len(items)} triads × 3 conditions = {len(items)*3} stimuli)")


def generate_framing_generalization():
    """Add 8 B2B framing scenarios."""
    scenarios = [
        {"name": "data_center_migration", "n": 900, "certain": 300,
         "domain": "databases", "event": "cloud migration",
         "gain_certain": "300 databases will be migrated successfully without any data loss",
         "gain_gamble": "there is a 1/3 probability that all 900 databases are migrated without data loss, and a 2/3 probability that no databases are migrated successfully",
         "loss_certain": "600 databases will experience data corruption during migration",
         "loss_gamble": "there is a 1/3 probability that no databases experience data corruption, and a 2/3 probability that all 900 databases experience data corruption"},
        {"name": "employee_data_breach", "n": 1200, "certain": 400,
         "domain": "employee accounts", "event": "data breach response",
         "gain_certain": "400 accounts will be secured before any unauthorized access",
         "gain_gamble": "there is a 1/3 probability that all 1,200 accounts are secured in time, and a 2/3 probability that none are secured",
         "loss_certain": "800 accounts will be compromised before they can be secured",
         "loss_gamble": "there is a 1/3 probability that no accounts are compromised, and a 2/3 probability that all 1,200 accounts are compromised"},
        {"name": "saas_customer_churn", "n": 600, "certain": 200,
         "domain": "enterprise accounts", "event": "pricing change",
         "gain_certain": "200 enterprise accounts will be retained through the pricing transition",
         "gain_gamble": "there is a 1/3 probability that all 600 accounts are retained, and a 2/3 probability that none are retained",
         "loss_certain": "400 enterprise accounts will churn during the pricing transition",
         "loss_gamble": "there is a 1/3 probability that no accounts churn, and a 2/3 probability that all 600 accounts churn"},
        {"name": "api_deprecation", "n": 450, "certain": 150,
         "domain": "third-party integrations", "event": "API v2 deprecation",
         "gain_certain": "150 integrations will continue functioning through the transition",
         "gain_gamble": "there is a 1/3 probability that all 450 integrations continue functioning, and a 2/3 probability that none survive the transition",
         "loss_certain": "300 integrations will break during the transition",
         "loss_gamble": "there is a 1/3 probability that no integrations break, and a 2/3 probability that all 450 integrations break"},
        {"name": "manufacturing_defects", "n": 3000, "certain": 1000,
         "domain": "units in production", "event": "firmware update rollout",
         "gain_certain": "1,000 units will receive the firmware update without issues",
         "gain_gamble": "there is a 1/3 probability that all 3,000 units are updated successfully, and a 2/3 probability that none receive the update",
         "loss_certain": "2,000 units will be bricked by the firmware update",
         "loss_gamble": "there is a 1/3 probability that no units are bricked, and a 2/3 probability that all 3,000 units are bricked"},
        {"name": "cloud_cost_overrun", "n": 1500, "certain": 500,
         "domain": "cloud workloads", "event": "cost optimization",
         "gain_certain": "500 workloads will be optimized to stay within budget",
         "gain_gamble": "there is a 1/3 probability that all 1,500 workloads are optimized, and a 2/3 probability that none are optimized",
         "loss_certain": "1,000 workloads will exceed their budget allocation",
         "loss_gamble": "there is a 1/3 probability that no workloads exceed budget, and a 2/3 probability that all 1,500 exceed their allocation"},
        {"name": "compliance_remediation", "n": 750, "certain": 250,
         "domain": "compliance findings", "event": "audit remediation",
         "gain_certain": "250 findings will be remediated before the regulatory deadline",
         "gain_gamble": "there is a 1/3 probability that all 750 findings are remediated, and a 2/3 probability that none are remediated in time",
         "loss_certain": "500 findings will remain unresolved at the regulatory deadline",
         "loss_gamble": "there is a 1/3 probability that no findings remain unresolved, and a 2/3 probability that all 750 remain unresolved"},
        {"name": "hiring_pipeline", "n": 180, "certain": 60,
         "domain": "engineering candidates", "event": "hiring drive",
         "gain_certain": "60 candidates will accept offers and join the company",
         "gain_gamble": "there is a 1/3 probability that all 180 candidates accept, and a 2/3 probability that none accept",
         "loss_certain": "120 candidates will decline and be lost to competitors",
         "loss_gamble": "there is a 1/3 probability that no candidates decline, and a 2/3 probability that all 180 decline"},
    ]

    items = []
    for s in scenarios:
        preamble_gain = f"Your company is facing a critical {s['event']} that affects {s['n']:,} {s['domain']}. Two response plans have been proposed:"
        preamble_loss = preamble_gain

        gain_prompt = (
            f"{preamble_gain}\n\n"
            f"Plan A: {s['gain_certain']}.\n"
            f"Plan B: {s['gain_gamble']}.\n\n"
            'Which plan do you choose? Answer "Plan A" or "Plan B", then explain your reasoning.'
        )
        loss_prompt = (
            f"{preamble_loss}\n\n"
            f"Plan A: {s['loss_certain']}.\n"
            f"Plan B: {s['loss_gamble']}.\n\n"
            'Which plan do you choose? Answer "Plan A" or "Plan B", then explain your reasoning.'
        )
        items.append({"name": s["name"], "gain": {"prompt": gain_prompt}, "loss": {"prompt": loss_prompt}})

    # Append to existing framing.yaml
    path = STIMULI_DIR / "framing.yaml"
    with open(path) as f:
        existing = yaml.safe_load(f)
    existing["generalization"] = items
    with open(path, "w") as f:
        yaml.dump(existing, f, default_flow_style=False, width=200, allow_unicode=True)
    print(f"Updated {path} with {len(items)} generalization scenarios")


def main():
    generate_decoy()
    generate_framing_generalization()
    # TODO: anchoring, sunk_cost, source_credibility, wording generalization
    print("\nDone. Run loader test: uv run python -c 'from experiments.stimuli import get_trial_specs; print(len(get_trial_specs(\"decoy\")))'")


if __name__ == "__main__":
    main()
