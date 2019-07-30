# -*- coding: utf-8 -*-

from wechatpy.enterprise import WeChatClient
from wechatpy.exceptions import WeChatClientException


class WeiXin:
    def __init__(self, corp='', agent=0, secret=''):
        self.corp = corp
        self.agent = agent
        self.secret = secret

    def connect(self):
        self.client = WeChatClient(self.corp, self.secret)

    def sendImage(self, user, img, party_ids='', tag_ids='', safe=0):
        media = self.client.media.upload('image', img)
        self.client.message.send_image(self.agent, user, media['media_id'], party_ids, tag_ids,
                                       safe)

    def sendText(self, user, content, party_ids='', tag_ids='', safe=0):
        self.client.message.send_text(self.agent, user, content, party_ids, tag_ids, safe)

    def sendArticles(self, user, dat, party_ids='', tag_ids=''):
        self.client.message.send_articles(self.agent, user, dat, party_ids, tag_ids)

    def getDepartment(self):
        return self.client.department.get()

    def createDepartment(self, dat):
        return self.client.department.create(dat.get('name'), dat.get('parent_id'),
                                             dat.get('order'), dat.get('id'))

    def updateDepartment(self, dat):
        return self.client.department.update(dat.get('id'), dat.get('name'), dat.get('parent_id'),
                                             dat.get('order'))

    def deleteDepartment(self, id):
        return self.client.department.delete(id)

    def listUser(self, dat):
        return self.client.user.list(dat.get('department_id'), dat.get('fetch_child'),
                                     dat.get('status'))

    def getUser(self, user_id):
        return self.client.user.get(user_id)

    def createUser(self, dat):
        return self.client.user.create(dat.get('user_id'), dat.get('name'), dat.get('department'),
                                       dat.get('position'),
                                       dat.get('mobile'), dat.get('gender'), dat.get('tel'),
                                       dat.get('email'),
                                       dat.get('weixin_id'), dat.get('extattr'))

    def updateUser(self, dat):
        return self.client.user.update(dat.get('user_id'), dat.get('name'), dat.get('department'),
                                       dat.get('position'),
                                       dat.get('mobile'), dat.get('gender'), dat.get('tel'),
                                       dat.get('email'),
                                       dat.get('weixin_id'), dat.get('enable'), dat.get('extattr'))

    def deleteUser(self, user_id):
        return self.client.user.delete(user_id)

    def inviteUser(self, user_id, tips=None):
        return self.client.user.invite(user_id, tips)

    def getAgent(self, agent_id):
        return self.client.agent.get(agent_id)
