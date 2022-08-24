from app import create_app

######################################################
# create the flask app
# 
# The app will be run by the 'flask run' command.
#
# Flask picks up entrypoint.py because it is
# configured in .flaskenv
######################################################
app = create_app()

