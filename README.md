# Landwirtschaft Management System

## Ausgangslage 
Ziel ist es ein funktionsfähiges Landwirtschaft Management System zu bauen, um eine Übersicht über den Tierbestand, Fahrzeuge, Flächen, Futterbestand, Ernteertag zu gewährleisten. Aufgeteilt wird das Projekt in Frontend und Backend. Über Docker Container soll die Anwendung gestartet werden können. 

## Untersuchungsanliegen der individuellen Themenstellung
Benutzern soll es ermöglicht werden einen Überblick über ihre Landwirtschaft zu haben. Zusätzlich soll der zeitliche Ernteertrag graphisch visualisiert werden. 

## Zielsetzung & geplantes Ergebnis
Dem Benutzer soll es ermöglicht werden folgende Daten in das Informationssystem hinzuzufügen, zu löschen, zu updaten oder anzuzeigen: <br>
    - Tierbestand <br>
    - Fahrzeuge <br>
    - Flächen (Eigenbesitz, Gepachtet) <br>
    - Futterbestand <br>
    - Ernteertrag <br>

## Zielkriterien
Das Projekt wird in Frontend und Backend aufgegliedert. Beim Backend wird auf Python und Flask gesetzt und die CRUD-Operationen werden hier implementiert. Für das Frontend kommt HTML, CSS und JavaScript zum Einsatz. Bei der Datenbank wird auf PostgreSQL gesetzt - bei der Modellierung auf SqlAlchemy.

## Erweiterte Ziel- oder Wunschkriterien
Wünschenswert wäre die Integration einer Wettervorhersage der nächsten 3 Tage.

## Meilensteine

| Datum | Meilenstein | 
|----------|----------|
| 16.02.2024   | Entwicklungsumgebung - Container, Aufteilung: Frontend - Backend   | 
| 01.03.2024   | CRUD-Funktionalitäten des Tierbestands, der Fahrzeuge  | 
| 15.03.2024   | CRUD-Funktionalitäten des Futterbestands, des Ernteertrags  | 
| 23.03.2024   | CRUD-Funktionalitäten der Flächen  | 
| 01.04.2024   | Visualisierung des Ernteertrags  | 
| 15.04.2024   | Integration der Wettervorhersage   | 

## Mockup

### Landing Page
Beim Starten der Anwendung werden dem Benutzer Auswahlmöglichkeiten gegeben, um den Tierbestand, Fahrzeugbestand, Flächenbestand, Futterbestand oder Ernteertrag anzuzeigen, updaten, löschen oder hinzufügen zu können. In den jeweiligen Auwahlmöglichkeiten kann der Benutzer Datensätze hinzufügen, löschen, ändern und anzeigen. Beim Ertneertrag soll ein Graph der vergangengen Ertnen einen Überblick über die Zeit schaffen.

<img src="https://github.com/denisepostl/farming-project-2024/blob/main/img/img01.png">

### Tierbestand 
<img src="https://github.com/denisepostl/farming-project-2024/blob/main/img/img02.png">

### Agrar Flächen Besitz 
<img src="https://github.com/denisepostl/farming-project-2024/blob/main/img/img03.png">

### Fahrzeugbestand
<img src="https://github.com/denisepostl/farming-project-2024/blob/main/img/img04.png">

### Futterbestand
<img src="https://github.com/denisepostl/farming-project-2024/blob/main/img/img05.png">

### Ernteertrag
<img src="https://github.com/denisepostl/farming-project-2024/blob/main/img/img06.png">

## Datenmodell
<img src="https://github.com/denisepostl/farming-project-2024/blob/main/img/project_2024.jpg">
