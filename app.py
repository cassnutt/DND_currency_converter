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


# df2 = df.set_index('Coin Name')


# In[ ]:


st.table(df)


# In[ ]:


# text = st.empty()
# value = "default value"
# if st.button('reset textarea'):
#     value = "new value"

# or

placeholder = st.empty()

iput = placeholder.text_input('text')
click_clear = st.button('clear text input', key=1)
if click_clear:
    inpt = placeholder.text_input('text', value='', key=1)


# In[ ]:


# text = st.empty()
# value = "default value"
# if st.button('reset textarea'):
#     value = "new value"

# or

click_clear = st.button('Restart Calculations')
if click_clear:
    inpt = placeholder.text_input('text', value='', key=1)


# In[ ]:


# # plot on matplotlib
# def plot_results(data, x, y):
#     # set variables
#     x = data[x]
#     y = data[y]
#     colors = ['#CDC8C1', '#F0BE60', '#AB7E43','#D68505', '#7D7C64'] # set colors
#     fig, ax = plt.subplots(figsize=(10, 6))
    
#     # input variables into horizontal bar chart
#     ax.barh(y,x, color = colors)
#     ax.set_xlabel('Number of Coins')
#     ax.set_ylabel('Coin Type')
#     ax.set_title(f'Coins You Need for {userSpendGold} Gold', fontsize= 15);
    
#     #plot on streamlit
#     st.pyplot(fig)
# plot_results(df, 'Amount', 'Coin Name')


# In[ ]:


# plot on matplotlib

    # set variables
x = df['Amount']
y = df['Coin Name']
colors = ['#CDC8C1', '#F0BE60', '#D68505', '#7D7C64', '#AB7E43'] # set colors
fig, ax = plt.subplots(figsize=(10, 6))
    
    # input variables into horizontal bar chart
ax.barh(y,x, color = colors)
ax.set_xlabel('Number of Coins')
ax.set_ylabel('Coin Type')
ax.set_title(f'Coins You Need for {userSpendGold} Gold', fontsize= 15);
    
    #plot on streamlit
#     st.pyplot(fig)


# In[ ]:


# st.bar_chart(df)


# In[ ]:


placeholder = st.empty()
if st.checkbox('Show Chart'):
#     placeholder.bar_chart(df)
    placeholder.pyplot(fig)


# In[ ]:


# st.subheader(f'Coin Breakdown for {userSpendGold} gold pieces')
# st.write(df)
# #Bar Chart
# st.bar_chart(df['Coin Name'])


# In[ ]:


# terminal 


# In[ ]:


# jupyter nbconvert   --to script Streamlit_code.ipynb
# streamlit run app.py

