"""Server registry — the map of East Africa's MCP coordination stack.

Each entry describes one PyPI-installable server: how to launch it, which
domain pack it belongs to, and the coordination gap it addresses. Names are
Swahili; the ``gloss`` field translates the root word.

Servers with ``script`` set expose a console entry point; the rest are
launched as ``python -m <module>.server`` (validated against live installs).
``kind: library`` entries are Python libraries, not MCP stdio servers, and
are excluded from client configuration.
"""

from __future__ import annotations

DEMO_NOTICE = (
    "DEMO data notice: servers ship illustrative datasets, not live "
    "institutional feeds. Do not use outputs for operational, financial, "
    "medical, or legal decisions."
)

# pack name -> human description
PACKS: dict[str, str] = {
    "core": "Coordination bus, agent kit, offline sync, decision frameworks",
    "financial": "Payments, tax, credit, insurance, markets, remittances",
    "health": "Facilities, community health, mental health, Swahili-native health tools",
    "agriculture": "Crops, drought and water, environment, market prices",
    "civic": "Counties, forms, labour rights, jobs, media, education, skills, history",
    "diaspora": "Land, housing, family, community, faith institutions, remittances",
    "mobility-energy": "Transport and energy access",
    "language": "Swahili translation infrastructure",
}

SERVERS: dict[str, dict] = {
    # ---- core ----
    "africa-coord-bus": {
        "module": "africa_coord_bus", "script": None, "kind": "library",
        "packs": ["core"], "gloss": "coordination bus",
        "desc": "Cross-domain event routing — drought alerts reach insurance, crop, health, county, and market tools automatically. Offline-first JSONL queue.",
    },
    "civic-agent-kit": {
        "module": "civic_agent_kit", "script": None, "kind": "library",
        "packs": ["core"], "gloss": "agent kit",
        "desc": "Building blocks for civic AI agents operating on East African data.",
    },
    "offline-mcp": {
        "module": "offline_mcp", "script": "offline-mcp", "kind": "server",
        "packs": ["core"], "gloss": "offline",
        "desc": "Offline-first tooling for intermittent-connectivity environments.",
    },
    "decision-intelligence-mcp": {
        "module": "classical_strategy_mcp", "script": "decision-intelligence-mcp", "kind": "server",
        "packs": ["core"], "gloss": "decision intelligence",
        "desc": "Strategic decision frameworks as agent-callable tools for constrained, high-stakes institutional choices.",
    },
    # ---- financial ----
    "mpesa-mcp": {
        "module": "mpesa_mcp", "script": "mpesa-mcp", "kind": "server",
        "packs": ["financial"], "gloss": "mobile money",
        "desc": "M-PESA payment rails (Daraja) exposed to AI agents — STK push, B2C, transaction status.",
    },
    "kra-mcp": {
        "module": "kra_mcp", "script": "kra-mcp", "kind": "server",
        "packs": ["financial"], "gloss": "tax authority",
        "desc": "Kenya Revenue Authority workflows — PIN checks, filing calendars, obligation lookup.",
    },
    "mkopo-mcp": {
        "module": "mkopo_mcp", "script": None, "kind": "server",
        "packs": ["financial"], "gloss": "mkopo = credit/loan",
        "desc": "Credit and lending reference — products, rates, CRB context for borrowers and SACCOs.",
    },
    "bima-mcp": {
        "module": "bima_mcp", "script": "bima-mcp", "kind": "server",
        "packs": ["financial"], "gloss": "bima = insurance",
        "desc": "Insurance tools including parametric drought cover evaluation triggered by satellite signals.",
    },
    "faida-mcp": {
        "module": "faida_mcp", "script": "faida-mcp", "kind": "server",
        "packs": ["financial"], "gloss": "faida = profit/returns",
        "desc": "Investment and returns reference for Kenyan savers — instruments, rates, comparisons.",
    },
    "remit-mcp": {
        "module": "remit_mcp", "script": None, "kind": "server",
        "packs": ["financial", "diaspora"], "gloss": "remittances",
        "desc": "Diaspora remittance corridors — costs, routes, and timing across providers.",
    },
    "soko-mcp": {
        "module": "soko_mcp", "script": "soko-mcp", "kind": "server",
        "packs": ["financial", "agriculture"], "gloss": "soko = market",
        "desc": "Commodity market price signals — narrowing the farm-gate/market information asymmetry.",
    },
    # ---- health ----
    "afya-mcp": {
        "module": "afya_mcp", "script": "afya-mcp", "kind": "server",
        "packs": ["health"], "gloss": "afya = health",
        "desc": "Health system tools — facility lookup, CHW protocols, malnutrition surveillance activation.",
    },
    "afya-ya-akili-mcp": {
        "module": "afya_ya_akili_mcp", "script": "afya-ya-akili-mcp", "kind": "server",
        "packs": ["health"], "gloss": "afya ya akili = mental health",
        "desc": "Mental health resources and referral pathways, Swahili-aware.",
    },
    "kenya-health-mcp": {
        "module": "kenya_health_mcp", "script": "kenya-health-mcp", "kind": "server",
        "packs": ["health"], "gloss": "health registry",
        "desc": "Facility registry and service availability — which facility offers what, at which referral level.",
    },
    "swahili-health-mcp": {
        "module": "swahili_health_mcp", "script": "swahili-health-mcp", "kind": "server",
        "packs": ["health", "language"], "gloss": "Swahili-native health",
        "desc": "Health tools with Swahili-native descriptions and outputs for community health workers.",
    },
    # ---- agriculture ----
    "kilimo-mcp": {
        "module": "kilimo_mcp", "script": "kilimo-mcp", "kind": "server",
        "packs": ["agriculture"], "gloss": "kilimo = agriculture",
        "desc": "Crop advisory — planting calendars, drought-resistant guidance, extension knowledge as tools.",
    },
    "wapimaji-mcp": {
        "module": "wapimaji_mcp", "script": "wapimaji-mcp", "kind": "server",
        "packs": ["agriculture"], "gloss": "maji = water",
        "desc": "Drought and water access — NDMA drought phases, borehole registry, county water coverage.",
    },
    "mazingira-mcp": {
        "module": "mazingira_mcp", "script": "mazingira-mcp", "kind": "server",
        "packs": ["agriculture"], "gloss": "mazingira = environment",
        "desc": "Environment and climate signals for planning and early warning.",
    },
    # ---- civic ----
    "county-mcp": {
        "module": "county_mcp", "script": "county-mcp", "kind": "server",
        "packs": ["civic"], "gloss": "county government",
        "desc": "County government reference — services, budgets, CDF, alert channels for 47 counties.",
    },
    "fomu-mcp": {
        "module": "fomu_mcp", "script": "fomu-mcp", "kind": "server",
        "packs": ["civic"], "gloss": "fomu = forms",
        "desc": "Government forms and document requirements — what a process needs, where to file, what it costs.",
    },
    "haki-ya-kazi-mcp": {
        "module": "haki_ya_kazi_mcp", "script": "haki-ya-kazi-mcp", "kind": "server",
        "packs": ["civic"], "gloss": "haki ya kazi = labour rights",
        "desc": "Employment rights in Swahili — contracts, dismissal, leave, minimum wage.",
    },
    "kazi-mcp": {
        "module": "kazi_mcp", "script": "kazi-mcp", "kind": "server",
        "packs": ["civic"], "gloss": "kazi = work",
        "desc": "Jobs and livelihoods reference for the Kenyan labour market.",
    },
    "habari-mcp": {
        "module": "habari_mcp", "script": "habari-mcp", "kind": "server",
        "packs": ["civic"], "gloss": "habari = news",
        "desc": "Media and public-information tools for journalists and civic monitors.",
    },
    "elimu-mcp": {
        "module": "elimu_mcp", "script": "elimu-mcp", "kind": "server",
        "packs": ["civic"], "gloss": "elimu = education",
        "desc": "Education system reference — institutions, curricula, transitions.",
    },
    "sifa-mcp": {
        "module": "sifa_mcp", "script": "sifa-mcp", "kind": "server",
        "packs": ["civic"], "gloss": "sifa = qualifications/reputation",
        "desc": "Skills and reference verification where credentials are hard to check and trust is expensive.",
    },
    "historia-mcp": {
        "module": "historia_mcp", "script": "historia-mcp", "kind": "server",
        "packs": ["civic"], "gloss": "historia = history",
        "desc": "East African historical corpora as queryable institutional memory.",
    },
    # ---- diaspora ----
    "diaspora-mcp": {
        "module": "diaspora_mcp", "script": "diaspora-mcp", "kind": "server",
        "packs": ["diaspora"], "gloss": "diaspora",
        "desc": "Diaspora workflows — documents, timelines, and cross-border obligations in one place.",
    },
    "ardhi-mcp": {
        "module": "ardhi_mcp", "script": "ardhi-mcp", "kind": "server",
        "packs": ["diaspora"], "gloss": "ardhi = land",
        "desc": "Land records and transaction guidance — reducing opacity in Kenya's highest-stakes asset class.",
    },
    "nyumba-mcp": {
        "module": "nyumba_mcp", "script": "nyumba-mcp", "kind": "server",
        "packs": ["diaspora"], "gloss": "nyumba = housing",
        "desc": "Housing and construction reference for diaspora builders and local buyers.",
    },
    "familia-mcp": {
        "module": "familia_mcp", "script": "familia-mcp", "kind": "server",
        "packs": ["diaspora"], "gloss": "familia = family",
        "desc": "Family workflows — succession, guardianship, and property protection guidance.",
    },
    "jumuia-mcp": {
        "module": "jumuia_mcp", "script": "jumuia-mcp", "kind": "server",
        "packs": ["diaspora"], "gloss": "jumuia = community",
        "desc": "Community group coordination — chamas, welfare groups, and their record-keeping.",
    },
    "church-mcp": {
        "module": "church_mcp", "script": "church-mcp", "kind": "server",
        "packs": ["diaspora"], "gloss": "faith institutions",
        "desc": "Membership, giving, and program workflows for faith institutions — trusted coordination structures still run on paper.",
    },
    # ---- mobility & energy ----
    "usafiri-mcp": {
        "module": "usafiri_mcp", "script": "usafiri-mcp", "kind": "server",
        "packs": ["mobility-energy"], "gloss": "usafiri = transport",
        "desc": "Transport reference — matatu routes, boda economics, logistics context.",
    },
    "nishati-mcp": {
        "module": "nishati_mcp", "script": "nishati-mcp", "kind": "server",
        "packs": ["mobility-energy"], "gloss": "nishati = energy",
        "desc": "Energy access and program data for last-mile connection decisions.",
    },
    # ---- language ----
    "tafsiri-mcp": {
        "module": "tafsiri_mcp", "script": "tafsiri-mcp", "kind": "server",
        "packs": ["language"], "gloss": "tafsiri = translation",
        "desc": "Swahili/English translation infrastructure for agent pipelines.",
    },
}


def by_pack(pack: str) -> dict[str, dict]:
    """Return servers belonging to a pack."""
    return {k: v for k, v in SERVERS.items() if pack in v["packs"]}


def launch_spec(name: str, python: str = "python") -> dict:
    """MCP client launch spec for a server (command + args)."""
    s = SERVERS[name]
    if s["script"]:
        return {"command": s["script"], "args": []}
    return {"command": python, "args": ["-m", f"{s['module']}.server"]}


def resolve(names_or_packs: list[str]) -> list[str]:
    """Expand pack names and validate server names; preserves order, dedupes."""
    out: list[str] = []
    for n in names_or_packs:
        if n == "all":
            targets = list(SERVERS)
        elif n in PACKS:
            targets = list(by_pack(n))
        elif n in SERVERS:
            targets = [n]
        else:
            raise KeyError(n)
        for t in targets:
            if t not in out:
                out.append(t)
    return out
