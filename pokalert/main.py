import requests     # To interface with the servers
import re           # To process sever data
import struct       # To interface with the servers (?)
import json         # To load pokemon data
import argparse     # To interface with the servers
import pokemon_pb2  # Unofficial Pokemon Go API
import time         # Time delays to throttle server queries
import os           # To refresh the screen between displaying nearby pokemon

from google.protobuf.internal import encoder # Location handling

from datetime import datetime, timedelta # To display himan-readable time stamps

from geopy.geocoders import GoogleV3 # Location handling
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from s2sphere import *

import pokedex # Home-made pokemon storage database
import alert # Home-made notification sender for interesting pokemon

def encode(cellid):
    output = []
    encoder._VarintEncoder()(output.append, cellid)
    return ''.join(output)

def getNeighbors():
    origin = CellId.from_lat_lng(LatLng.from_degrees(FLOAT_LAT, FLOAT_LONG)).parent(15)
    walk = [origin.id()]
    # 10 before and 10 after
    next = origin.next()
    prev = origin.prev()
    for i in range(10):
        walk.append(prev.id())
        walk.append(next.id())
        next = next.next()
        prev = prev.prev()
    return walk



API_URL = 'https://pgorelease.nianticlabs.com/plfe/rpc'
LOGIN_URL = 'https://sso.pokemon.com/sso/login?service=https%3A%2F%2Fsso.pokemon.com%2Fsso%2Foauth2.0%2FcallbackAuthorize'
LOGIN_OAUTH = 'https://sso.pokemon.com/sso/oauth2.0/accessToken'

SESSION = requests.session()
SESSION.headers.update({'User-Agent': 'Niantic App'})
SESSION.verify = False

DEBUG = False
COORDS_LATITUDE = 0
COORDS_LONGITUDE = 0
COORDS_ALTITUDE = 0
FLOAT_LAT = 0
FLOAT_LONG = 0

origin = '' # Starting location

def f2i(float):
  return struct.unpack('<Q', struct.pack('<d', float))[0]

def f2h(float):
  return hex(struct.unpack('<Q', struct.pack('<d', float))[0])

def h2f(hex):
  return struct.unpack('<d', struct.pack('<Q', int(hex,16)))[0]

def set_location(location_name):
    geolocator = GoogleV3()
    loc = geolocator.geocode(location_name)

    print('[!] Your given location: {}'.format(loc.address.encode('utf-8')))
    print('[!] lat/long/alt: {} {} {}'.format(loc.latitude, loc.longitude, loc.altitude))
    set_location_coords(loc.latitude, loc.longitude, loc.altitude)

def set_location_coords(lat, long, alt):
    global COORDS_LATITUDE, COORDS_LONGITUDE, COORDS_ALTITUDE
    global FLOAT_LAT, FLOAT_LONG
    FLOAT_LAT = lat
    FLOAT_LONG = long
    COORDS_LATITUDE = f2i(lat) # 0x4042bd7c00000000 # f2i(lat)
    COORDS_LONGITUDE = f2i(long) # 0xc05e8aae40000000 #f2i(long)
    COORDS_ALTITUDE = f2i(alt)

def get_location_coords():
    return (COORDS_LATITUDE, COORDS_LONGITUDE, COORDS_ALTITUDE)

def api_req(api_endpoint, access_token, *mehs, **kw):
    try:
        p_req = pokemon_pb2.RequestEnvelop()
        p_req.rpc_id = 1469378659230941192

        p_req.unknown1 = 2

        p_req.latitude, p_req.longitude, p_req.altitude = get_location_coords()

        p_req.unknown12 = 989

        if 'useauth' not in kw or not kw['useauth']:
            p_req.auth.provider = 'ptc'
            p_req.auth.token.contents = access_token
            p_req.auth.token.unknown13 = 14
        else:
            p_req.unknown11.unknown71 = kw['useauth'].unknown71
            p_req.unknown11.unknown72 = kw['useauth'].unknown72
            p_req.unknown11.unknown73 = kw['useauth'].unknown73

        for meh in mehs:
            p_req.MergeFrom(meh)

        protobuf = p_req.SerializeToString()

        r = SESSION.post(api_endpoint, data=protobuf, verify=False)

        p_ret = pokemon_pb2.ResponseEnvelop()
        p_ret.ParseFromString(r.content)

        if DEBUG:
            print("REQUEST:")
            print(p_req)
            print("Response:")
            print(p_ret)
            print("\n\n")

        # Waiut 2 sec between searches to avoid rate limits
        time.sleep(2)
        return p_ret
    except Exception, e:
        if DEBUG:
            print(e)
        return None

def get_profile(access_token, api, useauth, *reqq):
    req = pokemon_pb2.RequestEnvelop()

    req1 = req.requests.add()
    req1.type = 2
    if len(reqq) >= 1:
        req1.MergeFrom(reqq[0])

    req2 = req.requests.add()
    req2.type = 126
    if len(reqq) >= 2:
        req2.MergeFrom(reqq[1])

    req3 = req.requests.add()
    req3.type = 4
    if len(reqq) >= 3:
        req3.MergeFrom(reqq[2])

    req4 = req.requests.add()
    req4.type = 129
    if len(reqq) >= 4:
        req4.MergeFrom(reqq[3])

    req5 = req.requests.add()
    req5.type = 5
    if len(reqq) >= 5:
        req5.MergeFrom(reqq[4])

    return api_req(api, access_token, req, useauth = useauth)

def get_api_endpoint(access_token, api = API_URL):
    p_ret = get_profile(access_token, api, None)
    try:
        return ('https://%s/rpc' % p_ret.api_url)
    except:
        return None


def login_ptc(username, password):
    print('[!] login for: {}'.format(username))
    head = {'User-Agent': 'niantic'}
    r = SESSION.get(LOGIN_URL, headers=head)
    jdata = json.loads(r.content)
    data = {
        'lt': jdata['lt'],
        'execution': jdata['execution'],
        '_eventId': 'submit',
        'username': username,
        'password': password,
    }
    r1 = SESSION.post(LOGIN_URL, data=data, headers=head)

    ticket = None
    try:
        ticket = re.sub('.*ticket=', '', r1.history[0].headers['Location'])
    except e:
        if DEBUG:
            print(r1.json()['errors'][0])
        return None

    data1 = {
        'client_id': 'mobile-app_pokemon-go',
        'redirect_uri': 'https://www.nianticlabs.com/pokemongo/error',
        'client_secret': 'w8ScCUXJQc6kXKw8FiOhd8Fixzht18Dq3PEVkUCP5ZPxtgyWsbTvWHFLm2wNY0JR',
        'grant_type': 'refresh_token',
        'code': ticket,
    }
    r2 = SESSION.post(LOGIN_OAUTH, data=data1)
    access_token = re.sub('&expires.*', '', r2.content)
    access_token = re.sub('.*access_token=', '', access_token)
    return access_token

def heartbeat(api_endpoint, access_token, response):
    m4 = pokemon_pb2.RequestEnvelop.Requests()
    m = pokemon_pb2.RequestEnvelop.MessageSingleInt()
    m.f1 = int(time.time() * 1000)
    m4.message = m.SerializeToString()
    m5 = pokemon_pb2.RequestEnvelop.Requests()
    m = pokemon_pb2.RequestEnvelop.MessageSingleString()
    m.bytes = "05daf51635c82611d1aac95c0b051d3ec088a930"
    m5.message = m.SerializeToString()

    walk = sorted(getNeighbors())

    m1 = pokemon_pb2.RequestEnvelop.Requests()
    m1.type = 106
    m = pokemon_pb2.RequestEnvelop.MessageQuad()
    m.f1 = ''.join(map(encode, walk))
    m.f2 = "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"
    m.lat = COORDS_LATITUDE
    m.long = COORDS_LONGITUDE
    m1.message = m.SerializeToString()
    response = get_profile(
        access_token,
        api_endpoint,
        response.unknown7,
        m1,
        pokemon_pb2.RequestEnvelop.Requests(),
        m4,
        pokemon_pb2.RequestEnvelop.Requests(),
        m5)
    payload = response.payload[0]
    heartbeat = pokemon_pb2.ResponseEnvelop.HeartbeatPayload()
    heartbeat.ParseFromString(payload)
    return heartbeat

def loadSettings():
    # Load default settinsg from settings.txt if no arguments are provided on program start
    settingFile = open("settings.txt", "r")
    settings = settingFile.readlines()

    username, password, location = "", "", ""
    for item in settings:
        item = item.split("=")
        if item[0] == "username":
            username = item[1].strip()
        elif item[0] == "password":
            password = item[1].strip()
        elif item[0] == "location":
            location = item[1]
        else:
            print " [!] Error: Unrecognised setting '{0}' in settings.txt.".format(item[0])

    return username, password, location

def getExpTime(seconds):
    now = datetime.now()
    seconds = timedelta(seconds=seconds)
    return now + seconds

def main():
    defaultSettings = loadSettings()

    pokemons = json.load(open('pokemon.json'))
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="PTC Username", required=False, default=defaultSettings[0])
    parser.add_argument("-p", "--password", help="PTC Password", required=False, default=defaultSettings[1])
    parser.add_argument("-l", "--location", help="Location", required=False, default="'{0}'".format(defaultSettings[2]))
    parser.add_argument("-d", "--debug", help="Debug Mode", action='store_true')
    parser.set_defaults(DEBUG=False)
    args = parser.parse_args()

    if args.debug:
        global DEBUG
        DEBUG = True
        print('[!] DEBUG mode on')

    set_location(args.location)

    access_token = login_ptc(args.username, args.password)
    if access_token is None:
        print('[-] Wrong username/password')
        return
    print('[+] RPC Session Token: {} ...'.format(access_token[:25]))

    api_endpoint = get_api_endpoint(access_token)
    if api_endpoint is None:
        print('[-] RPC server offline')
        return
    print('[+] Received API endpoint: {}'.format(api_endpoint))

    response = get_profile(access_token, api_endpoint, None)
    if response is not None:
        print('[+] Login successful')

        payload = response.payload[0]
        profile = pokemon_pb2.ResponseEnvelop.ProfilePayload()
        profile.ParseFromString(payload)
        print('[+] Username: {}'.format(profile.profile.username))

        creation_time = datetime.fromtimestamp(int(profile.profile.creation_time)/1000)
        print('[+] You started playing Pokemon Go on: {}'.format(
            creation_time.strftime('%Y-%m-%d %H:%M:%S'),
        ))

        for curr in profile.profile.currency:
            print('[+] {}: {}'.format(curr.type, curr.amount))
    else:
        print('[-] No response from server.')

    global origin
    origin = LatLng.from_degrees(FLOAT_LAT, FLOAT_LONG)
    while True:
        original_lat = FLOAT_LAT
        original_long = FLOAT_LONG
        parent = CellId.from_lat_lng(LatLng.from_degrees(FLOAT_LAT, FLOAT_LONG)).parent(15)

        try:
            h = heartbeat(api_endpoint, access_token, response)
            hs = [h]
            seen = set([])
            for child in parent.children():
                latlng = LatLng.from_point(Cell(child).get_center())
                set_location_coords(latlng.lat().degrees, latlng.lng().degrees, 0)
                hs.append(heartbeat(api_endpoint, access_token, response))
            set_location_coords(original_lat, original_long, 0)

            visible = []

            for hh in hs:
                for cell in hh.cells:
                    for wild in cell.WildPokemon:
                        hash = wild.SpawnPointId + ':' + str(wild.pokemon.PokemonId)
                        if (hash not in seen):
                            visible.append(wild)
                            seen.add(hash)

            print('')
            for cell in h.cells:
                if cell.NearbyPokemon:
                    other = LatLng.from_point(Cell(CellId(cell.S2CellId)).get_center())
                    diff = other - origin
                    # print(diff)
                    difflat = diff.lat().degrees
                    difflng = diff.lng().degrees
                    direction = (('N' if difflat >= 0 else 'S') if abs(difflat) > 1e-4 else '')  + (('E' if difflng >= 0 else 'W') if abs(difflng) > 1e-4 else '')

                    # THIS ORIGINALLY PRINTED A SUMMARY OF THE CLOSEST POKEMON
                    #print("Within one step of %s (%sm %s from you):" % (other, int(origin.get_distance(other).radians * 6366468.241830914), direction))
                    #for poke in cell.NearbyPokemon:
                        #print('    (%s) %s' % (poke.PokedexNumber, pokemons[poke.PokedexNumber - 1]['Name']))
            
           

            print('')
            # THIS IS THE BIT THAT LISTS ALL NEARBY POKEMON

            
            for poke in visible:
                other = LatLng.from_degrees(poke.Latitude, poke.Longitude)
                diff = other - origin
                difflat = diff.lat().degrees
                difflng = diff.lng().degrees
                direction = (('N' if difflat >= 0 else 'S') if abs(difflat) > 1e-4 else '')  + (('E' if difflng >= 0 else 'W') if abs(difflng) > 1e-4 else '')

                ### USEFUL INFO ON LOCATED POKEMON
                num = poke.pokemon.PokemonId # pokedex number
                name = pokemons[poke.pokemon.PokemonId - 1]['Name'] # Fetched from pokemon.json file
                distance = int(origin.get_distance(other).radians * 6366468.241830914) # Distance from start lat/lon in meters
                timeToExp = poke.TimeTillHiddenMs / 1000 / 60 # minutes until disappearance
                expiresAt = getExpTime(poke.TimeTillHiddenMs / 1000).strftime("%y-%m-%d %H:%M") # Time of disappearance
                lat = poke.Latitude # Current pokemon location
                lon = poke.Longitude # Current pokemon location

                #################
                # MY STUFF
                if timeToExp > 0: # Only display pokemon that haven't expired since they were found
                    
                    pokedex.updateLocal(num, name, lat, lon, expiresAt)
                    pokedex.saveHistory(num, name, lat, lon, args.location)
                    alert.alert(num, name, lat, lon, expiresAt) # Send alert of interesting pokemon appearance

            displayPokemon()

            print('')
            walk = getNeighbors()
            next = LatLng.from_point(Cell(CellId(walk[2])).get_center())
            set_location_coords(next.lat().degrees, next.lng().degrees, 0)
        except Exception, e:
            print " [!] An error occurred:\n     {0}".format(e)

def displayPokemon():
    "Using the data stored in pokedex.db in the main() loop above, display nearby pokemon"
    
    # Clear screen between refreshes of the nearby pokemon list
    try:            
        os.system("cls") # Windows
    except:
        os.system("clear") # Linux

    # I've se the program to display a table of pokemon on screen
    print "\nPokedex\tName\t\tDist\tDir\tExpires"
    print "-------\t----\t\t----\t---\t-------"

    # This bit is just to make sure the long names fit nicely in the displayed output

    nearby = [] # This list will hold formatted data for all nearby pokemon
    localList = pokedex.getLocal()
    # localList format:
    #[ (NUM, NAME, LAT, LNG, EXPIRY), (NUM, NAME, LAT, LNG, EXPIRY), etc. ]
    for pokemon in localList:
        # Get basic info from database:
        num = int(pokemon[0])
        name = pokemon[1]
        latitude = float(pokemon[2])
        longitude = float(pokemon[3])
        expiry = pokemon[4]

        # Calculate distance & direction from coordinates:
        other = LatLng.from_degrees(latitude, longitude)
        diff = other - origin
        difflat = diff.lat().degrees
        difflng = diff.lng().degrees
        
        direction = (('N' if difflat >= 0 else 'S') if abs(difflat) > 1e-4 else '')  + (('E' if difflng >= 0 else 'W') if abs(difflng) > 1e-4 else '')
        distance = int(origin.get_distance(other).radians * 6366468.241830914) # Distance from start lat/lon in meters

        nearby.append([num, name, latitude, longitude, distance, direction, expiry])

    # Sort the nearby list by distance
    nearby.sort(key=lambda x: x[4])
    for pokemon in nearby:
        num = pokemon[0]
        name = pokemon[1]
        lat = pokemon[2]
        lng = pokemon[3]
        distance = pokemon[4]
        direction = pokemon[5]
        expiry = pokemon[6]

        if len(name)<8:
            extraTab = "\t"
        else:
            extraTab = ""

        print "{num}\t{name}\t{extraTab}{distance}m\t{direction}\t{expiry}".format(num=num, name=name, extraTab=extraTab, distance=distance, direction=direction, expiry=expiry)

if __name__ == '__main__':
    main()
