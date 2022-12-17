# _*_ coding: utf-8 _*_
"""
@Time : 2022/12/09
@Author : Dasein
@Version：V 3.0
@File : task_input.py
"""
import time
import pandas as pd
import streamlit as st
import random
import pages.日历 as Cal


def header():
    """
    页面标题
    :return: 页面标题
    """
    header_text_list = ['😅 今天又不想上班了吗？',
                        '🥹 今天还是得上班呀！',
                        '☺️ 好好上班吧，可能明天班就不给你上了',
                        '🫡 英子姐牛逼！',
                        '叫👮🏾♂ 把你带走！！',
                        '👴🏿 令人失望，男人是不来大姨妈的',
                        '🥺 嘤嘤嘤····',
                        ]
    header_text = st.header(random.choice(header_text_list))
    return header_text


class Task:
    def __init__(self, creation_date):
        self.task_creation_date = creation_date

    def task_input(self):
        """
        录入任务清单
        :return: 任务清单的相关信息
        """

        with st.form(' '):
            task_name = st.text_input('给你的任务起个名字')
            task_description = st.text_area('王鹏飞让你用一句话描述一下')

            col1, col2 = st.columns(2)
            with col1:
                task_date_begin = st.date_input('这个活儿打算什么时候开始呢？')
            with col2:
                task_date_end = st.date_input('这个活儿打算什么时候结束呢？')

            col3, col4, col5 = st.columns(3)
            with col3:
                task_emergency = st.selectbox('有多急？', ['️🔥', '🔥🔥️', '🔥🔥🔥️'])
            with col4:
                task_important = st.selectbox('催你的人有多牛逼？', ['🐮', '🐮🐮', '🐮🐮🐮'])

            with col5:
                task_energy = st.selectbox('这活儿多费劲？', ['💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'])
            creat_new_task = st.form_submit_button("Let's figure it out!!!")

        return {
            'task_date_begin': task_date_begin
            , 'task_date_end': task_date_end
            , 'task_name': task_name
            , 'task_description': task_description
            , 'task_emergency': task_emergency
            , 'task_energy': task_energy
            , 'creat_new_task_button': creat_new_task
            , 'task_important': task_important
            , 'task_creation_date': self.task_creation_date
        }

    @staticmethod
    def save_task(new_task_info):
        task_df = pd.read_csv('task_menu.csv')

        # 判断任务名是否为唯一值
        task_name_on_file = task_df['task_name'].to_list()
        if new_task_info['task_name'] in task_name_on_file:
            st.error('任务名重复啦，重取个名字吧')

        # 非空校验
        elif new_task_info['task_name'] == '' or new_task_info['task_description'] == '':
            st.error('名字和描述不能为空呀，二货')

        # 任务名不重复则新建成功
        else:
            new_task = pd.DataFrame(
                {
                    'task_name': [new_task_info['task_name']]
                    , 'task_begin_date': [new_task_info['task_date_begin']]
                    , 'task_end_date': [new_task_info['task_date_end']]
                    , 'task_description': [new_task_info['task_description']]
                    , 'task_emergency': [new_task_info['task_emergency']]
                    , 'task_energy': [new_task_info['task_energy']]
                    , 'task_important': [new_task_info['task_important']]
                    , 'task_status': ['待办']
                }
            )

            # 保存新录入的任务记录
            task_df = task_df.append(new_task)
            task_df.to_csv('task_menu.csv', index=False)
            st.balloons()
            st.success('存上了，滚去干活吧')

    @staticmethod
    def save_proj(new_proj_info):
        # 判断项目名是否重复
        proj_name_on_file = pd.read_csv('proj_menu.csv')['proj_name'].to_list()
        proj_name_on_file = set(proj_name_on_file)
        if new_proj_info['proj_name'] in proj_name_on_file:
            st.error('项目名重复啦，重取个名字吧')

        elif new_proj_info['proj_name'] == '' or new_proj_info['related_task_list'] == []:
            st.error('别拿空值来忽悠我，蠢货！')

        # 归档新建项目
        else:
            proj_df = pd.read_csv('proj_menu.csv')
            new_proj = pd.DataFrame(
                {
                    'proj_name': [new_proj_info['proj_name']] * len(new_proj_info['related_task_list'])
                    , 'related_task': new_proj_info['related_task_list']
                }
            )
            proj_df = proj_df.append(new_proj)
            proj_df.to_csv('proj_menu.csv', index=False)
            st.balloons()
            st.success('存上了，滚去干活吧')

    def proj_input(self):
        """
        录入项目
        :return: 项目名，项目按钮状态
        """
        proj_name = st.text_input('给你的大事取个响亮的名字！')

        # 读取任务列表
        task_menu = pd.read_csv('task_menu.csv')
        task_list = task_menu[task_menu['task_status'] == '待办']['task_name'].to_list()
        related_task_list = st.multiselect('这个世界不允许存在没有任务的项目', task_list)
        create_new_proj = st.button("Let's figure it out!!!")

        return {
            'proj_name': proj_name,
            'creat_new_proj_button': create_new_proj,
            'related_task_list': related_task_list,
            'creation_date': self.task_creation_date
        }


def main():
    header()

    # 获取一下当前时间，以后万一用得上呢
    task = Task(time.time())

    # 分俩tab
    tab1, tab2 = st.tabs(['干点小情！！', '干点大事！！'])
    with tab1:
        # 新任务信息
        new_task_info = task.task_input()
    with tab2:
        # 新项目信息
        new_proj_info = task.proj_input()

    # 点击保存按钮后生成新任务记录
    if new_task_info['creat_new_task_button']:
        task.save_task(new_task_info)
    # 点击保存按钮后生成新项目记录
    if new_proj_info['creat_new_proj_button']:
        task.save_proj(new_proj_info)

    # 日历功能
    if st.sidebar.checkbox('展现神迹吧！'):
        Cal.main()


if __name__ == '__main__':
    main()
