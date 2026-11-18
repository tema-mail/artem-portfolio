"""GPT Image через OpenRouter: python3 or_img.py <out.png> <prompt.txt> <img1> [img2 ...]"""
import sys, json, base64, io, ssl, urllib.request, pathlib, time
import certifi
from PIL import Image
CTX = ssl.create_default_context(cafile=certifi.where())
KEY = pathlib.Path('~/.claude/secrets/openrouter.key').expanduser().read_text().strip()
out, prompt, imgs = sys.argv[1], pathlib.Path(sys.argv[2]).read_text().strip(), sys.argv[3:]
def uri(p):
    im = Image.open(p).convert('RGB'); im.thumbnail((1280, 1280)); b = io.BytesIO(); im.save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
content = [{'type': 'text', 'text': prompt}] + [{'type': 'image_url', 'image_url': {'url': uri(p)}} for p in imgs]
body = {'model': 'openai/gpt-5.4-image-2', 'modalities': ['image', 'text'], 'image_config': {'aspect_ratio': '9:16'},
        'messages': [{'role': 'user', 'content': content}]}
req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=json.dumps(body).encode(),
                             headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
t = time.time(); j = json.loads(urllib.request.urlopen(req, timeout=600, context=CTX).read())
msg = j['choices'][0]['message']; ims = msg.get('images') or []
if not ims: print('нет картинки:', json.dumps(j)[:500]); sys.exit(1)
pathlib.Path(out).write_bytes(base64.b64decode(ims[0]['image_url']['url'].split(',', 1)[1]))
print(out, round(time.time() - t), 'с', 'usage', j.get('usage', {}).get('cost'))
