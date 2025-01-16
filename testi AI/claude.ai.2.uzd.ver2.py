import h5py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def apstrade_xanes_dati():
    """
    Galvenā funkcija XANES datu apstrādei un vizualizācijai
    """
    # Definējam tukšus masīvus datu glabāšanai
    energijas = []
    attiecibas = []
    
    try:
        # Atveram .h5 failu
        with h5py.File('CTS_Test.h5', 'r') as f:
            # Atrodam visas entry8xxx grupas
            entries = [key for key in f.keys() if key.startswith('entry8')]
            
            for entry in sorted(entries):  # Sakārtojam ierakstus, lai saglabātu secību
                try:
                    # Pārbaudām vai eksistē visi nepieciešamie kanāli
                    if all(channel in f[entry] for channel in ['aem_27_ch01', 'aem_27_ch02', 'pcap_energy_avg']):
                        # Nolasām datus no katra kanāla
                        ch01_data = np.array(f[f'{entry}/aem_27_ch01'])
                        ch02_data = np.array(f[f'{entry}/aem_27_ch02'])
                        energy_data = np.array(f[f'{entry}/pcap_energy_avg'])
                        
                        # Pārbaudām vai dati nav tukši un vai garumi sakrīt
                        if len(ch01_data) > 0 and len(ch02_data) > 0 and len(energy_data) > 0:
                            if len(ch01_data) == len(ch02_data) == len(energy_data):
                                # Aprēķinām attiecību, izvairamies no dalīšanas ar nulli
                                with np.errstate(divide='ignore', invalid='ignore'):
                                    ratio = np.where(ch02_data != 0, ch01_data / ch02_data, np.nan)
                                
                                # Pievienojam datus masīviem
                                energijas.extend(energy_data)
                                attiecibas.extend(ratio)
                            else:
                                print(f"Datu garumi nesakrīt ierakstā {entry}")
                        else:
                            print(f"Tukši dati ierakstā {entry}")
                    else:
                        print(f"Trūkst kāds no kanāliem ierakstā {entry}")
                        
                except Exception as e:
                    print(f"Kļūda apstrādājot ierakstu {entry}: {e}")
                    continue
        
        # Pārveidojam datus par DataFrame
        df = pd.DataFrame({
            'pcap_energy_avg': energijas,
            'ch01_ch02_ratio': attiecibas
        })
        
        # Noņemam NaN vērtības
        df = df.dropna()
        
        # Sakārtojam datus pēc enerģijas
        df = df.sort_values('pcap_energy_avg')
        
        # Saglabājam CSV failā
        df.to_csv('CTS_TiO2-8815.csv', index=False)
        
        # Vizualizējam datus
        vizualizet_datus(df)
        
    except Exception as e:
        print(f"Kļūda darbā ar failu: {e}")

def vizualizet_datus(df):
    """
    Funkcija datu vizualizācijai
    
    Parameters:
    df (pandas.DataFrame): DataFrame ar 'pcap_energy_avg' un 'ch01_ch02_ratio' kolonnām
    """
    try:
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
        
        # Optimizējam grafika robežas
        plt.margins(x=0.02)
        
        # Pielāgojam grafika izmērus
        plt.tight_layout()
        
        # Saglabājam grafiku
        plt.savefig('XANES.pdf', dpi=300, bbox_inches='tight')
        print("Grafiks veiksmīgi saglabāts kā 'XANES.pdf'")
        
    except Exception as e:
        print(f"Kļūda vizualizējot datus: {e}")

# Palaiž programmu
if __name__ == "__main__":
    apstrade_xanes_dati()