from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from marshmallow import fields, Schema
import datetime

class WhiteboardModel(db.Model):
  """
  Whiteboard Events Model
  """
  __tablename__ = 'wb_events'
  id = db.Column(db.Integer, primary_key=True)
  status = db.Column(db.String, nullable=False)
  description = db.Column(db.String)
  contact_name = db.Column(db.String)
  contact_phone_number = db.Column(db.String)
  notes = db.Column(db.Text)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.status = data.get('status')
    self.description = data.get('description')
    self.contact_name = data.get('contact_name')
    self.contact_phone_number = data.get('contact_phone_number')
    self.notes = data.get('notes')

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    #self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @staticmethod
  def get_all_events():
    return WhiteboardModel.query.all()

  @staticmethod
  def get_one_event(id):
    return WhiteboardModel.query.get(id)

  @staticmethod
  def get_event_on_status(status):
    return WhiteboardModel.query.filter(WhiteboardModel.status == status).all()

  def __repr(self):
    return '<id {}>'.format(self.id)


class WhiteboardSchema(Schema):
  """
  Whiteboard Schema
  """
  id = fields.Integer(dump_only=True)
  status = fields.Str(required=True)
  description = fields.Str(required=True)
  contact_name = fields.Str(required=True)  
  contact_phone_number = fields.Str(required=True)
  notes = fields.Str(required=True)