# -*- coding: utf-8 -*-
"""3일차 밤 — 목요일, 편의점 앞 벤치"""


def build(S):
    S.line(ch="3일차 · 목요일 밤", bg="office_night", bgm="night",
           text="목요일. 하루가 이상할 만큼 빨리 지나갔다. 발표 자료를 만들고, 지우고, 다시 만들었다.")
    S.line(text="여덟 시에 하람이 메시지를 보냈다. 「수습님, 아직 회사죠?」")
    S.line(text="「네」라고 답했더니, 삼 초 뒤에 답이 왔다. 「편의점. 십 분 드릴게요.」")
    S.line(bg="store_night", bgm="dusk", hide=True,
           text="빌딩을 나와 골목을 따라 이백 미터. 편의점 불빛이 골목 끝에서 새어 나오고 있었다.")
    S.line(show={"id": "haram", "expr": "base"}, who="오하람", text="여기요! 벤치!"
    )
    S.line(text="그녀는 벤치 위에 봉지를 펼쳐 놓고 앉아 있었다. 봉지 안에는 삼각김밥 네 개, 컵라면 두 개, 그리고 이상하게 큰 아이스크림 하나.")
    S.line(who="나", text="이걸 다 먹어요?")
    S.line(who="오하람", text="아이스크림은 제 거예요. 나머지는 수습님 거예요. 어제 저녁 못 먹었다면서요.")
    S.line(who="나", text="그건 어제 얘기인데요.")
    S.line(who="오하람", e="base", text="어제 못 먹은 건 오늘도 배고픈 거예요. 이건 시간이 지나도 안 고쳐져요.")

    S.line(text="벤치에 나란히 앉았다. 편의점 유리창의 하얀 빛이 아스팔트 위에 네모를 만들고 있었다.")
    S.line(text="삼각김밥을 하나 까서 먹었다. 밥이 조금 딱딱했다. 그게 오히려 좋았다.")
    S.line(who="오하람", text="수습님. 저 어제 팀장님이랑 얘기했어요.")
    S.line(who="나", text="…팀장님이요?")
    S.line(who="오하람", e="serious", text="네. 제 심사 이야기. 그리고 수습님 이야기도 조금.")
    S.line(who="나", text="제 이야기를요?")
    S.line(who="오하람", text="네. 팀장님이 물었어요. 첫 주에 스테이징 누가 고쳤는지 아느냐고.")
    S.line(text="손에 든 김밥이 멈췄다. 어제 밤에 그 얘기를 했었지. 그리고 그녀가 여기서 그 얘기를 꺼냈다.")
    S.line(who="나", text="…팀장님이 그걸 왜 물어요?")
    S.line(who="오하람", e="base", text="글쎄요. 그냥 물어보더라고요. 저는 모른다고 했어요.")
    S.line(text="그녀가 아이스크림 뚜껑을 열었다. 바닐라였다. 한 숟갈을 떠서, 나에게 먼저 내밀었다.")
    S.line(who="오하람", text="먼저 드세요.")
    S.line(who="나", text="…이건 하람 님이 먹는다고 했잖아요.")
    S.line(who="오하람", text="첫 숟갈은 원래 남 주는 거예요.")

    S.line(text="나는 그 숟갈을 받아 먹었다. 그리고 바로 물었다. 더 미룰수록 말하기 어려워질 것 같아서.")
    S.line(who="나", text="하람 님. 첫 주에 스테이징, 하람 님이 고쳤죠.")
    S.line(text="그녀가 숟가락을 내려놓았다. 놀란 얼굴이었다. 아니, 놀란 얼굴을 만들려고 애쓰는 얼굴이었다.")
    S.line(who="오하람", e="surprised", text="…어떻게 알았어요?")
    S.line(who="나", text="팀장님이 자기가 안 했다고 했어요. 그리고 그날 밤에 남아 있던 사람이, 여기 한 명 더 있었고요.")
    S.line(text="편의점 냉장고가 웅웅거렸다. 그 소리가 갑자기 커진 것 같았다.")
    S.line(who="오하람", e="serious", text="…맞아요. 제가 했어요. 밤 열한 시에 남아서, 환경 변수 되돌리고, 다시 올렸어요.")
    S.line(who="나", text="왜 말 안 했어요?")
    S.line(who="오하람", text="그날 제 일도 안 끝났어요. 그러니까 그냥 남아 있었던 거예요. 그런데 다음 날 아침에 수습님이 얼굴 하얗게 되고 있는 거예요.")
    S.line(who="오하람", e="blush", text="말하면, 고맙다고 할 거잖아요. 그런데 그때는 그 말이 싫었어요. 저도 수습이고, 수습님이 고마워하면, 제가 뭔가 대단한 사람이 된 것 같아서.")
    S.line(who="나", text="…그게 싫었어요?")
    S.line(who="오하람", text="네. 저는 그냥 옆자리 사람이 곤란한 걸 본 것뿐인데, 그걸로 제가 좋은 사람이 되면, 그건 제가 아니잖아요.")

    S.choice([
        {"t": "“그래도 고마워요. 진짜로. 말 안 해도 알았으면 좋았을 텐데.”", "to": "p_truth_thanks",
         "eff": {"haram": 3}, "flag": "haram_truth"},
        {"t": "“왜 그런 걸 혼자 해요. 다음엔 저한테 말해요.”", "to": "p_truth_together",
         "eff": {"haram": 2}, "flag": "haram_truth"},
        {"t": "“팀장님은 그걸 모르고 있었어요. 그건 좀… 아니에요.”", "to": "p_truth_shape",
         "eff": {"haram": 2}, "flag": "haram_truth"},
    ])

    S.label("p_truth_thanks")
    S.line(who="오하람", e="blush", text="…알았으면 좋았을 텐데, 라는 말, 처음 들어요.")
    S.line(who="나", text="보통은 뭐라고 해요?")
    S.line(who="오하람", text="괜찮아요, 라고 해요. 그런데 저는 괜찮지 않았어요. 그날 밤에 되게 무서웠어요. 혼자 서버 만지다가 다 망가뜨리면 어쩌지 싶어서.")
    S.line(who="나", text="그럼 왜 했어요?")
    S.line(who="오하람", e="base", text="수습님이 다음 날 아침에 혼날 걸 알았으니까요. 그리고 저는 그거, 안 혼나도 되는 일이라고 생각했어요.")
    S.goto("p_truth_after")

    S.label("p_truth_together")
    S.line(who="오하람", e="surprised", text="다음엔요?")
    S.line(who="나", text="네. 제가 실수하면 하람 님이 고치고, 하람 님이 실수하면 제가 고치는 거예요.")
    S.line(who="오하람", e="base", text="…그거, 되게 좋은데요. 근데 저 실수 많이 해요.")
    S.line(who="나", text="저도요. 어제 했잖아요.")
    S.line(who="오하람", text="아, 맞다. 그거 봤어요. 롤백할 때 손 안 떨리던 거.")
    S.line(who="나", text="떨렸다고 했잖아요.")
    S.line(who="오하람", e="blush", text="그래서 더 좋다고 했잖아요.")
    S.goto("p_truth_after")

    S.label("p_truth_shape")
    S.line(who="오하람", e="surprised", text="…네?")
    S.line(who="나", text="아니에요. 하람 님이 한 일이 남의 이름으로 처리된 게, 그냥 좀 이상해서요.")
    S.line(who="오하람", e="serious", text="그거요. 저도 그 생각 했어요. 근데 그건 제가 선택한 거예요. 그러니까 이상하게 만들지 말아요.")
    S.line(who="나", text="…네.")
    S.line(who="오하람", e="base", text="대신 하나만 약속해 주세요. 나중에 누가 그 일을 물으면, 제가 했다고 말해 주세요. 자랑은 아니고, 그냥 사실이라서.")
    S.line(who="나", text="그럴게요. 사실대로.")
    S.goto("p_truth_after")

    S.label("p_truth_after")
    S.line(text="아이스크림이 절반쯤 녹았다. 그녀가 아쉬운 얼굴로 마지막 숟갈을 먹었다.")
    S.line(who="오하람", text="수습님. 저 내일 발표, 이걸로 해요.")
    S.line(text="휴대폰 화면을 보여 줬다. 계단참에서 그린 그림이었다. 밤의 창문과, 창가에 놓인 의자와, 의자에 앉은 사람의 뒷모습.")
    S.line(who="나", text="…이거, 발표에 써도 돼요? 회사 일 아니잖아요.")
    S.line(who="오하람", e="serious", text="회사 일이에요. 제가 여기서 아홉 시간을 보내는 이유가 이거예요. 이걸 보여주지 않으면, 저는 그냥 화면 예쁘게 만드는 사람이에요.")
    S.line(who="오하람", text="근데 이걸 보여주면, 저는 이 회사에서 밤을 그리는 사람이 돼요. 그게 달라요.")
    S.line(text="그 말을 하는 얼굴이, 오늘 처음으로 웃지 않고 있었다. 그게 더 예뻤다.")

    S.choice([
        {"t": "“그럼 저는 그 발표를 제일 앞에서 볼게요.”", "to": "p_final_watch",
         "eff": {"haram": 3}},
        {"t": "“하람 님이 밤을 그리는 사람이면, 저는 그 밤에 있는 사람이네요.”", "to": "p_final_moon",
         "eff": {"haram": 3}, "flag": "haram_line"},
        {"t": "“발표 잘하고 오면, 뭐 해 줄게요.” 웃으면서 넘긴다.", "to": "p_final_joke",
         "eff": {"haram": 2}},
    ])

    S.label("p_final_watch")
    S.line(who="오하람", e="blush", text="…맨 앞은 부담스러운데요.")
    S.line(who="나", text="그럼 뒤에서 볼게요. 대신 끝까지요.")
    S.line(who="오하람", e="base", text="좋아요. 대신 제가 중간에 말 더듬으면, 웃지 마요.")
    S.line(who="나", text="안 웃어요.")
    S.line(who="오하람", text="거짓말. 수습님 웃음 많이 참는 사람이에요. 저 그거 알아요.")
    S.goto("p_store_end")

    S.label("p_final_moon")
    S.line(who="오하람", e="surprised", text="…뭐라고요?")
    S.line(who="나", text="그림에 사람이 있잖아요. 그 사람이 누군지는 모르겠는데, 하람 님이 그 밤을 그리면 저는 거기 있고 싶어서요.")
    S.line(text="그녀가 아무 말도 하지 않았다. 아이스크림 통을 두 손으로 감싸고, 한참 아래를 봤다.")
    S.line(who="오하람", e="blush", text="…수습님, 그런 말은요. 발표 끝나고 하면 안 돼요?")
    S.line(who="나", text="왜요?")
    S.line(who="오하람", text="지금 들으면, 내일 발표 망쳐요. 머리에 그것만 남아서.")
    S.line(who="나", text="…죄송해요.")
    S.line(who="오하람", e="base", text="죄송하진 마요. 대신 내일 다시 해 주세요. 그때는 제가 대답할게요.")
    S.goto("p_store_end")

    S.label("p_final_joke")
    S.line(who="오하람", e="base", text="오, 그거 좋다. 뭐 해 줄 거예요?")
    S.line(who="나", text="…생각해 볼게요. 일단 붙고 나서요.")
    S.line(who="오하람", text="그럼 저도 생각해 볼게요. 붙으면 받을 거고, 안 붙으면 못 받는 거네요.")
    S.line(text="농담처럼 말했는데, 그 문장이 오래 남았다. 못 받는 것들에 대해 우리는 너무 자주 농담을 했다.")

    S.label("p_store_end")
    S.line(text="열한 시가 넘었다. 편의점 직원이 밖으로 나와 쓰레기봉투를 정리했다.")
    S.line(who="오하람", text="수습님. 내일 끝나고, 시간 있어요?")
    S.line(who="나", text="있어요. 왜요?")
    S.line(who="오하람", e="base", text="그냥. 있으면 좋겠다 싶어서.")
    S.line(text="그녀가 일어나 봉지를 접었다. 접는 손이 아주 느렸다.")
    S.line(who="오하람", text="내일, 우리 둘 다 붙으면 좋겠다.")
    S.line(who="나", text="…네.")
    S.line(who="오하람", e="blush", text="아, 이거 이상한 말이었죠. 하나만 붙어도 좋은 건데.")
    S.line(who="나", text="아니에요. 둘 다 붙는 게 좋겠어요.")
    S.line(bg="office_day", hide=True,
           text="골목을 돌아 나오면서 뒤를 봤다. 그녀는 아직 편의점 앞에 서 있었다. 손을 흔들지 않았다. 그냥 서 있었다.")
    S.line(text="그게 이상하게 오래 보였다.")
