#!/usr/bin/env python
import argparse
parser = argparse.ArgumentParser("Process something")
parser.add_argument("-d", "--directory", default="db", type=str, help="input directory to analyze from")
parser.add_argument("-i", "--input", default="freq_.*\.log", type=str, help="input regex pattern to analyze from")
args=parser.parse_args()
print(args)
import os, sys, re
import pandas as pd
import math
import statistics

for f in os.listdir(args.directory):
  if bool(re.search(args.input, f)):
    hp=os.path.splitext(f)[0]
    print(f"Processing {hp}")
    with open(f"{args.directory}/{f}", 'r') as fr:
      flns=fr.readlines()
    df=None
    cf=None; ls=None
    for ln in flns:
      lv=ln.split(' [INFO] ')[-1].replace('\n','') # line value
      if lv.startswith('-'):
        v=float(lv.lstrip('-').rstrip('\n').split(' ')[-1])
        ls.append(v)
      else:
        if cf is not None:
          # print(cf, sum(ls)/len(ls))
          # _df=pd.DataFrame.from_dict({'freq': [cf], 'resp': [10.0*math.log(sum(ls)/len(ls), 10.0)]})
          _df=pd.DataFrame.from_dict({'freq': [cf], 'resp': [10.0*math.log(statistics.median(ls), 10.0)]})
          if df is None:
            df=_df
          else:
            df=pd.concat([df,_df])
        cf=float(lv.rstrip(':'))
        ls=[]
    df.resp=df.resp-df.resp[df.freq==1008.44]
    df.to_csv(f"{args.directory}/{hp}.csv", index=False)
    import plotly.express as px
    fig=px.scatter(x=df.freq, y=df.resp, log_x=True)
    fig.write_html(f"{args.directory}/{hp}.html")



