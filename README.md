# do-it-now

## 说在前面
纯新手，代码极其乐色，勿喷

## 这玩意儿能干啥
do-it-now 是一个 ToDo list 工具，我的目标是实现高度自动化的，可以根据你每日的工作热忱自动为你分配任务，能让你专注眼前事项的工具。它非常适合用来帮老板来管理你自己。
目前，他实现了两个自动化功能：
* 根据所有待办清单中录入的重要、紧急和工作量维度，自动为你分配事物；
* 按照我们公司的要求，自动生成工作日报及月报。
* 在录入任务的页面还为你提供了日历热力图，帮助你更好地确定任务时限。

它未来还会实现的功能有：
* 项目视图功能，让你除了专注眼前的事务外，还给你提供长远目标；
* 标签漫游功能（类似 Obsidian），帮助你发现所有经手任务的内在联系；
* 其他·····

## requirement
```
pip3 install streamlit
pip3 install streamlit-echarts
pip3 install st-pages
pip3 install pyecharts
pip3 install pandas
```

## 运行方法
```
streamlit run run.py
```

## 注意事项
所有底层数据均用csv格式保存，别问我问啥·····
另外，在使用前，你需要先在本地创建 csv 表格，格式为：
|  task_name   | task_begin_date  |  task_end_date   | task_description  |  task_emergency   | task_energy  |  task_important   | task_status  | task_recording_motive_date  |
|  ----  | ----  |  ----  | ----  |  ----  | ----  |  ----  | ----  |  ----  |
| 示例task名  | 2022-1-1 | 2022-1-2  | 示例任务描述 | 🔥🔥  | 💪💪 | 🐮  | 已办（待办） | 2022-1-3  |

冲冲冲

