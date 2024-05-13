from flask import Flask, render_template
from security import safe_requests

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

@app.route('/contact')
def contact():
    h1 = "Contact Me"
    subheading = "Have questions? I have answers."
    image = "static/assets/img/contact-bg.jpg"

    return render_template("contact.html", h1=h1, subheading=subheading, image=image)
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