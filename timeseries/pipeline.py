# -*- coding: utf-8 -*-
# @PydevCodeAnalysisIgnore
from goerr import Err
from dataswim import ds
from chartflo.widgets.number import Number
from chartflo.widgets.datatable import DataTable


class Generator(Err):
    
    def __init__(self):
        self.trace_errs = True
    
    def timeline(self, slug):
        ds.status("Generating timeline for " + slug)
        ds.chart("Date", "Value")
        ds.date("Date", format="%d %B")
        if slug == "month":
            c = ds.bar_()
        elif slug == "rawdata":
            c = ds.point_()
        else:
            c = ds.area_()
        c1 = ds.hline_("Value")
        c2 = c * c1
        ds.stack(slug + "_timeline", c2, "Timeline")
        
    def difftimeline(self, slug):
        ds.status("Generating diff timeline for " + slug)
        ds.df = ds.df.rename(columns={"Value": "Start Value"})
        ds.diffm("Start Value")
        ds.drop_nan("Diff")
        ds.height(350)
        ds.opts(dict(tools=["hover"]))
        ds.chart("Date", "Diff")
        # ds.date("Date", format="%Y-%m-%d")
        c = ds.bar_()
        ds.color("green")
        c1 = ds.lreg_()
        c2 = c * c1
        ds.stack(slug + "_difftimeline", c2, "Diff timeline")
        ds.height(250)
        ds.color("#30A2DA")
        ds.opts(dict(tools=[]))
        
    def seaborn_charts(self, slug):
        ds.status("Generating Seaborn charts for " + slug)
        ds.timestamps("Date")
        ds.engine = "seaborn"
        ds.chart("Timestamps", "Value")
        ds.width(8)
        ds.height(5)
        c = ds.density_()
        ds.stack(slug + "_density", c)
        ds.chart("Value", "Timestamps")
        c = ds.distrib_()
        ds.stack(slug + "_distrib", c)
        ds.chart("Timestamps", "Value")
        ds.to_int("Timestamps")
        ds.width(12)
        ds.height(6) 
        c = ds.dlinear_()
        ds.stack(slug + "_linear", c)
        ds.width(900)
        ds.height(250)
        ds.engine = "bokeh" 
        
    def datatable(self, slug):
        ds.status("Generating datatable for " + slug)
        dt = DataTable()
        if slug != "rawdata":
            ds.date("Date", format="%Y-%m-%d")
            ds.zero_nan("Number")
            ds.drop_nan("Number")
            ds.to_int("Number")
            ds.df = ds.df[['Date', 'Value', "Number"]]   
        dt.create(slug, "timeseries", df=ds.df, search=False)
        
    def mean_num(self, slug, title, icon="arrows-alt-h", sparkline=None):
        ds.status("Generating mean number for " + slug)
        mean = int(round(ds.df.Value.mean()))
        n = Number()
        if icon is not None:
            html = n.simple(mean, title, icon=icon, spdata=sparkline)
        else:
            html = n.simple(mean, title, spdata=sparkline)
        n.write("mean_" + slug, "timeseries", html)
        
    def min_num(self, slug, title, icon="long-arrow-alt-down", sparkline=None):
        ds.status("Generating min number for " + slug)
        mean = int(round(ds.df.Value.min()))
        n = Number()
        if icon is not None:
            html = n.simple(mean, title, icon=icon, spdata=sparkline)
        else:
            html = n.simple(mean, title, spdata=sparkline)
        n.write("min_" + slug, "timeseries", html)
        
    def max_num(self, slug, title, icon="long-arrow-alt-up", sparkline=None):
        ds.status("Generating max number for " + slug)
        mean = int(round(ds.df.Value.max()))
        n = Number()
        if icon is not None:
            html = n.simple(mean, title, icon=icon, spdata=sparkline)
        else:
            html = n.simple(mean, title, spdata=sparkline)
        n.write("max_" + slug, "timeseries", html)
        
    def charts_tables(self, slug, df):
        try:
            self.timeline(slug)
        except Exception as e:
            self.fatal(e)
        ds.df = df
        try:
            if slug != "raw_data":
                self.difftimeline(slug)
        except Exception as e:
            self.fatal(e)
        ds.df = df
        try:
            self.datatable(slug)
        except Exception as e:
            self.fatal(e)
        ds.df = df
        try:
            self.seaborn_charts(slug)
        except Exception as e:
            self.fatal(e)
        
    def nums(self, slug, df):
        sparkline = None
        try:
            if slug == "week" or slug == "month":
                sparkline = list(ds.df.Value)
            self.mean_num(slug, "Mean", sparkline=sparkline)
        except Exception as e:
            self.fatal(e)
        sparkline = None
        ds.df = df
        try:
            self.max_num(slug, "Max", sparkline=sparkline)
        except Exception as e:
            self.fatal(e)
        ds.df = df
        try:
            self.min_num(slug, "Min", sparkline=sparkline)
        except Exception as e:
            self.fatal(e)
        ds.df = df
        
    def raw_nums(self, slug, title):
        try:
            icon = None
            if slug == "raw":
                icon = "arrows-alt-h"
            sparkline = None
            if slug == "raw_week" or slug == "raw_month":
                sparkline = list(ds.df.Value)
            self.mean_num(slug, title, icon=icon, sparkline=sparkline)
        except Exception as e:
            self.fatal(e)

    
def generate(query):
    ds.start("Running data pipeline")
    ds.width(900)
    ds.height(250)
    ds.opts(dict(xrotation=45))
    ds.report_path = "templates/dashboards/timeseries/charts"
    ds.static_path = "static/dashboards/timeseries"
    ds.df = query.to_dataframe()
    ds.df = ds.df.rename(columns={"value": "Value", "date": "Date"})
    ds.drop("id")
    ds.dateindex("Date")
    ds.backup()
    gen = Generator()
    # raw data
    gen.charts_tables("rawdata", ds.df.copy())
    gen.raw_nums("raw", "Mean")
    # day
    ds.restore()
    ds.rsum("1D")
    df = ds.df.copy()
    gen.charts_tables("day", df)
    gen.raw_nums("raw_day", "Day")
    gen.nums("day", df)
    # week
    ds.restore()
    ds.rsum("1W")
    df = ds.df.copy()
    gen.charts_tables("week", df)
    gen.raw_nums("raw_week", "Week")
    gen.nums("week", df)
    # day
    ds.restore()
    ds.rsum("1M")
    df = ds.df.copy()
    gen.charts_tables("month", df)
    gen.raw_nums("raw_month", "Month")
    gen.nums("month", df)
    ds.status("Saving to files")
    ds.to_files()
    ds.end("Data pipeline completed")
    ds.trace()
