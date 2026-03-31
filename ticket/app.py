import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timezone
# WICHTIG: Wir importieren db und die Models aus der models.py
from models import db, Ticket, Comment 

app = Flask(__name__)

# Konfiguration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Datenbank mit App verknüpfen
db.init_app(app)

# Tabellen erstellen, falls sie noch nicht existieren
with app.app_context():
    db.create_all()

# --- ROUTEN ---

@app.route('/')
def index():
    return render_template('kunde.html')

@app.route('/add', methods=['POST'])
def add_ticket():
    neues = Ticket(
        titel=request.form.get('titel'),
        beschreibung=request.form.get('beschreibung'),
        prioritaet=request.form.get('prioritaet', 'Mittel'),
        kategorie=request.form.get('kategorie', 'Allgemein'),
        kunde_name=request.form.get('name'),
        kunde_firma=request.form.get('firma'),
        kunde_email=request.form.get('email'),
        kunde_telefon=request.form.get('telefon'),
        kunde_strasse=request.form.get('strasse'),
        kunde_plz=request.form.get('plz'),
        kunde_ort=request.form.get('ort')
    )
    db.session.add(neues)
    db.session.commit()
    return redirect(url_for('support_view'))

@app.route('/support')
def support_view():
    q = request.args.get('q', '')
    kat = request.args.get('kat', '')
    prio = request.args.get('prio', '')
    st = request.args.get('status', '')
    
    query = Ticket.query
    if q: 
        query = query.filter((Ticket.titel.contains(q)) | (Ticket.kunde_name.contains(q)))
    if kat: 
        query = query.filter(Ticket.kategorie == kat)
    if prio: 
        query = query.filter(Ticket.prioritaet == prio)
    if st: 
        query = query.filter(Ticket.status == st)
        
    tickets = query.order_by(Ticket.id.desc()).all()
    return render_template('support.html', tickets=tickets, q=q, kat=kat, pr=prio, st=st)

@app.route('/support/ticket/<int:id>')
def ticket_detail(id):
    ticket = Ticket.query.get_or_404(id)
    return render_template('detail.html', ticket=ticket)

@app.route('/assign/<int:id>', methods=['POST'])
def assign_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    neuer_bearbeiter = request.form.get('bearbeiter')
    
    log_text = f"Ticket zugewiesen an: {neuer_bearbeiter} (Status: In Bearbeitung)"
    new_log = Comment(text=log_text, author="System", ticket_id=id)
    
    ticket.bearbeiter = neuer_bearbeiter
    ticket.status = "In Bearbeitung"
    
    db.session.add(new_log)
    db.session.commit()
    return redirect(url_for('ticket_detail', id=id))

@app.route('/solve/<int:id>', methods=['POST'])
def solve_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    ticket.loesung = request.form.get('loesung')
    ticket.status = "Erledigt"
    
    new_log = Comment(text="Ticket wurde abgeschlossen.", author="System", ticket_id=id)
    db.session.add(new_log)
    db.session.commit()
    return redirect(url_for('support_view'))

@app.route('/reopen/<int:id>')
def reopen_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    ticket.status = "Offen"
    
    new_log = Comment(text="Ticket wurde reaktiviert.", author="System", ticket_id=id)
    db.session.add(new_log)
    db.session.commit()
    return redirect(url_for('ticket_detail', id=id))

@app.route('/comment/<int:id>', methods=['POST'])
def add_comment(id):
    text = request.form.get('comment_text')
    if text:
        new_comment = Comment(text=text, author="Support", ticket_id=id)
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for('ticket_detail', id=id))

if __name__ == '__main__':
    app.run(debug=True)