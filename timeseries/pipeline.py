# -*- coding: utf-8 -*-
# @PydevCodeAnalysisIgnore
from goerr import Err
from dataswim import ds
from chartflo.widgets.number import Number
from chartflo.widgets.datatable import DataTable
from chartflo.altair import save_altair_chart


class Generator(Err):
    
    def __init__(self):
        self.trace_errs = True
    
    def timeline(self, slug):
        ds.status("Generating timeline for " + slug)
        ds.defaults()
        if slug == "rawdata":
            ds.engine = "altair"
            ds.width(700)
            ds.height(200)
            ds.size(15)
            ds.date("Date")
            ds.aenc("color", "Value")
            ds.chart("Date:T", "Value:Q")
            c = ds.point_()
            ds.raencs()
            c1 = ds.hline_()
            c2 = c1 + c
            save_altair_chart(c2, slug + "_timeline", "timeseries")
        elif slug in ["month", "week"]:
            ds.opt("tools", ["hover"])
            if slug == "week":
                ds.opt("xrotation", 45)
            ds.date("Date", precision="D")
            ds.chart("Date", "Value")
            if slug == "week":
                c = ds.line_point_()
            else:
                c = ds.bar_()
            ds.ropts()
            ds.color("green")
            c1 = ds.hline_("Value")
            c2 = c * c1
            ds.stack(slug + "_timeline", c2, "Timeline")   
        else:
            ds.engine = "altair"
            ds.width(750)
            ds.height(200)
            ds.zero_nan("Value")
            ds.drop_nan("Value")
            ds.chart("Date:T", "Value:Q")
            c = ds.line_num_()
            ds.color("green")
            ds.style("opacity", 0.7)
            c2 = ds.hline_()
            c3 = c2 + c
            save_altair_chart(c3, slug + "_timeline", "timeseries")
        ds.engine = "bokeh"
        
    def difftimeline(self, slug):
        ds.status("Generating diff timeline for " + slug)
        ds.defaults()
        if slug == "day":
            ds.engine = 'altair'
            ds.raencs()
            ds.width(750)
            ds.height(200)
            ds.diffm("Value")
            ds.fill_nan(0, "Diff")
            ds.timestamps("Date")
            ds.lreg("Timestamps", "Diff")
            ds.color("green")
            ds.chart("Date:T", "Regression:Q")
            ds.style("opacity", 0.7)
            c = ds.line_()
            ds.chart("Date:T", "Diff:Q")
            ds.rcolor()
            ds.rstyle("opacity")
            c2 = ds.bar_()
            ds.styles(dict(align="center", baseline="bottom"))
            ds.aenc("text", "Diff:Q")
            ds.color("grey")
            c3 = ds.text_()
            c4 = c + c2 + c3
            save_altair_chart(c4, slug + "_difftimeline", "timeseries")
        else:
            ds.diffm("Value")
            ds.fill_nan(0, "Diff")
            ds.chart("Date", "Diff")
            ds.opts(dict(tools=["hover"]))
            if slug != "month":
                ds.opt("xrotation", 45)
            ds.date("Date", precision="D")
            ds.height(350)
            c = ds.bar_()
            ds.color("green")
            ds.style('date_format', "%Y-%m-%d")
            c1 = ds.lreg_()
            c2 = c * c1
            ds.stack(slug + "_difftimeline", c2, "Diff timeline")
        ds.defaults()
        ds.engine = "bokeh"
        
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
            if slug != "rawdata":
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
        ds.df = df
        
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
