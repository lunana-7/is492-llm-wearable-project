# Test fixtures

**Owner — Min Kim.**

Android tests generate synthetic names, orthogonal/normalized vectors and a colored bitmap in memory. They use the test-only preference namespace min_cp3_test_roster and remove its contents after each case. The bitmap verifies that the bundled model runs, with no claim about recognizing a real person.

Neha's synthetic prompt cases live in app/prompts/regression_cases.json. Keep photographs, embeddings from real participants, roster exports, recordings and unredacted logs out of this directory. Real-device trials should report synthetic trial IDs and aggregate outcomes.
