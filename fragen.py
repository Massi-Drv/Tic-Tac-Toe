import json

data = {
    "Fragen": [
        {
            "Kategorie": "Stadt Detmold (Umweltkontext)",
            "Fragen": [
                {
                    "Frage": "Lohnt sich in einer Stadt wie Detmold ein Auto bereits ab 1,5 km?",
                    "Antwort": "Nein"
                },
                {
                    "Frage": "Detmold hat insgesamt mehr als 350.000 m^2 Grünfläche",
                    "Antwort": "Ja"
                },
                {
                    "Frage": "Detmold erzeugt mehr erneuerbare, als fossile Energie",
                    "Antwort": "Ja"
                }
            ]
        },
        {
            "Kategorie": "Allgemeiner Umweltkontext",
            "Fragen": [
                {
                    "Frage": "Gehört Deutschland zu den Top 10 im Klimaschutz Index (KSI)?",
                    "Antwort": "Nein, Platz 16"
                },
                {
                    "Frage": "Bräuchte es über 7 Mio. neue Bäume für die CO^2 Kompensierung in Deutschland?",
                    "Antwort": "Ja, 7.475.000"
                },
                {
                    "Frage": "Würde es der natürlichen Ökonomie gut tun, mehr Biodiversität zu integrieren?",
                    "Antwort": "Nein, Artenvielfalt"
                }
            ]
        },
        {
            "Kategorie": "Sustainable Living",
            "Fragen": [
                {
                    "Frage": "Bebaute Fläche lässt sich mit \"vergrünung\" auf anderen Plätzen ausgleichen",
                    "Antwort": "Jain"
                },
                {
                    "Frage": "Reichen 7 Tage selbst erzeugte Solarenergie aus, um ein ganzes Einfamilienhaus für einen Monat mit Strom zu versorgen?",
                    "Antwort": "Ja (durchschnittliche Einspeisung: 157.5 kWh/Woche, Bedarf: 83.3 kWh pro Woche)"
                },
                {
                    "Frage": "Zement ist der umweltfreundlichste Baustoff",
                    "Antwort": "Nein"
                }
            ]
        }
    ]
}

with open('fragen.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
