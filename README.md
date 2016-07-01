# brexit
Geographical Data Aalysis (voting, demographics, etc.) with Python

Raw data was downloaded from Electoral Commission website in CSV format; data file format as follows (header plus example data row):

"id","Region\_Code","Region","Area\_Code","Area","Electorate","ExpectedBallots","VerifiedBallotPapers","Pct\_Turnout","Votes\_Cast","Valid\_Votes","Remain","Leave","Rejected\_Ballots","No\_official\_mark","Voting\_for\_both\_answers","Writing\_or\_mark","Unmarked\_or\_void","Pct\_Remain","Pct\_Leave","Pct_Rejected"
 "100","E00000000","xxxxxxx","E00000000","xxxxxxxxxxxx","123456","12345","12345","00.00","12345","12345","12345","12345","00","0","00","0","00","00.00","00.00","0.00"
 
 Program reads raw data from file, updates to SQLite database, scores the voting and updates to database, then calcultes/displays various top ten results by voting area.


