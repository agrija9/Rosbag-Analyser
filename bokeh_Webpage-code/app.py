from flask import Flask, render_template
	
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid, Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
import random
# from bokeh.charts import Bar
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource

app = Flask(__name__)

@app.route("/<int:bars_count>/")
def chart(bars_count):
	if bars_count <= 0:
		bars_count = 1

	data = {"days": [], "bugs": [], "costs": []}
	for i in range(1, bars_count + 1):
		data["days"].append(i) # testing
		data["bugs"].append(random.randint(1,100))
		data["costs"].append(random.uniform(1.00, 1000.00))

	hover = create_hover_tool()

	# this creates the barchart
	plot = create_bar_chart(data, "Bugs found per day", "days", "bugs", hover)
	
	# check this
	script, div = components(plot)

	return render_template("chart.html", bars_count=bars_count,
							the_div=div, the_script=script)

def create_hover_tool():
	"""
	Generates HTML for the Bokeh's data tool on our graph.
	"""

	hover_html= """
	 <div>
	 	<span class = "hover-tooltip">$x</span>
	 </div>
	 <div>
	 	<span class = "hover-tooltip">@bugs bugs </span>
	 </div>
	 <div>
       <span class="hover-tooltip">$@costs{0.00}</span>
     </div>
	 """
	return HoverTool(tooltips=hover_html)

def create_bar_chart(data, title, x_name, y_name, hover_tool=None, 
					 width=1200, height=300):
	"""
	Creates a barchart
	"""
	source = ColumnDataSource(data)

	# xdr = FactorRange(factors=data[x_name])
	xdr = FactorRange(factors=[str(x) for x in data[x_name]])
	ydr = Range1d(start=0,end=max(data[y_name])*1.5)

	tools = []
	if hover_tool:
		tools = [hover_tool,]

	plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width, 
				  plot_height=height, h_symmetry=False, v_symmetry=False, 
				  min_border=0, toolbar_location="above", tools=tools, 
				  outline_line_color="#666666") # responsive=True

	glyph = VBar(x=x_name, top=y_name, bottom=0, width=0.8, fill_color="#e12127")

	plot.add_glyph(source, glyph)

	xaxis = LinearAxis()
	yaxis = LinearAxis()

	plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
	plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
	plot.toolbar.logo = None
	plot.min_border_top = 0
	plot.xgrid.grid_line_color = None
	plot.ygrid.grid_line_color = "#999999"
	plot.yaxis.axis_label = "Bugs found"
	plot.ygrid.grid_line_alpha = 0.1
	plot.xaxis.axis_label = "Days after app deployment"
	plot.xaxis.major_label_orientation = 1

	return plot


if __name__ == "__main__":
	app.run(debug=True)

