import os
import requests
from bs4 import BeautifulSoup

URL = os.environ["URL"]
NTFY_TOPIC = os.environ["NTFY_TOPIC"]

def notify(title: str, message: str):
    # Send a push notification via ntfy
    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=message.encode("utf-8"),
        headers={"Title": title, "Priority": "high"},
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
        notify("IN STOCK ✅", f"Buy now:\n{URL}")
    else:
        notify("IN STOCK ✅", f"Buy now:\n{URL}")

if __name__ == "__main__":
    main()
