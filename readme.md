<div align="center">
  <p>
    <a href="https://github.com/Vicwxy9/RedScarf" target="_blank">
      <img width="100%" src="https://i.328888.xyz/2023/03/29/ik78i3.png"></a>
  </p>
</div>

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
效果会在摄像头上标出人和红领巾的位置，若未戴红领巾则为黄色，若带了则为绿色
具体如下(所有图片均使用图床，如果需要请到data/images寻找)：

![ikxYOt.png](https://i.328888.xyz/2023/03/29/ikxYOt.png) | ![ikxQZX.png](https://i.328888.xyz/2023/03/29/ikxQZX.png) 
--- | ---
![ikxqeJ.png](https://i.328888.xyz/2023/03/29/ikxqeJ.png) | ![ikxuac.png](https://i.328888.xyz/2023/03/29/ikxuac.png)
![ik7i0A.png](https://i.328888.xyz/2023/03/29/ik7i0A.png) | ![ik7kaa.png](https://i.328888.xyz/2023/03/29/ik7kaa.png)
![ik7D5b.png](https://i.328888.xyz/2023/03/29/ik7D5b.png) | ![ik7Ard.png](https://i.328888.xyz/2023/03/29/ik7Ard.png)
![ik7nZq.png](https://i.328888.xyz/2023/03/29/ik7nZq.png) | ![ik7tOz.png](https://i.328888.xyz/2023/03/29/ik7tOz.png)
![ik7Wzw.png](https://i.328888.xyz/2023/03/29/ik7Wzw.png) | ![ik7C0x.png](https://i.328888.xyz/2023/03/29/ik7C0x.png)
</details>

## <div align="center">说明</div>

<details open><summary>项目架构</summary>

```bash
  data
    |- images (markdown图片)
    |- datasets.zip (数据集)
    |- models.zip (原始未经优化 pt onnx 模型)
  detector
    |-persondetector.py (人体检测封装函数库)
    |-redscarfdetector.py (红领巾检测封装函数库)
  models
    |-redscarf_openvino_model (红领巾优化后OpenVINO 模型)
    |-yolov8n_openvino_model (人体检测优化后OpenVINO 模型)
  tools
    |-ChangeToOpenVINO.py (模型转换)
    |-GetImage.py (百度图片爬虫)
    |-Json2txt.py (数据集转换)
    |-Picture.py (摄像头数据采集)
  Log.py (日志文件)
  Main.py (主程序)
  Train.ipynb (在Colab上的模型训练文件及过程)
```

</details>

<details open><summary>项目设计方案</summary>

本程序首先通过数据采集，和训练的方式得到了一个模型，可以较好地检测红领巾

随机此模型性能较差，单单一个模型既需要 150ms 的推理时间，故我通过OpenVINO的方式优化了模型，使得它能达到 50ms 的推理时间，大大减少了性能损耗

同时我亦使用了官方预训练模型，进行人体检测，只要红领巾在此人体范围之内，及判断改人戴了红领巾（此方法有缺点，便是红领巾拿在手上会被误检成戴了红领巾）

最后，通过cv2的绘图工具进行绘图，得到结果

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
![ik7lXk.png](https://i.328888.xyz/2023/03/29/ik7lXk.png)
![ik7wJL.png](https://i.328888.xyz/2023/03/29/ik7wJL.png)
![ik7HDp.png](https://i.328888.xyz/2023/03/29/ik7HDp.png)
![ik7O3U.png](https://i.328888.xyz/2023/03/29/ik7O3U.png)
![ik7b5v.png](https://i.328888.xyz/2023/03/29/ik7b5v.png)
具体数据在[此](/data/data.zip)

最重要的是，本项目并没有采用传统的手动标注思想，而是采用了半监督学习化的自动标注，大大的节省了人力，我仅标注了50张图片，它即可标注800张，颇为高效。

</details>



## <div align="center">不足</div>

1.本项目由于时间原因，没有做UI。

2.训练数据集不够完善，导致mAP没有达到极限。

3.本项目没有适配大多数机型（OpenVINO 有局限性），没有打包exe。

在后续的学习中我会不断更近此项目，如有疑问请发issue


-----------------
# by 傅雷中学王新语