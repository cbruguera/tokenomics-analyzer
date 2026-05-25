Run adversarial stress tests on a token model to identify collapse conditions.

Arguments: $ARGUMENTS
(Path to a TokenModel YAML file, e.g. models/nova-protocol.yaml)

Steps:
1. Load the TokenModel from $ARGUMENTS.
2. Load knowledge/failure_postmortems.md and, if staking is present, knowledge/staking_dynamics.md.
3. Run the following stress scenarios:

   **Bear market:** Simulate 80% price decline over 6 months. Track staking rate, inflation vs. demand, treasury runway, and whether a death spiral triggers.

   **Whale exit:** Simulate the top 3 holder categories (team, investors, ecosystem) unlocking simultaneously at vesting cliff. Calculate sell pressure as % of circulating supply and estimated price impact.

   **Revenue collapse:** Simulate protocol revenue dropping to zero. How long does the treasury last? When does the emission-funded staking yield become purely dilutive?

   **Governance attack:** Given the governance parameters, calculate the cost of a 51% attack (flash loan or accumulation). Flag if it is economically viable.

4. For each scenario: produce a chart, identify the threshold at which the model breaks, and state whether the current design survives.
5. Save all outputs to analysis/<token-name>/stress-tests/.
6. Write a stress test summary section suitable for inclusion in a full audit report.
