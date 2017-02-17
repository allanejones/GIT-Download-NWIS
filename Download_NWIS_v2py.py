def download_NWIS_data(site_number ='08189500', begin_date='ALL',
                       end_date='today', file_name = 'unspecified',
                       file_directory = 'current', folder_name='unknown',
                       US_state = 'tx', download_type = 'Discharge'):
    """\
Basic input:
download_NWIS_data(site_number='08189500', begin_date='ALL',
                       end_date='today', file_name = 'unspecified',
                       file_directory = 'current', folder_name='unknown',
                       US_state = 'tx', download_type = 'Discharge'):

This script (re-written for Python2.7) is desgined to download the gage,
discharge, and other surfacewater data from the NWIS database during the
designated time-period.

Description of inputs:  ALL INPUTS ARE STRINGS.
The inputs are preset to retrieve all available data for the Mission River
USGS station (from '2007-10-01' to present) and save it in the current
directory with the default filename. ALL INPUTS ARE STRINGS.

All inputs should be strings. site_number is the eight-digit number for
each site (e.g. '08189500' for the Mission River gage of South Texas).

The 'download_type' input will allow the user to search for the available
data_types, such as "discharge", "stage height", "precipitation", etc.

'begin_date' is a string denoting the earliest time from which to retreive
data. All dates should be specified as followed 'YYYY-MM-DD'. An example
of an acceptable 'begin_date' would be '2007-10-01'. However, if you would
like to retrieve all available data, input 'ALL'.

The 'end_date' signifies the end of the time period for data retrieval. The
string 'end_date' may either be a specified date (format 'YYYY-MM-DD') or
a the string 'today', where the script will use the current date. As a
warning when using 'today' as the 'end_date' the NWIS dataset, the most
recent month's (approximate) data will be preliminary until reviewed by
the USGS offices.

The 'file_name' input will allow you to specify the
filename of the data to be saved. If no file name is specified, the
default filename will be:
[river_name+'_data_from_'+begin_date+'_to_'+end_date+'.txt'].

'file_directory' allows the user to specify the directory of the
file-to-be-saved. When specifying a file directory, make sure to include
"\\" for every backslash in the directory. If no file directory is specified,
the file will save in the current directory.

'folder_name' allows the user to input the name of the folder within the
current directory where the file will be saved. If no folder name is provided
the file will be saved in the current directory of this python script.

Also, if interested in a gaging station outside of Texas, you will need to
input (lowercase) the two-letter mail code for the state (e.g., 'co' - for
colorado). 

Remember:
!!! ALL INPUTS ARE STRINGS !!!!
"""

#### EXPANSIONS!
# - allow selection of wanted downloads

### find the end_date, if used 'today'
    time_fmt = "%Y-%m-%d"
    if end_date == 'today':
        import time
        end_date = time.strftime(time_fmt)

### Imports
    print('Beginning download for site number: '+site_number+' \n')
    import urllib
    import re
    import os
    import sys
    import time
    from bs4 import BeautifulSoup
    from bs4 import NavigableString

## Checking for good inputs/requests
# checking the state input    
    if len(US_state) != 2:
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'+
          '%%%')
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'+
          '%%%')
        print('State name is incorrect: '+US_state)
        
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'+
          '%%%')
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'+
          '%%% \n\n\n')
        return (site_number+'\t'+US_state)
    
### Find possible begin_date for input 'ALL'
### Open selctions page        
    URL = ('http://waterdata.usgs.gov/'+US_state+
                            '/nwis/uv?site_no='+site_number)
    print("Trying to access first website with: \n"+URL+"\n")
    website = urllib.urlopen(URL)
    source_page = website.read()
    soup = BeautifulSoup(source_page, "html.parser")

### returns the tags that have a second nested string and the tag name 'td'
    def find_text_wanted(tag):
        return (isinstance(tag.next_element.next_element, NavigableString)
                and tag.name == 'td')               
    text_tags = soup.find_all(find_text_wanted)


# iterates through the returned tags to find the downloadable
# data and the associated dates
    all_labels = []
    for tag in text_tags:
        if re.match('\w',tag.next_element.next_element):
            all_labels.append(
                tag.next_element.next_element.encode('ascii','ignore'))
            
## loops through the obtained tags and dates and pairs them into
# a master tuple variable
    download_dictionary = {}
    for entry in all_labels:
        # checks for hyphen not present, but digits present
        if '-' not in entry and re.search(r'\d', entry):
            index = all_labels.index(entry)
            download_dictionary[str(entry)] = [all_labels[index+1],
                                           all_labels[index+2]]
    ##        downloadable_options.append([all_labels[index],
    ##                                    all_labels[index+1],
    ##                                    all_labels[index+2]])
            
# checking that the master list was constructed properly
# a dictionary where each 'usgs option' is a key to the dates
    ##print(downloadable_options)

## Selects the earliest date to dowload data
    earliest = time.strptime(end_date,time_fmt)
    if begin_date == 'ALL': ## Find possible begin_date for input 'ALL'
        print('Finding the start date... \n')
        for key in download_dictionary:
            # loop through keys and check their start dates
            beginner = download_dictionary[key][0]
            holder = time.strptime(beginner, time_fmt)
            if holder < earliest:
                earliest = holder   
        begin_date = time.strftime(time_fmt,earliest)
        print("Date selected: "+begin_date+" \n")


## for loop separates out the call numbers for the discharge and stage data
    gage_num = []
    dis_num = []
    vel_num = []
    caveat = 0
    for key in download_dictionary:
        if 'gage height' in key.lower():
            gage_num = key[:key.index(" ")]
            if caveat != 2:
                caveat = 1
        elif 'discharge' in key.lower():
            dis_num = key[:key.index(" ")]
            caveat = 2
        elif 'velocity' in key.lower():
            vel_num = key[:key.index(" ")]
            caveat = 2
    
## Creates a list of all the call numbers of possible downloads
    downloads = []
    if gage_num:
        downloads.append(gage_num)
    if dis_num:
        downloads.append(dis_num)
    if vel_num:
        downloads.append(vel_num)

### Concatenate/Complete final URL
    URL = ("http://waterdata.usgs.gov/"+US_state.lower()+"/nwis/uv?")
    for num in downloads:
        URL += "cb_"+num+"=on&"

    URL += ("format=rdb&period=&begin_date="+begin_date+
            "&end_date="+end_date+"&site_no="+site_number)

## Secondary URL configuration
    URL2 = ("http://nwis.waterdata.usgs.gov/usa/nwis/uv/?")
    for num in downloads:
        URL2 += "cb_"+num+"=on&"

    URL2 += ("format=rdb&site_no="+site_number+"&period="+
            "&begin_date="+begin_date+"&end_date="+end_date)        

### Open the text-file webpage using URL, urllib2
    print("Trying to access download page with: \n"+URL2+'\n')
    try:
        website = urllib.urlopen(URL2)
        source_page = website.read()
        soup = BeautifulSoup(source_page, "html.parser")
    except ConnectionError:
        print('Trying to access with secondary URL: \n'+URL+'\n')
        try:
            website = urllib.urlopen(URL)
            source_page = website.read()
            soup = BeautifulSoup(source_page, "html.parser")
        except ConnectionError:
            print('There was an error with the connection. Try again later.'+'\n')
            return (site_number+'\tConnection issues...')

##### Find tags beginning with "b"
##    regex = re.compile("^b")
##    result_set = soup.find_all(regex)
##
##### Removes the string inside of the tags
##    for tag in result_set:
##        data = tag.string

## obtaining the textfile lines from the html parsing
    data = str(soup)

# checking for data to have been downloaded
# prints a QA warning when found or not
    if 'data' in locals():
        print("Download completed successfully for site number: "+
              site_number+" \n")
    else:
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'+
              '%%%')
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'+
          '%%%')
        print("\nDownload received no data for site number: "+
              site_number+" \n")
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'+
          '%%%')
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'+
          '%%% \n\n\n')
        return site_number

### Create filename from the downloaded data
    find_river ="USGS "+ site_number
    site = re.compile(site_number)

# search downloaded data for location/river name
    for item in data.split('\n'):
        if find_river in item:
           name_line = item
           break

# tease river name apart from the location ("near" or "at")
    if 'name_line' in locals(): # checks for name_line variable
        if ' at ' in name_line.lower() and ' nr ' in name_line.lower():
            if name_line.lower().index(' at ') < name_line.lower().index(' nr '):
                location_name = (name_line[site.search(name_line).end()+1
                                              :name_line.lower().index(' at ')])
            else:
                location_name = (name_line[site.search(name_line).end()+1
                                              :name_line.lower().index(' nr ')])
        elif ' at ' in name_line.lower() and ' nr ' not in name_line.lower():
            location_name = (name_line[site.search(name_line).end()+1
                                              :name_line.lower().index(' at ')])
        elif ' nr ' in name_line.lower() and ' at ' not in name_line.lower():
            location_name = (name_line[site.search(name_line).end()+1
                                              :name_line.lower().index(' nr ')])
        elif ',' in name_line.lower():
            location_name = (name_line[site.search(name_line).end()+1
                                           :re.search(',',name_line).start()])
        else:
            location_name = (name_line[site.search(name_line).end()+1
                                           :re.search(US_state,name_line).start()-1])

# makes a final river name for the file from the location name
    if 'location_name' in locals(): # checks for location_name variable
        river_name = '_'.join(location_name.split(' '))

# concatenate final filename
    if file_name == 'unspecified' and 'river_name' in locals():
        file_name = (site_number+'_'+river_name+'_data_from_'+begin_date+
                     '_to_'+end_date+'.txt')
    elif file_name == 'unspecified' and 'river_name' not in locals():
        file_name = (site_number+'_data_from_'+begin_date+
                     '_to_'+end_date+'.txt') 

### Find current file directory
    if file_directory == 'current' and folder_name == 'unknown':
        file_directory = os.getcwd()
        file_directory += '\\'+US_state
    elif file_directory == 'current' and folder_name !='unknown':
        file_directory = os.getcwd()
        file_directory = file_directory + '\\' + folder_name +'\\'+US_state
    elif file_directory != 'current' and folder_name != 'unknown':
        file_directory += '\\' + folder_name +'\\'+US_state

### Replacing the \t (tab) characters with commas for ease
### of reading in matalab
    data = data.replace("\t", ",")

### Writing the data (string) to the file
    path_full = file_directory + '\\' + file_name
    try:
        if not os.path.exists(file_directory):
            os.makedirs(file_directory)
        with open(path_full, "w") as file_out:
            if  caveat < 2:
                file_out.write('*********** WARNING!! CAVEAT!!'+
                               ' ***************'+'\n' + "!!!! ONE OR MORE OF"+
                               "THE WANTED DATA IS MISSING!!!!!"+
                               '\n' + '*********** WARNING!! CAVEAT!!' +
                               ' ***************\n\n')
            file_out.write('The downloadable data possible for'+
                           ' site number: '+site_number+'\n')
            [file_out.write('- '+ key+'\n') for key in download_dictionary]
            file_out.write('\n\n #### FILE BEGINS HERE!! #### \n')               
            file_out.write(data) # writing the data to the file
            print("The requested file has been written and saved. \n")
    except IOError as e:
        print("\nCould not write to file. \n")
        sys.exit(1)

### Returns the full directory path of the file saved so that you may
### easily call the saved file for subsequent analysis
    print('The followingis the file directory of the downloaded data for site: '
          +site_number +'\n'+path_full +'\n')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'+
          '%%% \n\n\n')
    #return path_full
