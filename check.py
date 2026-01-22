import os
import requests
from bs4 import BeautifulSoup

URL = os.environ["URL"]
NTFY_TOPIC = os.environ["NTFY_TOPIC"]

def notify(title: str, message: str):
    # Keep headers ASCII-only (latin-1 safe)
    safe_title = title.encode("latin-1", "ignore").decode("latin-1")
    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode("utf-8"),
        headers={
            "Title": safe_title,   # no emoji here
            "Priority": "high",
        },
        timeout=20
    )


def main():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=25)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    checkout_button = soup.select_one("button[name='checkout']")

    if checkout_button is None:
        # Markup changed. Notify once so you know it broke.
        notify("Stock check failed ⚠️", f"Could not find checkout button.\n{URL}")
        return

    is_sold_out = checkout_button.has_attr("disabled")

    if is_sold_out:
        pass
    else:
        notify("IN STOCK ✅", f"Buy now:\n{URL}")

if __name__ == "__main__":
    main()
