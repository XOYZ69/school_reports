# school_reports

Dieses Projekt stellt eine einfache möglichkeit, professionelle und individuelle Wochenberichte für die IHK zu erstellen.

## Disclaimer

* Jeder ist für den Inhalt, die Formatierung und Abgabe der Berichte selbst verantwortlich
* Wenn Änderungen gewünscht sind oder Bugs auftreten einen Git Issue anlegen!
* Bei jedem pull wird report.tex und config.py überschrieben. Bedenkt das!

## Requirements

Dieses Projekt benötigt Python und LaTeX um vernünfig zu laufen.

* Python 
  * *Beim installieren von Python sollte das "Path-Limit" entfernt werden. Ist im normalfall eine checkbox beim Installationsclient.*
  * Python kann man von der offiziellen Seite herunterladen: <https://www.python.org/downloads/>
  * Das Projekt wurde in Python 3.9.2 entwickelt und bietet somit keinen offiziellen support für ältere Versionen
* LaTeX 
  * LaTeX zu installieren klingt immer schwierig ist es aber nicht.
  * Zunächst besucht man die Seite <https://miktex.org/download>
  * Hier lädt man sich die Version für sein Betriebssystem herunter. Hierbei lieber den installer als die portable edition nutzen.
  * Beim Installieren sollten folgende Einstellungen beachtet werden: 
    * Preffered paper: <span style="color:red">A4</span>
    * Install missing packages on-the-fly: <span style="color:red">Yes</span> 
      * Diese Option führt dazu, dass man nicht jedes mal bestätigen muss wenn bestimmte Packages fehlen. Später beim ausführen merkt man wie viele eigentlich installiert werden müssen für dieses Template.
  * Danach kann man MikTeX ganz einfach installieren.
  * Anschließend sollte man einmal MikTeX öffnen um nach updates zu suchen (Der erste Start gibt dies auch meist als Fehlermeldung aus.)
  * In dem Reiter "Updates" kann man dann einfach alle verfügbaren updates installieren. So hat man immer sicher die neuste Version.

## Vorbereitung

* Zunächst braucht man eine "reports.json"-file 
  * In zukünftigen Updates kann man den Speicherort dynamisch angeben. Aktuell muss diese im main directory liegen
  * In dem repository liegt eine Beispiel Datei um den Aufba zu erklären. Bei weiteren Fragen den Source code lesen oder an KP wenden.
* Überprüfen ob alle Tools aus den *Requirements* installiert sind.
* Danach die *setup.py* ausführen und einige Zeit warten.
* Die Ausgabe befindet sich in dem Ordner "report_output\_\*"
* Daten müssen in config.py bzw. reports/report.tex angepasst werden.

## Informationen & Tips

* Wenn Zeichen wie z.B. '&' nicht richtig angezeigt werden, liegt das Problem meist an LaTeX selber. Ändert man '&' zu '\\\\&' wird dieses Problem behoben. 
  * Dies gilt auch z.B. für ["]
  * Da json hier als Format genutzt wird muss vor anführungszeichen ein Backslash [\\].
  * ["] -> [\\"]
* Einträge die mit "$s " markiert werden gelten als Berufsschuleinträge und werden deshalb anders im Bericht angezeigt
* Der Marker "::" trennt einen Eintrag und macht den ersten Teil fettgedruckt und ersetzt "::" mit " - "
* Mit Hilfe von folgender Notation kann man farben nutzen 
  * \<color:red\>Text\<color:end\>
* In config.py befinden sich shortcuts die man nutzen kann um spezeille Events zu definieren