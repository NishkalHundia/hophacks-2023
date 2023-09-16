import psycopg2
import datetime

conn = psycopg2.connect("dbname=hophacks user=ubuntu password=0912")

cur = conn.cursor()

# name = "ananya"
# firstname = "Ananya"
# lastname = "idk"
# height = 150
# weight = 50
# dateofbirth = datetime.date(2005, 2, 11)
# nurseid = 1
# doctrid = 1
# password = "password4"

# cur.execute("INSERT INTO usertable (name) VALUES (%s)", (name,))
# conn.commit()
# userid = cur.execute("SELECT user_id FROM usertable WHERE name = %s", (name,))
# userid = cur.fetchone()
# print(userid)

# cur.execute("INSERT INTO userinfo (user_id, firstname, lastname, height, weight, dateofbirth) VALUES (%s, %s, %s, %s, %s, %s)", (userid, firstname, lastname, height, weight, dateofbirth))
# conn.commit()
# result = cur.execute("SELECT * FROM userinfo WHERE user_id = %s", (userid,))
# result = cur.fetchone()
# print(result)

# cur.execute("INSERT INTO userstaff (user_id, nurse_id, doctor_id) VALUES (%s, %s, %s)", (userid, nurseid, doctrid))
# conn.commit()
# result = cur.execute("SELECT * FROM userstaff WHERE user_id = %s", (userid,))
# result = cur.fetchone()
# print(result)

# cur.execute("INSERT INTO userpwd (user_id, pwd) VALUES (%s, %s)", (userid, password))
# conn.commit()
# result = cur.execute("SELECT * FROM userpwd WHERE user_id = %s", (userid,))
# result = cur.fetchone()
# print(result)

# userid = cur.execute("SELECT user_id FROM usertable")
# userid = cur.fetchall()
# print(userid)
# result = cur.execute("SELECT * FROM userinfo")
# result = cur.fetchall()
# print(result)
# result = cur.execute("SELECT * FROM userstaff")
# result = cur.fetchall()
# print(result)
# result = cur.execute("SELECT * FROM userpwd")
# result = cur.fetchall()
# print(result)

#------------------------

userid = 4
nurseid = 1
rxcuid = 161
drugname = "Paracetamol"
drugdescription = "never gonna let you down"
drugpower = 100
drugdays = "daily"
drugtime = "every 6 hours"
expiry = datetime.date(2023, 7, 2)

cur.execute("INSERT INTO prescription (user_id, nurse_id, rxcuid, drug_name, drug_description, drug_power, drug_days, drug_time, expiry) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (userid, nurseid, rxcuid, drugname, drugdescription, drugpower, drugdays, drugtime, expiry))
conn.commit()
result = cur.execute("SELECT * FROM prescription WHERE user_id = %s", (userid,))
result = cur.fetchone()
print(result)

cur.close()
conn.close()
