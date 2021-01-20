import pandas as pd

class loader(object):

    def __init__(self):
        pass

    def rawdata(self):
        return pd.read_csv('/Users/kevinseegers/Desktop/Master /housing_data.csv', delimiter=',')

    def gemeentes(self):
        return pd.read_csv("//Users/kevinseegers/Desktop/Master /database management/Funda CBS tables/Gemeenten alfabetisch 2020.csv", delimiter=";")

    def population_dens(self):
        return pd.read_csv("//Users/kevinseegers/Desktop/Master /database management/Funda CBS tables/Bevolkingsdichtheid_CBS.csv", delimiter=";")

    def postcodes(self):
        return pd.read_csv("/Users/kevinseegers/Desktop/Master /database management/Funda CBS tables/CBS-postcode-gemeenten.csv", delimiter=";")




