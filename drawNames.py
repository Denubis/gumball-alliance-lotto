#!/usr/bin/env python3

from quickstart import *
import random
import sqlite3
import datetime
NAMES_TO_DRAW = 4


#print(getMembers())

def drawMember(currentMembers, alliancecon):
	drawList = list(currentMembers.keys())

	# removes all prior people in this run
	try:
		for member in alliancecon.execute("SELECT member FROM lotto where inCurrentRun = 'True'"):
			#print(member[0])
			drawList = list(filter(lambda a: a != member[0], drawList))
		random.shuffle(drawList)
		alliancecon.execute("REPLACE INTO MEMBER (member) VALUES (?)", [drawList[0]])
		alliancecon.execute("REPLACE INTO lotto (member) VALUES (?)", [drawList[0]])
		print("Drew {} from {} possible remaining.".format(drawList[0], len(drawList)))
		return ("{}".format(drawList[0]))
	except IndexError:
		# Nothing left in drawList

		alliancecon.execute("UPDATE lotto set inCurrentRun = null;")
		print("All members have had a go. Resetting lotto.")
		return drawMember(currentMembers, alliancecon)
def main():
	with sqlite3.connect("alliance.db") as alliancecon:
		try:
			print("Last run {}.".format(alliancecon.execute("SELECT max(wondate) from lotto").fetchone()))
		except:
			alliancecon.executescript("""
	CREATE TABLE member (
	Member TEXT Primary Key
	);

	CREATE TABLE lotto (
	wondate DATE DEFAULT CURRENT_TIMESTAMP,
	member TEXT REFERENCES member,
	inCurrentRun BOOL DEFAULT 'True',
	PRIMARY KEY (member, wondate)
	);
				""")

	currentMembers = getMembers()
	todaysDraw = []

	for i in range(0, NAMES_TO_DRAW):
		#print(i)
		todaysDraw.append(drawMember(currentMembers, alliancecon))

	
	


	print("Friendship lotto winners for {0} are {1}.".format(
							datetime.date.today(), 
							', '.join(todaysDraw)))
							
	alliancecon.commit()

if __name__ == '__main__':
	main()