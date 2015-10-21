import gzip
from collections import defaultdict

def readGz(f):
  for l in gzip.open(f):
    yield eval(l)

### Helpfulness baseline: similar to the above. Compute the global average helpfulness rate, and the average helpfulness rate for each user

allHelpful = []
userHelpful = defaultdict(list)
items = []

for l in readGz("train.json.gz"):
  user,item = l['reviewerID'],l['itemID']
  allHelpful.append(l['helpful'])
  userHelpful[user].append(l['helpful'])
  items.append(item)
  

averageRate = sum([x['nHelpful'] for x in allHelpful]) * 1.0 / sum([x['outOf'] for x in allHelpful])

userRate = {}
for u in userHelpful:
  userRate[u] = sum([x['nHelpful'] for x in userHelpful[u]]) * 1.0 / sum([x['outOf'] for x in userHelpful[u]])

predictions = open("predictions_Helpful.txt", 'w')
for l in open("pairs_Helpful.txt"):
  if l.startswith("userID"):
    #header
    predictions.write(l)
    continue
  u,i,outOf = l.strip().split('-')
  outOf = int(outOf)
  if u in userRate:
   if outOf >40:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(outOf*userRate[u]-.7) + '\n')
   elif outOf == 1:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(1) + '\n')
   elif outOf == 2:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(2) + '\n') 
   elif outOf < 4:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(outOf*(averageRate+.17)) + '\n')
   elif outOf < 10:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(outOf*(averageRate+.07)) + '\n')
   elif outOf < 20:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(outOf*(averageRate+.09)) + '\n')
   elif outOf < 30:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(outOf*(averageRate+.13)) + '\n')
   elif outOf < 40:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(outOf*(averageRate+.12)) + '\n')
   else:
   	predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(outOf*userRate[u]) + '\n')
  elif outOf == 1:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(1) + '\n') 
  elif outOf == 2:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(2) + '\n') 
  elif outOf < 4:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(outOf*(averageRate+.17)) + '\n')
  elif outOf < 10:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(outOf*(averageRate+.04)) + '\n')
  elif outOf < 20:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(outOf*(averageRate+.06)) + '\n')
  elif outOf < 30:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(outOf*(averageRate+.12)) + '\n')
  else:
    predictions.write(u + '-' + i + '-' + str(outOf) + ',' + str(outOf*(averageRate+.1)) + '\n')

predictions.close()
