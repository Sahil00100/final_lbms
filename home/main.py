import razorpay
client = razorpay.Client(auth=("rzp_test_HILSu4mI2BIBak", "I8hWFGpL2SbFPHXNwkLisHzU"))

data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }

payment = client.order.create(data=data)