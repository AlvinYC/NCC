from bokeh.models.widgets import Panel, Tabs
from bokeh.io import output_file, show
from bokeh.plotting import figure

output_file("xx_tab_multiple.html")


# method 1 : generate tab one by one / no for loop architecture
'''
p1 = figure(plot_width=300, plot_height=300)
p1.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
tab1 = Panel(child=p1, title="circle")

p2 = figure(plot_width=300, plot_height=300)
p2.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=3, color="navy", alpha=0.5)
tab2 = Panel(child=p2, title="line")

tabs = Tabs(tabs=[ tab1, tab2 ])
'''
# method 2 : for loop to generate tab
tab_name_list = ['circle','line1','line2']
tab_oo_list = []
for tab_name in tab_name_list:

    p1 = figure(plot_width=300, plot_height=300)
    if tab_name == 'circle':
        p1.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
    elif tab_name == 'line1':
        p1.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=3, color="navy", alpha=0.5)
    else:
        p1.line([1, 2, 3, 4, 5], [2, 4, 6, 4, 2], line_width=3, color="navy", alpha=0.5)
    tab1 = Panel(child=p1, title=tab_name)
    tab_oo_list.append(tab1)

tabs = Tabs(tabs=tab_oo_list)
show(tabs)