from urllib.request import Request, urlopen
import csv, os, shutil
import datetime

# def ark_csvs_download():
ark_csv_urls ={
    "arkk":"https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv",
    "arkq":"https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv",
    "arkw":"https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv",
    "arkg":"https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS.csv",
    "arkf":"https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv",
    "prnt":"https://ark-funds.com/wp-content/fundsiteliterature/csv/THE_3D_PRINTING_ETF_PRNT_HOLDINGS.csv",
    "izrl":"https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_ISRAEL_INNOVATIVE_TECHNOLOGY_ETF_IZRL_HOLDINGS.csv"
}

# us_time = pytz.timezone('US/Eastern')
# current_estern_time = datetime.datetime.now(us_time)
# current_date = str(current_estern_time.date())
data_dir = os.listdir("data/")

def ark_csv_download():
    file_date =""
    for urls in ark_csv_urls.keys():
        ark_url = ark_csv_urls.get(urls)
        url_req = Request(ark_url, headers={'User-Agent': 'Mozilla/5.0'})

        with urlopen(url_req) as ark_csv_file:  #before download the file, check if the file has already downloaded
            read_csv = ark_csv_file.read().decode()  #read and check dates
            rows = read_csv.split('\n')
            first_data_row = rows[1]
            file_date_str = first_data_row.split(',')[0]
            file_date = str(datetime.datetime.strptime(file_date_str, "%m/%d/%Y").date())

            # rows = [row for row in rows if row.split(",")[0]=='date' or row.split(",")[0]==file_date_str]

            if file_date in data_dir:
                print ('File already exist')
            else:  #if above check all passed, then download the file
                with open('data/{}.csv'.format(urls.upper()), 'w') as f:
                    f.write(read_csv)
    try:
        path_name = "data/{}".format(file_date)
        os.mkdir(path_name)
        files = [files.upper() + '.csv' for files in ark_csv_urls.keys()]
        for f in files:
            shutil.move("data/{}".format(f), "data/{}".format(file_date))
        print ('all files have downloaded')

    except FileExistsError as e:
        print (e)

def check_if_missing_file():
    for i in data_dir:
        daily_file = os.listdir("data/{}".format(i))
        if len(daily_file) < 7 :
            print ('missing file in folrder {}'.format(i))
        else:
            pass

ark_csv_download()
check_if_missing_file()