AGENTEN-VERHALTENSBESCHREIBUNG: "FPS-Resource Builder"

PERSPEKTIVE:
- Agent befindet sich in einer First-Person-Ansicht.
- Die Kamera ist an die Augenhöhe gebunden und folgt den Bewegungen.

UMGEBUNG:
- Die Welt wird bei jedem Spielstart zufällig generiert.
- Es existieren verschiedene Ressourcenvorkommen in der Umgebung:
  - Eisen-Node
  - Kupfer-Node
  - Stein-Node

AUFGABE:
1. BEWEGUNG:
   - Agent kann sich mit WASD durch die Welt bewegen.
   - Blickrichtung wird durch Maussteuerung angepasst.
   - Sprung mit Leertaste möglich.
   - Sprint mit linker Umschalttaste für schnelleres Vorankommen.

2. ENTDECKUNG:
   - Agent erkundet die Umgebung, bis er Ressourcenvorkommen entdeckt.
   - Ressourcen-Nodes sind klar visuell unterscheidbar.
   - Ein Tag-Nacht-Zyklus sorgt für wechselnde Lichtbedingungen.

3. SAMMELN:
   - Wenn Agent sich nahe an einem Ressourcenvorkommen befindet:
     - Er kann per "E"-Taste Ressourcen abbauen.
     - Pro Interaktion wird eine festgelegte Menge gesammelt:
       - Eisen: +1 Eisen
       - Kupfer: +1 Kupfer
       - Stein: +1 Stein
   - Rohstoffe können später in Gebäuden weiterverarbeitet werden.

4. INTERFACE:
   - Am oberen Bildschirmrand befindet sich ein Ressourcen-HUD:
     - [Eisen: X] [Kupfer: Y] [Stein: Z]
   - Die Werte aktualisieren sich in Echtzeit beim Sammeln und Bauen.
   - Eine Energieleiste zeigt verfügbare Stromkapazität an.

5. GEBÄUDEAUFBAU:
   - Agent kann Miner platzieren, wenn er genug Ressourcen besitzt.
   - Voraussetzungen für Miner-Platzierung:
     - Agent steht auf einem Ressourcenknoten
     - Ressourcenkosten erfüllt:
       - 5 Stein, 3 Eisen, 2 Kupfer
     - Platzierungsmodus wird per "B"-Taste aktiviert.
     - Platzierung per Linksklick auf validem Node

6. MINER-FUNKTION:
   - Nach Platzierung erzeugt der Miner alle 10 Sekunden +1 Einheit der zugehörigen Ressource.
   - Miner ist ein einfacher Block mit sichtbarem Partikeleffekt.

7. ZIEL:
   - Agent soll automatisierte Ressourcengewinnung durch Miner aufbauen.
   - Weitere Gebäudearten sind zukünftig vorgesehen.

8. VERARBEITUNG:
   - Ein Schmelzofen kann auf freiem Boden platziert werden.
   - Kosten: 10 Stein, 5 Eisen, 2 Kupfer.
   - Er verarbeitet je 1 Einheit Erz zu 1 Barren in 5 Sekunden.
   - Schmelzöfen benötigen 1 Energie pro aktivem Vorgang.

9. ENERGIESYSTEM:
   - Windräder erzeugen kontinuierlich 1 Energieeinheit.
   - Smelter und andere Maschinen verbrauchen Energie während des Betriebs.
   - Ohne ausreichend Energie pausiert die Produktion.

10. VERTEIDIGUNG:
   - Nachts erscheinen feindliche Kreaturen, die Gebäude angreifen können.
   - Geschütztürme (Kosten: 5 Kupfer, 5 Eisen) feuern automatisch auf Gegner.
   - Einfache Wegfindung steuert die Gegner zu den Gebäuden des Spielers.

ZUSÄTZLICHE REGELN:
- Der Agent priorisiert Stein > Eisen > Kupfer in frühen Phasen.
- Miner dürfen nicht überlappend platziert werden.
- Ressourcenlager ist unbegrenzt.
- Bei Nacht steigt die Spawnrate von Gegnern.
- Ohne Energie funktionieren Schmelzofen und Turrets nicht.

Ordnerstruktur
project_root/
│
├── main.py              # Startet das Spiel
├── world_generator.py   # Weltaufbau und Ressourcennodes
├── entities/
│   ├── player.py        # FirstPersonPlayer mit Zusatzlogik
│   ├── resource_node.py # ResourceNode + Miner
│   ├── smelter.py       # Verarbeitung von Erzen
│   ├── turret.py        # Verteidigungsgebäude
│   └── hud.py           # Ressourcen-HUD
├── systems/
│   ├── build_system.py  # Platzierungslogik, Bau-Checks
│   ├── energy_system.py # Stromverwaltung
│   └── enemy_spawner.py # Gegnerwellen bei Nacht
├── data/
│   └── resource_pool.py # Zentrale Ressourcendaten
└── assets/              # (optional später für Texturen etc.)

Grundidee: Komponentenlogik
main.py: Initialisiert Engine, lädt Module, startet Spiel
resource_node.py: Enthält ResourceNode und Miner
player.py: Erweiterter FirstPersonController mit Interaktion
smelter.py: Steuert die Verarbeitungsvorgänge
energy_system.py: Berechnet verfügbare Energie
enemy_spawner.py: Erzeugt Gegner je nach Tageszeit
hud.py: Anzeige aller Ressourcen, evtl. später mit Health, Strom etc.
build_system.py: Logik zum Platzieren von Gebäuden
resource_pool.py: Globale resources = {} Variable + Methoden wie can_afford(), spend() usw.
