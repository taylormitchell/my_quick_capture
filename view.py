"CLI to captured content"
import sys, os, json
import argparse
from datetime import datetime
import pandas as pd
import capture

def print_sorted_captures(path):
    if os.path.exists(path):
        with open(path) as f: 
            capture = json.load(f)
    
    df = pd.DataFrame.from_dict(capture['items'])
    df['created_datetime'] = df['created'].apply(lambda x: datetime.fromtimestamp(x))
    df['created_date'] = df.created_datetime.dt.date
    
    def get_day_suffix(d):
        return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
    
    def strftime_day_suffix(dt, format="%B %d, %Y"):
        # Datetime to date string with day suffix 
        return dt.strftime(format.replace('%d', str(dt.day) + get_day_suffix(dt.day)))
    
    lines = []
    for date in reversed(sorted(df['created_date'].unique())):
        roam_date = strftime_day_suffix(date, "[[%B %d, %Y]]")
        lines.append(roam_date)
        for text in df.loc[df['created_date']==date, 'text']:
            lines.append(text)
        lines.append("-"*100)
        lines.append("")
        
    print("\n".join(lines))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='cli to captured content')
    parser.add_argument('--path', action='store', type=str,
        default="~/GoogleDrive/capture.json",
        help='filepath which captures are saved in')
    parser.add_argument('--reset', action='store_true',
        help='reset capture file after printing')
    args = parser.parse_args()

    path = os.path.expanduser(args.path)
    print_sorted_captures(path)

    if args.reset:
        capture.reset(path)

