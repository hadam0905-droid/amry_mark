
import streamlit as st
import random
from PIL import Image

st.set_page_config(
    page_title="대한민국 군 계급 맞추기",
    page_icon="🎖️",
    layout="centered"
)

# 계급장 원본 사진 불러오기
import streamlit as st
import random
from PIL import Image
from pathlib import Path

# 현재 파이썬 파일이 있는 폴더 확인
BASE_DIR = Path(__file__).resolve().parent

# 계급장 사진 불러오기
IMAGE_PATH = BASE_DIR / "2015010609533000000024079.jpg"

if not IMAGE_PATH.exists():
    st.error("계급장 사진 파일을 찾을 수 없습니다.")
    st.stop()

image = Image.open(IMAGE_PATH)

# 대한민국 육군 계급장 리스트
# 사진의 한국군 부분을 계급별로 잘라서 사용
ranks = [
    {"name": "원수", "crop": (110, 43, 195, 82)},
    {"name": "대장", "crop": (110, 82, 195, 122)},
    {"name": "중장", "crop": (110, 122, 195, 162)},
    {"name": "소장", "crop": (110, 162, 195, 202)},
    {"name": "준장", "crop": (110, 202, 195, 242)},

    {"name": "대령", "crop": (110, 255, 195, 295)},
    {"name": "중령", "crop": (110, 295, 195, 335)},
    {"name": "소령", "crop": (110, 335, 195, 375)},

    {"name": "대위", "crop": (110, 380, 195, 420)},
    {"name": "중위", "crop": (110, 420, 195, 460)},
    {"name": "소위", "crop": (110, 460, 195, 500)},

    {"name": "준위", "crop": (110, 505, 195, 550)},

    {"name": "원사", "crop": (110, 550, 195, 595)},
    {"name": "상사", "crop": (110, 590, 195, 635)},
    {"name": "중사", "crop": (110, 630, 195, 675)},
    {"name": "하사", "crop": (110, 670, 195, 715)},

    {"name": "병장", "crop": (110, 715, 195, 757)},
    {"name": "상병", "crop": (110, 757, 195, 799)},
    {"name": "일병", "crop": (110, 799, 195, 841)},
    {"name": "이병", "crop": (110, 841, 195, 883)}
]

# 정답 입력을 비교하기 위한 함수
def normalize(answer):
    return answer.strip().replace(" ", "")


# 계급장 10개씩 무작위 추출하는 함수
def draw_ranks(remaining):
    selected = random.sample(
        remaining,
        min(10, len(remaining))
    )

    new_remaining = [
        rank for rank in remaining
        if rank not in selected
    ]

    return selected, new_remaining


# 게임 초기 설정
if "initialized" not in st.session_state:

    st.session_state.remaining = list(range(20))

    st.session_state.batch, st.session_state.remaining = (
        draw_ranks(st.session_state.remaining)
    )

    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.feedback = ""
    st.session_state.correct = False
    st.session_state.finished = False
    st.session_state.initialized = True


# 제목
st.title("🎖️ 대한민국 군 계급 맞추기")
st.write("계급장 사진을 보고 정확한 계급을 입력하세요!")

st.divider()


# 게임 종료 확인
if not st.session_state.finished:

    # 현재 문제의 계급 번호
    current_number = st.session_state.batch[
        st.session_state.index
    ]

    current_rank = ranks[current_number]

    # 진행 상황
    completed = 20 - len(st.session_state.remaining) - (
        len(st.session_state.batch) - st.session_state.index
    )

    st.subheader(f"문제 {completed + 1} / 20")

    st.metric("현재 점수", f"{st.session_state.score}점")

    st.progress(completed / 20)

    st.divider()

    # 계급장 사진 출력
    st.subheader("이 계급장의 이름은 무엇일까요?")

    rank_image = image.crop(current_rank["crop"])

    st.image(
        rank_image,
        caption="대한민국 육군 계급장",
        width=300
    )

    # 답안 입력
    with st.form(
        key=f"answer_{completed}"
    ):

        answer = st.text_input(
            "정답을 입력하세요.",
            placeholder="예: 대위"
        )

        submit = st.form_submit_button("정답 확인")

        if submit:

            if answer.strip() == "":
                st.warning("답을 입력해주세요.")

            else:

                user_answer = normalize(answer)

                correct_answer = normalize(
                    current_rank["name"]
                )

                # 선택구조: 정답 및 오답 확인
                if user_answer == correct_answer:

                    st.session_state.feedback = (
                        "정답입니다! +1점 🎉"
                    )

                    st.session_state.score += 1
                    st.session_state.correct = True

                elif user_answer != correct_answer:

                    st.session_state.feedback = (
                        f"오답입니다. 정답은 "
                        f"{current_rank['name']}입니다."
                    )

                    st.session_state.correct = False

                else:
                    st.session_state.feedback = (
                        "다시 입력해주세요."
                    )

                st.session_state.answered = True

    # 정답 결과 표시
    if st.session_state.answered:

        if st.session_state.correct:

            st.success(
                st.session_state.feedback
            )

        else:

            st.error(
                st.session_state.feedback
            )

        st.info("다음 문제로 가세요!")

        # 다음 문제로 이동
        if st.button("다음 문제 →", use_container_width=True):

            st.session_state.index += 1
            st.session_state.answered = False

            # 현재 10문제를 모두 풀었는지 확인
            if st.session_state.index >= len(
                st.session_state.batch
            ):

                # 남은 계급장이 있으면 다시 10개 추출
                if len(st.session_state.remaining) > 0:

                    (
                        st.session_state.batch,
                        st.session_state.remaining
                    ) = draw_ranks(
                        st.session_state.remaining
                    )

                    st.session_state.index = 0

                else:

                    st.session_state.finished = True

            st.rerun()


# 모든 문제 종료
else:

    st.balloons()

    st.title("🏆 게임 종료!")

    st.success("모든 군 계급 문제를 완료했습니다!")

    st.subheader(
        f"최종 점수: {st.session_state.score} / 20점"
    )

    st.write(
        f"정답: {st.session_state.score}개"
    )

    st.write(
        f"오답: {20 - st.session_state.score}개"
    )

    if st.session_state.score == 20:
        st.success("완벽합니다! 모든 계급을 맞혔습니다!")

    elif st.session_state.score >= 15:
        st.info("훌륭합니다! 군 계급을 잘 알고 있네요!")

    else:
        st.info("다시 도전해서 계급을 익혀보세요!")

    # 게임 다시 시작
    if st.button("다시 시작하기", use_container_width=True):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()
