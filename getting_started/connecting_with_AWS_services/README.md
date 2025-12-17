first install req.txt then:
Use sh deploy_prereqs.sh shell command to create kb(use git bash)

When to use Decorator vs TOOL_SPEC Approach
Use Decorator Approach When:
working in Python-only environments ( follows Python decorator syntax )
creating quick prototypes or internal tools
your team is primarily Python developers
the tool has few parameters with simple types
you need minimal code and maximum readability
Use TOOL_SPEC Approach When:
creating tools that might be used across different LLM providers
building complex tools with detailed parameter validation
you need precise control over input schema validation
working with tools that have many parameters or nested structures ( follows JSON-like dictionary structure )
interoperability with other systems is important
The decorator approach is best for simplicity and rapid development, while TOOL_SPEC is better for complex, production-grade tools that need portability and strict schema validation.