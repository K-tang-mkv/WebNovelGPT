DETAILED_OUTLINE_GENERATOR_PROMPT = """
# 网文细纲生成器
根据用户输入的网文粗纲和前几卷的细纲总结以及指定分卷生成对应的网文细纲。

# 用户输入
## 指定分卷
{designated_volume}

## 网文描述
{description}
要求每章内容字数不少于{section_word_count}字。

## 网文粗纲
{rough_outline}

## 前几卷细纲总结
{prev_volume_summary}

# 输出格式
# 第x章
## 第x章基础信息
1. 明确章节类型
  过渡章:调节节奏,转换氛围
  铺垫章:埋设伏笔,营造基调
  发展章:推进剧情,深化人物
  高潮章:爆发冲突,情感释放
  总结章:梳理线索,沉淀情感
- 确定核心功能
  主线推进作用
  人物刻画作用
  情感渲染作用
  悬念设置作用

2. 篇章定位
   - 所属卷册与阶段
   - 章节总字数范围(不少于2000字)
   - 本章在剧情线上的定位
   - 需要推进的主要剧情方向

3. 衔接关系
   - 承接上章末尾情境/情绪
   - 本章结尾预期效果
   - 为下章开头做好铺垫

## 第x章（核心内容）

### 一、故事主线
1. 核心事件
   - 起因(可选，前文铺垫与当前局势)
   - 发展(必要，2-3个关键节点)
   - 高潮(可选，爆发冲突,情感释放)
   - 结果(可选，不一定有结果，若有则直接影响与后续走向)

2. 转折设计
   - 主要转折点
   - 合理性说明
   - 对后续的影响

### 二、情感设计
- 确定主导情绪
  装逼型:痛快、自得、扬眉吐气
  热血型:激昂、振奋、不屈
  温情型:感动、温暖、治愈
  悲情型:忧伤、愤怒、不甘
- 设计情绪曲线
  与上章情绪的承接点
  本章情绪的推进路线
  情绪曲线并非都是闭合的
  可选，情绪宣泄的高潮点
  可选，为下章埋设的情绪引子

- 规划爽点设置
  主要爽点(1-2个)
  次要爽点(2-3个)
  爽点出现的时机
  爽点的递进关系

### 三、人物刻画
1. 主要人物(1-2个)
   - 当前状态
   - 行为动机
   - 心理变化
   - 性格体现

2. 重要互动
   - 核心对手/盟友
   - 关键对话/冲突
   - 关系发展

### 四、场景呈现
1. 主场景(1-2处)
   - 环境特征
   - 氛围营造
   - 细节点缀

2. 场景作用
   - 衬托情绪
   - 推动剧情
   - 体现主题

### 五、节奏设计
- 总体节奏基调
  舒缓型:徐徐展开,细腻描写
  平稳型:稳步推进,重在过渡
  紧凑型:快速发展,重在推进
  激烈型:节奏强烈,重在爆发
- 节奏变化规划
  开头节奏(承接上文)
  发展节奏(必要，推进情节)
  高潮节奏(可选，爆发冲突)
  结尾节奏(可选，埋设引子)
- 伏笔设置(可选)

## 注意事项

1. 聚焦原则
   - 需要详细生成指定章节范围的所有细纲
   - 每章突出一条主线
   - 其他内容作为陪衬

2. 连贯要求
   - 与前文自然衔接
   - 为后文做好铺垫
   - 保持人物性格连贯

3. 创作提示
   - 情节要出人意料
   - 情感要真实自然
   - 细节要生动传神
   - 节奏要张弛有度
"""

DETAILED_OUTLINE_SUMMARY_PROMPT = """
# 网文细纲总结生成器
根据用户输入的网文粗纲和网文细纲生成对应的细纲总结：

# 用户输入
## 指定章节范围
{chapter_count_per_volume}

## 网文细纲：第{volume_number}卷
{detailed_outline}

## 网文粗纲
{rough_outline}

# 输出格式
## 第x卷基础信息
1. 明确卷节类型
  过渡卷:调节节奏,转换氛围
  铺垫卷:埋设伏笔,营造基调
  发展卷:推进剧情,深化人物
  高潮卷:爆发冲突,情感释放
  总结卷:梳理线索,沉淀情感
- 确定核心功能
  主线推进作用
  人物刻画作用
  情感渲染作用
  悬念设置作用

2. 篇卷定位
   - 所属卷册与阶段
   - 卷节总字数范围
   - 本卷在剧情线上的定位
   - 需要推进的主要剧情方向

3. 衔接关系
   - 承接上卷末尾情境/情绪
   - 本卷结尾预期效果
   - 为下卷开头做好铺垫

## 第x卷总结（核心内容）

### 一、故事主线
1. 核心事件
   - 起因(前文铺垫与当前局势)
   - 发展(2-3个关键节点)
   - 结果(直接影响与后续走向)

2. 转折设计
   - 主要转折点
   - 合理性说明
   - 对后续的影响

### 二、情感设计
- 确定主导情绪
  装逼型:痛快、自得、扬眉吐气
  热血型:激昂、振奋、不屈
  温情型:感动、温暖、治愈
  悲情型:忧伤、愤怒、不甘
- 设计情绪曲线
  与上卷情绪的承接点
  本卷情绪的推进路线
  情绪宣泄的高潮点
  为下卷埋设的情绪引子
- 规划爽点设置
  主要爽点(1-2个)
  次要爽点(2-3个)
  爽点出现的时机
  爽点的递进关系

### 三、人物刻画
1. 主要人物(1-2个)
   - 当前状态
   - 行为动机
   - 心理变化
   - 性格体现

2. 重要互动
   - 核心对手/盟友
   - 关键对话/冲突
   - 关系发展

### 四、场景呈现
1. 主场景(1-2处)
   - 环境特征
   - 氛围营造
   - 细节点缀

2. 场景作用
   - 衬托情绪
   - 推动剧情
   - 体现主题

### 五、节奏设计
- 总体节奏基调
  舒缓型:徐徐展开,细腻描写
  平稳型:稳步推进,重在过渡
  紧凑型:快速发展,重在推进
  激烈型:节奏强烈,重在爆发
- 节奏变化规划
  开头节奏(承接上文)
  发展节奏(推进情节)
  高潮节奏(爆发冲突)
  结尾节奏(埋设引子)

## 注意事项

1. 聚焦原则
   - 需要精炼地生成指定卷的细纲总结
   - 每卷突出若1～3条主线
   - 其他内容作为陪衬

2. 连贯要求
   - 与前文自然衔接
   - 为后文做好铺垫
   - 保持人物性格连贯

3. 创作提示
   - 情节要出人意料
   - 情感要真实自然
   - 细节要生动传神
   - 节奏要张弛有度
"""
