# RESTful API接口设计标准及规范

## RESTful发展背景及简介
网络应用程序，分为前端和后端两个部分。当前的发展趋势，就是前端设备层出不穷（手机、平板、桌面电脑、其他专用设备…）。因此，必须有一种统一的机制，方便不同的前端设备与后端进行通信。这导致API构架的流行，甚至出现"APIFirst"的设计思想。RESTful API是目前比较成熟的一套互联网应用程序的API设计理论。

REST（Representational State Transfer）表述性状态转换，REST指的是一组架构约束条件和原则。 如果一个架构符合REST的约束条件和原则，我们就称它为RESTful架构。REST本身并没有创造新的技术、组件或服务，而隐藏在RESTful背后的理念就是使用Web的现有特征和能力， 更好地使用现有Web标准中的一些准则和约束。虽然REST本身受Web技术的影响很深， 但是理论上REST架构风格并不是绑定在HTTP上，只不过目前HTTP是唯一与REST相关的实例。

## 1. URI
URI 表示资源，资源一般对应服务器端领域模型中的实体类。

### URI规范

- 不用大写
- 用中杠-不用下杠_
- 参数列表要encode
- URI中的名词表示资源集合，使用**复数形式**

### 资源集合 vs 单个资源

URI表示资源的两种方式：资源集合、单个资源。

资源集合：

```
zoos //所有动物园
/zoos/1/animals //id为1的动物园中的所有动物
12
```

单个资源：

```
/zoos/1 //id为1的动物园
/zoos/1;2;3 //id为1，2，3的动物园
```

### 避免层级过深的URI
- /在url中表达层级，用于按实体关联关系进行对象导航，**一般根据id导航**

- 过深的导航容易导致url膨胀，不易维护，如 `GET /zoos/1/areas/3/animals/4`

- 尽量使用查询参数代替路径中的实体导航，如 `GET /animals?zoo=1&area=3`

### 对Composite资源的访问
**服务器端的组合实体必须在uri中通过父实体的id导航访问。**

组合实体不是first-class的实体，它的生命周期完全依赖父实体，无法独立存在，在实现上通常是对数据库表中某些列的抽象，不直接对应表，也无id。一个常见的例子是 User — Address，Address是对User表中zipCode/country/city三个字段的简单抽象，无法独立于User存在。必须通过User索引到Address：GET /user/1/addresses

## 2. Request
### HTTP方法
通过标准HTTP方法对资源CRUD：

- GET：查询

	```
	GET /zoos
	GET /zoos/1
	GET /zoos/1/employees
	```

- POST：创建单个资源。POST一般向“资源集合”型uri发起

	```
	POST /animals  //新增动物
	POST /zoos/1/employees //为id为1的动物园雇佣员工
	```

- PUT：更新单个资源（**全量**），客户端提供完整的更新后的资源。与之对应的是 PATCH，PATCH 负责**部分更新**，客户端提供要更新的那些字段。PUT/PATCH一般向“**单个资源**”型uri发起

  ```
  PUT /animals/1
  PUT /zoos/1
  ```

- DELETE：删除

	```
	DELETE /zoos/1/employees/2
	DELETE /zoos/1/employees/2;4;5
	DELETE /zoos/1/animals  //删除id为1的动物园内的所有动物
	```

HEAD / OPTION 用的不多，就不多解释了。

### 安全性和幂等性

1. 安全性：不会改变资源状态，可以理解为只读的；
2. 幂等性：执行1次和执行N次，对资源状态改变的效果是等价的。

|        | 安全性 | 幂等性 |
| ------ | ------ | ------ |
| GET    | √      | √      |
| POST   | ×      | ×      |
| PUT    | ×      | √      |
| DELETE | ×      | √      |

安全性和幂等性均不保证反复请求能拿到相同的response。以 DELETE 为例，第一次DELETE返回200表示删除成功，第二次返回404提示资源不存在，这是允许的。

### 复杂查询

查询可以捎带以下参数：

|          | 示例                       | 备注                                         |
| -------- | -------------------------- | -------------------------------------------- |
| 过滤条件 | `?type=1&age=16`           | 允许一定的uri冗余，如`/zoos/1`与`/zoos?id=1` |
| 排序     | `?sort=age,desc`           |                                              |
| 投影     | `?whitelist=id,name,email` |                                              |
| 分页     | `?limit=10&offset=3`       |                                              |

## 3. Bookmarker

经常使用的、复杂的查询标签化，降低维护成本。

如：

```
GET /trades?status=closed&sort=created,desc
```

快捷方式：

```
GET /trades#recently-closed
或者
GET /trades/recently-closed
```

## 4. Format

只用以下常见的3种body format：

- Content-Type: application/json

  ```http
  POST /v1/animal HTTP/1.1
  Host: api.example.org
  Accept: application/json
  Content-Type: application/json
  Content-Length: 24
   
  {   
    "name": "Gir",
    "animalType": "12"
  }
  ```

- Content-Type: application/x-www-form-urlencoded (浏览器POST表单用的格式)

  ```http
  POST /login HTTP/1.1
  Host: example.com
  Content-Length: 31
  Accept: text/html
  Content-Type: application/x-www-form-urlencoded
   
  username=root&password=Zion0101
  ```

- Content-Type: multipart/form-data; boundary=—-RANDOM_jDMUxq4Ot5 (表单有文件上传时的格式)

  ## Content Negotiation

  资源可以有多种表示方式，如json、xml、pdf、excel等等，客户端可以指定自己期望的格式，通常有两种方式：

  1. http header Accept：

  ```
  Accept:application/xml;q=0.6,application/atom+xml;q=1.0
  ```

  q为各项格式的偏好程度

  2. url中加文件后缀：/zoo/1.json

## 5. Response

1. 不要包装： 
   response 的 body 直接就是数据，不要做多余的包装。错误示例：

## 6. Response

1. 不要包装： 
   response 的 body 直接就是数据，不要做多余的包装。错误示例：

   ```json
    {
    	"success": true,
       "data": {
           "id": 1,
           "name": "xiaotuan"
       }
    }
   ```

2. 各HTTP方法成功处理后的数据格式：

   | method    | response 格式  |
   | --------- | -------------- |
   | GET       | 单个对象、集合 |
   | POST      | 新增成功的对象 |
   | PUT/PATCH | 更新成功的对象 |
   | DELETE    | 空             |

3. json格式的约定：

   1. 时间用长整形(毫秒数)，客户端自己按需解析
   2. 不传`null`字段

### 分页response

```json
{
    "paging":{
        "limit":10,"offset":0,"total":729
    },
    "data":[{},{},{}...]
}
```

## 7. 错误处理

1. 发生了错误不要给2xx响应，客户端可能会缓存成功的http请求；

2. 正确设置http状态码，不要自定义；

3. Response body 提供 

   1) 错误的代码（日志/问题追查）

   2) 错误的描述文本（展示给用户）

对第三点的实现稍微多说一点：

Java 服务器端一般用异常表示 RESTful API 的错误。API 可能抛出两类异常：**业务异常**和**非业务异常**。

业务异常由自己的业务代码抛出，表示一个用例的前置条件不满足、业务规则冲突等，比如参数校验不通过、权限校验失败。

非业务类异常表示不在预期内的问题，通常由类库、框架抛出，或由于自己的代码逻辑错误导致，比如数据库连接失败、空指针异常、除0错误等等。

业务类异常必须提供2种信息：

	1. 如果抛出该类异常，HTTP 响应状态码应该设成什么；
 	2. 异常的文本描述；

在Controller层使用统一的异常拦截器：

1. 设置 HTTP 响应状态码：对业务类异常，用它指定的 HTTP code；对非业务类异常，统一500；
2. Response Body 的错误码：异常类名
3. Response Body 的错误描述：对业务类异常，用它指定的错误文本；对非业务类异常，线上可以统一文案如“服务器端错误，请稍后再试”，开发或测试环境中用异常的 stacktrace，服务器端提供该行为的开关。

常用的http状态码及使用场景：

| 状态码                    | 使用场景                                                     |
| ------------------------- | ------------------------------------------------------------ |
| 400 bad request           | 常用在参数校验                                               |
| 401 unauthorized          | 未经验证的用户，常见于未登录。如果经过验证后依然没权限，应该 403（即 authentication 和 authorization 的区别）。 |
| 403 forbidden             | 无权限                                                       |
| 404 not found             | 资源不存在                                                   |
| 500 internal server error | 非业务类异常                                                 |
| 503 service unavaliable   | 由容器抛出，自己的代码不要抛这个异常                         |

## 8. 服务型资源
除了资源简单的CRUD，服务器端经常还会提供其他服务，这些服务无法直接用上面提到的URI映射。如：

按关键字搜索；
1.计算地球上两点间的距离；
2.批量向用户推送消息
3.可以把这些服务看成资源，计算的结果是资源的 presentation，按服务属性选择合适的HTTP方法。

例：

```
GET /search?q=filter?category=file  搜索
GET /distance-calc?lats=47.480&lngs=-122.389&late=37.108&lnge=-122.448
POST /batch-publish-msg

[{"from":0,"to":1,"text":"abc"},{},{}...]
```

## 9. 异步任务

对耗时的异步任务，服务器端接受客户端传递的参数后，应返回创建成功的任务资源，其中包含了任务的执行状态。客户端可以轮训该任务获得最新的执行进度。

```
提交任务：
POST /batch-publish-msg
[{"from":0,"to":1,"text":"abc"},{},{}...]
 
返回：
{"taskId":3,"createBy":"Anonymous","status":"running"}
 
GET /task/3
{"taskId":3,"createBy":"Anonymous","status":"success"}
```

如果任务的执行状态包括较多信息，可以把“执行状态”抽象成组合资源，客户端查询该状态资源了解任务的执行情况。

```
提交任务：
POST /batch-publish-msg
[{"from":0,"to":1,"text":"abc"},{},{}...]
 
返回：
{"taskId":3,"createBy":"Anonymous"}
 
GET /task/3/status
{"progress":"50%","total":18,"success":8,"fail":1}
```

## 10. API的演进
版本
常见的三种方式：

1.在uri中放版本信息：GET /v1/users/1
2.Accept Header：Accept: application/json+v1
3.自定义 Header：X-Api-Version: 1
用第一种，虽然没有那么优雅，但最明显最方便。

URI失效
随着系统发展，总有一些API失效或者迁移，对失效的API，返回404 not found 或 410 gone；对迁移的API，返回 301 重定向。
