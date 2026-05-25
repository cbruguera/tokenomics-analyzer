Run a full token audit on the provided model file or description.

Arguments: $ARGUMENTS
(Pass either a path to a .yaml model file, or a verbal description of a token model in quotes)

Follow the full audit workflow defined in CLAUDE.md:
1. If $ARGUMENTS is a file path, load it as the TokenModel. If it is a verbal description, parse it into a TokenModel first using models/schema.yaml as the schema and save it to models/.
2. Classify the token archetypes.
3. Load the relevant knowledge files per the selective loading map in CLAUDE.md.
4. Run the weakness scanner and produce all findings with severity ratings.
5. Generate and run the appropriate simulation scripts per the simulation selection logic. Save outputs to analysis/<token-name>/.
6. Generate an Excel spreadsheet model and save to analysis/<token-name>/.
7. Write the full audit report using templates/report_template.md and save to reports/<token-name>_audit.md.

At the end, print a summary: token name, overall grade, finding counts by severity, and the output file paths.
