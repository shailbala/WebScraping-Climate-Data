import pandas as pd, re, json

def process_scraped_city(cityNames, months = [1,2,3,4,5], \
                         path = '', verbose = False):
    '''
    Returns a dictionary of pandas data frame, with key as cityName
    Returns a list of unprocessed cityNames
    '''
    useful = []
    missing = []
    data_dict = {}
    for city in cityNames:
        ## to keep data for all months for a city
        city_data_all = []
        curly_all = []
        for month in months:
            p = path
            with open(p+city+str(month), 'r') as cityS:
                data = cityS.read()
                #useful = re.findall('\"details\"\:\[.*\"grid\"', data)
                useful = re.findall('\"detail\"\:.+grid', data)
                if verbose:
                    print("No. of useful parts found using regex:", len(useful))
                # useful contains only one item
                ## find all {} entries, store it in a list curly_all
                ## not greedy, for every pair
                curly_all = re.findall('{.+?}', useful[0])
                if verbose:
                    print("Curly_all, all entries for each day found: ", len(curly_all))
                ## if the number of entries is not divided by 4, some entries are missing
                elif len(curly_all) % 4 != 0:
                    ## add it to the list, missing data
                    missing.append(city+str(month))

            ## process each city data and add it to the
            ## city_data_all, for all months
            ## remove hl part from every 4th entry
            for i in range(len(curly_all)):
                curly_all[i] = json.loads(curly_all[i])
                if 'hl' in curly_all[i].keys():
                    #print(curly_all[i])                    
                    del curly_all[i]['hl']
                    del curly_all[i]['hls']
                    del curly_all[i]['hlsh']
                    #print(curly_all[i])

            ## add it to city_data_all   
            city_data_all.extend(curly_all)
            if verbose:
                print("\nMonth:", month)
                print("Length of main city list: ", len(city_data_all))
        ## make dataframe
        city_df = pd.DataFrame(city_data_all)
        ## drop irrelevant data
        city_df = city_df.drop(axis=1, columns=['date', 'icon'])
        ## city_df.columns
        ## Index(['ts', 'ds', 'desc', 'temp', 'templow',
        ##'baro', 'wind', 'wd', 'hum'], dtype='object')
        
        ## add to data_dict
        data_dict[city] = city_df
    return data_dict, missing

def write_df_dict(df_dict, path = '', verbose=False):
    '''
    Input: A dictionary of key: pandas.DataFrame, path to write the files
    Function: Writes each dataFrame at the given path with name given in key
    '''
    for city in df_dict.keys():
        city_df = df_dict[city]
        city_df.to_csv(path+city, index=False)
    if verbose:
        print("All DataFrames written succesfully!")


cityNames = []
with open('city_names.txt') as file:
    l = file.readlines()
    for line in l:
        cityNames.append(line.strip("\n"))

## for testing, take only first city
## cityNames = cityNames[:1]
months = [1,2,3,4,5]
path = '/home/magiclair/Documents/covid-19/climate-data-test/new-scraped data/'
# path for writing dataFrame
path2 = "/home/magiclair/Documents/covid-19/climate-data-test/df/"

df_dict, missing = process_scraped_city(cityNames, months, path)
write_df_dict(df_dict, path2, True)

## write the cities not processed for manual inspection
with open("/home/magiclair/Documents/covid-19/climate-data-test/MissingData", 'w') as file:
    for each in missing:
        file.write(each+"\n")

