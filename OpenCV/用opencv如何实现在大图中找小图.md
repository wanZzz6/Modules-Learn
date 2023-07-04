# 用opencv如何实现在大图中找小图



> 注：以下内容来自ChatGPT



以java代码为例：

```java
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Point;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Mat;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;
```



在 OpenCV 中，`Imgproc.matchTemplate` 方法用于在图像中搜索模板。它的语法如下：

```java
public static void matchTemplate(Mat image, Mat templ, Mat result, int method)
```

其中，image 是输入图像，templ 是模板图像，result 是输出结果图像，method 是匹配方法。常用的匹配方法有：

- `Imgproc.TM_SQDIFF`：平方差匹配法，计算图像和模板之间的像素差的平方和，值越小表示匹配度越高。
- `Imgproc.TM_SQDIFF_NORMED`：归一化平方差匹配法，计算图像和模板之间的像素差的平方和，并将结果归一化到0-1之间，值越小表示匹配度越高。
- `Imgproc.TM_CCORR`：相关匹配法，计算图像和模板之间的像素点乘积和，值越大表示匹配度越高。
- `Imgproc.TM_CCORR_NORMED`：归一化相关匹配法，计算图像和模板之间的像素点乘积和，并将结果归一化到0-1之间，值越大表示匹配度越高。
- `Imgproc.TM_CCOEFF`：相关系数匹配法，计算图像和模板之间的相关系数，值越大表示匹配度越高。
- `Imgproc.TM_CCOEFF_NORMED`：归一化相关系数匹配法，计算图像和模板之间的相关系数，并将结果归一化到0-1之间，值越大表示匹配度越高。

不同的匹配方法适用于不同的场景，需要根据具体情况选择合适的方法。例如，平方差匹配法适用于模板和图像的亮度差异较大的情况，相关匹配法适用于模板和图像的亮度差异较小的情况。归一化匹配法可以消除亮度和对比度的影响，但计算量较大。



使用方法如下：

```java
Mat image = Imgcodecs.imread("path/to/image");
Mat templ = Imgcodecs.imread("path/to/template");
Mat result = new Mat();
int matchMethod = Imgproc.TM_CCOEFF_NORMED;
Imgproc.matchTemplate(image, templ, result, matchMethod);
```

其中，image 和 templ 是输入的图像和模板图像，result 是输出的结果图像，`Imgproc.TM_CCOEFF_NORMED` 是匹配方法。匹配结果保存在 result 中。



后续可以使用 `Core.minMaxLoc` 方法找到最大匹配位置，用法如下：

```java
Core.MinMaxLocResult mmr = Core.minMaxLoc(result);
```

其中，result 是匹配结果图像。方法返回一个 `Core.MinMaxLocResult` 对象，包含匹配结果的最大值、最小值、最大值位置和最小值位置。

在代码中判断最佳匹配位置的方式取决于使用的匹配方法。

- 对于平方差匹配法（TM_SQDIFF）和归一化平方差匹配法（TM_SQDIFF_NORMED），可以使用 `mmr.minVal` 判断最佳匹配位置，如果 mmr.minVal 的值越小，则表示匹配度越高，最佳匹配位置就是 `mmr.minLoc`。
- 对于相关匹配法（TM_CCORR）和归一化相关匹配法（TM_CCORR_NORMED），可以使用 `mmr.maxVal` 判断最佳匹配位置，如果 `mmr.maxVal` 的值越大，则表示匹配度越高，最佳匹配位置就是 `mmr.maxLoc`。
- 对于相关系数匹配法（TM_CCOEFF）和归一化相关系数匹配法（TM_CCOEFF_NORMED），也可以使用 `mmr.maxVal` 判断最佳匹配位置，如果 `mmr.maxVal` 的值越大，则表示匹配度越高，最佳匹配位置就是 `mmr.maxLoc`。

```java
// 获取最佳匹配位置和相似度
Core.MinMaxLocResult mmr = Core.minMaxLoc(result);
Point matchLoc;
double value;

if (matchMethod == Imgproc.TM_SQDIFF || matchMethod == Imgproc.TM_SQDIFF_NORMED) {
  matchLoc = mmr.minLoc;
  value = -mmr.minVal;
} else {
  matchLoc = mmr.maxLoc;
  value = mmr.maxVal;
}
```

其中，matchLoc 是最大匹配位置。

注意，最大匹配位置是匹配结果图像中的位置，需要根据模板图像的大小和匹配结果图像的大小计算出在原始图像中的位置。例如：

```java
Rect rect = new Rect(matchLoc, new Size(templ.cols(), templ.rows()));
Imgproc.rectangle(image, rect.tl(), rect.br(), new Scalar(0, 0, 255), 2);
```

其中，rect 是最大匹配位置在原始图像中的矩形区域，可以使用 `Imgproc.rectangle` 方法在原始图像中绘制出该区域。