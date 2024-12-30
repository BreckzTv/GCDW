import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote  # Import unquote to decode URL-encoded strings

banner=r"""
   _____  _____ _______          __
  / ____|/ ____|  __ \ \        / /
 | |  __| |    | |  | \ \  /\  / / 
 | | |_ | |    | |  | |\ \/  \/ /  
 | |__| | |____| |__| | \  /\  /   
  \_____|\_____|_____/   \/  \/
  Gamecube Downloader
  Owner:https://github.com/BreckzTv  V1.0  
                                  
"""
print(banner)


def get_rom_links(base_url):
    response = requests.get(base_url)
    response.raise_for_status()  # Überprüfen Sie, ob der Download erfolgreich war
    soup = BeautifulSoup(response.text, 'html.parser')

    # Suchen Sie nach Links zu ROM-Dateien
    rom_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and (href.endswith('.iso') or href.endswith('.zip')):  # Passen Sie die Dateiendungen an
            full_url = f"{base_url}/{href}"
            rom_links.append(full_url)

    return rom_links

def download_rom(rom_url, save_directory):
    rom_name = rom_url.split('/')[-1]  # Beispiel für den ROM-Namen
    rom_name = unquote(rom_name)  # Decodieren Sie den Namen, um Prozent-Codierungen zu entfernen
    save_path = os.path.join(save_directory, rom_name)

    try:
        print(f"Herunterladen von {rom_url}...")
        response = requests.get(rom_url)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f'Download abgeschlossen: {save_path}')

    except Exception as e:
        print(f'Fehler beim Herunterladen von {rom_name}: {e}')

def search_roms(rom_links, search_query):
    # Filter ROMs based on a search query
    filtered_roms = [rom for rom in rom_links if search_query.lower() in rom.split('/')[-1].lower()]
    return filtered_roms

if __name__ == '__main__':
    base_url = 'https://myrient.erista.me/files/Internet%20Archive/kodi_amp_spmc_canada/EuropeanGamecubeCollectionByGhostware'
    save_directory = 'downloaded_games'

    # Erstellen Sie das Verzeichnis, falls es nicht existiert
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # ROM-Links abrufen
    rom_links = get_rom_links(base_url)
    print("Verfügbare ROMs:")
    for i, rom in enumerate(rom_links):
        print(f"{i + 1}: {rom}")

    # Benutzer zur Eingabe eines Suchbegriffs auffordern
    print(banner)
    search_query = input("Geben Sie den Namen des ROMs ein, nach dem Sie suchen möchten: ")
    filtered_roms = search_roms(rom_links, search_query)

    print("Gefilterte ROMs:")
    for i, rom in enumerate(filtered_roms):
        print(f"{i + 1}: {rom}")

    # Benutzer zur Auswahl auffordern
    print(banner)
    selected_indices = input("Geben Sie die Nummern der ROMs ein, die Sie herunterladen möchten (getrennt durch Kommas): ")
    selected_indices = [int(i) - 1 for i in selected_indices.split(',')]

    # Ausgewählte ROMs herunterladen
    selected_roms = [filtered_roms[i] for i in selected_indices if 0 <= i < len(filtered_roms)]
    for rom in selected_roms:
        download_rom(rom, save_directory)
