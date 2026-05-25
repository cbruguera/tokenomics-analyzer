Parse a verbal description of a token economic model into a structured TokenModel YAML file.

Arguments: $ARGUMENTS
(A verbal description of the token model — can be a few sentences or several paragraphs)

Steps:
1. Read models/schema.yaml to understand the full schema structure.
2. Extract all information from the description in $ARGUMENTS and map it to the schema fields.
3. For any required field that cannot be determined from the description, use the value "unknown" and note it.
4. Ask clarifying questions for any Critical or High-impact fields that are missing (e.g., vesting schedule, emission rate, burn mechanism). Present them as a numbered list and wait for answers before saving.
5. Once complete, save the result to models/<token-name>.yaml.
6. Print a summary of what was parsed and list all fields marked "unknown" — these represent gaps in the model description that the team should address.
