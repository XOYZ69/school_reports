# Changelog

---

## alpha v2-commit_kp_2023-02-02_01
    - Neuer Config Paramter: config_group_list: bool
        - Ist dieser auf true, so werden Auflistungen (die durch " | " entstehen) gruppiert und besser gekennzeichnet
    - Neuer Config Paramter: config_lists_spacing: string
        - Gibt das spacing zwischen auflistungen an (itemize)

## alpha v2-commit_kp_2023-02-01_01
    - Neuer Parameter " | " hinzugefügt.
        - Wird ein Inhalt eines eintrags nach dem normalen Trenner "::" noch zusätzlich mit " | " getrennt so werden die einzelnen Abschnitte als Tabelle dargestellt.
    - Neue Parameter für die Console
        - Es wird nun verlangt einen Paramter mit dem Python programm mitzugeben:
            - LIST-MISSING
                - Zeigt fehlende oder ungenügende einträge an
            - BUILD
                - erstellt den Report
    - Error Handling
        - Es wird nun überprüft ob ein wochentag exisitert. tut dies nicht beendet sich das programm selbst
