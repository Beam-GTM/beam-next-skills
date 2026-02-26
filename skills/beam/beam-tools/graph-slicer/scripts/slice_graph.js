#!/usr/bin/env node
/**
 * Unified graph slicing tool with two modes:
 * - markdown: Human-readable docs (default) - GRAPH.md + individual node .md files in nodes/
 * - json: Programmatic data - Enriched JSON files with topology metadata
 *
 * Usage:
 *   node slice_graph.js <input-file> [--markdown|--json] [--output <dir>]
 *
 * Options:
 *   --markdown        Markdown mode (default)
 *   --json           JSON mode
 *   --output <dir>   Output directory (default: same as input file)
 *
 * Note: The skill should ask the user for mode preference and output directory before calling this script.
 */

const fs = require('fs');
const path = require('path');

// ===== SHARED: Topology Extraction =====
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

  // Check if we need to use embedded toolConfiguration (when graphTools is empty)
  const useEmbeddedToolConfig = graphTools.length === 0;
  if (useEmbeddedToolConfig) {
    console.log('[INFO] No graphTools array found, using embedded toolConfiguration from nodes');
  }

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

    // Try to get toolData from graphTools map first
    if (node.toolConfiguration?.toolFunctionName) {
      toolData = toolConfigMap.get(node.toolConfiguration.toolFunctionName);
      if (toolData?.toolName) toolName = toolData.toolName;
    }
    if (!toolData && node.objective) {
      toolData = toolConfigMap.get(node.objective);
      if (toolData?.toolName) toolName = toolData.toolName;
    }

    // Fallback: Extract toolData from embedded toolConfiguration
    if (!toolData && node.toolConfiguration) {
      const tc = node.toolConfiguration;
      toolData = {
        toolName: tc.toolName || node.objective,
        toolFunctionName: tc.toolFunctionName,
        description: tc.description,
        inputParams: tc.inputParams || [],
        outputParams: tc.outputParams || [],
        // Get prompt from originalTool if available
        prompt: tc.originalTool?.prompt || null,
        // Preserve additional metadata
        integrationProviderId: tc.integrationProviderId,
        isMemoryTool: tc.isMemoryTool,
        isBackgroundTool: tc.isBackgroundTool,
        requiresConsent: tc.requiresConsent
      };
      if (tc.toolName) toolName = tc.toolName;
    }

    const levelNumber = parentBranches.length === 0 ? `${level}` : `${level}.${branch}`;

    topology.push({
      nodeId: node.id,
      level,
      branch,
      levelNumber,
      toolName,
      objective: node.objective,
      onError: node.onError || 'STOP',
      evaluationCriteria: node.evaluationCriteria || [],
      createdAt: node.createdAt,
      updatedAt: node.updatedAt,
      isEntry: node.isEntryNode || false,
      isExit: node.isExitNode || false,
      childEdges: node.childEdges || [],
      toolData
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

// ===== MODE 1: Markdown Generation =====
function generateGraphMd(topology, agentInfo) {
  let md = `# ${agentInfo.name || 'Agent'} - Graph Documentation\n\n`;
  md += `> **Auto-generated** from graph topology\n\n`;

  // High-level explanation
  md += `## Overview\n\n`;
  md += `This agent processes documents through a ${topology.length}-node workflow with topology-aware routing.\n\n`;

  const exitNodes = topology.filter(n => n.isExit || n.childEdges.length === 0);
  const routerCount = topology.filter(n => n.childEdges.length > 1).length;
  const maxDepth = Math.max(...topology.map(n => n.level));

  md += `**Statistics:**\n`;
  md += `- Total Nodes: ${topology.length}\n`;
  md += `- Max Depth: ${maxDepth} levels\n`;
  md += `- Decision Points: ${routerCount}\n`;
  md += `- Exit Points: ${exitNodes.length}\n\n`;

  // Mermaid flowchart
  md += `## Flow Diagram\n\n`;
  md += `\`\`\`mermaid\nflowchart TD\n`;
  md += `    classDef entry fill:#2d5016,stroke:#4a7c2c,stroke-width:3px,color:#fff\n`;
  md += `    classDef exit fill:#8b2252,stroke:#b8255f,stroke-width:3px,color:#fff\n`;
  md += `    classDef router fill:#1e5a8e,stroke:#2b7dc1,stroke-width:2px,color:#fff\n`;
  md += `    classDef processor fill:#6b5d0f,stroke:#9c8718,stroke-width:2px,color:#fff\n\n`;

  topology.forEach(node => {
    const safeName = node.toolName.replace(/[^a-zA-Z0-9]/g, '_');
    const displayName = node.toolName.replace(/"/g, '\\"');
    const hasMultipleBranches = node.childEdges.length > 1;

    if (node.isEntry) {
      md += `    ${safeName}[("${node.levelNumber}<br/>Entry")]:::entry\n`;
    } else if (node.isExit || node.childEdges.length === 0) {
      md += `    ${safeName}(["${node.levelNumber}<br/>${displayName}"]):::exit\n`;
    } else if (hasMultipleBranches) {
      md += `    ${safeName}{"${node.levelNumber}<br/>${displayName}"}:::router\n`;
    } else {
      md += `    ${safeName}["${node.levelNumber}<br/>${displayName}"]:::processor\n`;
    }
  });

  md += '\n';

  topology.forEach(node => {
    const sourceName = node.toolName.replace(/[^a-zA-Z0-9]/g, '_');
    node.childEdges.forEach(edge => {
      const targetNode = topology.find(n => n.nodeId === edge.targetAgentGraphNodeId);
      if (targetNode) {
        const targetName = targetNode.toolName.replace(/[^a-zA-Z0-9]/g, '_');
        let label = '';
        if (edge.name?.trim()) {
          label = edge.name.trim().substring(0, 40);
        } else if (edge.condition?.trim()) {
          label = edge.condition.trim().substring(0, 40);
        }
        if (label) {
          label = label.replace(/"/g, "'").replace(/\|/g, '/');
          md += `    ${sourceName} -->|"${label}"| ${targetName}\n`;
        } else {
          md += `    ${sourceName} --> ${targetName}\n`;
        }
      }
    });
  });

  md += `\`\`\`\n\n`;

  // Topology summary
  md += `## Topology Summary\n\n\`\`\`\n`;
  function printLevel(nodes, indent = '') {
    nodes.forEach(node => {
      const branches = node.childEdges.length;
      const branchInfo = branches > 0 ? ` (${branches} branches)` : ' [EXIT]';
      md += `${indent}${node.levelNumber} - ${node.toolName}${branchInfo}\n`;
    });
  }
  topology.forEach(node => {
    const indent = '  '.repeat(node.level);
    const branches = node.childEdges.length;
    const branchInfo = branches > 0 ? ` (${branches} branches)` : ' [EXIT]';
    md += `${indent}${node.levelNumber} - ${node.toolName}${branchInfo}\n`;
  });
  md += `\`\`\`\n\n`;

  // Node index
  md += `## Node Index\n\n`;
  topology.forEach(node => {
    if (!node.isEntry) {
      md += `- [${node.levelNumber} - ${node.toolName}](nodes/${node.levelNumber}-${node.toolName}.md)\n`;
    }
  });
  md += `\n`;

  return md;
}

function generateNodeMarkdown(node) {
  if (!node.toolData) return null;

  let md = `# ${node.levelNumber} - ${node.toolName}\n\n`;
  md += `**Level**: ${node.level}  \n`;
  md += `**Branch**: ${node.branch}  \n`;
  md += `**Tool Name**: ${node.toolName}\n\n`;

  // Description (if available)
  if (node.toolData.description) {
    md += `## Description\n\n${node.toolData.description}\n\n`;
  }

  // Input Params FIRST - with fill type aware rendering
  const inputParams = node.toolData.inputParams || [];
  if (inputParams.length > 0) {
    md += `## Input Parameters\n\n`;
    inputParams.forEach(param => {
      const fillType = param.fillType || 'unknown';
      const dataType = param.dataType ? ` \`${param.dataType}\`` : '';

      md += `**${param.paramName}**${dataType} *(${fillType})*\n\n`;

      // Handle different fill types
      if (fillType === 'static') {
        // Static: Show the actual value
        if (param.staticValue !== null && param.staticValue !== undefined) {
          let staticVal = param.staticValue;

          // Try to parse JSON strings (staticValue is sometimes stored as JSON string)
          if (typeof staticVal === 'string') {
            try {
              const parsed = JSON.parse(staticVal);
              if (typeof parsed === 'object') {
                staticVal = parsed;
              }
            } catch (e) {
              // Not JSON, keep as string
            }
          }

          if (Array.isArray(staticVal)) {
            // Handle array values (like files array with code)
            staticVal.forEach((item, idx) => {
              if (typeof item === 'object' && item.name && item.content) {
                // This is a file object (e.g., code files)
                md += `**File ${idx + 1}**: \`${item.name}\`\n\n`;
                md += `\`\`\`${getLanguageFromFilename(item.name)}\n${item.content}\n\`\`\`\n\n`;
              } else {
                // Generic array item
                md += `\`\`\`json\n${JSON.stringify(item, null, 2)}\n\`\`\`\n\n`;
              }
            });
          } else if (typeof staticVal === 'object') {
            // Object value
            md += `\`\`\`json\n${JSON.stringify(staticVal, null, 2)}\n\`\`\`\n\n`;
          } else {
            // Simple value (string, number, etc.)
            md += `**Value**: \`${staticVal}\`\n\n`;
          }
        } else {
          md += `*No static value set*\n\n`;
        }
        // Also show description if available
        if (param.paramDescription) {
          md += `> ${param.paramDescription}\n\n`;
        }
      } else if (fillType === 'linked') {
        // Linked: Show what it's linked to
        if (param.linkOutputParam) {
          const linkedParam = param.linkOutputParam;
          md += `**Linked to**: \`${linkedParam.paramName}\`\n\n`;
          if (linkedParam.paramDescription) {
            md += `> Source parameter description: ${linkedParam.paramDescription}\n\n`;
          }
          if (linkedParam.outputExample) {
            md += `**Example value**:\n\`\`\`json\n${linkedParam.outputExample}\n\`\`\`\n\n`;
          }
        } else if (param.linkParamOutputId) {
          md += `**Linked to output ID**: \`${param.linkParamOutputId}\`\n\n`;
        }
        // Also show description if available
        if (param.paramDescription) {
          md += `> ${param.paramDescription}\n\n`;
        }
      } else if (fillType === 'ai_fill') {
        // AI Fill: Show the description (instructions for AI)
        if (param.paramDescription) {
          md += `**AI Instructions**:\n\n${param.paramDescription}\n\n`;
        } else {
          md += `*No AI instructions provided*\n\n`;
        }
        // Show example if available
        if (param.outputExample) {
          md += `**Example**:\n\`\`\`\n${param.outputExample}\n\`\`\`\n\n`;
        }
      } else {
        // Unknown fill type - show what we have
        if (param.paramDescription) {
          md += `${param.paramDescription}\n\n`;
        }
        if (param.staticValue) {
          md += `**Value**: \`${JSON.stringify(param.staticValue)}\`\n\n`;
        }
      }

      md += `---\n\n`;
    });
  }

  // Prompt SECOND
  if (node.toolData.prompt) {
    md += `## Prompt\n\n`;
    md += `\`\`\`\n${node.toolData.prompt}\n\`\`\`\n\n`;
  }

  // Output Params THIRD
  const outputParams = node.toolData.outputParams || [];
  if (outputParams.length > 0) {
    md += `## Output Parameters\n\n`;
    outputParams.forEach(param => {
      const dataType = param.dataType ? ` \`${param.dataType}\`` : '';
      md += `**${param.paramName}**${dataType}: ${param.paramDescription || 'No description'}\n\n`;
      if (param.outputExample) {
        md += `**Example**:\n\`\`\`\n${param.outputExample}\n\`\`\`\n\n`;
      }
    });
  }

  return md;
}

// Helper function to get syntax highlighting language from filename
function getLanguageFromFilename(filename) {
  const ext = filename.split('.').pop().toLowerCase();
  const langMap = {
    'py': 'python',
    'js': 'javascript',
    'ts': 'typescript',
    'json': 'json',
    'md': 'markdown',
    'sh': 'bash',
    'bash': 'bash',
    'sql': 'sql',
    'html': 'html',
    'css': 'css',
    'yaml': 'yaml',
    'yml': 'yaml',
    'xml': 'xml'
  };
  return langMap[ext] || ext;
}

function generateMarkdown(inputFile, topology, agentInfo, outputDir = null) {
  const baseDir = outputDir || path.dirname(inputFile);
  const nodeDir = path.join(baseDir, 'nodes');

  // Safety check - warn if directory exists
  if (fs.existsSync(nodeDir)) {
    console.warn(`⚠️  Warning: nodes/ folder already exists at ${nodeDir}`);
    console.warn(`⚠️  Existing files may be overwritten!`);
  } else {
    fs.mkdirSync(nodeDir, { recursive: true });
    console.log(`Created: ${nodeDir}`);
  }

  // Generate GRAPH.md
  const graphMd = generateGraphMd(topology, agentInfo);
  fs.writeFileSync(path.join(nodeDir, 'GRAPH.md'), graphMd);
  console.log(`Created: nodes/GRAPH.md`);

  // Generate individual node files
  let count = 0;
  topology.forEach(node => {
    const md = generateNodeMarkdown(node);
    if (md) {
      const fileName = `${node.levelNumber}-${node.toolName}.md`;
      fs.writeFileSync(path.join(nodeDir, fileName), md);
      console.log(`Created: nodes/${fileName}`);
      count++;
    }
  });

  console.log(`\n✅ Markdown mode: Generated GRAPH.md + ${count} node files in ${nodeDir}`);
}

// ===== MODE 2: JSON Generation =====
function generateJson(inputFile, topology, outputDir = null) {
  const baseDir = outputDir || path.dirname(inputFile);
  const nodeDir = path.join(baseDir, 'nodes');

  // Safety check - warn if directory exists
  if (fs.existsSync(nodeDir)) {
    console.warn(`⚠️  Warning: nodes/ folder already exists at ${nodeDir}`);
    console.warn(`⚠️  Existing files may be overwritten!`);
  } else {
    fs.mkdirSync(nodeDir, { recursive: true });
    console.log(`Created: ${nodeDir}`);
  }

  let count = 0;
  topology.forEach(node => {
    if (!node.toolData) return;

    const parentNodes = topology.filter(n =>
      n.childEdges.some(e => e.targetAgentGraphNodeId === node.nodeId)
    );

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

    const outgoingEdges = node.childEdges.map(edge => {
      const targetNode = topology.find(n => n.nodeId === edge.targetAgentGraphNodeId);
      return {
        toNode: targetNode ? targetNode.toolName : 'Unknown',
        toLevel: targetNode ? targetNode.levelNumber : 'N/A',
        condition: edge.condition || '',
        edgeName: edge.name || ''
      };
    });

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
        incomingEdges,
        outgoingEdges,
        totalIncoming: incomingEdges.length,
        totalOutgoing: outgoingEdges.length
      },
      ...node.toolData
    };

    const fileName = `${node.levelNumber}-${node.toolName}.json`;
    fs.writeFileSync(path.join(nodeDir, fileName), JSON.stringify(enrichedTool, null, 2));
    console.log(`Created: nodes/${fileName}`);
    count++;
  });

  console.log(`\n✅ JSON mode: Generated ${count} enriched JSON files in ${nodeDir}`);
}

// ===== Main =====
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error('Usage: node slice_graph.js <input-file> [--markdown|--json] [--output <dir>]');
    process.exit(1);
  }

  const inputFile = args[0];
  if (!fs.existsSync(inputFile)) {
    console.error(`Error: File not found: ${inputFile}`);
    process.exit(1);
  }

  let mode = 'markdown'; // default
  let outputDir = null; // default: same as input file

  // Parse arguments
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--json') {
      mode = 'json';
    } else if (args[i] === '--markdown') {
      mode = 'markdown';
    } else if (args[i] === '--output' && i + 1 < args.length) {
      outputDir = args[i + 1];
      i++; // skip next arg
    }
  }

  console.log(`\nMode: ${mode}`);
  console.log(`Output: ${outputDir || path.dirname(inputFile)}/nodes/\n`);

  try {
    const data = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
    const { topology, agentInfo } = extractTopology(data);

    if (mode === 'markdown') {
      generateMarkdown(inputFile, topology, agentInfo, outputDir);
    } else {
      generateJson(inputFile, topology, outputDir);
    }
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { extractTopology, generateMarkdown, generateJson };
