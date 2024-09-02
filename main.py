import os
import json
import hmac
import hashlib
import requests
from datetime import datetime
import argparse
from dotenv import load_dotenv
import sys

class BitfinexAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = "https://api.bitfinex.com/v2"

    def _build_authentication_headers(self, endpoint, payload=None):
        nonce = str(round(datetime.now().timestamp() * 1_000))
        message = f"/api/v2/{endpoint}{nonce}"
        if payload:
            message += json.dumps(payload)
        signature = hmac.new(
            key=self.api_secret.encode("utf8"),
            msg=message.encode("utf8"),
            digestmod=hashlib.sha384
        ).hexdigest()
        return {
            "bfx-apikey": self.api_key,
            "bfx-nonce": nonce,
            "bfx-signature": signature
        }

    def _send_request(self, endpoint, payload=None):
        headers = {
            "Content-Type": "application/json",
            **self._build_authentication_headers(endpoint, payload)
        }
        response = requests.post(f"{self.api_url}/{endpoint}", json=payload, headers=headers)
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            response_json = {"error": "Failed to decode JSON response"}
        return response_json

    def place_order(self, amount, price, order_type="EXCHANGE LIMIT", symbol="tTESTBTC:TESTUSD"):
        endpoint = "auth/w/order/submit"
        payload = {
            "type": order_type,
            "symbol": symbol,
            "amount": str(amount),
            "price": str(price)
        }
        return self._send_request(endpoint, payload)

    def modify_order(self, order_id, new_amount, new_price):
        endpoint = "auth/w/order/update"
        payload = {
            "id": order_id,
            "amount": str(new_amount),
            "price": str(new_price)
        }
        return self._send_request(endpoint, payload)

    def cancel_order(self, order_id):
        endpoint = "auth/w/order/cancel"
        payload = {"id": order_id}
        return self._send_request(endpoint, payload)

    def get_orders(self):
        endpoint = "auth/r/orders"
        return self._send_request(endpoint)

    def retrieve_position(self):
        endpoint = "auth/r/positions"
        return self._send_request(endpoint)

def main():
    load_dotenv()  # Load environment variables from .env file

    api_key = os.getenv("BITFINEX_API_KEY")
    api_secret = os.getenv("BITFINEX_API_SECRET")

    parser = argparse.ArgumentParser(description="Bitfinex API Command Line Tool")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    place_order_parser = subparsers.add_parser("p", help="Place a new order")
    place_order_parser.add_argument("--amount", type=float, required=True, help="Amount of the order")
    place_order_parser.add_argument("--price", type=float, required=True, help="Price of the order")
    place_order_parser.add_argument("--order_type", default="EXCHANGE LIMIT", help="Type of the order")
    place_order_parser.add_argument("--symbol", default="tTESTBTC:TESTUSD", help="Trading symbol")

   
    modify_order_parser = subparsers.add_parser("m", help="Modify an existing order")
    modify_order_parser.add_argument("--order_id", type=int, required=True, help="ID of the order to modify")
    modify_order_parser.add_argument("--new_amount", type=float, required=True, help="New amount of the order")
    modify_order_parser.add_argument("--new_price", type=float, required=True, help="New price of the order")


    cancel_order_parser = subparsers.add_parser("c", help="Cancel an order")
    cancel_order_parser.add_argument("--order_id", type=int, required=True, help="ID of the order to cancel")

    subparsers.add_parser("g", help="Get all active orders")

    subparsers.add_parser("rp", help="Retrieve all positions")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit("Error: No command provided. Please specify a command.")


    api = BitfinexAPI(api_key=api_key, api_secret=api_secret)

    if args.command in "p":
        response = api.place_order(args.amount, args.price, args.order_type, args.symbol)
    elif args.command in "m":
        response = api.modify_order(args.order_id, args.new_amount, args.new_price)
    elif args.command in "c":
        response = api.cancel_order(args.order_id)
    elif args.command in "g":
        response = api.get_orders()
    elif args.command in "rp":
        response = api.retrieve_position()
    
    print(json.dumps(response, indent=4))

if __name__ == "__main__":
    main()
