
import csv

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        with open(file_path, "r", newline='', encoding='utf-8') as f:
            reader=csv.DictReader(f)

            # L'idea è quella di creare un dizionario (album) nel quale inserisco gli anni,
            # i quali a loro volta sono delle liste che contengono le foto e le loro informazioni
            # relative a quell'anno
            album={}
            for row in reader:
                if row[' anno'] not in album:
                    album[row[' anno']]=[]
                    album[row[' anno']].append(row)
                else:
                    album[row[' anno']].append(row)
            # Una volta aperto il file itero sulle singole righe che contengono le
            # informazioni, in particolare inizialmente mi concentro solo sull'anno,
            # se esso non è presente nel mio album, allora creo l'anno nell'album come lista
            # nella quale poi inserirò quella foto, altrimenti inserisco direttamente la
            # foto nella lista che riguarda il suo anno

            return album



    except FileNotFoundError:
        return None





def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""

    # Per prima cosa controllo che il mese inserito sia tra i numeri possibili
    # e che il codice della foto non sia già all'interno dell'album, così poi da poter creare una libreria
    # della foto che contiene i dati inseriti

    if mese < 1 or mese > 12:
        return None
    for el in album:
        for photo in album[el]:
            if photo['codice'] == codice:
                return None

        foto={
            'codice': codice,
            ' titolo': titolo,
            ' autore': autore,
            ' mese': mese,
            ' anno': anno,
        }

    try:
        # Apro il file in modo da poter aggiungere alla fine di quest'ultimo la foto con le sue informazioni
        # indicate nel passaggio prima
        with open(file_path, "a", newline='', encoding='utf-8') as f:

            writer = csv.DictWriter(f, fieldnames=foto.keys())
            writer.writerow(foto)

            # faccio un controllo riguardante l'anno della foto, vedendo se esso sia già presente
            # o meno, in tal caso creo all'interno del dizionario album una lista denominata con
            # l'anno nella quale inserisco la foto che si presenta come un dizionario
            # (passaggio simile fatto nella def precedente)
            if anno not in album:
                album[anno]=[]
                album[anno].append(foto)
            else:
                album[anno].append(foto)

        return foto

    except FileNotFoundError:
        return None





def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""

    # Dato il codice dall'utente, col ciclo for itero sugli elementi dell'album (gli anni), e poi itero
    # sui singoli elementi all'interno degli anni (le foto) e se c'è un codice che coincide faccio return
    for el in album:
        for photo in album[el]:
            if photo['codice'] == codice:
                return photo

    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    if anno not in album:
        return None

    # Con un ciclo for itero sugli elementi all'interno dell'anno (foto_anno) per poterli aggiungere ad una
    # lista che riunisce tutti i titoli di un determinato anno, per poi usare il comando sorted sulla lista per
    # poterli ordinare alfabeticamente
    titoli_anno=[]
    foto_anno=album[anno]
    for el in foto_anno:
        titoli_anno.append(el[' titolo'])

    titoli_ordinati=sorted(titoli_anno)

    return titoli_ordinati



def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                for el in album:
                    print(el)
                    for i in range(len(album[el])):
                        print(album[el][i])

                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = input("Anno: ").strip()
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                #for el in album:
                    #print(el)
                    #for i in range(len(album[el])):
                        #print(album[el][i])

                print(f"Foto aggiunta con successo!")
                print(foto)
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato['codice']}, {risultato[' titolo']}, {risultato[' autore']}, {risultato[' mese']}, {risultato[' anno']}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = input("Inserisci l'anno da consultare: ").strip()
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
