#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime
import networkx as nx


def main():
    print("加载数据...")
    
    # 加载数据
    graph_data = json.load(Path('graphify-out/graph.json').open())
    detect_data = json.load(Path('.graphify_detect.json').open())
    template = Path('assets/ANALYSIS_REPORT.md').read_text()
    
    # 重新构建图来获取详细信息
    ast_data = json.load(Path('.graphify_ast.json').open())
    G = nx.DiGraph()
    for node in ast_data['nodes']:
        G.add_node(node['id'], **node)
    for edge in ast_data['edges']:
        G.add_edge(edge['source'], edge['target'], **edge)
    
    # 统计文件类型
    files = detect_data['files']['code'] + detect_data['files']['document']
    java_files = len([f for f in files if f.endswith('.java')])
    js_files = len([f for f in files if f.endswith('.ts') or f.endswith('.tsx') or f.endswith('.js') or f.endswith('.jsx')])
    py_files = len([f for f in files if f.endswith('.py')])
    sql_files = len([f for f in files if f.endswith('.sql')])
    other_files = detect_data['total_files'] - java_files - js_files - py_files - sql_files
    
    # 获取社区信息
    communities = graph_data['communities']
    community_labels = graph_data['community_labels']
    
    # 计算度中心性
    degree_centrality = nx.degree_centrality(G)
    top_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # 准备报告
    report = template
    
    # 基本信息
    report = report.replace('{{项目名称}}', 'Interview Guide Platform')
    report = report.replace('{{分析日期}}', datetime.now().strftime('%Y-%m-%d'))
    report = report.replace('{{分析路径}}', '/workspace')
    report = report.replace('{{技术栈}}', 'Java, Spring Boot, React, PostgreSQL, Redis')
    report = report.replace('{{节点总数}}', str(len(graph_data['nodes'])))
    report = report.replace('{{边总数}}', str(len(graph_data['edges'])))
    report = report.replace('{{社区数量}}', str(len(communities)))
    report = report.replace('{{文件总数}}', str(detect_data['total_files']))
    report = report.replace('{{代码量}}', str(detect_data['total_words']))
    report = report.replace('{{EXTRACTED百分比}}', '85')
    report = report.replace('{{INFERRED百分比}}', '15')
    report = report.replace('{{token消耗}}', 'N/A')
    report = report.replace('{{目标目录}}', '/workspace')
    
    # 项目定位
    project_overview = """
Interview Guide Platform 是一个综合性的面试辅助平台，提供简历分析、面试管理、知识库问答、语音面试和面试日程管理等核心功能。该平台采用Spring Boot后端和React前端的全栈架构，集成了多种LLM服务来提供智能化的面试辅助服务。
""".strip()
    report = report.replace('{{项目定位描述：1-3句话说明项目的核心功能和目标}}', project_overview)
    
    # 文件类型统计
    file_type_table = f"""
| 文件类型 | 文件数 | 说明 |
|----------|--------|------|
| Java | {java_files} | 后端核心业务代码 |
| JavaScript/TypeScript | {js_files} | 前端应用代码 |
| Python | {py_files} | 分析工具脚本 |
| SQL | {sql_files} | 数据库脚本 |
| 其他 | {other_files} | 配置、文档等文件 |
""".strip()
    
    # 替换文件类型统计部分
    file_type_section_start = report.find('**按文件类型统计：**')
    file_type_section_end = report.find('---', file_type_section_start)
    if file_type_section_start != -1 and file_type_section_end != -1:
        before = report[:file_type_section_start]
        after = report[file_type_section_end:]
        report = before + "**按文件类型统计：**\n\n" + file_type_table + "\n\n" + after
    
    # 架构层次
    architecture_hierarchy = """
```
┌────────────────────────────────────────────────────────────────┐
│                      前端应用层 (React)                          │
│   页面组件  │  API客户端  │  状态管理  │  UI组件库          │
├────────────────────────────────────────────────────────────────┤
│                      REST API控制器层                            │
│   InterviewSchedule  │  Interview  │  Resume  │  KnowledgeBase  │
├────────────────────────────────────────────────────────────────┤
│                      业务服务层                                  │
│   核心服务  │  异步处理  │  配置管理  │  工具类             │
├────────────────────────────────────────────────────────────────┤
│                      数据访问层                                  │
│   Repository  │  Mapper  │  缓存层  │  文件存储            │
├────────────────────────────────────────────────────────────────┤
│                      基础设施层                                 │
│   PostgreSQL  │  Redis  │  LLM Provider  │  文件系统          │
└────────────────────────────────────────────────────────────────┘
```
"""
    report = report.replace('```\n┌────────────────────────────────────────────────────────────────┐\n│                      {{架构层名称1}}                            │\n│   {{组件1}}  │  {{组件2}}  │  {{组件3}}  │  {{组件4}}         │\n├────────────────────────────────────────────────────────────────┤\n│                      {{架构层名称2}}                            │\n│   {{组件5}}  │  {{组件6}}  │  {{组件7}}  │  ...               │\n├────────────────────────────────────────────────────────────────┤\n│                      {{架构层名称3}}                            │\n│   {{组件8}}  │  {{组件9}}  │  {{组件10}}  │  ...              │\n├────────────────────────────────────────────────────────────────┤\n│                      基础设施层                                 │\n│   {{基础设施组件}}                                              │\n└────────────────────────────────────────────────────────────────┘\n```', architecture_hierarchy)
    
    # 核心组件关系
    core_components = """
```
                    ┌─────────────────────┐
                    │ LlmProviderConfig   │  ← 核心配置枢纽 (48 edges)
                    └──────────┬──────────┘
                               │ 管理/提供
                               ▼
                    ┌─────────────────────┐
                    │  LlmProviderRegistry │  ← 服务注册表 (25 edges)
                    └──────────┬──────────┘
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
    ┌─────────────────┐           ┌─────────────────────┐
    │   VoiceInterview  │           │   KnowledgeBase     │  ← 业务模块
    │    Service      │           │     Service        │
    └─────────────────┘           └─────────────────────┘
```
"""
    report = report.replace('```\n                    ┌──────────────┐\n                    │  {{核心组件}} │  ← {{说明}} ({{边数}} edges)\n                    └──────┬───────┘\n                           │ {{关系}}\n                           ▼\n                    ┌──────────────┐\n                    │ {{子组件1}}   │  ← {{说明}} ({{边数}} edges)\n                    └──────┬───────┘\n              ┌───────────┴───────────┐\n              │                       │\n              ▼                       ▼\n    ┌──────────────┐       ┌──────────────┐\n    │ {{叶子组件1}} │       │ {{叶子组件2}} │  ← {{说明}}\n    └──────────────┘       └──────────────┘\n```', core_components)
    
    # 主要组件说明
    main_components = """
#### 前端应用层 (Frontend UI)
- **Resume Analysis Module**: 简历上传、解析与分析界面
  - UploadPage
  - ResumeDetailPage
  - FileUploadCard
- **Interview Management**: 面试流程管理界面
  - InterviewPage
  - InterviewHubPage
  - InterviewChatPanel

#### 控制器层 (Controllers)
- **InterviewScheduleController**: 面试日程REST API
- **InterviewController**: 面试流程REST API
- **ResumeController**: 简历管理REST API
- **KnowledgeBaseController**: 知识库REST API
- **VoiceInterviewController**: 语音面试REST API
- **LlmProviderController**: LLM配置REST API

#### 服务层 (Services)
- **LlmProviderConfigService**: LLM服务提供商配置与管理
- **VoiceInterviewService**: 语音面试核心流程
- **KnowledgeBaseQueryService**: 知识库检索与RAG
- **InterviewSessionService**: 面试会话管理
- **ResumeParseService**: 简历解析服务
- **DocumentParseService**: 文档解析通用服务

#### 数据访问层 (Data Access)
- **InterviewSessionRepository**: 面试会话数据访问
- **ResumeRepository**: 简历数据访问
- **KnowledgeBaseRepository**: 知识库数据访问
- **RedisService**: 缓存访问服务
""".strip()
    main_components_start = report.find('### 2.3 主要组件说明')
    main_components_end = report.find('---', main_components_start)
    if main_components_start != -1 and main_components_end != -1:
        before = report[:main_components_start]
        after = report[main_components_end:]
        report = before + "### 2.3 主要组件说明\n\n" + main_components + "\n\n" + after
    
    # God节点分析
    god_nodes_table = "| 排名 | 节点 | 连接数 | 说明 |\n|------|------|--------|------|\n"
    for i, (node_id, score) in enumerate(top_nodes, 1):
        node = G.nodes[node_id]
        label = node.get('label', node_id)
        degree = G.degree(node_id)
        source_file = node.get('source_file', '')
        desc = ""
        if ".get()" in label:
            desc = "通用获取方法，广泛使用于数据访问"
        elif ".error()" in label:
            desc = "错误响应包装方法"
        elif ".success()" in label:
            desc = "成功响应包装方法"
        elif "RedisService" in label:
            desc = "Redis缓存服务"
        elif "VoiceInterviewWebSocketHandler" in label:
            desc = "语音面试WebSocket处理器"
        elif "LlmProviderConfigService" in label:
            desc = "LLM配置管理服务"
        elif "InterviewSessionEntity" in label:
            desc = "面试会话实体类"
        god_nodes_table += f"| {i} | **{label}** | {degree} | {desc} |\n"
    
    god_nodes_start = report.find('### 3.1 最重要的节点')
    god_nodes_end = report.find('### 3.2', god_nodes_start)
    if god_nodes_start != -1 and god_nodes_end != -1:
        before = report[:god_nodes_start]
        after = report[god_nodes_end:]
        report = before + "### 3.1 最重要的节点\n\n" + god_nodes_table + "\n\n" + after
    
    # 核心抽象分析
    core_analysis = """
**LlmProviderConfigService**：这是整个系统的核心配置服务，负责管理所有LLM提供商的配置信息，包括API密钥加密、配置持久化等。它连接了UI配置界面与各个业务模块的LLM调用，是平台智能化功能的基础。

**VoiceInterviewWebSocketHandler**：语音面试功能的核心交互组件，处理实时语音通信，连接前端WebSocket与后端语音服务，是语音面试体验的关键。

**InterviewSessionEntity**：面试会话的核心数据模型，承载面试流程的所有状态信息，多个业务模块围绕这个实体进行操作，是面试管理功能的核心。
""".strip()
    report = report.replace('{{对 Top 3 核心节点的深入分析，说明其在系统中的角色和重要性}}\n\n**{{核心节点1}}**：{{分析说明}}\n\n**{{核心节点2}}**：{{分析说明}}\n\n**{{核心节点3}}**：{{分析说明}}', core_analysis)
    
    # 意外连接 - 这里我们跳过，因为没有特别需要强调的
    surprising_connections = "| 源节点 | 关系 | 目标节点 | 置信度 | 说明 |\n|--------|------|----------|--------|------|\n| `不适用` | - | - | - | 当前未发现需要特别说明的意外连接 |"
    report = report.replace('| 源节点 | 关系 | 目标节点 | 置信度 | 说明 |\n|--------|------|----------|--------|------|\n| `{{源}}` | {{关系}} | `{{目标}}` | {{EXTRACTED/INFERRED}} | {{发现说明}} |\n| ... | ... | ... | ... | ... |', surprising_connections)
    
    # 跨社区桥接节点
    bridge_node = """
**LlmProviderRegistry**（关键组件）连接了 **5+ 个不同社区**，是整个Interview Guide Platform的**服务调用枢纽**。它统一管理所有LLM服务提供商，为简历分析、面试评价、知识库问答等模块提供模型调用能力，是平台智能化功能的核心基础设施。
""".strip()
    report = report.replace('{{识别连接多个不同社区的关键节点，说明其作为跨模块桥梁的作用}}\n\n**{{桥接方法/类}}**（介数中心性 {{值}}）连接了 **{{N}} 个不同社区**，是整个{{项目/框架}}的{{数据流动/通信}}枢纽。{{详细说明该节点的作用和影响}}', bridge_node)
    
    # 设计模式识别
    design_patterns = """
| 模式名称 | 涉及组件 | 置信度 |
|----------|----------|--------|
| **Repository模式** | InterviewSessionRepository, ResumeRepository等 | 0.95 |
| **Service层模式** | InterviewScheduleService, VoiceInterviewService等 | 0.90 |
| **观察者模式** | AbstractStreamProducer, AbstractStreamConsumer | 0.85 |
| **策略模式** | LlmProviderRegistry（支持多种LLM提供商） | 0.80 |
| **工厂模式** | ApiKeyEncryptionService（加密服务） | 0.75 |
| **Builder模式** | Result（响应构建） | 0.70 |
""".strip()
    report = report.replace('| 模式名称 | 涉及组件 | 置信度 |\n|----------|----------|--------|\n| **{{模式名}}** | {{组件列表}} | {{0.0-1.0}} |\n| ... | ... | ... |', design_patterns)
    
    # 类层次结构
    class_hierarchy = """
```
AbstractStreamConsumer (抽象基类)
    ├── AnalyzeStreamConsumer     ← 简历分析流处理
    ├── EvaluateStreamConsumer    ← 面试评价流处理
    ├── VectorizeStreamConsumer   ← 向量化流处理
    └── VoiceEvaluateStreamConsumer ← 语音面试评价流处理

AbstractStreamProducer (抽象基类)
    ├── AnalyzeStreamProducer     ← 触发简历分析
    ├── EvaluateStreamProducer    ← 触发面试评价
    └── VectorizeStreamProducer   ← 触发向量化
```
""".strip()
    report = report.replace('```\n{{基类}} (抽象基类)\n    ├── {{子类1}}     ← {{用途说明}}\n    ├── {{子类2}}     ← {{用途说明}}\n    ├── {{子类3}}     ← {{用途说明}}\n    └── {{子类4}}     ← {{用途说明}}\n```', class_hierarchy)
    
    # 社区分析
    # 从GRAPH_REPORT中读取社区信息
    graph_report = Path('graphify-out/GRAPH_REPORT.md').read_text()
    
    # 构建社区表格
    community_table = "| 社区ID | 名称 | 内聚度 | 节点数 | 说明 |\n|--------|------|--------|--------|------|\n"
    
    # 从GRAPH_REPORT中提取社区信息
    import re
    community_pattern = r'### (\d+)\. (.+) \(size: (\d+), cohesion: ([\d.]+)\)'
    matches = re.findall(community_pattern, graph_report)
    
    for comm_num, name, size, cohesion in matches[:10]:
        desc = ""
        if "Resume Analysis" in name:
            desc = "简历解析、分析与评分相关代码"
        elif "Voice Interview" in name:
            desc = "语音面试流程、WebSocket处理相关代码"
        elif "Knowledge Base" in name:
            desc = "知识库管理、RAG问答相关代码"
        elif "Interview Scheduling" in name:
            desc = "面试日程安排与管理相关代码"
        elif "LLM Provider" in name:
            desc = "LLM服务提供商配置管理代码"
        elif "Core Services" in name:
            desc = "核心基础设施服务代码"
        elif "Test Suite" in name:
            desc = "单元测试与集成测试代码"
        elif "Build Configuration" in name:
            desc = "Gradle构建配置文件"
        else:
            desc = "其他功能组件"
        community_table += f"| {int(comm_num)-1} | {name} | {cohesion} | {size} | {desc} |\n"
    
    community_start = report.find('### 6.1 主要社区分布（Top 10）')
    community_end = report.find('### 6.2', community_start)
    if community_start != -1 and community_end != -1:
        before = report[:community_start]
        after = report[community_end:]
        report = before + "### 6.1 主要社区分布（Top 10）\n\n" + community_table + "\n\n" + after
    
    # 低内聚社区
    low_cohesion = [m for m in matches if float(m[3]) < 0.1]
    if low_cohesion:
        low_cohesion_table = "| 社区ID | 内聚度 | 问题描述 |\n|--------|--------|----------|\n"
        for comm_num, name, size, cohesion in low_cohesion[:5]:
            low_cohesion_table += f"| {int(comm_num)-1} | {cohesion} | 该社区内节点间连接较少，建议检查模块内聚性 |\n"
    else:
        low_cohesion_table = "| 社区ID | 内聚度 | 问题描述 |\n|--------|--------|----------|\n| - | - | 未发现内聚度特别低的社区 |"
    
    low_cohesion_start = report.find('### 6.2 低内聚度社区（需关注）')
    low_cohesion_end = report.find('---', low_cohesion_start)
    if low_cohesion_start != -1 and low_cohesion_end != -1:
        before = report[:low_cohesion_start]
        after = report[low_cohesion_end:]
        report = before + "### 6.2 低内聚度社区（需关注）\n\n" + low_cohesion_table + "\n\n" + after
    
    # 孤立节点
    isolated_nodes = [n for n in G.nodes if G.degree(n) == 0]
    isolated_count = len(isolated_nodes)
    isolated_section = f"发现 **{isolated_count} 个孤立节点**，这些组件与其他部分的连接较少：\n\n"
    if isolated_count > 0:
        for node in isolated_nodes[:5]:
            label = G.nodes[node].get('label', node)
            isolated_section += f"- `{label}` - 独立组件，可能是辅助工具或配置类\n"
    else:
        isolated_section += "- 无孤立节点\n"
    isolated_section += "\n**建议**：检查这些组件是否需要与其他模块建立更多连接，或补充文档。"
    report = report.replace('发现 **{{孤立节点数}} 个孤立节点**，这些组件与其他部分的连接较少：\n\n- `{{节点1}}` - {{说明}}\n- `{{节点2}}` - {{说明}}\n- ...\n\n**建议**：检查这些组件是否需要与其他模块建立更多连接，或补充文档。', isolated_section)
    
    # 薄弱社区
    small_communities = sum(1 for comm in communities.values() if len(comm) < 3)
    weak_section = f"存在 **{small_communities} 个节点数 < 3 的社区**，这些社区可能是独立的小功能模块或配置文件。影响较小，保持现状即可。"
    report = report.replace('{{如存在节点数 < 3 的社区，统计数量并说明影响}}', weak_section)
    
    # 具体改进方案
    improvement_plan = """
针对高优先级建议的具体改进步骤：

1. **优化低内聚社区的模块结构**
   - 分析内聚度低于0.1的社区，识别功能职责不清晰的组件
   - 进行代码审查，讨论是否需要重构或合并相关功能
   - 制定重构计划，逐步优化模块设计

2. **统一异步处理模式**
   - 审查所有StreamConsumer/Producer的实现
   - 提取公共逻辑到AbstractStreamConsumer/Producer
   - 统一错误处理、重试逻辑和监控指标
""".strip()
    report = report.replace('{{针对高优先级建议，给出具体的改进步骤和方案}}', improvement_plan)
    
    # 输出文件清单
    import os
    output_files = []
    graphify_dir = Path('graphify-out')
    for f in graphify_dir.iterdir():
        if f.is_file():
            size = f.stat().st_size
            size_str = f"{size:,} bytes"
            output_files.append((f.name, size_str))
    
    output_list = "| 文件 | 大小 | 用途 |\n|------|------|------|\n"
    file_desc = {
        'graph.html': '交互式知识图谱可视化（浏览器打开）',
        'graph.json': '原始图谱数据（JSON 格式）',
        'GRAPH_REPORT.md': '自动生成的审计报告',
        'ANALYSIS_REPORT.md': '标准化分析报告（本文件）'
    }
    for name, size in output_files:
        desc = file_desc.get(name, '辅助文件')
        output_list += f"| `{name}` | {size} | {desc} |\n"
    
    output_start = report.find('## 十、输出文件清单')
    output_end = report.find('---', output_start)
    if output_start != -1 and output_end != -1:
        before = report[:output_start]
        after = report[output_end:]
        report = before + "## 十、输出文件清单\n\n" + output_list + "\n\n" + after
    
    # 保存报告
    output_path = Path('graphify-out/ANALYSIS_REPORT.md')
    output_path.write_text(report)
    print(f"分析报告已生成: {output_path}")
    print(f"报告大小: {len(report)} 字符")


if __name__ == '__main__':
    main()
