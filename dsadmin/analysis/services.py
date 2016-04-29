import sys
import os
import requests
import json

def get_donation_by_year(year):
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    donations = []
    for month, month_name in enumerate(months):
        total_amt = get_donation_by_year_month(year, month)
        donations.append({"MonthName":month_name,"Total":total_amt})
    return donations

def get_donation_by_year_month(year, month):
    payload = {'year':year, 'month':month}
    total_amt = 0
    if payload:
        r = requests.get('http://172.22.117.244/api/donation', params=payload)
        data = r.json()
        if data:
            for donation in data:
                total_amt += donation['DonationAmount']
    return total_amt

