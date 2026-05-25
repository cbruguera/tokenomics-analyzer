Run simulations for a token model and save outputs to the analysis directory.

Arguments: $ARGUMENTS
(Path to a TokenModel YAML file, e.g. models/nova-protocol.yaml)

Steps:
1. Load the TokenModel from $ARGUMENTS.
2. Load knowledge/token_archetypes.md to confirm archetypes.
3. Determine which simulations to run per the simulation selection logic in CLAUDE.md.
4. For each simulation: generate the Python script in simulations/<token-name>/, run it, and save CSV data and matplotlib charts to analysis/<token-name>/.
5. After all simulations complete, print a summary of results: key metrics, chart file paths, and 1-2 sentence interpretation of each simulation's main finding.

If a simulation script already exists for this token, re-run it rather than regenerating it unless the model file has changed.
