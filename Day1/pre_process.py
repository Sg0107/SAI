
import pandas as pd
import numpy as np
from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(1, 100))

def pre_processing(pnl_path, indicators_path, sequence_length):
    def get_candles(df, time, num_candles):
        return df[df['timestamp'] < time].tail(num_candles)

    pnl_data = pd.read_csv(pnl_path)
    indicators_data = pd.read_csv(indicators_path)
    indicators_data = indicators_data.drop(columns='rsi')
    indicators_data = indicators_data.drop(columns='volume').iloc[:, 1:]  # Drop 'volume' and first column
    pnl_data['Buy Time'] = pd.to_datetime(pnl_data['Buy Time'])
    indicators_data['timestamp'] = pd.to_datetime(indicators_data['timestamp'])

    buy_sequences = []
    attention_masks = []
    targets = []

    for _, row in pnl_data.iterrows():
        buy_time = row['Buy Time']
        target = row['Reason']
        buy_seq = get_candles(indicators_data, buy_time, sequence_length)

        if len(buy_seq) == sequence_length:
            # Drop the timestamp column
            buy_seq_values = buy_seq.drop(columns='timestamp').values
            buy_seq_values = min_max_scaler.fit_transform(buy_seq_values)
            # Flatten the scaled sequence and append to buy_sequences
            buy_sequences.append(buy_seq_values.flatten())  # Flatten the sequence into a 1D array

            # Create attention masks: 1 for each token in the sequence
            attention_mask = [1] * len(buy_seq_values.flatten())
            attention_masks.append(attention_mask)
            targets.append(target)

    buy_sequences = np.array(buy_sequences)  # Shape: (num_samples, sequence_length * num_features)
    attention_masks = np.array(attention_masks)  # Shape: (num_samples, sequence_length * num_features)
    targets = np.array(targets)  # Shape: (num_samples,)

    return buy_sequences.astype(np.int32), attention_masks.astype(np.int32), targets.astype(np.int32)
