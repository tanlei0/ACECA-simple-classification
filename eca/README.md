# ACCA模拟的实现

## acca文件夹

### ACECA.py

异步ECA

### ECA.py

ECA

### m2_2m.py

$m^2+2m$的ACCA模拟ECA

### m3.py

$m^3$ 的ACCA模拟ECA

### plot_ACCA.py

绘制模拟的结果

* plot_line()

  绘制ECA运行次数和ACCA运行次数的关系图

* plot_all_space

  绘制细胞自动机模拟结果图，对于ACCA来说，会给定一个采样间隔，以此来更好展示模拟效果

* get_run_datas_multi

  获取运行次数的对应关系，这里采用了多进程来加快数据的获取

**绘制运行次数关系图：**

```python
# 获取各个CA的运行次数
get_run_datas_multi(save_path="./result/multi_data.json") 
# 将结果保存为excel
json2excel(json_path="./result/multi_data.json") 
# 将保存运行次数的文件绘制成函数关系图
plot_line(path="./result/multi_data.json")
```

 colors = ['red', 'yellow', 'blue']
 alphas = [1.0, 0.5, 0.2]
 m2 虚线
 m3 实线

![acca-aca-run-times](/home/cmk/projectE/pycharmP/ECA/acca/result/plot/acca-aca-run-times.jpeg)

**绘制所有CA的模拟结果** 

```python
plot_all_space()
```

**ECA_run50_cell201_rule90**

![ECA_run50_cell201_rule90](/home/cmk/projectE/pycharmP/ECA/acca/result/ECA_run50_cell201_rule90.jpeg)

**m2_alpha=0.2_carunnum=50_runnum=16282_run=16282_cell=201_每隔60取一次**

![m2_alpha=0.2_carunnum=50_runnum=16282_run=16282_cell=201_每隔60取一次](/home/cmk/projectE/pycharmP/ECA/acca/result/m2_alpha=0.2_carunnum=50_runnum=16282_run=16282_cell=201_每隔60取一次.jpeg)	

**m2_alpha=0.5_carunnum=50_runnum=6625_run=6625_cell=201_每隔24取一次**

![m2_alpha=0.5_carunnum=50_runnum=6625_run=6625_cell=201_每隔24取一次](/home/cmk/projectE/pycharmP/ECA/acca/result/m2_alpha=0.5_carunnum=50_runnum=6625_run=6625_cell=201_每隔24取一次.jpeg)

**m2_alpha=1.0_carunnum=50_runnum=3416_run=3416_cell=201_每隔12取一次**

![m2_alpha=1.0_carunnum=50_runnum=3416_run=3416_cell=201_每隔12取一次](/home/cmk/projectE/pycharmP/ECA/acca/result/m2_alpha=1.0_carunnum=50_runnum=3416_run=3416_cell=201_每隔12取一次.jpeg)

**m3_alpha=0.2_carunnum=50_runnum=5885_run=5885_cell=201_每隔40取一次**

![m3_alpha=0.2_carunnum=50_runnum=5885_run=5885_cell=201_每隔40取一次](/home/cmk/projectE/pycharmP/ECA/acca/result/m3_alpha=0.2_carunnum=50_runnum=5885_run=5885_cell=201_每隔40取一次.jpeg)



**m3_alpha=0.5_carunnum=50_runnum=2319_run=2319_cell=201_每隔16取一次**

![m3_alpha=0.5_carunnum=50_runnum=2319_run=2319_cell=201_每隔16取一次](/home/cmk/projectE/pycharmP/ECA/acca/result/m3_alpha=0.5_carunnum=50_runnum=2319_run=2319_cell=201_每隔16取一次.jpeg)

**m3_alpha=1.0_carunnum=50_runnum=1094_run=1094_cell=201_每隔8取一次**

![m3_alpha=1.0_carunnum=50_runnum=1094_run=1094_cell=201_每隔8取一次](/home/cmk/projectE/pycharmP/ECA/acca/result/m3_alpha=1.0_carunnum=50_runnum=1094_run=1094_cell=201_每隔8取一次.jpeg)



### utils.py

一些工具函数 

