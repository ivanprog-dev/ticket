import random
import os
from datetime import datetime, timedelta, timezone
from app import app
from models import db, Ticket

def fill():
    with app.app_context():
        print("Datenbank wird neu erstellt...")
        db.drop_all()
        db.create_all()

        probleme = [
            ("Login-Fehler", "Passwort wird nicht akzeptiert."),
            ("Blue Screen", "Systemabsturz nach Start."),
            ("Drucker", "Netzwerkdrucker reagiert nicht."),
            ("Update-Fehler", "Sicherheits-Update schlägt fehl."),
            ("E-Mail Sync", "Outlook lädt keine Mails."),
            ("Passwort Reset", "Mitarbeiter benötigt neues Passwort."),
            ("Internet langsam", "Verbindung bricht ständig ab."),
            ("Monitor", "Bildschirm bleibt schwarz."),
            ("VPN", "Kein Zugriff aus dem Homeoffice."),
            ("Lizenz", "Office-Lizenz abgelaufen."),
            ("Tastatur", "Einige Tasten klemmen."),
            ("Spam-Filter", "Wichtige Mails werden geblockt."),
            ("Datenbank", "Timeout bei Abfragen."),
            ("2FA", "SMS Code kommt nicht an."),
            ("Laufwerk", "Kein Zugriff auf Marketing-Ordner."),
            ("Akku", "Laptop lädt nicht."),
            ("PDF-Export", "Programm stürzt bei Export ab."),
            ("WLAN Gäste", "Gäste haben kein Internet."),
            ("Skype Audio", "Mikrofon wird nicht erkannt."),
            ("Excel Makro", "VBA Fehler nach Update.")
        ]

        kunden = [
            ("Anna Schmidt", "Tech GmbH", "0170-123", "Hauptstr. 1", "10115", "Berlin", "a@web.de"),
            ("Lars Weber", "Handel AG", "040-444", "Kirchweg 4", "20095", "Hamburg", "l@gmx.de"),
            ("Julia Meyer", "Design Ltd.", "089-555", "Südring 22", "80331", "München", "j@mail.com")
        ]

        for i in range(20):
            titel, beschr = probleme[i]
            k = random.choice(kunden)
            t = Ticket(
                titel=titel, beschreibung=beschr,
                prioritaet=random.choice(["Niedrig", "Mittel", "Hoch"]),
                kategorie=random.choice(["Software", "Hardware", "Zugang/Account"]),
                status=random.choice(["Offen", "In Bearbeitung", "Erledigt"]),
                bearbeiter=random.choice(["Max", "Lisa", "Nicht zugewiesen"]),
                datum=datetime.now(timezone.utc) - timedelta(days=random.randint(0, 30)),
                kunde_name=k[0], kunde_firma=k[1], kunde_telefon=k[2],
                kunde_strasse=k[3], kunde_plz=k[4], kunde_ort=k[5], kunde_email=k[6]
            )
            db.session.add(t)
        
        db.session.commit()
        print("20 Tickets erfolgreich erstellt!")

if __name__ == '__main__':
    fill()