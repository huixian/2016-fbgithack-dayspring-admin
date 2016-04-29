import sys
import os
import requests
import json
import math
from datetime import date, timedelta, datetime

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
                    if donation_date < last_donate_time:
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
            

