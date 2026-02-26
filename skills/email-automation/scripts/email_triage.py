#!/usr/bin/env python3
"""
Email Triage Script
Fetches unread emails, classifies them, and generates action recommendations.
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path to import gmail operations
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "00-system" / "skills" / "google" / "gmail" / "scripts"))

try:
    from gmail_operations import list_emails, read_email, create_draft, archive_email, mark_read
except ImportError:
    print("⚠️  Gmail operations not found. Make sure google integration is set up.")
    print("Run: python 00-system/skills/google/google-master/scripts/google_auth.py")
    sys.exit(1)


class EmailTriageAgent:
    """AI-powered email triage agent for Inbox Zero"""
    
    def __init__(self, max_emails=50, hours_back=None):
        self.max_emails = max_emails
        self.hours_back = hours_back  # Optional - for inbox zero we process all inbox emails
        
    def fetch_inbox_emails(self):
        """Fetch emails from INBOX (Inbox Zero methodology)"""
        print(f"\n📥 Fetching emails from INBOX...")
        
        # Inbox Zero: Process everything in INBOX, regardless of read status
        query = "in:inbox"
        
        # Optional: Add date filter if specified
        if self.hours_back:
            after_date = (datetime.now() - timedelta(hours=self.hours_back)).strftime('%Y/%m/%d')
            query = f"in:inbox after:{after_date}"
        
        try:
            # Use existing Gmail operations
            email_list = list_emails(query=query, max_results=self.max_emails)
            
            if not email_list:
                print("🎉 INBOX ZERO ACHIEVED! No emails to process.")
                return []
            
            print(f"📧 Found {len(email_list)} emails in INBOX")
            
            # Fetch full message details
            emails = []
            for i, email in enumerate(email_list, 1):
                print(f"   Loading email {i}/{len(email_list)}...", end='\r')
                try:
                    full_email = read_email(email['id'])
                    emails.append(full_email)
                except Exception as e:
                    print(f"\n⚠️  Error loading email {email['id']}: {e}")
                    continue
            
            print(f"✅ Loaded {len(emails)} emails     ")
            return emails
            
        except Exception as e:
            print(f"❌ Error fetching emails: {e}")
            print("\nTry running: python 00-system/skills/google/google-master/scripts/google_auth.py")
            return []
    
    def classify_email(self, email):
        """Classify email using Inbox Zero methodology and determine action"""
        # Inbox Zero actions: RESPOND, DELEGATE (task), DEFER (snooze), DO (quick), DELETE (archive)
        
        from_addr = email['from'].lower()
        subject = email['subject'].lower()
        body = email['body'].lower()
        snippet = email.get('snippet', '').lower()
        
        # Simple heuristic classification (will be replaced with AI)
        classification = {
            'category': 'RESPOND',  # Default: needs response
            'urgency': 'medium',
            'reason': '',
            'action': 'draft_response',
            'snooze_until': None,
            'estimated_time': '5 min'  # Inbox Zero: estimate time needed
        }
        
        # 1. DELETE (Archive) - No action needed
        newsletter_signals = ['unsubscribe', 'newsletter', 'no-reply', 'noreply', 'notification']
        notification_domains = ['github.com', 'linkedin.com', 'calendar', 'notifications', 'automated']
        
        if any(sig in from_addr for sig in newsletter_signals):
            classification['category'] = 'DELETE'
            classification['action'] = 'archive'
            classification['reason'] = 'Newsletter/automated email'
            classification['estimated_time'] = '< 1 min'
            return classification
        
        if any(domain in from_addr for domain in notification_domains):
            classification['category'] = 'DELETE'
            classification['action'] = 'archive'
            classification['reason'] = 'Automated notification'
            classification['estimated_time'] = '< 1 min'
            return classification
        
        # 2. DO (Quick action < 2 min) - Simple yes/no, quick info
        quick_signals = ['yes or no', 'quick question', 'just wanted to let you know', 'fyi', 'heads up']
        if any(sig in body or sig in snippet for sig in quick_signals):
            classification['category'] = 'DO'
            classification['action'] = 'draft_response'
            classification['reason'] = 'Quick response possible'
            classification['estimated_time'] = '< 2 min'
            return classification
        
        # 3. URGENT - Needs immediate attention (today)
        urgent_keywords = ['urgent', 'asap', 'immediately', 'today', 'deadline today', 'now', 'breaking']
        client_keywords = ['issue', 'problem', 'not working', 'broken', 'down', 'error']
        
        if any(kw in subject or kw in body for kw in urgent_keywords):
            classification['category'] = 'URGENT'
            classification['urgency'] = 'high'
            classification['action'] = 'draft_response'
            classification['reason'] = 'Time-sensitive - needs response today'
            classification['estimated_time'] = '10-15 min'
            return classification
        
        if any(kw in subject or kw in body for kw in client_keywords):
            classification['category'] = 'URGENT'
            classification['urgency'] = 'high'
            classification['action'] = 'draft_response'
            classification['reason'] = 'Potential client issue'
            classification['estimated_time'] = '10-15 min'
            return classification
        
        # 4. DELEGATE - Create task for later (needs work > 20 min)
        task_keywords = ['can you', 'could you', 'please review', 'need feedback on', 'when you have time', 'at your convenience']
        if any(kw in body or kw in snippet for kw in task_keywords):
            classification['category'] = 'DELEGATE'
            classification['action'] = 'create_task'
            classification['reason'] = 'Requires focused work - create task'
            classification['estimated_time'] = '> 20 min'
            return classification
        
        # 5. DEFER (Snooze) - Important but not urgent, follow up later
        defer_keywords = ['end of week', 'next week', 'next month', 'when you can', 'no rush', 'whenever']
        future_dates = ['next monday', 'next quarter', 'q2', 'q3', 'q4']
        
        if any(kw in body or kw in snippet for kw in defer_keywords + future_dates):
            classification['category'] = 'DEFER'
            classification['action'] = 'snooze'
            classification['reason'] = 'Not urgent - can defer'
            classification['estimated_time'] = '5 min (later)'
            classification['snooze_until'] = 'Next Monday'  # Default snooze
            return classification
        
        # 6. RESPOND (Default) - Needs thoughtful response
        classification['category'] = 'RESPOND'
        classification['action'] = 'draft_response'
        classification['reason'] = 'Requires response within 2-3 days'
        classification['estimated_time'] = '5-10 min'
        return classification
    
    def draft_response(self, email, classification):
        """Generate draft response for email using Jonas's style"""
        from_addr = email['from']
        subject = email['subject']
        body = email['body']
        category = classification['category']
        
        # Extract first name from email address
        from_name = from_addr.split('<')[0].strip()
        if ',' in from_name:
            # Handle "Last, First" format
            parts = from_name.split(',')
            from_name = parts[1].strip() if len(parts) > 1 else parts[0].strip()
        else:
            # Take first word as first name
            from_name = from_name.split()[0] if from_name else "there"
        
        # Generate draft based on category using Jonas's style
        if category == 'DO':
            # Quick response
            draft = f"""Hi {from_name},

[Quick answer to your question]

Looking forward!

-Jonas"""
        
        elif category == 'URGENT':
            # Urgent response
            draft = f"""Hi {from_name},

Thanks for flagging this. Looking into it now with the team.

I'll update you by [specific time today].

-Jonas"""
        
        elif category == 'RESPOND':
            # Standard response
            draft = f"""Hi {from_name},

Thanks for reaching out!

[2-3 sentences addressing their email]

Let me know if you have any questions.

Looking forward!

-Jonas"""
        
        elif category == 'DELEGATE':
            # This will become a task, but draft acknowledgment
            draft = f"""Hi {from_name},

Got it, I'll take a look at this and get back to you by [timeframe].

Thanks!

-Jonas"""
        
        elif category == 'DEFER':
            # Acknowledge but defer
            draft = f"""Hi {from_name},

Thanks for this! I'll review and get back to you [next week/after deadline].

-Jonas"""
        
        else:
            # Default template
            draft = f"""Hi {from_name},

Thanks for your email.

[Response here]

Let me know if you have questions!

-Jonas"""
        
        # Add AI note
        draft += "\n\n---\n[AI DRAFT - Review and customize before sending]"
        draft += f"\n[Email context: {classification.get('reason', 'Standard response')}]"
        
        return draft
    
    def deduplicate_by_thread(self, emails):
        """Group emails by thread_id, return one representative per thread.
        
        Gmail API returns individual messages, not threads.
        A single conversation may have 5-15 messages.
        We pick the most recent message per thread as the representative.
        """
        from collections import defaultdict
        threads = defaultdict(list)
        for e in emails:
            tid = e.get('thread_id', e.get('id'))
            threads[tid].append(e)
        
        # Return most recent message per thread (first in list = most recent)
        unique = []
        for tid, msgs in threads.items():
            unique.append(msgs[0])
        
        if len(emails) != len(unique):
            print(f"📊 Deduplicated: {len(emails)} messages → {len(unique)} threads")
        
        return unique

    def process_emails(self):
        """Main workflow: fetch, classify, and present recommendations (Inbox Zero)"""
        emails = self.fetch_inbox_emails()
        
        if not emails:
            return
        
        # Deduplicate by thread - Gmail returns messages, not threads
        emails = self.deduplicate_by_thread(emails)
        
        print("\n🤖 Classifying emails with AI...\n")
        
        results = []
        for i, email in enumerate(emails, 1):
            print(f"   Processing {i}/{len(emails)}...", end='\r')
            classification = self.classify_email(email)
            
            draft = None
            if classification['action'] == 'draft_response':
                draft = self.draft_response(email, classification)
            
            results.append({
                'email': email,
                'classification': classification,
                'draft': draft
            })
        
        print(f"✅ Processed {len(results)} threads     \n")
        
        # Present results
        self.present_results(results)
        
        return results
    
    def present_results(self, results):
        """Present triage results in Inbox Zero format"""
        # Group by category (Inbox Zero: DO, DELEGATE, DEFER, DELETE, RESPOND)
        categories = {
            'URGENT': [],
            'DO': [],
            'RESPOND': [],
            'DELEGATE': [],
            'DEFER': [],
            'DELETE': []
        }
        
        for result in results:
            cat = result['classification']['category']
            categories.setdefault(cat, []).append(result)
        
        print("\n" + "="*70)
        print("📊 INBOX ZERO - TRIAGE RESULTS".center(70))
        print("="*70 + "\n")
        
        # Show summary in Inbox Zero priority order
        category_order = ['URGENT', 'DO', 'RESPOND', 'DELEGATE', 'DEFER', 'DELETE']
        
        for cat_name in category_order:
            cat_results = categories.get(cat_name, [])
            if not cat_results:
                continue
            
            icon = {
                'URGENT': '🔴',
                'DO': '⚡',
                'RESPOND': '💬',
                'DELEGATE': '📋',
                'DEFER': '⏰',
                'DELETE': '🗑️'
            }.get(cat_name, '📧')
            
            print(f"{icon} {cat_name} ({len(cat_results)} emails)")
            
            for result in cat_results[:5]:  # Show first 5 per category
                email = result['email']
                classification = result['classification']
                from_short = email['from'].split('<')[0].strip()[:25]
                subject_short = email['subject'][:40]
                time_est = classification.get('estimated_time', '')
                
                has_draft = "✅ DRAFT" if result['draft'] else ""
                
                print(f"   ├─ {from_short:25} | {subject_short:40} | {time_est:8} {has_draft}")
            
            if len(cat_results) > 5:
                print(f"   └─ ... and {len(cat_results) - 5} more")
            
            print()
        
        # Summary stats (Inbox Zero metrics)
        total = len(results)
        quick_actions = len(categories.get('DO', [])) + len(categories.get('DELETE', []))
        needs_response = len(categories.get('URGENT', [])) + len(categories.get('RESPOND', []))
        can_defer = len(categories.get('DELEGATE', [])) + len(categories.get('DEFER', []))
        
        print("─"*70)
        print(f"📈 INBOX ZERO SUMMARY:")
        print(f"   📧 Total in inbox: {total}")
        print(f"   ⚡ Quick wins (< 2 min): {quick_actions}")
        print(f"   💬 Need response: {needs_response}")
        print(f"   📅 Can defer: {can_defer}")
        print(f"   ⏱️  Estimated time to inbox zero: ~{sum(int(r['classification'].get('estimated_time', '5').split()[0].replace('<', '').replace('>', '')) for r in results if r['classification'].get('estimated_time', '5').split()[0].replace('<', '').replace('>', '').isdigit())} minutes")
        print("─"*70)
        
        # Save results to file
        output_file = Path(__file__).parent.parent / 'output' / f'email_triage_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump([{
                'from': r['email']['from'],
                'subject': r['email']['subject'],
                'category': r['classification']['category'],
                'action': r['classification']['action'],
                'has_draft': r['draft'] is not None
            } for r in results], f, indent=2)
        
        print(f"\n💾 Full results saved to: {output_file.name}")
        print("\n💡 INBOX ZERO WORKFLOW:")
        print("   1. ⚡ Process quick wins first (DO + DELETE) → ~5 min")
        print("   2. 🔴 Handle urgent items → respond today")
        print("   3. 💬 Draft other responses → batch process")
        print("   4. 📋 Create tasks for DELEGATE items → move to Notion")
        print("   5. ⏰ Snooze DEFER items → out of inbox")
        print("\n   Goal: Inbox Zero achieved! 🎉")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Email Triage Agent - Inbox Zero Methodology',
        epilog='Inbox Zero: Process all emails in INBOX to get to zero'
    )
    parser.add_argument('--max-emails', type=int, default=100, help='Maximum emails to process (default: 100)')
    parser.add_argument('--hours-back', type=int, default=None, help='Optional: Only process emails from last N hours')
    parser.add_argument('--test', action='store_true', help='Test mode (dry run)')
    
    args = parser.parse_args()
    
    print("="*70)
    print("📧 INBOX ZERO - Email Triage".center(70))
    print("="*70)
    
    agent = EmailTriageAgent(
        max_emails=args.max_emails,
        hours_back=args.hours_back
    )
    
    agent.process_emails()
    
    print("\n✅ Email triage complete!\n")


if __name__ == '__main__':
    main()
