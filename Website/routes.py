import os
from flask import Blueprint, render_template, views 
from .functions import convert_notebook_to_html



routes = Blueprint('routes', __name__)

@routes.route('/about-us')
def about_us():
    return 'About Us Page'

@routes.route('/markets')
def markets():
    notebook_path = os.path.join(os.getcwd(), 'test.ipynb')

    notebook_html = convert_notebook_to_html(notebook_path)
    
    return render_template('markets.html')