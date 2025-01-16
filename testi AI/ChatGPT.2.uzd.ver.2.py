import h5py
import csv
import numpy as np
import matplotlib.pyplot as plt

# 1. Datu nolasīšana no HDF5 faila
input_file = 'CTS_Test.h5'
output_csv = 'CTS_TiO2-8815.csv'

# Saglabāsim rezultātus šajā sarakstā
results = []

with h5py.File(input_file, 'r') as f:
    # Iterē cauri visām "entry8xxx" grupām
    for group_name in f.keys():
        if group_name.startswith("entry8"):
            group = f[group_name]
            try:
                # Nolasām kanālu datus, pārbaudot, vai tie eksistē
                if ('aem_27_ch01' in group and 
                    'aem_27_ch02' in group and 
                    'pcap_energy_avg' in group):
                    ch01 = group['aem_27_ch01'][:]
                    ch02 = group['aem_27_ch02'][:]
                    energy = group['pcap_energy_avg'][:]

                    # Pārbaudām, vai datu garumi sakrīt
                    if len(ch01) == len(ch02) == len(energy):
                        # Aprēķina attiecību un saglabā rezultātus
                        ratio = ch01 / ch02
                        for e, r in zip(energy, ratio):
                            results.append([e, r])
                    else:
                        print(f"Brīdinājums: Datu garumi nesakrīt grupā {group_name}")
                else:
                    print(f"Brīdinājums: Trūkst nepieciešamie kanāli grupā {group_name}")

            except Exception as e:
                print(f"Kļūda apstrādājot grupu {group_name}: {e}")

# 2. Saglabājam rezultātus CSV failā
if results:
    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Rakstām galvenes
        csvwriter.writerow(['pcap_energy_avg', 'ch01_ch02_ratio'])
        # Rakstām datus
        csvwriter.writerows(results)
else:
    print("Nav datu, ko saglabāt CSV failā.")

# 3. Datu vizualizācija
if results:
    # Ielasām datus no CSV faila
    data = np.genfromtxt(output_csv, delimiter=',', skip_header=1)

    # Izvelkam x un y asis
    x = data[:, 0]  # pcap_energy_avg
    y = data[:, 1]  # ch01 / ch02

    # Izveidojam grafiku
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label='ch01 / ch02', color='blue')
    plt.title('Ti L$_{2,3}$ edge (TiO$_2$ SolGel)')
    plt.xlabel('Energy, eV')
    plt.ylabel('Normalized intensity, a.u.')
    plt.grid(True)
    plt.legend()

    # Saglabājam grafiku kā PDF
    output_pdf = 'XANES.pdf'
    plt.savefig(output_pdf)
    plt.close()
else:
    print("Nav datu, ko vizualizēt.")
