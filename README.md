# reli

East Africa has 30+ open MCP servers covering payments, tax, health, drought, land, counties, labour rights, and more — but an AI agent builder had to discover, install, and hand-wire each one into their client. The stack existed; the on-ramp didn't.

`reli` (Swahili: *rails*) is that on-ramp. One command chain takes any MCP-capable client from zero to the full Kenya coordination stack:

```bash
pip install reli-cli
reli up --pack core        # install + wire into Claude Desktop + verify
```

Under two minutes. Then ask your agent: *"what Kenya-stack tools do you have?"*

## Commands

```bash
reli list                  # every component, grouped by domain pack
reli list --pack financial # payments, tax, credit, insurance, markets
reli install health        # or any pack, server name, or "all"
reli config                # wire installed servers into Claude Desktop (backs up first)
reli config --stdout       # print JSON for any other MCP client
reli doctor                # verify every installed component imports cleanly
reli demo drought          # watch one signal cascade across five institutions
```

## Domain packs

| Pack | Covers |
|---|---|
| `core` | coordination bus, agent kit, offline sync, decision frameworks |
| `financial` | M-PESA, KRA, credit, insurance, returns, remittances, markets |
| `health` | facilities, CHW protocols, mental health, Swahili-native health tools |
| `agriculture` | crops, drought & water, environment, market prices |
| `civic` | counties, forms, labour rights, jobs, media, education, skills, history |
| `diaspora` | land, housing, family, community groups, faith institutions |
| `mobility-energy` | transport, energy access |
| `language` | Swahili translation infrastructure |

## The demo

```bash
reli install core && reli demo drought
```

A drought alert in Baringo fires real routing rules from `africa-coord-bus`: parametric insurance evaluation, drought-resistant crop advisory, malnutrition surveillance activation, county alerts, market price signals. One signal, multiple institutions, zero phone calls — that is the coordination gap this stack closes.

## Trust integrity

Stack servers ship **DEMO datasets** — illustrative, not live institutional feeds. Do not use outputs for operational, financial, medical, or legal decisions. No partnership with any government, regulator, or financial institution is implied.

## The wider stack

Full developer reference: [The Nairobi Stack](https://gabrielmahia.github.io/nairobi-stack/)

## IP & Collaboration

MIT licensed. Feedback via GitHub Issues only — pull requests are not accepted. Full policy: [docs/architecture/IP_POLICY.md](docs/architecture/IP_POLICY.md). Security reports: see [SECURITY.md](SECURITY.md).

<!-- interconnect:v1 -->
## Part of the East Africa coordination stack

- **Install & run:** `pip install reli-cli && reli list` — 33 MCP servers on the [official MCP Registry](https://registry.modelcontextprotocol.io) under `io.github.gabrielmahia`
- **Evaluate any model on Swahili agent tasks:** [kipimo](https://github.com/gabrielmahia/kipimo) · [dataset](https://huggingface.co/datasets/gmahia/kipimo) · [leaderboard](https://huggingface.co/spaces/gmahia/kipimo-leaderboard)
- **Coordinate across servers:** [africa-coord-bus](https://pypi.org/project/africa-coord-bus/) — offline-first event bus with a built-in Kenya routing table
- **Datasets:** [huggingface.co/gmahia](https://huggingface.co/gmahia) · **Docs hub:** [nairobi-stack](https://github.com/gabrielmahia/nairobi-stack)

Model-agnostic by design: closed APIs, open-weight models, and small distilled models are all first-class citizens.
<!-- /interconnect:v1 -->
