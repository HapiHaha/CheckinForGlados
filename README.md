# CheckinForGlados
Checkin script for Glados, program with Python, just for purposes. Comments are welcome~
# 为Glados专门写的签到程序
- 配合操作系统提供的定时运行脚本，实现每日自动签到。
- 通过server酱，可将签到结果上报至微信，方便确定签到情况。
- 逻辑比较清晰简单，稍作更改可以用于其他cookie不常更改的网站的签到。
- 代码不精，仅作交流参考。
# 文件结构
- Checkin.py即为签到使用的脚本，需要使用账号对应的cookie以用于网站的身份验证。
- cookie可以自行从浏览器提取，或者使用GetCookie.py脚本获取。
- 以上两个脚本模拟发送HTTP的post数据包以获得需要的信息。
- 另也可使用selenium模块模拟浏览器行为进行签到，可以用于更加复杂的签到场景。
- 代码不精，仅作参考。
# server酱使用方法简述
- server酱可将脚本or程序运行数据上报至微信，方便与随时随地查看运行状态。
- 官方网站：
 https://sct.ftqq.com/
- 注册后获得SendKey填写进Checkin.py脚本即可实现签到结果上报至微信，掌握签到信息。
