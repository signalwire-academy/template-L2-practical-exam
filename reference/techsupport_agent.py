#!/usr/bin/env python3
"""
TechSupport Pro Agent - Level 2 Practical Exam Reference Solution

This is the instructor reference solution. Students should implement
their own version in solution/techsupport_agent.py
"""

from signalwire_agents import AgentBase, SwaigFunctionResult
from signalwire_agents.contexts import ContextBuilder

# Mock databases
CUSTOMERS = {
    "john@example.com": {"id": "C001", "name": "John Smith", "tier": "premium"},
    "+15551234567": {"id": "C002", "name": "Jane Doe", "tier": "standard"},
    "mike@example.com": {"id": "C003", "name": "Mike Wilson", "tier": "premium"}
}

SPECIALISTS = {
    "billing": "+15551111111",
    "technical": "+15552222222",
    "account": "+15553333333"
}

_ticket_counter = 1000


class TechSupportAgent(AgentBase):
    def __init__(self):
        super().__init__(
            name="techsupport-agent",
            route="/support"
        )

        self._configure_prompts()
        self._configure_recording()
        self._configure_language()
        self._setup_contexts()
        self._setup_functions()

    def _configure_prompts(self):
        self.prompt_add_section(
            "Role",
            "You are a technical support agent for TechSupport Pro. "
            "This call may be recorded for quality and training purposes."
        )

        self.prompt_add_section(
            "Capabilities",
            bullets=[
                "Identify customers by phone or email",
                "Create and manage support tickets",
                "Troubleshoot common issues",
                "Escalate to specialists when needed"
            ]
        )

        self.prompt_add_section(
            "Privacy",
            "When collecting sensitive information like account numbers or "
            "passwords, always use secure_mode to pause recording first."
        )

    def _configure_recording(self):
        self.set_params({
            "record_call": True,
            "record_format": "mp3",
            "record_stereo": True
        })

    def _configure_language(self):
        self.add_language(
            "English",
            "en-US",
            "rime.spore",
            speech_fillers=["Um", "Let me see"],
            function_fillers=["One moment please...", "Looking that up..."]
        )

    def _setup_contexts(self):
        # Greeting context
        greeting = ContextBuilder("greeting")
        greeting.add_step(
            "system",
            "Welcome the customer and ask how you can help. "
            "Use identify_customer to look up the caller."
        )
        greeting.set_functions(["identify_customer", "get_status"])
        self.add_context(greeting)

        # Triage context
        triage = ContextBuilder("triage")
        triage.add_step(
            "system",
            "Collect details about the customer's issue. "
            "Use describe_issue and create_ticket to document the problem."
        )
        triage.set_functions(["describe_issue", "create_ticket", "check_knowledge_base"])
        self.add_context(triage)

        # Resolution context
        resolution = ContextBuilder("resolution")
        resolution.add_step(
            "system",
            "Work to resolve the issue or escalate if needed. "
            "Use resolve_ticket when fixed, or escalate_ticket for specialists."
        )
        resolution.set_functions(["resolve_ticket", "escalate_ticket", "schedule_callback", "secure_mode"])
        self.add_context(resolution)

    def _setup_functions(self):
        @self.tool(
            description="Identify customer by email or phone number",
            parameters={
                "type": "object",
                "properties": {
                    "identifier": {
                        "type": "string",
                        "description": "Customer email or phone number"
                    }
                },
                "required": ["identifier"]
            }
        )
        def identify_customer(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            identifier = args.get("identifier", "").lower().strip()

            # Check both email and phone formats
            customer = CUSTOMERS.get(identifier)
            if not customer:
                # Try normalized phone
                normalized = identifier.replace(" ", "").replace("-", "")
                customer = CUSTOMERS.get(normalized)

            if customer:
                result = SwaigFunctionResult(
                    f"Found customer: {customer['name']} (ID: {customer['id']}, "
                    f"Tier: {customer['tier']}). How can I help you today?"
                )
                result.update_global_data({
                    "customer_id": customer["id"],
                    "customer_name": customer["name"],
                    "customer_tier": customer["tier"]
                })
                result.set_context_switch("triage")
                return result
            else:
                return SwaigFunctionResult(
                    "I couldn't find an account with that information. "
                    "Can you provide your email address or phone number?"
                )

        @self.tool(
            description="Get status of a previous ticket",
            parameters={
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "Ticket ID to look up"
                    }
                },
                "required": ["ticket_id"]
            }
        )
        def get_status(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            ticket_id = args.get("ticket_id", "")
            return SwaigFunctionResult(
                f"Ticket {ticket_id} is currently being processed. "
                "Would you like to speak with someone about it?"
            )

        @self.tool(
            description="Record details about the customer's issue",
            parameters={
                "type": "object",
                "properties": {
                    "issue_type": {
                        "type": "string",
                        "description": "Type of issue",
                        "enum": ["login", "performance", "billing", "account", "other"]
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the issue"
                    }
                },
                "required": ["issue_type", "description"]
            }
        )
        def describe_issue(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            issue_type = args.get("issue_type", "other")
            description = args.get("description", "")

            result = SwaigFunctionResult(
                f"I've noted your {issue_type} issue. Let me create a ticket for you."
            )
            result.update_global_data({
                "issue_type": issue_type,
                "issue_description": description
            })
            return result

        @self.tool(
            description="Create a support ticket",
            parameters={
                "type": "object",
                "properties": {
                    "priority": {
                        "type": "string",
                        "description": "Ticket priority",
                        "enum": ["low", "medium", "high", "urgent"]
                    }
                },
                "required": ["priority"]
            }
        )
        def create_ticket(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            global _ticket_counter
            priority = args.get("priority", "medium")

            _ticket_counter += 1
            ticket_id = f"TKT-{_ticket_counter}"

            result = SwaigFunctionResult(
                f"I've created ticket {ticket_id} with {priority} priority. "
                "Let me work on resolving this for you."
            )
            result.update_global_data({"ticket_id": ticket_id})
            result.set_context_switch("resolution")
            return result

        @self.tool(
            description="Search knowledge base for solutions",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        )
        def check_knowledge_base(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            query = args.get("query", "")
            return SwaigFunctionResult(
                f"I found some information about '{query}'. "
                "Let me walk you through the solution."
            )

        @self.tool(
            description="Mark ticket as resolved",
            parameters={
                "type": "object",
                "properties": {
                    "resolution_notes": {
                        "type": "string",
                        "description": "Notes about how the issue was resolved"
                    }
                },
                "required": ["resolution_notes"]
            }
        )
        def resolve_ticket(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            resolution_notes = args.get("resolution_notes", "")
            raw_data = raw_data or {}
            global_data = raw_data.get("global_data", {})
            ticket_id = global_data.get("ticket_id", "unknown")

            result = SwaigFunctionResult(
                f"Great! I've resolved ticket {ticket_id}. "
                "Is there anything else I can help you with?"
            )
            # Send SMS confirmation
            result.add_action("send_sms", {
                "to": "+15551234567",
                "body": f"Your ticket {ticket_id} has been resolved. Thank you for contacting TechSupport Pro!"
            })
            result.set_context_switch("greeting")
            return result

        @self.tool(
            description="Escalate ticket to a specialist",
            parameters={
                "type": "object",
                "properties": {
                    "specialist_type": {
                        "type": "string",
                        "description": "Type of specialist needed",
                        "enum": ["billing", "technical", "account"]
                    }
                },
                "required": ["specialist_type"]
            }
        )
        def escalate_ticket(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            specialist_type = args.get("specialist_type", "technical")
            phone = SPECIALISTS.get(specialist_type, SPECIALISTS["technical"])

            result = SwaigFunctionResult(
                f"I'm transferring you to our {specialist_type} specialist now."
            )
            result.update_global_data({"escalation_reason": specialist_type})
            result.swml_transfer(phone, final=True)
            return result

        @self.tool(
            description="Schedule a callback from support",
            parameters={
                "type": "object",
                "properties": {
                    "preferred_time": {
                        "type": "string",
                        "description": "Preferred callback time"
                    }
                },
                "required": ["preferred_time"]
            }
        )
        def schedule_callback(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            preferred_time = args.get("preferred_time", "")
            return SwaigFunctionResult(
                f"I've scheduled a callback for {preferred_time}. "
                "One of our specialists will call you then."
            )

        @self.tool(
            description="Enter secure mode - pauses recording for sensitive data",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        def secure_mode(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            result = SwaigFunctionResult(
                "Recording has been paused. You can now share sensitive information safely."
            )
            result.toggle_record(on=False)
            return result


# Create agent instance
agent = TechSupportAgent()

if __name__ == "__main__":
    agent.run()
