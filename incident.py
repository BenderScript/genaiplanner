from typing import Annotated, Dict
from langchain_core.tools import tool, StructuredTool


class Incident:
    @tool
    def read_incident(self, incident_id: Annotated[str, "ID of the incident to read"]) -> Dict[str, str]:
        """
        Read the details of a DevOps incident from PagerDuty

        Args:
            incident_id (str): ID of the incident to read.

        Returns:
            Dict[str, str]: A dictionary containing the incident details.
        """
        # Implement the logic to read the incident details
        return {
            "id": "INC-123",
            "title": "Server Outage",
            "description": "The main application server went down, causing a service disruption.",
            "severity": "high",
            "status": "open",
        }

    @tool
    def clean_incident(self, incident: Annotated[Dict[str, str], "Incident details to clean"]) -> Dict[str, str]:
        """
        Clean the details of a DevOps incident to be triaged.

        Args:
            incident (Dict[str, str]): A dictionary containing the incident details.

        Returns:
            Dict[str, str]: The cleaned incident details.
        """
        # Implement the logic to clean the incident details
        cleaned_incident = incident.copy()
        cleaned_incident["description"] = cleaned_incident["description"].strip()
        return cleaned_incident

    @tool
    def escalate_incident(self, incident: Annotated[Dict[str, str], "Incident details to escalate"]) -> str:
        """
        Escalate a DevOps incident.

        Args:
            incident (Dict[str, str]): A dictionary containing the incident details.

        Returns:
            str: A confirmation message.
        """
        # Implement the logic to resolve the incident
        return f"Incident {incident['id']} has been resolved."

    def get_tools(self):
        """Return a list of unbound method callables in this toolkit."""
        return [
            self.__class__.read_incident,
            self.__class__.clean_incident,
            self.__class__.escalate_incident
        ]

