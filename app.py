from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
import io
import base64
from flask import session
import uuid
import matplotlib
import os
matplotlib.use('Agg')

import matplotlib.font_manager as fm

# 폰트 경로 설정
font_path = './static/Apple_산돌고딕_Neo/AppleSDGothicNeoUL.ttf'
font_prop = fm.FontProperties(fname=font_path)
font_path_title = './static/Apple_산돌고딕_Neo/AppleSDGothicNeoSB.ttf'
font_prop_title = fm.FontProperties(fname=font_path_title)

font_path_text = './static/Apple_산돌고딕_Neo/AppleSDGothicNeoEB.ttf'
font_prop_text = fm.FontProperties(fname=font_path_text)

# matplotlib의 기본 설정 변경
plt.rcParams['font.family'] = font_prop.get_name()
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'some_secret_key'

def loading_bar_simulation():
    time.sleep(2)  # Simulate processing time

def generate_data(n, mean, std_dev):
    return np.random.normal(mean, std_dev, n)

def create_plots(purchase_amounts, user_mbti, debate_topic, mean, std_dev, n):
    purchase_amounts_1 = np.random.chisquare(df=100, size=len(purchase_amounts)) -60
    purchase_amounts_2 = np.random.normal(mean + 15, std_dev, n)

    # 그래프의 전체 크기를 줄입니다.
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6), dpi=200)
    
    color_with_alpha = (0.0078, 0.2235, 0.4863, 0.5)
    sns.kdeplot(purchase_amounts_1, fill=True, color='#01397C', linewidth=2, linestyle='-', label='전체 SNU 궁합 분포', ax=ax1, alpha = 0.5, edgecolor=color_with_alpha)
    sns.kdeplot(purchase_amounts_2, fill=True, color='#01397C', linewidth=2, linestyle='-', label='참여자들의 궁합 분포', ax=ax1, alpha = 0.9)

    ax1.set_title(f'KDEplot : GH와의 궁합 분석\nMBTI: {user_mbti}\n민트초코 선호여부: {debate_topic}', fontsize=12, color='black',fontproperties=font_prop_title)
    random_index = np.random.randint(0, len(purchase_amounts))
    selected_purchase_amount = purchase_amounts_2[random_index]
    ax1.scatter(selected_purchase_amount, 0.005, color='red', marker='*', s=100, label=f'당신의 점수\n(Value: {selected_purchase_amount:.2f})')
    percentile_10 = np.percentile(purchase_amounts_2, 95)
    ax1.axvline(percentile_10, color='red', linestyle='--', label=f'상위 1%\n(Value: {percentile_10:.2f})')
    ax1.set_xlabel('GH와의 궁합', fontsize=12,fontproperties=font_prop_title)
    ax1.set_ylabel('분포', fontsize=12,fontproperties=font_prop_title)
    ax1.legend()

    #sns.boxplot(y=purchase_amounts, ax=ax2, width=0.3, boxprops=dict(facecolor='#01397C', alpha=0.5, linestyle='-', linewidth=2,))
    boxprops = {'facecolor': '#01397C', 'alpha': 0.5, 'edgecolor': 'black'}
    sns.boxplot(y=purchase_amounts, ax=ax2, width=0.3, boxprops = boxprops)
    # 박스의 색상 및 투명도 설정
    # for patch in ax2.artists:
    #     fc = patch.get_facecolor()
    #     patch.set_facecolor(matplotlib.colors.to_rgba(fc, 0.5)) # 0.5는 투명도를 나타냅니다.
    debate_text = f'당신의 점수\n(Selected Value: {selected_purchase_amount:.2f})'
    ax2.annotate(debate_text, xy=(0, selected_purchase_amount), xytext=(0.15, 30.0),
                arrowprops=dict(arrowstyle="->", color='black'), fontsize=12, color='black')
    ax2.axhline(percentile_10, color='red', linestyle='--', label=f'상 5%\n(Value: {percentile_10:.2f})')
    ax2.set_title(f'Boxplot: GH와의 궁합 분석\nMBTI: {user_mbti}\n민트초코 선호여부: {debate_topic}', fontsize=12, color='black', fontproperties=font_prop_title)
    ax2.set_ylabel('궁합 점수', fontsize=12, fontproperties=font_prop_title)
    ax2.set_xticklabels([''])
    



    for label in ax1.get_xticklabels():
        label.set_fontproperties(font_prop_title)
    for label in ax1.get_yticklabels():
        label.set_fontproperties(font_prop_title)

    # ax2의 y축 라벨 값 폰트 설정
    for label in ax2.get_yticklabels():
        label.set_fontproperties(font_prop_title)

    ax3 = plt.subplot(1, 3, 3)
    ax3.set_xlim(0, 100)
    ax3.set_ylim(0, 1)
    ax3.text(50,0.5, f'당신과 GH의 궁합점수 :\n{selected_purchase_amount:.2f}', ha='center', fontsize=35, color='#053699',fontproperties=font_prop_text)
    message = "지금 당장 GH에 지원하세요 :)" if selected_purchase_amount > mean+15 else "지금부터 서로 더 잘 알아가기로 해요 :)"
    ax3.text(50, 0.3, message, ha='center', fontsize=20, color='black',fontproperties=font_prop_title)
    ax3.axis('off')
    ax3.set_position([0.7, 0.11, 0.27, 0.77])  

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    
    # 이미지 데이터를 일시적으로 파일로 저장
    filename = f"plot_{uuid.uuid4().hex}.png"
    with open(filename, 'wb') as f:
        f.write(img.getvalue())
    
    return filename

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('input_form.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    user_mbti = request.form['user_mbti']
    debate_topic = request.form['debate_topic']
    purchase_amounts = generate_data(10000, 50, 8)
    plot_data = create_plots(purchase_amounts, user_mbti, debate_topic, 50, 8, 10000)
    loading_bar_simulation()  # Simulate some processing time for the loading bar

    # 이미지 데이터를 session에 저장
    session['plot_filename'] = plot_data

    return jsonify(result_url=f"/result?user_mbti={user_mbti}&debate_topic={debate_topic}")


@app.route('/result')
def result():
    user_mbti = request.args.get('user_mbti')
    debate_topic = request.args.get('debate_topic')
    plot_filename = session.get('plot_filename', '')  # session에서 파일명 가져오기
    
    # 파일을 읽어 base64 인코딩 수행
    with open(plot_filename, 'rb') as f:
        plot_data = base64.b64encode(f.read()).decode()

    # 일시적으로 저장된 이미지 파일 삭제
    os.remove(plot_filename)

    return render_template('result.html', user_mbti=user_mbti, debate_topic=debate_topic, plot_data=plot_data)

# ... [나머지 코드는 유지]
if __name__ == '__main__':
    app.run()
