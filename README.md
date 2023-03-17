# -UrbanResilence_backend

git clone后，进入mysite的文件夹，与mange.py同级运行以下命令：
python3 manage.py runserver
访问http://127.0.0.1:8000/daping/rank_list

```json

[{"model": "daping.rankinglist", "pk": "\u897f\u6e56\u533a", "fields": {"count": 2}}, {"model": "daping.rankinglist", "pk": "\u9053\u91cc\u533a", "fields": {"count": 1}}]

```
与视图中的查询结果一致

表示后端程序已成功接受前端的请求，查询到数据中的视图并以json格式返回。
