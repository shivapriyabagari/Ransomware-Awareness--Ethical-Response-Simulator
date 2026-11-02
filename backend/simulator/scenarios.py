def get_scenarios():
    return [
        {
            'id': 'scenario-1',
            'title': 'Suspicious login banner',
            'summary': 'A user sees a sudden banner warning of encrypted files in a training sandbox.',
            'warning': 'Critical alert: multiple dummy files show a pending encryption routine in the simulation environment.',
            'dummyFiles': ['finance-report.docx', 'hr-records.xlsx', 'backup_manifest.txt'],
            'suspiciousActivity': ['Unexpected file access pattern', 'High CPU spike', 'Untrusted script launch'],
            'choices': [
                {
                    'label': 'Report the activity and disconnect from the sandbox',
                    'score': 100,
                    'explanation': 'This is the safest response. Reporting and isolating the environment limits impact and creates a proper incident trail.'
                },
                {
                    'label': 'Ignore it and continue working',
                    'score': 0,
                    'explanation': 'Ignoring suspicious activity can allow a threat to spread or hide additional indicators.'
                },
                {
                    'label': 'Open the suspicious file to inspect it manually',
                    'score': 15,
                    'explanation': 'Opening suspicious content without authorization can trigger malicious behavior and provide attackers more access.'
                }
            ]
        },
        {
            'id': 'scenario-2',
            'title': 'Locked training workspace',
            'summary': 'An employee finds a canvas panel showing a ransom note in a fictional cyber range.',
            'warning': 'Training message: a simulated extortion note is displayed to teach safe response habits only.',
            'dummyFiles': ['student-portfolio.pdf', 'inventory.csv', 'policy-template.md'],
            'suspiciousActivity': ['Encrypted naming pattern', 'Demand note in shared drive', 'Rapid file rename events'],
            'choices': [
                {
                    'label': 'Notify the security lead and preserve evidence',
                    'score': 100,
                    'explanation': 'Preserving evidence and reporting through the approved channel is the correct security response.'
                },
                {
                    'label': 'Attempt to reverse the lock screen on your own',
                    'score': 10,
                    'explanation': 'Unauthorized troubleshooting can destroy evidence and risk further compromise.'
                },
                {
                    'label': 'Pay the ransom demand immediately',
                    'score': 0,
                    'explanation': 'Paying does not guarantee recovery and encourages criminal behavior.'
                }
            ]
        }
    ]


def get_alerts():
    return [
        {
            'id': 'alert-1',
            'title': 'Suspicious email attachment',
            'severity': 'High',
            'description': 'A mock message contains a password-protected archive attachment with a suspicious extension.',
            'timestamp': '2026-11-02T09:15:00Z',
            'recommendedAction': 'Do not open the attachment. Submit it to the security team for review and quarantine.',
            'simulated': True
        },
        {
            'id': 'alert-2',
            'title': 'Unusual login attempt',
            'severity': 'Medium',
            'description': 'A training account attempted a sign-in from an unknown device in a different geography.',
            'timestamp': '2026-11-02T08:40:00Z',
            'recommendedAction': 'Verify the user and enforce a password reset if required.',
            'simulated': True
        },
        {
            'id': 'alert-3',
            'title': 'Unexpected file modification event',
            'severity': 'Critical',
            'description': 'A fictional file in the sandbox shows rapid renaming and changes to extension names.',
            'timestamp': '2026-11-02T07:55:00Z',
            'recommendedAction': 'Isolate the host, preserve logs, and escalate through the incident process.',
            'simulated': True
        },
        {
            'id': 'alert-4',
            'title': 'Suspicious application activity',
            'severity': 'High',
            'description': 'A dummy application attempts to access unexpected key folders in the virtual environment.',
            'timestamp': '2026-11-02T06:30:00Z',
            'recommendedAction': 'Terminate the process and review application controls with the help desk.',
            'simulated': True
        }
    ]


def get_phishing_emails():
    return [
        {
            'id': 'email-1',
            'sender': 'security@company-helpdesk.co',
            'subject': 'Action required: update your password now',
            'message': 'Urgent! Your password will expire in one hour. Please click the attached link to maintain access.',
            'link': 'https://secure-login-check.invalid',
            'isSuspicious': True,
            'explanation': 'The email uses urgency, a generic sender address, and a suspicious link to pressure the recipient into acting quickly.'
        },
        {
            'id': 'email-2',
            'sender': 'hr@yourcompany.com',
            'subject': 'Benefits enrollment reminder',
            'message': 'Please review your document package and confirm your details by Friday.',
            'link': 'https://yourcompany.com/benefits',
            'isSuspicious': False,
            'explanation': 'This is legitimate because it comes from a known domain and does not ask for immediate action outside normal business processes.'
        },
        {
            'id': 'email-3',
            'sender': 'alerts@cloud-service-update.net',
            'subject': 'Your account has been suspended',
            'message': 'Your cloud account is restricted. Sign in here to restore access immediately.',
            'link': 'https://cloudservice-update.net/login',
            'isSuspicious': True,
            'explanation': 'The sender domain is not the official service, and the message uses high-pressure language to trigger panic.'
        },
        {
            'id': 'email-4',
            'sender': 'noreply@internal-payroll.com',
            'subject': 'Payroll update',
            'message': 'Attached is the current payroll sheet for review. If you have questions, contact HR through the approved portal.',
            'link': 'https://internal-payroll.com/portal',
            'isSuspicious': True,
            'explanation': 'This email encourages opening an attachment without clear business context and uses a mismatched or unknown sender.'
        },
        {
            'id': 'email-5',
            'sender': 'it-support@company.edu',
            'subject': 'MFA enrollment required',
            'message': 'Your team must complete enrollment before security updates are applied. Follow the instructions in the secure portal.',
            'link': 'https://company.edu/security/mfa',
            'isSuspicious': False,
            'explanation': 'This is a realistic internal communication from a trusted domain, with clear context and a known security process.'
        }
    ]


def get_incident_steps():
    return [
        {'id': 1, 'title': 'Identify suspicious activity', 'description': 'Look for unusual logins, file changes, or unexpected notifications.'},
        {'id': 2, 'title': 'Stop interacting with suspicious content', 'description': 'Close the message, avoid opening attachments, and disconnect if needed.'},
        {'id': 3, 'title': 'Report through the approved channel', 'description': 'Use your organization’s official help desk or security portal.'},
        {'id': 4, 'title': 'Follow authorized isolation procedures', 'description': 'Only isolate systems using the team-approved workflow.'},
        {'id': 5, 'title': 'Preserve relevant information', 'description': 'Capture timestamps, URLs, and screenshots for the investigation team.'},
        {'id': 6, 'title': 'Contact the responsible IT/security team', 'description': 'Escalate with all information in a structured and timely manner.'},
        {'id': 7, 'title': 'Follow approved recovery procedures', 'description': 'Restore systems only after authorized validation and remediation.'}
    ]


def get_quiz_questions():
    return [
        {'id': 1, 'question': 'What is ransomware?', 'options': ['A harmless system check', 'Malicious software that encrypts files for extortion', 'A safe backup tool', 'A browser plugin'], 'answer': 1},
        {'id': 2, 'question': 'Which is the best first action when you spot a suspicious email?', 'options': ['Open the attachment to inspect it', 'Close it and report it through the approved process', 'Reply to the sender', 'Forward it to your friends'], 'answer': 1},
        {'id': 3, 'question': 'Why are backups important?', 'options': ['They increase internet speed', 'They help restore data after a disruption or attack', 'They prevent all phishing emails', 'They delete malware automatically'], 'answer': 1},
        {'id': 4, 'question': 'Which signal is a red flag?', 'options': ['Known internal sender with normal wording', 'Unexpected urgent request and suspicious link', 'Password reset from the correct portal', 'Approved software update request'], 'answer': 1},
        {'id': 5, 'question': 'What is the safest response to a suspicious incident?', 'options': ['Pay the ransom immediately', 'Disconnect from the activity and notify the security team', 'Delete all files', 'Ignore it and continue working'], 'answer': 1},
        {'id': 6, 'question': 'What should you do with a suspicious attachment?', 'options': ['Open it in a sandbox', 'Delete or quarantine it and report it', 'Send it to everyone', 'Keep it on the desktop'], 'answer': 1},
        {'id': 7, 'question': 'Which is a strong password habit?', 'options': ['Use the same password everywhere', 'Use a unique passphrase with length and complexity', 'Write it on a sticky note', 'Share it with coworkers'], 'answer': 1},
        {'id': 8, 'question': 'Why should you verify a link before clicking?', 'options': ['Because it speeds up the browser', 'Because malicious links may mimic trusted websites', 'Because all links are safe', 'Because the browser blocks all phishing'], 'answer': 1},
        {'id': 9, 'question': 'What is account lockout a sign of?', 'options': ['Routine maintenance', 'Potential suspicious access attempts', 'A good backup policy', 'An outdated browser'], 'answer': 1},
        {'id': 10, 'question': 'What does incident response focus on?', 'options': ['Avoiding all technology', 'Coordinated investigation and safe recovery', 'Creating new malware', 'Disabling all security tools'], 'answer': 1},
        {'id': 11, 'question': 'Which backup practice is recommended?', 'options': ['Keep only one copy on the same device', 'Store backups offline or in a separate protected system', 'Skip testing restoration', 'Never back up system settings'], 'answer': 1},
        {'id': 12, 'question': 'What is phishing?', 'options': ['A secure communication method', 'A deception attempt using fake messages or links', 'A file compression method', 'A password manager'], 'answer': 1},
        {'id': 13, 'question': 'Which action is appropriate when a warning mentions encrypted files?', 'options': ['Delete the device immediately', 'Confirm with your security procedure and preserve evidence', 'Click the link to learn more', 'Restart the system without reporting'], 'answer': 1},
        {'id': 14, 'question': 'Which is a good way to validate a message that appears urgent?', 'options': ['Follow the instructions immediately', 'Check the official source through a trusted communication channel', 'Click the provided link only once', 'Share the warning with everyone'], 'answer': 1},
        {'id': 15, 'question': 'Why is user awareness training important?', 'options': ['It eliminates all cyber risks', 'It helps people detect and respond to threats early', 'It reduces the need for backups', 'It blocks all malware'], 'answer': 1},
        {'id': 16, 'question': 'Which type of communication is usually least trustworthy?', 'options': ['Official corporate portal', 'Email from a known sender with a strange domain', 'A password reset via the company website', 'A scheduled security briefing'], 'answer': 1},
        {'id': 17, 'question': 'What should organizations do to recover from a major disruption?', 'options': ['Skip technical review and restore everything at once', 'Use an approved recovery plan and validated backups', 'Ignore the incident and continue business as usual', 'Pay any demand to restart service'], 'answer': 1},
        {'id': 18, 'question': 'Which behavior demonstrates good cybersecurity hygiene?', 'options': ['Using the same password across all systems', 'Verifying MFA prompts and reporting suspicious activity', 'Downloading files from unknown senders', 'Deleting logs after every issue'], 'answer': 1},
        {'id': 19, 'question': 'What is the purpose of multi-factor authentication?', 'options': ['To replace backups', 'To add another credential layer beyond a password', 'To encrypt backups', 'To generate spam emails'], 'answer': 1},
        {'id': 20, 'question': 'Which statement is true?', 'options': ['Ransomware awareness is only for IT staff', 'Awareness and preparedness reduce risk and improve response readiness', 'All suspicious files should be opened for review', 'Backup files are never useful for recovery'], 'answer': 1},
    ]
