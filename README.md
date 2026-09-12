当前正式版本：3.2.0。新增 DIY 数据接口与联动，说明与模板见 [DIY 手册](docs/diy/GUIDE.zh-CN.md)。已通过离线检查，游戏内实机验收待完成。

# HavocEnemyDirector

本目录是此模组唯一的活动工程。当前正式版：3.2.0。

- `src/HavocEnemyDirector/`：安装源码与三语说明，ZIP 中的唯一顶层目录。
- `tests/run.py`：当前原版模板架构的检查入口；历史检查文件仅用于旧版追溯，不纳入当前发布。
- `publishing/`：中英功能正文、英文简介和更新日志、版本与 Main Files 配置。
- `release/3.2.0/`：独立安装 ZIP、中英 BBCode、英文简介、英文更新日志，恰好四个文件。
- `build/checks/`：检查与验证记录；不复制到发布目录。

在本目录执行 `./Test.ps1` 检查，`./Release.ps1` 检查并打包，`./Release.ps1 -Check` 校验已有发布。已有发布目录不可覆盖。

[安装 ZIP](release/3.2.0/HavocEnemyDirector-3.2.0.zip) · [功能与安装说明](src/HavocEnemyDirector/docs/README.zh-CN.md) · [发布流程](发布流程.md)

原版游戏源码与 LuaJIT 测试运行库默认位于工作区 `dev-support/`。可通过 DARKTIDE_DEV_SUPPORT、DARKTIDE_SOURCE 和 DARKTIDE_TEST_RUNTIME 指定位置。两个工程仅在联动检查中读取彼此声明的源码依赖，发布入口每次只生成本项目产物。

正式源码已完整移除诊断系统；Main Files 打包仍执行移除检查。原版方法回归和离线界面布局检查不替代游戏内游玩测试。测试和发布不会部署游戏或上传 Nexus。
