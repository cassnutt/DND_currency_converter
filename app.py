#!/usr/bin/env python
# coding: utf-8

# In[12]:


import streamlit as st
import numpy as np
import pprint
import pandas as pd

import matplotlib.pyplot as plt


# In[7]:


st.title('''
Dungeons & Dragons Currency Converter
''')

st.write('''
Please type the number of coins you have for each coin type''')


# In[13]:


# Function to convert 
copper = 1/100
silver = 1/10
electrum = 1/2
gold = 1
platinum = 10

def getCoins(coins, amount, coinIndex = 0):
    amount = float(amount)
    if amount == 0:
        return [] # all done! You did it!
    if coinIndex >= len(coins):
        return None # don't have enough money / coins
    
    # names of coins to print later
    coinNames = ['', 'Gold', 'Platinum', 'Electrum', 'Silver', 'Copper']
    
    # start calculations
    coin = coins[coinIndex] # 1= gold, 2= platinum, ...
    coinIndex += 1 
    # First, take as may as possible from first listed coin (will start at Index 1 (gold))
    canTake = int(min(amount / coin['value'], coin['count']))
    
    #Reduce the number taken from this coin until success
    for count in np.arange(canTake, -1.0, -1):  # take away 1 until count reaches 0
        
        # Recurse to decide how many to take from next coin
        change = getCoins(coins, amount - coin['value'] * count, coinIndex)
        if change != None: # Success! We are done!
            if count: # Register this number for this coin
                return change + [{'Coin Name': coinNames[coinIndex], 'Amount': int(count)}]
            return change


# In[9]:


# # have user input the amount they have for each coin
while True:
    try: 
        userNumCopper = st.number_input('Enter number of Copper: ', min_value= 0, max_value= 99999999)
        userNumSilver = st.number_input('Enter number of Silver: ', min_value= 0, max_value= 99999999)
        userNumElectrum = st.number_input('Enter number of Electrum: ', min_value= 0, max_value= 99999999)
        userNumGold = st.number_input('Enter number of Gold: ', min_value= 0, max_value= 99999999)
        userNumPlatinum = st.number_input('Enter number of Platinum: ', min_value= 0, max_value= 999999)

    except ValueError:
        continue
    
    break


# In[ ]:


# tell user how much they have in gold pieces

# st.write('''Total Coins in Gold Pieces''')
totalGold = (userNumCopper * copper) + (userNumSilver * silver) + (userNumElectrum * electrum) +     (userNumGold) + (userNumPlatinum * platinum)
totalGold = round(totalGold)

st.subheader(f'You have {totalGold} gold pieces.')


# In[ ]:


# ask how much they are trying to spend
st.title('''Gold you would like to spend''')
userSpendGold = st.number_input('How much gold do you want to spend? ', min_value= 0, max_value= 9999999999)


# In[ ]:


if userSpendGold > totalGold:
    st.write('You do not have enough money. Sorry!')
    st.write(f'Total Gold: {totalGold}')
    st.write(f'Gold you need: {userSpendGold}')
    
else:
    coins = [
    { "value": gold, "count":  userNumGold },   
    { "value": platinum, "count":  userNumPlatinum },   
    { "value":  electrum, "count":  userNumElectrum },
    { "value":  silver, "count":  userNumSilver },
    { "value":  copper, "count": userNumCopper } 
    ]
    
    
    result = getCoins(coins, userSpendGold)


# In[11]:


df = pd.DataFrame(result)


# In[ ]:





# In[ ]:


df = df.set_index('Coin Name')
st.table(df)

# In[ ]:
# st.bar_chart(df)

placeholder = st.empty()
if st.checkbox('Show Chart'):
    placeholder.bar_chart(df)

# st.subheader(f'Coin Breakdown for {userSpendGold} gold pieces')
# st.write(df)
# #Bar Chart
# st.bar_chart(df['Coin Name'])


# In[ ]:


# jupyter nbconvert   --to script Streamlit_code.ipynb
# streamlit run app.py

