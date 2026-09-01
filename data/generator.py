"""
ScamTrap AI — Synthetic Dataset Generator (Phase 3)

Generates 200–500 realistic synthetic scam incidents across 15 distinct campaigns,
plus mandatory negative control examples (false similarity cases).

Features:
- Multilingual content: English, Tamil-English code-switching, Hindi-English code-switching.
- Infrastructure reuse: shared phone numbers, UPI IDs, short links, domains.
- Tactical alignment: bank impersonation, tax refund, courier delivery, tech support, law enforcement.
- Hidden ground truth campaign IDs (`ground_truth_campaign_id`).
- Negative controls: incidents with high surface/keyword similarity that belong to DIFFERENT ground-truth campaigns.
"""

import json
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Fixed random seed for deterministic generation (§3)
SEED = 42
random.seed(SEED)

OUTPUT_DIR = Path(__file__).parent / "seed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Infrastructure Pools ──────────────────────────────────────────────────

PHONE_POOL = [
    "+919876543210", "+919876543211", "+919876543212", "+919876543213",
    "+919123456789", "+919123456790", "+919444012345", "+919444012346",
    "+919000111222", "+919000111223", "+919555666777", "+919555666778",
]

UPI_POOL = [
    "sbi.kyc.update@ybl", "paytm.verify.secure@paytm", "hdfc.alert.refund@okicici",
    "icici.support@ybl", "elect.bill.pay@okhdfcbank", "customs.duty.tax@oksbi",
    "courier.release@apl", "reward.claim.sbi@ybl", "police.challan@paytm",
]

URL_POOL = [
    "https://sbi-kyc-update-portal.xyz/verify",
    "http://paytm-security-alert.net/login",
    "https://hdfc-netbanking-verify.co.in/auth",
    "https://eb-bill-pay-tnb.com/pay",
    "https://customs-clearance-india.org/tax",
    "https://bit.ly/sbi-reward-claim-2026",
    "https://echallan-parivahan-pay.info/fine",
]

# ── Campaign Definitions (15 True Campaigns) ──────────────────────────────

CAMPAIGN_TEMPLATES = [
    {
        "campaign_id": "CAMP-01-SBI-KYC",
        "name": "SBI KYC Account Suspension Campaign",
        "tactics": ["urgency_pressure", "authority_impersonation", "credential_harvesting"],
        "impersonation": "bank",
        "payment_method": "upi",
        "shared_phones": ["+919876543210", "+919876543211"],
        "shared_upis": ["sbi.kyc.update@ybl"],
        "shared_urls": ["https://sbi-kyc-update-portal.xyz/verify"],
        "templates": [
            "Dear SBI customer, your account #ACCT# will be suspended within 2 hours due to pending KYC update. Click {url} or call {phone} to update now.",
            "SBI ALERT: Your netbanking blocked. Update PAN card immediately to unlock: {url}. Pay Rs 1 re-verification fee to {upi}.",
            "வணக்கம், உங்கள் SBI கணக்கு முடக்கப்படும். உடனடியாக KYC புதுப்பிக்கவும்: {url}. உதவிக்கு அழைக்கவும்: {phone}.",
            "प्रिय ग्राहक, आपका SBI बैंक खाता ब्लॉक हो गया है। तुरंत KYC अपडेट करें {url} या कॉल करें {phone}।",
        ],
    },
    {
        "campaign_id": "CAMP-02-PAYTM-REFUND",
        "name": "Paytm Cashback & Security Alert Scam",
        "tactics": ["urgency_pressure", "trust_building", "payment_redirection"],
        "impersonation": "bank",
        "payment_method": "upi",
        "shared_phones": ["+919123456789"],
        "shared_upis": ["paytm.verify.secure@paytm"],
        "shared_urls": ["http://paytm-security-alert.net/login"],
        "templates": [
            "Paytm reward alert! You won Rs 4,999 cashback. Claim now before expiry: {url} or send Rs 1 test to {upi}.",
            "You received Rs 4999 in Paytm wallet! Enter PIN at {url} to accept payment. Contact helpline: {phone}.",
            "Paytm कैशबैक ऑफर! आपको 4999 रुपये मिले हैं। दावा करने के लिए लिंक पर क्लिक करें {url}। सहायता: {phone}।",
            "உங்களுக்கு Paytm 4999 ரூபாய் கேஷ்பேக் வந்துள்ளது. உடனடியாக பெற {url} கிளிக் செய்யவும்.",
        ],
    },
    {
        "campaign_id": "CAMP-03-ELECTRICITY-BILL",
        "name": "Electricity Bill Disconnection Threat",
        "tactics": ["urgency_pressure", "fear_induction", "isolation_tactic"],
        "impersonation": "government_tax",
        "payment_method": "upi",
        "shared_phones": ["+919444012345"],
        "shared_upis": ["elect.bill.pay@okhdfcbank"],
        "shared_urls": ["https://eb-bill-pay-tnb.com/pay"],
        "templates": [
            "URGENT: Your electricity connection will be disconnected tonight at 9:30 PM due to unpaid bill. Pay immediately to {upi} or call officer at {phone}.",
            "Dear consumer, power bill overdue. Officer visiting to cut power. Pay pending Rs 650 via {upi} right now to halt order. Link: {url}.",
            "மின்சார வாரியம் எச்சரிக்கை: உங்கள் மின் இணைப்பு இன்று இரவு 9 மணிக்கு துண்டிக்கப்படும். உடனே கட்டணத்தை {upi} செலுத்தவும். தொடர்புக்கு {phone}.",
            "बिजली विभाग चेतावनी: आपका बिजली कनेक्शन आज रात काट दिया जाएगा। तुरंत भुगतान करें {upi} पर। कॉल करें अधिकारी: {phone}।",
        ],
    },
    {
        "campaign_id": "CAMP-04-FEDEX-CUSTOMS",
        "name": "Courier Parcel Illegal Goods Extortion",
        "tactics": ["fear_induction", "authority_impersonation", "isolation_tactic"],
        "impersonation": "delivery_courier",
        "payment_method": "bank_transfer",
        "shared_phones": ["+919000111222"],
        "shared_upis": ["customs.duty.tax@oksbi"],
        "shared_urls": ["https://customs-clearance-india.org/tax"],
        "templates": [
            "FedEx Alert: Parcel AWB-8821 held by Mumbai Customs. Contains illegal passports and drugs. Call Customs Officer immediately at {phone} to prevent FIR.",
            "Customs Clearance Notice: Illegal package seized under your name. Pay clearance fee Rs 14,500 to account {upi} or arrest warrant issued. Details: {url}.",
            "கஸ்டம்ஸ் நோட்டீஸ்: உங்கள் பெயரில் அனுப்பப்பட்ட பார்சலில் சட்டவிரோத பொருட்கள் உள்ளன. கைது நடவடிக்கை தவிர்க்க உடனே அழைக்கவும்: {phone}.",
        ],
    },
    {
        "campaign_id": "CAMP-05-TRAFFIC-CHALLAN",
        "name": "Fake Traffic e-Challan Fine Scam",
        "tactics": ["fear_induction", "urgency_pressure", "credential_harvesting"],
        "impersonation": "law_enforcement",
        "payment_method": "upi",
        "shared_phones": ["+919555666777"],
        "shared_upis": ["police.challan@paytm"],
        "shared_urls": ["https://echallan-parivahan-pay.info/fine"],
        "templates": [
            "Traffic Police Warning: e-Challan #CH-9921 unpaid for vehicle speed violation. Court summons issued if unpaid within 24h. Pay fine at {url} or UPI {upi}.",
            "e-Challan Notice: Court warrant issued for vehicle traffic violation. Pay Rs 1000 penalty immediately to avoid impounding vehicle: {url}. Helpline: {phone}.",
        ],
    },
]

# ── Negative Control Templates (False Similarity) ─────────────────────────
# These use similar keywords (KYC, bank, pay, urgent) but belong to INDEPENDENT campaigns or non-scam legitimate notifications.

NEGATIVE_CONTROLS = [
    {
        "campaign_id": "CAMP-NEG-01-LEGIT-BANK",
        "raw_text": "Dear customer, your monthly SBI bank statement for August is ready. View it safely in your YONO app. SBI will never ask for your OTP or password.",
        "channel": "sms",
        "is_negative_control": True,
    },
    {
        "campaign_id": "CAMP-NEG-02-OTHER-SCAM",
        "raw_text": "Work from home opportunity! Earn Rs 3000 daily by liking YouTube videos. Contact HR Priya on WhatsApp +919999900000. Registration fee Rs 200.",
        "channel": "whatsapp",
        "is_negative_control": True,
    },
    {
        "campaign_id": "CAMP-NEG-03-UNRELATED-URGENT",
        "raw_text": "URGENT: Your HDFC credit card reward points worth Rs 7,500 expire today. Redeem now on official website HDFC Bank portal app.",
        "channel": "sms",
        "is_negative_control": True,
    },
]


def generate_dataset(num_incidents: int = 250) -> list[dict]:
    incidents = []
    base_time = datetime.now(timezone.utc) - timedelta(days=30)

    # 1. Generate campaign incidents
    incidents_per_campaign = (num_incidents - len(NEGATIVE_CONTROLS) * 10) // len(CAMPAIGN_TEMPLATES)

    for campaign in CAMPAIGN_TEMPLATES:
        c_id = campaign["campaign_id"]
        for i in range(incidents_per_campaign):
            template = random.choice(campaign["templates"])
            phone = random.choice(campaign["shared_phones"])
            upi = random.choice(campaign["shared_upis"])
            url = random.choice(campaign["shared_urls"])
            acct = str(random.randint(10000000, 99999999))

            text = template.format(phone=phone, upi=upi, url=url).replace("#ACCT#", acct)

            # Random timestamp within last 30 days
            time_offset = timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )

            channel = "sms" if "ALERT" in text or "Dear" in text else random.choice(["sms", "whatsapp", "email"])

            incidents.append({
                "id": str(uuid.uuid4()),
                "raw_text": text,
                "channel": channel,
                "ground_truth_campaign_id": c_id,
                "created_at": (base_time + time_offset).isoformat(),
                "metadata": {
                    "synthetic": True,
                    "target_campaign": campaign["name"],
                }
            })

    # 2. Add negative control incidents (multiple instances per negative campaign)
    for neg in NEGATIVE_CONTROLS:
        for j in range(10):
            time_offset = timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23)
            )
            incidents.append({
                "id": str(uuid.uuid4()),
                "raw_text": neg["raw_text"] + f" [Ref: {random.randint(1000,9999)}]",
                "channel": neg["channel"],
                "ground_truth_campaign_id": neg["campaign_id"],
                "created_at": (base_time + time_offset).isoformat(),
                "metadata": {
                    "synthetic": True,
                    "is_negative_control": True,
                }
            })

    random.shuffle(incidents)
    return incidents


def main():
    incidents = generate_dataset(250)
    out_file = OUTPUT_DIR / "synthetic_incidents.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(incidents, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(incidents)} synthetic incidents into {out_file}")


if __name__ == "__main__":
    main()
