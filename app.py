from flask import Flask, request, jsonify
from flask_cors import CORS

from agents.sentinel import detect_pci_pii
from agents.coordinator import compliance_decision
from audit.blockchain import verify_chain

app = Flask(__name__)
CORS(app)  # Allow v0 frontend to call backend

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Main compliance analysis endpoint
    """
    try:
        data = request.json.get("text", "")

        # Sentinel Agent
        detection = detect_pci_pii(data)

        # Coordinator Agent
        decision, audit_block = compliance_decision(detection)

        return jsonify({
            "status": "success",
            "detection": detection,
            "decision": decision,
            "audit_block": audit_block
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/verify", methods=["GET"])
def verify():
    """
    Verify audit chain integrity
    """
    valid = verify_chain()
    return jsonify({
        "chain_valid": valid
    })


@app.route("/", methods=["GET"])
def health():
    """
    Health check endpoint
    """
    return jsonify({
        "message": "Agentic Compliance Backend is running"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
