# -*- coding: utf-8 -*-

from ..extensions import db, SLBigInteger
import time


class TtsHistory(db.Model):
    __tablename__ = 'tts_history'
    id = db.Column(SLBigInteger, primary_key=True)
    lsh = db.Column(db.String(30))
    phone_number = db.Column(db.String(20))
    note = db.Column(db.Text)
    send_at = db.Column(SLBigInteger)
    send_status = db.Column(db.Integer)
    result_id = db.Column(db.String(20))
    accept_at = db.Column(SLBigInteger)
    accept_duration = db.Column(db.Integer)
    accept_status = db.Column(db.Integer)
    accept_reason = db.Column(db.String(30))

    def __repr__(self):
        return '<TtsHistory %r>' % self.id

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def display(self):
        return {
            'lsh': self.lsh,
            'phone_number': self.phone_number,
            'send_at': self.send_at,
            'note': self.note,
            'send_status': self.send_status,
        }

    @staticmethod
    def new(lsh, phone, note, send_status, result_id):
        send_at = int(time.time())
        return TtsHistory(send_at=send_at,
                          lsh=lsh,
                          phone_number=phone,
                          note=note,
                          send_status=send_status,
                          result_id=result_id,
                          )

    @classmethod
    def from_data(cls, data):
        pass