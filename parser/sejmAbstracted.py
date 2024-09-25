import pandas as pd
import os
import logging
import codecs

# Niestandardowy FileHandler, aby obsłużyć polskie znaki
class UTF8FileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a', encoding='utf-8', delay=False):
        super().__init__(filename, mode, encoding, delay)

    def _open(self):
        return codecs.open(self.baseFilename, self.mode, self.encoding)

# Konfiguracja loggera z niestandardowym handlerem dla polskich znaków
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[UTF8FileHandler('sejm_projects_processing.log', mode='w')])

def process_sejm_projects(file_path, output_path):
    logging.info("Rozpoczęto przetwarzanie pliku CSV.")

    df = pd.read_csv(file_path, sep=',')
    logging.info(f"Wczytano plik CSV z {len(df)} wierszami.")

    for i, row in df.iterrows():
        if "Projekt wpłynął do Sejmu" in row['Activity']:
            df.at[i, 'Activity'] = "Projekt wpłynął do Sejmu"
            logging.info(f"Zaktualizowano wpis dla wiersza {i}: 'Projekt wpłynął do Sejmu'.")

        if "Sprawozdanie komisji" in row['Activity']:
            if i > 0 and df.at[i - 1, 'Activity'] == "I czytanie w komisjach":
                df.at[i, 'Activity'] = "Sprawozdanie komisji po I czytaniu"
                logging.info(f"Zaktualizowano wpis dla wiersza {i}: 'Sprawozdanie komisji po I czytaniu'.")
            elif i > 0 and df.at[i - 1, 'Activity'] == "I czytanie na posiedzeniu Sejmu":
                df.at[i, 'Activity'] = "Sprawozdanie komisji po I czytaniu na posiedzeniu Sejmu"
                logging.info(f"Zaktualizowano wpis dla wiersza {i}: 'Sprawozdanie komisji po I czytaniu na posiedzeniu Sejmu'.")
            elif i > 0 and df.at[i - 1, 'Activity'] == "II czytanie na posiedzeniu Sejmu":
                df.at[i, 'Activity'] = "Sprawozdanie komisji po II czytaniu na posiedzeniu Sejmu"
                logging.info(f"Zaktualizowano wpis dla wiersza {i}: 'Sprawozdanie komisji po II czytaniu na posiedzeniu Sejmu'.")

        if "Sprawozdanie komisji" in row['Activity']:
            if i > 0 and df.at[i - 1, 'Activity'] == "Stanowisko Senatu":
                df.at[i, 'Activity'] = "Sprawozdanie komisji po poprawkach Senatu"
                logging.info(f"Zaktualizowano wpis dla wiersza {i}: 'Sprawozdanie komisji po poprawkach Senatu'.")

    df.to_csv(output_path, index=False, sep=',')
    logging.info(f"Zapisano przetworzone dane do pliku: {output_path}.")
    print("Przetwarzanie zakończone. Plik zapisany na pulpicie jako 'sejm_projects_abstracted.csv'.")

input_file_path = 'C:/Users/Anonymous/Desktop/sejm_projects.csv'
output_file_path = 'C:/Users/Anonymous/Desktop/sejm_projects_abstracted.csv'

process_sejm_projects(input_file_path, output_file_path)
