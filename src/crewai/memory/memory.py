from typing import Any, Dict

from crewai.memory.storage.interface import Storage


class Memory:
    """
    Base class for memory, now supporting agent tags and generic metadata.
    """

    def __init__(self, storage: Storage, ontology: Ontology):
        self.storage = storage
        self.ontology = ontology

    def save(
        self, value: Any, metadata: Dict[str, Any] = None, agent: str = None
    ) -> None:
        metadata = metadata or {}
        if agent:
            metadata["agent"] = agent
        self.storage.save(value, metadata)
        self.ontology.update_knowledge(value, metadata, agent)

    def search(self, query: str) -> Dict[str, Any]:
        # Perform a semantic search using the ontology
        results = self.ontology.semantic_search(query)

        # Retrieve the relevant knowledge from the storage based on the search results
        knowledge = self.storage.get_knowledge(results)

        return knowledge

    def reason(self, query: str) -> Dict[str, Any]:
        # Perform reasoning using the ontology
        results = self.ontology.reason(query)

        return results
