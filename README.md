
---

# Multi-Agent System Study: Naive vs AutoGen

**Naive(수동 제어)** 방식, 
Microsoft의 **AutoGen 프레임워크**를 활용한 워크플로우 구현

## 📂 프로젝트 구조

```bash
multiagent/
├── .env                        # API 키 관리
├── requirements.txt            # 의존성 라이브러리
├── README.md                   # 프로젝트 설명서
│
├── # 1. Naive System 
├── naive_system/
│   ├── agents/                 # 에이전트 클래스 정의
│   ├── utils/                  # 유틸리티 함수
│   ├── config.py               # 모델 설정
│   ├── pipeline.py             # Naive 워크플로우 로직
│   └── prompts.py              # 프롬프트 템플릿
│
├── # 2. AutoGen System 
├── autogen_system/
│   ├── config.py               # AutoGen 모델 클라이언트 설정
│   ├── agents.py               # 에이전트 정의 (Debater, Verifier, Experts 등)
│   ├── workflow_round_robin.py # [순차] RoundRobin 로직
│   ├── workflow_selector.py    # [동적] Selector 로직
│   └── workflow_graph.py       # [구조] GraphFlow 로직
│
 # 실행 파일 (Entry Points)
├── run_naive.py            # Naive 방식 실행
├── run_autogen_round_robin.py
├── run_autogen_selector.py
└── run_autogen_graph.py

```

---

## 📚 1. Naive 방식 

파이썬 코드로 대화의 순서와 데이터를 직접 제어하는 가장 기초적인 방식입니다.

* **특징:** 개발자가 `Planner` -> `Drafter` -> `Critic` 순서를 직접 하드코딩.
* **한계:** 대화 히스토리 관리, 유연한 순서 변경, 에이전트 간 상호작용 구현이 복잡함.
* **실행:**
```bash
python run_naive.py

```



---

## 🤖 2. AutoGen 방식 

AutoGen 프레임워크를 사용하여 에이전트 간의 자율적인 대화와 협업을 구현했습니다.

### ① Round Robin (순차 순환)

가장 기본적인 형태로, 정해진 순서대로 에이전트들이 발언

* **흐름:** `Debater` ➡ `Verifier` ➡ `Moderator` (무한 반복)
* **특징:**
* 대화 히스토리가 자동으로 공유됨.
* `Verifier`가 승인하여 `Moderator`가 "최종 답변"을 선언하거나, 대화 Turn 수가 10이 넘어가면 종료 조건(`Termination`)에 의해 멈춤.


* **실행:**
```bash
python run_autogen_round_robin.py

```



### ② Selector (동적 선택)

LLM(지능)이 대화 맥락을 파악하여 **"다음에 누가 말할지"** 를 스스로 결정

* **흐름:** 상황에 따라 유동적 (예: 초안이 부족하면 `Debater` 재호출, 완벽하면 바로 `Moderator` 호출)
* **특징:**
* `SELECTOR_PROMPT`에 정의된 규칙에 따라 판단.
* 불필요한 턴을 줄이고 효율적인 협업 가능 (필요한 에이전트만 호출).


* **실행:**
```bash
python run_autogen_selector.py

```



### ③ GraphFlow (구조적 병렬 처리)

복잡한 업무 절차를 **그래프(설계도)** 로 그려서 강제하는 방식

* **흐름:** `Manager(Start)` ➡ `Experts(3명 동시 수행)` ➡ `Manager(Final)`
* **특징:**
* **Fan-Out/Fan-In 구조:** 업무 지시(확산) 후 결과 취합(수렴).
* **병렬 처리:** 서로 다른 전문가들이 동시에 작업하여 속도와 독립성 확보.
* 도미노처럼 연결된 화살표(Edge)를 따라 자동으로 실행됨.


* **실행:**
```bash
python run_autogen_graph.py

```



---

## 📝 요약

| 방식 | 제어 주체 | 특징 | 추천 상황 |
| --- | --- | --- | --- |
| **Naive** | Python Code | 직접 제어 | 아주 단순한 선형 작업 |
| **Round Robin** | List Order | 정해진 순서 반복 | 자유 토론, 단순 피드백 루프 |
| **Selector** | LLM Logic | 상황 보고 다음 사람 지목 | 유동적인 대화, 효율성 중시 |
| **GraphFlow** | Edge Map | 설계된 화살표 따라 이동 | SOP, 병렬 처리 |

---

 


## 🚀 시작 가이드 (Getting Started)

### 1. 환경 설정

Python 3.11.4 환경에서 필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt

```

### 2. API 키 설정

프로젝트 루트에 `.env` 파일을 생성하고 OpenAI API 키를 입력하세요.

```ini
# .env 파일
OPENAI_API_KEY=your_api_key_here

```
