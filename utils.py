import static

def displayAllCurrencies():
    print("Currencies: ")

    for idx, key in enumerate(static.CURRENCY.items()):
        if idx % 3 == 0:
            print("")
        print(key[0], end="\t")
    print("\n")
    exit()

def SaveDataToCSV(data, filename):

    if filename == "None":
        filename = "data.csv"

    if filename.endswith != ".csv":
        filename = filename + ".csv"

    with open(filename, 'w') as f:
        f.write("Price\tFloat\tSeed\tListingID\tAssetID\tJSLink\n")
        for i in data:
            f.write(str(i["item_price"]) + "\t" + str(i["float_value"]) + "\t" + str(i["pattern_id"]) + "\t" + str(
                i["listing_id"]) + "\t" + str(i["asset_id"]) + "\t" + str(i["js_link"])+"\n")
        f.close()