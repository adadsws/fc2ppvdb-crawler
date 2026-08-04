# 固定上游参考

`grill-with-docs/` 使用 Git submodule 保存固定版本的外部参考代码，只读使用，不与本项目源码混合。

| 项目 | 值 |
|---|---|
| 上游 URL | `https://github.com/mattpocock/skills.git` |
| 固定 commit | `ed37663cc5fbef691ddfecd080dff42f7e7e350d` |
| 许可证 | MIT（见 `grill-with-docs/LICENSE`） |
| 记录方式 | Git submodule / gitlink |

重建固定内容：

```powershell
git submodule update --init --recursive -- reference/grill-with-docs
git -C reference/grill-with-docs rev-parse HEAD
```

第二条命令必须输出上述完整 commit；不得改为浮动分支或未验证 tag。
