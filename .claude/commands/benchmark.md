Benchmark a token model against comparable protocols and well-known reference tokens.

Arguments: $ARGUMENTS
(Path to a TokenModel YAML file, e.g. models/nova-protocol.yaml)

Steps:
1. Load the TokenModel from $ARGUMENTS.
2. Load knowledge/token_archetypes.md and knowledge/failure_postmortems.md.
3. Identify 2-3 comparable protocols from the model's `competitive.comparable_protocols` field. If none are specified, infer appropriate comparables from the archetype and use-case.
4. Always include at least one reference token appropriate to the archetype:
   - Governance token → compare against UNI or COMP
   - Real-yield token → compare against GMX
   - ve-token → compare against veCRV
   - Staking/inflation token → compare against SOL or MATIC (pre-merge era)
   - Algorithmic stablecoin → compare against FRAX and flag Terra as a negative reference

5. Produce a comparison table covering: team allocation %, investor allocation %, vesting cliff/duration, Y1 inflation rate, staking yield source, governance timelock, treasury runway.

6. Write a narrative section (300-500 words) identifying where this model is stronger, weaker, or meaningfully different from its comparables. Be specific — reference exact parameter differences.

7. Save the benchmark section as analysis/<token-name>/benchmark.md, formatted for direct inclusion in the audit report.
