import sqlite3
import datetime

dbFile = 'pokedex.db'
db = ''
c =''

def initialise():
	"Initialise database"
	global dbFile, c, db
	db = sqlite3.connect(dbFile) # Open database (create it if it does't exist)
	db.text_factory = str
	c = db.cursor()

def updateLocal(pokeNum, pokeName, lat, lng, expiry):
	"Save details of nearby pokemon & remove expired ones from the database"
	if c == '':
		initialise()

	# expiry format:
	# yyyy-mm-dd HH:MM:SS

	# Save new appearances
	c.execute("INSERT OR IGNORE INTO localPkmn (NUM, NAME, LAT, LNG, EXPIRY) VALUES (?, ?, ?, ?, ?)", (pokeNum, pokeName, lat, lng, expiry))

	currentTime = datetime.datetime.now().strftime("%y-%m-%d %H:%M")
	#c.execute("SELECT NAME, EXPIRY FROM local WHERE EXPIRY<?", (currentTime,))
	#expired = c.fetchall()
	#print "Remioving expired pokemon:"
	#for pokemon in expired:
	#	print "\t {0}".format(pokemon)

	# Delete expired pokemon
	c.execute("DELETE FROM localPkmn WHERE EXPIRY<?", (currentTime,))
	db.commit()

def getLocal():
	"Returns a list of all non-epired pokemon in the area."

	if c == '':
		initialise()

	c.execute("SELECT NUM, NAME, LAT, LNG, EXPIRY FROM localPkmn ORDER BY NAME ASC")
	nearby = c.fetchall()

	# nearby format:
	#[ (NUM, NAME, LAT, LNG, EXPIRY), (NUM, NAME, LAT, LNG, EXPIRY), etc. ]

	return nearby

def saveHistory(pokeNum, pokeName, lat, lng, location):
	"Add to the record of all pokemon's appearances & locations"
	if c == '':
		initialise()

	currentTime = datetime.datetime.now().strftime("%y-%m-%d %H:%M")

	c.execute("INSERT INTO history (NUM, NAME, LAT, LNG, LOCATION, APPEARANCE) VALUES (?, ?, ?, ?, ?, ?)", (pokeNum, pokeName, lat, lng, location.upper(), currentTime))
	db.commit

	# Store new pokemon appearance in the pokedex
	add(pokeNum, pokeName, lat, lng, location)

def add(pokeNum, pokeName, lat, lng, location):
	"Add newly discovered pokemon to Pokedex. Returns true if this is the first encounter"
	try:
		c.execute("INSERT INTO pokedex (NUM, NAME, LAT, LNG, COUNT, LOCATION) VALUES (?, ?, ?, ?, ?)", (pokeNum, pokeName, lat, lng, 1, location.upper()))
		result = True
	except:
		# The above will fail for pokemon already in the database
		# because the NUM field is set to be unique
		c.execute("UPDATE pokedex SET COUNT=COUNT+1 WHERE NUM=?", (pokeNum,))
		result = False
	db.commit
	return result

if __name__ == "__main__":
	getLocal()

