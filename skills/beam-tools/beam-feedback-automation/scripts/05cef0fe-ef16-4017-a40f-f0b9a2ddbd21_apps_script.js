/**
 * Feedback Collection Script for Highlights Generation Agent - 1
 * Generated automatically by beam-feedback-automation
 * Agent ID: 05cef0fe-ef16-4017-a40f-f0b9a2ddbd21
 */

// Configuration
const CONFIG = {
  BEAM_API_KEY: PropertiesService.getScriptProperties().getProperty('BEAM_API_KEY'),
  AGENT_ID: '05cef0fe-ef16-4017-a40f-f0b9a2ddbd21',
  AGENT_NAME: 'Highlights Generation Agent - 1'
};

/**
 * Creates custom menu when spreadsheet opens
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Feedback Automation')
    .addItem('Pre-fill Agent Data', 'prefillAgentData')
    .addItem('Send Feedback Emails', 'sendFeedbackEmails')
    .addItem('Aggregate Results', 'aggregateResults')
    .addItem('Highlight Incomplete', 'highlightIncomplete')
    .addSeparator()
    .addItem('Settings', 'showSettings')
    .addToUi();
}

/**
 * Pre-fill spreadsheet with agent task data from Beam API
 */
function prefillAgentData() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const ui = SpreadsheetApp.getUi();

  // Get task count from user
  const response = ui.prompt(
    'Pre-fill Agent Data',
    'How many tasks should I fetch?',
    ui.ButtonSet.OK_CANCEL
  );

  if (response.getSelectedButton() !== ui.Button.OK) return;

  const taskCount = parseInt(response.getResponseText()) || 50;

  ui.alert(`Fetching ${taskCount} tasks from Beam API...`);

  try {
    const tasks = fetchBeamTasks(taskCount);

    if (!tasks || tasks.length === 0) {
      ui.alert('No tasks found!');
      return;
    }

    // Write tasks to sheet
    tasks.forEach((task, index) => {
      const row = index + 2; // Start from row 2 (row 1 is header)

      // Task metadata
      sheet.getRange(row, 1).setValue(task.id);
      sheet.getRange(row, 2).setValue(`https://beam.ai/task/${task.id}`);

      // Agent output data
      sheet.getRange(row, 3).setValue(task.output?.task_id || '');
      sheet.getRange(row, 4).setValue(task.output?.task_url || '');
      sheet.getRange(row, 5).setValue(task.output?.verification_status || '');
      sheet.getRange(row, 6).setValue(task.output?.comments || '');

      // Set status
      sheet.getRange(row, 11).setValue('Pending Review');
    });

    ui.alert(`✅ Successfully pre-filled ${tasks.length} tasks!`);
  } catch (error) {
    ui.alert(`❌ Error: ${error.message}`);
    Logger.log(error);
  }
}

/**
 * Fetch tasks from Beam API
 */
function fetchBeamTasks(limit = 50) {
  const url = `https://api.beam.ai/v1/task?agent_id=${CONFIG.AGENT_ID}&limit=${limit}&status=completed`;

  const options = {
    method: 'get',
    headers: {
      'Authorization': `Bearer ${CONFIG.BEAM_API_KEY}`,
      'Content-Type': 'application/json'
    },
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch(url, options);
  const data = JSON.parse(response.getContentText());

  return data.tasks || [];
}

/**
 * Send feedback request emails
 */
function sendFeedbackEmails() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const ui = SpreadsheetApp.getUi();

  // Get reviewer email
  const response = ui.prompt(
    'Send Feedback Emails',
    'Enter reviewer email address:',
    ui.ButtonSet.OK_CANCEL
  );

  if (response.getSelectedButton() !== ui.Button.OK) return;

  const reviewerEmail = response.getResponseText();

  if (!reviewerEmail || !reviewerEmail.includes('@')) {
    ui.alert('❌ Invalid email address');
    return;
  }

  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  const statusCol = headers.indexOf('Status');

  let sentCount = 0;

  // Send emails for pending reviews
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const status = row[statusCol];

    if (status === 'Pending Review') {
      const taskId = row[0];
      const taskUrl = row[1];

      try {
        sendFeedbackEmail(reviewerEmail, taskId, taskUrl, i + 1);
        sheet.getRange(i + 1, statusCol + 1).setValue('Email Sent');
        sentCount++;
      } catch (error) {
        Logger.log(`Error sending email for task ${taskId}: ${error}`);
      }
    }
  }

  ui.alert(`✅ Sent ${sentCount} feedback request emails to ${reviewerEmail}`);
}

/**
 * Send individual feedback email
 */
function sendFeedbackEmail(to, taskId, taskUrl, rowNumber) {
  const spreadsheetUrl = SpreadsheetApp.getActiveSpreadsheet().getUrl();
  const reviewLink = `${spreadsheetUrl}#gid=0&range=A${rowNumber}`;

  const subject = `Feedback Request: ${CONFIG.AGENT_NAME} - Task ${taskId}`;

  const body = `
Hi,

Please review the output from ${CONFIG.AGENT_NAME} for the following task:

Task ID: ${taskId}
Task URL: ${taskUrl}

Review Link: ${reviewLink}

Instructions:
1. Click the review link above to open the feedback sheet
2. Review the agent's output in the corresponding row
3. Fill in all feedback fields (ratings, comments, etc.)
4. Change the Status column to "Completed" when done

Thank you for your feedback!

---
This email was sent automatically by the Beam Feedback Automation system.
  `;

  GmailApp.sendEmail(to, subject, body);
}

/**
 * Aggregate feedback results
 */
function aggregateResults() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const ui = SpreadsheetApp.getUi();

  const data = sheet.getDataRange().getValues();
  const headers = data[0];

  const results = {
    totalTasks: data.length - 1,
    completedReviews: 0,
    pendingReviews: 0,
    averageScores: {},
    commonIssues: []
  };

  // Count statuses
  for (let i = 1; i < data.length; i++) {
    const status = data[i][headers.indexOf('Status')];
    if (status === 'Completed') {
      results.completedReviews++;
    } else {
      results.pendingReviews++;
    }
  }

  // No rating fields to aggregate

  // Display results
  const summary = `
📊 Feedback Results Summary

Total Tasks: ${results.totalTasks}
Completed Reviews: ${results.completedReviews}
Pending Reviews: ${results.pendingReviews}
Completion Rate: ${Math.round((results.completedReviews / results.totalTasks) * 100)}%

Average Scores:
${Object.entries(results.averageScores).map(([key, value]) => `  - ${key}: ${value.toFixed(2)}/5`).join('\n')}

Check the console (View > Logs) for detailed results.
  `;

  ui.alert(summary);
  Logger.log(JSON.stringify(results, null, 2));
}

/**
 * Highlight incomplete feedback rows
 */
function highlightIncomplete() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  const headers = data[0];

  const statusCol = headers.indexOf('Status') + 1;

  for (let i = 2; i <= data.length; i++) {
    const status = sheet.getRange(i, statusCol).getValue();

    if (status === 'Pending Review' || status === 'Email Sent') {
      sheet.getRange(i, 1, 1, headers.length).setBackground('#fff3cd'); // Light yellow
    } else if (status === 'Completed') {
      sheet.getRange(i, 1, 1, headers.length).setBackground('#d4edda'); // Light green
    }
  }

  SpreadsheetApp.getUi().alert('✅ Highlighted incomplete rows');
}

/**
 * Show settings dialog
 */
function showSettings() {
  const ui = SpreadsheetApp.getUi();
  const properties = PropertiesService.getScriptProperties();

  const currentKey = properties.getProperty('BEAM_API_KEY') || 'Not set';

  const response = ui.prompt(
    'Settings',
    `Current Beam API Key: ${currentKey.substring(0, 10)}...\n\nEnter new API key (or leave blank to keep current):`,
    ui.ButtonSet.OK_CANCEL
  );

  if (response.getSelectedButton() === ui.Button.OK) {
    const newKey = response.getResponseText();
    if (newKey && newKey.trim() !== '') {
      properties.setProperty('BEAM_API_KEY', newKey.trim());
      ui.alert('✅ API key updated!');
    }
  }
}
