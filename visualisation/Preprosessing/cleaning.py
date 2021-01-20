import pandas as pd
import numpy as np

class cleaner(object):

    def __init__(self):
        pass

    def rawcleaner(self, data):
        '''removing the NULL values from koopprijs & setting it to numeric '''
        data.loc[data['koopPrijs'] == 'NULL', 'koopPrijs'] = 0
        data['koopPrijs'] = pd.to_numeric(data['koopPrijs'])

        '''removing the NaN values from energielabelklasse '''
        data.loc[data['energielabelKlasse'] == 'NaN', 'energielabelKlasse'] = 0

        ''' read date format as years-month-days'''
        data["publicatieDatum"] = pd.to_datetime(data["publicatieDatum"], format="%Y-%m-%d")
        data["datum_ondertekening"] = pd.to_datetime(data["datum_ondertekening"], format="%Y-%m-%d")

        '''setting soortwoning to string and remove special characters'''
        data["soortWoning"] = data["soortWoning"].astype('str')
#        data["soortWoning"] = data["soortWoning"].replaceAll("[-+.^:,<>{}]", "");

        ''' creating column selltime '''
        data["listed_time"] = (data["datum_ondertekening"] - data["publicatieDatum"]).abs()

        '''creating column price per m2'''
        data["price_per_m2"] = (data["koopPrijs"] / data["oppervlakte"])

        '''Removes the two letters at the end of the postcodes. 
        When this step is not taken, the one hot encoding step creates an extreme amount of columns in the df'''
        data.loc[:, "postcode"] = data.postcode.str[0:4]
        data.loc[:, "postcode"] = data.loc[:, "postcode"].astype("float64")
        data["postcode"] = data.postcode.astype("category")

        '''only take the year from the bouwjaar, and change it to numeric'''
        data.loc[:, "bouwjaar"] = data.bouwjaar.str[-4:]
        data.loc[:, "bouwjaar"] = data.loc[:, "bouwjaar"].astype("int")

        ''' function that removes NA values from listed_time (none)'''
        data = data.dropna(subset=["listed_time"])

        ''' Removing some columns that are unnecessary for the heatmap'''
        to_drop1 = ["globalId", "globalId.1", "volledigeOmschrijving", "datum_ondertekening", "publicatieDatum", "kantoor_naam_MD5hash",
                      "categorieObject"] # "soortWoning", , "postcode"
        data.drop(columns=to_drop1, inplace=True)

        data = data.rename(columns={'postcode': 'Postcode'})

        data['energielabelKlasse'] = pd.get_dummies(data['energielabelKlasse'], drop_first=True)

        '''transforming columns into float64 values for correlation testing'''
        data['energielabelKlasse'] = data['energielabelKlasse'].astype(np.float64)

        ''' changing listed time to numeric days for correlation testing'''
        data['listed_time'] = data['listed_time'].astype('timedelta64[D]').astype('int')

        '''dropping all rows with na values in any column '''
        clean_data = data.dropna()

        return clean_data

    def gemeentecleaner(self, gemeenten):
        to_drop = ["GemeentecodeGM", "Provinciecode", "ProvinciecodePV"]
        gemeenten_clean = gemeenten.drop(columns=to_drop)
        return gemeenten_clean

    def pop_dens_cleaner(self, pop_density):
        to_drop2 = ["ID", "Geslacht", "Leeftijd", "Perioden"]
        clean_pop_dens = pop_density.drop(columns=to_drop2)
        clean_pop_dens = clean_pop_dens.rename(columns={'Bevolking_1': 'population_density'})
        clean_pop_dens["Postcode"] = clean_pop_dens.Postcode.astype("category")
        return clean_pop_dens

    def postcodecleaner(self, postcodes):
        to_drop3 = ["Huisnummer", "Buurt2018", "Wijk2018"]
        clean_postcodes = postcodes.drop(columns=to_drop3)
        clean_postcodes = clean_postcodes.rename(columns={'Gemeente2018': 'Gemeentecode'})
        clean_postcodes = clean_postcodes.rename(columns={'PC6': 'Postcode'})
        clean_postcodes.loc[:, "Postcode"] = clean_postcodes.Postcode.str[0:4]
        clean_postcodes.loc[:, "Postcode"] = clean_postcodes.loc[:, "Postcode"].astype("float64")
#        clean_postcodes.loc[:, "Postcode"] = clean_postcodes.loc[:, "Postcode"].astype("float64")
        clean_postcodes["Postcode"] = clean_postcodes.Postcode.astype("category")
        clean_postcodes["Gemeentecode"] = clean_postcodes.Gemeentecode.astype("category")

        return clean_postcodes


