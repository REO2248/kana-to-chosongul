import re

PYKAKASI = False
try:
    from pykakasi import kakasi
    kks = kakasi()
    PYKAKASI = True
except:
    import warnings
    warnings.warn("pykakasi가 설치되여있지않습니다. 가다가나만을 지원합니다.")

def hangul_to_codepoint(hangul):
    codepoint = ord(hangul) - 0xAC00
    if codepoint < 0 or codepoint > 11172:
        return None
    else:
        return codepoint

def decompose_hangul(hangul):
    codepoint = hangul_to_codepoint(hangul)
    if codepoint is None:
        return None, None, None
    else:
        chosong = codepoint // (21 * 28)
        jungsong = (codepoint - chosong * 21 * 28) // 28
        jongsong = codepoint - chosong * 21 * 28 - jungsong * 28
        return chosong, jungsong, jongsong

convlist={
    "キャ":"갸꺄",
    "キュ":"규뀨",
    "キョ":"교꾜",
    "シャ":"샤",
    "シュ":"슈",
    "ショ":"쇼",
    "チャ":"쟈쨔",
    "チュ":"쥬쮸",
    "チョ":"죠쬬",
    "ニャ":"냐",
    "ニュ":"뉴",
    "ニョ":"뇨",
    "ヒャ":"햐",
    "ヒュ":"휴",
    "ヒョ":"효",
    "ミャ":"먀",
    "ミュ":"뮤",
    "ミョ":"묘",
    "リャ":"랴",
    "リュ":"류",
    "リョ":"료",
    "ギャ":"갸",
    "ギュ":"규",
    "ギョ":"교",
    "ジャ":"쟈",
    "ジュ":"쥬",
    "ジョ":"죠",
    "ヂャ":"쟈",
    "ヂュ":"쥬",
    "ヂョ":"죠",
    "ビャ":"뱌",
    "ビュ":"뷰",
    "ビョ":"뵤",
    "ピャ":"뺘",
    "ピュ":"쀼",
    "ピョ":"뾰",
    "ア":"아",
    "イ":"이",
    "ウ":"우",
    "エ":"에",
    "オ":"오",
    "カ":"가까",
    "キ":"기끼",
    "ク":"구꾸",
    "ケ":"게께",
    "コ":"고꼬",
    "サ":"사",
    "シ":"시",
    "ス":"스",
    "セ":"세",
    "ソ":"소",
    "タ":"다따",
    "チ":"지찌",
    "ツ":"쯔쯔",
    "テ":"데떼",
    "ト":"도또",
    "ナ":"나",
    "ニ":"니",
    "ヌ":"누",
    "ネ":"네",
    "ノ":"노",
    "ハ":"하",
    "ヒ":"히",
    "フ":"후",
    "ヘ":"헤",
    "ホ":"호",
    "マ":"마",
    "ミ":"미",
    "ム":"무",
    "メ":"메",
    "モ":"모",
    "ヤ":"야",
    "ユ":"유",
    "ヨ":"요",
    "ラ":"라",
    "リ":"리",
    "ル":"루",
    "レ":"레",
    "ロ":"로",
    "ワ":"와",
    "ヲ":"오",
    "ガ":"가",
    "ギ":"기",
    "グ":"구",
    "ゲ":"게",
    "ゴ":"고",
    "ザ":"자",
    "ジ":"지",
    "ズ":"즈",
    "ゼ":"제",
    "ゾ":"조",
    "ダ":"다",
    "ヂ":"지",
    "ヅ":"즈",
    "デ":"데",
    "ド":"도",
    "バ":"바",
    "ビ":"비",
    "ブ":"부",
    "ベ":"베",
    "ボ":"보",
    "パ":"빠",
    "ピ":"삐",
    "プ":"뿌",
    "ペ":"뻬",
    "ポ":"뽀",
}

upper_kana = r"(?=[アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ ])"
all_kana = r"[^アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポァィゥェォャュョン]"

def divide(text):
    result=  re.split(upper_kana, text)
    returnlist= [x if x != " " else "" for x in result]
    returnlist = [re.sub(all_kana, "", x) for x in returnlist]
    return returnlist


def convert(text:str):
    """Kana to Chosongul converter
    """
    text = text.replace(
                "金正恩", "キムジョンウン"
        ).replace("金正日", "キムジョンイル"
        ).replace("金日成", "キムイルソン"
        )
    if PYKAKASI:
        text = "".join([x["kana"] for x in kks.convert(text)])
    divided = divide(text)

    convlist1 = convlist.copy()
    convlist2 = convlist.copy()
    for key, value in convlist1.items():
        convlist1[key] = value[0]
    for key, value in convlist2.items():
        convlist2[key] = value[-1]

    divided2 = []
    for i in range(len(divided)):
        if divided[i-1] == "" or i == 0:
            result = divided[i]
            for key, value in convlist1.items():
                result = result.replace(key, value)
            divided2.append(result)
        else:
            result = divided[i]
            for key, value in convlist2.items():
                result = result.replace(key, value)
            divided2.append(result)

    for i in range(len(divided2)+2):
        try:
            result = divided2[i]
            nextchosong = 11
            #다음없는경우
            if i == len(divided2)-1 or divided2[i+1] == "":
                nextchosong = 11
            else:
                nextchosong = decompose_hangul(divided2[i+1][0])[0]

            #ッ
            if divided2[i][-1] == "ッ":
                if nextchosong == 1: #ㄱ
                    divided2[i] = chr(ord(divided2[i][0])+1)
                else: #ㅅ
                    divided2[i] = chr(ord(divided2[i][0])+19)

            #ン
            if divided2[i][-1] == "ン":
                if nextchosong == 11:
                    divided2[i] = chr(ord(divided2[i][0])+21) #ㅇ
                else:
                    divided2[i] = chr(ord(divided2[i][0])+4) #ㄴ
        except IndexError:
            pass

    return "".join(divided2)


if __name__ == "__main__":
    print("《 환영합니다! 이 프로그람은 일본말을 조선글자로 자동적으로 적습니다! 》")
    print("프로그람의 자세는 README.md를 참고하십시오.")
    print("프로그람을 종료하려면 Ctrl+C를 누르십시오.")
    while True:
        text = input("입력: ")
        print(convert(text))