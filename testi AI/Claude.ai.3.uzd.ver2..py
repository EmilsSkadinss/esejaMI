import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_and_process_data(file_path='Raw_Data.csv'):
    """
    Ielādē Raw_Data.csv failu un atgriež DataFrame ar paātrinājuma datiem
    
    Args:
        file_path (str): Ceļš līdz CSV failam (noklusējuma 'Raw_Data.csv')
    
    Returns:
        pd.DataFrame: Apstrādāti dati ar laika un paātrinājuma vērtībām
    """
    try:
        # Ielādējam CSV failu
        df = pd.read_csv(file_path)
        
        # Pārbaudam vai failā ir nepieciešamās kolonnas
        required_columns = ['Time', 'AccX', 'AccY', 'AccZ']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Failā trūkst kāda no nepieciešamajām kolonnām: {required_columns}")
        
        # Pārdēvējam kolonnas, lai tās atbilstu mūsu programmas prasībām
        df = df.rename(columns={
            'Time': 'time',
            'AccX': 'acceleration_x',
            'AccY': 'acceleration_y',
            'AccZ': 'acceleration_z'
        })
        
        # Aprēķinam kopējo paātrinājumu
        df['total_acceleration'] = np.sqrt(
            df['acceleration_x']**2 + 
            df['acceleration_y']**2 + 
            df['acceleration_z']**2
        )
        
        return df
        
    except FileNotFoundError:
        print(f"Kļūda: Fails '{file_path}' netika atrasts!")
        raise
    except Exception as e:
        print(f"Kļūda apstrādājot failu: {str(e)}")
        raise

def find_flight_period(df, threshold=2.0):
    """
    Atrod laika periodu, kurā telefons tika mests un lidoja
    
    Args:
        df (pd.DataFrame): Datu ietvars ar paātrinājuma datiem
        threshold (float): Paātrinājuma slieksnis lidojuma noteikšanai
    
    Returns:
        tuple: Sākuma un beigu indeksi lidojuma periodam
    """
    # Atrodam momentus, kur paātrinājums pārsniedz slieksni
    flight_mask = df['total_acceleration'] > threshold
    
    # Atrodam pirmo un pēdējo indeksu, kur notiek lidojums
    start_idx = flight_mask.idxmax()
    end_idx = len(df) - flight_mask[::-1].idxmax()
    
    return start_idx, end_idx

def calculate_metrics(df, mass=0.2):
    """
    Aprēķina spēku un augstumu no paātrinājuma datiem
    
    Args:
        df (pd.DataFrame): Datu ietvars ar paātrinājuma datiem
        mass (float): Telefona masa kilogramos
    
    Returns:
        DataFrame: DataFrame ar aprēķināto spēku un augstumu
    """
    # Aprēķinam spēku (F = ma)
    df['force'] = mass * df['total_acceleration']
    
    # Aprēķinam ātrumu, integrējot paātrinājumu
    df['velocity'] = np.zeros(len(df))
    for i in range(1, len(df)):
        dt = df['time'].iloc[i] - df['time'].iloc[i-1]
        df['velocity'].iloc[i] = df['velocity'].iloc[i-1] + df['total_acceleration'].iloc[i] * dt
    
    # Aprēķinam augstumu, integrējot ātrumu
    df['height'] = np.zeros(len(df))
    for i in range(1, len(df)):
        dt = df['time'].iloc[i] - df['time'].iloc[i-1]
        df['height'].iloc[i] = df['height'].iloc[i-1] + df['velocity'].iloc[i] * dt
    
    return df

def plot_metrics(df, output_file='flight_analysis.pdf'):
    """
    Izveido un saglabā grafikus PDF failā
    
    Args:
        df (pd.DataFrame): Datu ietvars ar visiem aprēķinātajiem parametriem
        output_file (str): Izvades PDF faila nosaukums
    """
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    
    # Paātrinājuma grafiks
    ax1.plot(df['time'], df['total_acceleration'])
    ax1.set_title('Paātrinājums laikā')
    ax1.set_xlabel('Laiks (s)')
    ax1.set_ylabel('Paātrinājums (m/s²)')
    ax1.grid(True)
    
    # Spēka grafiks
    ax2.plot(df['time'], df['force'])
    ax2.set_title('Spēks laikā')
    ax2.set_xlabel('Laiks (s)')
    ax2.set_ylabel('Spēks (N)')
    ax2.grid(True)
    
    # Augstuma grafiks
    ax3.plot(df['time'], df['height'])
    ax3.set_title('Augstums laikā')
    ax3.set_xlabel('Laiks (s)')
    ax3.set_ylabel('Augstums (m)')
    ax3.grid(True)
    
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def main():
    try:
        # Ielādējam datus
        df = load_and_process_data()
        
        # Atrodam lidojuma periodu
        start_idx, end_idx = find_flight_period(df)
        
        # Izgriežam tikai lidojuma datus
        flight_data = df.iloc[start_idx:end_idx].copy()
        
        # Aprēķinam papildu metriku
        flight_data = calculate_metrics(flight_data)
        
        # Zīmējam un saglabājam grafikus
        plot_metrics(flight_data)
        
        print("Programma veiksmīgi pabeigta! Grafiki saglabāti 'flight_analysis.pdf' failā.")
        
    except Exception as e:
        print(f"Programmas izpildes laikā radās kļūda: {str(e)}")

if __name__ == "__main__":
    main()