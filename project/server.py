import asyncio
import random
import tornado.ioloop
import tornado.web
from tornado.web import url

from db import db
from key_gen import KeyGenThread, key_queue


class MainHandler(tornado.web.RequestHandler):

    def initialize(self, db):
        self.db = db

    async def get(self):
        username = self.get_argument("user")
        print(f'connected user {username}')
        response = {'task_id': random.randint(50, 60), 'user': '', 'key': ''}
        task = asyncio.create_task(self.fetch_user(username))
        user = await task
        if user.public_key:
            response.update({'user': user.username, 'key': user.public_key})
            self.write(response)
        else:
            response.update(
                {'user': user.username, 'key': 'you have not a key, i\'d like to help you, but i can\'t :('})
            self.write(response)
            # KeyGenThread(key_queue=key_queue, length=128)
            # key_set = await self.set_public_key(user)
            # if key_set:
            #     print('awaited for key!')
            #     user = await self.fetch_user(username)
            #     response.update({'user': user.username, 'key': user.public_key})
            #     self.write(response)

    async def fetch_user(self, username):
        '''
        Fetch user from db
        :param username:
        :return: User instance
        '''
        print(f'in fetch_user {username}')
        await asyncio.sleep(random.randint(0, 3))
        user = db.get_user(username=username)
        print(f'in fetch_user is ready {user}')
        return user

    async def set_public_key(self, user):
        '''
        sets pubkey for user and commit
        :param user: User instance
        :return: True
        '''
        public_key = await self.key_gen(username=user.username)
        user.public_key = f'{user.username} - {public_key}'
        print(f'key for {user.username} is set')
        self.db.session.commit()
        return True

    async def key_gen(self, username):
        '''
        gets generated key from queue
        :param username:
        :return: key
        '''
        return key_queue.get()


def make_app():
    return tornado.web.Application([
        url(r"/", MainHandler, dict(db=db), name='main'),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    key_queue.join()
