import labels
import pandas as pd
import os
import matplotlib.pyplot as plt

# 设置文件夹路径
folder_path = 'D:\\CODE\\Python\\rentalhousingdataanalysis\\RentFromDanke'

# 获取文件夹下所有的文件名
files = os.listdir(folder_path)

# 筛选出以 .csv 结尾的文件
csv_files = [f for f in files if f.endswith('.csv')]

# 创建一个空的数据框
merged_data = pd.DataFrame()

# 遍历所有CSV文件并将它们合并在一起
for file in csv_files:
    # 读取指定路径下的CSV文件
    temp_data = pd.read_csv(os.path.join(folder_path, file), engine='pyarrow')

    # 删除全为空值的行
    temp_data.dropna(how='all', inplace=True)

    # 将当前文件的数据追加到主数据框中
    merged_data = pd.concat([merged_data, temp_data], ignore_index=True)

# 查看合并后的数据集基本信息和前几行数据
print('数据基本信息：')
merged_data.info()

# 查看数据集行数和列数
rows, columns = merged_data.shape

if rows < 100 and columns < 20:
    # 短表数据（行数少于100且列数少于20）查看全量数据信息
    print('数据全部内容信息：')
    print(merged_data.to_markdown(numalign='left', stralign='left'))
else:
    # 长表数据查看数据前几行信息
    print('数据前几行内容信息：')
    print(merged_data.head().to_markdown(numalign='left', stralign='left'))

# 删除缺失值所在行并重置索引
merged_data.dropna(inplace=True)
merged_data = merged_data.reset_index(drop=True)

# 删除重复值
merged_data.drop_duplicates(inplace=True)

# 处理错误值（假设错误值定义为负的数值）
# 找出所有数值型列
numeric_cols = merged_data.select_dtypes(include='number').columns
# 遍历每一个数值型列
for col in numeric_cols:
    # 筛选出负值所在的行
    negative_rows = merged_data[col] < 0
    # 删除这些行
    merged_data = merged_data[~negative_rows]

# 输出结果
csv_path = 'D:\\CODE\\Python\\rentalhousingdataanalysis\\RentFromDanke\\merged_data_danke.csv'
merged_data.to_csv(csv_path)




#下面给出的是数据分析过程，绘制了房源地区分布直方图，价格前十小区分布直方图，是否是电梯房的饼状图，离地铁站距离多少的折线图，户型直方图，以及面积价格直方图。
#如果要运行这些分析，需要先安装matplotlib库，可以通过pip命令进行安装，让后执行以下代码，绘制的每个图都需要单独执行

# # 绘制房源地区分布
# # 设置中文字体为黑体，解决中文显示问题
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# # 提取地区列数据
# area_data = merged_data['位置1']
# # 统计各地区出现的次数
# area_counts = area_data.value_counts()
# # 绘制地区分布直方图
# plt.figure(figsize=(12, 6))
# area_counts.plot(kind='bar')
# plt.xlabel('地区')
# plt.ylabel('房源数量')
# plt.title('房源地区分布')
# plt.xticks(rotation=90)
# plt.show()



# # #接下来我要画一个关于价格前十的小区直方图，横坐标为小区名称，纵坐标为价格，并在图中给出具体数值，颜色为蓝色
# # 设置中文字体为黑体，解决中文显示问题
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# merged_data['价格'] = pd.to_numeric(merged_data['价格'], errors='coerce')
# # 删除包含 NaN 的行
# merged_data = merged_data.dropna(subset=['价格'])
# # 或者填充 NaN 值
# merged_data['价格'].fillna(0, inplace=True)
#
# # 按照小区名称分组并计算平均价格
# grouped_by_community = merged_data.groupby('小区')['价格'].mean().sort_values(ascending=False)
# # 取价格前十的小区
# top_10_communities = grouped_by_community.head(10)
# # 绘制直方图
# plt.figure(figsize=(12, 6))
# plt.bar(top_10_communities.index, top_10_communities.values, color='blue')
# for i, value in enumerate(top_10_communities.values):
#     plt.text(i, value, f'{value:.0f}', ha='center', va='bottom')
# plt.xlabel('小区名称')
# plt.ylabel('价格')
# plt.title('价格前十小区价格分布')
# plt.xticks(rotation=90)
# plt.show()


# 接下来我要画一个关于是否是电梯房的饼状图，根据国家规定七层以上要装电梯，楼层高于七层为电梯房，楼层低于七层为非电梯房，给出数量和占比，分别用红色和蓝色表示
# # 检查函数，确保只对数字进行转换
# def is_elevator(x):
#     try:
#         floor = int(x.split('/')[0])
#         return '是' if floor > 7 else '否'
#     except ValueError:
#         return '未知'
# # 应用检查函数
# merged_data['是否电梯房'] = merged_data['楼层'].apply(is_elevator)
# # 统计电梯房和非电梯房的数量
# elevator_counts = merged_data['是否电梯房'].value_counts()
# # 设置中文字体为黑体，解决中文显示问题
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# # 绘制饼状图
# plt.figure(figsize=(6, 6))
# plt.pie(elevator_counts, labels=elevator_counts.index, autopct='%1.1f%%', colors=['red', 'blue'])
# plt.title('电梯房与非电梯房数量占比')
# plt.show()



# #接下来我要画一个关于离地铁站距离多少的折线图，分为500米以内，500到1000米以内，1000到1500米以内，1500到2000米以内四个房源的数量，图上给出具体房源数量，用绿色
# # 提取距离信息并转换为数值（单位：米）
# # 删除包含 NaN 的行
# merged_data['距离数值'] = merged_data['地铁'].str.extract('(\d+)米').dropna().astype(int)
# # 定义距离区间
# intervals = [0, 500, 1000, 1500, 2000]
# labels = ['500米以内', '500 - 1000米', '1000 - 1500米', '1500 - 2000米']
# # 统计各区间房源数量
# counts = []
# for i in range(len(intervals) - 1):
#     count = ((merged_data['距离数值'] >= intervals[i]) & (merged_data['距离数值'] < intervals[i + 1])).sum()
#     counts.append(count)
#
# # 设置中文字体为黑体，解决中文显示问题
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# # 绘制折线图
# plt.figure(figsize=(10, 6))
# plt.plot(labels, counts, marker='o', color='green')
# for i, count in enumerate(counts):
#     plt.text(i, count, str(count), ha='center', va='bottom')
# plt.xlabel('离地铁站距离区间')
# plt.ylabel('房源数量')
# plt.title('离地铁站不同距离房源数量分布')
# plt.show()




# #接下来我要画一个关于户型的直方图，横坐标为1 室 1 卫,2 室 1 卫,3 室 1 卫,4 室 1 卫,5 室 1 卫,6 室 1 卫，纵坐标为房源数量，分别用六种不同的颜色
# # 统计各户型的房源数量
# room_type_counts = merged_data['户型'].value_counts()
#
# # 选择需要绘制的户型
# selected_room_types = ['1室1卫', '2室1卫', '3室1卫', '4室1卫', '5室1卫', '6室1卫']
# selected_counts = room_type_counts[selected_room_types]
#
# # 设置中文字体为黑体，解决中文显示问题
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
#
# # 定义颜色列表
# colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow']
#
# # 绘制直方图
# plt.figure(figsize=(12, 6))
# plt.bar(selected_room_types, selected_counts, color=colors)
# for i, count in enumerate(selected_counts):
#     plt.text(i, count, str(count), ha='center', va='bottom')
# plt.xlabel('户型')
# plt.ylabel('房源数量')
# plt.title('不同户型房源数量分布')
# plt.xticks(rotation=90)
# plt.show()



# #接下来，我要画一个关于面积和价格的直方图，横坐标为面积分为0到30平方米，30到60,60到90,90到120，纵坐标为平均价格，分别用四种不同的颜色，要求跟前面一样直接从文件目录中调用
# # 定义面积区间
# area_bins = [0, 30, 60, 90, 120]
# labels = ['0-30平方米', '30-60平方米', '60-90平方米', '90-120平方米']
# # 将 '面积' 列转换为数值类型，无法转换的值设置为 NaN
# merged_data['面积'] = pd.to_numeric(merged_data['面积'], errors='coerce')
# # 计算各面积区间的平均价格
# # 使用 pd.cut 进行分段
# merged_data['面积区间'] = pd.cut(merged_data['面积'], bins=area_bins, labels=labels)
# # 可以选择删除或填充 NaN 值
# merged_data.dropna(subset=['面积'], inplace=True)
# # 检查 '价格' 列的数据类型
# print(merged_data['价格'].dtype)
# # 查看 '价格' 列中非数值类型的数据
# non_numeric_prices = merged_data[pd.to_numeric(merged_data['价格'], errors='coerce').isnull()]
# print(non_numeric_prices)
# # 清理非数值类型的数据，例如将其转换为 NaN 并删除或填充
# merged_data['价格'] = pd.to_numeric(merged_data['价格'], errors='coerce')
# merged_data = merged_data.dropna(subset=['价格'])
# # 再次计算平均价格
# average_price_by_area = merged_data.groupby('面积区间')['价格'].mean()
# # 设置中文字体为黑体，解决中文显示问题
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# # 绘制直方图
# plt.figure(figsize=(10, 6))
# plt.bar(average_price_by_area.index, average_price_by_area.values, color=['blue', 'green', 'red', 'purple'])
# for i, value in enumerate(average_price_by_area.values):
#     plt.text(i, value, f'{value:.0f}', ha='center', va='bottom')
# plt.xlabel('面积区间')
# plt.ylabel('平均价格')
# plt.title('不同面积区间房源的平均价格分布')
# plt.show()