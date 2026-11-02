import { useEffect, useMemo, useState } from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import './App.css'

const API_BASE = 'http://127.0.0.1:5000/api'
const sidebarItems = [
  'dashboard',
  'simulator',
  'threats',
  'phishing',
  'incident',
  'backup',
  'quiz',
  'reports',
  'profile',
  'logout',
]

const defaultDashboard = {
  welcome: 'Welcome back, Operator!',
  total_simulations_completed: 0,
  threat_awareness_score: 0,
  quiz_performance: 0,
  completed_learning_modules: 0,
  recent_activity: [],
  learning_progress: [],
  recommended_activities: [],
}

const defaultReports = {
  totalCompletedSimulations: 0,
  averageQuizScore: 0,
  moduleCompletion: 0,
  learningProgress: [],
  recentActivity: [],
}

const incidentQuestion = {
  question: 'A colleague reports an unusual login attempt and suggests you ignore it because it is a false alarm. What is the best response?',
  options: [
    'Treat it as a possible security event and report it through the approved process',
    'Delete the evidence so no one sees it',
    'Open the suspicious link for verification',
    'Wait until the system shuts down on its own',
  ],
  answer: 0,
}

function App() {
  const [token, setToken] = useState(() => localStorage.getItem('ransomware-token') || '')
  const [user, setUser] = useState(null)
  const [activeSection, setActiveSection] = useState('dashboard')
  const [authMode, setAuthMode] = useState('login')
  const [authForm, setAuthForm] = useState({ name: '', email: '', password: '' })
  const [dashboard, setDashboard] = useState(defaultDashboard)
  const [alerts, setAlerts] = useState([])
  const [scenarios, setScenarios] = useState([])
  const [emails, setEmails] = useState([])
  const [quizQuestions, setQuizQuestions] = useState([])
  const [quizResult, setQuizResult] = useState(null)
  const [reports, setReports] = useState(defaultReports)
  const [notice, setNotice] = useState({ type: '', message: '' })
  const [loading, setLoading] = useState(false)
  const [selectedAnswers, setSelectedAnswers] = useState({})
  const [selectedIncidentChoice, setSelectedIncidentChoice] = useState(null)

  const badgeColor = useMemo(
    () => [
      '#8b5cf6',
      '#a78bfa',
      '#c4b5fd',
      '#ddd6fe',
    ],
    [],
  )

  const fetchJson = async (endpoint, options = {}) => {
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
    })

    const payload = await response.json().catch(() => ({}))

    if (!response.ok) {
      throw new Error(payload.error || 'Request failed')
    }

    return payload
  }

  useEffect(() => {
    if (!token) {
      setUser(null)
      return
    }

    const loadData = async () => {
      try {
        setLoading(true)
        const [me, dashboardData, alertsData, scenariosData, emailsData, quizData, reportData] = await Promise.all([
          fetchJson('/auth/me'),
          fetchJson('/dashboard'),
          fetchJson('/threats'),
          fetchJson('/simulator/scenarios'),
          fetchJson('/phishing/emails'),
          fetchJson('/quiz/questions'),
          fetchJson('/reports'),
        ])

        setUser(me.user)
        setDashboard(dashboardData)
        setAlerts(alertsData.alerts)
        setScenarios(scenariosData.scenarios)
        setEmails(emailsData.emails)
        setQuizQuestions(quizData.questions)
        setReports(reportData)
      } catch (error) {
        setNotice({ type: 'error', message: error.message })
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [token])

  const handleAuthSubmit = async (event) => {
    event.preventDefault()

    try {
      setLoading(true)
      const endpoint = authMode === 'login' ? '/auth/login' : '/auth/register'
      const payload = await fetchJson(endpoint, {
        method: 'POST',
        body: JSON.stringify({
          name: authForm.name,
          email: authForm.email,
          password: authForm.password,
        }),
      })

      localStorage.setItem('ransomware-token', payload.token)
      localStorage.setItem('ransomware-user', JSON.stringify(payload.user))
      setToken(payload.token)
      setUser(payload.user)
      setNotice({ type: 'success', message: authMode === 'login' ? 'Login successful.' : 'Registration complete.' })
    } catch (error) {
      setNotice({ type: 'error', message: error.message })
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('ransomware-token')
    localStorage.removeItem('ransomware-user')
    setToken('')
    setUser(null)
    setActiveSection('dashboard')
    setNotice({ type: 'success', message: 'You have logged out.' })
  }

  const handleChoice = async (scenarioId, choice) => {
    try {
      setLoading(true)
      const response = await fetchJson('/simulator/complete', {
        method: 'POST',
        body: JSON.stringify({ scenarioId, choice }),
      })
      setNotice({ type: 'success', message: response.result.explanation })
      const nextDashboard = await fetchJson('/dashboard')
      setDashboard(nextDashboard)
    } catch (error) {
      setNotice({ type: 'error', message: error.message })
    } finally {
      setLoading(false)
    }
  }

  const handlePhishingEval = async (emailId, email, decision) => {
    try {
      const response = await fetchJson('/phishing/submit', {
        method: 'POST',
        body: JSON.stringify({
          emailId,
          decision,
          isSuspicious: email.isSuspicious,
        }),
      })

      setNotice({
        type: 'success',
        message: response.correct
          ? `Correct. ${email.explanation}`
          : `Review: ${email.explanation}`,
      })
    } catch (error) {
      setNotice({ type: 'error', message: error.message })
    }
  }

  const handleQuizSubmit = async () => {
    try {
      setLoading(true)
      const answers = Object.entries(selectedAnswers).map(([id, selected]) => ({ id: Number(id), selected }))
      const result = await fetchJson('/quiz/submit', {
        method: 'POST',
        body: JSON.stringify({ answers }),
      })
      setQuizResult(result)
      setNotice({ type: 'success', message: `Quiz submitted. Final score: ${result.score}%` })
      const reportData = await fetchJson('/reports')
      setReports(reportData)
    } catch (error) {
      setNotice({ type: 'error', message: error.message })
    } finally {
      setLoading(false)
    }
  }

  const syncIncidentChoice = (choice) => {
    setSelectedIncidentChoice(choice)
    setNotice({
      type: 'success',
      message: choice === 0
        ? 'Correct: reporting the suspicious activity through the approved process is the safest action.'
        : 'Review the workflow again and use the official escalation path before making a decision.',
    })
  }

  const triggerBackupRestore = async () => {
    try {
      const response = await fetchJson('/backup/restore', { method: 'POST' })
      setNotice({ type: 'success', message: response.message })
    } catch (error) {
      setNotice({ type: 'error', message: error.message })
    }
  }

  const renderStatCard = (label, value, detail) => (
    <div className="metric-card glass-card">
      <span className="metric-label">{label}</span>
      <strong className="metric-value">{value}</strong>
      <small>{detail}</small>
    </div>
  )

  if (!token) {
    return (
      <div className="auth-shell">
        <div className="auth-panel glass-card">
          <div className="auth-header">
            <span className="eyebrow">Cybersecurity training portal</span>
            <h1>RANSOMWARE AWARENESS & ETHICAL RESPONSE SIMULATOR</h1>
          </div>

          <div className="auth-toggle">
            <button
              type="button"
              className={authMode === 'login' ? 'active' : ''}
              onClick={() => setAuthMode('login')}
            >
              Login
            </button>
            <button
              type="button"
              className={authMode === 'register' ? 'active' : ''}
              onClick={() => setAuthMode('register')}
            >
              Register
            </button>
          </div>

          <form className="auth-form" onSubmit={handleAuthSubmit}>
            {authMode === 'register' && (
              <label>
                Full name
                <input
                  value={authForm.name}
                  onChange={(event) => setAuthForm({ ...authForm, name: event.target.value })}
                  placeholder="Alex Morgan"
                />
              </label>
            )}

            <label>
              Email
              <input
                type="email"
                value={authForm.email}
                onChange={(event) => setAuthForm({ ...authForm, email: event.target.value })}
                placeholder="operator@company.com"
              />
            </label>

            <label>
              Password
              <input
                type="password"
                value={authForm.password}
                onChange={(event) => setAuthForm({ ...authForm, password: event.target.value })}
                placeholder="••••••••"
              />
            </label>

            <button className="primary-btn" type="submit" disabled={loading}>
              {loading ? 'Processing...' : authMode === 'login' ? 'Log in' : 'Create account'}
            </button>
          </form>

          {notice.message && <div className={`notice ${notice.type}`}>{notice.message}</div>}
        </div>
      </div>
    )
  }

  return (
    <div className="app-shell">
      <aside className="sidebar glass-card">
        <div className="brand-block">
          <div className="brand-mark">R</div>
          <div>
            <span className="eyebrow">Cyber education</span>
            <h2>Ransomware Simulator</h2>
          </div>
        </div>

        <nav className="nav-list">
          {sidebarItems.map((item) => (
            <button
              key={item}
              type="button"
              className={`nav-item ${activeSection === item ? 'active' : ''}`}
              onClick={() => {
                if (item === 'logout') {
                  handleLogout()
                  return
                }
                setActiveSection(item)
              }}
            >
              {item === 'logout' ? 'Logout' : item.replace(/(^|\s)([a-z])/g, (_, space, char) => space + char.toUpperCase())}
            </button>
          ))}
        </nav>
      </aside>

      <main className="content-area">
        <header className="topbar glass-card">
          <div>
            <span className="eyebrow">Threat readiness</span>
            <h1>{dashboard.welcome}</h1>
          </div>
          <div className="status-pill">Status: Live training</div>
        </header>

        {notice.message && <div className={`notice ${notice.type}`}>{notice.message}</div>}

        {activeSection === 'dashboard' && (
          <section className="page-grid">
            <div className="metrics-grid">
              {renderStatCard('Total simulations completed', dashboard.total_simulations_completed, 'Learning sessions completed')}
              {renderStatCard('Threat awareness score', `${dashboard.threat_awareness_score}%`, 'Risk recognition capability')}
              {renderStatCard('Quiz performance', `${dashboard.quiz_performance}%`, 'Assessment readiness')} 
              {renderStatCard('Completed learning modules', dashboard.completed_learning_modules, 'Tracked modules')}
            </div>

            <div className="panel-grid two-up">
              <div className="glass-card chart-panel">
                <h3>Learning progress</h3>
                <div className="chart-wrap">
                  <ResponsiveContainer width="100%" height={220}>
                    <BarChart data={dashboard.learning_progress}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#3b3b67" />
                      <XAxis dataKey="label" stroke="#d4d4ff" />
                      <YAxis stroke="#d4d4ff" domain={[0, 100]} />
                      <Tooltip />
                      <Bar dataKey="value" radius={[8, 8, 0, 0]} fill="#8b5cf6" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="glass-card list-panel">
                <h3>Recent activities</h3>
                <ul className="activity-list">
                  {dashboard.recent_activity.length === 0 ? (
                    <li>No recent activity yet. Start your first simulator session.</li>
                  ) : (
                    dashboard.recent_activity.map((item, index) => (
                      <li key={`${item.title}-${index}`}>
                        <span className="dot" />
                        <div>
                          <strong>{item.title}</strong>
                          <small>{item.description}</small>
                        </div>
                      </li>
                    ))
                  )}
                </ul>
              </div>
            </div>

            <div className="panel-grid two-up">
              <div className="glass-card recommendation-panel">
                <h3>Recommended learning activities</h3>
                <ul className="recommendation-list">
                  {dashboard.recommended_activities.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="glass-card pie-panel">
                <h3>Readiness split</h3>
                <ResponsiveContainer width="100%" height={220}>
                  <PieChart>
                    <Pie dataKey="value" data={dashboard.learning_progress} innerRadius={40} outerRadius={80}>
                      {dashboard.learning_progress.map((entry, index) => (
                        <Cell key={`${entry.label}-${index}`} fill={badgeColor[index % badgeColor.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </section>
        )}

        {activeSection === 'simulator' && (
          <section className="panel-stack">
            {scenarios.map((scenario) => (
              <div key={scenario.id} className="glass-card scenario-card">
                <div className="scenario-header">
                  <h3>{scenario.title}</h3>
                  <span className="label-tag">Simulation</span>
                </div>
                <p>{scenario.summary}</p>
                <div className="warning-box">{scenario.warning}</div>
                <div className="file-list">
                  {scenario.dummyFiles.map((file) => (
                    <span key={file} className="file-tag">{file}</span>
                  ))}
                </div>
                <ul className="activity-steps">
                  {scenario.suspiciousActivity.map((activity) => (
                    <li key={activity}>{activity}</li>
                  ))}
                </ul>
                <div className="choice-grid">
                  {scenario.choices.map((choice) => (
                    <button
                      key={choice.label}
                      type="button"
                      className="choice-button"
                      onClick={() => handleChoice(scenario.id, choice)}
                    >
                      {choice.label}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </section>
        )}

        {activeSection === 'threats' && (
          <section className="panel-stack">
            <div className="glass-card info-banner">
              <strong>Educational note:</strong> These alerts are simulated examples for training and do not monitor a live operating system.
            </div>
            {alerts.map((alert) => (
              <div key={alert.id} className="glass-card threat-card">
                <div className="scenario-header">
                  <h3>{alert.title}</h3>
                  <span className={`label-tag severity-${alert.severity.toLowerCase()}`}>{alert.severity}</span>
                </div>
                <p>{alert.description}</p>
                <div className="meta-row">
                  <span>{new Date(alert.timestamp).toLocaleString()}</span>
                  <span>Simulated: {String(alert.simulated)}</span>
                </div>
                <div className="recommended-box">
                  <strong>Recommended defensive action:</strong>
                  <span>{alert.recommendedAction}</span>
                </div>
              </div>
            ))}
          </section>
        )}

        {activeSection === 'phishing' && (
          <section className="panel-stack">
            {emails.map((email) => (
              <div key={email.id} className="glass-card phishing-card">
                <div className="phishing-header">
                  <div>
                    <small>From</small>
                    <strong>{email.sender}</strong>
                  </div>
                  <span className={`label-tag ${email.isSuspicious ? 'flag-danger' : 'flag-safe'}`}>
                    {email.isSuspicious ? 'Suspicious' : 'Legitimate'}
                  </span>
                </div>
                <div className="meta-row">
                  <span><strong>Subject:</strong> {email.subject}</span>
                </div>
                <p>{email.message}</p>
                <div className="link-row">
                  <strong>Link:</strong> <a href={email.link} target="_blank" rel="noreferrer">{email.link}</a>
                </div>

                <div className="choice-grid compact">
                  <button type="button" className="choice-button" onClick={() => handlePhishingEval(email.id, email, 'suspicious')}>
                    Mark as suspicious
                  </button>
                  <button type="button" className="choice-button" onClick={() => handlePhishingEval(email.id, email, 'legitimate')}>
                    Mark as legitimate
                  </button>
                </div>

                <div className="recommended-box">
                  <strong>Explanation:</strong>
                  <span>{email.explanation}</span>
                </div>
              </div>
            ))}
          </section>
        )}

        {activeSection === 'incident' && (
          <section className="panel-stack">
            <div className="glass-card incident-panel">
              <h3>Incident response workflow</h3>
              <ol className="response-list">
                {['Identify suspicious activity', 'Stop interacting with suspicious content', 'Report through the approved channel', 'Follow authorized isolation procedures', 'Preserve relevant information', 'Contact the responsible IT/security team', 'Follow approved recovery procedures'].map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ol>
              <div className="question-block">
                <p>{incidentQuestion.question}</p>
                <div className="choice-grid stack">
                  {incidentQuestion.options.map((option, index) => (
                    <button
                      key={option}
                      type="button"
                      className={`choice-button ${selectedIncidentChoice === index ? 'selected' : ''}`}
                      onClick={() => syncIncidentChoice(index)}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </section>
        )}

        {activeSection === 'backup' && (
          <section className="panel-stack">
            <div className="glass-card backup-card">
              <h3>Virtual backup and recovery demonstration</h3>
              <div className="file-list">
                {['finance-backup.zip', 'hr-archive.tar.gz', 'research-dataset.db'].map((file) => (
                  <span key={file} className="file-tag">{file}</span>
                ))}
              </div>
              <div className="status-grid">
                <div>
                  <small>Backup status</small>
                  <strong>Healthy</strong>
                </div>
                <div>
                  <small>Last backup</small>
                  <strong>2026-11-02 02:00 UTC</strong>
                </div>
                <div>
                  <small>Retention</small>
                  <strong>30-day offline policy</strong>
                </div>
              </div>
              <button type="button" className="primary-btn" onClick={triggerBackupRestore}>Run simulated restore</button>
            </div>
          </section>
        )}

        {activeSection === 'quiz' && (
          <section className="panel-stack">
            <div className="glass-card quiz-panel">
              <h3>Cybersecurity quiz</h3>
              {quizQuestions.map((question, questionIndex) => (
                <div key={question.id} className="question-card">
                  <p>{questionIndex + 1}. {question.question}</p>
                  <div className="option-list">
                    {question.options.map((option, optionIndex) => (
                      <button
                        key={option}
                        type="button"
                        className={`option-button ${selectedAnswers[question.id] === optionIndex ? 'selected' : ''}`}
                        onClick={() => setSelectedAnswers({ ...selectedAnswers, [question.id]: optionIndex })}
                      >
                        {option}
                      </button>
                    ))}
                  </div>
                </div>
              ))}

              <button type="button" className="primary-btn" onClick={handleQuizSubmit}>
                Submit quiz
              </button>

              {quizResult && (
                <div className="quiz-result">
                  <strong>Final score:</strong> {quizResult.score}%
                </div>
              )}
            </div>
          </section>
        )}

        {activeSection === 'reports' && (
          <section className="panel-stack">
            <div className="metrics-grid">
              {renderStatCard('Total completed simulations', reports.totalCompletedSimulations, 'Recorded training sessions')}
              {renderStatCard('Average quiz score', `${reports.averageQuizScore}%`, 'Assessment trend')}
              {renderStatCard('Module completion', `${reports.moduleCompletion}%`, 'Overall learning completion')}
            </div>

            <div className="glass-card chart-panel">
              <h3>Performance trend</h3>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={reports.learningProgress}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#3b3b67" />
                  <XAxis dataKey="name" stroke="#d4d4ff" />
                  <YAxis stroke="#d4d4ff" domain={[0, 100]} />
                  <Tooltip />
                  <Bar dataKey="score" fill="#7c3aed" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </section>
        )}

        {activeSection === 'profile' && (
          <section className="panel-stack">
            <div className="glass-card profile-card">
              <h3>Profile</h3>
              <div className="profile-row">
                <span>Name</span>
                <strong>{user?.name || 'User'}</strong>
              </div>
              <div className="profile-row">
                <span>Email</span>
                <strong>{user?.email || 'unknown@example.com'}</strong>
              </div>
              <div className="profile-row">
                <span>Threat awareness</span>
                <strong>{dashboard.threat_awareness_score}%</strong>
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  )
}

export default App
