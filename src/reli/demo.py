"""Terminal-runnable coordination cascade demos.

Shows what the stack is *for*: a single domain signal (drought, disease
outbreak, flood) propagating across institutional boundaries via
africa-coord-bus routing rules. Everything printed is DEMO — illustrative
routing over illustrative data.
"""

from __future__ import annotations

from .registry import DEMO_NOTICE

SCENARIOS = {
    "drought": dict(
        domain="water", event_type="drought_alert", severity="alert",
        headline="NDMA drought phase reaches ALERT in Baringo County",
        data={"region": "Baringo", "ndvi_anomaly": -0.31, "spi": -1.6},
    ),
    "outbreak": dict(
        domain="health", event_type="disease_outbreak", severity="alert",
        headline="Cholera cluster reported near Lake Victoria shoreline",
        data={"disease": "cholera", "county": "Kisumu", "cases": 14},
    ),
    "flood": dict(
        domain="water", event_type="flood_alert", severity="warning",
        headline="Flash-flood warning issued for Tana River basin",
        data={"basin": "Tana", "county": "Tana River"},
    ),
}


def run(scenario: str = "drought") -> int:
    try:
        from africa_coord_bus import (
            CoordinationEvent,
            EventDomain,
            EventSeverity,
            KENYA_ROUTING_TABLE,
        )
    except ImportError:
        print("This demo needs the coordination bus:\n\n"
              "    pip install africa-coord-bus\n\n"
              "or simply `reli install core`, then re-run `reli demo`.")
        return 1

    s = SCENARIOS[scenario]
    event = CoordinationEvent(
        domain=EventDomain(s["domain"]),
        event_type=s["event_type"],
        source="reli-demo",
        severity=EventSeverity(s["severity"]),
        data=s["data"],
    )

    sev_order = ["info", "warning", "alert", "critical"]

    def fires(rule) -> bool:
        if rule.trigger_domain != event.domain:
            return False
        if rule.trigger_event_type != event.event_type:
            return False
        if sev_order.index(event.severity.value) < sev_order.index(
            rule.trigger_min_severity.value
        ):
            return False
        if rule.condition is not None:
            try:
                return bool(rule.condition(event))
            except Exception:
                return False
        return True

    matched = [r for r in KENYA_ROUTING_TABLE if fires(r)]

    print(f"\nSIGNAL  {s['headline']}")
    print(f"        domain={event.domain.value}  type={event.event_type}"
          f"  severity={event.severity.value}\n")
    if not matched:
        print("No routing rules fired at this severity. Try a higher-severity "
              "scenario: `reli demo drought`.")
        return 0
    print(f"CASCADE — {len(matched)} coordination rule(s) fired:\n")
    for r in matched:
        targets = ", ".join(d.value for d in r.target_domains)
        print(f"  → {r.name}")
        print(f"    reaches: {targets}")
        for action in r.target_actions:
            print(f"      · {action}")
        print(f"    why: {r.description}\n")
    print("One signal, multiple institutions, zero phone calls. That is the "
          "coordination gap this stack closes.\n")
    print(DEMO_NOTICE)
    return 0
