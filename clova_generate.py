#!/usr/bin/env python3
"""
아산시 스마트시티 홍보 영상 - NAVER Clova Voice 나레이션 생성 스크립트

사용법:
1. NAVER Cloud Platform에서 Clova Voice API 키 발급
   - https://www.ncloud.com/product/aiService/clovaVoice
2. 아래 CLIENT_ID, CLIENT_SECRET에 발급받은 키 입력
3. python clova_generate.py 실행
4. 생성된 audio/s0.mp3 ~ s11.mp3 파일을 GitHub 레포에 업로드

추천 음성: 
  - nara (나라, 여성, 자연스러운 뉴스 앵커 스타일)
  - clara (클라라, 여성, 밝고 친근한 스타일)
  - dara (다라, 여성, 차분한 스타일)
"""

import requests, os, time

# ====== 여기에 API 키를 입력하세요 ======
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
VOICE = "nara"  # nara, clara, dara 중 선택
# ========================================

narrations = [
    "안녕하세요. 충청남도 아산시가 추진하는, 강소형 스마트시티 조성사업을 소개합니다. 국토교통부 공모사업으로 선정된 이 사업은, 총 240억 원 규모로, 아산시를 대한민국 대표 스마트시티로 만들어 가고 있습니다.",
    "아산시는 세 가지 도시 과제에 직면해 있습니다. 도고온천 일원의 관광 인프라가 노후화되면서, 지역소멸 위기에 놓여 있고요. 배방 신도시와 서부 구도심 간의, 발전 격차가 점점 벌어지고 있습니다. 데이터 기반의 스마트한 도시 운영도 시급한 상황이에요.",
    "아산시는 두 개의 혁신 거점을 만들고 있어요. 서쪽 도고온천에는, 디지털 오아시스 존을 조성하여, 워케이션과 힐링 관광의 거점으로 탈바꿈시키고요. 동쪽 배방에는 이노베이션 존을 구축하여, AI 인재 양성의 허브로 만듭니다.",
    "도고 디지털 오아시스 존에서는요. 파라다이스 스파 도고 인근에, 디지털 오아시스 스팟이 건립됩니다. 무인매장과 워케이션 공간이 함께 운영되고요. AI CCTV 15대와 스마트폴이 관광객의 안전을 지킵니다.",
    "배방 이노베이션 존의 핵심은요. 호서대학교 KTX 캠퍼스에 구축한, 이노베이션센터입니다. 리빙랩 공간과 통합관제센터를 갖추었고요. SDDC 클라우드 플랫폼이, 모든 서비스의 두뇌 역할을 합니다. KAIST와 호서대의 AI 교육 프로그램이, 지역 청년들의 역량을 키우고 있어요.",
    "도고와 배방을 하나로 연결하는, 통합 서비스 플랫폼을 소개할게요. 모바일 전자시민증은, DID 기반의 디지털 지갑으로, 신분 인증과 할인 혜택을 한 번에 이용할 수 있어요. AI 통합관제 플랫폼은, 영상분석 기반으로 이상 행동을 자동 감지하고요.",
    "수요응답형 교통, DRT 서비스도 준비 중이에요. 앱으로 호출하면, 원하는 시간에 원하는 곳으로 이동할 수 있고요. KTX 천안아산역에서 이노베이션센터를 거쳐, 도고온천까지 동서를 잇는 스마트 교통 노선이 만들어집니다.",
    "이 프로젝트는, 다섯 개 기관의 협력으로 추진되고 있어요. 아산시가 사업을 총괄하고, 제일엔지니어링이 사업 관리를 담당합니다. 호서대학교는 이노베이션센터와 리빙랩을, 충남연구원은 거버넌스와 정책 연구를, KAIST는 첨단 기술 연구와 자문을 맡고 있어요.",
    "리빙랩은, 시민이 직접 참여하여, 도시 문제를 해결하는 혁신 모델이에요. 서로의멘토, 다인연클럽, 엔드롭, 마실기록소, 온화미로까지. 다섯 개 팀이 시민의 아이디어로, 도시를 바꾸고 있습니다.",
    "숫자로 정리해 볼게요. 총 사업비 240억 원. 9개 단위사업. AI CCTV 15대. 5개 참여기관. 5개 리빙랩 팀. 2023년 12월에 시작해서, 2026년 12월 완료를 목표로 달려가고 있습니다.",
    "전자시민증 하나로 편리하게. AI가 24시간 동네를 지키고. 부르면 오는 버스, 스마트한 무인매장. 내 아이디어가 정책이 되는 도시. 이것이 아산 스마트시티가 꿈꾸는 시민의 내일이에요.",
    "스마트한 내일. 아산에서 시작합니다. 감사합니다."
]

os.makedirs("audio", exist_ok=True)

for i, text in enumerate(narrations):
    print(f"Generating scene {i}...")
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": CLIENT_ID,
        "X-NCP-APIGW-API-KEY": CLIENT_SECRET,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "speaker": VOICE,
        "text": text,
        "volume": "0",
        "speed": "-1",     # slightly slower
        "pitch": "0",
        "format": "mp3"
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        with open(f"audio/s{i}.mp3", "wb") as f:
            f.write(response.content)
        print(f"  ✅ s{i}.mp3 ({len(response.content)} bytes)")
    else:
        print(f"  ❌ Error: {response.status_code} - {response.text}")
    
    time.sleep(0.5)

print("\n✅ 모든 나레이션 생성 완료!")
print("audio/ 폴더의 파일을 GitHub 레포에 업로드하세요.")
