class FraudRiskEngine:

    def __init__(self, lr, invoice):

        self.lr = lr
        self.invoice = invoice
        self.risk_points = 0
        self.reasons = []

    # -------- LR CHECK --------
    def check_lr(self):

        if self.lr.get("lr_number") != self.invoice.get("lr_number"):
            self.risk_points += 30
            self.reasons.append("LR number mismatch")

    # -------- MANUAL CHARGES FRAUD CHECK --------
    def check_manual_charges(self):

        freight = self.lr.get("freight", 0)
        manual = self.invoice.get("manual_total", 0)

        if manual > freight:

            self.risk_points += 70
            self.reasons.append("Manual charges exceed agreed freight")

    # -------- RISK LEVEL --------
    def risk_level(self):

        if self.risk_points < 20:
            return "SAFE"
        elif self.risk_points < 40:
            return "LOW RISK"
        elif self.risk_points < 70:
            return "MEDIUM RISK"
        else:
            return "HIGH FRAUD RISK"

    # -------- RUN ENGINE --------
    def run(self):

        self.check_lr()
        self.check_manual_charges()

        fraud_probability = min(self.risk_points, 100)

        return {
            "fraud_probability": fraud_probability,
            "risk_level": self.risk_level(),
            "reasons": self.reasons
        }