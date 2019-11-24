import sys
# sys.path.append('static/data')

from flask import Flask
from flask import render_template
from flask import jsonify
from flask_bootstrap import Bootstrap
from flask_bootstrap.nav import BootstrapRenderer
from flask_nav import Nav
from flask_nav.elements import *
from flask_nav import register_renderer
from flask import redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
# from sql_queries import *
from pymongodb import user_input
from pymongodb import setup
import matplotlib.pyplot as plt
import os


class InverseRenderer(BootstrapRenderer):
    def visit_Navbar(self, node):
        nav_tag = super(InverseRenderer, self).visit_Navbar(node)
        nav_tag['class'] += 'navbar navbar-inverse'
        return nav_tag

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


def define_routes(app):

    # @login_manager.loader
    # def loader(user_id):
    #     return User.query.get(user_id)

    @app.route('/', methods=['POST', 'GET'])
    def main():
        setup()
        return render_template("index.html", name="Main")

    @app.route('/vis', methods=['POST', 'GET'])
    # @login_required
    def vis():
        return render_template("vis.html", name="Visualisation")

    @app.route('/fetch_designs', methods=['GET'])
    def fetch_designs():
        cuisine = request.args.get("cuisine")
        # land_area_start = request.args.get("land_area_start")
        # land_area_end = request.args.get("land_area_end")
        timings_start = request.args.get("timings_start")
        timings_end = request.args.get("timings_end")
        labels = request.args.get("label")
        city = request.args.get("city")
        #
        label="inside"
        photo_ids = user_input(cuisine, city, timings_start, timings_end)
        print("ids", photo_ids)
        #TODO: Get results from database: similar to sql_queries
        all_images, all_labels = fetch_demo_data()
        # test_images, test_labels = fetch_demo_data()
        # print(test_images)
        # print(test_labels)

        return jsonify(img = all_images, labels = all_labels)

    @app.route('/fetch_business_details', methods=['GET'])
    def fetch_business_details():
        photo_id = request.args.get("photo_id")

        #TODO: Get results from database:
        business_name = 'Cafe Intermezzo'
        address = '1065 Peachtree St NE'
        city = 'Atlanta'
        state = 'Georgia'
        stars = '4.0'
        num_reviews = '1024'
        categories = 'Cafes, Bars, Desserts'

        img_src = './static/data/food/desserts/Cheesecake/165910.jpg'

        return render_template('business_details.html',
                    business_name = business_name,
                    address = address,
                    city = city,
                    state = state,
                    stars = stars,
                    num_reviews = num_reviews,
                    categories = categories,
                    img_src = img_src,
                    )

def nav_init(app):
    nav = Nav()

    @nav.navigation()
    def mynavbar():
        return Navbar(
            'Restaurant Design Inspiration Tool',
            View('Home', 'main'),
            View('Visualization', 'vis'),
        )

    nav.init_app(app)

def fetch_dummy_data():
    all_images = []
    all_labels = []

    images = [['img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg'],
    ['img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg'],
    ['img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg'],
    ['img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg'],
    ['img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg']];
    img_labels = ['Scenary', 'Bands', 'Scenary', 'Bands', 'Scenary' ]
    all_images.append(images)
    all_labels.append(img_labels)

    images = [['img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg'],
    ['img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg'],
    ['img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg'],
    ['img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg'],
    ['img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg']]
    img_labels = ['Scenary', 'Bands', 'Scenary', 'Bands', 'Scenary']
    all_images.append(images)
    all_labels.append(img_labels)

    images = [['img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg'],
    ['img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg'],
    ['img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg'],
    ['img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg'],
    ['img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg']]
    img_labels = ['Scenary', 'Bands', 'Scenary', 'Bands', 'Scenary' ]
    all_images.append(images)
    all_labels.append(img_labels)

    return all_images, all_labels

def fetch_demo_data():
    all_labels = []
    all_images = []

    indoor_outdoor_labels = ['Sweet Hut', 'Amelie\'s French Bakery', 'Sugar Shack', 'Jeni\'s', 'Sublime Donuts']
    food_labels = ['Cheesecake', 'Ice Cream', 'Frozen Yogurt', 'Donuts', 'Apple Pie']

    all_labels.append(food_labels)
    all_labels.append(indoor_outdoor_labels)
    all_labels.append(indoor_outdoor_labels)
    base_path = 'static/data/'

    curr_images = []
    for i in range(5):
        curr_label = food_labels[i]
        path = base_path + 'food/desserts/' + food_labels[i] + '/'
        curr_food_images = []
        for filename in os.listdir(path):
            if filename.endswith(".jpg"):
                curr_food_images.append('./' + path + filename)
        curr_images.append(curr_food_images)
    all_images.append(curr_images)

    curr_images = []
    for i in range(5):
        path = base_path + 'indoors/' + indoor_outdoor_labels[i] + '/'
        curr_food_images = []
        for filename in os.listdir(path):
            if filename.endswith(".jpg"):
                curr_food_images.append('./' + path + filename)
        curr_images.append(curr_food_images)
    all_images.append(curr_images)

    curr_images = []
    for i in range(5):
        path = base_path + 'outdoors/' + indoor_outdoor_labels[i] + '/'
        curr_food_images = []
        for filename in os.listdir(path):
            if filename.endswith(".jpg"):
                curr_food_images.append('./' + path + filename)
        curr_images.append(curr_food_images)
    all_images.append(curr_images)

    return all_images, all_labels


if __name__ == "__main__":
    app = create_app()
    define_routes(app)
    register_renderer(app, 'inverse', InverseRenderer)
    nav_init(app)
    # login_manager.init_app(app)
    app.run(port=8000 ,debug=True)
