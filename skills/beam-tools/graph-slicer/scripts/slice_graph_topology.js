#!/usr/bin/env node
/**
 * Slices graph tools using actual graph topology (BFS traversal)
 * and generates Mermaid flowchart.
 *
 * Usage: node slice_graph_topology.js <input-file> [options]
 *
 * Options:
 *   --topology     Use level-based numbering from graph structure (default)
 *   --mermaid      Generate Mermaid flowchart (GRAPH.md)
 *   --no-slice     Only generate topology info and Mermaid, don't create tool files
 */

const fs = require('fs');
const path = require('path');

function extractTopology(data) {
  // Get graph nodes and tools
  let graphNodes, graphTools, agentInfo;

  if (Array.isArray(data) && data[0]) {
    graphNodes = data[0].graph?.nodes || [];
    graphTools = data[0].graphTools || [];
    agentInfo = data[0].agent || {};
  } else if (data['0']) {
    graphNodes = data['0'].graph?.nodes || [];
    graphTools = data['0'].graphTools || [];
    agentInfo = data['0'].agent || {};
  } else {
    graphNodes = data.graph?.nodes || [];
    graphTools = data.graphTools || [];
    agentInfo = data.agent || {};
  }

  // Build node map: nodeId -> node data
  const nodeMap = new Map();
  graphNodes.forEach(node => {
    nodeMap.set(node.id, node);
  });

  // Build tool config map: toolFunctionName -> tool data
  // The graphTools array uses toolFunctionName as the key identifier
  const toolConfigMap = new Map();
  graphTools.forEach(tool => {
    if (tool.toolFunctionName) {
      toolConfigMap.set(tool.toolFunctionName, tool);
    }
    // Also map by tool name for fallback
    if (tool.toolName) {
      toolConfigMap.set(tool.toolName, tool);
    }
  });

  // Find entry node
  const entryNode = graphNodes.find(n => n.isEntryNode);
  if (!entryNode) {
    throw new Error('No entry node found in graph');
  }

  // BFS traversal to assign levels
  const topology = [];
  const visited = new Set();
  const queue = [{ nodeId: entryNode.id, level: 0, branch: 0, parentBranches: [] }];

  // Track branches at each level
  const levelBranches = new Map();

  while (queue.length > 0) {
    const { nodeId, level, branch, parentBranches } = queue.shift();

    if (visited.has(nodeId)) continue;
    visited.add(nodeId);

    const node = nodeMap.get(nodeId);
    if (!node) continue;

    // Get tool info
    let toolName = node.objective || 'Unknown';
    let toolData = null;

    // Try to find tool data by toolFunctionName from the node's embedded toolConfiguration
    if (node.toolConfiguration && node.toolConfiguration.toolFunctionName) {
      toolData = toolConfigMap.get(node.toolConfiguration.toolFunctionName);
      if (toolData && toolData.toolName) {
        toolName = toolData.toolName;
      }
    }
    // Fallback: try matching by objective/tool name
    if (!toolData && node.objective) {
      toolData = toolConfigMap.get(node.objective);
      if (toolData && toolData.toolName) {
        toolName = toolData.toolName;
      }
    }

    // Determine level numbering
    let levelNumber;
    if (parentBranches.length === 0) {
      levelNumber = `${level}`;
    } else {
      levelNumber = `${level}.${branch}`;
    }

    topology.push({
      nodeId: node.id,
      toolConfigId: node.agentToolConfigurationId,
      toolName: toolName,
      objective: node.objective,
      level: level,
      branch: branch,
      levelNumber: levelNumber,
      isEntry: node.isEntryNode || false,
      isExit: node.isExitNode || false,
      onError: node.onError || 'STOP',
      evaluationCriteria: node.evaluationCriteria || [],
      createdAt: node.createdAt,
      updatedAt: node.updatedAt,
      childEdges: node.childEdges || [],
      toolData: toolData
    });

    // Process children
    const children = node.childEdges || [];
    if (children.length > 0) {
      // Track branch count at next level
      if (!levelBranches.has(level + 1)) {
        levelBranches.set(level + 1, 0);
      }

      children.forEach((edge, idx) => {
        if (!visited.has(edge.targetAgentGraphNodeId)) {
          const childBranch = children.length > 1
            ? levelBranches.get(level + 1) + idx + 1
            : branch;

          queue.push({
            nodeId: edge.targetAgentGraphNodeId,
            level: level + 1,
            branch: childBranch,
            parentBranches: children.length > 1 ? [...parentBranches, level] : parentBranches
          });
        }
      });

      if (children.length > 1) {
        levelBranches.set(level + 1, levelBranches.get(level + 1) + children.length);
      }
    }
  }

  return { topology, agentInfo, graphTools };
}

function generateMermaid(topology, agentInfo) {
  let mermaid = `# ${agentInfo.name || 'Agent'} - Graph Flow\n\n`;
  mermaid += `> **Agent ID**: ${agentInfo.id || 'N/A'}\n`;
  mermaid += `> **Created**: ${agentInfo.createdAt ? agentInfo.createdAt.split('T')[0] : 'N/A'}\n`;
  mermaid += `> **Last Updated**: ${agentInfo.updatedAt ? agentInfo.updatedAt.split('T')[0] : 'N/A'}\n`;
  mermaid += `> **Auto-generated from graph topology**\n\n`;

  // Agent description if available
  if (agentInfo.description) {
    mermaid += `## Description\n\n${agentInfo.description}\n\n`;
  }

  mermaid += '## Flow Diagram\n\n';
  mermaid += '```mermaid\nflowchart TD\n';

  // Add styling classes
  mermaid += '    classDef entry fill:#90EE90,stroke:#228B22,stroke-width:3px\n';
  mermaid += '    classDef exit fill:#FFB6C1,stroke:#DC143C,stroke-width:3px\n';
  mermaid += '    classDef router fill:#87CEEB,stroke:#4169E1,stroke-width:2px\n';
  mermaid += '    classDef processor fill:#FFF8DC,stroke:#DAA520,stroke-width:2px\n\n';

  // Add nodes with styling
  topology.forEach(node => {
    const safeName = node.toolName.replace(/[^a-zA-Z0-9]/g, '_');
    const displayName = node.toolName.replace(/"/g, '\\"');
    const hasMultipleBranches = node.childEdges.length > 1;

    if (node.isEntry) {
      mermaid += `    ${safeName}[("${node.levelNumber}<br/>Entry")]:::entry\n`;
    } else if (node.isExit || node.childEdges.length === 0) {
      mermaid += `    ${safeName}(["${node.levelNumber}<br/>${displayName}"]):::exit\n`;
    } else if (hasMultipleBranches) {
      mermaid += `    ${safeName}{"${node.levelNumber}<br/>${displayName}"}:::router\n`;
    } else {
      mermaid += `    ${safeName}["${node.levelNumber}<br/>${displayName}"]:::processor\n`;
    }
  });

  mermaid += '\n';

  // Add edges with conditions and names
  topology.forEach(node => {
    const sourceName = node.toolName.replace(/[^a-zA-Z0-9]/g, '_');

    node.childEdges.forEach(edge => {
      const targetNode = topology.find(n => n.nodeId === edge.targetAgentGraphNodeId);
      if (targetNode) {
        const targetName = targetNode.toolName.replace(/[^a-zA-Z0-9]/g, '_');

        // Prefer edge name over condition for readability
        let label = '';
        if (edge.name && edge.name.trim()) {
          label = edge.name.trim().substring(0, 40);
        } else if (edge.condition && edge.condition.trim()) {
          label = edge.condition.trim().substring(0, 40);
        }

        if (label) {
          // Escape special characters for Mermaid
          label = label.replace(/"/g, "'").replace(/\|/g, '/');
          mermaid += `    ${sourceName} -->|"${label}"| ${targetName}\n`;
        } else {
          mermaid += `    ${sourceName} --> ${targetName}\n`;
        }
      }
    });
  });

  mermaid += '```\n\n';

  // Add detailed topology table
  mermaid += '## Node Details\n\n';
  mermaid += '| Level | Tool Name | Objective | Branches | On Error | Exit |\n';
  mermaid += '|-------|-----------|-----------|----------|----------|------|\n';

  topology.forEach(node => {
    const branches = node.childEdges.length;
    const isExit = node.isExit || branches === 0 ? '✅' : '';
    const objective = (node.objective || node.toolName).substring(0, 30);
    const onError = node.onError || 'N/A';
    mermaid += `| ${node.levelNumber} | ${node.toolName} | ${objective} | ${branches} | ${onError} | ${isExit} |\n`;
  });

  mermaid += '\n';

  // Add routing conditions section
  const routingNodes = topology.filter(n => n.childEdges.length > 1);
  if (routingNodes.length > 0) {
    mermaid += '## Routing Conditions\n\n';
    routingNodes.forEach(node => {
      mermaid += `### ${node.levelNumber} - ${node.toolName}\n\n`;
      node.childEdges.forEach((edge, idx) => {
        const targetNode = topology.find(n => n.nodeId === edge.targetAgentGraphNodeId);
        const targetName = targetNode ? targetNode.toolName : 'Unknown';
        const edgeName = edge.name || `Branch ${idx + 1}`;
        const condition = edge.condition || 'No condition';
        mermaid += `**${edgeName}** → ${targetName}\n`;
        mermaid += `\`\`\`\n${condition}\n\`\`\`\n\n`;
      });
    });
  }

  // Add statistics
  mermaid += '## Statistics\n\n';
  const exitNodes = topology.filter(n => n.isExit || n.childEdges.length === 0);
  const routerCount = topology.filter(n => n.childEdges.length > 1).length;
  const maxDepth = Math.max(...topology.map(n => n.level));

  mermaid += `- **Total Nodes**: ${topology.length}\n`;
  mermaid += `- **Entry Points**: 1\n`;
  mermaid += `- **Exit Points**: ${exitNodes.length}\n`;
  mermaid += `- **Decision Points (Routers)**: ${routerCount}\n`;
  mermaid += `- **Max Depth**: ${maxDepth} levels\n`;
  mermaid += `- **Total Branches**: ${topology.reduce((sum, n) => sum + n.childEdges.length, 0)}\n`;

  return mermaid;
}

function sliceWithTopology(inputFile, options = {}) {
  const { generateMermaidFile = true, sliceFiles = true } = options;

  const data = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
  const { topology, agentInfo, graphTools } = extractTopology(data);

  const outputDir = path.dirname(inputFile);
  const createdFiles = [];

  // Create tool files with topology-based naming
  if (sliceFiles) {
    topology.forEach(node => {
      if (!node.toolData) {
        // Skip entry node or nodes without tool data
        if (!node.isEntry) {
          console.warn(`Warning: No tool data for ${node.toolName}, skipping file creation`);
        }
        return;
      }

      const fileName = `${node.levelNumber}-${node.toolName}.json`;
      const filePath = path.join(outputDir, fileName);

      // Find parent nodes (nodes that have edges pointing to this node)
      const parentNodes = topology.filter(n =>
        n.childEdges.some(e => e.targetAgentGraphNodeId === node.nodeId)
      );

      // Get incoming edges with conditions
      const incomingEdges = [];
      parentNodes.forEach(parent => {
        parent.childEdges.forEach(edge => {
          if (edge.targetAgentGraphNodeId === node.nodeId) {
            incomingEdges.push({
              fromNode: parent.toolName,
              fromLevel: parent.levelNumber,
              condition: edge.condition || '',
              edgeName: edge.name || ''
            });
          }
        });
      });

      // Get outgoing edges with target info
      const outgoingEdges = node.childEdges.map(edge => {
        const targetNode = topology.find(n => n.nodeId === edge.targetAgentGraphNodeId);
        return {
          toNode: targetNode ? targetNode.toolName : 'Unknown',
          toLevel: targetNode ? targetNode.levelNumber : 'N/A',
          condition: edge.condition || '',
          edgeName: edge.name || ''
        };
      });

      // Add comprehensive topology metadata to the tool data
      const enrichedTool = {
        _topology: {
          level: node.level,
          branch: node.branch,
          levelNumber: node.levelNumber,
          nodeId: node.nodeId,
          objective: node.objective,
          onError: node.onError,
          evaluationCriteria: node.evaluationCriteria,
          isExitNode: node.isExit || node.childEdges.length === 0,
          nodeCreatedAt: node.createdAt,
          nodeUpdatedAt: node.updatedAt,
          incomingEdges: incomingEdges,
          outgoingEdges: outgoingEdges,
          totalIncoming: incomingEdges.length,
          totalOutgoing: outgoingEdges.length
        },
        ...node.toolData
      };

      fs.writeFileSync(filePath, JSON.stringify(enrichedTool, null, 2));
      createdFiles.push(fileName);
      console.log(`Created: ${fileName}`);
    });

    console.log(`\nTotal tool files created: ${createdFiles.length}`);
  }

  // Generate Mermaid flowchart
  if (generateMermaidFile) {
    const mermaidContent = generateMermaid(topology, agentInfo);
    const mermaidPath = path.join(outputDir, 'GRAPH.md');
    fs.writeFileSync(mermaidPath, mermaidContent);
    console.log(`\nGenerated: GRAPH.md (Mermaid flowchart)`);
  }

  // Print topology summary
  console.log('\n=== TOPOLOGY SUMMARY ===');
  topology.forEach(node => {
    const indent = '  '.repeat(node.level);
    const branches = node.childEdges.length;
    const branchInfo = branches > 0 ? ` (${branches} branches)` : ' [EXIT]';
    console.log(`${indent}${node.levelNumber} - ${node.toolName}${branchInfo}`);
  });

  return { topology, createdFiles };
}

// Main execution
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error('Usage: node slice_graph_topology.js <input-file> [--mermaid] [--no-slice]');
    process.exit(1);
  }

  const inputFile = args[0];
  const generateMermaidFile = args.includes('--mermaid') || !args.includes('--no-mermaid');
  const sliceFiles = !args.includes('--no-slice');

  if (!fs.existsSync(inputFile)) {
    console.error(`Error: File not found: ${inputFile}`);
    process.exit(1);
  }

  try {
    sliceWithTopology(inputFile, { generateMermaidFile, sliceFiles });
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

module.exports = { sliceWithTopology, extractTopology, generateMermaid };
