
from bs4 import BeautifulSoup
import requests
import pandas as pd

# df = pd.DataFrame(columns=['ranking', 'name', 'points', 'link', 'age', 'flag', 'height (cm)', 'weight (lbs)'])
# # url = 'https://www.atptour.com/en/rankings/singles?rankRange=1-5000'
# url = 'https://www.atptour.com/en/rankings/singles'
# url_doubles = 'https://www.atptour.com/en/rankings/doubles?rankRange=1-5000'

def scrape_player(link):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')

    test = soup.find('body', class_='is-desktop' )
    wrapper = test.find('div', class_='wrapper')
    container = wrapper.find('div', class_='container')
    main = container.find('div', id='mainContainer')
    content = main.find('div', id='mainContent')
    player = content.find('div',id='playerProfileHero')
    player_prof = player.find('div', class_='player-profile-hero-overflow')
    table = player_prof.find('div', class_='player-profile-hero-table').find('div', class_='inner-wrap').find('table')

    row1 = table.find_all('tr')[0]
    row2 = table.find_all('tr')[1]

    row1col = row1.find_all('td')
    row2col = row2.find_all('td')

    weight = row1col[2].find('div', class_='wrap').find('div', class_='table-big-value').find('span', class_='table-weight-lbs-wrapper')
    if weight is not None:
        weight = weight.find('span', class_='table-weight-lbs').text.strip()
        weight = int(weight)

    height = row1col[3].find('div', class_='wrap').find('div', class_='table-big-value').find('span', class_='table-height-cm-wrapper')
    if height is not None:
        height = height.text.strip()
        height = int(height[1:-3])
    
    return (height, weight)

    

def scrape_rank(url):
    # url = 'https://www.atptour.com/en/rankings/singles'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    test = soup.find('body', class_='is-desktop' )
    wrapper = test.find('div', class_='wrapper')
    container = wrapper.find('div', class_='container')
    singles = container.find('div', id='mainContainer')
    singlesRanking = singles.find('div', id='singlesRanking')
    tablesRanking = singlesRanking.find('div', class_='table-rankings-wrapper')
    megaTable = tablesRanking.find('table', class_='mega-table')
    tableBody = megaTable.find('tbody')

    root = 'www.atptour.com'
    entries = tableBody.find_all('tr')

    for i, entry in enumerate(entries):
        if i == 10:
            break
        cells = entry.find_all('td')

        player = cells[3]
        player_info = player.find('span')
        player_name = player_info.find('a').text.strip()
        player_link = root + player_info.find('a')['href']
        player_link = player_link.split('/')
        player_link[-1] = 'player-stats'
        player_link = 'http://' + '/'.join(player_link)
        
        height, weight = scrape_player(player_link)
        # print(player_link)

        player_rank = cells[0].text.strip()

        point_data = cells[5]
        player_points = point_data.find('a').text.strip()
        player_points = player_points.replace(',', '')
        player_points = int(player_points)
            

        player_flag = cells[2].div.div.img['alt']

        player_age = cells[4].text.strip()
        try:
            player_age = int(player_age)
        except:
            pass

        # print(player_rank, player_name, player_points, player_link, player_age, player_flag, height, weight)
        yield [player_rank, player_name, str(player_points), str(player_age), player_flag, str(height), str(weight)]
        # df.loc[i] = [player_rank, player_name, player_points, player_link, player_age, player_flag, height, weight ]
        # break

# # scrape_rank(url)
# scrape_rank(url)

# # scrape_player('https://www.atptour.com/en/players/kaichi-uchida/u120/player-stats')

# df = df.set_index('ranking')
# print(df)

# df.to_csv(r'C:\Users\Daniel\VSDiscord\DiscordBot\files\top100.csv')