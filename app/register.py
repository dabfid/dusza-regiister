from flask import Blueprint, render_template

register = Blueprint("register", __name__, static_folder="static", template_folder="templates")

@register', methods=['GET', 'POST'])
def register():
    return "a"

@register.route('/edit')
def edit():
    return "a"

@register.route('/modify')
def modify():
    return "a"
