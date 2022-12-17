# _*_ coding: utf-8 _*_
"""
@Time : 2022/12/09
@Author : Dasein
@Version：V 3.0
@File : run.py
"""
import datetime
import streamlit as st
# 这个包支持自定义页面名称
from st_pages import Page, show_pages, add_page_title
import pages.日历

st.title('沙漠既走了样，必是风，遇到了直角')
st.markdown('你好啊，欢迎来到异世界')
st.markdown('这里现在还没有名字，但我可以告诉你你能在这里做什么')
st.markdown(
    '这里是一个管理任务清单的工具，我们的目标是实现一个高度自动化的，可以根据你每日的工作热忱自动为你分配任务的 **To-do list** 工具')
st.markdown('这个工具不聚焦于复杂的个人管理理论，只聚焦于两件事：')
st.markdown('* 你今天要做什么？')
st.markdown('* 你有哪些长期目标？')
st.markdown('多说无益，请从左边的菜单开始吧')
st.markdown('祝你成功')

st.sidebar.markdown('这东西目前有俩bug：')
st.sidebar.markdown(
    '一个是当今日清单 = 所有待办任务时，程序会出现报错，原因是此时在今日清单和所有清单的「待办/已办」转换 button 的 key 是相同的，只要录入一个新的待办/已办任务就可以解决这个问题(⬅️已经解决了～)')
st.sidebar.markdown('另一个是所有任务清单中的「展开/折叠」按钮无法与搜索同时生效，这个原因不明，以后再说吧～')

add_page_title()

show_pages(
    [
        Page("run.py", "欢迎来到异世界", "🏠"),
        Page("pages/showtask.py", "清单", "🧾"),
        Page("pages/inputtask.py", "录入", "🖊️"),
        Page("pages/report.py", '报告', "📰"),
    ]
)

if st.sidebar.checkbox('展现神迹吧！'):
    pages.日历.main()
