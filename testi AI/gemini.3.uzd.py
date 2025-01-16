import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

# Ielādē datus no CSV faila
data = pd.read_csv("Raw_Data.csv")

# Definē masas vērtību
masa = 0.2  # kg

# Izvēlas datus par paātrinājumu un laiku (pielāgo pēc vajadzības)
paatrinajums = data['paatrinajums']
laiks = data['laiks']

# (Šeit jāievieto kods, lai automātiski noteiktu mešanas un lidošanas periodu)
# Piemēram, var izmantot tresholding, lai atrastu punktus, kur paātrinājums strauji mainās

# Aprēķina spēku
speks = masa * paatrinajums

# Aprēķina ātrumu (integrējot paātrinājumu)
atrums = cumulative_trapezoid(paatrinajums, x=laiks)

# Aprēķina augstumu (integrējot ātrumu)
augstums = cumulative_trapezoid(atrums, x=laiks)

# Zīmē grafikus
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(laiks, paatrinajums)
plt.xlabel("Laiks (s)")
plt.ylabel("Paātrinājums (m/s^2)")

plt.subplot(3, 1, 2)
plt.plot(laiks, speks)
plt.xlabel("Laiks (s)")
plt.ylabel("Spēks (N)")

plt.subplot(3, 1, 3)
plt.plot(laiks, augstums)
plt.xlabel("Laiks (s)")
plt.ylabel("Augstums (m)")

plt.tight_layout()
plt.savefig("telefona_lidojums.pdf")
plt.show()