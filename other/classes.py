from sql import SQL
from datetime import datetime

class User:

    def __init__(self, id, username, visibility, services):
        self.id = id
        self.username = username
        self.visibility = True if visibility else False
        self.services = services.split(', ')

    def getPosts(self, sql: SQL):
        # gets all posts for people this user is following
        allPosts = []
        for userid in self.getFollowing(sql):
            allPosts += User.getUserPosts(sql, userid)
        allPosts.sort(key = lambda x: x.dt)
        return allPosts
        
    def getFollowing(self, sql: SQL) -> list[int]:
        result = sql.read(f'SELECT * FROM friends WHERE user = {self.id}')
        return [i[2] for i in result]

    def post(self, sql: SQL, songid: int, caption: str):
        sql.createPost(self.id, datetime.now().replace(microsecond=0), songid, caption)

    def follow(self, sql: SQL, userid: int):
        sql.follow(self.id, userid)

    @staticmethod
    def getUserPosts(sql: SQL, id: int):
        result = sql.read(f'SELECT * FROM posts WHERE userid = {id}')
        return [Post.create(i) for i in result]

    @staticmethod
    def create(t):
        return User(t[0], t[1], t[3], t[4])

    @staticmethod
    def get(sql: SQL, id=None):
        if id:
            return sql.getUserById(id)
        return None

class Post:
    
    def __init__(self, id: int, userid: int, dt: str, songid: int, caption: str, likes: int):
        self.id = id
        self.userid = userid
        self.dt = datetime.fromisoformat(dt)
        self.songid = songid
        self.caption = caption
        self.likes = likes

    def toString(self, sql):
        return f"""Post from {User.get(sql, id=self.userid)[1]} at {self.dt}:
Song: {sql.getSong(self.songid)[1]}
Caption: {self.caption}
Likes: {self.likes}
        """

    @staticmethod
    def create(t):
        return Post(*t)
