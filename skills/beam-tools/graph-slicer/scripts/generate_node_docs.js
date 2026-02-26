#!/usr/bin/env node
/**
 * Generates clean markdown documentation for each node.
 * Focuses on what matters: level, name, prompt, input/output params.
 *
 * Usage: node generate_node_docs.js <input-file>
 */

const fs = require('fs');
const path = require('path');

function extractTopology(data) {
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

  const nodeMap = new Map();
  graphNodes.forEach(node => nodeMap.set(node.id, node));

  const toolConfigMap = new Map();
  graphTools.forEach(tool => {
    if (tool.toolFunctionName) toolConfigMap.set(tool.toolFunctionName, tool);
    if (tool.toolName) toolConfigMap.set(tool.toolName, tool);
  });

  const entryNode = graphNodes.find(n => n.isEntryNode);
  if (!entryNode) throw new Error('No entry node found');

  const topology = [];
  const visited = new Set();
  const queue = [{ nodeId: entryNode.id, level: 0, branch: 0, parentBranches: [] }];
  const levelBranches = new Map();

  while (queue.length > 0) {
    const { nodeId, level, branch, parentBranches } = queue.shift();
    if (visited.has(nodeId)) continue;
    visited.add(nodeId);

    const node = nodeMap.get(nodeId);
    if (!node) continue;

    let toolName = node.objective || 'Unknown';
    let toolData = null;

    if (node.toolConfiguration?.toolFunctionName) {
      toolData = toolConfigMap.get(node.toolConfiguration.toolFunctionName);
      if (toolData?.toolName) toolName = toolData.toolName;
    }
    if (!toolData && node.objective) {
      toolData = toolConfigMap.get(node.objective);
      if (toolData?.toolName) toolName = toolData.toolName;
    }

    const levelNumber = parentBranches.length === 0 ? `${level}` : `${level}.${branch}`;

    topology.push({
      level,
      branch,
      levelNumber,
      toolName,
      toolData,
      isEntry: node.isEntryNode || false,
      childEdges: node.childEdges || []
    });

    const children = node.childEdges || [];
    if (children.length > 0) {
      if (!levelBranches.has(level + 1)) levelBranches.set(level + 1, 0);
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

  return { topology, agentInfo };
}

function generateNodeDocs(topology, agentInfo) {
  let md = `# ${agentInfo.name || 'Agent'} - Node Documentation\n\n`;
  md += `> Auto-generated node documentation\n\n`;
  md += `---\n\n`;

  topology.forEach(node => {
    if (!node.toolData) {
      // Skip entry node or nodes without tool data
      if (!node.isEntry) {
        md += `## ${node.levelNumber} - ${node.toolName}\n\n`;
        md += `*No tool data available*\n\n---\n\n`;
      }
      return;
    }

    md += `## ${node.levelNumber} - ${node.toolName}\n\n`;
    md += `**Level**: ${node.level}\n`;
    md += `**Branch**: ${node.branch}\n\n`;

    // Prompt
    if (node.toolData.prompt) {
      md += `### Prompt\n\n`;
      md += `\`\`\`\n${node.toolData.prompt}\n\`\`\`\n\n`;
    }

    // Input Params
    const inputParams = node.toolData.inputParams || [];
    if (inputParams.length > 0) {
      md += `### Input Parameters\n\n`;
      inputParams.forEach(param => {
        md += `**${param.paramName}**: ${param.paramDescription || 'No description'}\n\n`;
      });
    }

    // Output Params
    const outputParams = node.toolData.outputParams || [];
    if (outputParams.length > 0) {
      md += `### Output Parameters\n\n`;
      outputParams.forEach(param => {
        md += `**${param.paramName}**:\n`;
        md += `\`\`\`\n${param.paramDescription || 'No description'}\n\`\`\`\n\n`;
      });
    }

    md += `---\n\n`;
  });

  return md;
}

// Main
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: node generate_node_docs.js <input-file>');
    process.exit(1);
  }

  const inputFile = args[0];
  if (!fs.existsSync(inputFile)) {
    console.error(`Error: File not found: ${inputFile}`);
    process.exit(1);
  }

  try {
    const data = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
    const { topology, agentInfo } = extractTopology(data);
    const docs = generateNodeDocs(topology, agentInfo);

    const outputPath = path.join(path.dirname(inputFile), 'NODES.md');
    fs.writeFileSync(outputPath, docs);
    console.log(`Generated: NODES.md`);
    console.log(`Documented ${topology.filter(n => n.toolData).length} nodes`);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

module.exports = { generateNodeDocs };
