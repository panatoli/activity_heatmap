# $ python3 -m venv .venv
# $ source .venv/bin/activate
# $ python3 heatmap.py
# ...
# $ deactivate

import os
import calplot
import numpy as np; np.random.seed(sum(map(ord, 'calplot')))
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Load and parse the CSV
df = pd.read_csv('log.csv', keep_default_na=False, parse_dates=['Date'])

#print(df)
#print(df['Games'])

# Ensure we only have the two necessary columns and correct types
#df = df[['Date', 'Finska']].dropna()
#df['value'] = pd.to_numeric(df['Game#'], errors='coerce')  # ensure numeric

# Set 'Date' as datetime index
df.set_index('Date', inplace=True)

#daily_values = df['Finska']
#print(daily_values)

# Plot the heatmaps

# Heatmaps for Games

# Validate Games
row_sets = df['Games'].str.lower().str.split(',').apply(set)
all_games = set().union(*row_sets)
all_games = sorted(set([g.strip() for g in all_games]))

print("Found the following games: ", '\n'.join(all_games))

df['Game#'] = df.apply(lambda row: np.nan if not row['Games'] else len(row['Games'].split(',')), axis=1)

GAMES=['yahtzee', 'pandemic', 'backgammon','carcassone', 'sushi go', '3d ttt', 'ticket to ride', '101']

plt.tight_layout()

imgs = []
for game in GAMES:
  series = df.apply(lambda row: 1 if game in row['Games'].lower() else np.nan, axis=1)
  fig, axes = calplot.calplot(series, colorbar=False, cmap='binary_r', how=None, figsize=(10,2), yearlabels=False)
  fig.suptitle(game.capitalize(), fontsize=15)
  TMP = game + '.png'
  fig.savefig(TMP)
  plt.close(fig)
  imgs.append(Image.open(TMP))
  os.remove(TMP)

# Plot the number of games per day also
series = df['Game#']
#print(series)
fig, axes = calplot.calplot(series, colorbar=True, cmap='YlGn', how=None, figsize=(20,3), yearlabels=False)
fig.suptitle("Games played by day", fontsize=20)
TMP = 'games.png'
fig.savefig(TMP)
plt.close(fig)
all_games_img = Image.open(TMP)
os.remove(TMP)

# Combine vertically
hgap = 20
vgap = 30
width = max(img.width for img in imgs) * 2 + hgap
height = all_games_img.height + vgap + (sum(img.height for img in imgs) + vgap * len(imgs)) // 2
combined = Image.new('RGB', (width, height), (255, 255, 255))

combined.paste(all_games_img, (10, 0))
current_y = all_games_img.height + vgap//2
for img in imgs[:len(imgs)//2]:
    combined.paste(img, (0, current_y))
    current_y += img.height + vgap  # Update the y-coordinate for the next image
current_y = all_games_img.height + vgap//2
for img in imgs[len(imgs)//2:]:
    combined.paste(img, (hgap+width//2, current_y))
    current_y += img.height + vgap  # Update the y-coordinate for the next image

#combined.show()
combined.save('games.png')


# Heatmaps for Sports

# Validate
row_sets = df['Sports'].str.lower().str.split(',').apply(set)
all_sports = set().union(*row_sets)
all_sports = sorted(set([g.strip() for g in all_sports]))

print("\nFound the following sports: ", '\n'.join(all_sports))

SPORTS=["cycling", "swimming", "finska"]

imgs = []
for sport in SPORTS:
  series = df.apply(lambda row: 1 if sport in row['Sports'].lower() else np.nan, axis=1)
  fig, axes = calplot.calplot(series, colorbar=False, cmap='flag_r', how=None, figsize=(20,4), yearlabels=False)
  fig.suptitle(sport.capitalize(), fontsize=20)
  TMP = sport + '.png'
  fig.savefig(TMP)
  plt.close(fig)
  imgs.append(Image.open(TMP))
  os.remove(TMP)

# Combine vertically
vgap = 30
width = max(img.width for img in imgs)
height = sum(img.height for img in imgs) + vgap * len(imgs)
combined = Image.new('RGB', (width, height), (255, 255, 255))

current_y = vgap//2
for img in imgs:
    combined.paste(img, (0, current_y))
    current_y += img.height + vgap  # Update the y-coordinate for the next image

#combined.show()
combined.save('sports.png')

# Heatmaps for Other Learning

# Validate
row_sets = df['Other Learning'].str.lower().str.split(',').apply(set)
other = set().union(*row_sets)
other = sorted(set([g.strip() for g in other]))

print("\nFound the following activities: ", '\n'.join(other))
exit

ACTIVITIES=["reading", "math", "chess", "coding", "electronics", "russian"]

imgs = []
for a in ACTIVITIES:
  series = df.apply(lambda row: 1 if a in row['Other Learning'].lower() else np.nan, axis=1)
  fig, axes = calplot.calplot(series, colorbar=False, cmap='flag_r', how=None, figsize=(20,4), yearlabels=False)
  fig.suptitle(a.capitalize(), fontsize=20)
  TMP = a + '.png'
  fig.savefig(TMP)
  plt.close(fig)
  imgs.append(Image.open(TMP))
  os.remove(TMP)

# Combine vertically
vgap = 30
width = max(img.width for img in imgs)
height = sum(img.height for img in imgs) + vgap * len(imgs)
combined = Image.new('RGB', (width, height), (255, 255, 255))

current_y = vgap//2
for img in imgs:
    combined.paste(img, (0, current_y))
    current_y += img.height + vgap  # Update the y-coordinate for the next image

#combined.show()
combined.save('Learning.png')

