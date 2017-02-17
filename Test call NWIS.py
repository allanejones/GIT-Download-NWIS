# as a test I want to see if the BeautifulSoup documentation I wrote
# for the USGS gages works on Python 2.7.8

import re
import os
from Download_NWIS_v2py import download_NWIS_data

# setting up the file pathways to save the document
file_directory = 'C:\\Users\\geo-aej662\\Desktop\\'

# creating a test dictionary of the usgs site information
Site_info = {'SiteNum': '08189700',
        # site number forDeschutes River gage       
        'State': 'TX',
        # US state postal code
        'begin': '2015-11-07', 
        # earliest date you want to obtain data for - 'yyyy-mm-dd'
        'ender': '2015-11-12', 
        # earliest date you want to obtain data for - 'yyyy-mm-dd'
        'Folder': 'TestUSGS_downloads',
        # folder name to be created for file saving
        'FilePath': file_directory}
        # directory where to save data

# checking the import of download_NWIS_data
bad_sites = download_NWIS_data(site_number    = Site_info['SiteNum'],
                               US_state       = Site_info['State'],
                               begin_date     = Site_info['begin'],
                               end_date       = Site_info['ender'],
                               folder_name    = Site_info['Folder'],
                               file_directory = Site_info['FilePath'])

# outputting an update of a complete file
print('We did it!! The file is now saved to the '+
      'provided file directory.')
        
