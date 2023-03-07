from flask import Flask, render_template
import requests

app = Flask(__name__)
response= requests.get('https://api.npoint.io/e9ce5efdcc66fd2beda7')
data = response.json()
data_len = len(data)
date_list = ['September 24, 2022', 'September 18, 2022', 'August 24, 2022', 'July 8, 2022']
post_wallpaper = ['https://cdn.wallpapersafari.com/9/26/Bcfp7u.jpeg', 'https://collegethoughts.com/wp-content/uploads/header-back-new.jpg', 'https://health.osu.edu/-/media/health/images/stories/2022/05/intermittent-fasting-plate.jpg']
@app.route('/')
def home():
    return render_template('index.html', data=data, dates=date_list, data_len=data_len)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/blog_post/<num>')
def blog_post(num):
    print(num)
    return render_template('post.html', num=int(num), data=data, data_len=data_len, dates=date_list, post_wallpaper=post_wallpaper)



if __name__=='__main__':
    app.run(debug=True)