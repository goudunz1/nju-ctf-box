# 南京大学 CTF 动态容器样题

## 打包题目

本节是给没有布过题的师傅写的，将打包好的题目部署到校内靶机上的方法请看下一节

本题目的原理是用 xinetd 代理挑战程序的标准输入输出

并提供一个 TCP 服务于 8888 端口

容器配置、xinetd 配置、题目源码均位于 `src` 下，本题的解位于 `solve.py`

`src/init.sh` 用于 xinetd 启动题目，需要将其最后一行改为挑战程序的路径

**关于镜像:**

推荐使用 Alpine Linux 作为 base 因为它不占空间

`xinetd.Dockerfile` 配置了一个基于 Alpine Linux 的  xinetd 2.3.15.4
镜像 goudunz1/xinetd:alpine

**PS:** xinetd 源代码有一个小问题，可能会导致每次启动容器时端口延迟很久才绑定，
所以上述镜像是 patch 过的

详情见 [issue47](https://github.com/openSUSE/xinetd/issues/47)

以本题的构建和测试为例，先打包镜像：

```sh
docker build src -t test
```

运行和测试

`docker run -d --rm -e GZCTF_FLAG='flag{PLACE_HOLDER}' --name test -p12345:8888 test`

## 如何在校内靶机上制作动态容器题

我们的机器 `114.212.190.11` 不出网，所以相比寻常的题目部署要麻烦一些

机器的 5000 端口处开放了一个私人注册表，
一是因为 GZCTF 每次都需要从指定的注册表拉取容器 (`ImagePullPolicy: Always`)，
二也是方便大家传题

请首先把制作好的容器上传到这个注册表

由于这是内网机器，第一次上传时请为机器的 SSL 证书 `trinity.crt` 添加信任，
如何添加信任取决于您的操作系统

为了防止冲突，建议的 tag 为 `[your_name]/[challenge]:[ver]`
或者 `[category]/[challenge]:[ver]`

以前者为例：

```sh
docker login 'https://114.212.190.11:5000' -u [username]
docker tag 'goudunz1/test:0.1' '114.212.190.11:5000/goudunz1/test:0.1'
docker push '114.212.190.11:5000/goudunz1/test:0.1' --platform=linux/amd64
```

接下来，在 GZCTF 中写明容器为 `[your_name]/[challenge]:[ver]` 就可以了，
无需添加 `114.212.190.11:5000` 作为前缀

在 GZCTF 发布题目之前，别忘了填您的服务开放的端口号！
（默认是 80，例如本题应改为 8888）

**PS:** 本机器还提供通过 scp 上传镜像 tar 包的办法，请登录机器后台查看 `/README`

**关于动态容器:**

如果题目是静态容器，那么已经可以开始使用了，如果您想布置动态 flag，
请在 flag 页面按照需求填写 flag 模板

GZCTF 实现动态 flag 的方式是将做好的动态 flag 以环境变量 `GZCTF_FLAG` 注入到容器中，
请将这个环境变量的值当作 flag，
具体的方法请参照样题的 `src/init.sh`

**flag 模板规则:**（来自 GZCTF 文档）

1. 请输入 flag 模版字符串，留空以生成随机 GUID 作为 flag
2. 指定 [GUID]则会仅替换此处的占位符为随机 GUID
3. 若指定 [TEAM_HASH] 则它将会被自动替换为队伍 Token 和比赛信息所生成的哈希值
4. 若未指定 [TEAM_HASH] 则将启用 Leet 字符串功能，将会基于模版对花括号内字符串进行变换，需要确保 flag 模版字符串的熵足够高
5. 若需要在指定 [TEAM_HASH] 的情况下启用 Leet 字符串功能，请在 flag 模版字符串 之前 添加 [LEET] 标记，此时不会检查 flag 模版字符串的熵
6. 如果需要在 flag 生成中启用特殊字符，请在字符串开头用 [CLEET] 代替 [LEET]，这可能造成对于题目的注入问题

flag 模板编写示例：

  - 留空 将会生成 `flag{1bab71b8-117f-4dea-a047-340b72101d7b}`
  - `flag{hello world}` 将会生成 `flag{He1lo_w0r1d}`
  - `[CLEET]flag{hello sara}` 将会生成 `flag{He1!o_$@rA}`
  - `flag{hello_world_[TEAM_HASH]}` 将会生成 `flag{hello_world_5418ce4d815c}`
  - `[LEET]flag{hello world [TEAM_HASH]}` 将会生成 `flag{He1lo_w0r1d_5418ce4d815c}`

本题的 flag 举例：

`[LEET]flag{This is why ECB is so insecure [TEAM_HASH]}`

`flag{7HI5_IS_WHY_Ecb_i5_5O_ins3cUrE_69e75b30796f}`

---

祝各位师傅玩得开心！

如果有其它需求可以查看机器后台 `/README` 中的说明

by 狗敦子

2024.10.23
