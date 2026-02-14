import json
import random
from pathlib import Path

random.seed(42)

CATEGORIES = [
    ("Identity > MFA", "Identity Team"),
    ("Identity > Password Reset", "Service Desk"),
    ("Endpoint > Intune Compliance", "Endpoint Team"),
    ("Endpoint > Device Encryption", "Endpoint Team"),
    ("Email > Outlook", "Service Desk"),
    ("Email > Exchange Online", "Messaging Team"),
    ("Collaboration > Teams", "Service Desk"),
    ("Networking > VPN", "Network Team"),
    ("Networking > Wi-Fi", "Network Team"),
    ("Access > Permissions", "Service Desk"),
    ("Hardware > Laptop", "Service Desk"),
    ("Printing > Printer", "Service Desk"),
]

PRIORITIES = ["P1", "P2", "P3", "P4"]

TEMPLATES = {
    "Identity > MFA": [
        "User cannot approve MFA prompt on new phone, keeps failing sign-in.",
        "MFA push notifications not arriving for user, sign-in blocked.",
        "User lost phone and cannot pass MFA, needs reset urgently.",
        "User sees 'MFA required' loop when accessing M365 apps."
    ],
    "Identity > Password Reset": [
        "User forgot password and cannot log in to Windows.",
        "Account locked after too many attempts, needs unlock and reset.",
        "User password expired and they cannot change it remotely.",
        "Password reset not working in self-service portal."
    ],
    "Endpoint > Intune Compliance": [
        "Device shows non-compliant in Intune, Conditional Access blocks sign-in.",
        "Windows device flagged non-compliant due to missing updates.",
        "Compliance policy says firewall disabled, user can't access apps.",
        "Device compliance failure after OS upgrade."
    ],
    "Endpoint > Device Encryption": [
        "BitLocker not enabled, device marked non-compliant.",
        "Encryption status unknown, user can't access resources.",
        "Recovery key prompt appeared unexpectedly after reboot.",
        "BitLocker escrow missing in Entra, needs verification."
    ],
    "Email > Outlook": [
        "Outlook stuck on 'Trying to connect' and won't sync mail.",
        "Outlook keeps asking for password repeatedly.",
        "User can't add shared mailbox to Outlook desktop client.",
        "Outlook search not returning recent emails."
    ],
    "Email > Exchange Online": [
        "Mailbox not receiving external emails, internal works.",
        "User can't send emails, gets NDR bounce back.",
        "Mail flow delayed, emails arrive hours late.",
        "User mailbox storage full, needs cleanup or increase."
    ],
    "Collaboration > Teams": [
        "Teams calls dropping frequently for one user.",
        "User can't join Teams meeting, stuck on connecting.",
        "Teams client crashes on startup after update.",
        "User can't access a Team/channel they should be in."
    ],
    "Networking > VPN": [
        "VPN fails to connect with authentication error.",
        "VPN connects but no access to internal resources.",
        "VPN disconnects every few minutes on home network.",
        "User cannot install VPN client on managed device."
    ],
    "Networking > Wi-Fi": [
        "Office Wi-Fi keeps disconnecting on laptop.",
        "Cannot connect to corporate Wi-Fi, certificate error.",
        "Wi-Fi slow only on one floor, user reports timeouts.",
        "New device cannot see corporate SSID."
    ],
    "Access > Permissions": [
        "User needs access to shared folder, permission denied.",
        "User lost access to SharePoint site after role change.",
        "Request: add user to security group for application access.",
        "User cannot open finance drive, access denied."
    ],
    "Hardware > Laptop": [
        "Laptop battery draining fast, needs diagnostics.",
        "Laptop overheating and fan loud during calls.",
        "Keyboard keys not working properly on user's laptop.",
        "Laptop won't boot, shows black screen."
    ],
    "Printing > Printer": [
        "User cannot print, printer shows offline.",
        "Print jobs stuck in queue and won't clear.",
        "User needs printer drivers installed on new device.",
        "Printer prints blank pages intermittently."
    ],
}

NEXT_ACTIONS = {
    "Identity > MFA": [
        "Check Entra sign-in logs, confirm Conditional Access, reset MFA methods if needed.",
        "Verify user is registered to correct authenticator; reset MFA and re-enrol.",
        "Confirm CA policies and device compliance; perform MFA reset as required."
    ],
    "Identity > Password Reset": [
        "Reset password in Entra/AD, confirm account unlock, advise user to re-authenticate.",
        "Unlock account, reset password, verify SSPR settings and sign-in."
    ],
    "Endpoint > Intune Compliance": [
        "Check compliance policy state; trigger sync, verify required settings (updates/firewall).",
        "Review Intune compliance report; remediate failing checks then re-evaluate."
    ],
    "Endpoint > Device Encryption": [
        "Verify BitLocker status; enable encryption and confirm key escrow to Entra.",
        "Check encryption compliance and recovery key escrow; remediate and re-sync."
    ],
    "Email > Outlook": [
        "Recreate Outlook profile, clear cached credentials, verify connectivity and autodiscover.",
        "Run Microsoft Support and Recovery Assistant; check add-ins and profile."
    ],
    "Email > Exchange Online": [
        "Check message trace and transport rules; verify mailbox settings and quotas.",
        "Review NDR details; validate connectors, SPF/DKIM/DMARC as applicable."
    ],
    "Collaboration > Teams": [
        "Check Teams service health and user network; clear cache and update client.",
        "Verify meeting policy and client version; test web client vs desktop."
    ],
    "Networking > VPN": [
        "Check client logs, verify credentials/CA; confirm VPN policy and MFA requirements.",
        "Validate split tunnel/routes; confirm user group membership and access rules."
    ],
    "Networking > Wi-Fi": [
        "Verify certificate/profile; re-enrol Wi-Fi profile and test connectivity.",
        "Check AP coverage and network health; compare with other devices."
    ],
    "Access > Permissions": [
        "Confirm required group membership; grant least-privilege access and validate.",
        "Check SharePoint permissions inheritance; re-add user or group as appropriate."
    ],
    "Hardware > Laptop": [
        "Collect diagnostics, check warranty, run hardware tests; arrange repair if needed.",
        "Validate power settings/thermals; run vendor diagnostics and update BIOS/drivers."
    ],
    "Printing > Printer": [
        "Restart spooler, clear queue, reinstall drivers; verify printer online status.",
        "Check printer mapping and permissions; test print from another app/device."
    ],
}

def choose_priority(category: str, text: str) -> str:
    t = text.lower()
    if "urgent" in t or "blocked" in t or "cannot log in" in t or "won't boot" in t:
        return "P1"
    if "fails" in t or "error" in t or "stuck" in t or "denied" in t:
        return "P2"
    if "slow" in t or "intermittent" in t:
        return "P3"
    return random.choice(["P3", "P4"])

def make_example():
    (cat, route) = random.choice(CATEGORIES)
    text = random.choice(TEMPLATES[cat])
    priority = choose_priority(cat, text)
    next_action = random.choice(NEXT_ACTIONS[cat])

    # Instruction-style prompt → JSON output
    prompt = (
        "You are an IT service desk triage classifier.\n"
        "Given a ticket, output STRICT JSON with keys:\n"
        "category, priority, route_to, next_action\n"
        "No extra text.\n\n"
        f"TICKET: {text}\n"
        "JSON:"
    )

    label = {
        "category": cat,
        "priority": priority,
        "route_to": route,
        "next_action": next_action
    }

    completion = json.dumps(label, ensure_ascii=False)

    return {"prompt": prompt, "completion": completion}

def main():
    out_train = Path("data/train.jsonl")
    out_eval = Path("data/eval.jsonl")
    out_train.parent.mkdir(parents=True, exist_ok=True)

    # Keep it small but real. You can increase later.
    n_total = 800
    n_eval = 120

    data = [make_example() for _ in range(n_total)]
    random.shuffle(data)
    eval_data = data[:n_eval]
    train_data = data[n_eval:]

    with out_train.open("w", encoding="utf-8") as f:
        for ex in train_data:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    with out_eval.open("w", encoding="utf-8") as f:
        for ex in eval_data:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"Wrote {len(train_data)} train → {out_train}")
    print(f"Wrote {len(eval_data)} eval  → {out_eval}")

if __name__ == "__main__":
    main()
