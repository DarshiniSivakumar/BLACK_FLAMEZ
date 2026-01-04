from agents.coordinator import compliance_decision
sample_detection = {
    "pci_detected": True,
    "pii_detected": False,
    "pci_examples": ["1234 5678 9012 3456"],
    "pii_examples": []
}
decision, block = compliance_decision(sample_detection)
print("Decision:", decision)
print("Audit Block:", block)