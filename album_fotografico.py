import csv

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        with open(file_path, "r", newline='', encoding='utf-8') as f:
            reader=csv.DictReader(f)

            #L'idea è quella di creare un dizionario album nel quale inserisco gli anni,
            #i quali a loro volta sono delle liste che contengono le informazioni delle
            #foto relative a quell'anno
            album={}
            for row in reader:
                if row[' anno'] not in album:
                    album[row[' anno']]=[]
                    album[row[' anno']].append(row)
                else:
                    album[row[' anno']].append(row)
            # Una volta aperto il file itero sulle singole righe che contengono le
            # informazioni, in particolare inizialmente mi concentro solo sull'anno,
            # se esso non è presente nel mio album allora creo l'anno nell'album come lista
            # nel quale poi inserirò quella foto, altrimenti inserisco direttamente la
            #foto nella lista che riguarda l'anno

            return album



    except FileNotFoundError:
        return None





def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    try:
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

        with open(file_path, "a", newline='', encoding='utf-8') as f:

            writer = csv.DictWriter(f, fieldnames=foto.keys())
            writer.writerow(foto)


            if anno not in album:
                album[anno]=[]
                album[anno].append(foto)
            else:
                album[anno].append(foto)

        return foto,album

    except FileNotFoundError:
        return None





def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # TODO


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO


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

            foto,album_nuovo = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                for el in album:
                    print(el)
                    for i in range(len(album[el])):
                        print(album[el][i])

                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
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
