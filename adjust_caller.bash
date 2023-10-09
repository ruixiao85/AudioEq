
python adjust_foobar18eq.py \
  -f "AKG K701" -f "Sennheiser IE 900 RX" -t "Sennheiser HD 800" -t "Audio-Technica ATH-W5000 2013" -t "AKG K812" -t "HIFIMAN HE1000 V2" \
  -r 9 -l 4

python adjust_foobar31geq.py \
  -f "AKG K701" -f "Sennheiser IE 900 RX" -t "Sennheiser HD 800" -t "Audio-Technica ATH-W5000 2013" -t "AKG K812" -t "HIFIMAN HE1000 V2" \
  -r 9 -l 4

python adjust_foobar31geq.py -f "AKG K701" -o AKGK701
python adjust_foobar31geq.py -f "Sennheiser HD 800" -o SnHD800
python adjust_foobar31geq.py -f "Sennheiser HD 580" -f "Sennheiser HD 580 precision" -o SnHD580
python adjust_foobar31geq.py -f "Audio-Technica ATH-W5000 2013" -o ATHW5000

python adjust_wavelet.py -f "Audio-Technica ATH-W5000 2013" -o "ATHW5000n"
python adjust_wavelet.py -f "Sennheiser HD 800" -o "SnHD800"
python adjust_wavelet.py -f "Anker Soundcore Space Q45" -o "AkrQ45"
python adjust_wavelet.py -f "Etymotic ER2XR" -o "EtyER2XR"
python adjust_wavelet.py -f "BLON BL-03" -o "TinT4BL3"
python adjust_wavelet.py \
  -f "Sennheiser HD 800" \
  -f "Audio-Technica ATH-W5000 2013" \
  -f "Audio-Technica ATH-W5000" \
  -f "Anker Soundcore Space Q45" \
  -f "Sennheiser IE 900 RX" \
  -r 9 -r 5 \
  -l 4

python adjust_foobar31geq.py -f "7Hz Timeless" -f "Etymotic ER2XR" -f "Final Audio E5000 AE" -f "Sennheiser IE 900 AE" -f "Sensaphonics 2X-S Bass" -f "Tin HiFi T4" -f "AKG K701" -f "Anker Soundcore Life Q45 (Wired)" -f "Audio-Technica ATH-W5000" -f "Sennheiser HD 580" -f "Sennheiser HD 800"

python adjust_wavelet.py -f "7Hz Timeless" -f "Etymotic ER2XR" -f "Final Audio E5000 AE" -f "Sennheiser IE 900 AE" -f "Sensaphonics 2X-S Bass" -f "Tin HiFi T4" -f "AKG K701" -f "Anker Soundcore Life Q45 (Wired)" -f "Audio-Technica ATH-W5000" -f "Sennheiser HD 580" -f "Sennheiser HD 800"



