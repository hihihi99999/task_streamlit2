import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# ページ設定
st.set_page_config(page_title="タスク管理アプリ", layout="wide")

# セッション状態の初期化
if 'tasks' not in st.session_state:
    # サンプルデータの作成
    st.session_state.tasks = {
        'タスク一覧': ['企画書作成', '会議準備', 'メール対応', 'プレゼン資料作成'],
        '予定時間': [120, 60, 30, 90],
        '完了状態': [True, False, True, False],
        '日付': [datetime.now().date() for _ in range(4)]
    }

# タイトル
st.title('📝 タスク管理アプリ')

# 日付選択
selected_date = st.date_input(
    "日付を選択してください",
    datetime.now().date(),
    format="YYYY/MM/DD"
)

# 新規タスク追加セクション
with st.container():
    st.subheader("新規タスク追加")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        new_task = st.text_input("タスク名を入力")
    
    with col2:
        time_col1, time_col2, time_col3 = st.columns(3)
        with time_col1:
            base_time = st.number_input("時間（分）", min_value=0, value=30, step=15)
        with time_col2:
            if st.button("-15分"):
                base_time = max(0, base_time - 15)
        with time_col3:
            if st.button("+15分"):
                base_time += 15

        time_col4, time_col5 = st.columns(2)
        with time_col4:
            if st.button("-60分"):
                base_time = max(0, base_time - 60)
        with time_col5:
            if st.button("+60分"):
                base_time += 60

    if st.button("タスクを追加"):
        if new_task:
            if isinstance(st.session_state.tasks, dict):
                st.session_state.tasks['タスク一覧'].append(new_task)
                st.session_state.tasks['予定時間'].append(base_time)
                st.session_state.tasks['完了状態'].append(False)
                st.session_state.tasks['日付'].append(selected_date)
                st.success(f"タスク「{new_task}」を追加しました！")
            st.rerun()

# タスク一覧表示
st.subheader("タスク一覧")

# データフレームの作成
df = pd.DataFrame(st.session_state.tasks)

# 選択された日付のタスクのみ表示
df_filtered = df[df['日付'] == selected_date]

# 各タスクの表示と操作
for idx, row in df_filtered.iterrows():
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    # タスク名の表示（完了時は取り消し線付き）
    with col1:
        task_name = row['タスク一覧']
        if row['完了状態']:
            st.markdown(f"~~{task_name}~~")
        else:
            st.write(task_name)
    
    # 予定時間の表示
    with col2:
        st.write(f"{row['予定時間']}分")
    
    # 完了状態の切り替え
    with col3:
        if st.checkbox("完了", value=row['完了状態'], key=f"check_{idx}"):
            df.at[idx, '完了状態'] = True
        else:
            df.at[idx, '完了状態'] = False
    
    # 削除ボタン
    with col4:
        if st.button("削除", key=f"del_{idx}"):
            if isinstance(st.session_state.tasks, dict):
                for key in st.session_state.tasks.keys():
                    st.session_state.tasks[key].pop(idx)
                st.rerun()

# グラフ表示
st.subheader("タスク時間グラフ")

if not df_filtered.empty:
    fig = px.bar(
        df_filtered,
        x='予定時間',
        y='タスク一覧',
        orientation='h',
        title='タスク別予定時間',
        labels={'予定時間': '時間（分）', 'タスク一覧': 'タスク名'},
        color='完了状態',
        color_discrete_map={True: '#90EE90', False: '#FFB6C6'}
    )
    
    fig.update_layout(
        showlegend=True,
        legend_title_text='完了状態',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("表示するタスクがありません。新しいタスクを追加してください。")

# セッション状態の更新
st.session_state.tasks = {
    'タスク一覧': df['タスク一覧'].tolist(),
    '予定時間': df['予定時間'].tolist(),
    '完了状態': df['完了状態'].tolist(),
    '日付': df['日付'].tolist()
}
