# Brexit001.py
# Geographical Data Aalysis
# (voting, demographics, etc.)


# import libraries
import sqlite3


# FUNCTION: drop database
def drop(curs):
    drp = raw_input('Reset database to empty (Y/N): ')
    if drp.lower() == 'n' or len(drp) < 0 : pass
    elif drp.lower() == 'y' :
        curs.executescript('''
            DROP TABLE IF EXISTS Region;
            DROP TABLE IF EXISTS Area;
            DROP TABLE IF EXISTS Vote;
            DROP TABLE IF EXISTS RefScore
            ''')
        conn.commit()


# FUNCTION: create database
def create(curs):
    curs.executescript('''
    CREATE TABLE IF NOT EXISTS Region (
        id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        code        TEXT UNIQUE,
        region      TEXT UNIQUE
    );
    
    CREATE TABLE IF NOT EXISTS Area (
        id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        code        TEXT UNIQUE,
        area        TEXT UNIQUE,
        Regn_id     INTEGER,
        electorate  INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS Vote (
        id          INTEGER NOT NULL PRIMARY KEY UNIQUE,
        Area_id     INTEGER UNIQUE,
        expected    INTEGER,
        actual      INTEGER,
        votes       INTEGER,
        validvotes  INTEGER,
        remain      INTEGER,
        leave       INTEGER,
        spoilt      INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS RefScore (
        Vote_id     INTEGER NOT NULL PRIMARY KEY UNIQUE,
        turnout     FLOAT,
        valid       FLOAT,
        spoilers    FLOAT,
        winner      TEXT,
        winpc       FLOAT,
        leavepc     FLOAT,
        remainpc    FLOAT,
        brexiteers  FLOAT
    );
    
    ''')
    conn.commit()


# MAIN PROGRAM
# create SQL database DB01 RawData
conn = sqlite3.connect('DBHome.db')
curs = conn.cursor()

# drop/create database
drop(curs)
create(curs)

# establish data file
fname = raw_input('1 = SNIP, 2 = FULL, Q = quit: ')
if fname.lower() == 'q' :
    quit()
elif fname == '1' :
    fname = 'EUrefdataSNIP.csv' 
elif fname == '2' :
    fname = 'EUrefdataFULL.csv'     
elif len(fname) == 0 :
    fname = 'EUrefdataSNIP.csv'       # default on enter
    
# open file or return error message
try:
    fhand = open(fname)
except:
    print 'Filename not found:', fname
    quit()

# add regions, areas and vote data to database
regions = list() ; areas = list()
for line in fhand :
    line = line.rstrip().split(',')
    
    # extract data
    vote_id = line[0][1:len(line[0])-1]
    regcode = line[1][1:len(line[1])-1]
    region = line[2][1:len(line[2])-1]
    areacode = line[3][1:len(line[3])-1]
    area = line[4][1:len(line[4])-1]
    electorate = line[5][1:len(line[5])-1]
    expected = line[6][1:len(line[6])-1]
    actual = line[7][1:len(line[7])-1]
    votes = line[9][1:len(line[9])-1]
    valid = line[10][1:len(line[10])-1]
    remain = line[11][1:len(line[11])-1]
    leave = line[12][1:len(line[12])-1]
    spoilt = line[13][1:len(line[13])-1]
    
    # updating regions
    if not region in regions and not region == 'Region' :
        regions.append(region)
        curs.execute('''INSERT OR IGNORE INTO Region (code, region) 
            VALUES ( ?, ? )''', ( regcode, region, ) )
        curs.execute('SELECT id FROM Region WHERE region = ? ', (region, ))
        regn_id = curs.fetchone()[0]
        #print regn_id, regcode, region
    
    # updating areas
    if not area == 'Area' :
        areas.append(area)
        electorate = int(electorate)
        curs.execute('''INSERT OR IGNORE INTO Area (code, area, Regn_id, electorate) 
            VALUES ( ?, ?, ?, ? )''', ( areacode, area, regn_id, electorate) )
        curs.execute('SELECT id FROM Area WHERE area = ? ', (area, ))
        area_id = curs.fetchone()[0]
        #print regn_id, area_id, areacode, area, electorate
    
    # updating vote data
    if not vote_id == 'id' :
        print vote_id
        curs.execute('''INSERT OR IGNORE INTO Vote (id, Area_id, expected,
            actual, votes, validvotes, remain, leave, spoilt) 
            VALUES ( ?, ?, ?, ?, ?, ?, ?,?, ? )''',( int(vote_id), area_id, int(expected),
            int(actual), int(votes), int(valid), int(remain), int(leave), int(spoilt)) )
    
    conn.commit()

curs.close()
quit()


########################################

# DATA FILE (INDEX)
# Download CSV from Electoral Commission
# http://www.electoralcommission.org.uk/find-information-by-subject/elections-and-referendums/upcoming-elections-and-referendums/eu-referendum/electorate-and-count-information

#  0 id
#  1 Region_Code
#  2 Region
#  3 Area_Code
#  4 Area
#  5 Electorate
#  6 ExpectedBallots
#  7 VerifiedBallotPapers
#  8 Pct_Turnout
#  9 Votes_Cast
# 10 Valid_Votes
# 11 Remain
# 12 Leave
# 13 Rejected_Ballots
# 14 No_official_mark
# 15 Voting_for_both_answers
# 16 Writing_or_mark
# 17 Unmarked_or_void
# 18 Pct_Remain
# 19 Pct_Leave
# 20 Pct_Rejected

