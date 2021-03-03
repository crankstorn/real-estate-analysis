import pandas as pd
import streamlit as st
import numpy_financial as npf
import numpy as np


## To execute, write in terminal:
# 1º -> cd C:\Users\ + rest of the path to the folder you saved the file
# 2º -> streamlit run Property_Analysis.py

############################################# FUNCTIONS SECTION #############################################

def net_operating(rent, tax_rate, price, years_amort, percent, down_paymnt):
    # TAKES INPUT AS MONTHLY EXPECTED RENT, PROPERTY TAX RATE, PROPERTY PRICE, LOAN YEARS,
    # LOAN INTEREST AND DOWN PAYMENT TO CALCULATE THE MONTHLY OPERATING INCOME
    # IN ADDITION, ASSUMES PROPERTY INSURANCE (1% OF THE RENT), CAPEX + REPAIRS (2% OF THE PROPERTY PRICE)
    # AND VACANCY (2% OF THE RENT)

    # LIST OF EXPENSES
    mortgage_amt = mortgage_monthly(price, years_amort, percent, down_paymnt)
    prop_insurance = rent * 0.01
    prop_tax = (price * (tax_rate / 100) / 12)
    prop_repairs = (price * 0.02) / 12
    vacancy = (rent * 0.02)

    # MONTHLY NET INCOME
    net_income = rent - prop_insurance - prop_tax - prop_repairs - vacancy - mortgage_amt

    # LIST OF RELEVANT OUTPUTS
    output = [prop_insurance, prop_tax, prop_repairs, vacancy, net_income]
    return output


def down_payment(price, percent):
    # SIMPLE FUNCTION TO GET THE DOWN PAYMENT RATE, RETURNING THE PAYMENT AMOUNT
    amt_down = price * (percent / 100)
    return amt_down


def mortgage_monthly(price, years, percent, down_paymnt):
    # THIS IMPLEMENTS AN APPROACH TO FINDING A MONTHLY MORTGAGE AMOUNT FROM THE PURCHASE PRICE,
    # YEARS, INTEREST RATE AND DOWN PAYMENT

    ##### PARAMETERS #####
    down = down_payment(price, down_paymnt)
    loan = price - down
    mortgage_amount = - loan
    interest_rate = (percent / 100) / 12
    periods = years * 12
    # CREATE ARRAY
    n_periods = np.arange(years * 12) + 1

    ##### BUILD AMORTIZATION SCHEDULE #####
    # INTEREST PAYMENT
    interest_monthly = npf.ipmt(interest_rate, n_periods, periods, mortgage_amount)

    # PRINCIPAL PAYMENT
    principal_monthly = npf.ppmt(interest_rate, n_periods, periods, mortgage_amount)

    # JOIN DATA
    df_initialize = list(zip(n_periods, interest_monthly, principal_monthly))
    df = pd.DataFrame(df_initialize, columns=['Period', 'Interest', 'Principal'])

    # MONTHLY MORTGAGE PAYMENT
    df['Monthly Payment'] = df['Interest'] + df['Principal']
    payment = df['Monthly Payment'].mean()

    return payment


def cap_rate(monthly_income, price):
    ##### RATIO FUNCTION #####
    # THIS FUNCTION TAKES MONTHLY INCOME, MULTIPLIES IT BY 12 (MONTHS) AND DIVIDES IT BY PRICE,
    # CALCULATING THE CAP RATE
    cap_rate = ((monthly_income * 12) / price) * 100
    cap_rate = round(cap_rate, 3)

    return cap_rate


def cash_on_cash(monthly_income, down_payment, repair_cost, additional_costs):
    ##### RATIO FUNCTION #####
    # THIS FUNCTION TAKES MONTHLY INCOME, MULTIPLIES IT BY 12 (MONTHS) AND DIVIDES THE NET INCOME
    # BY INITIAL COSTS (WITHOUT COUNTING THE MORTGAGE)
    cash_return = ((monthly_income * 12) / (down_payment + repair_cost + additional_costs)) * 100
    cash_return = round(cash_return, 3)
    return cash_return


def amortization_schedule(input_intrate, mortgage, years, down_paymnt):
    ##### PARAMETERS #####
    # CONVERT MORTGAGE AMOUNT TO NEGATIVE BECAUSE MONEY IS GOING OUT
    down = down_payment(mortgage, down_paymnt)
    loan = mortgage - down
    mortgage_amount = - (loan)
    interest_rate = (input_intrate / 100) / 12
    periods = years * 12
    # CREATE ARRAY
    n_periods = np.arange(years * 12) + 1

    ##### BUILD AMORTIZATION SCHEDULE #####
    # INTEREST PAYMENT
    interest_monthly = npf.ipmt(interest_rate, n_periods, periods, mortgage_amount)

    # PRINCIPAL PAYMENT
    principal_monthly = npf.ppmt(interest_rate, n_periods, periods, mortgage_amount)

    # JOIN DATA
    df_initialize = list(zip(n_periods, interest_monthly, principal_monthly))
    df = pd.DataFrame(df_initialize, columns=['Period', 'Interest', 'Principal'])

    # MONTHLY MORTGAGE PAYMENT
    df['Monthly Payment'] = df['Interest'] + df['Principal']

    # CALCULATE CUMULATIVE SUM OF MORTAGE PAYMENTS
    df['Balance'] = df['Monthly Payment'].cumsum()

    # REVERSE VALUES SINCE WE ARE PAYING DOWN THE BALANCE
    df.Balance = df.Balance.values[::-1]

    return df


def exportable_interface():
    ##### PROGRAM INTERFACE #####
    # TITLE AND HEADERS
    st.title("Real Estate Property Analysis")
    if project_id != "":
        st.header("Property Project ID: " + str(project_id))

    st.subheader("Property Selling Value Proposed: " + "{:,}".format(round(listing_notice), 0))
    st.markdown('#')

    # RATIO OUTPUTS
    st.write("The monthly cashflow is: ")
    st.write(monthly_cash)
    st.write("The cap rate is (in %): ")
    st.write(cap_return)
    st.write("The cash on cash return rate is (in %): ")
    st.write(cash_percent)
    st.write("""""")

    # MONTHLY COST DISTRIBUTION
    st.write("Monthly Cost Breakdown: ")
    st.write(costs_table)
    st.markdown('#')

    # AMORTIZATION SCHEDULE PLOT + TABLE
    st.write("Visual Amortization Schedule over " + str(years_amort) + " years: ")
    st.write('###### (French method)')
    st.area_chart(plot)
    if st.checkbox('Show Amortization Schedule Table over ' + str(years_amort) + ' years'):
        st.write(scenario)


############################################# MAIN CODE SECTION #############################################

try:
    ##### SIDEBAR SEGMENT #####
    # CREATING MANDATORY INPUT OBJECTS FOR THE INTERFACE SIDEBAR
    st.sidebar.write('### Set Inputs')
    st.sidebar.write('')
    project_id = st.sidebar.text_input("Enter a Project ID:   ")
    trial = st.sidebar.text_input("Enter the total property price:   ")
    down_paymnt = st.sidebar.text_input("Enter the loan down payment rate (0 - 100):   ")
    loan_interest = st.sidebar.text_input("Enter the loan interest rate (0 - 100):   ")
    years_amort = st.sidebar.text_input("Enter the length of loan in years:   ")
    rent_amt = st.sidebar.text_input("Enter the expected monthly rent price:   ")
    property_tax = st.sidebar.text_input("Enter the property tax rate (0 - 100):   ")

    # CREATING OPTIONAL INPUT OBJECTS FOR THE INTERFACE SIDEBAR
    if st.sidebar.checkbox('Display Optional inputs'):
        repair_cost = st.sidebar.text_input("Enter the property repair cost if needed:   ")
        additional_costs = st.sidebar.text_input("Enter the property additional costs if needed:   ")
        repair_cost = float(repair_cost)
        additional_costs = float(additional_costs)
    else:
        repair_cost = 0
        additional_costs = 0

    # FORMATTING INPUT DATA TYPES
    listing_notice = float(trial)
    rent_amt = float(rent_amt)
    property_tax = float(property_tax)
    years_amort = int(years_amort)
    loan_interest = float(loan_interest)
    down_paymnt = float(down_paymnt)

    # WITH INPUT VALUES, APPLYING FUNCTIONS
    mortgage = mortgage_monthly(listing_notice, years_amort, loan_interest, down_paymnt)
    cash = down_payment(listing_notice, down_paymnt)
    net_income = net_operating(rent_amt, property_tax, listing_notice, years_amort, loan_interest, down_paymnt)
    monthly_cash = round(net_income[4], 3)  # We extract the net income from the net_operating function
    cap_return = cap_rate(monthly_cash, listing_notice)
    cash_percent = cash_on_cash(monthly_cash, cash, repair_cost, additional_costs)
    if cash_percent == np.inf:  # Conditional to return 0 to avoid infinity values
        cash_percent = 0

    # INSERTING MORTGAGE VALUE TO THE NET INCOME LIST
    net_income.insert(0, mortgage)

    # SLICE THE NET INCOME FROM THE LIST, USE pd.DataFrame AND WE END UP WITH OUR COSTS TABLE
    costs = {'Expenses': ['Mortgage', 'Insurance', 'Property Tax', 'Repairs', 'Vacancy'],
             'Costs': net_income[0:5]
             }
    costs_table = pd.DataFrame(costs, columns = ['Expenses', 'Costs'])
    costs_table = costs_table.set_index('Expenses').T

    # APPLYING AMORTIZATION SCHEDULE FUNCTION
    scenario = amortization_schedule(loan_interest, listing_notice, years_amort, down_paymnt)

    # CREATING OBJECTS FOR THE PLOT AND TABLE
    scenario['Cumulative Interest'] = scenario['Interest'].cumsum()
    scenario['Equity'] = scenario['Principal'].cumsum() + scenario['Cumulative Interest']
    scenario = scenario.set_index('Period')
    plot = scenario[['Balance', 'Equity', 'Cumulative Interest']]
    scenario = scenario[['Monthly Payment', 'Principal', 'Interest', 'Balance']]

    exportable_interface()

except ValueError:
    ""
