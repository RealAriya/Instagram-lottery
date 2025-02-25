
import requests

def process_payment(amount, callback_url):
    api_key = "your_payir_api_key"
    response = requests.post(
        "https://pay.ir/payment/send",
        data={"api": api_key, "amount": amount, "redirect": callback_url}
    )
    if response.status_code == 200:
        payment_url = response.json().get("payment_url")
        return payment_url
    else:
        return None