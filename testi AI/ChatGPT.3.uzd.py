import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

# Telefona masa kilogramos
mass = 0.2  # kg

# Ielādē datus
file_path = 'Raw_Data.csv'  # Norādi faila nosaukumu
data = pd.read_csv(file_path, delimiter='\t')

# Pārsauc kolonnas, ja nepieciešams
data.columns = ['Time (s)', 'Acceleration x (m/s^2)', 'Acceleration y (m/s^2)', 
                'Acceleration z (m/s^2)', 'Absolute acceleration (m/s^2)']

# Aprēķina spēku (F = m * a)
data['Force (N)'] = mass * data['Absolute acceleration (m/s^2)']

# Aprēķina lidojuma augstumu, integrējot paātrinājumu divreiz
time = data['Time (s)']
vertical_acceleration = data['Acceleration z (m/s^2)'] - 9.81  # Novērš gravitācijas ietekmi
velocity = cumulative_trapezoid(vertical_acceleration, time, initial=0)  # Integrē paātrinājumu, lai iegūtu ātrumu
height = cumulative_trapezoid(velocity, time, initial=0)  # Integrē ātrumu, lai iegūtu augstumu
data['Height (m)'] = height

# Zīmē grafikus
plt.figure(figsize=(12, 8))

# Paātrinājuma grafiks
plt.subplot(3, 1, 1)
plt.plot(time, data['Absolute acceleration (m/s^2)'], label='Absolute Acceleration')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s^2)')
plt.title('Acceleration Over Time')
plt.grid(True)
plt.legend()

# Spēka grafiks
plt.subplot(3, 1, 2)
plt.plot(time, data['Force (N)'], label='Force', color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Force (N)')
plt.title('Force Over Time')
plt.grid(True)
plt.legend()

# Augstuma grafiks
plt.subplot(3, 1, 3)
plt.plot(time, data['Height (m)'], label='Height', color='green')
plt.xlabel('Time (s)')
plt.ylabel('Height (m)')
plt.title('Height Over Time')
plt.grid(True)
plt.legend()

# Saglabā grafikus PDF failā
plt.tight_layout()
plt.savefig('Phone_Throw_Analysis.pdf')
print("Grafiki veiksmīgi saglabāti kā 'Phone_Throw_Analysis.pdf'.")
