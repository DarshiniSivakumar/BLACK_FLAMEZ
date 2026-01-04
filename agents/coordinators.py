from audit.blockchain import add_audit_entry
<<<<<<< HEAD
=======

>>>>>>> 2bc8181 (Add all agent files)
def compliance_decision(detection_output):
    """
    Coordinator Agent:
    - Interprets sentinel output
    - Assigns compliance risk
    - Logs immutable audit entry
    """
    if detection_output.get("pci_detected"):
        risk = "HIGH"
        action = "Mask or tokenize card data"
    elif detection_output.get("pii_detected"):
        risk = "MEDIUM"
        action = "Apply data minimization"
    else:
        risk = "LOW"
        action = "No action required"

    decision = {
        "risk_level": risk,
        "recommended_action": action,
        "sentinel_findings": detection_output
    }
    audit_block = add_audit_entry(decision)
    return decision, audit_block