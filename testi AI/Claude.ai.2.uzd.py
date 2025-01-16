
import h5py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

def apstrade_xanes_dati():
    """
    Galvenā funkcija XANES datu apstrādei un vizualizācijai
    """
    # Izveidojam sarakstu rezultātu glabāšanai
    rezultati = {
        'pcap_energy_avg': [],
        'ch01_ch02_ratio': []
    }
    
    try:
        # Atveram .h5 failu
        with h5py.File('CTS_Test.h5', 'r') as f:
            # Atrodam visas entry8xxx grupas
            entries = [key for key in f.keys() if key.startswith('entry8')]
            
            for entry in entries:
                try:
                    # Mēģinām nolasīt visus nepieciešamos kanālus
                    ch01 = f[f'{entry}/aem_27_ch01'][()]
                    ch02 = f[f'{entry}/aem_27_ch02'][()]
                    energy = f[f'{entry}/pcap_energy_avg'][()]
                    
                    # Aprēķinām attiecību
                    ratio = ch01 / ch02
                    
                    # Pievienojam datus rezultātu sarakstam
                    rezultati['pcap_energy_avg'].extend(energy)
                    rezultati['ch01_ch02_ratio'].extend(ratio)
                    
                except KeyError as e:
                    print(f"Trūkst kanāla ierakstā {entry}: {e}")
                    continue
                except Exception as e:
                    print(f"Kļūda apstrādājot ierakstu {entry}: {e}")
                    continue
    
        # Izveidojam DataFrame un saglabājam CSV failā
        df = pd.DataFrame(rezultati)
        df.to_csv('CTS_TiO2-8815.csv', index=False)
        
        # Vizualizējam datus
        vizualizet_datus()
        
    except Exception as e:
        print(f"Kļūda darbā ar failu: {e}")

def vizualizet_datus():
    """
    Funkcija datu vizualizācijai no CSV faila
    """
    try:
        # Nolasām datus no CSV
        df = pd.read_csv('CTS_TiO2-8815.csv')
        
        # Izveidojam jaunu figūru
        plt.figure(figsize=(10, 6))
        
        # Zīmējam grafiku
        plt.plot(df['pcap_energy_avg'], df['ch01_ch02_ratio'], 'b-', linewidth=1.5)
        
        # Pievienojam nosaukumus
        plt.title('Ti L$_{2,3}$ edge (TiO$_2$ SolGel)')
        plt.xlabel('Energy, eV')
        plt.ylabel('Normalized intensity, a.u.')
        
        # Pielāgojam grafika izskatu
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Saglabājam grafiku
        plt.savefig('XANES.pdf', dpi=300, bbox_inches='tight')
        print("Grafiks veiksmīgi saglabāts kā 'XANES.pdf'")
        
    except Exception as e:
        print(f"Kļūda vizualizējot datus: {e}")

# Palaiž programmu
if __name__ == "__main__":
    apstrade_xanes_dati()