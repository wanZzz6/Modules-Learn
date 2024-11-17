## 一、问题原因

常见于前后端不分离的web项目中，因为该类型的项目通常没有集成类似于webpack之类的打包工具，导致html、js、css之类的静态文件访问链接长久不变，而浏览器为了提高加载速度和减少服务器负载，通常会对静态资源如JavaScript文件、CSS文件等进行缓存。当用户访问一个页面时，如果浏览器发现它已经缓存了该页面引用的某个资源（例如一个JS文件），那么它就会直接从本地缓存中读取这个资源而不是向服务器发送新的请求。这种行为可以显著加快页面的加载速度，但是也会带来一个问题，即当这些静态资源在服务器端更新后，浏览器可能仍然在使用旧的缓存文件。

## 二、解决方案

### 1. 用户自行清理浏览器缓存

在页面上按`Ctrl+Shift+R` 硬刷新页面。

缺点：不是所有用户（老板们）都知道如何清理缓存，且用户使用中不知道页面是否有新版本发布，总不能每次更新页面后都得通知用户进行清理缓存吧。

### 2. 使用`<meta>`标签设置缓存控制

虽然`<meta>`标签可以影响浏览器对当前HTML文档的缓存行为，但它对嵌入资源的缓存控制能力有限。`<meta>`标签主要用于**控制当前HTML文档本身的缓存策略，而不是其内部引用的所有资源**（如JavaScript文件、CSS文件、图片等）。

#### 2.1 禁止缓存

如果你想完全禁止浏览器缓存某个html页面，可以使用以下`<meta>`标签：

```html
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
```

- `Cache-Control: no-cache, no-store, must-revalidate`：指示浏览器不要缓存当前html页面，每次请求时都要重新验证资源。
- `Pragma: no-cache`：用于兼容HTTP/1.0的缓存控制。
- `Expires: 0`：设置资源的过期时间为过去的一个时间点，强制浏览器重新请求资源。

#### 2.2 设置缓存时间

如果你想设置页面的缓存时间，可以使用以下`<meta>`标签：

```html
<meta http-equiv="Cache-Control" content="max-age=3600">
```

- `Cache-Control: max-age=3600`：指示浏览器缓存页面1小时（3600秒）。

#### 2.3 限制和注意事项

- **有限的控制力**：`<meta>`标签的缓存控制能力有限，主要影响客户端浏览器的行为。服务器端的缓存控制（如通过HTTP响应头）更为强大和可靠。
- **兼容性**：虽然大多数现代浏览器都支持`<meta>`标签的缓存控制，但某些老旧浏览器可能不支持或表现不一致。
- **优先级**：如果服务器响应头中已经设置了缓存控制指令，`<meta>`标签可能会被忽略。**服务器响应头的优先级高于`<meta>`标签。**

> 尽管`<meta>`标签可以用来控制缓存策略，但更推荐的做法是在服务器端通过HTTP响应头来设置缓存控制。这样可以确保缓存策略在整个请求链路中一致且有效。

### 3. 为js和css文件添加版本号

在html文件中引用js、css、jpg等静态资源时，可以在URL后面加上一个版本号或者时间戳作为查询参数。例如:

```html
<link rel="stylesheet" type="text/css" href="${pageContext.request.contextPath}/static/css/style.css?v=20241027160111">
```

每次修改静态文件后，需同时更新引用地址中的版本号或时间戳，这样浏览器会认为这是一个新的资源而不会使用缓存，如果文件地址和参数都没变，则继续走浏览器缓存。



但是一个html文件里面有好多 css 和 js链接，每次发布都得手动添加和修改太费劲了，这就需要根据自己项目的打包方式借助打包件来实现，如果没有那就自己造轮子(其实就是一个正则匹配和替换功能)。

java项目中可用的插件:

#### 3.1 maven-antrun-plugin 插件

`maven-antrun-plugin` 可以在构建过程中执行Ant任务，这非常适合用于文件操作。

pom文件添加:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-antrun-plugin</artifactId>
            <version>3.0.0</version>
            <executions>
                <execution>
                    <phase>prepare-package</phase>
                    <goals>
                        <goal>run</goal>
                    </goals>
                    <configuration>
                        <target>
                            <property name="timestamp" value="${maven.build.timestamp}"/>
                            <replaceregexp match="(src|href)=\"([^\"]+)\.(js|css|png|jpg|jpeg|gif|svg)\""
                                          replace="\1=\"\2.\3?v=${timestamp}\""
                                          flags="g">
                                <fileset dir="src/main/resources">
                                    <include name="**/*.html"/>
                                </fileset>
                            </replaceregexp>
                        </target>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

#### 3.2 maven-replacer-plugin 插件

配置简单，专注于文件内容替换

注意此插件只会在生成 war 包源码时生效.

```xml
<properties>
        <java.version>1.8</java.version>
        <maven.build.timestamp.format>yyyyMMddHHmmss</maven.build.timestamp.format>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>com.google.code.maven-replacer-plugin</groupId>
            <artifactId>replacer</artifactId>
            <version>1.5.3</version>
            <executions>
                <execution>
                    <phase>prepare-package</phase>
                    <goals>
                        <goal>replace</goal>
                    </goals>
                    <configuration>
                        <basedir>src/main/resources</basedir>
                        <includes>
                            <include>**/*.html</include>
                            <include>**/*.jsp</include>
                        </includes>
                        <token>(src|href)=["']([^"]+)\.(js|css|png|jpg|jpeg|gif|svg)["']</token>
                        <value>$1="$2.$3?v=${maven.build.timestamp}"</value>
                        <regexFlags>
                            <regexFlag>MULTILINE</regexFlag>
                            <regexFlag>DOTALL</regexFlag>
                        </regexFlags>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```





> 参考:
>
> - https://www.codeleading.com/article/9999424424/
> - https://blog.csdn.net/liugang594/article/details/84615054
> - maven-resources-plugin

### 4. 使用ETag

ETag（Entity Tag）是一种用于HTTP缓存验证的机制，可以帮助浏览器确定服务器上的资源是否已经更改。ETag 是一个唯一标识符，每次资源发生变化时，服务器都会生成一个新的ETag值。浏览器在请求资源时会在请求头在带上上次请求时返回的ETag值（通过 `If-None-Match` 头），服务器根据这个值判断资源是否已更改。如果资源没有变化，服务器会返回304 Not Modified状态码，告知浏览器继续使用缓存；如果资源已更改，则返回200 OK状态码及新的资源内容。

#### 4.1 工作原理

**首次请求**:

假设有一个JavaScript文件`app.js`，服务器第一次返回该文件时，响应头如下：

```http
HTTP/1.1 200 OK
Content-Type: application/javascript
ETag: "1234567890abcdef"
```

浏览器缓存该文件及其ETag。

**后续请求**:

当浏览器再次请求该文件时，会在请求头中包含`If-None-Match`字段，值为上次请求时返回的ETag，请求头如下：

```http
GET /app.js HTTP/1.1
Host: yourdomain.com
If-None-Match: "1234567890abcdef"
```

**服务器响应**:

服务器接收到请求后，会检查资源的当前ETag是否与请求头中的`If-None-Match`值匹配。

- 如果匹配，即服务器上的`app.js`文件没有变化，服务器返回`304 Not Modified`状态码，浏览器继续使用缓存的资源。响应头如下：

  ```http
  HTTP/1.1 304 Not Modified
  ```

- 如果不匹配，即服务器上的`app.js`文件已更改，服务器返回200 OK状态码及新的资源内容，并附带新的ETag值。响应头如下：

  ```http
  HTTP/1.1 200 OK
  Content-Type: application/javascript
  ETag: "0987654321abcdef"
  ```

**总结**：

通过在服务器端配置ETag，可以有效减少不必要的资源传输，提高网站性能。ETag的使用相对简单，只需要在服务器配置文件中启用即可，浏览器会自动处理ETag相关的缓存验证逻辑。

常见的服务器中配置HTTP缓存控制头的方法如下。

#### 4.2 Nginx配置

在Nginx中，ETag默认是启用的。你可以在配置文件中进一步调整ETag的生成方式。以下是一个示例：

```nginx
server {
  listen 80;
  server_name yourdomain.com;

  location / {
    root /path/to/your/web/root;
    index index.html index.htm;

    # 启用ETag
    etag on;
    if_modified_since exact;
  }
}
```

- `etag on;`：启用ETag。
- `if_modified_since exact;`：指定如何处理`If-Modified-Since`头。`exact`表示使用精确的时间匹配。

#### 4.3 Tomcat 配置

在Tomcat中，ETag默认是启用的。你可以在`web.xml`中配置ETag。以下是一个示例：

```xml
<filter>
  <filter-name>ExpiresFilter</filter-name>
  <filter-class>org.apache.catalina.filters.ExpiresFilter</filter-class>
  <init-param>
    <param-name>ExpiresByType application/javascript</param-name>
    <param-value>access plus 1 day</param-value>
  </init-param>
  <init-param>
    <param-name>ExpiresByType text/css</param-name>
    <param-value>access plus 1 day</param-value>
  </init-param>
  <init-param>
    <param-name>EnableCacheControl</param-name>
    <param-value>true</param-value>
  </init-param>
  <init-param>
    <param-name>EnableETag</param-name>
    <param-value>true</param-value>
  </init-param>
</filter>

<filter-mapping>
  <filter-name>ExpiresFilter</filter-name>
  <url-pattern>/*</url-pattern>
</filter-mapping>
```

- `EnableETag true;`：启用ETag。

### 5. 使用Cache-Control

**作用**：

- **缓存策略**：`Cache-Control` 头用于控制浏览器和其他中间缓存（如CDN）如何缓存资源。
- **缓存时间**：通过设置 `max-age` 等指令，可以指定资源的缓存时间。

**常用指令**：

- `public`：指示响应可以被任何缓存存储。
- `private`：指示响应只能被单个用户的缓存存储，不能被共享缓存（如CDN）存储。
- `no-cache`：指示缓存必须在使用前先验证资源的新鲜度。
- `no-store`：指示缓存不应存储该响应的任何部分。
- `max-age=<seconds>`：指示资源的最大缓存时间，单位为秒。
- `s-maxage=<seconds>`：类似于 `max-age`，但仅适用于共享缓存（如CDN）。

#### 5.1 工作原理

**首次请求**:

浏览器请求资源，服务器返回资源内容，并在响应头中包含 `Cache-Control`。

```http
HTTP/1.1 200 OK
Content-Type: application/javascript
Cache-Control: max-age=86400, public
```

**后续请求:**

- 如果缓存时间未过期，浏览器直接使用缓存的资源，不会发送新的请求。
- 如果缓存时间已过期，浏览器会发送带有 `If-Modified-Since` 或 `If-None-Match` 头的条件请求，服务器根据这些头判断资源是否已更改。

#### 5.2 与Etag的区别

1. **目的**：
   - **ETag**：主要用于缓存验证，确保浏览器使用的资源是最新的。
   - **Cache-Control**：主要用于控制缓存策略，指定资源的缓存时间和范围。
2. **机制**：
   - **ETag**：通过唯一标识符（ETag）进行缓存验证，适用于资源内容频繁变化的场景。
   - **Cache-Control**：通过设置缓存时间（`max-age`）和缓存策略（`public`、`private`等）来控制缓存行为，适用于资源内容相对稳定的场景。
3. **使用场景**：
   - **ETag**：**适用于资源内容频繁更新**，需要精确验证资源是否已更改的场景。
   - **Cache-Control**：**适用于资源内容相对稳定**，希望长时间缓存的场景，或者需要控制缓存范围和行为的场景。

#### 5.3 Nginx配置

```nginx
server {
  listen 80;
  server_name yourdomain.com;

  location / {
    root /path/to/your/web/root;
    index index.html index.htm;

    # 设置JavaScript文件的缓存时间为1天
    location ~* \.(js)$ {
      expires 1d;
      add_header Cache-Control "public, max-age=86400";
    }

    # 设置其他静态文件的缓存时间为7天
    location ~* \.(css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
      expires 7d;
      add_header Cache-Control "public, max-age=604800";
    }

    # 防止某些敏感信息被缓存
    location ~* \.(php|html|htm)$ {
      add_header Cache-Control "no-store, no-cache, must-revalidate, max-age=0";
    }
  }
}
```

#### 5.4 Tomcat 配置

在Tomcat中，你可以通过配置`web.xml`文件来设置缓存控制头。下面是一个例子：

```xml
<filter>
  <filter-name>ExpiresFilter</filter-name>
  <filter-class>org.apache.catalina.filters.ExpiresFilter</filter-class>
  <init-param>
    <param-name>ExpiresByType application/javascript</param-name>
    <param-value>access plus 1 day</param-value>
  </init-param>
  <init-param>
    <param-name>ExpiresByType text/css</param-name>
    <param-value>access plus 1 week</param-value>
  </init-param>
  <init-param>
    <param-name>ExpiresByType image/jpeg</param-name>
    <param-value>access plus 1 month</param-value>
  </init-param>
  <init-param>
    <param-name>EnableCacheControl</param-name>
    <param-value>true</param-value>
  </init-param>
</filter>

<filter-mapping>
  <filter-name>ExpiresFilter</filter-name>
  <url-pattern>/*</url-pattern>
</filter-mapping>
```

以上配置为不同类型的文件设置了不同的缓存时间。`ExpiresFilter`是Tomcat提供的一个过滤器，用于设置HTTP响应头中的`Expires`字段和`Cache-Control`字段。

### 6. Etag结合Cache-Control

在实际应用中，通常会结合使用 `ETag` 和 `Cache-Control` 来达到最佳的缓存效果。例如：

```http
HTTP/1.1 200 OK
Content-Type: application/javascript
Cache-Control: max-age=86400, public
ETag: "1234567890abcdef"
```

这样，资源在缓存时间内可以直接使用缓存，超过缓存时间后，浏览器会通过ETag进行缓存验证，确保资源是最新的。

### 7. 其他缓存方案

#### 7.1 利用HTML5的manifest文件

HTML5提供了一种名为Application Cache的功能，允许开发者定义一个manifest文件来指定哪些资源应该被缓存，以及缓存的策略。不过需要注意的是，由于Application Cache存在一些设计上的缺陷和兼容性问题，现在已经被Service Worker所取代。

#### 7.2 Service Worker

在js文件中由前端开发者完全、自由控制浏览器端的请求策略.

Service Worker是一种可以在浏览器后台运行的脚本，它可以拦截网络请求，并根据预定义的逻辑决定是从网络获取资源还是从缓存中提供资源。Service Worker为现代Web应用提供了更强大的离线支持和缓存管理能力, 合理使用Service Worker，可以显著提升用户的体验和应用的整体性能。

**请求拦截**: Service Worker 可以拦截和处理所有的网络请求，不管是否静态资源, 允许你自定义请求的处理逻辑，如重定向请求、修改请求头等.

**灵活的缓存策略**: 可以根据应用需求实现各种缓存策略，如缓存优先、网络优先、网络失败回退到缓存等。

**无缝体验**：即使在网络不稳定或完全断开的情况下，用户也能继续使用应用，提高了应用的可靠性和用户体验。

**后台同步**：Service Worker 可以在后台同步数据，确保应用的数据始终是最新的。

**HTTPS**：Service Worker 只能在HTTPS环境下注册，确保了通信的安全性，防止中间人攻击。

**兼容性**：Service Worker 是渐进增强的技术，不会影响不支持Service Worker的浏览器的正常运行。

## 三、总结

- **\<meta\> 标签**: 简单,无需服务端配置;适用于html内容少的小型项目或者单页面应用.
- **为静态文件链接添加版本号**: 无需服务端配置; 但需要Maven、Webpack等打包插件配合.
- **ETag**: 对缓存行为进行精细控制,可高效利用浏览器缓存, 减少带宽压力; 仅服务端配置,开发者无需过多干预.
- **Cache-Control**: 精细控制缓存策略，如设置缓存时间、禁止缓存等; 仅服务端配置; 适用于跨域资源的缓存控制.
- **Service Worker**：适用于需要离线支持和实现复杂缓存策略的现代Web应用，提供更好的用户体验。

