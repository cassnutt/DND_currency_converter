#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import numpy as np
import pprint
import pandas as pd

# empty dataframe hidden until user inputs data
df = pd.DataFrame()


# In[7]:


st.title('Dungeons & Dragons Currency Converter')
st.write('')

st.image('images/DND.jpeg', use_column_width= True)

# create columns to right align photo source text
col1, col2, col3 = st.beta_columns([1,1,.5])
click_clear = col3.write('[Photo Source](https://www.polygon.com/deals/21294556/dnd-how-to-play-dungeons-dragons-5e-guide-spells-dice-character-sheets-dm)')


# add some space between photo and instructions
st.markdown('#')
st.write('''
Please input the number of coins you have for each coin type''')


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


# In[ ]:


# create placeholders to clear inputs when clicking "start over" button
placeholder_c = st.empty()
placeholder_s = st.empty()
placeholder_e = st.empty()
placeholder_g = st.empty()
placeholder_p = st.empty()


# In[9]:


# # have user input the amount they have for each coin
# while True:
#     try: 
#         userNumCopper = placeholder_c.number_input('Enter number of Copper: ', min_value= 0)
#         userNumSilver = placeholder_s.number_input('Enter number of Silver: ', min_value= 0)
#         userNumElectrum = placeholder_e.number_input('Enter number of Electrum: ', min_value= 0)
#         userNumGold = placeholder_g.number_input('Enter number of Gold: ', min_value= 0)
#         userNumPlatinum = placeholder_p.number_input('Enter number of Platinum: ', min_value= 0)

#     except ValueError:
#         continue
    
#     break


# In[9]:


# have user input the amount they have for each coin

userNumCopper = placeholder_c.number_input('Enter number of Copper: ', min_value= 0)
userNumSilver = placeholder_s.number_input('Enter number of Silver: ', min_value= 0)
userNumElectrum = placeholder_e.number_input('Enter number of Electrum: ', min_value= 0)
userNumGold = placeholder_g.number_input('Enter number of Gold: ', min_value= 0)
userNumPlatinum = placeholder_p.number_input('Enter number of Platinum: ', min_value= 0)


# In[ ]:


# tell user how much they have in gold pieces

# st.write('''Total Coins in Gold Pieces''')
totalGold = (userNumCopper * copper) + (userNumSilver * silver) + (userNumElectrum * electrum) +     (userNumGold) + (userNumPlatinum * platinum)
totalGold = round(totalGold)

st.subheader(f'You have {totalGold:,d} gold pieces.')


# In[ ]:


st.write('')


# In[ ]:


# ask how much they are trying to spend
st.header('''Gold you would like to spend''')
placeholder_u = st.empty()
userSpendGold = placeholder_u.number_input('How much gold do you want to spend? ', min_value= 0, value= 0)


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
    df = pd.DataFrame(result)


# In[ ]:


# show table after data is entered
table_placeholder = st.empty()

if not df.empty:
    table_placeholder.table(df)


# In[ ]:


# create dividing line to separate calculations from reset
st.write('-------------------------')


# In[ ]:


# create columns to right align restart button
col1, col2, col3 = st.beta_columns([1,1,.5])
click_clear = col3.button('Start Again')

# set fields back to 0 when clicking button
if click_clear:

    userNumCopper = placeholder_c.number_input('Enter number of Copper: ', 
                                               min_value= 0, value= 0, key= 'redo')
    userNumSilver = placeholder_s.number_input('Enter number of Silver: ', 
                                               min_value= 0, value= 0, key= 'redo1')
    userNumElectrum = placeholder_e.number_input('Enter number of Electrum: ', 
                                                 min_value= 0, value= 0, key= 'redo2')
    userNumGold = placeholder_g.number_input('Enter number of Gold: ', 
                                             min_value= 0, value= 0, key= 'redo3')
    userNumPlatinum = placeholder_p.number_input('Enter number of Platinum: ', 
                                                 min_value= 0, value= 0, key= 'redo4')
    userSpendGold = placeholder_u.number_input('How much gold do you want to spend? ', 
                                               min_value= 0, value= 0, key= 'redo5')



    st.write('The values have been reset')
    st.balloons()


# In[ ]:


# terminal 
# jupyter nbconvert   --to script Streamlit_code.ipynb
# streamlit run app.py

