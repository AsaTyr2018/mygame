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

2. ENTDECKUNG:
   - Agent erkundet die Umgebung, bis er Ressourcenvorkommen entdeckt.
   - Ressourcen-Nodes sind klar visuell unterscheidbar.

3. SAMMELN:
   - Wenn Agent sich nahe an einem Ressourcenvorkommen befindet:
     - Er kann per "E"-Taste Ressourcen abbauen.
     - Pro Interaktion wird eine festgelegte Menge gesammelt:
       - Eisen: +1 Eisen
       - Kupfer: +1 Kupfer
       - Stein: +1 Stein

4. INTERFACE:
   - Am oberen Bildschirmrand befindet sich ein Ressourcen-HUD:
     - [Eisen: X] [Kupfer: Y] [Stein: Z]
   - Die Werte aktualisieren sich in Echtzeit beim Sammeln und Bauen.

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

ZUSÄTZLICHE REGELN:
- Der Agent priorisiert Stein > Eisen > Kupfer in frühen Phasen.
- Miner dürfen nicht überlappend platziert werden.
- Ressourcenlager ist unbegrenzt.

Ordnerstruktur
project_root/
│
├── main.py              # Startet das Spiel
├── world_generator.py   # Weltaufbau und Ressourcennodes
├── entities/
│   ├── player.py        # FirstPersonPlayer mit Zusatzlogik
│   ├── resource_node.py # ResourceNode + Miner
│   └── hud.py           # Ressourcen-HUD
├── systems/
│   └── build_system.py  # Platzierungslogik, Bau-Checks
├── data/
│   └── resource_pool.py # Zentrale Ressourcendaten
└── assets/              # (optional später für Texturen etc.)

Grundidee: Komponentenlogik
main.py: Initialisiert Engine, lädt Module, startet Spiel
resource_node.py: Enthält ResourceNode und Miner
player.py: Erweiterter FirstPersonController mit Interaktion
hud.py: Anzeige aller Ressourcen, evtl. später mit Health, Strom etc.
build_system.py: Logik zum Platzieren von Gebäuden
resource_pool.py: Globale resources = {} Variable + Methoden wie can_afford(), spend() usw.


