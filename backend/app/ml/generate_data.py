import pandas as pd
import numpy as np
import random

def generate_synthetic_data(num_samples=3000):
    """
    Generates a synthetic dataset for credit card fraud detection.
    
    Args:
        num_samples (int): Number of transactions to generate.
        
    Returns:
        pd.DataFrame: The generated dataset.
    """
    np.random.seed(42)  # For reproducibility
    random.seed(42)

    # 1. Feature Generation
    
    # Amount: Skewed distribution. legitimate mostly small, fraud often large.
    # We'll use a log-normal distribution for base amounts.
    amounts = np.random.lognormal(mean=3.0, sigma=1.0, size=num_samples)
    amounts = np.round(amounts, 2)

    # Time: 0-23 (Hour of day)
    # Uniform for now, maybe slight peak in day for legit.
    times = np.random.randint(0, 24, size=num_samples)

    # Categories
    categories_list = ['groceries', 'electronics', 'utilities', 'entertainment', 'travel', 'dining', 'gas']
    categories = np.random.choice(categories_list, size=num_samples)

    # Age: 18 - 90
    ages = np.random.randint(18, 91, size=num_samples)

    # Locations
    locations_list = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    locations = np.random.choice(locations_list, size=num_samples)
    
    # Previous Transactions: Count of previous transactions
    # Legit users usually have history. Fraudsters might use fresh accounts or stolen cards quickly.
    previous_trans = np.random.poisson(lam=20, size=num_samples)

    # 2. Fraud Logic (Target variable generation)
    # Binary Classification: Legitimate = 0, Fraud = 1
    
    is_fraud = []
    
    for i in range(num_samples):
        fraud_prob = 0.01 # Base fraud probability (1%)
        
        # Condition 1: High Amount increases risk
        if amounts[i] > 200:
            fraud_prob += 0.3
        if amounts[i] > 1000:
            fraud_prob += 0.5
            
        # Condition 2: Late Night Transactions (0 - 4 AM)
        if 0 <= times[i] <= 4:
            fraud_prob += 0.2
            
        # Condition 3: Low Previous Transactions
        if previous_trans[i] < 5:
            fraud_prob += 0.3
            
        # Condition 4: Category Risk
        if categories[i] in ['electronics', 'jewelry', 'travel']: # Added jewelry implicitly for logic, but keeping to gen list
             fraud_prob += 0.1
        
        # Random Noise / randomness
        # We cap probability at 0.95 to avoid guaranteed fraud
        fraud_prob = min(fraud_prob, 0.95)
        
        # Determine label based on probability
        is_fraud.append(1 if np.random.rand() < fraud_prob else 0)

    # Create DataFrame
    df = pd.DataFrame({
        'amount': amounts,
        'time': times,
        'category': categories,
        'age': ages,
        'location': locations,
        'previous_trans': previous_trans,
        'is_fraud': is_fraud
    })

    return df

if __name__ == "__main__":
    df = generate_synthetic_data(3000)
    
    # Save to CSV in the root directory
    output_path = r"c:\Users\vansh\Downloads\Fraud_Detection\credit_card_fraud.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✅ Synthetic data generated with {len(df)} samples.")
    print(f"💾 Saved to: {output_path}")
    print("\n🔍 Class Distribution:")
    print(df['is_fraud'].value_counts(normalize=True))
    print("\n🔍 Data Preview:")
    print(df.head())
