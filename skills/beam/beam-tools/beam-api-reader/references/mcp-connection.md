# MCP Connection

Beam AI provides a Model Context Protocol (MCP) server for tool-based integration.

## MCP Server

**URL:** `https://api.beamstudio.ai/mcp`
**Transport:** Streamable HTTP
**Auth Header:** `x-api-key: YOUR_API_KEY`

## Available MCP Tools

### User Management
| Tool | Description |
|------|-------------|
| `getCurrentUser` | Get authenticated user profile |

### Agent Management
| Tool | Description |
|------|-------------|
| `listAgents` | List agents in workspace |
| `downloadContextFile` | Download agent context file |

### Agent Configuration
| Tool | Description |
|------|-------------|
| `getAgentGraph` | Get agent workflow graph |
| `testGraphNode` | Test a specific node |
| `getTaskNodesByTool` | Get task nodes by tool function |

### Task Operations
| Tool | Description |
|------|-------------|
| `createAgentTask` | Create a new task |
| `listAgentTasks` | List tasks with filters |
| `getTaskDetails` | Get task execution details |
| `getTaskUpdates` | Subscribe to task updates |

### Task Execution Control
| Tool | Description |
|------|-------------|
| `submitUserInput` | Provide input for paused tasks |
| `approveTaskExecution` | Approve tasks requiring consent |
| `rejectTaskExecution` | Reject task execution |
| `retryTaskExecution` | Retry failed tasks |

### Analytics & Optimization
| Tool | Description |
|------|-------------|
| `getAgentAnalytics` | Get performance metrics |
| `rateTaskOutput` | Rate task output quality |
| `optimizeTool` | Optimize tool configurations |
| `getToolOptimizationStatus` | Check optimization progress |
