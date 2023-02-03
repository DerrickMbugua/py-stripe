from flask import Flask, redirect, request, render_template, jsonify

import stripe
import os

app = Flask(__name__)

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
}

stripe.api_key = stripe_keys["secret_key"]

# stripe.api_key = "sk_test_51LBavkJmXMB6bamczRrcbUBvTNiR9j9k3tjinQ5Sa7RM9x7D9XAsuI6sFYkXrrxAMLyVUAG4KWY8uXDEUay0pRuO00r9Mnmaqs"

YOUR_DOMAIN = "http://localhost:5000"

@app.route("/")
def index():
  return render_template("home.html")
  # return render_template("index.html")
  
@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

# charges API (legacy) using frontend
@app.route("/charge", methods=["POST"])
def charge():
  # Get the credit card details submitted by the form
  token = request.form.get("stripeToken")
 
  # Create a charge: this will charge the user's card
  try:
    charge = stripe.Charge.create(
      amount=1000, # Amount in cents
      currency="usd",
      source=token,
      description="Example charge"
    )
  except stripe.error.CardError as e:
    # The card has been declined
    return render_template('cancel.html')
 
  return render_template('success.html')
  
@app.route("/checkout-page")
def checkout_page():
    return render_template('checkout.html')
  
@app.route("/success-page")
def success():
    return render_template('success.html')
  
@app.route("/cancel-page")
def checkout():
    return render_template('cancel.html')
  
@app.route("/cancelled")
def cancelled():
    return render_template("cancel.html")
  
@app.route('/create-checkout-session')
def create_checkout_session():
    domain_url = "http://127.0.0.1:5000/"
    stripe.api_key = stripe_keys["secret_key"]

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - capture the payment later
        # [customer_email] - prefill the email input in the form
        # For full details see https://stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "name": "T-shirt",
                    "quantity": 1,
                    "currency": "usd",
                    "amount": "2000",
                }
            ]
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e))
# def create_checkout_session():
#   try:
#         checkout_session = stripe.checkout.Session.create(
#             line_items = [
#                 {
#                     "price":"price_1MXIGzJmXMB6bamc04pg0pXU",
#                     "quantity":1
#                 }
#             ],
#             mode="subscription",
#             success_url=YOUR_DOMAIN + "/success.html",
#             cancel_url = YOUR_DOMAIN + "/cancel.html"
#         )
#   except Exception as e:
#         return str(e)
 
#   return "<p>Successful</p>"
  