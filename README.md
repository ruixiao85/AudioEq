# AudioEq

## Data Source Preparation

https://github.com/jaakkopasanen/AutoEq

[Download Script](download.bash): only download the frequency response data from the repo mentioned above.

## Utility Scripts
[Call Adjustment Script](call_adjust.bash)

### Wavelet App
```bash
python3 foobar18eq.py \
  -f "AKG K701" -f "Sennheiser HD 800" \
  -t "AKG K812" -t "HIFIMAN HE1000 V2" \
  -r 9 -l 4
# list all the "from" & "to" targets, ratio=9: maximum adjustment, limit=4: 2^4=16, range (-16,+16) db

python3 wavelet.py -f "Sennheiser HD 800" -o "wavelet_SnHD800" -r 9 -r 6
# from one headphone to all others with 2 different adjustment ratios, and to a specific output directory
```

### Foobar2000 plugin: 18-band Equalizer

### Foobar2000 plugin: 31-band Graphic Equalizer
