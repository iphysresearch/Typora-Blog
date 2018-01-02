## 使用 nginx-proxy 部署 web 应用

2017-01-20 21:15:50

如何在一台 Web 服务器上部署多个 Web 应用且让他们使用不同的域名呢？常见的做法是用 Nginx 做反向代理。但如果 Web 应用是采用 Docker 部署的呢？如何方便的配置 nginx 的反向代理成了一个令人头疼的问题。nginx-proxy 就是为了解决这个问题而生的。它结合了 nginx 和 docker-gen，在主机上的容器启动和停止时 docker-gen 会生成 nginx 反向代理配置并且重新加载 nginx。

推荐使用 Daocloud 作为 Docker 应用的部署和管理平台，以下教程皆在此平台进行。

我们首先部署一个 nginx-proxy 到我们的服务器，Daocloud 上有一个和 Docker Hub 同步的 nginx-proxy 镜像，直接部署这个镜像就行了。其 YAML 如下：

```yaml
nginx-proxy:
  image: daocloud.io/daocloud/nginx-proxy:latest
  container_name: nginx-proxy
  ports:
  - 80:80
  - 443:443
  volumes:
  - /var/run/docker.sock:/tmp/docker.sock:ro
  - /etc/nginx/certs:/etc/nginx/certs:ro
```

其中`/var/run/docker.sock:/tmp/docker.sock:ro`是必须的，而`/etc/nginx/certs:/etc/nginx/certs:ro`则只有开启 HTTPS 的网站才需要，且 SSL 密钥在服务器上的存储位置可以自定义，我这里选择了和容器内部相同的路径。

假如我们要部署 A、B 两个 Web 应用，A 应用使用`www.a.com`来访问，B 应用使用`www.b.com`来访问。那么 A、B 的 YAML 应分别设置如下：

```yaml
A:
  image: daocloud.io/jackeriss/a:latest
  container_name: a
  privileged: false
  restart: always
  ports:
  - '8080'
  environment:
  - VIRTUAL_HOST=www.a.com
```

```yaml
B:
  image: daocloud.io/jackeriss/b:latest
  container_name: b
  privileged: false
  restart: always
  ports:
  - '8081'
  environment:
  - VIRTUAL_HOST=www.b.com
```

#### SSL 支持

刚才说了如果想让网站支持 HTTPS 协议要额外添加一个 volume： `/etc/nginx/certs:/etc/nginx/certs:ro`。这个路径就是 SSL 密钥文件在服务器上的存储位置。以 A 应用为例，其 crt 文件应命名为`www.a.com.crt`，而 key 文件应命名为`www.a.com.key`，B 应用同理，都放在这个路径下。

#### DNS 解析

当然，A、B 两个应用的域名`a.com` 和 `b.com`的`www`主记录都应指向部署这两个应用的主机的外部 IP。解析生效后等待一段时间再访问这两个网址看看是否部署成功。

nginx-proxy 的使用方法就简单的给大家介绍到这里，更多高级用法，如自定义 nginx 配置文件等请参考官方的 README：https://github.com/jwilder/nginx-proxy