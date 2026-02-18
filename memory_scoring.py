import re
from collections import Counter


def score_memory(text: str) -> int:
    """
    메모리 텍스트의 점수를 계산합니다.
    
    Args:
        text: 점수를 계산할 텍스트 (200자 이내 권장)
    
    Returns:
        int: 0-100 사이의 점수
    """
    if not text or len(text.strip()) == 0:
        return 0

    text = text.strip()
    length = len(text)
    score = 30  # 기본 점수

    # -------------------------
    # 1. 길이 점수 (150자 이상 만점)
    # -------------------------
    if length < 20:
        length_score = 0
    elif length < 50:
        length_score = 5
    elif length < 100:
        length_score = 10
    elif length < 150:
        length_score = 13
    else:
        length_score = 15
    score += length_score

    # -------------------------
    # 2. 어휘 다양성 (최대 15)
    # -------------------------
    words = re.findall(r"[가-힣]+", text)
    word_count = len(words)

    if word_count == 0:
        diversity_score = 0
    else:
        unique_ratio = len(set(words)) / word_count
        if unique_ratio < 0.3:
            diversity_score = 0
        elif unique_ratio < 0.5:
            diversity_score = 5
        elif unique_ratio < 0.7:
            diversity_score = 10
        else:
            diversity_score = 15
    score += diversity_score

    # -------------------------
    # 3. 구체성 + 평가성 (대폭 확장, 최대 15)
    # -------------------------
    concrete_patterns = [

        # ── 시간: 숫자 없이 쓰는 경우
        r"오늘|어제|내일|그날|그때|당시|요즘|최근|예전|한동안|언젠가",
        r"아침|점심|저녁|밤|새벽|낮|오전|오후",
        r"주말|평일|휴일|방학|연휴",

        # ── 시간: 숫자 포함
        r"\d{1,2}시|\d{1,2}분|\d+일|\d+주|\d+달|\d+개월|\d+년|\d+월",
        r"\d{4}년",

        # ── 장소: 일상 최빈도
        r"집|방|침대|이불|거실|부엌|화장실",
        r"회사|사무실|학교|교실|강의실|학원",
        r"카페|식당|술집|편의점|마트|가게",
        r"길|골목|거리|횡단보도|신호등",

        # ── 이동 / 동선
        r"버스|지하철|기차|비행기|정류장|역",
        r"출근길|퇴근길|등굣길|하교길",
        r"가던길|오는길",

        # ── 사람 / 관계 (아주 중요)
        r"나|나혼자|혼자",
        r"친구|사람|누군가|그사람",
        r"엄마|아빠|부모|가족",
        r"형|누나|언니|오빠|동생",
        r"선생님|교수|상사|팀장|동료",
        r"연인|애인|남친|여친|전애인",

        # ── 사건 / 활동 (범용)
        r"시험|과제|숙제|공부|수업",
        r"출근|퇴근|야근|지각",
        r"회의|발표|면접|평가",
        r"일|업무|프로젝트",
        r"약속|연락|전화|메시지",
        r"여행|휴식|산책|운동",
        r"잠|수면|꿈",

        # ── 인생 이벤트
        r"입학|졸업|취업|퇴사|이직",
        r"이별|헤어짐|다툼|싸움|화해",
        r"실패|성공|좌절|포기|도전",

        # ── 회상 / 서술 트리거 (아주 중요)
        r"문득|갑자기|괜히",
        r"생각나|떠올랐",
        r"지나고보니|돌이켜보면|지금생각해보면",
        r"그때를생각하면",

        # ── 상태 / 맥락
        r"처음|마지막|계속|자꾸",
        r"아무일도없었지만",
        r"별일아니었지만",
        r"나름대로"
    ]

    concrete_hits = sum(bool(re.search(p, text)) for p in concrete_patterns)

    if concrete_hits == 0:
        concrete_score = 0
    elif concrete_hits <= 3:
        concrete_score = 5
    elif concrete_hits <= 6:
        concrete_score = 10
    else:
        concrete_score = 15
    score += concrete_score

    # -------------------------
    # 4. 문장 구조 (최대 15)
    # -------------------------
    sentence_endings = re.findall(r"[.!?]|다[.]?", text)
    particles = re.findall(r"(은|는|이|가|을|를|에|에서|에게|으로|와|과)", text)

    if len(sentence_endings) == 0 or len(particles) < 2:
        structure_score = 0
    elif len(sentence_endings) < 2:
        structure_score = 5
    elif len(sentence_endings) < 4:
        structure_score = 10
    else:
        structure_score = 15
    score += structure_score

    # -------------------------
    # 5. 감정 강도 (최대 10)
    # -------------------------
    emotion_words = [

        # ── 긍정 (일상)
        "좋다", "좋았", "괜찮", "만족", "편안", "편했다",
        "기분이좋", "기분좋",
        "행복", "기쁨", "즐거움", "설렘", "신났",
        "뿌듯", "든든", "안도", "감사",
        "따뜻", "훈훈",

        # ── 사랑 / 애착
        "사랑", "애정", "정들", "소중",
        "그립", "보고싶", "아끼",
        "의지", "믿었",

        # ── 슬픔 / 다운
        "슬프", "우울", "외롭", "쓸쓸",
        "허무", "공허",
        "눈물", "울었",
        "힘들", "버거웠",
        "지쳤", "피곤",

        # ── 분노 / 짜증
        "화가났", "화났",
        "짜증", "열받",
        "답답", "억울",
        "불쾌", "불편",
        "스트레스",

        # ── 불안 / 걱정
        "불안", "초조", "긴장",
        "걱정", "조마조마",
        "무서웠", "겁났",

        # ── 후회 / 자책
        "후회", "아쉬웠", "아쉽",
        "미안", "자책",
        "부끄러웠", "민망",

        # ── 혼란 / 복합
        "복잡", "미묘",
        "이상했", "낯설",
        "혼란", "어수선",

        # ── 강렬 / 인상
        "강렬", "충격",
        "놀랐", "당황",
        "인상깊",
        "잊히지않",

        # ── 상태형 감정 (매우 중요)
        "기분이이상", "기분이묘",
        "마음이무거웠",
        "마음이아팠",
        "마음이놓였",
        "생각이많아졌",
        "아무생각도안났"
    ]

    emotion_count = sum(text.count(w) for w in emotion_words)

    if emotion_count == 0:
        emotion_score = 0
    elif emotion_count == 1:
        emotion_score = 4
    elif emotion_count == 2:
        emotion_score = 7
    else:
        emotion_score = 10
    score += emotion_score

    # -------------------------
    # 6. 편법 입력 감점
    # -------------------------
    if re.search(r"(.)\1{4,}", text):
        score -= 15

    if word_count > 0:
        most_common = Counter(words).most_common(1)[0][1]
        if most_common / word_count > 0.4:
            score -= 10

    return max(0, min(100, score))
