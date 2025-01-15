import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
from tqdm import tqdm

banner = r"""
   _____  _____ _______          __
  / ____|/ ____|  __ \ \        / /
 | |  __| |    | |  | \ \  /\  / / 
 | | |_ | |    | |  | |\ \/  \/ /  
 | |__| | |____| |__| | \  /\  /   
  \_____|\_____|_____/   \/  \/
  Gamecube Downloader
  Owner: https://github.com/BreckzTv  V1.1  
                                  
"""
print(banner)

def get_rom_links(base_url):
    response = requests.get(base_url)
    response.raise_for_status()  
    soup = BeautifulSoup(response.text, 'html.parser')

    rom_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and (href.endswith('.iso') or href.endswith('.zip')):
            full_url = f"{base_url}/{href}"
            rom_links.append(full_url)

    return rom_links

def download_rom(rom_url, save_directory):
    rom_name = unquote(rom_url.split('/')[-1]) 
    save_path = os.path.join(save_directory, rom_name)
    response = requests.get(rom_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    try:
        with open(save_path, 'wb') as file, tqdm(
            desc=rom_name,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
        print(f'Download abgeschlossen: {save_path}')
    except Exception as e:
        print(f'Fehler beim Herunterladen von {rom_name}: {e}')

def search_roms(rom_links, search_query):
    # Filter ROMs based on a search query
    filtered_roms = [rom for rom in rom_links if search_query.lower() in unquote(rom.split('/')[-1]).lower()]
    return filtered_roms

if __name__ == '__main__':
    base_url = 'https://myrient.erista.me/files/Internet%20Archive/kodi_amp_spmc_canada/EuropeanGamecubeCollectionByGhostware'
    save_directory = 'downloaded_games'

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    rom_links = get_rom_links(base_url)
    print("Verfügbare ROMs:")
    for i, rom in enumerate(rom_links):
        print(f"{i + 1}: {unquote(rom.split('/')[-1])}")

    print(banner)
    search_query = input("Geben Sie den Namen des ROMs ein, nach dem Sie suchen möchten: ")
    filtered_roms = search_roms(rom_links, search_query)

    print("Gefilterte ROMs:")
    for i, rom in enumerate(filtered_roms):
        print(f"{i + 1}: {unquote(rom.split('/')[-1])}")

    print(banner)
    selected_indices = input("Geben Sie die Nummern der ROMs ein, die Sie herunterladen möchten (getrennt durch Kommas): ")
    selected_indices = [int(i) - 1 for i in selected_indices.split(',')]

    selected_roms = [filtered_roms[i] for i in selected_indices if 0 <= i < len(filtered_roms)]
    for rom in selected_roms:
        download_rom(rom, save_directory)
