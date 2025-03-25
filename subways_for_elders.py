import pandas as pd
import folium
from flask import Flask, render_template
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from branca.colormap import linear

# 플라스크 애플리케이션 초기화
server = Flask(__name__)

# 지하철 데이터 로드
file_path = 'C:/지하철_데이터_ree.csv'  # 경로 수정 필요
data = pd.read_csv(file_path, encoding='utf-8-sig')

# Pretendard 폰트 적용하는 CSS 스타일 추가
pretendard_font_url = "https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css"

# 무임하차인원 정수 처리
data['무임하차인원'] = data['무임하차인원'].astype(int)

# 소수점 둘째 자리에서 반올림 처리 (접근성 점수, 위험도 점수, 노인 친화도 점수)
data['접근성 점수'] = data['접근성 점수'].round(2)
data['위험도 점수'] = data['위험도 점수'].round(2)
data['노인 친화도 점수 (0~10)'] = data['노인 친화도 점수 (0~10)'].round(2)

# Dash 애플리케이션 초기화 (Flask 서버와 함께)
app = Dash(__name__, server=server, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP, pretendard_font_url])


# 위험도, 접근성, 노인 친화도 점수에 따른 색상 맵핑 (0~10 범위)
colormap_danger = linear.Reds_09.scale(0, 10)
colormap_accessibility = linear.Blues_09.scale(0, 10)
colormap_senior_friendly = linear.Greens_09.scale(0, 10)

# 지도 생성 함수
def create_map(filtered_data, score_type):
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=13)
    
    # 점수 타입에 따라 컬러맵과 점수를 설정
    if score_type == '위험도':
        colormap = colormap_danger
        score_column = '위험도 점수'
        border_color = 'red'  # 테두리 색상: 빨강
    elif score_type == '접근성':
        colormap = colormap_accessibility
        score_column = '접근성 점수'
        border_color = 'blue'  # 테두리 색상: 파랑
    else:
        colormap = colormap_senior_friendly
        score_column = '노인 친화도 점수'
        border_color = 'green'  # 테두리 색상: 초록

    for i, row in filtered_data.iterrows():
        folium.Circle(
            location=[row['위도'], row['경도']],
            radius=row['무임하차인원'] * 0.001,  # 무임하차인원에 따른 버블 크기
            fill=True,
            fill_opacity=0.6,
            color=border_color,  # 테두리 색상 설정
            fill_color=colormap(row[score_column]),  # 내부 색상은 컬러맵에서 설정
            popup=f"{row['역명']} ({score_type.capitalize()} 점수: {row[score_column]}, 무임하차인원: {row['무임하차인원']})"
        ).add_to(m)
        
    colormap.add_to(m)

    return m



# 공통 레이아웃: 위험도, 접근성, 노인친화도 대시보드를 동일하게 처리
def common_layout(dash_id, dropdown_id_line, dropdown_id_station, table_id, title):
    return dbc.Container([
        html.H1(title, style={'text-align': 'center', 'margin-bottom': '20px', 'font-family': 'Pretendard', 'color': '#333'}),
        
        # 지도 섹션
        dbc.Row([dbc.Col(html.Div(id=dash_id), width=12)], style={'padding-bottom': '20px'}),
        
        # 필터링 섹션과 표 섹션
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4("지하철 정보 필터링", style={'color': '#555', 'font-weight': 'bold', 'font-family': 'Pretendard'}),

                    html.Label("호선 선택", style={'margin-top': '10px', 'color': '#666', 'font-family': 'Pretendard'}),
                    dcc.Dropdown(
                        id=dropdown_id_line,
                        options=[{'label': i, 'value': i} for i in sorted(data['호선'].unique())],
                        multi=True,
                        placeholder="호선을 선택하세요",
                        style={'background-color': '#f9f9f9', 'font-family': 'Pretendard'}
                    ),
                    
                    html.Label("역명 선택", style={'margin-top': '10px', 'color': '#666', 'font-family': 'Pretendard'}),
                    dcc.Dropdown(
                        id=dropdown_id_station,
                        options=[],
                        multi=True,
                        placeholder="역명을 선택하세요",
                        style={'background-color': '#f9f9f9', 'font-family': 'Pretendard'}
                    )
                ], style={'background-color': '#f1f1f1', 'padding': '20px', 'border-radius': '5px'})
            ], width=12)
        ], style={'padding-bottom': '20px'}),
        
        # 표 섹션
        dbc.Row([
            dbc.Col([
                html.H4("검색 결과", style={'color': '#333', 'margin-top': '0px','margin-bottom': '5px', 'font-family': 'Pretendard'}),
                dcc.Graph(id=table_id, style={'height': '600px'})  # 표 높이 설정
            ], width=12)
        ])
    ], fluid=True)

# 각 대시보드 레이아웃 함수
def danger_layout():
    return common_layout('map-container-danger', 'line-dropdown-danger', 'station-dropdown-danger', 'table-container-danger', "지하철 위험도 점수 대시보드 (버블 사이즈 = 무임하차인원)")

def accessibility_layout():
    return common_layout('map-container-accessibility', 'line-dropdown-accessibility', 'station-dropdown-accessibility', 'table-container-accessibility', "지하철 노인 접근성 점수 대시보드 (버블 사이즈 = 무임하차인원)")

def senior_friendly_layout():
    return common_layout('map-container-senior-friendly', 'line-dropdown-senior-friendly', 'station-dropdown-senior-friendly', 'table-container-senior-friendly', "지하철 노인 친화도 점수 대시보드 (버블 사이즈 = 무임하차인원)")

# Dash 애플리케이션 레이아웃 설정
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),  # URL 변경 감지
    html.H1("지하철역 평가 지표 대시보드 선택", style={'text-align': 'center', 'margin-bottom': '20px', 'font-family': 'Pretendard', 'color': '#333'}),

    dbc.Row([
        dbc.Col(dbc.Button("위험도 점수 대시보드\n(색상: 위험도 점수)", href='/dash/danger', color="danger", n_clicks=0), width=4),
        dbc.Col(dbc.Button("노인 접근성 점수 대시보드\n(색상: 접근성 점수)", href='/dash/accessibility', color="primary", n_clicks=0), width=4),
        dbc.Col(dbc.Button("노인 친화도 점수 대시보드\n(색상: 노인 친화도 점수)", href='/dash/senior_friendly', color="success", n_clicks=0), width=4)
    ], style={'text-align': 'center', 'margin-top': '50px'}),

    html.Div(id='page-content')
])

# URL 경로에 따라 다른 레이아웃을 렌더링하는 콜백
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/dash/danger':
        return danger_layout()  # 변경된 위험도 점수 레이아웃
    elif pathname == '/dash/accessibility':
        return accessibility_layout()
    elif pathname == '/dash/senior_friendly':
        return senior_friendly_layout()
    else:
        return html.Div([html.H1("지하철 대시보드 선택", style={'text-align': 'center', 'font-family': 'Pretendard'})])

# 필터링 콜백 (예시: 위험도)

@app.callback(
    [Output('map-container-danger', 'children'),
     Output('table-container-danger', 'figure'),
     Output('station-dropdown-danger', 'options')],
    [Input('line-dropdown-danger', 'value'),
     Input('station-dropdown-danger', 'value')]
)
def update_danger_dashboard(selected_lines, selected_stations):
    # 데이터 복사
    filtered_data = data.copy()

    # 호선 선택 시 필터링
    if selected_lines:
        filtered_data = filtered_data[filtered_data['호선'].isin(selected_lines)]

    # 역명 드롭다운 옵션을 선택한 호선에 맞게 동적으로 업데이트
    station_options = [{'label': station, 'value': station} for station in sorted(filtered_data['역명'].unique())]

    # 역명 필터링: 선택된 역명이 있을 경우에만 적용
    if selected_stations and len(selected_stations) > 0:
        filtered_data = filtered_data[filtered_data['역명'].isin(selected_stations)]

    # 지도 생성 함수 호출
    danger_map = create_map(filtered_data, '위험도')
    map_html = danger_map._repr_html_()

    # 표 생성
    table_figure = {
        'data': [{
            'type': 'table',
            'header': {'values': ['호선', '역명', '무임하차인원', '위험도 점수', '연단간격 높음 수', '평균환승거리_m']},
            'cells': {'values': [
                filtered_data['호선'], filtered_data['역명'], 
                filtered_data['무임하차인원'], filtered_data['위험도 점수'],
                filtered_data['연단간격 높음 수'], filtered_data['평균환승거리_m']
            ]}
        }]
    }

    return html.Iframe(srcDoc=map_html, width='100%', height='800px'), table_figure, station_options


# 접근성 대시보드 지도와 표를 업데이트하는 콜백 함수
@app.callback(
    [Output('map-container-accessibility', 'children'),
     Output('table-container-accessibility', 'figure'),
     Output('station-dropdown-accessibility', 'options')],
    [Input('line-dropdown-accessibility', 'value'),
     Input('station-dropdown-accessibility', 'value')]
)
def update_accessibility_dashboard(selected_lines, selected_stations):
    # 필터링 로직
    filtered_data = data.copy()

    # 호선 선택 시 필터링
    if selected_lines:
        filtered_data = filtered_data[filtered_data['호선'].isin(selected_lines)]

    # 역명 드롭다운 옵션을 선택한 호선에 맞게 동적으로 업데이트
    station_options = [{'label': station, 'value': station} for station in sorted(filtered_data['역명'].unique())]

    # 역명 필터링: 선택된 역명이 있을 경우에만 적용
    if selected_stations and len(selected_stations) > 0:
        filtered_data = filtered_data[filtered_data['역명'].isin(selected_stations)]


    # 지도 생성
    accessibility_map = create_map(filtered_data, '접근성')
    map_html = accessibility_map._repr_html_()

    # 표 생성
    table_figure = {
        'data': [{
            'type': 'table',
            'header': {'values': ['호선', '역명', '무임하차인원', '접근성 점수', '전통시장수(500m이내)', '공원', '의료시설']},
            'cells': {'values': [
                filtered_data['호선'], filtered_data['역명'], 
                filtered_data['무임하차인원'], filtered_data['접근성 점수'],
                filtered_data['전통시장수(500m이내)'], filtered_data['공원'], 
                filtered_data['의료시설']
            ]},
            'style': {'font-family': 'Pretendard'}
        }]
    }

    return html.Iframe(srcDoc=map_html, width='100%', height='800px'), table_figure, station_options

# 노인 친화도 대시보드 지도와 표를 업데이트하는 콜백 함수
@app.callback(
    [Output('map-container-senior-friendly', 'children'),
     Output('table-container-senior-friendly', 'figure'),
     Output('station-dropdown-senior-friendly', 'options')],
    [Input('line-dropdown-senior-friendly', 'value'),
     Input('station-dropdown-senior-friendly', 'value')]
)
def update_senior_friendly_dashboard(selected_lines, selected_stations):
    # 필터링 로직
    # 데이터 복사
    filtered_data = data.copy()

    # 호선 선택 시 필터링
    if selected_lines:
        filtered_data = filtered_data[filtered_data['호선'].isin(selected_lines)]

    # 역명 드롭다운 옵션을 선택한 호선에 맞게 동적으로 업데이트
    station_options = [{'label': station, 'value': station} for station in sorted(filtered_data['역명'].unique())]

    # 역명 필터링: 선택된 역명이 있을 경우에만 적용
    if selected_stations and len(selected_stations) > 0:
        filtered_data = filtered_data[filtered_data['역명'].isin(selected_stations)]

    # 지도 생성
    senior_friendly_map = create_map(filtered_data, '노인 친화도')
    map_html = senior_friendly_map._repr_html_()

    # 표 생성
    table_figure = {
        'data': [{
            'type': 'table',
            'header': {'values': ['호선', '역명', '무임하차인원', '노인 친화도 점수', '접근성 점수', '위험도 점수']},
            'cells': {'values': [
                filtered_data['호선'], filtered_data['역명'], 
                filtered_data['무임하차인원'], filtered_data['노인 친화도 점수 (0~10)'],
                filtered_data['접근성 점수'], filtered_data['위험도 점수']
            ]},
            'style': {'font-family': 'Pretendard'}
        }]
    }

    return html.Iframe(srcDoc=map_html, width='100%', height='800px'), table_figure, station_options

# 애플리케이션 실행
if __name__ == '__main__':
    app.run_server(debug=True, port=8056)
