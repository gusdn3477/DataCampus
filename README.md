## 👩‍🏫PROJECT 소개


2020 데이터 청년 캠퍼스에서 진행한 아이디어를 토대로 개발한 Django 기반의 웹 프로젝트입니다.

파이썬 외부 라이브러리인 OSMNX를 활용하여 프로젝트를 진행하였습니다. 

(공식 문서 링크 : [https://osmnx.readthedocs.io/en/stable/](https://osmnx.readthedocs.io/en/stable/))

프로젝트는 3가지의 기능으로 이루어져 있습니다. (개발 당시에 사용했던 함수가 현재 deprecated된 함수도 있습니다. 개발 당시에 사용했던 함수 이름을 그대로 사용하겠습니다.)

🗓️ **작업기간** : 2021.4.

👨‍💻 **투입인원** : 1명

📒 **주요 기능** 

- 최적 경로 네비게이션 기능 구현
- 목적지 주변의 공공자전거 정류소 현황 시각화
- 서울특별시 전체 공공자전거 현황 시각화

🌱 **스킬 및 라이브러리**

`HTML5` `CSS3` `Bootstrap` `Kakao REST API` `Google Elevation API` `OSMNX` `Folium`

🌱 **실행 화면**

![메인](https://user-images.githubusercontent.com/46596758/150809739-35b87900-848f-425c-8f08-70a17e8ede0b.PNG)
![비교1](https://user-images.githubusercontent.com/46596758/150809746-f3b29c9c-ce8f-496f-801b-8eb99d803003.PNG)
![비교2](https://user-images.githubusercontent.com/46596758/150809758-f73abbf4-3975-40d3-9c99-ba6af7c96dd7.PNG)
![2번](https://user-images.githubusercontent.com/46596758/150809715-7498a595-4f78-4d1c-8bca-c82cb4d746d7.PNG)
![3번](https://user-images.githubusercontent.com/46596758/150809735-f6ed5a02-2634-48cc-ab58-33ebb5d806b6.PNG)

## 🌍PROJECT에서 담당한 부분

1) 최적 경로 네비게이션 기능 구현

- conda 가상환경을 통하여 OSMNX 라이브러리를 설치하였습니다.
- OSMNX의 **graph_from_place** 함수를 사용하여 서울특별시의 bike용 도로망을 내려받았습니다.
- 다운받은 도로망에 Google Elevation API와 연동하여 경사도 정보를 받아오는 **add_node_elevations, add_edge_grades** 함수를 사용하여 도로망에 경사도를 추가하였습니다.
- 경사도를 바탕으로 최소 에너지 소비 공식을 이용하여 데이터프레임에 새로운 열을 만들었습니다.
- 출발지와 도작지를 입력받은 후, KAKAO 장소검색 API를 통하여 출발지와 목적지의 데이터를 얻어왔고, 키 값이 y, x로 되어있는 위경도값을 추출해 내었습니다.
- **get_nearest_node** 함수를 사용하여 위에서 추출한 위경도를 바탕으로 다운받은 도로망에서 가장 가까운 노드를 찾고, **get_shortest_path** 함수의 가중치에 최소 에너지 소비 공식을 활용한 데이터를 두고 최적 경로를 구했습니다.
- 최적 경로를 구한 뒤, html 파일로 저장 후 렌더링 해주었습니다.

2) 검색한 지역 주변의 공공자전거 정류장 현황 시각화 

- 서울특별시 공공자전거 실시간 대여정보 API에서 얻어온 정보를 데이터프레임에 저장하였습니다. 이 과정에서 현재 자전거 수/ 거치대 갯수를 계산하여 충원율이라는 새로운 열을 만들었습니다.
- 출발지와 도작지를 입력받은 후, KAKAO 장소검색 API에 get 방식을 활용하여 출발지와 목적지의 정보를 얻어왔고, 데이터 안에 키 값이 y, x로 되어있는 위경도값을 추출해 내었습니다.
- 반경 1KM 안에 있는 정류장 이름, 총 거치대 갯수, 남아있는 자전거 수, 충원율 지도 상에 그려줍니다. (haversine 함수 사용)

3) 서울특별시 전체 공공자전거 현황 시각화

- 서울특별시 공공자전거 실시간 대여정보 API에서 얻어온 정보 전체를 활용하여 정류장 이름, 총 거치대 갯수, 남아있는 자전거 등을 지도 상에 표시하였습니다.
- **markercluster** 함수를 사용하여 군집도를 시각화하였습니다.


👨‍💻 **사용법**  

아래는 osmnx를 설치하기 위한 가상환경 설치법입니다.  
`conda config --prepend channels conda-forge`  
`conda create -n ox --strict-channel-priority osmnx`  
가상환경 설치 후, 가상환경 안에서 django를 설치 후, 실행시키시면 됩니다.
