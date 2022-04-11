from login.celery import celery_app as app


@app.task
def send_otp(otp, phone_number):
    # @todo 
    print(f"you otp is {otp}")
