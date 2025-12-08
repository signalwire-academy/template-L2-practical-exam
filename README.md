# Level 2 Practical Exam: Certified Agent Engineer

| | |
|--|--|
| **Duration** | 3 hours |
| **Passing Score** | 70% (automated) + manual review |

## Scenario: TechSupport Pro

Build a complete customer service agent system for **TechSupport Pro** that handles:

1. Customer identification
2. Issue triage and troubleshooting
3. Ticket creation
4. Escalation to specialists

## Requirements

### Part 1: Agent Structure (20 points)

Create `solution/techsupport_agent.py` with:

- Name: `techsupport-agent`
- Route: `/support`
- Language: English (en-US) with appropriate TTS
- Clear role definition as a technical support agent
- Recording disclosure in prompt

### Part 2: Customer Identification (20 points)

Implement customer identification with state management:

**Function: `identify_customer(identifier)`**
- Look up customer by phone or email
- Store customer info in metadata (id, name, tier)
- Handle unknown customers gracefully

**Customer Data:**
```python
CUSTOMERS = {
    "john@example.com": {"id": "C001", "name": "John Smith", "tier": "premium"},
    "+15551234567": {"id": "C002", "name": "Jane Doe", "tier": "standard"},
    "mike@example.com": {"id": "C003", "name": "Mike Wilson", "tier": "premium"}
}
```

### Part 3: Multi-Context Workflow (25 points)

Implement a three-context workflow:

**Context 1: Greeting**
- Welcome message
- Functions: `identify_customer`, `get_status`

**Context 2: Triage**
- Collect issue details
- Functions: `describe_issue`, `create_ticket`, `check_knowledge_base`

**Context 3: Resolution**
- Resolve or escalate
- Functions: `resolve_ticket`, `escalate_ticket`, `schedule_callback`

**Required Transitions:**
- Greeting → Triage (after customer identified)
- Triage → Resolution (after ticket created)
- Resolution → Greeting (after resolution or escalation)

### Part 4: Issue Handling Functions (20 points)

**`describe_issue(issue_type, description)`**
- Store issue in metadata
- Move to triage context

**`create_ticket(priority)`**
- Generate ticket ID
- Store ticket info in metadata
- Move to resolution context

**`resolve_ticket(resolution_notes)`**
- Update ticket status
- Send confirmation SMS to customer
- Return to greeting context

**`escalate_ticket(specialist_type)`**
- Set escalation reason in metadata
- Transfer to appropriate specialist

**Specialist Numbers:**
```python
SPECIALISTS = {
    "billing": "+15551111111",
    "technical": "+15552222222",
    "account": "+15553333333"
}
```

### Part 5: Recording Compliance (10 points)

- Enable stereo MP3 recording
- Implement `secure_mode()` function to pause recording
- Resume after sensitive info collected
- Include disclosure in agent prompt

### Part 6: Deployment Configuration (5 points)

Create production-ready configuration:
- `Dockerfile` with health check
- `requirements.txt` with dependencies
- `.env.example` with all required variables

## Testing Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Check agent loads
swaig-test solution/techsupport_agent.py --list-tools

# Verify SWML output
swaig-test solution/techsupport_agent.py --dump-swml

# Test customer identification
swaig-test solution/techsupport_agent.py --exec identify_customer \
  --identifier "john@example.com"

# Test ticket creation
swaig-test solution/techsupport_agent.py --exec create_ticket \
  --priority "high"

# Build Docker image
docker build -t techsupport:latest .
```

## Submission

1. Implement your solution in `solution/techsupport_agent.py`
2. Create deployment files (Dockerfile, requirements.txt, .env.example)
3. Add your demo recording (wav, mp3, or mp4)
4. Push to trigger auto-grading

**Note:** After automated checks pass, your submission will be tagged for manual review.

## Grading Breakdown

| Component | Points | Type |
|-----------|--------|------|
| Agent loads correctly | 10 | Automated |
| Valid SWML generation | 10 | Automated |
| identify_customer exists | 5 | Automated |
| identify_customer works | 10 | Automated |
| Contexts defined | 10 | Automated |
| describe_issue exists | 5 | Automated |
| create_ticket exists | 5 | Automated |
| resolve_ticket exists | 5 | Automated |
| escalate_ticket exists | 5 | Automated |
| create_ticket works | 5 | Automated |
| Transfer capability | 5 | Automated |
| Recording configured | 5 | Automated |
| secure_mode exists | 5 | Automated |
| Deployment files | 5 | Manual |
| Code quality | 5 | Manual |
| Live demonstration | 5 | Manual |
| **Total** | **100** | |

---

## Next Assignment

Congratulations on completing Level 2! Ready for Level 3? [**Start Lab 3.1: Enterprise Architecture**](https://classroom.github.com/a/pW8dxCLE)

---

*SignalWire AI Agents Certification - Level 2 Practical Exam*
