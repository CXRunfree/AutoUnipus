## AutoUnipus

#### Wake up!! 都到2024年了

##### 还在为刷不完的习题而苦恼?

##### 还要赶在DDL前求人代刷课? 

##### 为了帮助大学僧们(比如我自己)解决这些痛点, AutoUnipus项目应运而生~

**项目简述:**

本项目基于Microsoft开发的playwright库, 运用Python和部分Javascript编写而成, 程序预设了两种运行模式：自动模式(Automode) 和 辅助模式(Assistmode).

**功能介绍:**

- 启动时自动登录unipus并跳转至网课网站
- 在**自动模式**下, 程序将自行识别"必修"练习题,并依此进行作答,会**自动进行提交;**
- 在**辅助模式**下, 你只需进入任意一个题目界面, 在程序界面按下Enter键,程序会自动选中正确答案, 但**不会直接提交;**
- 程序获取的答案正确率为100%

**注意事项:**

0. 程序目前仅支持**单选题**作答, 若出现特殊类型题目将**不会提交作答**;

   目前只支持**能够重复作答**的课程, 如果**只记录第一次**成绩请勿用本程序;

3. 使用前须填写好**account.json**文件
   

<img width="701" alt="account" src="https://github.com/CXRunfree/AutoUnipus/assets/79365257/73a373f8-d656-4cd2-8810-ab8f6d09a260">


   **各项参数含义:**

   `username:`	填写账号;

   `password:`	填写密码;

   `Automode:`	指定程序运行模式, `true`为自动模式, `false`为辅助模式

   ​						(注意此项不加双引号,字母小写)

   `Driver:`		指定程序启动的浏览器,可选项为`Edge`和`Chrome` (Google浏览器)

   ​						注意此项首字母大写,默认启动Windows自带的Edge; 若使用Google浏览器, 请确保安装在**默认路径;**

   `Key:`				填写你获取的赞助密钥, 用来关闭程序内部的打赏广告

   `class_url:`	指定程序要进行自动答题的网课链接, 当且仅当**自动模式**启动时, 需要填写此项;

   示范链接:

   ```
   https://u.unipus.cn/user/student/mycourse/courseCatalog?courseId=...&school_id=...&eccId=...&classId=...&coursetype=0
   ```

3. 登录界面如果出现图形验证码, 请手动输入 (验证码太抽象了, 接入了ai识别也不好使)

5. 假如答题中途网站提示"检测到异常行为,请进行安全验证"不必担心, 只需手动验证即可

   如果不希望出现此提示, 你可以选择使用**辅助模式**, 能够一定程度减小出现的概率.

   (作者用自己的账号测试了几十次, 其实没啥问题) 


**发行版下载:**
   https://github.com/CXRunfree/AutoUnipus/releases
   

**作者的碎碎念:**

​	项目的开发的确是一件耗时又费力的事情, 从前期的构思设计到后期的优化测试, 用了差不多一个月吧, 但想到能帮助到更多像我一样有需要的人, 这个项目的存在也便有了意义。你的认可对作者很重要，不妨留下一个star？如果可以的话还请赞助一下作者的项目吧~

 ( 扫一扫文件夹里的`QRcode.jpg`就好啦！)

**赞助说明:**

​	为维持项目运转, 程序内置了赞助模块, 会在恰当的时候提示用户赞助。已打赏的用户可以关注作者的CSDN账号Runfreeone,通过私信获取赞助密钥, 然后填写在`account.json`文件里即可。



**声明:**

- 本项目完全免费,不存在收费才能解锁的功能, 打赏仅用于支持项目和关闭广告;

- 为了保护项目成果, 当下只开源主体文件，而部分核心代码选择不公开; 这不会影响**发行版**(Releases)程序的运行

-  本项目只能用于学习和研究英语及计算机原理(你懂的)

**还等什么，快开始愉快的刷课吧~~**

#### 
