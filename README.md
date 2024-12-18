1.下载代码

2.下载python

3.进入代码根目录，运行

​	```python 04-tieba.py```

xpath语法：2024/12/18 百度贴吧 xpath：
	提取下一页的链接： ```//*[@id="frs_list_pager"]/a[contains(text(), '下一页')]```

提取所有帖子的a标签：```//*[@id="thread_list"]/li[contains(@class, "j_thread_list")]/div/div[2]/div[1]/div/a```