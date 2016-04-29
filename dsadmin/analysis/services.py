import sys
import os
import requests
import json
import math
from datetime import date, timedelta, datetime
import operator

def get_donation_by_year(year):
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    donations = []
    for month, month_name in enumerate(months):
        total_amt = __get_donation_by_year_month(year, month+1)
        donations.append({"MonthName":month_name,"Total":total_amt})
    return donations

def __get_donation_by_year_month(year, month):
    payload = {'year':year, 'month':month}
    total_amt = 0
    if payload:
        r = requests.get('http://172.22.117.244/api/donation', params=payload)
        data = r.json()
        if data:
            for donation in data:
                total_amt += donation['DonationAmount']
    return total_amt

def __get_last_donation_data_in_days(days):
    payload = {'days':days}
    r = requests.get('http://172.22.117.244/api/inactiveDonation', params=payload)
    data = r.json()
    return data

def get_donation_target_by_year(year):
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    # targets should be retrieved from a central datasource, but we will mock it up for the time being
    targets = [100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000,100000]
    actuals = []
    for month, month_name in enumerate(months):
        total_amt = __get_donation_by_year_month(year, month+1)
        actuals.append(total_amt)
    months.insert(0, "Caption")
    targets.insert(0, "Target")
    actuals.insert(0, "Actual")
    return [months, targets, actuals]
    
def get_lapsed_donors(unit, value):
    date_format = "%Y-%m-%dT%H:%M:%S"
    units = ["days","weeks","months","years"]
    if unit not in units:
        return None
    inactive_donors = []
    donation_details = {}
    now = datetime.now()
    days = __convert_days_to_unit(value, unit)
    data = __get_last_donation_data_in_days(days)
    if data:
        for donation in data:
            id_num = donation['IdNumber']
            detail = {}
            try:
                detail = donation_details[id_num]
            except KeyError:
                detail = {
                    "IdType":donation['IdType'],
                    "IdNumber":donation['IdNumber'],
                    "FirstName":donation['FirstName'],
                    "LastName":donation['LastName'],
                    "Phone":donation['Phone'],
                    "Email":donation['Email'],
                    "AddressLine1":donation['AddressLine1'],
                    "AddressLine2":donation['AddressLine2'],
                    "AddressLine3":donation['AddressLine3'],
                    "PostalCode":donation['PostalCode'],
                    "Lapsed":0,
                    "Unit":unit,
                    "LastDonationDate":"",
                    "TotalDonationAmount":0,
                }
            if detail:
                donation_date = datetime.strptime(donation['DonationDate'], date_format)
                if detail['LastDonationDate']:
                    last_donate_time = datetime.strptime(detail['LastDonationDate'], date_format)
                    if donation_date > last_donate_time:
                        detail['LastDonationDate'] = donation_date.strftime(date_format)
                        detail['Lapsed'] = __convert_unit_from_days((now - donation_date).days, unit)
                else:
                    detail['LastDonationDate'] = donation_date.strftime(date_format)
                    detail['Lapsed'] = __convert_unit_from_days((now - donation_date).days, unit)
                detail['TotalDonationAmount'] += donation['DonationAmount']
                donation_details[id_num] = detail
        if donation_details:
            inactive_donors = donation_details.values()
    return inactive_donors

def get_top_donor_list_by_year(year, num):
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    donor_dict = {}
    donor_info = {}

    for month, month_name in enumerate(months):
        payload = {'year':year, 'month':month}
        r = requests.get('http://172.22.117.244/api/donation', params=payload)
        data = r.json()
        if data:
            for donation in data:
                if donation['IdNumber'] in donor_dict.keys():
                    donor_dict[donation['IdNumber']] = donor_dict[donation['IdNumber']] + donation['DonationAmount']
                else:
                    donor_dict[donation['IdNumber']] = donation['DonationAmount']
                    donor_info[donation['IdNumber']] = donation

    sorted_donor_dict = sorted(donor_dict.items(), key=operator.itemgetter(1), reverse=True)

    counter = 0
    top_donor_list = []
    for key, value in sorted_donor_dict:
        payload = {}
        if (counter < num):
            # print counter, key, value

             # print donor_info[key]
            payload['IdType'] = donor_info[key]['IdType']
            payload['IdNumber'] = donor_info[key]['IdNumber']
            payload['FirstName'] = donor_info[key]['FirstName']
            payload['LastName'] = donor_info[key]['LastName']
            payload['Phone'] = donor_info[key]['Phone']
            payload['Email'] = donor_info[key]['Email']
            payload['AddressLine1'] = donor_info[key]['AddressLine1']
            payload['AddressLine2'] = donor_info[key]['AddressLine2']
            payload['AddressLine3'] = donor_info[key]['AddressLine3']
            payload['PostalCode'] = donor_info[key]['PostalCode']

            payload['TotalDonationAmount'] = value
            payload['Rank'] = counter+1

            # print payload

            top_donor_list.append(payload)

            counter = counter + 1
        else:
            break

    print top_donor_list
    return top_donor_list

def __convert_days_to_unit(value, tounit):
    if tounit == "weeks":
        return value * 7
    elif tounit == "months":
        return value * 30
    elif tounit == "years":
        return value * 365
    else:
        return value
            
def __convert_unit_from_days(value, unit):
    if unit == "weeks":
        return int(math.ceil(value/7))
    elif unit == "months":
        return int(math.ceil(value/30))
    elif unit == "years":
        return int(math.ceil(value/365))
    else:
        return value
            

