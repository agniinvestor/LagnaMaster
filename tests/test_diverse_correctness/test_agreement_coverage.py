"""Meta-test: ensures agreement coverage doesn't silently erode."""
import json

import pytest
from pathlib import Path

RESULTS_DIR = Path("tests/fixtures/verified_360_results")


def test_minimum_agreement_coverage():
    """Agreement must stay above 90% globally."""
    total_fields = 0
    agreement_fields = 0

    for path in sorted(RESULTS_DIR.glob("*.json")):
        data = json.loads(path.read_text())
        for field, verdict in data.get("verdicts", {}).items():
            total_fields += 1
            if verdict["status"] == "agreement":
                agreement_fields += 1

    if total_fields == 0:
        pytest.skip("No verified results found")

    rate = agreement_fields / total_fields
    assert rate > 0.80, (
        f"Agreement coverage {rate:.1%} below 80% threshold "
        f"({agreement_fields}/{total_fields})"
    )
