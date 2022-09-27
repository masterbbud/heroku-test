import sqlite3

services = ['spotify', 'itunes', 'youtube', 'tidal', 'amazonMusic', 'soundcloud', 'youtubeMusic']

class SQL:

    def __init__(self, path):
        self.connection = self.connect(path)
        
    def connect(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Exception as e:
            print(f"The error '{e}' occurred")

        return connection

    def write(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Exception as e:
            print(f"The error '{e}' occurred")

    def read(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"The error '{e}' occurred")

    def songExists(self, id):
        query = f'SELECT 1 from songs where id = {id}'
        if self.read(query):
            return True
        return False

    def userExists(self, username):
        query = f"SELECT 1 from users where username = '{username}'"
        if self.read(query):
            return True
        return False
    
    def connectionStatus(self, user1, user2):
        # Returns a (bool, bool) where [0] is true if user1 follows user2 and [1] is true if user2 follows user1
        query = f"SELECT * from friends where (user1 = '{user1}' and user2 = '{user2}') or (user1 = '{user2}' and user2 = '{user1}')"
        connection = self.read(query)
        if connection:
            c = connection[0]
            if c[1] == user1:
                return (c[3] == 1, c[4] == 1)
            else:
                return (c[4] == 1, c[3] == 1)
        return (False, False)

    # get methods should have checks to make sure you got something and return properly
    
    def getSong(self, id):
        query = f'SELECT * from songs where id = {id}'
        return self.read(query)[0]

    def getUser(self, username):
        query = f"SELECT * from users where username = '{username}'"
        return self.read(query)[0]

    def getUserById(self, id):
        query = f'SELECT * from users where id = {id}'
        return self.read(query)[0]

    def addSong(self, id, title, artist, image, links):
        def format(id, title, artist, image, links):
            servicesString = ''
            for i in services:
                servicesString += "', '"
                servicesString += links.get(i, '')
            return f"({id}, '{title}', '{artist}', '{image}{servicesString}')"
        query = f"""
        INSERT INTO
        songs (id, title, artist, image, spotify, itunes, youtube, tidal, amazonMusic, soundcloud, youtubeMusic)
        VALUES
        {format(id, title, artist, image, links)};
        """
        self.write(query)

    def createUser(self, username, password, visibility):
        query = f"""
        INSERT INTO
        users (username, password, visibility, services)
        VALUES
        ('{username}', '{password}', {visibility}, '');
        """
        self.write(query)

    def createPost(self, user, datetime, songid, caption):
        print(datetime.isoformat())
        query = f"""
        INSERT INTO
        posts (userid, datetime, songid, caption, likes)
        VALUES
        ({user}, '{datetime.isoformat()}', {songid}, '{caption}', 0);
        """
        self.write(query)

    def follow(self, user, following):
        # user1 following user2
        # check if they are already followed
        query = f"""
        INSERT INTO
        friends (user, following)
        VALUES
        ({user}, {following});
        """
        self.write(query)

    def unfollow(self, user, following):
        # user1 unfollowing user2
        query = f"""
        DELETE FROM
        friends WHERE user = {user} and following = {following};
        """
        self.write(query)

    def initSongs(self):
        query = """
        CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY UNIQUE,
        title TEXT NOT NULL,
        artist TEXT,
        image TEXT,
        spotify TEXT,
        itunes TEXT,
        youtube TEXT,
        tidal TEXT,
        amazonMusic TEXT,
        soundcloud TEXT,
        youtubeMusic TEXT
        );
        """
        self.write(query)
    
    def initUsers(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        visibility BOOLEAN,
        services TEXT
        );
        """
        self.write(query)

    def initPosts(self):
        query = """
        CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid INTEGER,
        datetime TEXT,
        songid INTEGER,
        caption TEXT,
        likes INTEGER
        );
        """
        self.write(query)

    def initFriends(self):
        query = """
        CREATE TABLE IF NOT EXISTS friends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user INTEGER NOT NULL,
        following INTEGER NOT NULL
        );
        """
        self.write(query)
