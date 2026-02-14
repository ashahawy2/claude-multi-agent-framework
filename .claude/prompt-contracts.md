# Prompt Contracts -- Non-Negotiable Behaviors

> **Any agent modifying LLM prompts MUST verify these contracts still hold.**
> Removing directive language, examples, or guardrails from prompts is a REGRESSION unless explicitly justified.
>
> **This file is optional.** Only needed for projects that use LLM prompts as part of their system.
> Delete this file if your project doesn't use LLM prompts.

---

## How to Define Contracts

A prompt contract defines a behavior that MUST hold regardless of prompt changes. Each contract specifies:

1. **The rule** -- what must always be true
2. **Why it matters** -- what breaks if violated
3. **How to test** -- manual or automated verification

## Example Contracts

### Contract 1: Output Format Consistency

**The system MUST return responses in the specified format.**

- JSON responses MUST be valid JSON
- Error responses MUST include an error code and human-readable message
- The format MUST NOT change based on prompt modifications

**Test**: Send a standard request -> verify response matches the schema.

### Contract 2: Safety Guardrails

**The system MUST NOT generate harmful, biased, or off-topic content.**

- Prompts MUST include safety instructions
- Removing safety instructions is a REGRESSION
- Safety instructions MUST use `MUST` / `NEVER` directives (not "should" / "try to")

**Test**: Send an adversarial input -> verify the system refuses or redirects.

### Contract 3: Prompt Directive Strength

**Critical prompt sections MUST use strong directive language.**

- `MUST` directive (not just "should" or "try to")
- At least 2 GOOD examples showing desired behavior
- At least 2 BAD examples showing what NOT to do
- Strong header (`***CRITICAL***` or equivalent)

**Rationale**: LLMs respond much more reliably to prompts with examples than to abstract rules alone. Removing examples causes regressions.

---

## How to Verify Contracts

### Manual (during development)
1. Read the prompt output for a representative request
2. Check the response against each contract above
3. If ANY contract is violated, the prompt change is a regression

### Reviewer Agent
When reviewing changes to prompt files:
- Flag removal of `MUST`, `CRITICAL`, `ALWAYS`, `NEVER` directives
- Flag removal of good/bad examples
- Flag any prompt section that got shorter without justification
- Cross-reference against this contracts file

---

## Your Contracts

> **CUSTOMIZE**: Define your project's prompt contracts below.
> Delete the examples above and replace with your actual contracts.

_No contracts defined yet._
