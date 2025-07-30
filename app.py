import json
import threading
import time
from datetime import datetime
from typing import Optional, Dict, Any

import websocket
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Global variables to store the latest volume spike
latest_spike: Optional[Dict[str, Any]] = None
trade_history = []
MAX_TRADES = 200

def on_message(ws, message):
    """Handle incoming WebSocket messages from Binance"""
    global latest_spike, trade_history
    
    try:
        data = json.loads(message)
        
        # Extract trade data
        if 'data' in data:
            trade = data['data']
            price = float(trade['p'])  # price
            volume = float(trade['q'])  # quantity/volume
            timestamp = int(trade['T'])  # trade time
            
            # Add to trade history
            trade_history.append({
                'price': price,
                'volume': volume,
                'timestamp': timestamp
            })
            
            # Keep only the last 200 trades
            if len(trade_history) > MAX_TRADES:
                trade_history.pop(0)
            
            # Calculate moving average volume
            if len(trade_history) >= 10:  # Need at least 10 trades for meaningful average
                avg_volume = sum(t['volume'] for t in trade_history) / len(trade_history)
                
                # Check for volume spike (10x greater than average)
                if volume > avg_volume * 10:
                    # Store the spike details
                    latest_spike = {
                        'signal_type': 'VolumeSpike',
                        'price': price,
                        'volume': volume,
                        'timestamp': datetime.fromtimestamp(timestamp / 1000).isoformat() + 'Z'
                    }
                    print(f"Volume spike detected! Price: {price}, Volume: {volume}, Avg: {avg_volume}")
    
    except Exception as e:
        print(f"Error processing message: {e}")

def on_error(ws, error):
    """Handle WebSocket errors"""
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    """Handle WebSocket connection close"""
    print("WebSocket connection closed")

def on_open(ws):
    """Handle WebSocket connection open"""
    print("WebSocket connection opened")
    # Subscribe to BTC/USDT trade stream
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": ["btcusdt@trade"],
        "id": 1
    }
    ws.send(json.dumps(subscribe_message))

def start_websocket():
    """Start the WebSocket connection in a separate thread"""
    websocket_url = "wss://stream.binance.com:9443/ws"
    
    while True:
        try:
            ws = websocket.WebSocketApp(
                websocket_url,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.run_forever()
        except Exception as e:
            print(f"WebSocket connection failed: {e}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)

@app.route('/api/get_signal', methods=['GET'])
def get_signal():
    """API endpoint to get the latest volume spike signal"""
    global latest_spike
    
    if latest_spike is None:
        return jsonify({
            "status": "Awaiting first signal..."
        })
    
    return jsonify(latest_spike)

if __name__ == '__main__':
    # Start WebSocket connection in background thread
    websocket_thread = threading.Thread(target=start_websocket, daemon=True)
    websocket_thread.start()
    
    # Start Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)