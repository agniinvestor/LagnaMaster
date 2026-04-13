---
name: warn-model-downgrade
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: ^src/.*\.py$
  - field: new_text
    operator: regex_match
    pattern: (NATURAL_MALEFICS|NATURAL_BENEFICS).*#.*(static|simple|fallback)
---

**Possible model downgrade detected**

You may be replacing a rich, chart-conditional model with a static/simple fallback.

**Rule: always pick the RICHER model when consolidating.**
- Chart-conditional beats static (e.g., `is_natural_malefic(planet, chart)` beats `planet in NATURAL_MALEFICS`)
- Full dignity (20+ fields) beats simplified (5 states)
- BPHS-verified table beats computed approximation

If the static version is intentional (e.g., performance-critical inner loop), document why.
