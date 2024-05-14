from flask import Flask, render_template, request
from security import safe_requests

import smtplib
import os

app = Flask(import_name="main")

BLOGS = safe_requests.get("https://api.npoint.io/674f5423f73deab1e9a7").json()


@app.route('/')
def home():

    h1 = "Angela's Blog"
    subheading = "A Blog Theme by Start Bootstrap"
    image = "static/assets/img/home-bg.jpg"

    return render_template("index.html", blogs=BLOGS,h1=h1, subheading=subheading, image=image)

@app.route('/about')
def about():
    h1 = "About Me"
    subheading = "This is what I do."
    image = "static/assets/img/about-bg.jpg"

    return render_template("about.html", h1=h1, subheading=subheading, image=image)

@app.route('/contact', methods=["GET", "POST"])
def contact():
    api_token = os.environ.get('API_TOKEN')
    if request.method == 'GET':
        h1 = "Contact Me"
        subheading = "Have questions? I have answers."
        image = "static/assets/img/contact-bg.jpg"

        return render_template(
            "contact.html", h1=h1, subheading=subheading, image=image, api_key=api_token)

    elif request.method == 'POST':
        my_email = os.environ.get('EMAIL')
        pw = os.environ.get('PW')
        full_name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        msg = request.form['msg']

        full_email = (f"Subject: New message from {full_name}\n\n"
                      f"{msg}\n\nReply immediately to {email} or call at {phone}.").encode('utf-8')

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password="itksbmzvrgzlxnen")
            connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=full_email)

        return render_template("confirmation.html", api_key=api_token)

@app.route('/post/<int:id>')
def post(**kwargs):
    index = int(kwargs['id']) - 1
    blog = BLOGS[index]
    image = blog['image_url']
    h1 = blog['title']
    subheading = blog['subtitle']
    body = blog['body']

    return render_template(
        "post.html", h1=h1, subheading=subheading, image=image, body=body)


if __name__ == "__main__":
    app.run(debug=True)