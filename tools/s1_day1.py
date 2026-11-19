# -*- coding: utf-8 -*-
"""1일차 — 화요일, 여섯 시의 배포"""


def build(S):
    S.line(ch="1일차 · 화요일", bg="office_day", bgm="day",
           text="화요일 아침, 사무실 창가에는 어제보다 조금 더 많은 먼지가 떠 있었다.")
    S.line(text="어제 하람이 그려 준 사각형 두 개를 종이에서 화면으로 옮겼다. 여백을 넣었더니 진짜로 덜 답답해졌다.")
    S.line(show={"id": "haram", "expr": "base"}, who="오하람", text="어때요? 다르죠?")
    S.line(who="나", text="…이상하네요. 아무것도 안 넣었는데 좋아졌어요.")
    S.line(who="오하람", e="blush", text="그게 디자인이에요. 물감보다 여백이 더 비싸요.")
    S.line(text="그녀가 내 화면을 보다가, 손가락으로 모니터를 짚었다. 아주 살짝, 화면에서 2센티미터 떨어진 곳을.")
    S.line(who="오하람", text="여기, 날짜랑 금액 사이요. 여기서 사람이 한 번 숨 쉬어요. 그 숨 쉬는 자리를 아껴 주는 거예요.")

    S.choice([
        {"t": "“그럼 지금 바로 넣어 볼게요.”", "to": "p_gap_do",
         "eff": {"haram": 2}, "flag": "spacing"},
        {"t": "“여백이 왜 필요한지는 알겠는데, 기준을 모르겠어요.”", "to": "p_gap_ask",
         "eff": {"haram": 2}},
        {"t": "“나중에 시간 될 때 해 볼게요.”", "to": "p_gap_later",
         "eff": {"haram": 0}},
    ])

    S.label("p_gap_do")
    S.line(text="그 자리에서 사각형을 하나 넣었다. 화면이 조금 비어 보였고, 그게 이상하게 좋았다.")
    S.line(who="오하람", e="surprised", text="지금 했어요?")
    S.line(who="나", text="빨리 해 보고 싶어서요.")
    S.line(who="오하람", e="base", text="…좋아요. 그 마음, 삼 주만 유지해요. 그러면 진짜가 돼요.")
    S.goto("p_gap_after")

    S.label("p_gap_ask")
    S.line(who="오하람", e="base", text="기준은 없어요. 대신 순서가 있어요. 글자, 여백, 그다음 색. 색부터 하면 다 예뻐 보이는데 안 읽혀요.")
    S.line(who="나", text="그럼 여백은 두 번째네요.")
    S.line(who="오하람", text="네. 사람들이 제일 많이 건너뛰는 두 번째요.")
    S.line(text="그녀가 종이를 접어 내 책상 모서리에 세워 두었다. 여백이 없는 종이 조각이, 여백 이야기를 하고 있었다.")
    S.goto("p_gap_after")

    S.label("p_gap_later")
    S.line(who="오하람", e="base", text="네, 나중에요. 나중은 이번 주 안에만요.")
    S.line(who="나", text="이번 주 안이면 나중이 아니잖아요.")
    S.line(who="오하람", text="회사에서 나중은 다 이번 주 안이에요. 저도 그렇게 배웠어요.")
    S.line(text="농담처럼 웃고 지나갔는데, 책상 위의 종이는 일주일 내내 그 자리에 서 있었다.")

    S.label("p_gap_after")
    S.line(text="배포는 여섯 시. 하루 종일 그 숫자만 눈에 밟혔다.")
    S.line(text="다섯 시, 청구서 목록의 마지막 예외를 처리했다. 서버가 내려주는 날짜 형식이 회사마다 달라서, 하나는 콜론이 있고 하나는 없었다.")
    S.line(text="정규식 하나로 둘 다 잡히게 고쳤다. 테스트도 통과했다. 스테이징에서 세 번 확인했다.")
    S.line(text="그런데 세 번 확인한 사람은, 네 번째를 확인하지 않는다.")

    S.line(text="다섯 시 오십 분, 서윤이 내 뒤에 섰다. 정말로 숨소리가 들렸다.")
    S.line(show={"id": "seoyun", "expr": "base"}, who="한서윤", text="뭐 바꿨어요?")
    S.line(who="나", text="날짜 파서요. 형식이 두 개로 와서요.")
    S.line(who="한서윤", text="테스트는?")
    S.line(who="나", text="세 개 돌렸어요.")
    S.line(who="한서윤", e="serious", text="세 개 돌린 걸 자랑처럼 말하지 마세요. 세 개 중에 몇 개가 실제 데이터였어요?")
    S.line(text="대답을 못 했다. 그녀는 내 화면을 한 번 훑고, 아무 말 없이 자기 자리로 갔다.")

    S.line(bgm="day", text="여섯 시. 배포 버튼이 초록색으로 바뀌었다. 사무실에서 박수가 두 번 나왔다. 두 번이면 이 회사에서는 성대한 축하에 속한다.")
    S.line(text="육 시 이십 분. 아무 일도 없었다.")
    S.line(text="육 시 사십 분. 슬랙 알림이 울렸다.")
    S.line(text="「청구서 목록에서 금액이 Invalid Date로 표시됩니다」 — 고객지원 팀, 첨부 스크린샷 한 장.")

    S.line(bg="office_night", bgm="tense", show={"id": "seoyun", "expr": "serious"}, who="한서윤",
           text="롤백해요. 지금 바로.")
    S.line(who="나", text="원인은… 제가 찾아볼게요.")
    S.line(who="한서윤", text="원인은 내일 찾아도 돼요. 지금은 되돌려요. 되돌리는 데 삼 분, 찾는 데 세 시간이면 순서는 정해져 있어요.")
    S.line(text="손이 떨려서 버튼을 두 번 눌렀다. 롤백은 이 분 만에 끝났다. 사무실이 조용해졌다.")

    S.line(text="사람들이 하나둘 일어났다. 누군가는 다음 배포를 확인하고, 누군가는 고객지원 답변을 쓰고.")
    S.line(text="나는 아직 자리에 앉아 있었다. 화면에는 방금 되돌린 코드가 그대로 남아 있었다.")
    S.line(text="서윤이 옆 의자를 당겨 앉았다. 이렇게 가까이 앉은 건 처음이었다.")

    S.choice([
        {"t": "“제가 틀렸어요. 파서를 제가 짰어요.” 먼저 말한다.", "to": "p_own",
         "eff": {"seoyun": 3}, "flag": "own_bug"},
        {"t": "로그부터 다시 본다. 원인을 확실히 알고 말한다.", "to": "p_log",
         "eff": {"seoyun": 2}},
        {"t": "“테스트는 통과했어요.” 변명부터 한다.", "to": "p_excuse",
         "eff": {"seoyun": 0}},
    ])

    S.label("p_own")
    S.line(who="한서윤", e="surprised", text="…알아요. 롤백하면서 봤어요.")
    S.line(who="나", text="그럼 왜 안 혼내세요?")
    S.line(who="한서윤", e="base", text="혼내는 건 원인을 모를 때 하는 거예요. 원인을 아는 사람한테는 다음 걸 물어요.")
    S.line(who="한서윤", text="다음에 같은 게 오면, 어떻게 할 거예요?")
    S.line(who="나", text="…형식이 두 개인 걸 먼저 확인하고, 두 번째는 실제 데이터로 돌려 볼게요.")
    S.line(who="한서윤", e="base", text="좋아요. 그럼 오늘은 그거까지만 해요. 나머지는 내일.")
    S.line(text="그녀가 일어나 커피 머신 쪽으로 갔다. 두 캔을 들고 돌아왔다. 하나는 내 앞에 놓았다.")
    S.line(who="한서윤", text="마시고, 십 분 쉬고, 다시 봐요.")
    S.goto("p_after_own")

    S.label("p_log")
    S.line(text="로그를 뒤졌다. 롤백한 코드, 요청 파라미터, 응답 헤더. 십 분쯤 지났을 때 그녀가 말했다.")
    S.line(who="한서윤", text="정규식이에요.")
    S.line(who="나", text="네?")
    S.line(who="한서윤", e="base", text="콜론 있는 형식만 잡고 있어요. 서버가 이번 배포에서 콜론을 뺐어요. 우리 쪽 변경이 아니라, 그쪽 변경이에요.")
    S.line(text="확인해 보니 정말이었다. 나는 우리 코드만 봤다. 세상이 우리 코드대로만 움직인다고 생각한 셈이다.")
    S.line(who="나", text="…그럼 제 잘못은, 그걸 못 봤다는 거네요.")
    S.line(who="한서윤", text="네 잘못은, 한 번 더 안 물어본 거예요. 사람은 원래 한 번만 확인해요. 그 한 번을 어디에 쓸지가 일이에요.")
    S.goto("p_after_own")

    S.label("p_excuse")
    S.line(who="나", text="테스트는 통과했어요. 형식이 두 개인 줄 알았는데, 하나는 저희 쪽이 아니라 서버가 바꾼 거라서요.")
    S.line(who="한서윤", e="serious", text="그래서요.")
    S.line(who="나", text="…네?")
    S.line(who="한서윤", text="테스트가 통과한 건 사실이고, 서버가 바꾼 것도 사실이에요. 그 두 개가 사실이면 고객 화면에 표시된 잘못된 날짜도 사실이 아니게 되나요?")
    S.line(text="대답이 안 나왔다. 그녀는 한참 나를 보다가, 조용히 말했다.")
    S.line(who="한서윤", e="base", text="변명은 회의실에서 하세요. 여기서는 원인만 얘기해요. 저는 지금 혼내려고 온 게 아니에요.")
    S.goto("p_after_own")

    S.label("p_after_own")
    S.line(text="배포는 되돌렸고, 사무실은 다시 조용해졌다. 창밖의 성수동은 이미 불이 다 켜져 있었다.")
    S.line(text="여덟 시가 넘었다. 남은 사람은 셋. 서윤, 나, 그리고 아직 자리를 지키고 있는 하람.")
    S.line(show2={"id": "haram", "expr": "serious"}, who="오하람", text="수습님, 저 그거 봤어요. 방금.")
    S.line(who="나", text="…부끄럽네요.")
    S.line(who="오하람", text="아니요, 부끄러운 거 맞는데, 저는 다른 것도 봤어요. 롤백 버튼 누를 때 손 안 떨리던 거.")
    S.line(who="나", text="떨렸어요. 두 번 눌렀어요.")
    S.line(who="오하람", e="base", text="그럼 더 좋네요. 떨려도 눌렀잖아요.")

    S.line(hide2=True, text="하람이 먼저 들어갔다. 남은 둘은 각자 화면을 보고 있었다. 십 분 동안 아무도 말하지 않았다.")
    S.line(text="그 침묵이 불편하지 않았다. 그게 이상했다.")
    S.line(who="한서윤", e="base", text="수습님은 왜 개발자가 되려고 했어요?")
    S.line(text="갑자기라서, 대답이 반 박자 늦었다.")

    S.choice([
        {"t": "“만들면 바로 보이니까요. 남이 쓸 수 있게 되는 게 좋아서요.”", "to": "p_why_build",
         "eff": {"seoyun": 2}},
        {"t": "“취업이 급해서요. 솔직하게 말하면요.”", "to": "p_why_job",
         "eff": {"seoyun": 2}, "flag": "honest_motive"},
        {"t": "“팀장님은 왜 그렇게까지 하세요?” 되묻는다.", "to": "p_why_back",
         "eff": {"seoyun": 3}},
    ])

    S.label("p_why_build")
    S.line(who="한서윤", text="그럼 오늘 같은 날이 제일 힘들겠네요.")
    S.line(who="나", text="네?")
    S.line(who="한서윤", e="base", text="바로 보이는 걸 좋아하는 사람은, 잘못도 바로 보여서요. 대신 빨리 알죠. 오늘처럼.")
    S.line(text="그녀가 캔커피를 따서 내 쪽으로 밀었다. 손끝이 캔 위에 잠깐 머물렀다.")
    S.line(who="한서윤", text="이거, 제가 제일 좋아하는 거예요. 달지 않은 거. 마셔 보세요.")
    S.goto("p_coffee")

    S.label("p_why_job")
    S.line(who="한서윤", e="surprised", text="…솔직하네요.")
    S.line(who="나", text="거짓말하면 오늘 같은 날 더 힘들 것 같아서요.")
    S.line(who="한서윤", e="base", text="그 말, 면접 때 했으면 좋았을 텐데.")
    S.line(who="나", text="면접 때 했어요. 떨어질 뻔했죠.")
    S.line(text="그녀가 아주 작게 웃었다. 이 사무실에서 처음 보는 웃음이었다. 소리 없이, 눈만.")
    S.line(who="한서윤", text="안 떨어졌잖아요. 그럼 그때부터 시작이에요. 남은 건 여기서 만들어요.")
    S.goto("p_coffee")

    S.label("p_why_back")
    S.line(who="한서윤", e="surprised", text="…저요?")
    S.line(who="나", text="네. 아침에 사 분 만에 회의 끝내고, 조명도 혼자 고치고, 롤백도 삼 분 만에 시켰잖아요.")
    S.line(who="한서윤", e="base", text="그건 일이니까요.")
    S.line(who="나", text="일이면 다 그렇게 하세요?")
    S.line(text="그녀는 대답하지 않았다. 대신 캔커피 두 개를 들고 와서 하나를 내 앞에 놓았다. 그게 대답인지도 확실하지 않았다.")
    S.line(who="한서윤", text="이거, 제가 제일 좋아하는 거예요. 달지 않은 거.")

    S.label("p_coffee")
    S.line(text="캔을 땄다. 탄산이 아주 조금 올라왔다. 정말로 달지 않았다.")
    S.line(who="나", text="…이거, 맛있네요.")
    S.line(who="한서윤", e="blush", text="그렇죠. 대신 한 번에 두 캔은 마시지 마세요. 심장이 놀라요.")
    S.line(text="농담인지 진담인지 모를 말투였다. 이 사람의 말은 늘 그 경계에 서 있다.")

    S.choice([
        {"t": "“다음엔 제가 사올게요. 같은 거로요.”", "to": "p_coffee_next",
         "eff": {"seoyun": 2}},
        {"t": "“한 번에 두 캔 마시면 어떻게 되는데요?”", "to": "p_coffee_ask",
         "eff": {"seoyun": 1}},
        {"t": "조용히 캔을 들고, 그녀가 일어나기를 기다린다.", "to": "p_coffee_quiet",
         "eff": {"seoyun": 1}},
    ])

    S.label("p_coffee_next")
    S.line(who="한서윤", e="surprised", text="…저한테요?")
    S.line(who="나", text="네. 팀장님은 늘 사 주시잖아요. 이번 주에만 세 번이에요.")
    S.line(text="그녀가 캔을 내려다봤다. 자기가 몇 번 샀는지 세어 본 적은 없을 것이다.")
    S.line(who="한서윤", e="blush", text="세 번이었어요?")
    S.line(who="나", text="네. 월요일에 한 번, 오늘 한 번, 그리고 어제 한 번. 어제는 제가 못 받았지만요.")
    S.line(who="한서윤", text="…그거, 어디에 뒀어요?")
    S.line(who="나", text="서랍에 있어요. 안 마셨어요.")
    S.line(text="그녀가 아무 말 없이 고개를 끄덕였다. 그 동작이 오래 남았다. 아마 다음 날, 서랍을 열어 볼 것 같았다.")
    S.goto("p_coffee_end")

    S.label("p_coffee_ask")
    S.line(who="한서윤", e="base", text="심장이 놀라요. 진짜로요. 저 어제 두 캔 마시고 새벽 세 시에 잠깐 깼어요.")
    S.line(who="나", text="…그걸 자랑하시는 거예요?")
    S.line(who="한서윤", text="아뇨. 경고예요. 수습님도 그러지 말라고요.")
    S.line(text="그런데 말하면서 자기 캔을 하나 더 땃다. 경고하는 사람이 경고를 안 지키는 건, 이 회사에서 흔한 일이다.")
    S.line(who="나", text="팀장님, 지금 또 따셨어요.")
    S.line(who="한서윤", e="blush", text="…이건 마지막이에요.")
    S.goto("p_coffee_end")

    S.label("p_coffee_quiet")
    S.line(text="말없이 캔을 들고, 그녀가 일어나기를 기다렸다. 그런데 그녀는 일어나지 않았다.")
    S.line(text="노트를 정리하고, 펜을 놓고, 창밖을 한 번 보고. 그 모든 동작이 아주 느렸다. 일부러 느린 것 같았다.")
    S.line(who="한서윤", text="수습님이 먼저 가세요. 저는 조금 더 있다가요.")
    S.line(who="나", text="…네. 그럼 먼저 가겠습니다.")
    S.line(text="가방을 메고 일어났는데, 그녀가 부르지 않았다. 그게 조금 아쉬웠다. 아쉽다고 생각한 것도 조금 놀라웠다.")

    S.label("p_coffee_end")
    S.line(text="열한 시 십 분. 서윤이 자리에서 일어나 불을 껐다. 절반만.")
    S.line(who="한서윤", text="내일 아홉 시. 지각하지 마세요.")
    S.line(who="나", text="팀장님은요?")
    S.line(who="한서윤", e="base", text="저는 원래 여기 있어요.")
    S.line(text="계단을 내려가면서 뒤를 봤다. 창가 자리의 스탠드가 아직 켜져 있었다. 그 불빛만 사무실에 남아 있었다.")
