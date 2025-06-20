from app.gpt.prompt import BASE_PROMPT

note_formats = [
    {'label': '目录', 'value': 'toc'},
    {'label': '原片跳转', 'value': 'link'},
    {'label': '原片截图', 'value': 'screenshot'},
    {'label': 'AI总结', 'value': 'summary'}
]

note_styles = [
    {'label': '精简', 'value': 'minimal'},
    {'label': '详细', 'value': 'detailed'},
    {'label': '学术', 'value': 'academic'},
    {"label": '教程',"value": 'tutorial', },
    {'label': '小红书', 'value': 'xiaohongshu'},
    {'label': '生活向', 'value': 'life_journal'},
    {'label': '任务导向', 'value': 'task_oriented'},
    {'label': '商业风格', 'value': 'business'},
    {'label': '学习笔记', 'value': 'studynote'},
    {'label': '会议纪要', 'value': 'meeting_minutes'}
]


# 生成 BASE_PROMPT 函数
def generate_base_prompt(title, segment_text, tags, _format=None, style=None, extras=None):
    # 生成 Base Prompt 开头部分
    prompt = BASE_PROMPT.format(
        video_title=title,
        segment_text=segment_text,
        tags=tags
    )

    # 添加用户选择的格式
    if _format:
        prompt += "\n" + "\n".join([get_format_function(f) for f in _format])

    # 根据用户选择的笔记风格添加描述
    if style:
        prompt += "\n" + get_style_format(style)

    # 添加额外内容
    if extras:
        prompt += f"\n{extras}"
    return prompt


# 获取格式函数
def get_format_function(format_type):
    format_map = {
        'toc': get_toc_format,
        'link': get_link_format,
        'screenshot': get_screenshot_format,
        'summary': get_summary_format
    }
    return format_map.get(format_type, lambda: '')()


# 风格描述的处理
def get_style_format(style):
    style_map = {
        'minimal': '1. **精简信息**: 仅记录最重要的内容，简洁明了。',
        'detailed': '2. **详细记录**: 包含完整的内容和每个部分的详细讨论。需要尽可能多的记录视频内容，最好详细的笔记',
        'academic': '3. **学术风格**: 适合学术报告，正式且结构化。',
        'xiaohongshu': '''4. **小红书风格**: 
### 擅长使用下面的爆款关键词：
好用到哭，大数据，教科书般，小白必看，宝藏，绝绝子神器，都给我冲,划重点，笑不活了，YYDS，秘方，我不允许，压箱底，建议收藏，停止摆烂，上天在提醒你，挑战全网，手把手，揭秘，普通女生，沉浸式，有手就能做吹爆，好用哭了，搞钱必看，狠狠搞钱，打工人，吐血整理，家人们，隐藏，高级感，治愈，破防了，万万没想到，爆款，永远可以相信被夸爆手残党必备，正确姿势

### 采用二极管标题法创作标题：
- 正面刺激法:产品或方法+只需1秒 (短期)+便可开挂（逆天效果）
- 负面刺激法:你不XXX+绝对会后悔 (天大损失) +(紧迫感)
利用人们厌恶损失和负面偏误的心理

### 写作技巧
1. 使用惊叹号、省略号等标点符号增强表达力，营造紧迫感和惊喜感。
2. **使用emoji表情符号，来增加文字的活力**
3. 采用具有挑战性和悬念的表述，引发读、"无敌者好奇心，例如"暴涨词汇量"了"、"拒绝焦虑"等
4. 利用正面刺激和负面激，诱发读者的本能需求和动物基本驱动力，如"离离原上谱"、"你不知道的项目其实很赚"等
5. 融入热点话题和实用工具，提高文章的实用性和时效性，如"2023年必知"、"chatGPT狂飙进行时"等
6. 描述具体的成果和效果，强调标题中的关键词，使其更具吸引力，例如"英语底子再差，搞清这些语法你也能拿130+"
7. 使用吸引人的标题：''',

        'life_journal': '5. **生活向**: 记录个人生活感悟，情感化表达。',
        'task_oriented': '6. **任务导向**: 强调任务、目标，适合工作和待办事项。',
        'business': '7. **商业风格**: 适合商业报告、会议纪要，正式且精准。',
        'meeting_minutes': '8. **会议纪要**: 适合商业报告、会议纪要，正式且精准。',
        'studynote': '''9. **学习笔记**:
角色扮演：你是一位资深的知识管理专家和学习笔记撰写大师。你的核心任务是深入分析所提供的视频内容（基于文字稿），从中精准提炼关键信息，并将其组织成一份结构严谨、重点突出、易于学习和高效回顾的高质量Markdown笔记。
我的目标：根据提供的视频内容，为我生成一份详尽且高度结构化的Markdown学习笔记。此笔记旨在帮助我全面理解视频的核心思想、掌握关键知识点、洞悉重要论点，并获取有实际应用价值的信息。

请按照以下要求精心构建Markdown笔记：

整体摘要 (Overall Summary):
在笔记的开篇，务必提供一段精炼的摘要，清晰概括视频的核心主题、主要内容和最终结论。

主要章节/主题划分 (Main Sections/Topics):
1. **内容结构化**：依据文字稿的内在逻辑和信息流，将内容系统地划分为若干核心章节或主题。
2. **标题规范**：各章节及主题的标题应力求明确、简洁，并统一使用Markdown二级 (## 主题名称) 或三级 (### 子主题名称) 标题进行组织。
3. **参考标记**：若文字稿中包含明确的时间戳或章节提示，应积极利用这些标记辅助内容划分，以增强笔记与视频的同步性。

各章节核心内容 (Core Content for Each Section):
1. **信息提炼**：在每个章节/主题下，深入挖掘并系统性地提炼出关键信息点、核心论点、重要定义、详尽解释以及最终结论。
2. **列表呈现**：优先使用无序列表 (如 - 或 *) 或有序列表 (如 1.) 来清晰、有条理地呈现这些核心内容。
3. **重点强调**：对于至关重要的概念、高频关键词、核心原理或决定性结论，必须使用Markdown的粗体 (**文字**) 或斜体 (*文字*) 进行醒目强调，确保用户能迅速抓住学习重点。

关键术语/定义 (Key Terms/Definitions):
若视频内容中对特定专业术语或核心概念进行了解释，应将这些术语及其定义清晰地单独列出，或在相关内容旁显著标注。推荐格式：
   - **[术语/概念]:** [精准的定义或深入的解释]

精彩观点/引言 (Noteworthy Quotes/Insights):
精准摘录视频中那些富有启发性、高度概括性、或特别具有冲击力和洞察力的原话。使用Markdown的引用块 (> 引用的文字) 来突出展示这些金句。

示例/案例分析 (Examples/Case Studies):
如果视频通过具体的示例、实例或案例分析来阐述复杂观点或理论，应简明扼要地记录这些示例的核心情节、关键数据及其旨在说明的核心问题或启示。

行动建议/可实践点 (Actionable Advice/Practical Takeaways):
清晰、完整地列出视频内容中提供的所有具体行动建议、实用方法、操作步骤或可供实践的技巧。

提及的资源/工具 (Mentioned Resources/Tools - 如果有):
详尽记录视频中提及的所有具有参考价值的外部资源，例如推荐的书籍、引用的文章、相关网站链接、实用工具或软件等。

（可选）存疑点/启发性思考 (Points of Doubt/Questions for Further Thought):
若视频内容引发了任何值得进一步探讨的疑问，或者你（作为AI助手）判断某些观点或信息点需要观看者进行更深层次的思考和探究，可以明确列出这些存疑点或启发性问题。

Markdown格式与排版总要求 (Markdown Formatting and Layout Requirements):
1. **标准语法**：严格遵循并正确使用标准的Markdown语法。
2. **层级清晰**：通过合理运用标题层级（例如 #, ##, ###）来构建逻辑清晰、层次分明的内容结构。
3. **善用列表**：积极运用无序列表和有序列表，以增强信息点的组织性和可读性。
4. **有效强调**：恰当并一致地使用粗体、斜体、引用块等Markdown元素，以有效突出笔记的重点内容。
5. **整体美观**：确保最终输出的笔记排版整洁、段落分明、逻辑连贯，提供流畅、舒适的阅读体验，易于用户理解和消化。

**学习笔记的核心目标**：最终交付的笔记，不仅要做到信息全面准确，更要注重促进用户的深度理解、强化记忆和高效复习。请特别关注信息之间的内在逻辑联系，清晰揭示不同知识点之间的关联性与层级关系，帮助用户构建完整的知识体系。''',

        "tutorial":"10.**教程笔记**:尽可能详细的记录教程,特别是关键点和一些重要的结论步骤"
    }
    return style_map.get(style, '')


# 格式化输出内容
def get_toc_format():
    return '''
    9. **目录**: 自动生成一个基于 `##` 级标题的目录。不需要插入原片跳转
    '''


def get_link_format():
    return '''
    10. **原片跳转**: 为每个主要章节添加时间戳，使用格式 `*Content-[mm:ss]`。 
    重要：**始终**在章节标题前加上 `*Content` 前缀，例如：`AI 的发展史 *Content-[01:23]`。一定是标题在前 插入标记在后
    '''


def get_screenshot_format():
    return '''
11. **原片截图**:你收到的截图一般是一个网格，网格的每张图片就是一个时间点，左上角会包含时间mm:ss的格式，请你结合我发你的图片插入截图提示，请你帮助用户更好的理解视频内容，请你认真的分析每个图片和对应的转写文案，插入最合适的内容来备注用户理解，请一定按照这个格式 返回否则系统无法解析：
- 格式：`*Screenshot-[mm:ss]`

    '''


def get_summary_format():
    return '''
    12. **AI总结**: 在笔记末尾加入简短的AI生成总结,并且二级标题 就是 AI 总结 例如 ## AI 总结。
    '''
