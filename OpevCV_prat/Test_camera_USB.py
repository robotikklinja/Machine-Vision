import cv2

# Sett opp USB-kameraet med VideoCapture. Endre tallet (1, 2, 3 osv.) hvis 1 ikke fungerer.
cap = cv2.VideoCapture(1)  # Prøv 1 for USB-kameraet

if not cap.isOpened():
    print("Kan ikke åpne USB-kameraet. Prøv å endre tallet fra 1 til 2, 3 osv.")
    exit()

# Les fra kameraet i en loop
while True:
    # Les ramme-for-ramme
    ret, frame = cap.read()

    # Sjekk om rammen ble lest riktig
    if not ret:
        print("Kan ikke hente bilde fra USB-kameraet")
        break

    # Vis rammen i et vindu
    cv2.imshow("USB-Kamera", frame)

    # Avslutt ved å trykke på 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Frigjør kameraet og lukk vinduene når loopen avsluttes
cap.release()
cv2.destroyAllWindows()