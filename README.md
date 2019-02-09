# Benchmark PyMagnitude
This project is created to test the difference before and after the patch for `pymagnitude==0.1.120`.

## Install
```
virtualenv -p python3 .envrc
source .envrc/bin/activate
pip install -r requirements.txt
```

## Patch `pymagnitude`
```
./patch_pymagnitude.sh
```

## Reverse patch `pymagnitude`
```
./patch_pymagnitude.sh -R
```

## Run help
```
python main.py -h
```

## Compare vectors before and after the patch
```
./compare.sh medium_words.txt
```
