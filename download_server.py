import re
import requests
from flask import Flask, request, Response, stream_with_context

app = Flask(__name__)

# आपकी वेबसाइट का असली डोमेन नाम
MY_WEBSITE_NAME = "Omnimodstore.com"

@app.route('/secure-download')
def secure_download():
    target_url = request.args.get('url')
    app_name = request.args.get('name', 'App')
    
    if not target_url:
        return "फाइल का यूआरएल गायब है!", 400

    try:
        # थर्ड-पार्टी सर्ver से फाइल को स्ट्रीम मोड में रिक्वेस्ट करना
        req = requests.get(target_url, stream=True, timeout=30)
        
        # फाइल का साफ़-सुथरा नाम तैयार करना (जैसे: Omnimodstore.com-Insta-Pro.apk)
        clean_name = re.sub(r'[^a-zA-Z0-9\.\-_]', '', app_name.replace(' ', '-'))
        if not clean_name.endswith('.apk'):
            clean_name += '.apk'
            
        custom_filename = f"{MY_WEBSITE_NAME}-{clean_name}"

        # ब्राउज़र को मजबूर करने के लिए Headers सेट करना
        headers = {
            'Content-Disposition': f'attachment; filename="{custom_filename}"',
            'Content-Type': req.headers.get('Content-Type', 'application/vnd.android.package-archive'),
            'Content-Length': req.headers.get('Content-Length')
        }

        def generate():
            for chunk in req.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk

        return Response(stream_with_context(generate()), headers=headers, status=req.status_code)

    except Exception as e:
        return f"डाउनलोड सर्वर में समस्या: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
  
