"""
http://localhost:5000/84.2/56.8/7329.4
"""

from flask import Flask, url_for,render_template
import xlrd
import sklearn.ensemble
from sklearn.ensemble import RandomForestRegressor
app = Flask(__name__)
path = "/home/ubuntu/Q_Den.xlsx"
book = xlrd.open_workbook(path)
# print book.nsheets
first_sheet = book.sheet_by_index(0)
num_rows = first_sheet.nrows - 1
curr_row = 0
x=[]
y=[]
y_echo=[]
y_total_cooling_hours=[]
y_DX=[]
y_EERH=[]
y_consumption_saving=[]
y_peak_demand_saving=[]
y_water_consumption=[]
while curr_row < num_rows:
    curr_row += 1
    # row = first_sheet.row(curr_row)
    dry_bulb = first_sheet.cell(curr_row,1).value
    wet_bulb = first_sheet.cell(curr_row,3).value
    elevation = first_sheet.cell(curr_row,4).value
    echo = first_sheet.cell(curr_row,5).value
    total_cooling_hours = first_sheet.cell(curr_row,6).value
    DX = first_sheet.cell(curr_row,7).value
    EERH = first_sheet.cell(curr_row,8).value
    consumption_saving = first_sheet.cell(curr_row,9).value
    peak_demand_saving = first_sheet.cell(curr_row,10).value
    water_consumption = first_sheet.cell(curr_row,11).value


    xval = [dry_bulb,wet_bulb,elevation]

    y.append(echo)
    y_echo.append(echo)
    y_total_cooling_hours.append(total_cooling_hours)
    y_DX.append(DX)
    y_EERH.append(EERH)
    y_consumption_saving.append(consumption_saving)
    y_peak_demand_saving.append(peak_demand_saving)
    y_water_consumption.append(water_consumption)

    x.append(xval)



#4410 5 0.0103430437039, 960 7 0.010346165879
clf_echo = RandomForestRegressor(n_estimators=4410, max_depth=5)
clf_echo.fit(x, y_echo)

#960 19 977462.760895,
clf_total_cooling_hours = RandomForestRegressor(n_estimators=960, max_depth=19)
clf_total_cooling_hours.fit(x, y_total_cooling_hours)

clf_DX = RandomForestRegressor(n_estimators=1610, max_depth=8)
clf_DX.fit(x, y_DX)

#4810 4 7.19106692097   4810 4 7.19106692097    2760 18 7.3044908132
clf_EERH = RandomForestRegressor(n_estimators=4810, max_depth=4)
clf_EERH.fit(x, y_EERH)

#1910 18 0.00471920801752, 4610 7 0.00476592327654
clf_consumption_saving = RandomForestRegressor(n_estimators=1910, max_depth=18)
clf_consumption_saving.fit(x, y_consumption_saving)

#done 10 7 0.00819795771602, 510 14 0.00930511952647, 610 11 0.00936973055891,
clf_peak_demand_saving = RandomForestRegressor(n_estimators=510, max_depth=14)
clf_peak_demand_saving.fit(x, y_peak_demand_saving)

#2610 11 0.0129692552313
clf_water_consumption = RandomForestRegressor(n_estimators=2610, max_depth=11)
clf_water_consumption.fit(x, y_water_consumption)






# num_rows = 5
@app.route('/')
def api_root():
	return 'Welcome'

#routing the qden page to the User Interface 

@app.route('/qden')
def api_qden():
	return render_template('index.html')

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

# @app.route('/articles/<articleid>')
# def api_article(articleid):
#     return 'You are reading ' + articleid

@app.route('/articles/<articleid1>/<articleid2>/<articleid3>')
def api_article(articleid1):
    return "hii"
    # return 'You are reading ' + articleid1
@app.route('/<dry_bulb>/<wet_bulb>/<elevation>')
def user(dry_bulb,wet_bulb,elevation):
    # num_rows = 5
    # path = "/Users/prasanna/mrjob/Q_Den.xlsx"
    # book = xlrd.open_workbook(path)
    # # print book.nsheets
    # first_sheet = book.sheet_by_index(0)
    # num_rows = first_sheet.nrows - 1
    X_test = [dry_bulb,wet_bulb,elevation]
    preds_echo =  clf_echo.predict(X_test)
    preds_total_cooling_hours =  clf_total_cooling_hours.predict(X_test)
    preds_DX =  clf_DX.predict(X_test)
    preds_EERH =  clf_EERH.predict(X_test)
    preds_consumption_saving =  clf_consumption_saving.predict(X_test)
    preds_peak_demand_saving =  clf_peak_demand_saving.predict(X_test)
    preds_water_consumption =  clf_water_consumption.predict(X_test)
    obj = {"echo":preds_echo[0],"total cooling hours":preds_total_cooling_hours[0],"DX":preds_DX[0],"EERH":preds_EERH[0],
           "consumption saving":preds_consumption_saving[0],"demand saving":preds_peak_demand_saving[0],
           "water consumption":preds_water_consumption[0]
           }
    return str(obj) + "," + str(dry_bulb) + "," +  str(wet_bulb) + "," + str(elevation) + "," + str(preds_echo[0])  +  "," +  str(preds_total_cooling_hours[0]) + ","  +  str(preds_DX[0])  + "," +  str(preds_EERH[0]) + ","  +  str(preds_consumption_saving[0])  + ","  +  str(preds_peak_demand_saving[0]) + "," + str(preds_water_consumption[0])
    # return "usercalled"+str(dry_bulb)+str(wet_bulb)+str(elevation)
if __name__ == '__main__':
    app.run()
