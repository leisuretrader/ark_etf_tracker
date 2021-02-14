import os, csv, pytz, datetime
import numpy as np
import itertools

us_time = pytz.timezone('US/Eastern')
current_estern_time = datetime.datetime.now(us_time)
current_date = str(current_estern_time.date())

data_dir = os.listdir("data/")
ark_etfs = ['ARKK','ARKQ' ,'ARKW','ARKG','ARKF','PRNT','IZRL']

# load the most recent 2 dates data
most_recent_dates = [data_dir[-1], data_dir[-2]]
# print (most_recent_dates)

holdings_by_dates = {}
def comparison():
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

comparison()


newly_added = []
recent_removed = []

previous_date_holding = holdings_by_dates.get(most_recent_dates[1])
current_date_holding = holdings_by_dates.get(most_recent_dates[0])

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

    newly_added_stock_cusip_list = np.setdiff1d(current_stock_cusip_list, previous_stock_cusip_list)
    newly_added_stocks = [i for i in newly_added_stock_cusip_list if len(i) != 9]
    newly_added_dict = {}
    newly_added_dict[fund] = newly_added_stocks
    newly_added.append(newly_added_dict)

    recent_removed_stock_cusip_list = np.setdiff1d(previous_stock_cusip_list,current_stock_cusip_list)
    recent_removed_stocks = [i for i in recent_removed_stock_cusip_list if len(i) != 9]
    recent_removed_dict = {}
    recent_removed_dict[fund] = recent_removed_stocks
    recent_removed.append(recent_removed_dict)


print (current_date)
print ("\n")
print ("Newly Added Stocks: ","\n", "\n".join(map(str,newly_added)))
print ("====================================================")
print ("Recent Removed Stocks: ", "\n", "\n".join(map(str,recent_removed)))