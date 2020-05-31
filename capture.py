import os
import json
import time
import sys

def capture(title, text, url, path="~/capture.json"):
    # Load existing captures
    path = os.path.expanduser(path)
    if os.path.exists(path):
        with open(path) as f:
            capture = json.load(f)
    else:
        capture = {'items': []}

    # Add capture
    item = {
        'title':title,
        'text':text,
        'url':url,
        'created': int(time.time())
    }
    capture['items'].append(item)
    with open(path, 'w+') as f:
        json.dump(capture, f, indent=4)

def reset(path):
    with open(path, 'w+') as f:
        json.dump({'items': []}, f, indent=4)

if __name__=="__main__":
    path = os.path.expanduser("~/GoogleDrive/capture.json")
    title, text, url = sys.argv[1:4]
    capture(title, text, url, path)
