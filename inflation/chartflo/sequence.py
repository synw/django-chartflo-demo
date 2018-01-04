# -*- coding: utf-8 -*-
from django.template.defaultfilters import slugify


class Sequence():

    def process(self, name, cf):
        slug = slugify(name)
        cf.diff("Value")
        cf.df = cf.df.iloc[1:]
        cf.sequence(slug, "inflation", "Date", "Diff",
                    style="width:46px;padding:0.2em 0.6em 0.6em 0.2em",
                    trs=dict(high=3.0, low=0))

    def year(self, year, cf):
        cf.restore()
        inds = cf.split_("index")
        cf = inds["Global index"]
        if year == 1997:
            cf.daterange("Date", str(year)+"-01-01", "+", months=12)
            cf.sort("Date")
            cf.diff("Value")
            cf.df = cf.df.iloc[1:-1]
        else:
            cf.daterange("Date", str(year-1)+"-12-01", "+", months=13)
            cf.sort("Date")
            cf.diff("Value")
            cf.df = cf.df.iloc[1:-1]
        style = "width:81px;height:55px;padding:0.5em 0.6em 0.6em 0.2em"
        cf.sequence("years/"+str(year), "inflation", "Month", "Diff",
                    style=style,
                    trs=dict(high=0.5, low=0))


seq = Sequence()
