import pandas as pd
import koreanize_matplotlib
import numpy as np
import matplotlib.pyplot as plt
import folium
from tabulate import tabulate

bike = pd.read_csv('Python/Playground/bike/공공자전거 대여소 정보Mk.2.csv')
bike = bike.drop(columns = ['LCD'])
bike = bike.drop(columns = ['QR'])

sorted(list(set(bike['소재지'])))
sorted(list(set(bike['위도'])))
sorted(list(set(bike['경도'])))
sorted(list(set(bike['설치대수'])))

bike_dist = bike.groupby(['소재지']).sum()
bike_dist = bike_dist.drop(columns=['위도'])
bike_dist = bike_dist.drop(columns=['경도'])

bike_dist_df = pd.DataFrame(bike_dist).sort_values('설치대수',ascending=False)

bike_dist_df.plot(kind=('bar'))

plt.rcParams["figure.figsize"] = (20,10)
# plt.show()

df = pd.DataFrame(index=bike['보관소명'])
df['소재지'] = bike.set_index('보관소명')['소재지']
df['위도'] = bike.set_index('보관소명')['위도']
df['경도'] = bike.set_index('보관소명')['경도']
df['설치대수'] = bike.set_index('보관소명')['설치대수']

# print(df.loc['망원역 1번출구 앞'])

# print(tabulate(df[df['소재지']=='강남구']))

def geocoding(name):
  if name == None:
    return None

  crd=[str(df.loc[name]['위도']), str(df.loc[name]['경도'])]
  return crd

# print(geocoding('강남경찰서'))

#bike_station = df[df['소재지']=='강남구']

for i, row in enumerate(df.values):
  name = df.iloc[i].name
  # ['마포구' 37.5556488 126.9106293 15]
  dist, etitude, longitude, count = row
  crd = geocoding(name)

  
  if i == 0:
    map_ = folium.Map(location=crd, zoom_start=12)

  try:
    marker = folium.CircleMarker(
        crd,
        radius=count/3,
        color='red',
        fill_color='red'
    )
  except Exception as e:
    print(e)
  
  marker.add_to(map_)

# html 파일로 저장, jupyter notebook 사용시 바로 출력 가능
map_.save('Python/Playground/bike/map.html')