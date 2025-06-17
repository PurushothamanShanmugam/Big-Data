import pymysql

# Replace these with your actual MySQL credentials
host = "127.0.0.1"
user = "root"
password = "0000"

# Connect to MySQL server (without selecting a database first)
connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = connection.cursor()

# Create database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS music_streaming_1;")
print("Database 'music_streaming_1' created or already exists.")

# Select DataBase 
cursor.execute("use music_streaming_1 ")
print("Database 'music_streaming_1' has been selected")

# Create Users table 
cursor.execute(f"CREATE TABLE IF NOT EXISTS Users (user_id INTEGER PRIMARY KEY,name VARCHAR(100) NOT NULL,email VARCHAR(100) NOT NULL UNIQUE);")
print("Users Table has been created")

# Create Songs table 
cursor.execute(f"CREATE TABLE IF NOT EXISTS Songs (song_id INTEGER PRIMARY KEY,title VARCHAR(100) NOT NULL,artist VARCHAR(100) NOT NULL,genre VARCHAR(100));")
print("Songs Table has been created")

# Create Listens table
cursor.execute(f"CREATE TABLE IF NOT EXISTS Listens (listen_id INTEGER PRIMARY KEY,user_id INTEGER NOT NULL,song_id INTEGER NOT NULL,rating FLOAT,listen_time TIMESTAMP,FOREIGN KEY (user_id) REFERENCES Users(user_id),FOREIGN KEY (song_id) REFERENCES Songs(song_id));")
print("Listens Table has been created")

# Create Recommendations table
cursor.execute(f"CREATE TABLE IF NOT EXISTS Recommendations (recommendation_id INTEGER NOT NULL,recommendation_time TIMESTAMP,user_id INTEGER NOT NULL,song_id INTEGER NOT NULL,FOREIGN KEY (user_id) REFERENCES Users(user_id),FOREIGN KEY (song_id) REFERENCES Songs(song_id));")
print("Recommendations Table has been created")


#Data Insertion on user table
cursor.execute(f"INSERT INTO Users (user_id, name, email)VALUES(1, 'Mickey', 'mickey@example.com'),(2, 'Minnie', 'minnie@example.com'),(3, 'Daffy', 'daffy@example.com'),(4, 'Pluto', 'pluto@example.com');")
print("User Data has been inserted")
connection.commit()

#Data Interpretation on User Table
usertabe = cursor.execute(f"select * from Users;")
users = cursor.fetchall()
print("Users Table Data:")
for row in users:
    print(row)


# Insert sample songs from Taylor Swift, Ed Sheeran, Beatles
cursor.execute(f"INSERT INTO Songs (song_id, title, artist, genre)VALUES(1, 'Evermore', 'Taylor Swift', 'Pop'),(2, 'Willow', 'Taylor Swift', 'Pop'),(3, 'Shape of You', 'Ed Sheeran', 'Rock'),(4, 'Photograph', 'Ed Sheeran', 'Rock'),(5, 'Shivers', 'Ed Sheeran', 'Rock'),(6, 'Yesterday', 'Beatles', 'Classic'),(7, 'Yellow Submarine', 'Beatles', 'Classic'),(8, 'Hey Jude', 'Beatles', 'Classic'),(9, 'Bad Blood', 'Taylor Swift', 'Rock'),(10, 'DJ Mix', 'DJ', NULL);")
print("Songs Data has been inserted")
connection.commit()

#Data Interpretation on SongsTable
Songstabe = cursor.execute(f"select * from Songs;")
Songs = cursor.fetchall()
print("Songs Table Data:")
for row in Songs:
    print(row)


# Insert sample listens
cursor.execute(f"INSERT INTO Listens (listen_id, user_id, song_id, rating, listen_time)VALUES(1, 1, 1, 4.5, '2024-08-30 14:35:00'),(2, 1, 2, 4.2, NULL),(3, 1, 6, 3.9, '2024-08-29 10:15:00'),(4, 2, 2, 4.7, NULL),(5, 2, 7, 4.6, '2024-08-28 09:20:00'),(6, 2, 8, 3.9, '2024-08-27 16:45:00'),(7, 3, 1, 2.9, NULL),(8, 3, 2, 4.9, '2024-08-26 12:30:00'),(9, 3, 6, NULL, NULL);")
print("Listens Data has been inserted")
connection.commit()

#Data Interpretation on Listens Table
Listenstabe = cursor.execute(f"select * from Listens;")
Listeners = cursor.fetchall()
print("Listeners Table Data:")
for row in Listeners:
    print(row)

#Classic Songs Filtration
ClassicSongs=cursor.execute(f"SELECT Songs.title, Songs.artist FROM Songs WHERE Songs.genre= 'Classic'")
ClassicalSongs=cursor.fetchall()
print("Classic Songs table data ")
for row in ClassicalSongs:
    print(row)


#Find titles and artists if songs in Classic Genre with titles starting like Ye...
ClassicSongs2 = cursor.execute(f"SELECT Songs.title, Songs.artist FROM Songs WHERE Songs.genre= 'Classic' AND  Songs.title LIKE 'Ye%';")
ClassicalSongs2=cursor.fetchall()
print("Classic Songs table data which starts with ye..")
for row in ClassicalSongs2:
    print(row)


#List all the genres in the Songs table
qry_genres=cursor.execute(f"SELECT genre from Songs;")
qry_genres=cursor.fetchall()
print("Classic Songs table data which starts with ye..")
for row in qry_genres:
    print(row)


#Find the unique genres from the Songs table
qry_distinct=cursor.execute(f"SELECT DISTINCT genre FROM Songs;")
qry_distincts=cursor.fetchall()
print("Unique Genre table data which starts with ye..")
for row in qry_distincts:
    print(row)


#Find the number of songs by Taylor Swift in different genres
qry_taylor_count=cursor.execute(f"SELECT artist, genre,count(*) as num_songs FROM Songs WHERE Songs.artist='Taylor Swift' GROUP BY artist, genre;")
qry_taylor_counts=cursor.fetchall()
print("Count of songs by Taylor Swift in different genres")
for row in qry_taylor_counts:
    print(row)

#Find the number of songs by all artists in different genres
qry_artist_count=cursor.execute(f"SELECT artist, genre,count(*) as num_songs FROM Songs GROUP BY artist, genre;")
qry_artist_counts=cursor.fetchall()
print("Count of songs by artist in different genres")
for row in qry_artist_counts:
    print(row)

#Count of songs by artist in different genres
qry_large_table = cursor.execute(f"SELECT * FROM Songs LEFT JOIN Listens ON Songs.song_id=Listens.song_id LEFT JOIN Users ON Listens.user_id=Users.user_id;")
qry_artist_counts=cursor.fetchall()
print("Count of songs by artist in different genres")
for row in qry_artist_counts:
    print(row)


#Find the Highly Rates Songs. Consider Rating above 4.6 as highly rated
qry_rating_songs=cursor.execute(f"SELECT Songs.song_id, Songs.title, Songs.artist, Listens.rating FROM Songs JOIN Listens ON Songs.song_id = Listens.song_id WHERE Listens.rating > 4.6")
qry_rating_songs_counts=cursor.fetchall()
print("Highly Rates Songs")
for row in qry_rating_songs_counts:
    print(row)

#Find tha average rating of every song
qry_avg_songs=cursor.execute(f"SELECT Songs.song_id, Songs.title, Songs.artist, AVG(Listens.rating) FROM Songs JOIN Listens ON Songs.song_id = Listens.song_id GROUP BY Songs.song_id, Songs.title, Songs.artist")
qry_avg_songs_counts=cursor.fetchall()
print("Average rating Songs")
for row in qry_avg_songs_counts:
    print(row)


# #Find the popular songs by counting the listens
# qry_pop_songs = cursor.execute(""""
# SELECT Songs.song_id, Songs.title, Songs.artist, count(Listens.song_id)
# FROM Songs
# JOIN Listens
# ON Songs.song_id=Listens.song_id
# GROUP BY Songs.title, Songs.artist
# ORDER BY COUNT(Listens.song_id) DESC;""")
# qry_pop_songs_counts=cursor.fetchall()
# print("The Popular songs")
# for row in qry_pop_songs_counts:
#     print(row)


#Find songs by Ed Sheeran and Taylor Swift
qry_edtaylor= cursor.execute(f"SELECT title, artist FROM Songs WHERE artist IN ('Ed Sheeran', 'Taylor Swift');")
qry_pop_songs_counts=cursor.fetchall()
print("Ed Sheeran songs")
for row in qry_pop_songs_counts:
    print(row)


#Find songs from both pop and rock genres
qry_popandrock = cursor.execute(f"SELECT title, artist FROM Songs WHERE genre='Pop' UNION SELECT title, artist FROM Songs WHERE genre='Rock';")
qry_popandrock_counts=cursor.fetchall()
print("Songs both pop and rock genres")
for row in qry_popandrock_counts:
    print(row)


#Find songs listened to by user_id 1
qry_listen_usr=cursor.execute(f"SELECT title, artist FROM Songs WHERE song_id IN (SELECT song_id FROM Listens WHERE Listens.listen_time IS NULL);")
qry_listen_usr_counts=cursor.fetchall()
print("Songs listened to by user_id 1")
for row in qry_listen_usr_counts:
    print(row)


#Computing the recommendations
#Find the song pairs which are shared across > 1 user
qry_sharing=cursor.execute(""" WITH song_similarity AS (
SELECT u1.song_id as song1, u2.song_id as song2, COUNT(*) AS common_users
FROM LISTENS u1
JOIN LISTENS u2
ON u1.user_id=u2.user_id
AND u1.song_id != u2.song_id
GROUP BY u1.song_id, u2.song_id
HAVING COUNT(*)>1
),

recs AS (
  SELECT user_id, song2 as song_id
  FROM song_similarity
  JOIN Listens as L
  ON L.song_id = song_similarity.song1
  WHERE song_similarity.song2 NOT IN
  (SELECT song_id FROM Listens as temp where temp.user_id=L.user_id)
)
select * from recs;""")
qry_sharing_counts=cursor.fetchall()
print("Song pairs which are shared across more than 1 user")
for row in qry_sharing_counts:
    print(row)




# Question 1
# Insert the above into the recommendations table
# Answer here below 
#Data Insertion into Reccomandation table 
qry_reccomanding=cursor.execute(""" INSERT INTO Recommendations (recommendation_id, recommendation_time, user_id, song_id)
SELECT 
  ROW_NUMBER() OVER () AS recommendation_id,
  CURRENT_TIMESTAMP() AS recommendation_time,
  user_id,
  song_id
FROM (
  WITH song_similarity AS (
    SELECT u1.song_id AS song1, u2.song_id AS song2, COUNT(*) AS common_users
    FROM Listens u1
    JOIN Listens u2 ON u1.user_id = u2.user_id AND u1.song_id != u2.song_id
    GROUP BY u1.song_id, u2.song_id
    HAVING COUNT(*) > 1
  ),
  recs AS (
    SELECT L.user_id, song2 AS song_id
    FROM song_similarity
    JOIN Listens AS L ON L.song_id = song_similarity.song1
    WHERE song_similarity.song2 NOT IN (
      SELECT song_id FROM Listens AS temp WHERE temp.user_id = L.user_id
    )
  )
  SELECT * FROM recs
) AS recommendations;
""")
reccomand=cursor.execute(f"SELECT * FROM Recommendations;")
qry_reccomanding=cursor.fetchall()
print("Here the Data Insertions For recommanda ion table ")
for row in qry_reccomanding:
    print(row)



# Question 2
# Generate the recommendaions for Minnie
# Answer is below here 
# Generate the recommendations for Minnie
qry_reccomanding_for_Minnie=cursor.execute(""" WITH song_similarity AS (
  SELECT u1.song_id AS song1, u2.song_id AS song2, COUNT(*) AS common_users
  FROM Listens u1
  JOIN Listens u2 ON u1.user_id = u2.user_id AND u1.song_id != u2.song_id
  GROUP BY u1.song_id, u2.song_id
  HAVING COUNT(*) > 1
),
recs AS (
  SELECT L.user_id, song2 AS song_id
  FROM song_similarity
  JOIN Listens AS L ON L.song_id = song_similarity.song1
  WHERE song_similarity.song2 NOT IN (
    SELECT song_id FROM Listens AS temp WHERE temp.user_id = L.user_id
  )
)
SELECT s.title, s.artist
FROM recs
JOIN Songs s ON recs.song_id = s.song_id
WHERE recs.user_id = 2;

""")

qry_reccomanding_for_Minnie_count=cursor.fetchall()
print("Reccomanding for Minnie")
for row in qry_reccomanding_for_Minnie_count:
    print(row)


# Question 3
# Re-do the generation of recommendations now on the basis of listen time
# Answes is below here
# Re-do the generation of recommendations now on the basis of listen time
reccommandations_based_on_listening_time =cursor.execute(""" WITH recent_listens AS (
  SELECT * 
  FROM Listens 
  WHERE listen_time IS NOT NULL
),
song_similarity AS (
  SELECT l1.song_id AS song1, l2.song_id AS song2, COUNT(*) AS common_users
  FROM recent_listens l1
  JOIN recent_listens l2 ON l1.user_id = l2.user_id AND l1.song_id != l2.song_id
  GROUP BY l1.song_id, l2.song_id
  HAVING COUNT(*) > 1
),
recs AS (
  SELECT rl.user_id, song2 AS song_id
  FROM song_similarity
  JOIN recent_listens rl ON rl.song_id = song_similarity.song1
  WHERE song_similarity.song2 NOT IN (
    SELECT song_id FROM Listens WHERE user_id = rl.user_id
  )
)
SELECT DISTINCT s.title, s.artist, r.user_id
FROM recs r
JOIN Songs s ON r.song_id = s.song_id
WHERE r.user_id = 2;

""")

reccommandations_based_on_listening_time_count=cursor.fetchall()
print("reccommandations_based_on_listening_time_count is here below")
for row in reccommandations_based_on_listening_time_count:
    print(row)

connection.commit()
connection.close()
 


