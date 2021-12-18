from flask import Flask,render_template,request
import battleship
import random
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('172.16.0.14', 27017)
db = client.ship_database
coordinates = db.coordinates

def RandomShip():
       global ship_X, ship_Y, won
       ship_X = random.randint(0,3)
       ship_Y = random.randint(0,4)
       won = False
       print("ship_X: ",ship_X)
       print("ship_Y: ",ship_Y)

@app.route('/')
def root():
       global grid

       RandomShip()
       grid = battleship.initialiseGrid()
       coordinates.drop()

       return render_template('main.html', grid=grid)
 
@app.route('/calculate', methods = ["POST"])
def calculate():
       global won       

       data = request.form
       X = data['X']
       Y = data['Y']
       if battleship.validateRow(X) and battleship.validateCol(Y):

              xy_coord = { "X": X, "Y": Y }
              coordinates.insert_one(xy_coord)
              won = battleship.checkResult(grid, int(X), int(Y), ship_X, ship_Y, won)

              if won:
                     return render_template('won.html', coords=list(coordinates.find({})))

       return render_template('main.html', grid=grid) 
       
         
if __name__ == '__main__':
       app.run(port = 6789, debug = True)
