#!/bin/env python
from pathlib import Path
import os
limit=12; ratios=[0.6,0.9] # with limit and scaling
# limit=99; ratios=[1.0] # raw conversion

pretext="GraphicEQ: "
bands=[20, 21, 22, 23, 24, 26, 27, 29, 30, 32, 34, 36, 38, 40, 43, 45, 48, 50, 53, 56, 59, 63, 66, 70, 74, 78, 83, 87, 92, 97, 103, 109, 115, 121, 128, 136, 143, 151, 160, 169, 178, 188, 199, 210, 222, 235, 248, 262, 277, 292, 309, 326, 345, 364, 385, 406, 429, 453, 479, 506, 534, 565, 596, 630, 665, 703, 743, 784, 829, 875, 924, 977, 1032, 1090, 1151, 1216, 1284, 1357, 1433, 1514, 1599, 1689, 1784, 1885, 1991, 2103, 2221, 2347, 2479, 2618, 2766, 2921, 3086, 3260, 3443, 3637, 3842, 4058, 4287, 4528, 4783, 5052, 5337, 5637, 5955, 6290, 6644, 7018, 7414, 7831, 8272, 8738, 9230, 9749, 10298, 10878, 11490, 12137, 12821, 13543, 14305, 15110, 15961, 16860, 17809, 18812, 19871]
nband=len(bands)

def parse_integer(value: str, default: int=0) -> int:
  try:
    return round(float(value),0)
  except ValueError:
    return default

def band_left(folder: str, ext: str=".csv")-> []:
  files=[f for f in os.listdir(folder) if f.endswith(ext)]
  print(files[0])
  with open(folder+os.path.sep+files[0]) as f:
    ad=[0]*len(bands) # adjustment list
    lf,lv=0,0 # last frequency (Hz), last value (dB)
    bi=0 # band index
    for line in f:
      cols=line.split(',')
      cf=parse_integer(cols[0]) # current frequency
      cv=parse_integer(cols[1]) # current value
      if lf<=bands[bi]<cf:
        # print(f'{line}\tfreq{cf}\tval{cv}')
        ad[bi]=lv; bi+=1
      if bi>=len(bands):
        break
      lf=cf; lv=cv
  return ad

get_freq_resp=band_left

def clean_name(file: str)-> str:
  return file.replace("-","").replace(" ","").lower()


# myHps,myHpType=["Sennheiser HD 800"],"onear"
myHps,myHpType=["Audio-Technica ATH-W5000 2013", "Sennheiser HD 600", "Sennheiser HD 800","AKG K701"],"onear"
# myHps,myHpType=["Audio-Technica ATH-W5000","Audio-Technica ATH-W5000 2013","Sennheiser HD 600", "Sennheiser HD 800","AKG K701"],"onear"
myBrands=["Abyss","Audio-Technica","Audeze"]
# myBrands=["AKG","Denon","Focal","Fostex","HiFiMAN","Meze","Sennheiser","Sony","ZMF"]
# myBrands=["Abyss","Audio-Technica","Audeze","AKG","Beyerdynamic","Dan","Denon","E-Mu","Focal","Fostex","Grado","HiFiMAN","Meze","MrSpeakers","Philips","Pioneer","Sennheiser","Sony","Stax","Ultrasone","Yamaha","ZMF"]

# myHps,myHpType=["Etymotic ER2XR"],"inear"
# myHps,myHpType=["Etymotic ER2XR","Sennheiser IE 900","BLON BL-03"],"inear"
# myBrands=["64", "7Hz", "Audio-Technica","Audeze","AKG","Beyerdynamic","Bose","Bowers","Campfire","Denon","E-Mu","Etymotic","Focal","Fiio", "Final","Fostex","Grado","HiFiMAN", "KZ", "Massdrop","Meze","Monoprice","Monster","Moondrop", "MrSpeakers","Oppo","Pioneer","Polk","Sennheiser","Shure","Sony","Stax","Tin", "ThieAudio", "Ultrasone","ZMF"]

myHpsClean=[clean_name(hp) for hp in myHps]

myBrandsClean=[clean_name(b) for b in myBrands]
subDir="AutoEq/measurements"
outDir="out_wavelet"
try: os.mkdir(outDir)
except OSError as e: pass
for sourceDir in ["headphonecom", "innerfidelity", "oratory1990"]:
  for typeDir in ["inear","onear","earbud"]:
    for dirpath,dirnames,filenames in os.walk(f"{subDir}/{sourceDir}/data/{typeDir}"):
      hpsFoundClean=[clean_name(hp) for hp in dirnames]
      for hpc in myHps:
        if clean_name(hpc) in hpsFoundClean:
          fc=get_freq_resp(f"{subDir}/{sourceDir}/data/{typeDir}/{hpc}")
          # print(fc)
          for hpt in dirnames:
            if clean_name(hpt.split(" ")[0]) in myBrandsClean:
              ft=get_freq_resp(f"{subDir}/{sourceDir}/data/{typeDir}/{hpt}")
              for ratio in ratios:
                with open(f'{outDir}/{hpc}-{hpt}~{round(ratio*10)}~{sourceDir[:4]}.txt'.replace(" ",""),"w") as f:
                  f.write(pretext)
                  adjs=[(b-a)*ratio for a,b in zip(fc,ft)]
                  mean=max(-1*limit,min(limit,sum(adjs)/len(adjs)))
                  for band,adj in zip(bands,adjs):
                    f.write(f"{band} {round(max(-1*limit,min(limit,adj-mean)),2)}; ")
                #exit()
