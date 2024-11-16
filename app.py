from flask import Flask, request, jsonify
import numpy as np
import librosa
import os
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Directory to store uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Analyze the audio file: perform FFT and generate sentiment data
def analyze_audio(file_path):
    try:
        # Load audio file
        y, sr = librosa.load(file_path, sr=None)
        
        # Perform FFT analysis
        fft_data = np.abs(np.fft.fft(y))[:len(y)//2]
        fft_data = fft_data / np.max(fft_data)  # Normalize FFT data
        
        # Dummy sentiment analysis (replace with real ML model)
        sentiment = {
            "positive": np.random.randint(50, 100),
            "negative": np.random.randint(0, 50)
        }
        
        return fft_data.tolist(), sentiment
    except Exception as e:
        return None, {"error": f"Failed to process audio: {str(e)}"}

# Define API endpoint for audio analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    # Save uploaded file
    audio_file = request.files['audio']
    filename = secure_filename(audio_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audio_file.save(file_path)

    # Analyze the audio
    fft_data, sentiment = analyze_audio(file_path)
    if fft_data is None:
        return jsonify(sentiment), 500

    return jsonify({
        "fft": fft_data,
        "sentiment": sentiment
    })

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
