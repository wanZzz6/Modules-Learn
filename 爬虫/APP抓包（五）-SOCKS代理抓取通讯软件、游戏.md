# SOCKS代理抓取通讯软件、游戏

## 一、前言

在一些通讯类、游戏、体育解说类的软件中，为了保证数据的实时性、保密性和减少消息长度，客户端和服务器之间通常会设计私有协议，并使用 TCP/UDP 进行传输，而不是 HTTP(S) 协议。因此，一般的 HTTP 代理方式通常无法获取这种实时的数据包。

在本系列之前的文章中我们提到过 SOCKS 代理，本文将详细介绍一下SOCKS代理以及SOCKS代理与http代理的差异。

## 二、SOCKS 代理

### 2.1 简介

SOCKS代理（SOCKS proxy）是一种网络代理协议，用于在计算机网络上进行数据传输。它允许客户端通过中间代理服务器与远程服务器进行通信，同时隐藏客户端的真实IP地址和身份，使得客户端可以通过代理服务器与远程服务器建立连接并进行数据交换。

使用SOCKS代理时，客户端发送的网络请求将先发送到代理服务器，然后由代理服务器转发到远程服务器。代理服务器负责建立连接、中转数据和响应客户端请求。同时，代理服务器会改变数据包的源IP地址，使得远程服务器无法直接识别客户端的真实身份。

根据OSI模型，Socks代理工作在**会话层**，不要求应用程序遵循特定的操作系统平台，Socks代理只是简单地传递数据包，而不必关心是何种应用协议，这意味着它可以透明地处理不同类型的网络流量，包括Web浏览器、邮件客户端、文件传输协议（FTP）等等。

SOCKS代理可以用于各种网络活动，如访问被限制的网站、保护隐私、**绕过防火墙限制**等。

socks代理格式：

- `socks5://proxyip:proxyport`
- `socks4/4a://proxyip:proxyport`

### 2.2 SOCKS5

目前Socks代理分Socks4和Socks5两种类型，Socks4只支持TCP，而Socks5 提供了更多的功能和安全性，包括支持UDP协议、身份验证、加密以及IPv6。

> This new protocol extends the SOCKS Version 4 model to include UDP, and extends the framework to include provisions for generalized strong authentication schemes, and extends the addressing scheme to encompass domain-name and V6 IP addresses.

### 2.3 Socks代理与HTTP代理的差异

| 代理类型 | HTTP代理 | SOCKS5代理 |
| --- | --- | --- |
| 协议类型 | HTTP协议 | SOCKS协议 |
| 功能 | 可以转发HTTP和HTTPS请求 | 可以转发TCP和UDP请求 |
| 认证方式 | 基本认证、摘要认证等 | 用户名和密码或GSSAPI身份验证 |
| 支持的协议 | 仅支持HTTP和HTTPS协议 | **以TCP/UDP传输的任何上层协议** |
| 支持的应用程序 | 适用于HTTP和HTTPS应用程序 | 适用于更多类型的应用程序 |
| 安全性 | 不支持加密传输 | 支持加密传输和身份验证 |
| 性能 | 对HTTP和HTTPS请求的转发进行了优化 | 转发请求时需要更多的处理和计算 |
| 使用场景 | 适用于Web浏览器和HTTP客户端 | 适用于更广泛的应用程序和网络服务，如通讯应用、游戏等 |
| 使用限制 | 只能转发HTTP和HTTPS请求 | 可以转发更多类型的请求，但可能会被防火墙和安全策略限制；无法处理标准隧道加密 |

---上表由ChatGPT生成

## 三、SOCKS5 协议细节

RFC 1928 原文地址： [SOCKS Protocol Version 5](https://tools.ietf.org/pdf/rfc1928.pdf)

译文：[SOCKS5（1）- RFC1928](../网络协议/SOCKS5（1）- RFC1928翻译.md)
