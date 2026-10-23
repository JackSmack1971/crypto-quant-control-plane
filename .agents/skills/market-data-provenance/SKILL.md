---
name: market-data-provenance
description: Validate crypto asset identity, primary data provenance, point-in-time timestamps, coverage, upstream independence and data quality before consequential analysis.
---
# Market-data validation
Read `methodologies/06-source-provenance-methodology.md` and `methodologies/08-data-quality-validation-methodology.md`.
1. Identify canonical asset/contract, chain/network, exchange venue, instrument type, quote, multiplier and units; keep spot/index/perp separate.
2. For every observation record producer, wrapper/vendor, endpoint/tool identity, query parameters, event/availability/retrieval clocks, timezone, finality, revision and coverage where available.
3. Assess missingness, duplicate keys, gaps, outliers, staleness, selection/survivorship bias and dependence between alleged independent feeds. Do not interpolate silently.
4. Record conflicts without averaging incompatible markets; seek comparator where meaningful.
5. Return a provenance table, test outcomes, unresolved issues and a usable/restricted/rejected verdict per dataset. Data read permission is not implied by a skill.
