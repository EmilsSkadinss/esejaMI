import h5py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

def apstrade_xanes_dati(h5_file):
    """
    Apstrādā XANES datus no norādītā h5 faila.

    Args:
        h5_file (str): H5 faila nosaukums.
    """

    rezultati = {'pcap_energy_avg': [], 'ch01_ch02_ratio': []}

    try:
        with h5py.File(h5_file, 'r') as f:
            for entry in f.keys():
                if entry.startswith('entry8'):
                    try:
                        ch01 = f[f'{entry}/aem_27_ch01'][()]
                        ch02 = f[f'{entry}/aem_27_ch02'][()]
                        energy = f[f'{entry}/pcap_energy_avg'][()]

                        ratio = ch01 / ch02
                        rezultati['pcap_energy_avg'].extend(energy)
                        rezultati['ch01_ch02_ratio'].extend(ratio)

                    except KeyError as e:
                        print(f"Trūkst kanāla ierakstā {entry}: {e}")
                    except Exception as e:
                        print(f"Kļūda apstrādājot ierakstu {entry}: {e}")

        df = pd.DataFrame(rezultati)
        df.to_csv('CTS_TiO2-8815.csv', index=False)

        vizualizet_datus()

    except Exception as e:
        print(f"Kļūda darbā ar failu: {e}")

def vizualizet_datus():
    """
    Vizualizē datus no CSV faila.
    """

    try:
        df = pd.read_csv('CTS_TiO2-8815.csv')

        plt.figure(figsize=(10, 6))
        plt.plot(df['pcap_energy_avg'], df['ch01_ch02_ratio'], 'b-', linewidth=1.5)
        plt.title('Ti L$_{2,3}$ edge (TiO$_2$ SolGel)')
        plt.xlabel('Energy, eV')
        plt.ylabel('Normalized intensity, a.u.')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('XANES.pdf', dpi=300, bbox_inches='tight')
        print("Grafiks veiksmīgi saglabāts kā 'XANES.pdf'")

    except Exception as e:
        print(f"Kļūda vizualizējot datus: {e}")

# Palaiž programmu
if __name__ == "__main__":
    h5_file = 'CTS_Test.h5'  # Norādi šeit savu h5 faila nosaukumu
    apstrade_xanes_dati(h5_file)