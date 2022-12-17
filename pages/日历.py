# _*_ coding: utf-8 _*_
"""
@Time : 2022/12/16
@Author : Dasein
@Version：V 3.0
@File : Calendar.py
"""
import random
import pandas as pd
import streamlit as st
from datetime import datetime
from pyecharts import options as opts
from pyecharts.charts import Calendar
import streamlit_echarts
from pages.showtask import ShowTask


class CalendarSt(ShowTask):
    def __init__(self):
        super().__init__()

    def reshape_task_data(self):
        """
        整理时间数据
        :return: DataFrame{}
        """
        # 导入数据
        all_task_list = self.all_task_list
        all_task_list = all_task_list[all_task_list['task_status'] == '待办']

        # 把任务持续时间压平
        date_continue_area = []
        for i in all_task_list.iloc:
            begin_date = datetime.strptime(i['task_begin_date'], '%Y-%m-%d')
            end_date = datetime.strptime(i['task_end_date'], '%Y-%m-%d')
            date_range = pd.date_range(begin_date, end_date)
            date_continue_area.append([datetime.strftime(b, '%Y-%m-%d') for b in date_range])

        all_task_list['date_range'] = date_continue_area

        # 最小开始日期
        begin_date_list = all_task_list['task_begin_date'].to_list()
        min_date = []
        for i in begin_date_list:
            min_date.append(datetime.strptime(i, '%Y-%m-%d'))
        min_date = min(min_date)

        # 最大结束日期
        end_date_list = all_task_list['task_end_date'].to_list()
        max_date = []
        for i in end_date_list:
            max_date.append(datetime.strptime(i, '%Y-%m-%d'))
        max_date = max(max_date)

        # 获取日期区间列表
        date_list = pd.date_range(min_date, max_date)
        str_date_list = []
        for i in date_list:
            str_date_list.append(i.strftime('%Y-%m-%d'))

        # 获取每个日期对应的任务列表
        final_date_list = []
        final_task_name_list = []
        final_task_description_list = []
        final_task_emergency_list = []
        final_task_energy_list = []
        final_task_important_list = []
        for i in str_date_list:
            for k in all_task_list.iloc:
                if i in k['date_range']:
                    final_date_list.append(i)
                    final_task_name_list.append(k['task_name'])
                    final_task_description_list.append(k['task_description'])
                    final_task_emergency_list.append(k['task_emergency'])
                    final_task_energy_list.append(k['task_energy'])
                    final_task_important_list.append(k['task_important'])

        final_task_by_date = pd.DataFrame(
            {
                'date_list': final_date_list
                , 'task_name': final_task_name_list
                , 'task_description': final_task_description_list
                , 'task_emergency': final_task_emergency_list
                , 'task_energy': final_task_energy_list
                , 'task_important': final_task_important_list
            },
        )

        def get_energy_len(energy_icon):
            return len(energy_icon)

        final_task_by_date['energy_len'] = final_task_by_date['task_energy'].apply(get_energy_len)

        return final_task_by_date

    def show_plot(self):
        # 初始化数据
        df = self.reshape_task_data()
        date_list = set(df['date_list'].to_list())
        value_list = []
        for i in date_list:
            value = df[df['date_list'] == i]
            value = value['energy_len'].to_list()
            value = sum(value)
            value_list.append(value)

        data = list(zip(date_list, value_list))

        calendar = Calendar()

        # 选择显示方式，整年还是本月
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            user_choose_opts = st.selectbox('选择显示方式', ['本月', '整年'])
        if user_choose_opts == '整年':
            user_choose_opts = datetime.now().strftime('%Y')
            user_choose_orient = 'horizontal'
            user_choose_label = False
        else:
            user_choose_opts = datetime.now().strftime('%Y-%m')
            user_choose_orient = 'vertical'
            user_choose_label = True

        # 开始画图
        calendar.add(
            '',
            yaxis_data=data,

            # 日历基本设置
            calendar_opts=opts.CalendarOpts(
                range_=user_choose_opts,  # 显示方式

                # 设置中文
                daylabel_opts=opts.CalendarDayLabelOpts(name_map="cn"),
                monthlabel_opts=opts.CalendarMonthLabelOpts(name_map="cn"),

                # 根据显示方式调整方向
                orient=user_choose_orient,

                # 放大
                pos_bottom='0%',
                pos_top='20%',

                # 不显示年份
                yearlabel_opts=opts.CalendarYearLabelOpts(
                    is_show=False,
                ),

            ),

            # 配置标签内容
            label_opts=opts.LabelOpts(

                # 根据显示方式决定是否显示标签，全年不显示
                is_show=user_choose_label,

                # 标签内容（Pyecharts 的标签显示功能实在不够强大
                formatter='{c}',

                # 标签字体颜色
                color='white',

                # 标签字体大小
                font_size=11,
                position='insideTop',
                font_weight='bolder',
                font_family='Microsoft YaHei'
            )
        )
        calendar.set_global_opts(

            # 添加滑块组件
            visualmap_opts=opts.VisualMapOpts(
                orient='vertical',
                max_=20,
                pos_left='0%',
                pos_top='20%',
                range_text=None,
                textstyle_opts=opts.TextStyleOpts(
                    color='white'
                )
            ),

            # 悬浮展示内容（太不够强大了）
            tooltip_opts=opts.TooltipOpts(
                axis_pointer_type='cross'
            ),
        )

        streamlit_echarts.st_pyecharts(calendar, height='440px')


def main():
    calendar = CalendarSt()
    calendar.reshape_task_data()
    calendar.show_plot()


if __name__ == '__main__':
    main()
