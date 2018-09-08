# Django Chartflo demo

Demo for [Django Chartflo](https://github.com/synw/django-chartflo)

### Install

Clone the repository. Install the dependencies: 

   ```bash
   pip install --no-cache-dir dataset
   pip install -r requirements.txt
   ```

### Initialize

Make migrations and run them to create the Sqlite database.

Run the management command to generate data and initialize the dashboards:

   ```bash
   python3 manage.py init_timeseries
   ``` 
   
Go to `/dashboards/timeseries/`

### Management commands

Extra management commands are available: `delete_timeseries` to delete all the data and `pipeline` to run the
data pipeline to regenerate the charts.

### Regenerate the charts on save

Optional: run the Django rq worker: `python manage.py rqworker default`: the charts and widgets will be regenerated on 
every save of the Serie model
