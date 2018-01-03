import sqlite3

class DBHelper:

	def __init__(self, dbname="schedule.sqlite"):
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname)
	
	# build table called schedule, one column named time
	def setup(self):
		tblstmt = "CREATE TABLE IF NOT EXISTS schedule (description text, time text)"
		schedidx = "CREATE INDEX IF NOT EXISTS scheduleIndex ON schedule (description ASC)"		
		timeidx = "CREATE INDEX IF NOT EXISTS timeIndex ON schedule (time ASC)"
		self.conn.execute(tblstmt)
		self.conn.execute(schedidx)
		self.conn.execute(timeidx)	
		self.conn.commit()

	# takes the sched_text and insert into table
	def add_sched(self, sched_text, time):
		stmt = "INSERT INTO schedule (description, time) VALUES (?, ?)"
		args = (sched_text, time)
		self.conn.execute(stmt, args)
		self.conn.commit()

	def delete_sched(self, sched_text):
		stmt = "DELETE FROM schedule WHERE description = (?)"
		args = (sched_text, )
		self.conn.execute(stmt, args)
		self.conn.commit()

	# returns a list of all the items in our database
	def get_sched(self):
		stmt = "SELECT description FROM schedule"
		return [x[0] for x in self.conn.execute(stmt)]



