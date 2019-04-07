# 沙雕们的晚餐项目
## Quick Start
启动虚拟环境
```
source venv/bin/activate
```
导入数据
```python
python scripts/import_data.py
```
启动网站
```
python app.py
```
测试问句
命令行环境下
```bash
curl -H "Content-Type: application/json" -X POST  --data '{"question": "2018年招生计划?"}' http://localhost:5000/ask_question
```
或者使用reuqests库来测试
进入python中
```python
import requests
res = requests.post("http://localhost:5000/ask_question", data={'question':'毓泽奇的招生计划'})
print(res.json())
```