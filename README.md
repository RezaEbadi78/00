# Crypto Market Volume Spike Detector

A real-time Flask web application that analyzes BTC/USDT trade data from Binance WebSocket to detect volume spikes.

## Features

- **Real-time Data Streaming**: Connects to Binance WebSocket API to stream live BTC/USDT trade data
- **Volume Spike Detection**: Monitors trade volume and detects spikes that are 10x greater than the moving average
- **Background Processing**: Analysis runs in a separate thread to avoid blocking the web server
- **REST API**: Single endpoint `/api/get_signal` to retrieve the latest detected spike

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python app.py
```

2. The application will:
   - Start a Flask web server on `http://localhost:5000`
   - Connect to Binance WebSocket in a background thread
   - Begin monitoring BTC/USDT trades for volume spikes

3. Access the API endpoint:
   - **URL**: `http://localhost:5000/api/get_signal`
   - **Method**: GET
   - **Response**: JSON with spike details or status message

## API Response Examples

### When a spike is detected:
```json
{
  "signal_type": "VolumeSpike",
  "price": 67500.50,
  "volume": 15.34,
  "timestamp": "2025-07-30T17:20:05Z"
}
```

### When no spike has been detected yet:
```json
{
  "status": "Awaiting first signal..."
}
```

## How It Works

1. **Data Collection**: The application maintains a rolling window of the last 200 trades
2. **Moving Average**: Calculates the average volume from the trade history
3. **Spike Detection**: A volume spike is detected when a single trade's volume is 10x greater than the current moving average
4. **Signal Storage**: Only the most recent spike is stored globally
5. **API Access**: The `/api/get_signal` endpoint provides access to the latest spike data

## Technical Details

- **WebSocket URL**: `wss://stream.binance.com:9443/ws`
- **Trade Stream**: `btcusdt@trade`
- **Moving Average Window**: Last 200 trades
- **Spike Threshold**: 10x the moving average volume
- **Threading**: WebSocket connection runs in a daemon thread

## Error Handling

- Automatic WebSocket reconnection on connection failures
- Graceful error handling for malformed messages
- Thread-safe global variable access