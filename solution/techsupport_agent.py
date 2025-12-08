#!/usr/bin/env python3
"""
TechSupport Pro Agent - Level 2 Practical Exam

Implement your solution here.

Requirements:
1. Multi-context workflow (greeting, triage, resolution)
2. Customer identification with state management
3. Ticket creation and escalation functions
4. Recording compliance with secure_mode
5. Deployment configuration

See README.md for full requirements.
"""

from signalwire_agents import AgentBase, SwaigFunctionResult

# Mock customer database - use this data
CUSTOMERS = {
    "john@example.com": {"id": "C001", "name": "John Smith", "tier": "premium"},
    "+15551234567": {"id": "C002", "name": "Jane Doe", "tier": "standard"},
    "mike@example.com": {"id": "C003", "name": "Mike Wilson", "tier": "premium"}
}

# Specialist phone numbers
SPECIALISTS = {
    "billing": "+15551111111",
    "technical": "+15552222222",
    "account": "+15553333333"
}

# Your implementation here...
