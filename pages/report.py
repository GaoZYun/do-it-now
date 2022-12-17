# _*_ coding: utf-8 _*_
"""
@Time : 2022/12/13
@Author : Dasein
@Version：V 3.0
@File : report.py
"""
import datetime
import time
import streamlit as st
from pages import showtask
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts


class Report:
    def __init__(self):
        self.task_menu_list = pd.read_csv('task_menu.csv')

    def get_daily_report(self):
        task_menu_list = self.task_menu_list

        # 获取需要的日期
        date = st.date_input('选个日期')

        # 判断哪些任务是今日完成的
        today_finish_task_menu_list = task_menu_list[task_menu_list['task_recording_motive_date'] == str(date)]
        # 序号
        x = 1

        # 日报标题
        st.markdown('### ' + str(date) + ' 工作日报')

        # 循环取数，生成今日工作内容
        st.markdown('##### ' + ' 今日工作内容')
        for i in today_finish_task_menu_list.iloc:
            # 日报正文
            st.markdown(str(x) + '.**' + i['task_name'] + '**：' + i['task_description'])
            x += 1

        # 用 pickup 功能取出明日工作计划
        plan_task = showtask.ShowTask()
        plan_task = plan_task.today_task_pickup()

        # 生成工作计划内容
        y = 1
        st.markdown('##### ' + ' 明日工作计划')
        for i in plan_task.iloc:
            st.markdown(str(y) + '.**' + i['task_name'] + '**：' + i['task_description'])
            y += 1

    def get_monthly_report(self):
        """
        月报生成
        :return:
        """

        def return_range_day_datetime(start_dt, end_dt):
            """
            获取两个日期之间的 datetime 日期列表
            :param start_dt:  2022-10-01
            :param end_dt: 2022-10-10
            :return: ['2022-10-01', '2022-10-02', ...]
            """
            dates = []
            while start_dt <= end_dt:
                dates.append(start_dt.strftime('%Y-%m-%d'))
                start_dt += datetime.timedelta(days=1)

            return dates

        task_menu_list = self.task_menu_list
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input('开始日期')
        with col2:
            end_date = st.date_input('结束日期')

        st.markdown('### ' + ' 营销2.0集中工作总结')
        st.markdown('##### (' + start_date.strftime('%Y年%m月%d日') + '至' + end_date.strftime('%Y年%m月%d日') + ')')
        st.markdown('##### 一、工作完成情况')

        # 获取当前选择日期区间内的工作内容
        date_list = return_range_day_datetime(start_date, end_date)
        month_task = task_menu_list[task_menu_list['task_recording_motive_date'].isin(date_list)]

        # 这俩哥们是序号
        x = 1
        y = 1

        # 获取重点工作内容
        st.markdown('##### （一）重点工作')
        important_task = month_task[(month_task['task_important'] == '🐮🐮🐮') | (month_task['task_important'] == '🐮🐮')]
        for i in important_task.iloc:
            # 日报正文
            st.markdown(str(x) + '.**' + i['task_name'] + '**：' + i['task_description'])
            x += 1

        # 获取日常工作内容
        st.markdown('##### （二）常态工作')
        important_task = month_task[month_task['task_important'] == '🐮']
        for i in important_task.iloc:
            # 日报正文
            st.markdown(str(y) + '.**' + i['task_name'] + '**：' + i['task_description'])
            y += 1


def main():
    report = Report()
    tab1, tab2 = st.tabs(['日报', '月报', ])
    with tab1:
        report.get_daily_report()
    with tab2:
        report.get_monthly_report()


if __name__ == '__main__':
    main()
