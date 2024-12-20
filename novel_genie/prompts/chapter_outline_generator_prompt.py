CHAPTER_OUTLINE_GENERATOR_PROMPT = """
# 网文章纲生成器

用于生成网文章节级别的规划纲要，重点关注人物、人物关系及情感发展。
请注意：章节以字数为界，并非以完整事件或场景分割。请确保剧情连续，不以章节人为分割场景或剧情。场景在章节间连续延展，人物状态、情节冲突与关系变化自然推进。

# 核心准则（请内化到生成中）
1. 人物为先：明确人物性格、动机、行为逻辑，以人物推动剧情。
2. 人物关系与情感演进：通过角色互动和情绪变化塑造人物关系的微妙转变。
3. 剧情连续性：不出现“上章结束场景/新场景开启”之类的割裂描述，章节之间保持自然延续。
4. 不以完整事件或场景作为章节分割依据，以字数控制划分章节，确保情节自然流动。

# 输入要求

## 指定分卷
作品篇幅: {work_length}
第 {designated_volume} 卷，共 {chapter_count_per_volume} 章

## 指定章节
第{designated_chapter}章

## 用户需求
{user_input}

## 网文描述
{description}

## 世界观设计
{worldview_system}

## 人物系统
{character_system}

## 当前的卷纲
{volume_design}

## 已有的章纲
{existing_chapter_outlines}

# 输出格式
请你以 <chapter_overview> 和 <characters_content> 标签的格式输出网文章节纲要。

<chapter_overview>
## 第i章
1. 内容衔接（100字内）
- 承接点：与上一章节剧情衔接的关键情节点
- 持续状态：当前场景、人物状态与情绪在本章开篇的延续

2. 本章规划（300字内）
- 场景描述：当前所在的情境与环境氛围（请确保与上章连续）
- 剧情推进：本章内将推进的情节重点与矛盾深化点
- 核心事件：本章内发生的重要事件及对人物关系、情绪、行为的影响
</chapter_overview>

<characters_content>
## 人物内容

1. 主要人物
- 当前状态：延续上章末人物的心理状态、身体状况
- 即时反应：针对当前情境的直接情感与行动反应
- 行动选择：在此情境下的具体行为及其背后的动机
- 能力表现：在具体情境中展现的能力与特长
- 性格体现：通过行动与互动突出人物性格特征
- 变化积累：从过往经历到此章为止的持续性改变或隐性影响

2. 次要人物
- 场景身份：在当下环境中的具体作用与位置
- 互动内容：与主要人物的对话、动作、情绪碰撞
- 行为影响：对主要人物情感、决策或局势的实际推动与干扰

## 发展变化

1. 关系演进
- 互动细节：人与人之间的细微互动方式、信息交换
- 情感流动：在对话与行为中表现的情绪升温、冷却或波动
- 关系微变：本章情节对人物关系格局带来的微妙变化

2. 情感发展
- 情绪基础：延续自上章的人物情绪基底
- 情感触发：本章事件或互动引发的情绪变化来源
- 情绪递进：情感在此过程中进一步激化、沉淀或转折
- 情感结果：情感变化带来的影响

3. 剧情走向
- 主线推进：本章对主线剧情的推进点
- 支线发展：需要铺垫或推进的支线内容
- 悬念设置：需要埋下的伏笔或悬念
</characters_content>

# 写作要点

1. 章节连贯
- 保持情节与场景在章节间的自然延续，不以章节人为分割事件
- 人物状态、情绪的无缝延续，确保读者感受流畅

2. 人物为本
- 人物行动推动故事发展，而非依靠硬性转场
- 保持人物性格、动机和行为逻辑的一贯性

3. 情节节奏
- 根据剧情需要灵活安排节奏，不必刻意在章末结束情节点
- 合理分配叙事密度，灵活调整张弛与矛盾深化

"""
