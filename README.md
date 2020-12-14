[문제 1] 범죄 데이터 획득
=============
!['crime_2019.txt' 데이터 파일의 모습](image/0..JPG)


[문제 2] 범죄 데이터프레임 정리
=============
![crime_2019 데이터프레임의 내용](image/1.png)


[문제 3] 범죄 발생 건수 정규화
=============
![범죄 발생 건수를 자치구별 상대적 수치로 정규화한 결과](image/2.png)


[문제 4] 범죄 발생 비율 계산
=============
![범죄 발생 건수를 자치구별 (인구 십만 명 당) 비율로 계산한 결과](image/3.png)


[문제 5] 구청 좌표 획득
=============
![구글 지도 API를 활용하여 획득한 구청 좌표 1](image/4-1.png)
![구글 지도 API를 활용하여 획득한 구청 좌표 2](image/4-2.png)
![구글 지도 API를 활용하여 획득한 구청 좌표 3](image/4-3.png)


[문제 6] 범죄 발생 시각화
=============
![정규화된 범죄 발생 지표의 히트맵](image/5.png)


[문제 7] 범죄 검거 시각화
=============
![범죄 검거율의 히트맵](image/6.png)


[문제 8] 범죄 간 상관성 분석
=============
![범죄 간 상관계수 히트맵](image/7.png)


[문제 9] 인구/CCTV 및 범죄 상관성 분석
=============
![인구/CCTV 및 범죄 발생 간 상관계수 히트맵](image/8.png)


[문제 10] 인구/CCTV 및 검거 상관성 분석
=============
![인구/CCTV 및 범죄 검거 간 상관계수 히트맵](image/9.png)


[문제 11] 살인 건수 시각화
=============
![살인 건수 단계구분도](image/10.png)


[문제 12] 살인 비율 시각화
=============
![살인 비율 단계구분도](image/11.png)


[문제 13] 검거율 및 살인 비율 시각화
=============
![검거율 및 살인 비율 단계구분도](image/12.png)


[문제 14] 로컬 호스트에서 Covid19 시각화
=============
![로컬 호스트에서 Covid19 시각화](image/13.png)


[문제 15] 리모트 서버에서 Covid19 시각화
=============
![리모트 서버에서 Covid19 시각화](image/14.png)

_________________________________________________________________________________________________________________________________________________________________________________

[문제 1] 범죄 데이터 획득
=============


[문제 2] 범죄 데이터프레임 정리
=============
```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import folium
import json
from folium.features import DivIcon

%matplotlib inline

# 운영체제에 맞는 글꼴 지정
import platform

path = "c:/Windows/Fonts/gulim.ttc" # malgun.ttf"
from matplotlib import font_manager, rc
if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
    print('윈도우 운영체제: ' + font_name )
else:
    print('Unknown system... sorry~~~~') 
    
from sklearn.preprocessing import MinMaxScaler
import googlemaps

crime_2019=pd.read_csv("crime_2019.txt",sep='\t')
crime_2019 =crime_2019.iloc[2:,4:]
crime_2019.columns =['살인발생','살인검거','강도발생','강도검거','강간발생','강간검거','절도발생','절도검거','폭력발생','폭력검거']

crime_2019['절도발생'] =crime_2019['절도발생'].str.replace(",","").astype("int")
crime_2019['강간검거'] =crime_2019['강간검거'].str.replace(",","").astype("int")
crime_2019['강간발생'] =crime_2019['강간발생'].str.replace(",","").astype("int")
crime_2019['절도검거'] =crime_2019['절도검거'].str.replace(",","").astype("int")
crime_2019['폭력발생'] =crime_2019['폭력발생'].str.replace(",","").astype("int")
crime_2019['폭력검거'] =crime_2019['폭력검거'].str.replace(",","").astype("int")

crime_2019['살인발생'] = crime_2019['살인발생'].astype("int")
crime_2019['살인검거'] = crime_2019['살인검거'].astype("int")
crime_2019['강도발생'] = crime_2019['강도발생'].astype("int")
crime_2019['강도검거'] = crime_2019['강도검거'].astype("int")

crime_2019['강간검거율'] = (crime_2019['강간검거'] /crime_2019['강간발생']*100).round(2)
crime_2019['강도검거율'] = (crime_2019['강도검거'] /crime_2019['강도발생']*100).round(2)
crime_2019['살인검거율'] = (crime_2019['살인검거'] /crime_2019['살인발생']*100).round(2)
crime_2019['절도검거율'] = (crime_2019['절도검거'] /crime_2019['절도발생']*100).round(2)
crime_2019['폭력검거율'] = (crime_2019['폭력검거'] /crime_2019['폭력발생']*100).round(2)



crime_2019=crime_2019.iloc[:,[0,2,4,6,8,10,11,12,13,14]]
crime_2019.columns = ['살인','강도','강간','절도','폭력','강간검거율','강도검거율','살인검거율','절도검거율','폭력검거율']

cctv_pep= pd.read_csv('pop_cctv_2018.csv')
cctv_pep=cctv_pep[['자치구','인구 규모 2018','CCTV 규모 2018']]
cctv_pep =cctv_pep.set_index("자치구")
cctv_pep.columns = ['인구규모','CCTV 규모']
crime_2019.index =cctv_pep.index

crime_2019 = pd.concat([crime_2019,cctv_pep],axis=1)
crime_2019
```

[문제 3] 범죄 발생 건수 정규화
=============
```python
crime_2019_norm=crime_2019.iloc[:,:5]
scaler = MinMaxScaler() 
scaled_values = scaler.fit_transform(crime_2019_norm) 
crime_2019_norm.loc[:,:] = scaled_values
crime_2019_norm =crime_2019_norm.round(2)
crime_2019_norm
```

[문제 4] 범죄 발생 비율 계산
=============
```python
crime_2019_per_capita= crime_2019.iloc[:,:5]

crime_2019_per_capita['살인'] = (crime_2019_per_capita['살인']/crime_2019['인구규모']*100000).round(2)
crime_2019_per_capita['강도'] = (crime_2019_per_capita['강도']/crime_2019['인구규모']*100000).round(2)
crime_2019_per_capita['강간'] = (crime_2019_per_capita['강간']/crime_2019['인구규모']*100000).round(2)
crime_2019_per_capita['절도'] = (crime_2019_per_capita['절도']/crime_2019['인구규모']*100000).round(2)
crime_2019_per_capita['폭력'] = (crime_2019_per_capita['폭력']/crime_2019['인구규모']*100000).round(2)
crime_2019_per_capita
```

[문제 5] 구청 좌표 획득
=============
```python
gmaps_key = "AIzaSyAcZ06-jrG7GlBiv7d7YUK1GmgVrOpBg3o" 
gmaps = googlemaps.Client(key=gmaps_key)
station_name = []
for city in list(crime_2019.index):
    station_name.append(city+'청')

station_addreess = []  
station_lat = []       
station_lng = []       
for name in station_name:                               
    tmp = gmaps.geocode(name, language='ko')                
    station_addreess.append(tmp[0].get("formatted_address")) 
    tmp_loc = tmp[0].get("geometry")                         
    station_lat.append(round(tmp_loc['location']['lat'],6))          
    station_lng.append(round(tmp_loc['location']['lng'],6))         

lat_log = pd.DataFrame([station_lat,station_lng]).T.round(6)
name = pd.DataFrame(station_name)
office=pd.concat([name,lat_log],axis=1)
office.columns = ['자치구청','위도','경도']
office=office.set_index(crime_2019.index)
office
```

[문제 6] 범죄 발생 시각화
=============
```python
crime_2019_norm['total'] = crime_2019_norm.sum(axis=1)
crime_2019_norm =crime_2019_norm.reset_index().sort_values("total",ascending=False)
crime_2019_norm=crime_2019_norm.set_index("자치구").iloc[:,:5]
target_col = ['살인', '강도', '강간', '절도', '폭력']
plt.figure(figsize = (10,10))
sns.heatmap(crime_2019_norm, annot=True, fmt='.2f', linewidths=2, cmap='Reds')  
plt.title('정규화된 범죄 발생 지표')
plt.show()
```

[문제 7] 범죄 검거 시각화
=============
```python
ratio_data= crime_2019[['살인검거율','강도검거율','강간검거율','절도검거율','폭력검거율']]
ratio_data['total'] = ratio_data.sum(axis=1)
ratio_data =ratio_data.reset_index()
ratio_data=ratio_data.sort_values("total",ascending=False)
ratio_data=ratio_data.set_index("자치구").iloc[:,:5]
ratio_data=ratio_data.iloc[1:,:]
target_col = ['살인', '강도', '강간', '절도', '폭력']
plt.figure(figsize = (10,10))
sns.heatmap(ratio_data, annot=True, fmt='.2f', linewidths=2, cmap='Blues')
plt.title('범죄 검거율(검거율 합계로 정렬하되, 종로구 빼고)')
plt.show()
```

[문제 8] 범죄 간 상관성 분석
=============
```python
ratio_data= crime_2019[['살인검거율','강도검거율','강간검거율','절도검거율','폭력검거율']]
ratio_data['total'] = ratio_data.sum(axis=1)
ratio_data =ratio_data.reset_index()
ratio_data=ratio_data.sort_values("total",ascending=False)
ratio_data=ratio_data.set_index("자치구").iloc[:,:5]
ratio_data=ratio_data.iloc[1:,:]
target_col = ['살인', '강도', '강간', '절도', '폭력']
plt.figure(figsize = (10,10))
sns.heatmap(ratio_data, annot=True, fmt='.2f', linewidths=2, cmap='Blues')
plt.title('범죄 검거율(검거율 합계로 정렬하되, 종로구 빼고)')
plt.show()
```

[문제 9] 인구/CCTV 및 범죄 상관성 분석
=============
```python
corr_pep =crime_2019[['살인','강도','강간','절도','폭력','인구규모','CCTV 규모']].corr()
corr_pep= corr_pep[['인구규모','CCTV 규모']].iloc[:5,:]
target_col = ['인구규모','CCTV 규모']
plt.figure(figsize = (1.5,3))
sns.heatmap(corr_pep, annot=True, fmt='.2f', cmap='Reds')     
plt.show()
```

[문제 10] 인구/CCTV 및 검거 상관성 분석
=============
```python
c_corr =crime_2019[[ '살인검거율', '강도검거율', '강간검거율', '절도검거율','폭력검거율','인구규모','CCTV 규모']].corr()
c_corr= c_corr[['인구규모','CCTV 규모']].iloc[:5,:]
target_col = ['인구규모','CCTV 규모']
plt.figure(figsize = (1.5,3))
sns.heatmap(c_corr, annot=True, fmt='.2f', cmap='RdYlGn_r' )  
plt.show()
```

[문제 11] 살인 건수 시각화
=============
```python
map_data = pd.concat([crime_2019,office],axis=1)

geo_path = './skorea_municipalities_geo_simple.json'
geo_str = json.load(
    open(geo_path, encoding='utf-8'))

map = folium.Map(
    location=[37.5502, 126.982], zoom_start=11)
map.choropleth(
    geo_data = geo_str,
    data = map_data['살인'],
    columns = [map_data.index, map_data['살인']],
    fill_color = 'PuRd',    # PuRd, YlGnBu
    key_on = 'feature.id')
for n in list(map_data.index):
    text = f"{n}<br>{map_data['살인'][n]}({crime_2019_norm['살인'][n]})"
    folium.map.Marker(
        [map_data['위도'][n] * 1.0000, map_data['경도'][n] * 0.9999], 
        icon=DivIcon(
            icon_size=(150, 40),
            icon_anchor=(0, 10),
            html=f'<div style="font-size: 8pt">{text}</div>'
        )
    ).add_to(map)
map
```

[문제 12] 살인 비율 시각화
=============
```python
map_data['살인발생비율'] = (map_data['살인']/map_data['인구규모']*100000).round(2)

map = folium.Map(
    location=[37.5502, 126.982], zoom_start=11)

map.choropleth(
    geo_data = geo_str,
    data = map_data['살인발생비율'],
    columns = [map_data.index, map_data['살인발생비율']],
    fill_color = 'PuRd',   
    key_on = 'feature.id')
for n in list(map_data.index):
    text = f"{n}<br>{map_data['살인발생비율'][n]}({crime_2019_norm['살인'][n]})"
    folium.map.Marker(
        [map_data['위도'][n] * 1.0000, map_data['경도'][n] * 0.9999], 
        icon=DivIcon(
            icon_size=(150, 40),
            icon_anchor=(0, 10),
            html=f'<div style="font-size: 8pt">{text}</div>'
        )
    ).add_to(map)
map
```

[문제 13] 검거율 및 살인 비율 시각화
=============
```python
map = folium.Map(
    location=[37.5502, 126.982], zoom_start=11)
map.choropleth(
    geo_data = geo_str,
    data = map_data['살인발생비율'],
    columns = [map_data.index, map_data['살인발생비율']],
    fill_color = 'PuRd',   
    key_on = 'feature.id')

for n in map_data.index:
    folium.CircleMarker(
        [map_data['위도'][n], map_data['경도'][n]], 
        radius = map_data['살인검거율'][n]/3.5, 
        color='#3186cc', fill_color='#3186cc', fill=True, popup= map_data['살인검거율'][n],
    ).add_to(map)
    text = f"{n}<br>{map_data['살인발생비율'][n]}({crime_2019_norm['살인'][n]})"
    folium.map.Marker(
        [map_data['위도'][n] * 1.0000, map_data['경도'][n] * 0.9999], 
        icon=DivIcon(
            icon_size=(150, 40),
            icon_anchor=(0, 10),
            html=f'<div style="font-size: 8pt">{text}</div>'
        )
    ).add_to(map)
map
```

[문제 14] 로컬 호스트에서 Covid19 시각화
=============


[문제 15] 리모트 서버에서 Covid19 시각화
=============
제출자의 깃허브 저장소 주소: 
제출자의 파이썬애니웨어 웹 사이트 주소: http://sgeya7.pythonanywhere.com/








