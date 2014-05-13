from bs4 import BeautifulSoup, SoupStrainer
from lxml import html
from datetime import datetime
from numpy import zeros
import numpy as np
import requests
import httplib2
import unicodedata
import matplotlib.pyplot as plt
import csv
import math
import json

# local edited html file
ADDRESS = "tcgplayerDecksTOP8.html"

# Initializations
urls = []
dates = []
temp = []
deckIDs = []
deckRegUrls = []
cards = []
cardsTemp1 = []
cardsTemp2 = []
deckNames = []

## Scrape Data

# Beautiful Soup initialization
soup = BeautifulSoup(open(ADDRESS))

# grab all of the hrefs in a tags
for link in soup.find_all('a', href=True):
    temp.append((link['href']))

# grab links to the decks (every third link) (1st, 4th, etc)
for i in range(len(temp)):
    if (i % 3 == 0):
        urls.append("http://magic.tcgplayer.com" + temp[i])

# grab dates of the decks
for date in soup.find_all('td', attrs={'width':'9%'}):
    dates.append(date.text)

# convert dates from unicode to string and then to date format
for i in range(len(dates)):
    dates[i] = datetime.date(datetime.strptime(unicodedata.normalize('NFKD',dates[i]).encode('ascii','ignore'),'%m/%d/%Y'))

# truncate each url to last 6 characters to obtain deck ID
for i in range(len(urls)):
    deckIDs.append(urls[i][-7:])

# deck registration sheet urls
for i in range(len(urls)):
    deckRegUrls.append("http://magic.tcgplayer.com/db/printable_deck_reg_sheet.asp?ID=" + deckIDs[i])

# Gather card data
for i in range(len(urls)):
    page = requests.get(deckRegUrls[i])
    soup = BeautifulSoup(page.text)
    for card in soup.find_all('td', attrs={'class':'default_8'}):
        cardsTemp1.append(card.text)
    for deckName in soup.find_all('td', attrs={'class':'default_9'}):
        deckNames.append(deckName.text)
    # convert cards and deck names from unicode to string
    for i in range(len(cardsTemp1)):
        cardsTemp1[i] = unicodedata.normalize('NFKD',cardsTemp1[i]).encode('ascii','ignore')
    # munging
    cardsTemp1 = cardsTemp1[8:]
    for card in reversed(cardsTemp1):
        if card[-1:] == '\n' or card == '' or '?' in card or 'Island' in card or 'Swamp' in card or 'Mountain' in card or 'Forest' in card or 'Plains' in card:
            cardsTemp1.remove(card)
    for i in range(len(cardsTemp1)):
        cardsTemp2.append([int(cardsTemp1[i][:2]), cardsTemp1[i][2:]])
    cards.append(cardsTemp2)
    cardsTemp1 = []
    cardsTemp2 = []

## Munge Data



numDecks = len(deckNames)

# more munging
for i in range(numDecks):
    deckNames[i] = unicodedata.normalize('NFKD',deckNames[i]).encode('ascii','ignore')
    deckNames[i] = deckNames[i][11:]

# find unique deck names
uniqueDeckNames = list(set(deckNames))

# determine deck archetypes for each decklist and count number of each archetype
numControl = 0
numMidrange = 0
numDevotion = 0
numDredge = 0
numAggro = 0
numBurn = 0
numAuras = 0
archetypes = ['UNASSIGNED']*numDecks      # initialize list of archetypes
uniqueArchetypes = ['Devotion', 'Control', 'Midrange', 'Aggro', 'Auras', 'Dredge', 'Burn']
for deck in range(numDecks):
    if deckNames[deck]=='Dimir Control' or deckNames[deck]=='Esper Control' or deckNames[deck]=='BUG Control' or deckNames[deck]=='American Control' or deckNames[deck]=='Naya Control' or deckNames[deck]=='Rakdos Control' or deckNames[deck]=='Orzhov Control' or deckNames[deck]=='Azorius Control' or deckNames[deck]=='Bant Superfriends' or deckNames[deck]=='Chromanticore Control' or deckNames[deck]=="Maze's End":
        archetypes[deck] = 'Control'        # Control Decks
        numControl += 1
    elif deckNames[deck]=='Bant Midrange' or deckNames[deck]=='Boros Midrange' or deckNames[deck]=='RUG Midrange' or deckNames[deck]=='Esper Midrange' or deckNames[deck]=='BWR Midrange' or deckNames[deck]=='Naya Midrange' or deckNames[deck]=='Junk Midrange' or deckNames[deck]=='Azorius Midrange' or deckNames[deck]=='Orzhov Midrange' or deckNames[deck]=='Selesnya Midrange' or deckNames[deck]=='Golgari Midrange' or deckNames[deck]=='Rakdos Midrange' or deckNames[deck]=='BUG Midrange' or deckNames[deck]=='Jund Midrange' or deckNames[deck]=='Gruul Midrange' or deckNames[deck]=='4C Midrange':
        archetypes[deck] = 'Midrange'       # Midrange Decks
        numMidrange += 1
    elif deckNames[deck]=='UW Devotion' or deckNames[deck]=='Monogreen Devotion' or deckNames[deck]=='Monored Devotion' or deckNames[deck]=='Naya Devotion' or deckNames[deck]=='Monoblue Devotion' or deckNames[deck]=='UR Devotion' or deckNames[deck]=='BR Devotion' or deckNames[deck]=='RG Devotion' or deckNames[deck]=='UG Devotion' or deckNames[deck]=='Monoblack Devotion' or deckNames[deck]=='Esper Devotion' or deckNames[deck]=='UB Devotion' or deckNames[deck]=='RW Devotion':
        archetypes[deck] = 'Devotion'       # Devotion Decks
        numDevotion += 1
    elif deckNames[deck]=='BG Dredge' or deckNames[deck]=='Junk Reanimator':
        archetypes[deck] = 'Dredge'         # Dredge Decks
        numDredge += 1
    elif deckNames[deck]=='Orzhov Aggro' or deckNames[deck]=='Naya Aggro' or deckNames[deck]=='Red Deck Wins' or deckNames[deck]=='Monowhite Aggro' or deckNames[deck]=='Monoblack Aggro' or deckNames[deck]=='Jund Aggro' or deckNames[deck]=='Gruul Aggro' or deckNames[deck]=='Azorius Aggro' or deckNames[deck]=='Rakdos Aggro' or deckNames[deck]=='Monogreen Aggro' or deckNames[deck]=='Boros Aggro' or deckNames[deck]=='Selesnya Aggro' or deckNames[deck]=='Heroic White' or deckNames[deck]=='Immortal Servitude':
        archetypes[deck] = 'Aggro'          # Aggro Decks
        numAggro += 1
    elif deckNames[deck]=='Boros Burn':
        archetypes[deck] = 'Burn'           # Burn Decks
        numBurn += 1
    elif deckNames[deck]=='Selesnya Auras' or deckNames[deck]=='Naya Auras' or deckNames[deck]=='Boros Auras':
        archetypes[deck] = 'Auras'          # Auras Decks
        numAuras += 1
    else:
        archetypes[deck] = 'UNASSIGNED'     # for debugging. all decks should be assigned.

# create exhaustive lists of cards in each archetype for analysis
controlCards = []
midrangeCards = []
devotionCards = []
dredgeCards = []
aggroCards = []
burnCards = []
aurasCards = []
for deck in range(numDecks):
    if archetypes[deck] == 'Control':
        for card in range(len(cards[deck])):
            for i in range(cards[deck][card][0]):
                controlCards.append(cards[deck][card][1])
    elif archetypes[deck] == 'Midrange':
        for card in range(len(cards[deck])):
            for i in range(cards[deck][card][0]):
                midrangeCards.append(cards[deck][card][1])
    elif archetypes[deck] == 'Devotion':
        for card in range(len(cards[deck])):
            for i in range(cards[deck][card][0]):
                devotionCards.append(cards[deck][card][1])
    elif archetypes[deck] == 'Dredge':
        for card in range(len(cards[deck])):
            for i in range(cards[deck][card][0]):
                dredgeCards.append(cards[deck][card][1])
    elif archetypes[deck] == 'Aggro':
        for card in range(len(cards[deck])):
            for i in range(cards[deck][card][0]):
                aggroCards.append(cards[deck][card][1])
    elif archetypes[deck] == 'Burn':
        for card in range(len(cards[deck])):
            for i in range(cards[deck][card][0]):
                burnCards.append(cards[deck][card][1])
    elif archetypes[deck] == 'Auras':
        for card in range(len(cards[deck])):
            for i in range(cards[deck][card][0]):
                aurasCards.append(cards[deck][card][1])

# create unique lists of cards by archetype for convenience
uniqueControlCards = list(set(controlCards))
uniqueMidrangeCards = list(set(midrangeCards))
uniqueDevotionCards = list(set(devotionCards))
uniqueDredgeCards = list(set(dredgeCards))
uniqueAggroCards = list(set(aggroCards))
uniqueBurnCards = list(set(burnCards))
uniqueAurasCards = list(set(aurasCards))

# find the total number of cards across all decks for creating proportions
totalCards = len(controlCards)+len(midrangeCards)+len(devotionCards)+len(dredgeCards)+len(aggroCards)+len(burnCards)+len(aurasCards)

# create tuple of lists: [# occurrences of card], [card name]
countTemp = []
cardsTemp = []
for deck in range(numDecks):
    for card in range(len(cards[deck])):   # go through every card in every deck
        if cards[deck][card][1] in cardsTemp:
            countTemp[cardsTemp.index(cards[deck][card][1])] += 1
        else:
            countTemp.append(1)
            cardsTemp.append(cards[deck][card][1])
cardCounts = [countTemp, cardsTemp]
numUniqueCards = len(cardCounts[0])

# deal with card names containing "// " (like "Turn // Burn")
for i in range(len(cardCounts[1])):
    if "// " in cardCounts[1][i]:
        cardCounts[1][i] = cardCounts[1][i].replace('// ', '')
    if cardCounts[1][i][-1:] == ' ':        # handles cases ending with a space
        cardCounts[1][i] = cardCounts[1][i][:-1]

# get counts of each archetype over time
counts = np.zeros((7,6))
for deck in range(numDecks):
    if dates[deck].month == 2:
        if dates[deck].day < 21:
            counts[uniqueArchetypes.index(archetypes[deck])][0] += 1
        else:
            counts[uniqueArchetypes.index(archetypes[deck])][1] += 1
    elif dates[deck].month == 3:
        if dates[deck].day < 7:
            counts[uniqueArchetypes.index(archetypes[deck])][1] += 1
        elif dates[deck].day < 21:
            counts[uniqueArchetypes.index(archetypes[deck])][2] += 1
        else:
            counts[uniqueArchetypes.index(archetypes[deck])][3] += 1
    elif dates[deck].month == 4:
        if dates[deck].day < 4:
            counts[uniqueArchetypes.index(archetypes[deck])][3] += 1
        elif dates[deck].day < 18:
            counts[uniqueArchetypes.index(archetypes[deck])][4] += 1
        else:
            counts[uniqueArchetypes.index(archetypes[deck])][5] += 1
    else:
        counts[uniqueArchetypes.index(archetypes[deck])][5] += 1

# create archetypeSuccess.csv for visualization
with open('archetypeSuccess.csv','wb') as myfile:
    wrtr = csv.writer(myfile, delimiter=',')
    wrtr.writerow(["Devotion", "Control", "Midrange", "Aggro", "Auras", "Dredge", "Burn"])
    for i in range(6):
        wrtr.writerow([math.ceil(counts[0][i]/counts.T[i].sum()*100)/100, math.ceil(counts[1][i]/counts.T[i].sum()*100)/100, math.ceil(counts[2][i]/counts.T[i].sum()*100)/100, math.ceil(counts[3][i]/counts.T[i].sum()*100)/100, math.ceil(counts[4][i]/counts.T[i].sum()*100)/100, math.ceil(counts[5][i]/counts.T[i].sum()*100)/100, math.ceil(counts[6][i]/counts.T[i].sum()*100)/100])
    myfile.flush()


# create cardCounts.csv for table
with open('cardCounts.csv','wb') as myfile:
    wrtr = csv.writer(myfile, delimiter=',')
    wrtr.writerow(["Name", "Count"])
    for i in range(len(cardCounts[0])):
        wrtr.writerow([cardCounts[1][i], cardCounts[0][i]])
    myfile.flush()

cardProps = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
found = False
# rather than exporting a csv, just export the table for use in the visualization
output = '<table id="cardCts"><thead><tr><th rowspan="2" style="text-align:right">Card Names</th><th rowspan="2" style="border-right: 2px solid black; padding-right:5px">Count</th><th colspan="8">Proportions by Archetype</th></tr>'
output += '<tr><th class="col">TOTAL</th><th>Devotion</th><th>Control</th><th>Midrange</th><th>Aggro</th><th>Auras</th><th>Dredge</th><th>Burn</th></tr></thead><tbody>'
for i in range(len(cardCounts[0])):
    for deck in range(numDecks):
        for card in range(len(cards[deck])):
            if cardCounts[1][i] == cards[deck][card][1] and found is False:
                cardProps[0] += 1
                cardProps[uniqueArchetypes.index(archetypes[deck])+1] += 1
                found = True
        found = False
    cardProps[0] = round(cardProps[0]/(numDecks),4)*100
    cardProps[1] = round(cardProps[1]/(numDevotion),4)*100
    cardProps[2] = round(cardProps[2]/(numControl),4)*100
    cardProps[3] = round(cardProps[3]/(numMidrange),4)*100
    cardProps[4] = round(cardProps[4]/(numAggro),4)*100
    cardProps[5] = round(cardProps[5]/(numAuras),4)*100
    cardProps[6] = round(cardProps[6]/(numDredge),4)*100
    cardProps[7] = round(cardProps[7]/(numBurn),4)*100
    output += '<tr><td><a href="http://mtgimage.com/card/' + cardCounts[1][i] + '.jpg" class="screenshot" rel="http://mtgimage.com/card/' + cardCounts[1][i] + '.jpg">' + cardCounts[1][i] + '</a></td><td class="col" style="border-right: 2px solid black; padding-right:5px">' + str(cardCounts[0][i]) + '</td>'
    for j in range(len(cardProps)):
        output += '<td class="col">' + str(cardProps[j]) + '%</td>'
    output += '</tr>'
    cardProps = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
output += '</tbody></table>'
tableHTML = open('table.txt','w')
tableHTML.write(output)
tableHTML.close()
    

'''
## FIGURE 1: Evolution of the BNG Standard Metagame
x = [1, 2, 3]
x_ticks = ['February', 'March', 'April']
plt.xticks(x, x_ticks)
plt.plot(x, controlProps, label='Control')
plt.plot(x, midrangeProps, label='Midrange')
plt.plot(x, devotionProps, label='Devotion')
plt.plot(x, dredgeProps, label='Dredge')
plt.plot(x, aggroProps, label='Aggro')
plt.plot(x, burnProps, label='Burn')
plt.plot(x, aurasProps, label='Auras')
plt.xlabel('Month')
plt.ylabel('Proportion of decks in the Tier 1 Metagame')
plt.title('Evolution of BNG Standard Tier 1 Metagame')
plt.legend()
plt.show()
'''


## FIGURE 2: 25 most relevant cards of BNG Standard
cardCountsTemp = cardCounts
x = range(25)
relevantCardCounts = []
relevantCardNames = []
label_pos = []
for i in range(25):                     # sort cards
    index = cardCountsTemp[0].index(max(cardCountsTemp[0]))
    relevantCardCounts.append(cardCountsTemp[0][index])
    relevantCardNames.append(cardCountsTemp[1][index])
    del cardCountsTemp[0][index]
    del cardCountsTemp[1][index]
    label_pos.append(x[i] + .3)
plt.xticks(label_pos,relevantCardNames,rotation=90)
plt.bar(x,relevantCardCounts)
#plt.show()

# output to bestCards.csv for further visualization
with open('bestCards.csv','wb') as myfile:
    wrtr = csv.writer(myfile, delimiter=',')
    for i in range(len(relevantCardNames)):
        wrtr.writerow([relevantCardNames[i], relevantCardCounts[i]])
    myfile.flush()
    


    
    
    
    
    