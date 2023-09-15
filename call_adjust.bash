
python3 foobar18eq.py \
  -f "AKG K701" -f "Sennheiser IE 900 RX" -t "Sennheiser HD 800" -t "Audio-Technica ATH-W5000 2013" -t "AKG K812" -t "HIFIMAN HE1000 V2" \
  -r 9 -l 4

python3 foobar31geq.py \
  -f "AKG K701" -f "Sennheiser IE 900 RX" -t "Sennheiser HD 800" -t "Audio-Technica ATH-W5000 2013" -t "AKG K812" -t "HIFIMAN HE1000 V2" \
  -r 9 -l 4

python foobar31geq.py -f "AKG K701" -o AKGK701
python foobar31geq.py -f "Sennheiser HD 800" -o SnHD800
python foobar31geq.py -f "Audio-Technica ATH-W5000 2013" -o ATHW5000

python3 wavelet.py -f "Sennheiser HD 800" -o "wavelet_SnHD800"
python3 wavelet.py -f "Anker Soundcore Space Q45" -o "wavelet_AkrQ45"
python3 wavelet.py -f "Sennheiser IE 900" -o "wavelet_SnIE900"
python3 wavelet.py -f "Sennheiser IE 900 RX" -o "wavelet_SnIE900RX"
python3 wavelet.py -f "Meze 12 Classics" -o "wavelet_Mz12C"
python3 wavelet.py -f "Audio-Technica ATH-W5000 2013" -o "wavelet_ATHW5000n"
python3 wavelet.py -f "Audio-Technica ATH-W5000" -o "wavelet_ATHW5000"
python3 wavelet.py -f "Etymotic ER2XR" -o "wavelet_EtyER2XR"

python3 wavelet.py \
  -f "Sennheiser HD 800" \
  -f "Audio-Technica ATH-W5000 2013" \
  -f "Audio-Technica ATH-W5000" \
  -f "Anker Soundcore Space Q45" \
  -f "Sennheiser IE 900 RX" \
  -r 9 -r 5 \
  -l 4


