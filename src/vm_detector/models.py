from dataclasses import dataclass

@dataclass
class VMIndicator:
    evidence: str
    high_confidence: bool = False
