# _*_ coding: utf-8 _*_
"""
@Time : 2022/12/09
@Author : Dasein
@Version：V 3.0
@File : task_page.py
"""
import pandas as pd
import streamlit as st
import random
import datetime


class ShowTask:
    def __init__(self):
        self.all_task_list = pd.read_csv('task_menu.csv')

    @staticmethod
    def config():
        """
        配置项
        :return:
        """
        st.sidebar.title('💋撒点料～')
        today_work_energy = st.sidebar.slider('请输入英子姐的牛逼值', min_value=5, max_value=15,
                                              value=15)
        return today_work_energy

    @staticmethod
    def headers():
        # 性感的标题
        header_text_list = ['👀 搜它出来然后淦它',
                            '👁️ 克苏鲁在召唤～',
                            '🧑🏻‍💻 Macintosh 是地球上最好用的 Mac',
                            '🫡 好吧，英子姐还是牛逼！',
                            '👴🏿 令人失望，男人是不来大姨妈的',
                            '🥺 嘤嘤嘤····',
                            ]
        st.header(random.choice(header_text_list))

    def show_all_task(self):
        """
        任务查询
        :return:
        """

        # 查询条件单独封装
        with st.form('查询条件'):
            col1, col2 = st.columns(2)
            with col1:
                searching_name = st.text_input('搜个名字')
            with col2:
                searching_status = st.selectbox('搜个状态', ['待办', '已办'])

            col3, col4, col5, col6, col7, col8 = st.columns(6)
            with col7:
                searching_motive = st.form_submit_button('嗖嗖嗖！', type='primary')
            with col8:
                # streamlit 页面产生交互立刻刷新，重置按钮空白即可
                st.form_submit_button('正经重置')

        # 当输入的任务名为空时
        if searching_motive and searching_name is None:
            all_task_list = self.all_task_list[self.all_task_list['task_status'] == searching_status]
            self.show_card(all_task_list)

        # 当输入的任务名不为空时
        elif searching_motive and searching_name is not None:
            all_task_list = self.all_task_list[self.all_task_list['task_status'] == searching_status]
            all_task_list = all_task_list[all_task_list.task_name.str.contains(searching_name)]
            self.show_card(all_task_list, key='3')

        # 未执行搜索时
        else:
            all_task_list = self.all_task_list
            self.show_card(all_task_list, key='2')

    def show_today_task(self):
        st.markdown('#### 累了吗，快来一杯🪳咖啡')
        today_task = self.today_task_pickup()
        self.show_card(today_task, key='1')

    def today_task_pickup(self):
        """
        取出所有今日待办
        :return:符合当前工作强度的任务清单
        """
        # 引入所有待办清单，然后建立索引
        all_ready_status_task_list = self.all_task_list[self.all_task_list['task_status'] == '待办']
        all_ready_status_task_list.index = list(range(len(all_ready_status_task_list)))

        # 取出所有要用到的值
        all_ready_task_name_list = all_ready_status_task_list['task_name'].to_list()
        all_ready_emergency_list = all_ready_status_task_list['task_emergency'].to_list()
        all_ready_important_list = all_ready_status_task_list['task_important'].to_list()
        all_ready_begein_date_list = all_ready_status_task_list['task_begin_date'].to_list()
        all_ready_end_date_list = all_ready_status_task_list['task_end_date'].to_list()

        # 先按照紧急程度0.5，重要程度0.6的比例计算优先程度
        preferentially_list = []
        for i in all_ready_task_name_list:
            # 获取重要程度得分
            preferentially_value = len(all_ready_emergency_list[all_ready_task_name_list.index(i)]) * 0.6
            # 获取综合得分
            preferentially_value = preferentially_value + len(
                all_ready_important_list[all_ready_task_name_list.index(i)]) * 0.5

            # 加入时间判断因素，如果任务超期，则按天数 * 0.2 提升当前优先级得分
            begin_date = all_ready_begein_date_list[all_ready_task_name_list.index(i)]
            end_date = all_ready_end_date_list[all_ready_task_name_list.index(i)]
            today_date = datetime.datetime.now().strftime('%Y-%m-%d')

            # 开始时间大于当前时间，计算日期差
            if datetime.datetime.strptime(today_date, '%Y-%m-%d') < datetime.datetime.strptime(begin_date, '%Y-%m-%d'):
                date_distance = datetime.datetime.strptime(begin_date, '%Y-%m-%d') - datetime.datetime.strptime(
                    today_date, '%Y-%m-%d')
                date_distance = date_distance.days
                # 将开始时间大于今日的任务做延后处理
                preferentially_value_distance = preferentially_value * date_distance * 0.2
                preferentially_value = preferentially_value - preferentially_value_distance
            # 结束时间小于今天，计算日期差
            elif datetime.datetime.strptime(today_date, '%Y-%m-%d') > datetime.datetime.strptime(end_date, '%Y-%m-%d'):
                date_distance = datetime.datetime.strptime(today_date, '%Y-%m-%d') - datetime.datetime.strptime(
                    end_date, '%Y-%m-%d')
                date_distance = date_distance.days
                # 将结束时间小于今日的任务做提前处理
                preferentially_value_distance = preferentially_value * date_distance * 0.2
                preferentially_value = preferentially_value + preferentially_value_distance
            # 如果不存在早做或延期情况，则正常执行
            else:
                preferentially_value = preferentially_value
            # 把数据保存为列表
            preferentially_list.append(preferentially_value)

        # 在原始表格中加入一列
        all_ready_status_task_list['preferentially_value'] = preferentially_list

        # 按照得分从高到低排序，重建索引
        all_ready_status_task_list.sort_values(by='preferentially_value', ascending=False, inplace=True)
        all_ready_status_task_list.index = list(range(len(all_ready_status_task_list)))

        # 计算工作强度
        today_energy = self.config()
        task_energy_list = all_ready_status_task_list['task_energy'].to_list()
        task_energy_value_list = []

        # 先得出工作强度
        for i in task_energy_list:
            task_energy_value_list.append(len(i))

        # 按序相加，获取当前工作状态下能干多少活儿
        data1 = [sum(task_energy_value_list[:x]) for x in range(1, len(task_energy_value_list) + 1)]
        # 把结果加入表中
        all_ready_status_task_list['data'] = data1

        # 筛选出符合当前工作强度的行（快完成了）
        all_ready_status_task_list = all_ready_status_task_list[all_ready_status_task_list['data'] <= today_energy]
        return all_ready_status_task_list

    def show_card(self, all_task, key):
        """
        根据条件展示任务卡片
        :param key: 一个用于辨别身份的关键字
        :param all_task: 符合当前筛选条件的 Dataframe
        :return:
        """
        # 控制卡片状态
        key_value = all_task.shape[0]
        card_status = st.checkbox('展开/折叠', key=key_value)

        # 先给传进来的表建索引，避免查不到
        all_task.index = list(range(len(all_task)))

        # 给所有要用到的东西分好类
        task_name_list = all_task['task_name']
        task_begin_date_list = all_task['task_begin_date']
        task_end_date_list = all_task['task_end_date']
        task_description_list = all_task['task_description']
        task_emergency_list = all_task['task_emergency']
        task_energy_list = all_task['task_energy']
        task_important_list = all_task['task_important']
        task_status = all_task['task_status']
        task_recording_motive_date = all_task['task_recording_motive_date']
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)

        # 遍历 task_name 列，创建卡片
        for name in task_name_list:
            with st.expander(name, expanded=card_status):
                # 卡片的内容
                col111, col222, col333, col44 = st.columns(4)
                with col111:
                    # 用遍历到的name的下标来取其他对应的值
                    st.markdown(
                        '**始:' + task_begin_date_list[task_name_list.to_list().index(name)] + '  |  ' + '终:' +
                        task_end_date_list[task_name_list.to_list().index(name)] + "**")

                # 增加办结日期查看功能
                if task_status[task_name_list.to_list().index(name)] == '已办':
                    with col333:
                        st.markdown(' **<font color=#A9A9A9 >办结日期：{}</font>**'.format(
                            task_recording_motive_date[task_name_list.to_list().index(name)]), unsafe_allow_html=True)

                # 针对提前任务增加标签说明
                elif datetime.datetime.strptime(task_begin_date_list[task_name_list.to_list().index(name)],
                                                '%Y-%m-%d') > now:
                    with col333:
                        st.markdown(' **<font color=#A9A9A9 >提前</font>**', unsafe_allow_html=True)

                # 针对延期任务增加标签说明
                elif datetime.datetime.strptime(task_end_date_list[task_name_list.to_list().index(name)],
                                                '%Y-%m-%d') < yesterday:
                    with col333:
                        st.markdown(' **<font color=#FF000 >延期</font>**', unsafe_allow_html=True)

                with col44:
                    st.markdown('**' + task_status[task_name_list.to_list().index(name)] + '**')
                st.write(task_description_list[task_name_list.to_list().index(name)])
                col11, col22, col33, col44 = st.columns(4)
                with col11:
                    st.write('火急火燎:' + task_emergency_list[task_name_list.to_list().index(name)])
                with col22:
                    st.write('累否?:' + task_energy_list[task_name_list.to_list().index(name)])
                with col33:
                    st.write('催的人:' + task_important_list[task_name_list.to_list().index(name)])

                # 待办/已办切换
                with col44:
                    if task_status[task_name_list.to_list().index(name)] == '待办':
                        task_target_status = st.button('转为已办', key=name + key, type='primary')

                        if task_target_status:
                            self.task_status_motive(task_status[task_name_list.to_list().index(name)], name)

                    elif task_status[task_name_list.to_list().index(name)] == '已办':
                        task_target_status = st.button('转为待办', key=name + key)
                        if task_target_status:
                            self.task_status_motive_to_pre(name)

    def task_status_motive(self, task_status_now, task_name):
        """
        切换按钮状态
        :param task_name: 任务名，用于定位
        :param task_status_now:待办或已办
        :return:
        """
        task_menu = self.all_task_list
        if task_status_now == '待办':
            # 用at方法比较快
            task_menu.at[task_menu['task_name'].to_list().index(task_name), 'task_status'] = '已办'
            # 保存当前日期
            task_menu.at[task_menu['task_name'].to_list().index(
                task_name), 'task_recording_motive_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
            task_menu.to_csv('task_menu.csv', index=False)
            # 保存文件后刷新全局
            st.experimental_rerun()
        elif task_status_now == '已办':
            task_menu.at[task_menu['task_name'].to_list().index(task_name), 'task_status'] = '待办'
            task_menu.to_csv('task_menu.csv', index=None)
            st.experimental_rerun()

    def task_status_motive_to_pre(self, task_name):
        """
        切换任务状态至待办
        :param task_name:
        :return:
        """
        task_menu = self.all_task_list
        task_menu.at[task_menu['task_name'].to_list().index(task_name), 'task_status'] = '待办'
        task_menu.to_csv('task_menu.csv', index=None)
        st.experimental_rerun()


def main():
    # 取个时间戳，避免以后用得到
    show_task = ShowTask()
    show_task.headers()
    tab1, tab2 = st.tabs(['今儿个针不戳', '来点焦虑的～'])
    with tab1:
        show_task.show_today_task()
        st.caption(
            '你必须在每日工作结束后统一修改「每日清单」中的任务状态，或者每完成一个任务就立即评估自己的状态并修改「撒点料」，不然它会给你塞新任务，直到把你累死😱😱😱')
    with tab2:
        show_task.show_all_task()
        st.caption('这里只能进行有限的维护（streamlit特性限制），想要进行整体维护，请去归档CSV呦呦呦')


if __name__ == '__main__':
    main()

