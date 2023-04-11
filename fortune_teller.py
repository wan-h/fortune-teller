# coding: utf-8
# Author: wanhui0729@gmail.com

from transformers import AutoModel, AutoTokenizer
import datetime
import streamlit as st
from streamlit_chat import message

# 模型获取
@st.cache_resource
def get_model():
    # 对于低成本部署需求的同学，这里修改加载的模型，我这里使用量化后的模型
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b-int4", trust_remote_code=True, resume_download=True, cache_dir="models")
    model = AutoModel.from_pretrained("THUDM/chatglm-6b-int4", trust_remote_code=True, resume_download=True, cache_dir="models").half().cuda()
    model = model.eval()
    return tokenizer, model

# 根据日期计算星座
def get_constellation(month, day):
  n = ('摩羯座', '水瓶座', '双鱼座', '白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座')
  d = ((1, 20), (2, 19), (3, 21), (4, 21), (5, 21), (6, 22), (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23))
  return n[len(list(filter(lambda y:y <= (month, day), d))) % 12]


# sidebar 内容
st.set_page_config(
    page_title="看到未来",
    page_icon=":robot:",
    layout="wide"
)

st.sidebar.header("看到未来🤖")
st.sidebar.write("🤡你相信命运的安排吗")
st.sidebar.write("😍你相信丘比特的箭吗")
st.sidebar.write("💀死神今天会来吗")
st.sidebar.write("🤑财神会眷顾我吗")
st.sidebar.write("🤔世界还会变好吗")
st.sidebar.write("😄 😊 🙂 😔 🙁 😣")
st.sidebar.write("人生就是一个过程")
st.sidebar.write("现在我们不信命，就信 GPT ！！！")
st.sidebar.image("https://img2.woyaogexing.com/2019/08/06/ab2d3ef151884fee8cb80dad8da89d10%211080x1920.jpeg")

# 布局
messgae_box, controller_box = st.columns([2, 1])

# 交互空间
container = messgae_box.container()
with container:
    message("你好呀，请完善右方信息，让我了解你更多一点，然后给你算一卦！", avatar_style="big-smile")

# 这里实现了增加各种提示词来让大模型输出结果
def predict(name, gender, birthday, occupation, agree, companion_name, companion_birthday):
    tokenizer, model = get_model()
    chat_list = []
    with container:
        message("来吧，算我！", avatar_style="adventurer-neutral", is_user=True)
        gender_wraper = "帅哥" if gender == "男" else "美女"
        message(f"捕获{gender_wraper}一枚，容我掐指一算！", avatar_style="big-smile")
        constellation = get_constellation(birthday.month, birthday.day)
        chat_input_1 = f"我的名字叫{name}，性别{gender}，星座是{constellation}，出生日期是{birthday.year}年{birthday.month}月{birthday.day}日，" \
                       f"请分析一下我的八字和星座"
        chat_list.append(chat_input_1)
        chat_input_2 = "我会遇到哪些波折"
        chat_list.append(chat_input_2)
        chat_input_3 = f"我的职业是{occupation}，结合我的八字和星座，给我一些事业上的建议"
        chat_list.append(chat_input_3)
        if agree:
            if marriage == "单身":
                chat_input_4 = "我现在还是单身，根据我的八字和星座，说一下我适合找什么样的伴侣"
            else:
                companion_constellation = get_constellation(companion_birthday.month, companion_birthday.day)
                if marriage == "已婚":
                    companion_wrapper = "老婆"
                else:
                    companion_wrapper = "女朋友"
                chat_input_4 = f"我的{companion_wrapper}名字叫{companion_name}，星座是{companion_constellation}，出生日期是{companion_birthday.year}年{companion_birthday.month}月{companion_birthday.day}日，" \
                               f"请根据我们的八字和星座分析一下我们应该怎么更好的相处"
            chat_list.append(chat_input_4)
        chat_input_5 = "最后结合以上信息给我一些鼓励和人生建议吧"
        chat_list.append(chat_input_5)
        history = []
        for chat in chat_list:
            with st.empty():
                for response, history in model.stream_chat(tokenizer, chat, history):
                    query, response = history[-1]
                    response = response.replace(name, "你")
                    st.write(response)

# 输入空间
controller_box.subheader("让我了解你多一点 😘")
name = controller_box.text_input(label="姓名", placeholder="请输入你的姓名", value="无名氏")
gender = controller_box.radio(label="性别", options=("男", "女"))
birthday = controller_box.date_input(label="出生日期", value=datetime.date(2000, 1, 1),
                                     min_value=datetime.date(1900, 1, 1), max_value=datetime.datetime.now())
occupation = controller_box.text_input(label="职业", placeholder="请输入你的职业", value="自由职业者")
agree = controller_box.checkbox('看看你的爱情？')
companion_name = None
companion_birthday = None
companion_occupation = None
if agree:
    marriage = controller_box.radio(label="婚姻", options=("单身", "已婚", "未婚有情侣"))
    if marriage != "单身":
        companion_name = controller_box.text_input(label="伴侣姓名", placeholder="请输入伴侣的姓名")
        companion_birthday = controller_box.date_input(label="伴侣出生日期", value=datetime.date(2000, 1, 1),
                                                       min_value=datetime.date(1900, 1, 1), max_value=datetime.datetime.now())

if controller_box.button("让我给你算算", use_container_width=True):
    with st.spinner("掐指一算中......"):
        predict(name, gender, birthday, occupation, agree, companion_name, companion_birthday)