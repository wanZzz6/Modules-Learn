## 域间目录订阅

国标附录P部分

- 订阅目标可以是：下级域ID、下级设备ID、下级的下级设备ID、下级行政区划编码、下级上报的业务分组ID、虚拟组织ID。
- 业务系统里可以当下级注册成功后，自动向其发送设备级订阅，称为**初始订阅**
- 为保持两个域间目录状态一致, 订阅域在**初始订阅**成功后需默认被订阅对象范围内的目录状态为在线, 被订阅域在收到初始订阅消息后,需要通知被订阅对象范围内目录的离线和其他异常状态。
- 上级主动订阅下级，在 Expires 过期时间内再次发送订阅以刷线订阅状态，否则下级认为上级取消订阅，不再推送设备状态通知。
- Expires 默认 600s
- 在订阅有效期内下级也可主动取消订阅
- 解码器(114)不需要订阅
- 

上级订阅示例：

```http
SUBSCRIBE sip:34020000001310000096@10.20.70.25:5060 SIP/2.0 
Call-ID: 22de68d3186948ba76bd1c2c67c0b181@0.0.0.0 
CSeq: 1 SUBSCRIBE 
From: <sip:37012300002000000001@10.20.100.11:5060>;tag=1650090755 
To: <sip:34020000001310000096@3402000000> 
Via: SIP/2.0/UDP 10.20.100.11:5060;branch=z9hG4bK1650090755102;rport;received=10.20.100.11 
Max-Forwards: 70 
Contact: "37012300002000000001" <sip:37012300002000000001@10.20.100.11:5060> 
Expires: 31536000 
Content-Type: Application/MANSCDP+xml 
Event: Catalog;id=1894 
Content-Length: 149 
 
<?xml version="1.0" encoding="GB2312"?> 
<Query>
  <CmdType>Catalog</CmdType>
  <SN>575586</SN>
  <DeviceID>34020000001310000096</DeviceID>
</Query>
```

下级回复订阅示例：

```http
SIP/2.0 200 OK 
Via: SIP/2.0/UDP 10.20.100.11:5060;branch=z9hG4bK1650090755102;rport=5060;received=10.20.100.11 
From: <sip:37012300002000000001@10.20.100.11:5060>;tag=1650090755 
To: <sip:34020000001310000096@3402000000>;tag=83055903 
Call-ID: 22de68d3186948ba76bd1c2c67c0b181@0.0.0.0 
CSeq: 1 SUBSCRIBE 
Contact: <sip:34020000001310000096@10.20.70.25:5060> 
Content-Type: Application/MANSCDP+xml 
Event: Catalog;id=1894 
User-Agent: IP Camera 
Expires: 31536000 
Content-Length:   168 
 
<?xml version="1.0" encoding="GB2312"?>
<Response>
<CmdType>Catalog</CmdType>
<SN>575586</SN>
<DeviceID>34020000001310000096</DeviceID>
<Result>OK</Result>
</Response>
```

