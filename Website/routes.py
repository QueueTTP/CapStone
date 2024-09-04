from flask import Blueprint, views 

routes = Blueprint('routes', __name__)

@routes.route('/about-us')
def about_us():
    return 'About Us Page'

@routes.route('/markets')
def markets():
    return 'Markets Page'