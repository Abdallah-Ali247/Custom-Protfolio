web: gunicorn architect_portfolio.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn architect_portfolio.wsgi
