CONTENT_OPTIMIZER_PROMPT = """
# 网文章节内容优化器
根据用户提供的章节内容，优化为符合网文写作规则的详细章节内容，突出情节连贯性、情感波动和细节描写。

# 用户输入
## 原始章节内容
{original_chapter_content}

---
# 优化目标
根据以下规则优化章节内容：
1. 连贯性
   - 衔接上下文自然，逻辑清晰。
   - 运用伏笔为后续情节铺垫。
2. 情节设计
   - 设定2-3个转折点，增强剧情张力。
   - 确保情节设计符合人物性格与情感逻辑。
3. 情感推进
   - 设计情感曲线，设置情绪高潮点。
   - 通过场景与对话深化情感表达。
4. 细节描写
   - 突出人物内心活动与情绪变化。
   - 场景描写烘托情感氛围，增强沉浸感。

# 创作指南
1. 加强情感体验：以情感为核心，服务情节发展。
2. 注重代入感：增强阅读吸引力，让读者共情。
3. 灵活调整：根据章节类型合理分配情节、情感与叙事比重。

---
# 输出格式
## 优化后的章节内容
生成不少于2000字的完整正文，结构紧凑，情节流畅，情感丰富。
"""
