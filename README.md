<div align="center">

[![SMFS](https://raw.githubusercontent.com/suchencjusz/steam_market_float_sniper/main/.github/sniperlogo.png)](#readme)

Find float, seed value in the steam market - inspired by [CSGO-Market-Float-Finder](https://github.com/adamb70/CSGO-Market-Float-Finder)

</div>

The main purpose of the program is to collect data from the steam market and serialize it to simple .csv file

## To do:

 - [x] Gather data from steam
 - [x] Gather float and pattern data (with csgofloat api)
 - [ ] **Operate the program with cli**
 - [ ] One-Click buy link
 - [ ] Monitor market for desired float/pattern
 - [ ] Notify of the desired float/pattern
 - [ ] Auto item buying

# Installation:

Requirements:
 - git (Or you can download the zip file)
 - Python (On 3.10.4 - works fine)

Open your terminal, and execute the following commands
```
git clone https://github.com/suchencjusz/steam_market_float_sniper
cd steam_market_float_sniper
```

Install needed packages
```
pip install -r requirements.txt
```

# Ussage:

```
python3 main.py -h
```

Example request
```
python3.10 main.py -l https://steamcommunity.com/market/listings/730/AWP%20%7C%20Electric%20Hive%20%28Field-Tested%29 -c PLN -o hive
```

The collected data will be saved in a csv file
[![SMFS-csv-file](https://raw.githubusercontent.com/suchencjusz/steam_market_float_sniper/main/.github/csv_file.png)]