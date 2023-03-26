## <div align="center">前景</div>

在我校行为规范管理的背景下，我突发奇想，想使用AI帮助规范检查。于是，这个项目便产生了。[Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)的支持下完成的.[Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) 是由 [Ultralytics](https://ultralytics.com) 开发的一个前沿的SOTA 模型。它在以前成功的 YOLO 版本基础上，引入了新的功能和改进，进一步提升了其性能和灵活性。基于快速、准确和易于使用的设计理念，使其成为广泛的目标检测、图像分割和图像分类任务的绝佳选择。

## <div align="center">文档</div>
<details open>
<summary>安装</summary>

Pip 安装包含所有 [requirements.txt](https://github.com/ultralytics/ultralytics/blob/main/requirements.txt) 的包，环境要求 [**Python>=3.7**](https://www.python.org/)，且 [\*\*PyTorch>=1.7
\*\*](https://pytorch.org/get-started/locally/)。

```bash
pip install -r requirements.txt
```

</details>

<details open>
<summary>使用方法</summary>

该项目由于时间原因没有做UI以及其他功能，只能在命令行界面（CLI）中使用 `python` 命令运行：

```bash
python Main.py
```
效果会在摄像头上标出红领巾的位置
具体如下：

![Alt](https://s.imgkb.xyz/abcdocker/2023/03/26/cff41e0db1389/cff41e0db1389.png)
![Alt](https://s.imgkb.xyz/abcdocker/2023/03/26/0a092fc915e01/0a092fc915e01.png)
![Alt](https://s.imgkb.xyz/abcdocker/2023/03/26/e3ae881678b06/e3ae881678b06.png)
![Alt](https://s.imgkb.xyz/abcdocker/2023/03/26/5e4480633b783/5e4480633b783.png)
</details>

## <div align="center">模型</div>

<details open><summary>目标检测</summary>

| 模型 | 尺寸<br><sup>（像素） | mAP<sup>val<br>50-95 | 推理速度<br><sup>CPU(i7-8565U) ONNX<br>(ms) | 参数量<br><sup>(K) |
| --------- | ------- | -------- | ------------| ---------- |
| [RedScarf](/data/best.pt) | 640*480   | 55.62    | 95.84      | 0.81  

</details>

<details open><summary>训练</summary>

本项目通过[爬虫](GetImage.py)，[拍摄](Picture.py)两种方式进行数据采集

拍摄过程中共进行了5次数据迭代，第一代由于数据单一，且验证集过小失败。第二代增加了网络数据，不过手动的下载显得慢二累赘。故，第三代采用爬虫，但是爬虫数据大多不符合要求数据量不够打。第四代增加了600张自己拍摄的照片，但是服装，方式单一，没有很好的效果。在第五代，增加了各种复杂环境进行识别，在134次epoch后，mAP50-95达到了55.62，mAP50达到了89.61。实现了较好的识别，能适应复杂情况
![Alt](https://s.imgkb.xyz/abcdocker/2023/03/26/f80ba3ad0f32e/f80ba3ad0f32e.png)
![Alt](https://s.imgkb.xyz/abcdocker/2023/03/26/03ad0ac03c0a9/03ad0ac03c0a9.png)
![Alt](https://s.imgkb.xyz/abcdocker/2023/03/26/b06c9185498d8/b06c9185498d8.png)
![Alt](https://s.imgkb.xyz/abcdocker/2023/03/26/1558199e7e708/1558199e7e708.png)
![Alt](https://s.imgkb.xyz/abcdocker/2023/03/26/dbdc621009c47/dbdc621009c47.png)
具体数据在[此](/data/data.zip)

最重要的是，本项目并没有采用传统的手动标注思想，而是采用了半监督学习化的自动标注，大大的节省了人力，我仅标注了50张图片，它即可标注800张，颇为高效。

</details>

## <div align="center">不足</div>

本项目由于时间原因，没有做UI，没有增加自动识别功能，数据集也不够大，mAP没有达到极限。
并且本项目没有适配大多数机型，没有打包exe。
在后续的学习中我会不断更近此项目，如有疑问请发issue


-----------------
# by 傅雷中学王新语