# Level 2: Professional Practical Exam

**Time Limit:** 120 minutes  
**Passing Score:** 70%

## Objective

Build a multi-context agent with integrations

## Requirements

- Implement multiple contexts with transitions
- Use DataMap for external data
- Add skills for reusable functionality
- Implement state management
- Add call recording capability

## Instructions

1. Clone this repository
2. Implement your solution in `solution/agent.py`
3. Test locally with `swaig-test`
4. Push to trigger auto-grading

## Grading Criteria

| Criteria | Points |
|----------|--------|
| Agent instantiates without errors | 15 |
| Generates valid SWML | 15 |
| All required functions present | 30 |
| Functions return expected results | 25 |
| Code quality and organization | 15 |
| **Total** | **100** |

## Testing Locally

```bash
# Install dependencies
pip install signalwire-agents

# Check your agent loads
swaig-test solution/agent.py --list-tools

# Verify SWML output
swaig-test solution/agent.py --dump-swml

# Test specific functions
swaig-test solution/agent.py --exec function_name --param value
```

## Submission

Push your code to the `main` branch. Grading runs automatically.

Check the "Grading Results" issue for your score.

---

*SignalWire AI Agents Certification - Level 2 Practical Exam*
