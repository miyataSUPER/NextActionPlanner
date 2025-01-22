"""
動画や会議の文字起こしテキストから次のアクションを抽出するStreamlitアプリ

このモジュールは、ユーザーがアップロードした動画ファイル、YouTubeリンク、
または直接入力されたテキストから、次に取るべきアクションを抽出し、
Markdown形式で表示するStreamlitアプリケーションを提供します。
"""

import streamlit as st
from audio_processor import AudioProcessor
from text_processor import TextProcessor
from gemini_client import GeminiClient
from database import Database
from utils import setup_logging
from typing import List
from datetime import datetime


def main():
    """
    Streamlitアプリケーションのメインエントリーポイント
    """
    st.set_page_config(layout="wide")
    st.title("会議アクション抽出ツール")
    
    # サイドバーでモードを選択
    mode = st.sidebar.radio(
        "モードを選択",
        ["新規アクション作成", "アクション管理"]
    )
    
    db = Database()
    
    if mode == "新規アクション作成":
        input_type = st.radio(
            "入力方式を選択してください：",
            ["MP4ファイル", "YouTubeリンク", "テキスト直接入力"]
        )
        
        try:
            if input_type == "MP4ファイル":
                uploaded_file = st.file_uploader("MP4ファイルをアップロード", type=['mp4'])
                if uploaded_file:
                    with st.spinner('音声を文字起こし中...'):
                        text = AudioProcessor.process_video_file(uploaded_file)
                
            elif input_type == "YouTubeリンク":
                youtube_url = st.text_input("YouTubeのURLを入力")
                if youtube_url and st.button('処理開始'):
                    with st.spinner('動画をダウンロードして文字起こし中...'):
                        text = AudioProcessor.process_youtube_video(youtube_url)
                
            else:  # テキスト直接入力
                text = st.text_area("会議の文字起こしテキストを入力")
            
            if 'text' in locals() and text:
                with st.spinner('アクションを生成中...'):
                    processed_text = TextProcessor.preprocess(text)
                    client = GeminiClient()
                    actions = client.generate_actions(processed_text)
                    
                    st.markdown("### 生成されたアクション")
                    st.markdown(actions)
                    
                    if st.button("データベースに保存"):
                        # アクションをパースしてデータベースに保存
                        for action in parse_actions(actions):
                            db.add_action(**action)
                        st.success("アクションを保存しました！")

        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")

    else:  # アクション管理モード
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("未完了のアクション")
            actions = db.get_pending_actions()
            for action in actions:
                with st.container():
                    st.markdown(f"""
                    ### {action['content']}
                    - 担当者: {action['assignee']}
                    - 優先度: {action['priority']}
                    - 期限: {action['due_date']}
                    """)
                    if st.button(f"完了 #{action['id']}", key=f"complete_{action['id']}"):
                        db.complete_action(action['id'])
                        st.experimental_rerun()
        
        with col2:
            st.header("統計情報")
            stats = db.get_action_stats()
            st.metric("未完了タスク", stats['pending_count'])
            st.metric("完了タスク", stats['completed_count'])
            if stats['avg_completion_time']:
                st.metric("平均完了時間", f"{stats['avg_completion_time']:.1f}時間")


def parse_actions(markdown_text: str) -> List[dict]:
    """
    Markdownテキストからアクション情報を抽出します。

    Args:
        markdown_text (str): Gemini APIから返されたMarkdownテキスト

    Returns:
        List[dict]: アクション情報のリスト
    """
    actions = []
    current_action = {}
    
    for line in markdown_text.split('\n'):
        line = line.strip()
        
        if line.startswith('## アクション'):
            if current_action:
                actions.append(current_action)
            current_action = {}
            continue
            
        if line.startswith('- '):
            key_value = line[2:].split(': ', 1)
            if len(key_value) == 2:
                key, value = key_value
                if key == '作業内容':
                    current_action['content'] = value
                elif key == '担当者':
                    current_action['assignee'] = value
                elif key == '優先度':
                    try:
                        current_action['priority'] = int(value)
                    except ValueError:
                        pass
                elif key == '期限':
                    try:
                        current_action['due_date'] = datetime.strptime(value, '%Y-%m-%d')
                    except ValueError:
                        pass
                elif key == '必要なリソース':
                    current_action['resources'] = value
    
    if current_action:
        actions.append(current_action)
    
    return actions


if __name__ == "__main__":
    setup_logging()
    main() 
