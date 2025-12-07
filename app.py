from flask import Flask, request, send_file, jsonify
import os
import subprocess
import uuid
import base64

app = Flask(__name__)
TEMP_DIR = '/tmp'

@app.route('/base64-to-pptx', methods=['POST'])
def convert_base64():
    pdf_path = None
    pptx_path = None
    try:
        data = request.get_json()
        if not data or 'base64' not in data:
            return jsonify({"error": "No base64 data found"}), 400

        unique_id = str(uuid.uuid4())
        pdf_path = os.path.join(TEMP_DIR, f"{unique_id}.pdf")
        pptx_path = os.path.join(TEMP_DIR, f"{unique_id}.pptx")

        # Base64 ni PDF ga aylantiramiz
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(base64.b64decode(data['base64']))

        # Konvertatsiya (pdf2pptx)
        command = f"pdf2pptx '{pdf_path}' -o '{pptx_path}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({"error": "Conversion failed", "details": result.stderr}), 500

        return send_file(
            pptx_path, 
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            as_attachment=True, 
            download_name='converted.pptx'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)
        # PPTX fayl avtomatik tozalanadi (Docker restartda /tmp tozalanadi)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
