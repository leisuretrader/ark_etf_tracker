import os, csv, pytz, datetime
import numpy as np
import itertools

us_time = pytz.timezone('US/Eastern')
current_estern_time = datetime.datetime.now(us_time).date()

data_dir = os.listdir("data/")
ark_etfs = ['ARKK','ARKQ' ,'ARKW','ARKG','ARKF','PRNT','IZRL']

# load the most recent 2 dates data from directory folder
most_recent_dates = [data_dir[-1], data_dir[-2]]  #[current_date, previous_date]

current_date = most_recent_dates[0]
preivous_date = most_recent_dates[1]


def csv_to_dict_by_dates(current_date, previous_date):
    holdings_by_dates = {}
    for ark_date in most_recent_dates:
        current_cusip = {}
        for etf in ark_etfs:
            with open("data/{}/{}.csv".format(ark_date, etf)) as f:
                reader = csv.reader(f)
                next(reader)
                row_list = []
                for row in reader:
                    cusip = row[4]
                    if cusip:
                        # company, ticker, cusip, shares, market value, weight
                        row_data = [row[2], row[3], row[4], row[5], row[6], row[7]]
                        row_list.append(row_data)
                        current_cusip[etf] = row_list

        holdings_by_dates[ark_date] = current_cusip
    return holdings_by_dates

holdings_by_dates = csv_to_dict_by_dates(current_date, preivous_date)

def ark_change_between_two_dates(current_date, previous_date):
    newly_added = []
    recent_removed =[]

    current_date_holding = holdings_by_dates.get(current_date)
        # most_recent_dates[0])
    previous_date_holding = holdings_by_dates.get(previous_date)
        # most_recent_dates[1])

    for fund, values in current_date_holding.items():
        current_stock_cusip_list = [[i[1], i[2]] for i in values]
        previous_stock_cusip_list = [[i[1], i[2]] for i in previous_date_holding.get(fund)]

    #######################below section create stock_cusip dictionary, seems useless. eg {'CGEN': 'M25722105', 'CRSP': 'H17182108', 'DOCU': '256163106', 'EDIT': '28106W103',...}
        stock_cusip_lookup = {} # ****

        stock_cusip_list = current_stock_cusip_list + previous_stock_cusip_list
        stock_cusip_list.sort()
        stock_cusip_list= list(stock_cusip_list for stock_cusip_list,_ in itertools.groupby(stock_cusip_list)) #remove duplicates
        
        for l in stock_cusip_list:
            key, value = l[0], l[1]
            stock_cusip_lookup[key] = value
    #########################################################

        newly_added_stock_cusip_list = np.setdiff1d(current_stock_cusip_list, previous_stock_cusip_list) #find difference between the two lists
        newly_added_stocks = [i for i in newly_added_stock_cusip_list if len(i) != 9]  #remove cusip data from the list
        newly_added_dict = {} #create a dict
        newly_added_dict[fund] = newly_added_stocks
        newly_added.append(newly_added_dict) #append the dict result to the final list

        recent_removed_stock_cusip_list = np.setdiff1d(previous_stock_cusip_list,current_stock_cusip_list)
        recent_removed_stocks = [i for i in recent_removed_stock_cusip_list if len(i) != 9]
        recent_removed_dict = {}
        recent_removed_dict[fund] = recent_removed_stocks
        recent_removed.append(recent_removed_dict)
    
    print ("\n")
    print ('Comparing ARK holdings between {} and {}. Below are newly added and recent removed tickers'.format(previous_date,current_date))
    print ("\n")
    print ("Newly Added Stocks: ","\n", "\n".join(map(str,newly_added)))
    print ("====================================================")
    print ("Recent Removed Stocks: ", "\n", "\n".join(map(str,recent_removed)))

ark_change_between_two_dates(current_date, preivous_date)