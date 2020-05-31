import sys, os, json
import pandas as pd
from datetime import datetime

def main(path):
    if os.path.exists(path):
        with open(path) as f: 
            capture = json.load(f)
    
    df = pd.DataFrame.from_dict(capture['items'])
    df['created_dt'] = df['created'].apply(lambda x: datetime.fromtimestamp(x))
    
    has_text = df.text!=''
    is_tweet = df.url.str.startswith('https://twitter.com')
    
    df.loc[has_text, 'type'] = 'QUOTE'
    df.loc[is_tweet&(~has_text), 'type'] = 'TWEET'
    df.loc[(~is_tweet)&(~has_text), 'type'] = 'PAGE'
    
    df['date'] = df.created_dt.dt.date
    df['time'] = df.created_dt.dt.strftime("%H:00")
    
    df.loc[df['type']=='QUOTE', 'block'] = df['text'] + ' #Quote ' + df['url'].apply(lambda x: f"[source]({x})")
    df.loc[df['type']=='TWEET', 'block'] = df['title'] + ' #Quote ' + df['url'].apply(lambda x: f"[source]({x})")
    df.loc[df['type']=='PAGE', 'block'] = df['title'].apply(lambda x: f"[{x}]") + df['url'].apply(lambda x: f"({x})")
    
    def get_day_suffix(d):
        return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
    
    def strftime_day_suffix(dt, format="%B %d, %Y"):
        # Datetime to date string with day suffix 
        return dt.strftime(format.replace('%d', str(dt.day) + get_day_suffix(dt.day)))
    
    lines = []
    for date in reversed(sorted(df['date'].unique())):
        roam_date = strftime_day_suffix(date, "[[%B %d, %Y]]")
        lines.append(roam_date)
        for block in df.loc[df['date']==date, 'block']:
            lines.append(f"- {block}")
        lines.append("-"*100)
        lines.append("")
        
    print("\n".join(lines))

if __name__=="__main__":
    path = os.path.expanduser('~/GoogleDrive/capture.json')
    main(path)
