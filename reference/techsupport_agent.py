#!/usr/bin/env python3
"""
TechSupport Pro Agent - Level 2 Practical Exam

A complete customer service agent system with:
1. Multi-context workflow (greeting, triage, resolution)
2. Customer identification with state management
3. Ticket creation and escalation functions
4. Recording compliance with secure_mode
5. Deployment configuration
"""

import uuid
from signalwire_agents import AgentBase, SwaigFunctionResult

# Mock customer database
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


class TechSupportAgent(AgentBase):
    """TechSupport Pro customer service agent."""

    def __init__(self):
        super().__init__(
            name="techsupport-agent",
            route="/support",
            record_call=True,
            record_format="mp3",
            record_stereo=True
        )

        # Configure language
        self.add_language("English", "en-US", "rime.spore")

        # Set up prompts (required before define_contexts)
        self.prompt_add_section(
            "Role",
            "You are a professional technical support agent for TechSupport Pro. "
            "You help customers identify issues, create support tickets, and resolve "
            "or escalate problems as needed."
        )

        self.prompt_add_section(
            "Recording Disclosure",
            "IMPORTANT: At the start of each call, inform the customer that this call "
            "may be recorded for quality and training purposes."
        )

        self.prompt_add_section(
            "Guidelines",
            bullets=[
                "Always verify the customer's identity first",
                "Be professional and empathetic",
                "Gather complete issue details before creating a ticket",
                "Use secure_mode when collecting sensitive information",
                "Escalate to specialists when the issue requires expertise"
            ]
        )

        # Initialize global data
        self.set_global_data({
            "customer_identified": False,
            "ticket_created": False
        })

        # Register functions first (so they can be referenced in contexts)
        self._setup_functions()

        # Set up contexts
        self._setup_contexts()

    def _setup_contexts(self):
        """Set up the three-context workflow."""
        contexts = self.define_contexts()

        # Context 1: Greeting - Customer identification
        greeting = contexts.add_context("greeting")
        greeting.add_step("welcome") \
            .set_text(
                "Welcome to TechSupport Pro! This call may be recorded for quality purposes. "
                "I'll need to verify your identity first. Can you provide your email or phone number?"
            ) \
            .set_functions(["identify_customer", "get_status"]) \
            .set_step_criteria("Customer has been identified or needs to be found") \
            .set_valid_contexts(["triage"])

        # Context 2: Triage - Issue collection
        triage = contexts.add_context("triage") \
            .add_enter_filler("en-US", [
                "Let me help you with your issue...",
                "Now let's discuss what's going on..."
            ])
        triage.add_step("collect_issue") \
            .set_text(
                "Thank you for verifying your identity. Now, please describe the issue "
                "you're experiencing so I can assist you."
            ) \
            .set_functions(["describe_issue", "create_ticket", "check_knowledge_base"]) \
            .set_step_criteria("Customer has described their issue and ticket has been created") \
            .set_valid_contexts(["resolution", "greeting"])

        # Context 3: Resolution - Resolve or escalate
        resolution = contexts.add_context("resolution") \
            .add_enter_filler("en-US", [
                "Let me help resolve this issue...",
                "Now let's work on a solution..."
            ])
        resolution.add_step("resolve") \
            .set_text(
                "I have your ticket information. Let me help resolve this issue or "
                "connect you with a specialist if needed."
            ) \
            .set_functions(["resolve_ticket", "escalate_ticket", "schedule_callback"]) \
            .set_step_criteria("Issue has been resolved or escalated") \
            .set_valid_contexts(["greeting"])

    def _setup_functions(self):
        """Register all SWAIG functions."""

        # Part 2: Customer Identification
        @self.tool(
            description="Look up customer by phone number or email",
            parameters={
                "type": "object",
                "properties": {
                    "identifier": {
                        "type": "string",
                        "description": "Customer phone number or email address"
                    }
                },
                "required": ["identifier"]
            }
        )
        def identify_customer(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            identifier = args.get("identifier", "")
            customer = CUSTOMERS.get(identifier)
            if customer:
                return (
                    SwaigFunctionResult(
                        f"Customer identified: {customer['name']}, "
                        f"Account ID: {customer['id']}, Tier: {customer['tier']}. "
                        "Switching to issue triage."
                    )
                    .update_global_data({
                        "customer_id": customer["id"],
                        "customer_name": customer["name"],
                        "customer_tier": customer["tier"],
                        "customer_identified": True
                    })
                )
            else:
                return SwaigFunctionResult(
                    "I couldn't find an account with that information. "
                    "Please try a different email or phone number, "
                    "or I can create a new account for you."
                )

        # Status function for greeting context
        @self.tool(description="Get system status")
        def get_status(args: dict = None, raw_data: dict = None) -> SwaigFunctionResult:
            return SwaigFunctionResult(
                "TechSupport Pro is fully operational. "
                "All systems are running normally."
            )

        # Part 3: Triage context functions
        @self.tool(
            description="Record the customer's issue description",
            parameters={
                "type": "object",
                "properties": {
                    "issue_type": {
                        "type": "string",
                        "description": "Type of issue (technical, billing, account, other)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the issue"
                    }
                },
                "required": ["issue_type", "description"]
            }
        )
        def describe_issue(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            issue_type = args.get("issue_type", "")
            description = args.get("description", "")
            return (
                SwaigFunctionResult(
                    f"I've recorded your {issue_type} issue: {description}. "
                    "Let me create a support ticket for you."
                )
                .update_global_data({
                    "issue_type": issue_type,
                    "issue_description": description
                })
            )

        @self.tool(
            description="Create a support ticket",
            parameters={
                "type": "object",
                "properties": {
                    "priority": {
                        "type": "string",
                        "description": "Ticket priority (low, medium, high, urgent)"
                    }
                },
                "required": ["priority"]
            }
        )
        def create_ticket(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            priority = args.get("priority", "medium")
            ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
            return (
                SwaigFunctionResult(
                    f"Support ticket created: {ticket_id} with {priority} priority. "
                    "Moving to resolution phase."
                )
                .update_global_data({
                    "ticket_id": ticket_id,
                    "ticket_priority": priority,
                    "ticket_status": "open",
                    "ticket_created": True
                })
            )

        @self.tool(
            description="Search knowledge base for solutions",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for the knowledge base"
                    }
                },
                "required": ["query"]
            }
        )
        def check_knowledge_base(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            query = args.get("query", "")
            return SwaigFunctionResult(
                f"I searched our knowledge base for '{query}'. "
                "Here are some common solutions: "
                "1. Restart the device, "
                "2. Clear cache and cookies, "
                "3. Check network connectivity. "
                "Would you like me to create a ticket if these don't help?"
            )

        # Part 4: Resolution context functions
        @self.tool(
            description="Resolve and close the ticket",
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
            return (
                SwaigFunctionResult(
                    f"Ticket resolved: {resolution_notes}. "
                    "I'm sending you a confirmation SMS. "
                    "Is there anything else I can help you with?"
                )
                .update_global_data({
                    "ticket_status": "resolved",
                    "resolution_notes": resolution_notes
                })
                .add_action("send_sms", {
                    "to_number": "${global_data.customer_phone}",
                    "body": "Your TechSupport Pro ticket has been resolved. Thank you!"
                })
            )

        @self.tool(
            description="Escalate ticket to a specialist",
            parameters={
                "type": "object",
                "properties": {
                    "specialist_type": {
                        "type": "string",
                        "description": "Type of specialist (billing, technical, account)"
                    }
                },
                "required": ["specialist_type"]
            }
        )
        def escalate_ticket(args: dict, raw_data: dict = None) -> SwaigFunctionResult:
            specialist_type = args.get("specialist_type", "technical")
            specialist_number = SPECIALISTS.get(specialist_type, SPECIALISTS["technical"])
            return (
                SwaigFunctionResult(
                    f"I'm transferring you to our {specialist_type} specialist now. "
                    "Please hold while I connect you.",
                    post_process=True
                )
                .update_global_data({
                    "escalated_to": specialist_type,
                    "ticket_status": "escalated"
                })
                .connect(specialist_number, final=True)
            )

        @self.tool(
            description="Schedule a callback from a specialist",
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
            return (
                SwaigFunctionResult(
                    f"I've scheduled a callback for {preferred_time}. "
                    "A specialist will reach out to you then. "
                    "Is there anything else I can help you with?"
                )
                .update_global_data({
                    "callback_scheduled": preferred_time
                })
            )

        # Part 5: Recording Compliance
        @self.tool(
            description="Enable secure mode to pause recording for sensitive information",
            secure=True
        )
        def secure_mode(args: dict = None, raw_data: dict = None) -> SwaigFunctionResult:
            return (
                SwaigFunctionResult(
                    "Secure mode enabled. Recording has been paused. "
                    "Please provide the sensitive information now."
                )
                .add_action("toggle_record", {"state": "pause"})
            )


if __name__ == "__main__":
    agent = TechSupportAgent()
    agent.run()
