import pandas as pd
import numpy as np

from Preprosessing.dataloader import loader
from Preprosessing.cleaning import cleaner

'''renaming my functions'''
dataloading = loader()
cleaning = cleaner()

'''loading the data'''
data = dataloading.rawdata()
gemeenten = dataloading.gemeentes()
pop_density = dataloading.population_dens()
postcodes = dataloading.postcodes()

'''clean the data'''
clean_data = cleaning.rawcleaner(data)
clean_gemeenten = cleaning.gemeentecleaner(gemeenten)
clean_pop_density = cleaning.pop_dens_cleaner(pop_density)
clean_postcodes = cleaning.postcodecleaner(postcodes)

'''merging tables'''
popdensinfo = pd.merge(clean_postcodes, clean_pop_density, on=['Postcode'],how='left')
big_info = pd.merge(popdensinfo, clean_gemeenten, on=['Gemeentecode'], how='left')
final_data = pd.merge(clean_data, big_info, on=["Postcode"], how='left')

final_data.to_csv('visualisationdata')


