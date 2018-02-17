from flask import render_template
# from ..models import EditableHTML
from flask import request

from . import main



@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/about')
def about():
    # editable_html_obj = EditableHTML.get_editable_html('about')
    # return render_template('main/about.html', editable_html_obj=editable_html_obj)
    return render_template('main/about.html')


@main.route('/expense/add')
def add_expense():
    # TODO: Handle adding expense to the database
    TPP_TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJsdmY0MzJAbWFpbC5ydS1UUFBUT0tFTi0xIiwiZXhwIjoxNTUwMzQ5NDMzfQ.qWrII0mXMew4o8VMG8LJz0P7UgVIF57ofo7jI5KJa3NPYVvnam2_3KKC6ONFPUW73wQlLCb2pV6N64rUrGxttw"
    USER_TOKEN = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJERU1PRUUsaWJzVXNlcjEiLCJleHAiOjE1NTAzOTI1MzV9.hW2Ov9k3vHsLN-f_l09hajRXNUsRtx-x5MnpCvf1Z0bpnI9Rx7Kget-4x0vx7al2JJ1ADK1gqdTle6pwdtbTvw'



    return render_template('main/expense/add.html', **locals())


@main.route('/expense/confirm')
def confirm_expense():
    # TODO: Handle adding expense to the database
    


    return render_template('main/expense/confirm.html', **locals())