# AutoX-对象、图片资源懒加载+Storage持久化

## 一、使用场景

需要懒加载的场景有很多，我最开始是需要懒加载功能是在编写一个游戏自动化脚本时，需要事先检测某个物品的坐标，才能进行后续的点击操作，该物品在页面中的位置是固定的，我如果确定了其坐标点[x, y]，那么以后就可以一直使用。但是考虑到脚本要在不同分辨率的机型上适配，所以这个物品的坐标我不能写死，只能通过找图、找色手段确定后，将其保存到本地缓存中，后续使用时直接加载缓存即可。在同一脚本中，这种先确定物品固定坐标再操作的情况有很多，因此我需要一个能统一处理坐标检测和持久化的方法。

另外，在游戏脚本中通常会涉及大量的找图需求，如果在其中的每个方法中单独加载图片、释放图片资源会使得代码重复部分较多，不够优雅。此时就需要设计一套流程，能够对图片资源按需加载、统一释放资源，并且还可以针对不同分辨率的机型在图片加载后进行统一缩放处理。

## 二、代码实现

针对我在实际中遇到的以上这两种需求，结合 AutoX 提供的 API 和 Rhino 引擎特性实现了以下懒加载方法：

- `createLazyObject(obj[,saveKey])`: 能够对普通对象属性值进行动态获取和Storage持久化，下次启动时可直接加载Storage中的缓存；清理缓存后可重新触发懒加载方法。
- `createImageLazyObject(imagePathMap)`：对前一方法的进一步封装了，然后就能像 `resource.图片1` 访问对象属性的方式触发图片加载，再配合退出事件 `events.on('exit', xxx)` 完成对资源的统一释放。



（后文有测试用例，可直接测试使用）

```js
const isFunction = (val) => typeof val === 'function';

/**
 * 创建一个懒加载对象。动态获取到的属性值可保存在内存中，也可持久化到Storage中，下次运行时从Storage中直接加载
 * @param {object} obj
 * @param {string|null} saveKey 为空则只在内存中进行懒加载；如果不为空，表示此对象以saveKey为键存储到Storage。
 */
function createLazyObject(obj, saveKey) {
  let lazyObject = {};
  let cacheData = saveKey ? getCache(saveKey, {}) : {};

  for (let key in obj) {
    if (!obj.hasOwnProperty(key)) {
      continue;
    }

    // 静态值不做处理
    if (!isFunction(obj[key])) {
      lazyObject[key] = obj[key];
      continue;
    }
    // 动态加载方法，且有缓存值
    if (cacheData[key] !== undefined) {
      lazyObject[key] = cacheData[key];
      continue;
    }
    // 是动态加载方法，但没有缓存值
    let tempKey = key; // Getter属性值
    let memoryKey = '_' + key; // 内存中实际存储属性
    let fetchMethod = obj[key];

    Object.defineProperty(lazyObject, tempKey, {
      get: function () {
        if (!this.hasOwnProperty(memoryKey)) {
          let value = fetchMethod();
          if (value === null || value === undefined) {
            console.warn(`⚠The result of "${tempKey}" lazy loading method is ${value}`);
          }
          Object.defineProperty(this, memoryKey, {
            value: value,
            writable: true,
            configurable: true,
            enumerable: false
          });
          // 保存到Storage
          if (saveKey) {
            cacheData[tempKey] = value;
            updateCache(saveKey, cacheData);
          }
        }
        return this[memoryKey];
      },
      set: function (value) {
        if (value === undefined) {
          delete this[memoryKey];
        } else {
          this[memoryKey] = value;
        }
        if (saveKey) {
          cacheData[tempKey] = value;
          // 更新缓存，值为undefined的属性会被略过，有清除部分缓存的功能
          updateCache(saveKey, cacheData);
        }
      },
      enumerable: true,
      configurable: false
    });
  }

  return lazyObject;
}

const _myStorage = storages.create('xxx脚本缓存');
/**
 * 缓存数据
 * @param {string} key
 * @param {any} value
 * @param {number} expire 过期时间戳，ms
 */
function updateCache(key, value, expire) {
  if (!key) {
    throw new Error('缓存key不能为空');
  }
  if (expire) {
    value.__expire = expire;
  }
  _myStorage.put(key, value);
  delete value.__expire;
}

/**
 * 读取缓存数据，数据不存在或者过期会返回默认值或null
 * @param {string} key key
 * @param {any} defaultValue 数据不存在时返回的默认值
 * @returns 没有缓存会返回null
 */
function getCache(key, defaultValue) {
  if (!key) {
    return defaultValue;
  }
  const value = _myStorage.get(key);

  if (value === undefined || (value.__expire && value.__expire < Date.now())) {
    return defaultValue || null;
  }

  delete value.__expire;
  return value;
}

/**
 * 清理缓存，key为空时清理当前Storage全部缓存
 * @param {string|undefined} key
 */
function clearCache(key) {
  if (key) {
    _myStorage.remove(key);
  } else {
    console.info('清除当前脚本所有缓存\n');
    _myStorage.clear();
  }
}

// ==================== 图像懒加载 =======================
let _imageCache = {};
events.on('exit', function () {
  console.log('释放图片资源', Object.values(_imageCache).length);
  Object.values(_imageCache).forEach((img) => {
    img.recycle();
  });
});

// 通过闭包保存图片路径参数
function _loadImage(path) {
  return function () {
    console.log('加载图片：' + path);
    let img = images.read(path);
    if (img == null) {
      throw new Error('图片资源不存在：' + path);
    }
    _imageCache[path] = img;
    return img;
  };
}

function createImageLazyObject(imagePathMap) {
  let lazyObject = {};
  for (let key in imagePathMap) {
    if (Object.hasOwnProperty.call(imagePathMap, key)) {
      // 将图片路径转为动态加载图片方法
      lazyObject[key] = _loadImage(imagePathMap[key]);
    }
  }

  return createLazyObject(
    lazyObject,
    undefined // 图片对象不建议保存到Storage，如果需要得先转为base64
  );
}
```

## 三、使用示例

### 1. 普通懒加载对象

通过 `createLazyObject(obj[, saveKey])` 创建一个懒加载对象，obj的每个属性值为 `Function` 类型的懒加载方法。

若设置了`saveKey` 参数，在懒加载方法触发后，将方法的返回值存储到 Storage 中，`saveKey` 作为不同懒加载对象的标识符号；若 `saveKey` 参数为空，懒加载方法触发后，返回值则仅保存在内存中，下次程序启动后在用到该属性时重新触发其懒加载方法。

> **注意事项**：懒加载方法不要返回 `null` 或者 `undefined`

```js
// 定义两个懒加载方法
function fetchName() {
  console.log('触发name动态方法');
  return 'John Doe'; // 假设获取到的名称是 'John Doe'
}

function fetchAge() {
  console.log('触发age动态方法');
  return 30; // 假设获取到的年龄是 30
}

let identifier = 'foo';

// 定义一个懒加载对象
let lazyObject = createLazyObject(
  {
    name: fetchName,
    age: fetchAge,
    sex: 'male'
  },
  identifier // 开启Storage持久化
);
```

测试属性获取、修改

```js
// 先清理缓存
clearCache(identifier);
console.log(getCache(identifier));

console.log(lazyObject);

console.log('================测试获取===================');
console.log(lazyObject.name); // 懒加载
console.log(lazyObject.name); // 已获取到
console.log(lazyObject.age); // 懒加载
console.log(getCache(identifier));
console.log(lazyObject);

console.log('================测试修改===================');
lazyObject.age = 20; // 懒加载属性被重新赋值，触发Setter方法；保存到Storage
lazyObject.sex = 'female'; // 静态属性被重新赋值，不触发Setter方法；不保存到Storage
console.log(lazyObject.age);
console.log(getCache(identifier));
console.log(lazyObject);

console.log('================测试清除缓存===================');
lazyObject.age = undefined;
console.log(lazyObject.age); // 重新触发懒加载
console.log(getCache(identifier));
console.log(lazyObject);
```

### 2. 图像资源

```js
// 定义一个图像懒加载对象，值为图片路径
let imgResource = createImageLazyObject({
  home: '/sdcard/Download/home.jpg',
  shop: '/sdcard/Download/shop.jpg',
});

console.log(imgResource);
console.log(imgResource.icon);
console.log(imgResource.icon.getWidth());
console.log(imgResource.icon2);
console.log(imgResource.icon2.getWidth());
```

