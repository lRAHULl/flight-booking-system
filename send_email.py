import os
import smtplib


def sendMail(userEmail: str, bookingId: int, flight: dict, flag: bool):
    """
        @author Rahul
        
        Send Emails using `smtplib`
    """
    SERVER_EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    SERVER_EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            print('--------------------------------------------------------')

            print("creating connection to email server")
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            print("logging into email")
            smtp.login(SERVER_EMAIL_ADDRESS, SERVER_EMAIL_PASSWORD)

            print("Prepparing Email")
            if flag:
                subject = 'Flight Booking System - Booking Confirmation'
                body = f'Hello {userEmail},\n\nYour Flight Booking with booking id {bookingId} has been confirmed from {flight["source"]} to {flight["destination"]}.\n\nHave a safe journey.'
            else:
                subject = 'Flight Booking System - Booking Cancellation'
                body = f'Hello {userEmail},\n\nAs per your request, your booking with id {bookingId} has been cancelled.\n\nThank you.'

            message = f'Subject: {subject}\n\n{body}'

            print("sending Email")
            smtp.sendmail(SERVER_EMAIL_ADDRESS, userEmail, message)
            print(f'Successfully sent email to {userEmail}')
            print('--------------------------------------------------------')
            return True
    except:
        print("Cannot send Email.. something went wrong")
        return False