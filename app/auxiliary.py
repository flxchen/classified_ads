from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_mail import Message
import stripe.error
from config import Config
from . import mail
import stripe

aux = Blueprint('aux',__name__)
# This module defines routes for an auxiliary Flask application, handling about, contact, and donation functionalities. 
# The 'about' route renders an about page, the 'contact' route manages contact form submissions and sends emails, 
# and the 'donate' route processes payments via Stripe, sends receipts, and handles errors.
@aux.route("/about")
def about():
    return render_template("about.html")

@aux.route("/contact", methods=['POST','GET'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        topic = request.form['topic']
        body = request.form['body']
        
        # Compose the email message
        msg = Message(f"New Contact Us message: {topic}",
                      recipients=[Config.MAIL_USERNAME])
        msg.body = f"From: {email}\nTopic: {topic}\n\n{body}"
        
        try:
            mail.send(msg)
            flash('Message sent successfully!','success')
            return redirect(url_for('auth.home'))
        except Exception as e:
            flash('Failed to send message.','danger')
            print(e)
    return render_template('contact.html')


stripe.api_key = Config.STRIPE_SECRET_KEY
@aux.route('/donate',methods=['POST','GET'])
def payment():
    if request.method == 'POST':
        email = request.form['email']
        amount = int(float(request.form['amount']) * 100)  # Convert dollars to cents
        token = request.form['stripeToken']  # Stripe token from form
        
        try:
            # Create a charge on Stripe
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description='Payment for classified ad',
                source=token,
                receipt_email=email,
            )
            
            # Send email receipt
            send_receipt(email,amount/100)  # Convert cents back to dollars
            flash('Thank you! Your payment has been received.','success')
            # Redirect to success page
            return redirect(url_for('auth.home'))

        except stripe.error.StripeError as e:
            flash('Unfortunately, your payment could not be processed. Please try again.','danger')
            print(f"Stripe error: {e.user_message}")
            return render_template('payment.html', stripe_public_key=Config.STRIPE_PUBLIC_KEY)
    return render_template('payment.html', stripe_public_key=Config.STRIPE_PUBLIC_KEY)

@aux.route('/send-receipt', methods=['POST'])
def send_receipt(email,amount):    
    try:        
        msg = Message(
            subject="Payment Receipt",            
            recipients=[email]
        )
        msg.body = f"Thank you for your payment ${amount}! Your transaction was successful!\n\nmylisting16 management team"
        mail.send(msg)        
        return jsonify({'status': 'Receipt sent'}), 200
    except Exception as e:
        print(f"email error: {e}")
        return jsonify({'error': str(e)}), 400
    
from flask import send_from_directory
from os import path
@aux.route('/robots.txt')
def robots_txt():
    cur_path = path.dirname(path.abspath(__file__))
    return send_from_directory(cur_path, 'robots.txt')