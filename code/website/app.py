import sys
sys.path.append('static/data')

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
from sql_queries import *

import matplotlib.pyplot as plt


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

    # @login_manager.user_loader
    # def user_loader(user_id):
    #     return User.query.get(user_id)

    @app.route('/', methods=['POST', 'GET'])
    def main():
        return render_template("index.html", name="Main")

    @app.route('/vis', methods=['POST', 'GET'])
    # @login_required
    def vis():
        return render_template("vis.html", name="Visualisation")


    @app.route('/fetch_filtered_data')
    def fetch_filtered_data():
        # return(jsonify(request.args.getlist('census_tracts[]')))
        census_tracts = request.args.getlist("census_tracts[]")
        start_year = "2018"
        end_year = request.args.get("prediction_year")
        bathrooms_start = request.args.get("bathrooms_start")
        bathrooms_end = request.args.get("bathrooms_end")
        bedrooms_start = request.args.get("bedrooms_start")
        bedrooms_end = request.args.get("bedrooms_end")
        land_area_start = request.args.get("land_area_start")
        land_area_end = request.args.get("land_area_end")
        price_start = request.args.get("price_start")
        price_end = request.args.get("price_end")

        result = choropleth_query(census_tracts,start_year,end_year,
        bathrooms_start,bathrooms_end,bedrooms_start,bedrooms_end,
        land_area_start,land_area_end,price_start,price_end)

        return jsonify(result)
    
    @app.route('/fetch_tract_data')
    def fetch_tract_data():
        census_tract = request.args.get("census_tract")
        start_year = "2018"
        end_year = request.args.get("prediction_year")
        bathrooms_start = request.args.get("bathrooms_start")
        bathrooms_end = request.args.get("bathrooms_end")
        bedrooms_start = request.args.get("bedrooms_start")
        bedrooms_end = request.args.get("bedrooms_end")
        land_area_start = request.args.get("land_area_start")
        land_area_end = request.args.get("land_area_end")
        price_start = request.args.get("price_start")
        price_end = request.args.get("price_end")

        result = census_tract_data(census_tract,start_year,end_year,
        bathrooms_start,bathrooms_end,bedrooms_start,bedrooms_end,
        land_area_start,land_area_end,price_start,price_end)

        result = result[int(census_tract)]

        # Create plot
        x = result.keys()
        y = result.values()
        plt.plot(x, y)
        plt.title("Census Tract Details")
        plt.xlabel("Years")
        plt.ylabel("Average Prices")
        plt.savefig('static/data/images/tractDetails.png', dpi=200)
        plt.close()

        return census_tract


    @app.route('/fetch_designs', methods=['GET'])
    def fetch_designs():
        cuisine = request.args.get("cuisine")
        land_area_start = request.args.get("land_area_start")
        land_area_end = request.args.get("land_area_end")
        timings_start = request.args.get("timings_start")
        timings_end = request.args.get("timings_end")
        labels = request.args.get("label")

        #TODO: Get results from database: similar to sql_queries
        # image = '<img src="../static/data/images/tractDetails.png" alt="Sample" width="600" height="400">'
        all_images = []
        all_labels = []
        # if(label == 'Food'):

        images = [['img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg'], 
        ['img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg'],
        ['img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg'],
        ['img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg'],
        ['img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg', 'img_nature_wide.jpg']];
        img_labels = ['Scenary', 'Bands', 'Scenary', 'Bands', 'Scenary' ]
        all_images.append(images)
        all_labels.append(img_labels)
        # return jsonify(img = images, labels = img_labels)

        # if(label == 'Indoors'):
        images = [['img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg'], 
        ['img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg'],
        ['img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg'],
        ['img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg'],
        ['img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg', 'img_mountains_wide.jpg']]
        img_labels = ['Scenary', 'Bands', 'Scenary', 'Bands', 'Scenary']
        all_images.append(images)
        all_labels.append(img_labels)

        # if(label == 'Outdoors'):
        images = [['img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg'], 
        ['img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg'],
        ['img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg'],
        ['img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg'],
        ['img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg', 'img_band_la.jpg']]
        img_labels = ['Scenary', 'Bands', 'Scenary', 'Bands', 'Scenary' ]
        all_images.append(images)
        all_labels.append(img_labels)
            
        return jsonify(img = all_images, labels = all_labels)


    @app.route('/fetch_portfolio', methods=['GET'])
    def fetch_portfolio():
        census_tracts = request.args.getlist("census_tracts[]")
        start_year = "2018"
        end_year = request.args.get("prediction_year")
        bathrooms_start = request.args.get("bathrooms_start")
        bathrooms_end = request.args.get("bathrooms_end")
        bedrooms_start = request.args.get("bedrooms_start")
        bedrooms_end = request.args.get("bedrooms_end")
        land_area_start = request.args.get("land_area_start")
        land_area_end = request.args.get("land_area_end")
        price_start = request.args.get("price_start")
        price_end = request.args.get("price_end")
        total_budget = request.args.get("total_budget")




        result, names_dict, best_years = portfolio_query(census_tracts,start_year,end_year,
        bathrooms_start,bathrooms_end,bedrooms_start,bedrooms_end,
        land_area_start,land_area_end,price_start,price_end,total_budget)


        # Plot CUM RETURN
        x = [year for year in range(int(start_year), int(end_year)+1)]
        y = [sum([row[names_dict[str(year)]] for row in result]) for year in x]
        plt.plot(x, y)
        plt.title("Portfolio Value over the Years")
        plt.xlabel("Years")
        plt.ylabel("Portfolio Value")
        plt.savefig('static/data/images/portfolioValue.png', dpi=200)
        plt.close()


        # Plot scatter of rooms vs returns with size depending on landarea
        x = [row[names_dict["returns"]] for row in result]
        y = [row[names_dict["ROOMS"]] for row in result]
        areas = [row[names_dict["LANDAREA"]] for row in result]

        plt.scatter(x, y, s=areas, alpha=0.5)
        plt.title("Rooms vs Returns scaled by Land Area")
        plt.xlabel("Returns")
        plt.ylabel("Number of Rooms")
        plt.savefig('static/data/images/portfolioRooms.png', dpi=200)
        plt.close()

        # Piechart of grade
        labels = set([row[names_dict['GRADE']] for row in result])
        sizes =  [sum([ (1 if row[names_dict['GRADE']] == label else 0) for row in result]) for label in labels]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal') 
        plt.title("Distribution of Property Grades")
        plt.savefig('static/data/images/portfolioPie.png', dpi=200)
        plt.close()

        return render_template("portfolio.html",result = result, names_dict = names_dict, end_year = end_year, best_years = best_years)


    @app.route('/login', methods=['POST', 'GET'])
    def login():
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'admin' or request.form['password'] != 'admin':
                error = 'Invalid Credentials. Please try again.'
            else:
                return redirect(url_for('main'))
        return render_template('login.html', error=error)

def nav_init(app):
    nav = Nav()

    @nav.navigation()
    def mynavbar():
        return Navbar(
            'Real Estate Portfolio',
            View('Home', 'main'),
            View('Visualization', 'vis'),
        )

    nav.init_app(app)


if __name__ == "__main__":
    app = create_app()
    define_routes(app)
    register_renderer(app, 'inverse', InverseRenderer)
    nav_init(app)
    # login_manager.init_app(app)
    app.run(port=8000 ,debug=True)
