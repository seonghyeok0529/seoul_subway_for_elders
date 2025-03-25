# seoul_subway_for_elders

# 🧓 노인을 위한 지하철은 있다

> "서울시 지하철, 정말 노인 친화적인가요?"  
> 본 프로젝트는 고령 인구 증가 시대에 맞춰, 서울시 지하철의 **노인 친화도**를 데이터 기반으로 평가하고, 정책적 제언을 도출한 데이터 분석 프로젝트입니다.

## 📌 프로젝트 개요

- **주제**: 서울시 지하철역의 노인 친화도 분석
- **목적**: 노인 인구의 지하철 이용 편의성 및 안전성을 데이터로 분석하여, 관련 정책 수립 및 시설 개선에 기여
- **데이터 출처**: 서울시 열린데이터광장, 공공데이터포털, 카카오 로컬 API 등
- **사용 기간 데이터**: 2015 ~ 2024년

## 📊 주요 분석 내용

### 🔍 EDA 및 전처리
- 결측치/이상치 처리 (예: 9호선 일부역 데이터 미수집, 3호선 충무로역 구조 이슈 등)
- 환승역 중복 처리
- 좌표 및 주소 기준 통일

### 📈 데이터 분석 및 모델링
- 회귀분석을 통한 무임승차율과 고령화의 관계 분석
- 지하철역별 위험도 점수, 접근성 점수, 노인 친화도 점수 산출
- 클러스터링(K-means) 및 변수 가중치 설정

### 🗺️ 시각화 및 대시보드
- 노인 친화도, 위험도, 접근성 점수 지도 시각화
- 행정구별 시설 편중 여부 분석

## 📌 주요 결론 및 제언

- **청량리, 종로5가역** 등은 노인 친화도가 높음
- **신길, 홍대입구역** 등은 낮은 점수로 개선 필요
- 시설 부족 지역 식별 및 예산 우선 배분 필요
- 지표는 향후 **정책 입지 선정 기준**으로 활용 가능

## 🔧 사용 기술 스택

- **Python** (Pandas, Numpy, Seaborn, Scikit-learn)
- **Jupyter Notebook**, **Google Colab**
- **Kakao API**, **Public Data APIs**
- **Tableau / Folium / matplotlib** (시각화 도구)

## 👥 팀 소개 (6조 - DATNGUE)

- 김선혁, 이유진, 조성학, 최성혁, 최온

## 🔁 회고 및 학습

- 프로젝트 내내 협업 툴(Notion 댓글 기능 등)과 업무 분장을 적극 활용
- 데이터 오류 및 결측 대응 과정에서 문제 해결력 향상
- 주피터 노트북 동시 작업의 한계를 극복하기 위한 노력을 지속함

## 📁 폴더 구조
📂 subway-senior-friendly ├── 📁 data # 데이터셋 및 전처리 결과 ├── 📁 notebooks # 분석 코드(Jupyter Notebook) ├── 📁 reports # 발표자료 및 결과 보고서 ├── 📁 dashboard # 시각화 자료 및 대시보드 이미지 └── README.md


## 📽️ 시연 영상

👉 [시연 영상 링크 삽입 예정]

---

## 📎 참고자료

- 서울시 열린데이터광장
- 공공데이터포털
- 한국경제연구원 노인실태조사
- 행정안전부 인구통계 등

---

💡 **“데이터로 사회 문제 해결에 기여하고 싶다면? 이 프로젝트에서 영감을 받아보세요.”**


[초급프로젝트_발표자료.pdf](https://github.com/user-attachments/files/19441427/_.pdf)
