# Machine vision
Prosjektet er få en robot-arm til å gjenkjenne kort eller brikker og hvor den skal plukke de opp, så få den til å spille ting som kort eller kanskje sortere ting. Så skal den bruke en algoritme til å bestemme hvilke trekk å gjøre i en bestemt situasjon. Den skal kunne spille Krypkasino.

## Hvorfor
Det er for å promotere robotikk og fordi dette er relevant til våre videre studier/fremtiden.
Det er også for generall læring innen KI/AI og praksis bruk.

## Prosjektplan
Kartlegging:
Utstyr og ressurser:

Utstyr: 
 - UR-robot (UR5/UR3)
 - sugekopp til UR
 -  USB-kamera,
 -  Kortstokk (52 kort)

Ressurser:
	Finnes i Resources-branchen
  
## Steg for å fullføre prosjektet:

### Forkunnskap/Læring før utvikling av prosjektet:
1. Lære/Kunne python
2. Lære/Kunne det basics av OpenCV.
   	Link til en YouTube som kan hjelpe fra freeCodeCamp for OpenCV:
        https://www.youtube.com/watch?v=oXlwWbU8l2o&t=6303s
   	- Trenger ikke å gå gjennom alt, 1 t 50 min er mer enn nok. :)
3. Lære/Kunne modbus (via python)

### Utføring:

1. Lag en kode som kan gjenkjenne kortene (se etter firkanter).
   Bruk dette til å isolere kortene i 2D (flat), eget bilde for eget kort.
   Dette blir gjort gjennom en for loop for vær av kortene.
   Dette bilde går gjennom en AI som gjenkjenner kortet (1 av 52).
   	Vis du har en kvantedatamaskin skal det skalere bedre (lignene på Grovers algoritme).
   
2. Bruk gjenkjenningen av kort til å lagre informasjon til å fine ut hva som er best å gjøre (utføre i praksis).
   	Det roboten gjør kan forandre seg fra program til program på UR-en,
   	men informasjonen ut fra PC-en er lignene, kan gjøre justeringer vis nødvendig*.

4. Få UR-en til å spille kort*, så lenge det er noe praksis.
5. Kombinere Kort-koden og Modbus koden.
   	Hvordan det blir gjort kan forandre seg.
   	Man kan velge* mellom å ha alt på en kode/file (denne valgte vi)
   	eller importere noen filer in i en annen kode til å utføre classer,funksjoner og AI der sammen.
7. Legg til sikkerhet der det trengs.
   	Spørsmål som "Hva børe AI-en PC-koden ha murlighet til å gjøre?" er viktig.
   	Planen er å lage "actions" i et program på UR-en og forandringen av en variabel/kommunikasjonen
   	mellom PC og UR utfører/aktivere denne "action". Det kan være å plokke noe opp eller plassere noe et sted, osv.









