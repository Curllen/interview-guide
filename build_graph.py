#!/usr/bin/env python3
import json
import networkx as nx
from pathlib import Path
import sys
from collections import defaultdict, Counter
from itertools import groupby


def build_graph_from_ast():
    # 加载AST提取的结果
    ast_data = json.load(Path('.graphify_ast.json').open())
    
    # 构建图
    G = nx.DiGraph()
    
    # 添加节点
    for node in ast_data['nodes']:
        G.add_node(
            node['id'],
            label=node['label'],
            file_type=node['file_type'],
            source_file=node.get('source_file'),
            source_location=node.get('source_location')
        )
    
    # 添加边
    for edge in ast_data['edges']:
        G.add_edge(
            edge['source'],
            edge['target'],
            relation=edge.get('relation', 'references'),
            confidence=edge.get('confidence', 'EXTRACTED'),
            confidence_score=edge.get('confidence_score', 1.0),
            weight=edge.get('weight', 1.0),
            source_file=edge.get('source_file')
        )
    
    print(f"图谱构建完成: {len(G.nodes)} 个节点, {len(G.edges)} 条边")
    return G


def detect_communities(G):
    # 使用Louvain算法进行社区检测
    try:
        import community
        G_undirected = G.to_undirected()
        partition = community.best_partition(G_undirected, random_state=42)
    except (ImportError, ModuleNotFoundError):
        # 如果没有community模块，使用更简单的算法
        from networkx.algorithms.community import greedy_modularity_communities
        G_undirected = G.to_undirected()
        communities = greedy_modularity_communities(G_undirected)
        partition = {}
        for i, comm in enumerate(communities):
            for node in comm:
                partition[node] = i
    
    communities = defaultdict(list)
    for node, comm_id in partition.items():
        communities[comm_id].append(node)
    
    print(f"社区检测完成: {len(communities)} 个社区")
    return partition, communities


def generate_meaningful_labels(G, communities):
    labels = {}
    
    # 分析每个社区，生成有意义的标签
    for comm_id, nodes in communities.items():
        # 收集节点关键词
        keywords = []
        for node in nodes:
            label = G.nodes[node].get('label', '')
            source_file = G.nodes[node].get('source_file', '')
            
            # 从标签中提取关键词
            keywords.extend(label.split())
            
            # 从源文件路径中提取模块信息
            if source_file:
                parts = Path(source_file).parts
                if 'modules' in parts:
                    idx = parts.index('modules')
                    if idx + 1 < len(parts):
                        keywords.append(parts[idx + 1])
        
        # 统计关键词频率
        counter = Counter(keywords)
        
        # 确定社区标签
        most_common = counter.most_common(5)
        
        # 根据关键词生成标签
        module_name = None
        for word, count in most_common:
            if word in ['voiceinterview', 'interview', 'resume', 'llmprovider', 'knowledgebase']:
                module_name = word
                break
        
        if module_name:
            # 检查更具体的关键词
            if 'voice' in [k.lower() for k in keywords]:
                labels[comm_id] = "Voice Interview Module"
            elif 'llm' in [k.lower() for k in keywords]:
                labels[comm_id] = "LLM Provider Configuration"
            elif 'resume' in [k.lower() for k in keywords]:
                labels[comm_id] = "Resume Analysis Module"
            elif 'knowledgebase' in [k.lower() for k in keywords]:
                labels[comm_id] = "Knowledge Base & RAG"
            elif 'interview' in [k.lower() for k in keywords]:
                labels[comm_id] = "Interview Scheduling & Management"
            else:
                labels[comm_id] = f"{module_name.capitalize()} Module"
        else:
            # 检查是否是基础设施或通用组件
            file_types = [G.nodes[n].get('file_type', '') for n in nodes]
            if 'config' in ' '.join(keywords).lower() or 'properties' in ' '.join(keywords).lower():
                labels[comm_id] = "Configuration & Properties"
            elif 'service' in ' '.join(keywords).lower():
                labels[comm_id] = "Core Services Layer"
            elif 'entity' in ' '.join(keywords).lower() or 'model' in ' '.join(keywords).lower():
                labels[comm_id] = "Data Models & Entities"
            elif 'repository' in ' '.join(keywords).lower():
                labels[comm_id] = "Data Access Layer"
            elif 'controller' in ' '.join(keywords).lower():
                labels[comm_id] = "REST API Controllers"
            elif 'test' in ' '.join(keywords).lower():
                labels[comm_id] = "Test Suite"
            elif 'util' in ' '.join(keywords).lower() or 'common' in ' '.join(keywords).lower():
                labels[comm_id] = "Common Utilities"
            elif 'redis' in ' '.join(keywords).lower() or 'cache' in ' '.join(keywords).lower():
                labels[comm_id] = "Caching & Infrastructure"
            elif 'gradle' in ' '.join(keywords).lower() or 'build' in ' '.join(keywords).lower():
                labels[comm_id] = "Build Configuration"
            else:
                labels[comm_id] = f"Component Group {comm_id + 1}"
    
    # 确保标签没有默认的"Community N"
    for comm_id in labels:
        if 'Community' in labels[comm_id] and any(str(i) in labels[comm_id] for i in range(100)):
            # 重新尝试更智能的标签
            nodes = communities[comm_id]
            file_paths = [G.nodes[n].get('source_file', '') for n in nodes]
            paths = []
            for fp in file_paths:
                if fp:
                    parts = Path(fp).parts
                    if 'main' in parts:
                        idx = parts.index('main')
                        if idx + 1 < len(parts):
                            paths.append(parts[idx + 1])
            if paths:
                common_path = Counter(paths).most_common(1)[0][0]
                labels[comm_id] = f"{common_path.capitalize()} Components"
    
    print(f"社区标签生成完成: {len(labels)} 个标签")
    return labels


def compute_cohesion_scores(G, partition):
    # 计算每个社区的凝聚度分数
    G_undirected = G.to_undirected()
    cohesion_scores = {}
    
    for comm_id in set(partition.values()):
        comm_nodes = [n for n in partition if partition[n] == comm_id]
        if len(comm_nodes) < 2:
            cohesion_scores[comm_id] = 1.0
            continue
        
        subgraph = G_undirected.subgraph(comm_nodes)
        internal_edges = len(subgraph.edges())
        
        # 计算可能的最大内部边数
        max_possible = len(comm_nodes) * (len(comm_nodes) - 1) / 2
        
        # 计算可能的外部边数（计算实际外部边数）
        external_edges = 0
        for node in comm_nodes:
            for neighbor in G_undirected.neighbors(node):
                if partition[neighbor] != comm_id:
                    external_edges += 1
        
        # 调整凝聚度分数计算方式
        if max_possible > 0:
            density = internal_edges / max_possible
            # 使用密度作为主要指标
            cohesion_scores[comm_id] = density
        else:
            cohesion_scores[comm_id] = 0.5
    
    return cohesion_scores


def generate_graph_report(G, communities, labels, cohesion_scores, detect_data):
    # 生成报告
    report_lines = []
    
    report_lines.append("# Graphify Analysis Report")
    report_lines.append("")
    
    # 统计信息
    report_lines.append("## Overview")
    report_lines.append(f"- **Nodes**: {len(G.nodes)}")
    report_lines.append(f"- **Edges**: {len(G.edges)}")
    report_lines.append(f"- **Communities**: {len(communities)}")
    report_lines.append(f"- **Files Analyzed**: {detect_data.get('total_files', 0)}")
    report_lines.append("")
    
    # God节点（度最高的节点）
    report_lines.append("## Key Nodes")
    degree_centrality = nx.degree_centrality(G)
    top_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    
    for i, (node_id, score) in enumerate(top_nodes, 1):
        label = G.nodes[node_id].get('label', node_id)
        source_file = G.nodes[node_id].get('source_file', '')
        report_lines.append(f"{i}. **{label}** (score: {score:.3f})")
        if source_file:
            report_lines.append(f"   - Source: {source_file}")
    report_lines.append("")
    
    # 社区详细信息
    report_lines.append("## Communities")
    sorted_communities = sorted(communities.items(), key=lambda x: len(x[1]), reverse=True)
    
    for i, (comm_id, nodes) in enumerate(sorted_communities, 1):
        label = labels.get(comm_id, f"Community {comm_id}")
        cohesion = cohesion_scores.get(comm_id, 0)
        report_lines.append(f"### {i}. {label} (size: {len(nodes)}, cohesion: {cohesion:.3f})")
        
        # 列出社区中最重要的节点
        comm_subgraph = G.subgraph(nodes)
        comm_degrees = dict(comm_subgraph.degree())
        top_comm_nodes = sorted(comm_degrees.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for node_id, deg in top_comm_nodes:
            node_label = G.nodes[node_id].get('label', node_id)
            report_lines.append(f"   - {node_label} (degree: {deg})")
        report_lines.append("")
    
    return '\n'.join(report_lines)


def export_html(G, partition, labels, output_path):
    # 生成HTML可视化
    import json
    
    # 准备节点数据
    nodes_data = []
    for node_id in G.nodes:
        comm_id = partition[node_id]
        nodes_data.append({
            'id': node_id,
            'label': G.nodes[node_id].get('label', node_id),
            'group': comm_id,
            'fileType': G.nodes[node_id].get('file_type', ''),
            'sourceFile': G.nodes[node_id].get('source_file', '')
        })
    
    # 准备边数据
    edges_data = []
    for u, v, attr in G.edges(data=True):
        edges_data.append({
            'source': u,
            'target': v,
            'relation': attr.get('relation', ''),
            'confidence': attr.get('confidence', '')
        })
    
    # 准备社区标签
    community_labels = {str(k): v for k, v in labels.items()}
    
    # HTML模板
    html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Graphify Analysis</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f0f2f5; }
        #container { width: 100vw; height: 100vh; display: flex; }
        #sidebar { 
            width: 320px; 
            background: white; 
            padding: 20px; 
            overflow-y: auto;
            box-shadow: 2px 0 5px rgba(0,0,0,0.1);
        }
        #graph-container { flex: 1; position: relative; }
        #network { width: 100%; height: 100%; }
        h1 { margin: 0 0 15px 0; color: #333; font-size: 22px; }
        h2 { margin: 15px 0 10px 0; color: #555; font-size: 16px; }
        .community { 
            padding: 8px 12px; 
            margin: 5px 0; 
            border-radius: 6px; 
            cursor: pointer;
            transition: background 0.2s;
        }
        .community:hover { background: #e8f4ff; }
        .legend { display: flex; align-items: center; margin: 5px 0; }
        .legend-color { width: 16px; height: 16px; border-radius: 50%; margin-right: 10px; }
        #node-info { 
            position: absolute; 
            bottom: 20px; 
            left: 20px; 
            background: white; 
            padding: 15px; 
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 300px;
            display: none;
        }
    </style>
</head>
<body>
    <div id="container">
        <div id="sidebar">
            <h1>Graph Analysis</h1>
            <div>
                <strong>Nodes:</strong> <span id="node-count">0</span>
            </div>
            <div>
                <strong>Edges:</strong> <span id="edge-count">0</span>
            </div>
            <h2>Communities</h2>
            <div id="communities"></div>
        </div>
        <div id="graph-container">
            <div id="network"></div>
            <div id="node-info"></div>
        </div>
    </div>

    <script src="https://unpkg.com/vis-network@9.1.6/dist/vis-network.min.js"></script>
    <link href="https://unpkg.com/vis-network@9.1.6/dist/vis-network.min.css" rel="stylesheet">
    
    <script>
        const nodesData = NODES_DATA;
        const edgesData = EDGES_DATA;
        const communityLabels = COMMUNITY_LABELS;
        
        // 创建节点数组
        const nodes = new vis.DataSet(nodesData.map(n => ({
            id: n.id,
            label: n.label,
            group: n.group,
            title: n.label + '\\n' + (n.sourceFile || '')
        })));
        
        // 创建边数组
        const edges = new vis.DataSet(edgesData.map(e => ({
            from: e.source,
            to: e.target,
            arrows: 'to'
        })));
        
        // 设置节点和边数量
        document.getElementById('node-count').textContent = nodes.length;
        document.getElementById('edge-count').textContent = edges.length;
        
        // 颜色映射
        const colors = [
            '#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0',
            '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8',
            '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000'
        ];
        
        // 创建社区列表
        const communitiesDiv = document.getElementById('communities');
        const groupCounts = {};
        nodesData.forEach(n => {
            const group = n.group;
            groupCounts[group] = (groupCounts[group] || 0) + 1;
        });
        
        Object.keys(groupCounts).sort((a, b) => groupCounts[b] - groupCounts[a]).forEach(group => {
            const div = document.createElement('div');
            div.className = 'community';
            const label = communityLabels[group] || 'Community ' + group;
            div.innerHTML = `<div class="legend"><div class="legend-color" style="background: ${colors[parseInt(group) % colors.length]}"></div>${label} (${groupCounts[group]})</div>`;
            communitiesDiv.appendChild(div);
        });
        
        // 创建网络
        const container = document.getElementById('network');
        const data = { nodes, edges };
        const options = {
            nodes: {
                shape: 'dot',
                size: 12,
                font: { size: 10 }
            },
            edges: {
                width: 0.5,
                smooth: true
            },
            groups: {
                useDefaultGroups: true
            },
            physics: {
                stabilization: { iterations: 100 },
                barnesHut: {
                    gravitationalConstant: -3000,
                    centralGravity: 0.3,
                    springLength: 95,
                    springConstant: 0.04
                }
            }
        };
        
        // 分配颜色到组
        for (let group in groupCounts) {
            options.groups[group] = { color: colors[parseInt(group) % colors.length] };
        }
        
        const network = new vis.Network(container, data, options);
        
        // 显示节点信息
        const nodeInfoDiv = document.getElementById('node-info');
        network.on('click', function (params) {
            if (params.nodes.length > 0) {
                const nodeId = params.nodes[0];
                const node = nodesData.find(n => n.id === nodeId);
                if (node) {
                    nodeInfoDiv.style.display = 'block';
                    nodeInfoDiv.innerHTML = '<strong>' + node.label + '</strong><br>' +
                        'Group: ' + (communityLabels[node.group] || 'Community ' + node.group) + '<br>' +
                        (node.sourceFile ? 'Source: ' + node.sourceFile : '');
                }
            } else {
                nodeInfoDiv.style.display = 'none';
            }
        });
    </script>
</body>
</html>"""
    
    # 替换占位符
    html_content = html_template.replace('NODES_DATA', json.dumps(nodes_data))
    html_content = html_content.replace('EDGES_DATA', json.dumps(edges_data))
    html_content = html_content.replace('COMMUNITY_LABELS', json.dumps(community_labels))
    
    Path(output_path).write_text(html_content)
    print(f"HTML可视化已导出到 {output_path}")


def main():
    # 1. 构建图谱
    print("步骤 1: 构建图谱...")
    G = build_graph_from_ast()
    
    # 2. 社区检测
    print("步骤 2: 检测社区...")
    partition, communities = detect_communities(G)
    
    # 3. 生成有意义的标签
    print("步骤 3: 生成社区标签...")
    labels = generate_meaningful_labels(G, communities)
    
    # 验证没有"Community N"标签
    for comm_id, label in labels.items():
        if 'Community' in label and any(str(i) in label for i in range(100)):
            print(f"警告: 社区 {comm_id} 的标签 '{label}' 包含默认格式")
    
    # 4. 计算凝聚度分数
    print("步骤 4: 计算社区凝聚度...")
    cohesion_scores = compute_cohesion_scores(G, partition)
    
    # 5. 加载检测数据
    print("步骤 5: 加载检测数据...")
    detect_data = json.load(Path('.graphify_detect.json').open())
    
    # 6. 生成报告
    print("步骤 6: 生成报告...")
    report = generate_graph_report(G, communities, labels, cohesion_scores, detect_data)
    Path('graphify-out/GRAPH_REPORT.md').write_text(report)
    
    # 7. 导出 JSON
    print("步骤 7: 导出图谱数据...")
    graph_data = {
        'nodes': [dict(id=node, **G.nodes[node]) for node in G.nodes],
        'edges': [dict(source=u, target=v, **G.edges[u, v]) for u, v in G.edges],
        'communities': {str(k): v for k, v in communities.items()},
        'community_labels': {str(k): v for k, v in labels.items()}
    }
    Path('graphify-out/graph.json').write_text(json.dumps(graph_data, indent=2))
    
    # 8. 导出 HTML
    print("步骤 8: 生成 HTML 可视化...")
    export_html(G, partition, labels, 'graphify-out/graph.html')
    
    print("\nGraphify 分析完成！输出已保存到 graphify-out/")
    print("  - GRAPH_REPORT.md: 分析报告")
    print("  - graph.json: 图谱数据")
    print("  - graph.html: 可视化界面")


if __name__ == '__main__':
    main()
