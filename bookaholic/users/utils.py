import os
import secrets
from PIL import Image
from flask import url_for,current_app
from flask_mail import Message
from bookaholic import mail

def save_picture(picture_form):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture_form.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output = (125,125)
    i = Image.open(picture_form)
    i.thumbnail(output)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
        sender = 'mohamedraees2@gmail.com',
        recipients=[user.email])
    msg.body = f'''To reset your passwowrd visit following link:
{url_for('users.reset_token',token = token, _external = True)}
if you DID NOT MAKE THIS REQUEST IGNORE
    '''
    mail.send(msg)