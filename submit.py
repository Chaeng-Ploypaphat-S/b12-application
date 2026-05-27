import hashlib
import hmac
import json
import os
from datetime import datetime, timezone

import requests


def main():
    signing_secret = os.environ["SIGNING_SECRET"].encode("utf-8")

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    payload = {
        "action_run_link": os.environ["ACTION_RUN_LINK"],
        "email": "ploypaphat.saltz@gmail.com",
        "name": "Ploypaphat Saltz",
        "repository_link": "https://github.com/Chaeng-Ploypaphat-S/b12-application",
        "resume_link": "https://github.com/Chaeng-Ploypaphat-S/b12-application/blob/main/Resume.pdf",
        "timestamp": timestamp,
    }

    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

    hex_digest = hmac.new(signing_secret, body, hashlib.sha256).hexdigest()

    response = requests.post(
        "https://b12.io/apply/submission",
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Signature-256": f"sha256={hex_digest}",
        },
    )
    response.raise_for_status()

    result = response.json()
    print(f"Receipt: {result['receipt']}")


if __name__ == "__main__":
    main()
