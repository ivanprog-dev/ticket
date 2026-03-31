from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(100), nullable=False)
    beschreibung = db.Column(db.Text, nullable=False)
    prioritaet = db.Column(db.String(20), default='Mittel')
    kategorie = db.Column(db.String(50), default='Allgemein')
    status = db.Column(db.String(20), default='Offen')
    bearbeiter = db.Column(db.String(100), default='Nicht zugewiesen')
    datum = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    loesung = db.Column(db.Text)
    
    # Kundendaten
    kunde_name = db.Column(db.String(100))
    kunde_firma = db.Column(db.String(100))
    kunde_email = db.Column(db.String(100))
    kunde_telefon = db.Column(db.String(50))
    kunde_strasse = db.Column(db.String(100))
    kunde_plz = db.Column(db.String(10))
    kunde_ort = db.Column(db.String(100))
    
    comments = db.relationship('Comment', backref='ticket', lazy=True, cascade="all, delete-orphan")

    def get_kat_color(self):
        mapping = {'Software': 'bg-blue-600', 'Hardware': 'bg-amber-600', 'Zugang/Account': 'bg-purple-600'}
        return mapping.get(self.kategorie, 'bg-gray-600')

    def get_prio_color(self):
        mapping = {
            'Hoch': 'bg-red-600/20 text-red-400 border border-red-600/50',
            'Mittel': 'bg-orange-600/20 text-orange-400 border border-orange-600/50',
            'Niedrig': 'bg-emerald-600/20 text-emerald-400 border border-emerald-600/50'
        }
        return mapping.get(self.prioritaet, 'bg-gray-600/20 text-gray-400')

    def get_status_color(self):
        mapping = {
            'Offen': 'bg-blue-500/10 text-blue-400 border border-blue-500/30',
            'In Bearbeitung': 'bg-indigo-500/10 text-indigo-300 border border-indigo-500/30',
            'Erledigt': 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
        }
        return mapping.get(self.status, 'bg-gray-500/10 text-gray-400')

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    datum = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    author = db.Column(db.String(50), default='System')
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)