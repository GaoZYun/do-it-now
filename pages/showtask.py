# _*_ coding: utf-8 _*_
"""
@Time : 2022/12/09
@Author : Dasein
@Versionï¼V 3.0
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
        éç½®é¡¹
        :return:
        """
        st.sidebar.title('ðæç¹æï½')
        today_work_energy = st.sidebar.slider('è¯·è¾å¥è±å­å§ççé¼å¼', min_value=5, max_value=15,
                                              value=15)
        return today_work_energy

    @staticmethod
    def headers():
        # æ§æçæ é¢
        header_text_list = ['ð æå®åºæ¥ç¶åæ·¦å®',
                            'ðï¸ åèé²å¨å¬å¤ï½',
                            'ð§ð»âð» Macintosh æ¯å°çä¸æå¥½ç¨ç Mac',
                            'ð«¡ å¥½å§ï¼è±å­å§è¿æ¯çé¼ï¼',
                            'ð´ð¿ ä»¤äººå¤±æï¼ç·äººæ¯ä¸æ¥å¤§å§¨å¦ç',
                            'ð¥º å¤å¤å¤Â·Â·Â·Â·',
                            ]
        st.header(random.choice(header_text_list))

    def show_all_task(self):
        """
        ä»»å¡æ¥è¯¢
        :return:
        """

        # æ¥è¯¢æ¡ä»¶åç¬å°è£
        with st.form('æ¥è¯¢æ¡ä»¶'):
            col1, col2 = st.columns(2)
            with col1:
                searching_name = st.text_input('æä¸ªåå­')
            with col2:
                searching_status = st.selectbox('æä¸ªç¶æ', ['å¾å', 'å·²å'])

            col3, col4, col5, col6, col7, col8 = st.columns(6)
            with col7:
                searching_motive = st.form_submit_button('åååï¼', type='primary')
            with col8:
                # streamlit é¡µé¢äº§çäº¤äºç«å»å·æ°ï¼éç½®æé®ç©ºç½å³å¯
                st.form_submit_button('æ­£ç»éç½®')

        # å½è¾å¥çä»»å¡åä¸ºç©ºæ¶
        if searching_motive and searching_name is None:
            all_task_list = self.all_task_list[self.all_task_list['task_status'] == searching_status]
            self.show_card(all_task_list)

        # å½è¾å¥çä»»å¡åä¸ä¸ºç©ºæ¶
        elif searching_motive and searching_name is not None:
            all_task_list = self.all_task_list[self.all_task_list['task_status'] == searching_status]
            all_task_list = all_task_list[all_task_list.task_name.str.contains(searching_name)]
            self.show_card(all_task_list, key='3')

        # æªæ§è¡æç´¢æ¶
        else:
            all_task_list = self.all_task_list
            self.show_card(all_task_list, key='2')

    def show_today_task(self):
        st.markdown('#### ç´¯äºåï¼å¿«æ¥ä¸æ¯ðª³åå¡')
        today_task = self.today_task_pickup()
        self.show_card(today_task, key='1')

    def today_task_pickup(self):
        """
        ååºææä»æ¥å¾å
        :return:ç¬¦åå½åå·¥ä½å¼ºåº¦çä»»å¡æ¸å
        """
        # å¼å¥ææå¾åæ¸åï¼ç¶åå»ºç«ç´¢å¼
        all_ready_status_task_list = self.all_task_list[self.all_task_list['task_status'] == 'å¾å']
        all_ready_status_task_list.index = list(range(len(all_ready_status_task_list)))

        # ååºææè¦ç¨å°çå¼
        all_ready_task_name_list = all_ready_status_task_list['task_name'].to_list()
        all_ready_emergency_list = all_ready_status_task_list['task_emergency'].to_list()
        all_ready_important_list = all_ready_status_task_list['task_important'].to_list()
        all_ready_begein_date_list = all_ready_status_task_list['task_begin_date'].to_list()
        all_ready_end_date_list = all_ready_status_task_list['task_end_date'].to_list()

        # åæç§ç´§æ¥ç¨åº¦0.5ï¼éè¦ç¨åº¦0.6çæ¯ä¾è®¡ç®ä¼åç¨åº¦
        preferentially_list = []
        for i in all_ready_task_name_list:
            # è·åéè¦ç¨åº¦å¾å
            preferentially_value = len(all_ready_emergency_list[all_ready_task_name_list.index(i)]) * 0.6
            # è·åç»¼åå¾å
            preferentially_value = preferentially_value + len(
                all_ready_important_list[all_ready_task_name_list.index(i)]) * 0.5

            # å å¥æ¶é´å¤æ­å ç´ ï¼å¦æä»»å¡è¶æï¼åæå¤©æ° * 0.2 æåå½åä¼åçº§å¾å
            begin_date = all_ready_begein_date_list[all_ready_task_name_list.index(i)]
            end_date = all_ready_end_date_list[all_ready_task_name_list.index(i)]
            today_date = datetime.datetime.now().strftime('%Y-%m-%d')

            # å¼å§æ¶é´å¤§äºå½åæ¶é´ï¼è®¡ç®æ¥æå·®
            if datetime.datetime.strptime(today_date, '%Y-%m-%d') < datetime.datetime.strptime(begin_date, '%Y-%m-%d'):
                date_distance = datetime.datetime.strptime(begin_date, '%Y-%m-%d') - datetime.datetime.strptime(
                    today_date, '%Y-%m-%d')
                date_distance = date_distance.days
                # å°å¼å§æ¶é´å¤§äºä»æ¥çä»»å¡åå»¶åå¤ç
                preferentially_value_distance = preferentially_value * date_distance * 0.2
                preferentially_value = preferentially_value - preferentially_value_distance
            # ç»ææ¶é´å°äºä»å¤©ï¼è®¡ç®æ¥æå·®
            elif datetime.datetime.strptime(today_date, '%Y-%m-%d') > datetime.datetime.strptime(end_date, '%Y-%m-%d'):
                date_distance = datetime.datetime.strptime(today_date, '%Y-%m-%d') - datetime.datetime.strptime(
                    end_date, '%Y-%m-%d')
                date_distance = date_distance.days
                # å°ç»ææ¶é´å°äºä»æ¥çä»»å¡åæåå¤ç
                preferentially_value_distance = preferentially_value * date_distance * 0.2
                preferentially_value = preferentially_value + preferentially_value_distance
            # å¦æä¸å­å¨æ©åæå»¶ææåµï¼åæ­£å¸¸æ§è¡
            else:
                preferentially_value = preferentially_value
            # ææ°æ®ä¿å­ä¸ºåè¡¨
            preferentially_list.append(preferentially_value)

        # å¨åå§è¡¨æ ¼ä¸­å å¥ä¸å
        all_ready_status_task_list['preferentially_value'] = preferentially_list

        # æç§å¾åä»é«å°ä½æåºï¼éå»ºç´¢å¼
        all_ready_status_task_list.sort_values(by='preferentially_value', ascending=False, inplace=True)
        all_ready_status_task_list.index = list(range(len(all_ready_status_task_list)))

        # è®¡ç®å·¥ä½å¼ºåº¦
        today_energy = self.config()
        task_energy_list = all_ready_status_task_list['task_energy'].to_list()
        task_energy_value_list = []

        # åå¾åºå·¥ä½å¼ºåº¦
        for i in task_energy_list:
            task_energy_value_list.append(len(i))

        # æåºç¸å ï¼è·åå½åå·¥ä½ç¶æä¸è½å¹²å¤å°æ´»å¿
        data1 = [sum(task_energy_value_list[:x]) for x in range(1, len(task_energy_value_list) + 1)]
        # æç»æå å¥è¡¨ä¸­
        all_ready_status_task_list['data'] = data1

        # ç­éåºç¬¦åå½åå·¥ä½å¼ºåº¦çè¡ï¼å¿«å®æäºï¼
        all_ready_status_task_list = all_ready_status_task_list[all_ready_status_task_list['data'] <= today_energy]
        return all_ready_status_task_list

    def show_card(self, all_task, key):
        """
        æ ¹æ®æ¡ä»¶å±ç¤ºä»»å¡å¡ç
        :param key: ä¸ä¸ªç¨äºè¾¨å«èº«ä»½çå³é®å­
        :param all_task: ç¬¦åå½åç­éæ¡ä»¶ç Dataframe
        :return:
        """
        # æ§å¶å¡çç¶æ
        key_value = all_task.shape[0]
        card_status = st.checkbox('å±å¼/æå ', key=key_value)

        # åç»ä¼ è¿æ¥çè¡¨å»ºç´¢å¼ï¼é¿åæ¥ä¸å°
        all_task.index = list(range(len(all_task)))

        # ç»ææè¦ç¨å°çä¸è¥¿åå¥½ç±»
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

        # éå task_name åï¼åå»ºå¡ç
        for name in task_name_list:
            with st.expander(name, expanded=card_status):
                # å¡ççåå®¹
                col111, col222, col333, col44 = st.columns(4)
                with col111:
                    # ç¨éåå°çnameçä¸æ æ¥åå¶ä»å¯¹åºçå¼
                    st.markdown(
                        '**å§:' + task_begin_date_list[task_name_list.to_list().index(name)] + '  |  ' + 'ç»:' +
                        task_end_date_list[task_name_list.to_list().index(name)] + "**")

                # å¢å åç»æ¥ææ¥çåè½
                if task_status[task_name_list.to_list().index(name)] == 'å·²å':
                    with col333:
                        st.markdown(' **<font color=#A9A9A9 >åç»æ¥æï¼{}</font>**'.format(
                            task_recording_motive_date[task_name_list.to_list().index(name)]), unsafe_allow_html=True)

                # éå¯¹æåä»»å¡å¢å æ ç­¾è¯´æ
                elif datetime.datetime.strptime(task_begin_date_list[task_name_list.to_list().index(name)],
                                                '%Y-%m-%d') > now:
                    with col333:
                        st.markdown(' **<font color=#A9A9A9 >æå</font>**', unsafe_allow_html=True)

                # éå¯¹å»¶æä»»å¡å¢å æ ç­¾è¯´æ
                elif datetime.datetime.strptime(task_end_date_list[task_name_list.to_list().index(name)],
                                                '%Y-%m-%d') < yesterday:
                    with col333:
                        st.markdown(' **<font color=#FF000 >å»¶æ</font>**', unsafe_allow_html=True)

                with col44:
                    st.markdown('**' + task_status[task_name_list.to_list().index(name)] + '**')
                st.write(task_description_list[task_name_list.to_list().index(name)])
                col11, col22, col33, col44 = st.columns(4)
                with col11:
                    st.write('ç«æ¥ç«ç:' + task_emergency_list[task_name_list.to_list().index(name)])
                with col22:
                    st.write('ç´¯å¦?:' + task_energy_list[task_name_list.to_list().index(name)])
                with col33:
                    st.write('å¬çäºº:' + task_important_list[task_name_list.to_list().index(name)])

                # å¾å/å·²ååæ¢
                with col44:
                    if task_status[task_name_list.to_list().index(name)] == 'å¾å':
                        task_target_status = st.button('è½¬ä¸ºå·²å', key=name + key, type='primary')

                        if task_target_status:
                            self.task_status_motive(task_status[task_name_list.to_list().index(name)], name)

                    elif task_status[task_name_list.to_list().index(name)] == 'å·²å':
                        task_target_status = st.button('è½¬ä¸ºå¾å', key=name + key)
                        if task_target_status:
                            self.task_status_motive_to_pre(name)

    def task_status_motive(self, task_status_now, task_name):
        """
        åæ¢æé®ç¶æ
        :param task_name: ä»»å¡åï¼ç¨äºå®ä½
        :param task_status_now:å¾åæå·²å
        :return:
        """
        task_menu = self.all_task_list
        if task_status_now == 'å¾å':
            # ç¨atæ¹æ³æ¯è¾å¿«
            task_menu.at[task_menu['task_name'].to_list().index(task_name), 'task_status'] = 'å·²å'
            # ä¿å­å½åæ¥æ
            task_menu.at[task_menu['task_name'].to_list().index(
                task_name), 'task_recording_motive_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
            task_menu.to_csv('task_menu.csv', index=False)
            # ä¿å­æä»¶åå·æ°å¨å±
            st.experimental_rerun()
        elif task_status_now == 'å·²å':
            task_menu.at[task_menu['task_name'].to_list().index(task_name), 'task_status'] = 'å¾å'
            task_menu.to_csv('task_menu.csv', index=None)
            st.experimental_rerun()

    def task_status_motive_to_pre(self, task_name):
        """
        åæ¢ä»»å¡ç¶æè³å¾å
        :param task_name:
        :return:
        """
        task_menu = self.all_task_list
        task_menu.at[task_menu['task_name'].to_list().index(task_name), 'task_status'] = 'å¾å'
        task_menu.to_csv('task_menu.csv', index=None)
        st.experimental_rerun()


def main():
    # åä¸ªæ¶é´æ³ï¼é¿åä»¥åç¨å¾å°
    show_task = ShowTask()
    show_task.headers()
    tab1, tab2 = st.tabs(['ä»å¿ä¸ªéä¸æ³', 'æ¥ç¹ç¦èçï½'])
    with tab1:
        show_task.show_today_task()
        st.caption(
            'ä½ å¿é¡»å¨æ¯æ¥å·¥ä½ç»æåç»ä¸ä¿®æ¹ãæ¯æ¥æ¸åãä¸­çä»»å¡ç¶æï¼æèæ¯å®æä¸ä¸ªä»»å¡å°±ç«å³è¯ä¼°èªå·±çç¶æå¹¶ä¿®æ¹ãæç¹æãï¼ä¸ç¶å®ä¼ç»ä½ å¡æ°ä»»å¡ï¼ç´å°æä½ ç´¯æ­»ð±ð±ð±')
    with tab2:
        show_task.show_all_task()
        st.caption('è¿éåªè½è¿è¡æéçç»´æ¤ï¼streamlitç¹æ§éå¶ï¼ï¼æ³è¦è¿è¡æ´ä½ç»´æ¤ï¼è¯·å»å½æ¡£CSVå¦å¦å¦')


if __name__ == '__main__':
    main()

