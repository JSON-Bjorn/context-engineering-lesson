# Context Engineering Lesson - index.html & Notebook Specifications

## Document Purpose
This document provides complete specifications for the two most critical student-facing files: `index.html` (the starting point) and `notebooks/context_engineering_lesson.ipynb` (the main interactive lesson).

---

# Part 1: index.html Complete Specification

## File Overview
- **Location:** `/index.html` (project root)
- **Type:** HTML5 with embedded CSS
- **Size:** ~18-22 KB
- **Purpose:** Primary entry point and comprehensive guide
- **Design:** Clean, professional, self-contained (no external dependencies)

---

## Complete HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Context Engineering - Interactive Micro-Lesson</title>
    <style>
        /* === GLOBAL STYLES === */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: #f5f7fa;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        /* === HEADER === */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin: -40px -40px 40px -40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.95;
        }
        
        .header .meta {
            margin-top: 15px;
            font-size: 0.9em;
            opacity: 0.85;
        }
        
        /* === SECTIONS === */
        h2 {
            color: #667eea;
            font-size: 1.8em;
            margin: 30px 0 15px 0;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        
        h3 {
            color: #764ba2;
            font-size: 1.3em;
            margin: 20px 0 10px 0;
        }
        
        h4 {
            color: #555;
            font-size: 1.1em;
            margin: 15px 0 8px 0;
        }
        
        p {
            margin: 12px 0;
            font-size: 1.05em;
        }
        
        /* === CALLOUT BOXES === */
        .info-box {
            background: #e3f2fd;
            border-left: 5px solid #2196f3;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        
        .info-box.warning {
            background: #fff3cd;
            border-left-color: #ffc107;
        }
        
        .info-box.success {
            background: #d4edda;
            border-left-color: #28a745;
        }
        
        .info-box.danger {
            background: #f8d7da;
            border-left-color: #dc3545;
        }
        
        .info-box strong {
            display: block;
            margin-bottom: 8px;
            font-size: 1.1em;
        }
        
        /* === LISTS === */
        ul, ol {
            margin: 15px 0 15px 30px;
        }
        
        li {
            margin: 8px 0;
            font-size: 1.05em;
        }
        
        /* === CODE BLOCKS === */
        .code-block {
            background: #282c34;
            color: #abb2bf;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 15px 0;
            font-family: 'Courier New', Consolas, Monaco, monospace;
            font-size: 0.95em;
            line-height: 1.5;
        }
        
        code {
            background: #f4f4f4;
            padding: 3px 6px;
            border-radius: 3px;
            font-family: 'Courier New', Consolas, Monaco, monospace;
            font-size: 0.9em;
            color: #e83e8c;
        }
        
        .code-block code {
            background: transparent;
            padding: 0;
            color: #abb2bf;
        }
        
        /* === TABLES === */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 1em;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px 15px;
            text-align: left;
        }
        
        th {
            background: #667eea;
            color: white;
            font-weight: 600;
        }
        
        tr:nth-child(even) {
            background: #f8f9fa;
        }
        
        /* === BADGES === */
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-right: 8px;
        }
        
        .badge.time {
            background: #e3f2fd;
            color: #1976d2;
        }
        
        .badge.difficulty {
            background: #fff3cd;
            color: #856404;
        }
        
        /* === BUTTONS === */
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 600;
            margin: 10px 10px 10px 0;
            transition: background 0.3s;
        }
        
        .btn:hover {
            background: #5568d3;
        }
        
        /* === FOOTER === */
        .footer {
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #777;
            font-size: 0.95em;
        }
        
        /* === RESPONSIVE === */
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            
            .header {
                margin: -20px -20px 20px -20px;
                padding: 25px;
            }
            
            .header h1 {
                font-size: 1.8em;
            }
            
            h2 {
                font-size: 1.5em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1>🎯 Context Engineering</h1>
            <p>Master LLM Context Window Optimization in 30 Minutes</p>
            <div class="meta">
                <span class="badge time">⏱️ 30 minutes</span>
                <span class="badge difficulty">📊 Intermediate</span>
            </div>
        </div>

        <!-- SECTION 1: WELCOME & OVERVIEW -->
        <section id="welcome">
            <h2>📚 Welcome to Context Engineering</h2>
            <p>
                This interactive lesson teaches you the fundamentals of <strong>context engineering</strong> – 
                the art and science of optimizing how information is structured and presented to Large Language Models (LLMs).
            </p>
            
            <h3>What You'll Learn</h3>
            <ul>
                <li><strong>Context Window Mechanics:</strong> Understand token limits, counting, and budget constraints</li>
                <li><strong>The "Lost in the Middle" Problem:</strong> Why position matters in long contexts</li>
                <li><strong>Strategic Placement:</strong> Primacy, recency, and sandwich techniques</li>
                <li><strong>Optimization Methods:</strong> Compression, summarization, and dynamic allocation</li>
                <li><strong>Quantitative Comparison:</strong> Measure and prove what works best</li>
            </ul>

            <div class="info-box success">
                <strong>✅ 100% Free & Local</strong>
                This lesson runs entirely on your machine using open-source models. 
                No API keys required, no cloud costs, no data sent to external services!
            </div>

            <h3>Why Context Engineering Matters</h3>
            <p>
                As LLMs become more powerful with larger context windows (200K+ tokens), the ability to 
                strategically engineer context becomes crucial for:
            </p>
            <ul>
                <li>Building efficient RAG (Retrieval-Augmented Generation) systems</li>
                <li>Managing multi-turn conversations with memory</li>
                <li>Optimizing token usage and costs in production</li>
                <li>Improving answer quality through smart context assembly</li>
            </ul>
        </section>

        <!-- SECTION 2: PREREQUISITES -->
        <section id="prerequisites">
            <h2>⚙️ Prerequisites</h2>
            
            <h3>Required Software</h3>
            <ul>
                <li><strong>Python 3.12:</strong> Must be installed and accessible</li>
                <li><strong>uv or pip:</strong> Package manager (uv recommended for speed)</li>
                <li><strong>Git:</strong> For cloning/extracting the lesson</li>
                <li><strong>Jupyter:</strong> Installed automatically via requirements.txt</li>
            </ul>

            <h3>Hardware Requirements</h3>
            <table>
                <tr>
                    <th>Component</th>
                    <th>Minimum</th>
                    <th>Recommended</th>
                </tr>
                <tr>
                    <td>RAM</td>
                    <td>8 GB</td>
                    <td>16 GB</td>
                </tr>
                <tr>
                    <td>Disk Space</td>
                    <td>10 GB free</td>
                    <td>15 GB free</td>
                </tr>
                <tr>
                    <td>GPU</td>
                    <td>None (CPU works)</td>
                    <td>NVIDIA with 8GB+ VRAM</td>
                </tr>
                <tr>
                    <td>Internet</td>
                    <td>Required for initial model download (~7 GB)</td>
                    <td>-</td>
                </tr>
            </table>

            <div class="info-box">
                <strong>ℹ️ Model Downloads</strong>
                On first run, the lesson will automatically download:
                <ul style="margin: 10px 0 0 20px;">
                    <li>Qwen2.5-3B-Instruct (~6.5 GB) - Main LLM</li>
                    <li>all-MiniLM-L6-v2 (~80 MB) - Embedding model</li>
                </ul>
                Total: ~6.6 GB. This happens once, then everything runs offline.
            </div>

            <h3>Knowledge Prerequisites</h3>
            <ul>
                <li>Basic Python programming</li>
                <li>Familiarity with LLMs and prompting</li>
                <li>Understanding of tokens (helpful but not required)</li>
            </ul>

            <h3>Time Commitment</h3>
            <ul>
                <li><strong>Setup:</strong> 10-15 minutes (one-time)</li>
                <li><strong>Lesson:</strong> 30 minutes active work</li>
                <li><strong>Model downloads:</strong> 10-20 minutes (depends on internet speed)</li>
            </ul>
        </section>

        <!-- SECTION 3: SETUP INSTRUCTIONS -->
        <section id="setup">
            <h2>🚀 Setup Instructions</h2>
            
            <h3>Step 1: Extract the Lesson</h3>
            <div class="code-block"><code>unzip VG_[Name]_[Date].zip
cd VG_[Name]_[Date]</code></div>

            <h3>Step 2: Create Virtual Environment</h3>
            
            <h4>Linux / MacOS:</h4>
            <div class="code-block"><code># Make setup script executable
chmod +x scripts/setup_venv.sh

# Run setup script
./scripts/setup_venv.sh

# Activate the environment
source .venv/bin/activate</code></div>

            <h4>Windows:</h4>
            <div class="code-block"><code># Run setup script
scripts\setup_venv.bat

# OR manually:
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt</code></div>

            <div class="info-box warning">
                <strong>⚠️ Important: Always Activate the Environment</strong>
                Before running any lesson commands, ensure your virtual environment is activated. 
                You should see <code>(.venv)</code> in your terminal prompt.
            </div>

            <h3>Step 3: Verify Installation</h3>
            <div class="code-block"><code># Test that dependencies are installed
python -c "import transformers; import torch; print('✅ Setup successful!')"</code></div>

            <p>If you see "✅ Setup successful!" you're ready to go!</p>
        </section>

        <!-- SECTION 4: RUNNING THE LESSON -->
        <section id="running">
            <h2>▶️ Running the Lesson</h2>
            
            <h3>Quick Start (Recommended)</h3>
            <div class="code-block"><code># Make entrypoint executable
chmod +x run_lesson.sh

# Run the lesson
./run_lesson.sh</code></div>

            <p>This script will:</p>
            <ul>
                <li>✅ Check all prerequisites</li>
                <li>✅ Activate the virtual environment</li>
                <li>✅ Verify dependencies</li>
                <li>✅ Launch Jupyter Notebook</li>
            </ul>

            <h3>Manual Start (Alternative)</h3>
            <div class="code-block"><code># Activate environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Start Jupyter
jupyter notebook notebooks/context_engineering_lesson.ipynb</code></div>

            <h3>What to Expect</h3>
            <ol>
                <li>Jupyter will open in your default web browser</li>
                <li>The lesson notebook will load automatically</li>
                <li>Follow the instructions in each cell</li>
                <li>Run cells sequentially (Shift+Enter)</li>
                <li>Complete all TODO sections</li>
            </ol>

            <div class="info-box">
                <strong>💡 First Run Takes Longer</strong>
                The first time you run the lesson, models will download automatically (~6.6 GB). 
                This may take 10-20 minutes depending on your internet speed. Subsequent runs are instant!
            </div>
        </section>

        <!-- SECTION 5: LESSON FLOW -->
        <section id="flow">
            <h2>📖 Lesson Flow</h2>
            
            <p>The lesson is divided into 5 phases, each building on the previous:</p>

            <table>
                <thead>
                    <tr>
                        <th>Phase</th>
                        <th>Duration</th>
                        <th>Activities</th>
                        <th>Key Concepts</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>1. Context Windows</strong></td>
                        <td>7 min</td>
                        <td>Token counting, budget analysis</td>
                        <td>Token limits, context constraints</td>
                    </tr>
                    <tr>
                        <td><strong>2. Baseline</strong></td>
                        <td>8 min</td>
                        <td>Implement naive context assembly</td>
                        <td>Basic concatenation, metrics</td>
                    </tr>
                    <tr>
                        <td><strong>3. Strategic Placement</strong></td>
                        <td>10 min</td>
                        <td>Primacy, recency, sandwich strategies</td>
                        <td>"Lost in the middle" problem</td>
                    </tr>
                    <tr>
                        <td><strong>4. Optimization</strong></td>
                        <td>5 min</td>
                        <td>Choose and implement one optimization</td>
                        <td>Compression, summarization, allocation</td>
                    </tr>
                    <tr>
                        <td><strong>5. Evaluation</strong></td>
                        <td>Auto</td>
                        <td>Run verify.py for grading</td>
                        <td>Validation, metrics comparison</td>
                    </tr>
                </tbody>
            </table>

            <h3>Interactive Elements</h3>
            <ul>
                <li><strong>Code Implementation:</strong> Fill in TODO sections with your code</li>
                <li><strong>Experiments:</strong> Run and compare different strategies</li>
                <li><strong>Metrics Tracking:</strong> Automated measurement of your implementations</li>
                <li><strong>Hints System:</strong> Progressive hints if you get stuck</li>
                <li><strong>Visualizations:</strong> Charts comparing strategy performance</li>
            </ul>
        </section>

        <!-- SECTION 6: EVALUATION -->
        <section id="evaluation">
            <h2>✅ Evaluation & Grading</h2>
            
            <h3>How Grading Works</h3>
            <p>After completing the notebook, run the auto-grader:</p>
            <div class="code-block"><code>python src/verify.py</code></div>

            <h3>What Gets Checked</h3>
            <table>
                <thead>
                    <tr>
                        <th>Check</th>
                        <th>Requirement</th>
                        <th>Points</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Token Calculations</td>
                        <td>Within ±5% of expected values</td>
                        <td>20%</td>
                    </tr>
                    <tr>
                        <td>Naive Implementation</td>
                        <td>Function works, metrics recorded</td>
                        <td>20%</td>
                    </tr>
                    <tr>
                        <td>Strategic Placement (3)</td>
                        <td>All three strategies implemented</td>
                        <td>30%</td>
                    </tr>
                    <tr>
                        <td>Optimization</td>
                        <td>≥10% accuracy OR ≥20% token reduction</td>
                        <td>20%</td>
                    </tr>
                    <tr>
                        <td>Metrics Comparison</td>
                        <td>All data recorded properly</td>
                        <td>10%</td>
                    </tr>
                </tbody>
            </table>

            <h3>Passing Criteria</h3>
            <div class="info-box success">
                <strong>✅ To Pass:</strong>
                <ul style="margin: 10px 0 0 20px;">
                    <li>All 5 checks must pass</li>
                    <li>Total score ≥ 80%</li>
                    <li>At least one optimization shows measurable improvement</li>
                </ul>
            </div>

            <h3>Output</h3>
            <p>Results are saved to: <code>progress/lesson_progress.json</code></p>
            <p>This JSON file contains:</p>
            <ul>
                <li>Your completion status for each task</li>
                <li>Accuracy metrics for all strategies</li>
                <li>Comparison data and improvements</li>
                <li>Overall PASS/FAIL grade</li>
                <li>Timestamp and completion time</li>
            </ul>
        </section>

        <!-- SECTION 7: TROUBLESHOOTING -->
        <section id="troubleshooting">
            <h2>🔧 Troubleshooting</h2>
            
            <h3>Common Issues & Solutions</h3>

            <h4>Issue: "Python 3.12 not found"</h4>
            <div class="info-box danger">
                <strong>Error:</strong> <code>python3.12: command not found</code>
                <br><br>
                <strong>Solution:</strong> Install Python 3.12 from python.org or your package manager:
                <div class="code-block" style="margin-top: 10px;"><code># Ubuntu/Debian
sudo apt install python3.12

# MacOS (using Homebrew)
brew install python@3.12

# Windows: Download from python.org</code></div>
            </div>

            <h4>Issue: "No module named 'transformers'"</h4>
            <div class="info-box danger">
                <strong>Cause:</strong> Virtual environment not activated or dependencies not installed
                <br><br>
                <strong>Solution:</strong>
                <div class="code-block" style="margin-top: 10px;"><code># Activate environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt</code></div>
            </div>

            <h4>Issue: Models downloading too slowly</h4>
            <div class="info-box warning">
                <strong>Solution:</strong> The models download from Hugging Face Hub. If slow:
                <ul style="margin: 10px 0 0 20px;">
                    <li>Be patient - it's a one-time 6.6 GB download</li>
                    <li>Try a different network connection</li>
                    <li>Download manually and place in <code>~/.cache/huggingface/</code></li>
                </ul>
            </div>

            <h4>Issue: Out of memory during inference</h4>
            <div class="info-box warning">
                <strong>Cause:</strong> System has less than 8 GB RAM
                <br><br>
                <strong>Solutions:</strong>
                <ul style="margin: 10px 0 0 20px;">
                    <li>Close other applications</li>
                    <li>Reduce batch size in notebook (set <code>batch_size=1</code>)</li>
                    <li>Use CPU instead of GPU if GPU memory is limited</li>
                </ul>
            </div>

            <h4>Issue: Jupyter kernel not found</h4>
            <div class="info-box danger">
                <strong>Solution:</strong> Install ipykernel and register it:
                <div class="code-block" style="margin-top: 10px;"><code>pip install ipykernel
python -m ipykernel install --user --name=context_eng</code></div>
            </div>

            <h4>Issue: verify.py fails with import errors</h4>
            <div class="info-box danger">
                <strong>Cause:</strong> Running from wrong directory or venv not activated
                <br><br>
                <strong>Solution:</strong>
                <div class="code-block" style="margin-top: 10px;"><code># Make sure you're in project root
cd /path/to/VG_[Name]_[Date]

# Activate venv
source .venv/bin/activate

# Run from project root
python src/verify.py</code></div>
            </div>

            <h3>Still Having Issues?</h3>
            <p>If problems persist:</p>
            <ol>
                <li>Check that Python 3.12 is truly installed: <code>python3.12 --version</code></li>
                <li>Verify virtual environment is activated (look for <code>(.venv)</code> in prompt)</li>
                <li>Try deleting <code>.venv</code> and running setup again</li>
                <li>Ensure you have at least 10 GB free disk space</li>
                <li>Check system RAM (need at least 8 GB)</li>
            </ol>
        </section>

        <!-- SECTION 8: EXPECTED OUTCOMES -->
        <section id="outcomes">
            <h2>📊 Expected Learning Outcomes</h2>
            
            <h3>Skills You'll Master</h3>
            <ul>
                <li>Calculate token budgets for any context window size</li>
                <li>Implement strategic context placement algorithms</li>
                <li>Measure and compare context engineering approaches quantitatively</li>
                <li>Apply optimization techniques to reduce costs and improve quality</li>
                <li>Understand trade-offs between different context strategies</li>
            </ul>

            <h3>Expected Performance Results</h3>
            <table>
                <thead>
                    <tr>
                        <th>Strategy</th>
                        <th>Expected Accuracy</th>
                        <th>Improvement vs Baseline</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Naive (Baseline)</td>
                        <td>65-72%</td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td>Primacy</td>
                        <td>70-77%</td>
                        <td>+5-8%</td>
                    </tr>
                    <tr>
                        <td>Recency</td>
                        <td>75-82%</td>
                        <td>+10-15%</td>
                    </tr>
                    <tr>
                        <td>Sandwich</td>
                        <td>78-85%</td>
                        <td>+15-20%</td>
                    </tr>
                    <tr>
                        <td>Optimized</td>
                        <td>80-88%</td>
                        <td>+20-25%</td>
                    </tr>
                </tbody>
            </table>

            <p>
                <em>Note: Actual results may vary based on hardware and model loading time, 
                but relative improvements should be consistent.</em>
            </p>

            <h3>Real-World Applications</h3>
            <p>After this lesson, you'll be able to apply context engineering to:</p>
            <ul>
                <li><strong>RAG Systems:</strong> Optimize document retrieval and context assembly</li>
                <li><strong>Chatbots:</strong> Manage conversation history efficiently</li>
                <li><strong>Document Q&A:</strong> Handle long documents within token limits</li>
                <li><strong>Production LLMs:</strong> Reduce costs while maintaining quality</li>
            </ul>
        </section>

        <!-- SECTION 9: ADDITIONAL RESOURCES -->
        <section id="resources">
            <h2>📚 Additional Resources</h2>
            
            <h3>Research Papers</h3>
            <ul>
                <li>
                    <strong>"Lost in the Middle"</strong> - Liu et al., 2023
                    <br><a href="https://arxiv.org/abs/2307.03172" target="_blank">https://arxiv.org/abs/2307.03172</a>
                </li>
                <li>
                    <strong>"Extending Context Window of Large Language Models"</strong>
                    <br>Overview of techniques for context management
                </li>
            </ul>

            <h3>Documentation</h3>
            <ul>
                <li>
                    <strong>Hugging Face Transformers:</strong>
                    <a href="https://huggingface.co/docs/transformers" target="_blank">Documentation</a>
                </li>
                <li>
                    <strong>Qwen2.5 Model Card:</strong>
                    <a href="https://huggingface.co/Qwen/Qwen2.5-3B-Instruct" target="_blank">Model Details</a>
                </li>
                <li>
                    <strong>Sentence Transformers:</strong>
                    <a href="https://www.sbert.net/" target="_blank">Official Docs</a>
                </li>
            </ul>

            <h3>Further Learning</h3>
            <ul>
                <li>Anthropic's Prompt Engineering Guide</li>
                <li>OpenAI's Context Window Best Practices</li>
                <li>LangChain documentation on context management</li>
            </ul>
        </section>

        <!-- SECTION 10: LICENSE -->
        <section id="license">
            <h2>📜 License & Attribution</h2>
            
            <p>
                <strong>Lesson Content:</strong> Licensed under Apache 2.0
                <br>You are free to use, modify, and distribute this lesson with attribution.
            </p>

            <p>
                <strong>Models Used:</strong>
            </p>
            <ul>
                <li>Qwen2.5-3B-Instruct: Apache 2.0 (Alibaba Cloud)</li>
                <li>all-MiniLM-L6-v2: Apache 2.0 (Sentence Transformers)</li>
            </ul>

            <p>See <code>DATA_LICENSES.md</code> for complete third-party license information.</p>
        </section>

        <!-- FOOTER -->
        <div class="footer">
            <p><strong>Context Engineering Interactive Micro-Lesson</strong></p>
            <p>Version 1.0 | Apache 2.0 License | 2025</p>
            <p>🎓 Built for AI Engineering students</p>
        </div>
    </div>
</body>
</html>
```

---

## HTML Design Requirements

### Visual Hierarchy
1. **Header:** Gradient background, centered, clear lesson title
2. **Sections:** Clear H2 headers with colored bottom borders
3. **Info Boxes:** Color-coded (blue=info, yellow=warning, green=success, red=danger)
4. **Code Blocks:** Dark theme with syntax highlighting
5. **Tables:** Striped rows, colored headers
6. **Responsive:** Works on mobile and desktop

### Accessibility
- Semantic HTML5 elements
- Sufficient color contrast (WCAG AA)
- Clear font sizing (min 16px body)
- Descriptive link text
- Alt text where applicable

---

# Part 2: Jupyter Notebook Complete Specification

## File Overview
- **Location:** `/notebooks/context_engineering_lesson.ipynb`
- **Type:** Jupyter Notebook (.ipynb)
- **Size:** ~50-80 KB (JSON format)
- **Purpose:** Main interactive lesson content
- **Kernel:** Python 3.12
- **Estimated Cells:** ~40-50 cells

---

## Notebook Structure Overview

```
Cell Type Legend:
[M] = Markdown cell
[C] = Code cell
[T] = TODO cell (student implements)
```

### Complete Cell-by-Cell Structure

```
Cells 1-5:   Introduction & Setup
Cells 6-10:  Phase 1 - Context Windows (Theory + Practice)
Cells 11-18: Phase 2 - Baseline Implementation
Cells 19-32: Phase 3 - Strategic Placement (3 strategies)
Cells 33-40: Phase 4 - Optimization Challenge
Cells 41-45: Phase 5 - Results & Comparison
Cells 46-48: Next Steps & Verification
```

---

## Detailed Cell Specifications

### Section 1: Introduction (Cells 1-5)

#### Cell 1 [M]: Title & Welcome
```markdown
# 🎯 Context Engineering: Optimizing LLM Context Windows

Welcome to this interactive lesson! You'll learn how to strategically structure and optimize context for Large Language Models.

**Duration:** ~30 minutes  
**Difficulty:** Intermediate  
**Approach:** 100% local, no API costs

---

## What You'll Build

By the end of this lesson, you will:
- ✅ Understand token budgets and context constraints
- ✅ Implement 4 different context assembly strategies
- ✅ Measure and compare their performance quantitatively
- ✅ Apply optimization techniques to improve quality or reduce costs

**Let's get started!** 🚀
```

#### Cell 2 [C]: Imports & Setup
```python
# Cell 2: Import required libraries
import os
import json
import warnings
from pathlib import Path

import torch
import numpy as np
import pandas as pd
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Import lesson modules
import sys
sys.path.append('../src')

from token_manager import count_tokens, fits_in_budget, TokenBudgetManager
from helpers import load_documents, load_questions, calculate_similarity
from evaluation import evaluate_answer, LLMEvaluator

print("✅ All imports successful!")
print(f"📊 PyTorch version: {torch.__version__}")
print(f"🖥️  Device available: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
```

#### Cell 3 [C]: Load Models (First Run Downloads)
```python
# Cell 3: Load models (this will download on first run)
print("Loading models... (first run downloads ~6.6 GB, please be patient)")
print("Subsequent runs will be instant.\n")

from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer

# Load LLM for generation
MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
print(f"Loading {MODEL_NAME}...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)
print("✅ LLM loaded!")

# Load embedding model for similarity
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
print(f"\nLoading {EMBED_MODEL}...")
embedder = SentenceTransformer(EMBED_MODEL)
print("✅ Embedding model loaded!")

print("\n🎉 All models ready! Let's start learning.")
```

#### Cell 4 [C]: Load Data
```python
# Cell 4: Load lesson data
print("Loading lesson data...")

# Load documents
documents = load_documents('../data/source_documents.json')
print(f"✅ Loaded {len(documents)} documents")

# Load evaluation questions
questions = load_questions('../data/evaluation_questions.json')
print(f"✅ Loaded {len(questions)} evaluation questions")

# Preview first document
print("\n📄 Sample Document:")
print(f"Title: {documents[0]['title']}")
print(f"Tokens: {documents[0]['tokens']}")
print(f"Preview: {documents[0]['content'][:200]}...")
```

#### Cell 5 [M]: Lesson Roadmap
```markdown
---

## 📋 Lesson Roadmap

### Phase 1: Understanding Context Windows (7 min)
Learn about token limits and budget constraints

### Phase 2: Baseline Implementation (8 min)
Build a naive context assembly function

### Phase 3: Strategic Placement (10 min)
Implement and compare three placement strategies:
- **Primacy:** Important info at the start
- **Recency:** Important info at the end
- **Sandwich:** Important info at both ends

### Phase 4: Optimization (5 min)
Choose and implement one advanced optimization

### Phase 5: Results & Evaluation
Compare all strategies and see your improvements!

---

**Ready? Let's dive into Phase 1!** ⬇️
```

---

### Section 2: Phase 1 - Context Windows (Cells 6-10)

#### Cell 6 [M]: Phase 1 Introduction
```markdown
# Phase 1: Understanding Context Windows (7 minutes)

## What is a Context Window?

A **context window** is the maximum amount of text (measured in tokens) that an LLM can process at once. This includes:
- Your prompt/instructions
- Any retrieved documents or context
- The user's question
- The model's response

## Why Does This Matter?

Every token costs:
- **Money:** API providers charge per token
- **Time:** More tokens = slower inference
- **Attention:** Models struggle with very long contexts ("lost in the middle")

## Your Challenge

You have 10 documents and need to answer questions about them. But they don't all fit in the context window at once!

**Let's see what we're working with...**
```

#### Cell 7 [C]: Token Analysis
```python
# Cell 7: Analyze token counts
print("📊 Document Token Analysis\n")

# Calculate statistics
total_tokens = sum(doc['tokens'] for doc in documents)
avg_tokens = total_tokens / len(documents)
min_tokens = min(doc['tokens'] for doc in documents)
max_tokens = max(doc['tokens'] for doc in documents)

print(f"Total tokens across all documents: {total_tokens:,}")
print(f"Average tokens per document: {avg_tokens:.0f}")
print(f"Smallest document: {min_tokens} tokens")
print(f"Largest document: {max_tokens} tokens")

# Visualize distribution
token_counts = [doc['tokens'] for doc in documents]
plt.figure(figsize=(10, 5))
plt.bar(range(len(token_counts)), token_counts, color='steelblue', alpha=0.7)
plt.xlabel('Document Index')
plt.ylabel('Token Count')
plt.title('Token Distribution Across Documents')
plt.axhline(y=avg_tokens, color='r', linestyle='--', label=f'Average ({avg_tokens:.0f})')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print(f"\n💡 Key Insight: All documents together = {total_tokens:,} tokens")
print("    Most LLMs have 4K-8K token windows. We need to be selective!")
```

#### Cell 8 [M]: Token Budget Exercise
```markdown
## 🧮 Exercise: What Fits in Different Windows?

Given our total of ~8,500 tokens across all documents, let's see what fits in common context window sizes.

Remember: You also need room for:
- The question (~50 tokens)
- The response (~200 tokens)
- System instructions (~50 tokens)

So subtract ~300 tokens from each window for overhead!
```

#### Cell 9 [T]: TODO - Calculate Fits
```python
# Cell 9: TODO - Calculate what fits in different windows
# This is your first coding task!

def calculate_fit_analysis(documents, window_sizes=[2048, 4096, 8192]):
    """
    TODO: For each window size, determine:
    1. How many documents fit (accounting for 300 token overhead)
    2. What percentage of total tokens can be included
    3. Which specific documents fit (in order, until limit reached)
    
    Args:
        documents: List of document dicts with 'tokens' field
        window_sizes: List of context window sizes to analyze
    
    Returns:
        Dictionary with results for each window size
    """
    results = {}
    overhead = 300  # tokens for question + response + instructions
    
    # TODO: Your implementation here
    # Hint: Iterate through documents in order, track cumulative tokens
    # Hint: Stop when adding next doc would exceed (window_size - overhead)
    
    for window_size in window_sizes:
        available_tokens = window_size - overhead
        # TODO: Calculate how many docs fit
        # TODO: Calculate percentage of total
        # TODO: Track which specific docs
        
        results[window_size] = {
            'docs_fit': 0,  # TODO: Replace with actual count
            'tokens_used': 0,  # TODO: Replace with actual sum
            'percentage': 0,  # TODO: Replace with actual percentage
            'doc_indices': []  # TODO: Replace with actual indices
        }
    
    return results

# Test your implementation
fit_analysis = calculate_fit_analysis(documents)

# Display results
print("📊 Context Window Fit Analysis\n")
for window_size, stats in fit_analysis.items():
    print(f"Window Size: {window_size:,} tokens")
    print(f"  Documents that fit: {stats['docs_fit']}/{len(documents)}")
    print(f"  Tokens used: {stats['tokens_used']:,}")
    print(f"  Coverage: {stats['percentage']:.1f}%")
    print()

# 💡 HINT: If you're stuck, uncomment the next line
# %load ../src/hints/hint_calculate_fit.py
```

#### Cell 10 [M]: Phase 1 Reflection
```markdown
## ✅ Phase 1 Complete!

**What you learned:**
- Context windows have hard token limits
- Not all information can fit at once
- Strategic selection is crucial

**Key Takeaway:** With an 8K window, you can only fit ~75% of documents. **Which ones should you choose? And where should you put them?**

That's what we'll explore next! ⬇️

---
```

---

### Section 3: Phase 2 - Baseline Implementation (Cells 11-18)

#### Cell 11 [M]: Phase 2 Introduction
```markdown
# Phase 2: Baseline Context Assembly (8 minutes)

## The Naive Approach

The simplest strategy: concatenate documents in order until you run out of space.

**No intelligence, no optimization, just raw concatenation.**

This will be our **baseline** for comparison. Every other strategy must beat this!

## Your Task

Implement `naive_context_assembly()` that:
1. Takes documents and a query
2. Concatenates documents in order
3. Stops when approaching the token limit
4. Returns the assembled context string

Let's build it! 💪
```

#### Cell 12 [T]: TODO - Naive Implementation
```python
# Cell 12: TODO - Implement naive context assembly

def naive_context_assembly(documents, query, token_limit=4000):
    """
    Naive context assembly: concatenate documents in order until token limit.
    
    Args:
        documents: List of document dicts with 'content' and 'tokens' fields
        query: The question being asked (string)
        token_limit: Maximum tokens for context (int)
    
    Returns:
        Assembled context string
    """
    # TODO: Implement naive concatenation
    # Hint 1: Reserve some tokens for the query itself (~50)
    # Hint 2: Iterate through documents in order
    # Hint 3: Keep track of cumulative tokens
    # Hint 4: Stop when adding next doc would exceed limit
    # Hint 5: Format nicely with document separators
    
    context_parts = []
    used_tokens = 0
    available_tokens = token_limit - 50  # Reserve for query
    
    # TODO: Your implementation here
    
    return "\n\n".join(context_parts)

# Test your implementation
test_query = questions[0]['question']
test_context = naive_context_assembly(documents, test_query, token_limit=4000)

print(f"✅ Naive context assembled!")
print(f"📏 Length: {len(test_context)} characters")
print(f"🔢 Tokens: ~{count_tokens(test_context)}")
print(f"\n📄 Preview:\n{test_context[:300]}...")

# 💡 HINT: Stuck? Uncomment for solution skeleton
# %load ../src/hints/hint_naive_assembly.py
```

#### Cell 13 [C]: Create Evaluator
```python
# Cell 13: Set up evaluator
print("Setting up evaluation system...")

evaluator = LLMEvaluator(model, tokenizer)
print("✅ Evaluator ready!")

# Test on one question
print("\n🧪 Testing evaluator with one question...")
test_context = naive_context_assembly(documents, questions[0]['question'])
test_answer = evaluator.generate_answer(test_context, questions[0]['question'])
test_score = evaluator.score_answer(
    test_answer, 
    questions[0]['ground_truth_answer']
)

print(f"\nQuestion: {questions[0]['question']}")
print(f"Generated Answer: {test_answer}")
print(f"Score: {test_score:.2f}")
```

#### Cell 14 [C]: Evaluate Naive Strategy
```python
# Cell 14: Evaluate naive strategy on all questions
print("🔬 Evaluating naive strategy on all questions...")
print("This may take 2-3 minutes...\n")

naive_results = []

for q in tqdm(questions, desc="Evaluating"):
    # Assemble context
    context = naive_context_assembly(documents, q['question'], token_limit=4000)
    
    # Generate answer
    answer = evaluator.generate_answer(context, q['question'])
    
    # Score answer
    score = evaluator.score_answer(answer, q['ground_truth_answer'])
    
    naive_results.append({
        'question_id': q['id'],
        'question': q['question'],
        'answer': answer,
        'score': score,
        'tokens_used': count_tokens(context)
    })

# Calculate metrics
naive_accuracy = np.mean([r['score'] for r in naive_results])
naive_tokens = np.mean([r['tokens_used'] for r in naive_results])

print(f"\n📊 Naive Strategy Results:")
print(f"   Average Accuracy: {naive_accuracy:.2%}")
print(f"   Average Tokens: {naive_tokens:.0f}")
print(f"   Token Efficiency: {(naive_accuracy / naive_tokens * 1000):.3f} (accuracy per 1K tokens)")

# Save for later comparison
baseline_metrics = {
    'strategy': 'naive',
    'accuracy': naive_accuracy,
    'avg_tokens': naive_tokens,
    'all_results': naive_results
}
```

#### Cell 15 [M]: Baseline Reflection
```markdown
## 📈 Baseline Established!

You've now measured the **naive approach** performance. This is your baseline.

**Typical Results:**
- Accuracy: 65-72%
- Token usage: ~3800/4000

## What's Wrong with Naive?

1. **No relevance ranking** - Treats all documents equally
2. **Order dependency** - First documents always included, last ones never are
3. **Ignores the query** - Doesn't consider what's actually being asked
4. **Wastes attention** - Model must process irrelevant info

**Can we do better? Absolutely!** ⬇️

---
```

---

### Section 4: Phase 3 - Strategic Placement (Cells 19-32)

#### Cell 16 [M]: Phase 3 Introduction
```markdown
# Phase 3: Strategic Context Placement (10 minutes)

## The "Lost in the Middle" Problem

Research shows that LLMs have **positional bias**:
- ✅ **Strong recall** for information at the START of context
- ✅ **Strong recall** for information at the END of context
- ❌ **Weak recall** for information in the MIDDLE

This is called the **"lost in the middle"** phenomenon.

## Three Strategies to Test

### 1. Primacy Placement
Place most relevant documents at the **beginning**

### 2. Recency Placement  
Place most relevant documents at the **end**

### 3. Sandwich Placement
Place relevant documents at **both ends**, less relevant in middle

## Your Challenge

Implement all three strategies and measure which performs best!

**First, we need a way to rank document relevance...**
```

#### Cell 17 [C]: Document Ranking Function
```python
# Cell 17: Implement document ranking by relevance
def rank_documents_by_relevance(documents, query, embedder):
    """
    Rank documents by semantic similarity to the query.
    
    Args:
        documents: List of document dicts
        query: Question string
        embedder: SentenceTransformer model
    
    Returns:
        List of (doc, similarity_score) tuples, sorted by score descending
    """
    # Encode query
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    
    # Encode all documents and calculate similarity
    ranked = []
    for doc in documents:
        doc_embedding = embedder.encode(doc['content'], convert_to_tensor=True)
        similarity = calculate_similarity(query_embedding, doc_embedding)
        ranked.append((doc, similarity.item()))
    
    # Sort by similarity (highest first)
    ranked.sort(key=lambda x: x[1], reverse=True)
    
    return ranked

# Test ranking
test_query = "What is the lost in the middle problem?"
ranked_docs = rank_documents_by_relevance(documents, test_query, embedder)

print("📊 Document Ranking for Query:", test_query)
print("\nTop 3 most relevant:")
for i, (doc, score) in enumerate(ranked_docs[:3], 1):
    print(f"{i}. {doc['title'][:50]}... (similarity: {score:.3f})")

print("\nBottom 3 least relevant:")
for i, (doc, score) in enumerate(ranked_docs[-3:], 1):
    print(f"{i}. {doc['title'][:50]}... (similarity: {score:.3f})")
```

#### Cell 18 [T]: TODO - Primacy Strategy
```python
# Cell 18: TODO - Implement primacy placement strategy

def primacy_context_assembly(documents, query, token_limit=4000, embedder=None):
    """
    Primacy placement: Most relevant documents at the START.
    
    Args:
        documents: List of document dicts
        query: Question string
        token_limit: Max tokens
        embedder: SentenceTransformer for ranking
    
    Returns:
        Assembled context string
    """
    # TODO: Implement primacy strategy
    # Step 1: Rank documents by relevance to query
    # Step 2: Place highest-ranked docs first
    # Step 3: Continue adding until token limit
    # Step 4: Return formatted context
    
    # TODO: Your implementation here
    # Hint: Use rank_documents_by_relevance() from above
    # Hint: Similar to naive, but with sorted order
    
    pass

# Test your implementation
test_primacy_context = primacy_context_assembly(
    documents, 
    questions[0]['question'], 
    embedder=embedder
)

print(f"✅ Primacy context assembled!")
print(f"📏 Tokens: ~{count_tokens(test_primacy_context)}")

# 💡 HINT: Stuck?
# %load ../src/hints/hint_primacy.py
```

#### Cell 19 [T]: TODO - Recency Strategy
```python
# Cell 19: TODO - Implement recency placement strategy

def recency_context_assembly(documents, query, token_limit=4000, embedder=None):
    """
    Recency placement: Most relevant documents at the END.
    
    Args:
        documents: List of document dicts
        query: Question string  
        token_limit: Max tokens
        embedder: SentenceTransformer for ranking
    
    Returns:
        Assembled context string
    """
    # TODO: Implement recency strategy
    # Step 1: Rank documents by relevance
    # Step 2: Add documents in REVERSE rank order (least relevant first)
    # Step 3: This puts most relevant at the end
    # Step 4: Return formatted context
    
    # TODO: Your implementation here
    # Hint: Very similar to primacy, but reverse the order!
    
    pass

# Test
test_recency_context = recency_context_assembly(
    documents,
    questions[0]['question'],
    embedder=embedder
)

print(f"✅ Recency context assembled!")
print(f"📏 Tokens: ~{count_tokens(test_recency_context)}")

# 💡 HINT: Stuck?
# %load ../src/hints/hint_recency.py
```

#### Cell 20 [T]: TODO - Sandwich Strategy
```python
# Cell 20: TODO - Implement sandwich placement strategy

def sandwich_context_assembly(documents, query, token_limit=4000, embedder=None):
    """
    Sandwich placement: Relevant docs at BOTH ends, less relevant in middle.
    
    Strategy:
    - Top 50% of relevant docs → split into two groups
    - First group at START
    - Second group at END
    - Remaining docs in MIDDLE
    
    Args:
        documents: List of document dicts
        query: Question string
        token_limit: Max tokens
        embedder: SentenceTransformer for ranking
    
    Returns:
        Assembled context string
    """
    # TODO: Implement sandwich strategy
    # Step 1: Rank documents by relevance
    # Step 2: Identify top-ranked docs (most relevant)
    # Step 3: Split top docs into two groups
    # Step 4: Assemble: [group1] + [middle docs] + [group2]
    # Step 5: Respect token limit throughout
    
    # TODO: Your implementation here
    # Hint: This is the most complex strategy!
    # Hint: Consider what % of top docs to sandwich (try 40%)
    
    pass

# Test
test_sandwich_context = sandwich_context_assembly(
    documents,
    questions[0]['question'],
    embedder=embedder
)

print(f"✅ Sandwich context assembled!")
print(f"📏 Tokens: ~{count_tokens(test_sandwich_context)}")

# 💡 HINT: Stuck? This one is tricky!
# %load ../src/hints/hint_sandwich.py
```

#### Cell 21 [C]: Evaluate All Three Strategies
```python
# Cell 21: Evaluate primacy, recency, and sandwich strategies
print("🔬 Evaluating all three strategic placement approaches...")
print("This will take 5-8 minutes total...\n")

strategies = {
    'primacy': primacy_context_assembly,
    'recency': recency_context_assembly,
    'sandwich': sandwich_context_assembly
}

all_results = {'naive': baseline_metrics}  # Include baseline

for strategy_name, strategy_func in strategies.items():
    print(f"\n📊 Evaluating {strategy_name.upper()} strategy...")
    
    results = []
    for q in tqdm(questions, desc=f"  {strategy_name}"):
        # Assemble context using this strategy
        context = strategy_func(
            documents, 
            q['question'], 
            token_limit=4000,
            embedder=embedder
        )
        
        # Generate and score answer
        answer = evaluator.generate_answer(context, q['question'])
        score = evaluator.score_answer(answer, q['ground_truth_answer'])
        
        results.append({
            'question_id': q['id'],
            'score': score,
            'tokens_used': count_tokens(context)
        })
    
    # Calculate metrics
    accuracy = np.mean([r['score'] for r in results])
    avg_tokens = np.mean([r['tokens_used'] for r in results])
    
    all_results[strategy_name] = {
        'strategy': strategy_name,
        'accuracy': accuracy,
        'avg_tokens': avg_tokens,
        'all_results': results
    }
    
    print(f"   ✅ Accuracy: {accuracy:.2%}")
    print(f"   📏 Avg Tokens: {avg_tokens:.0f}")

print("\n🎉 All strategies evaluated!")
```

#### Cell 22 [C]: Compare Strategies Visually
```python
# Cell 22: Visualize strategy comparison
# Create comparison dataframe
comparison_df = pd.DataFrame([
    {
        'Strategy': name.capitalize(),
        'Accuracy': metrics['accuracy'],
        'Avg Tokens': metrics['avg_tokens'],
        'Improvement': (metrics['accuracy'] - all_results['naive']['accuracy']) / all_results['naive']['accuracy']
    }
    for name, metrics in all_results.items()
])

# Sort by accuracy
comparison_df = comparison_df.sort_values('Accuracy', ascending=False)

# Display table
print("📊 STRATEGY COMPARISON\n")
print(comparison_df.to_string(index=False))
print()

# Plot comparison
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy comparison
ax1.barh(comparison_df['Strategy'], comparison_df['Accuracy'] * 100, color='steelblue')
ax1.set_xlabel('Accuracy (%)')
ax1.set_title('Strategy Accuracy Comparison')
ax1.grid(True, alpha=0.3)

# Improvement over baseline
ax2.barh(
    comparison_df['Strategy'][1:],  # Exclude naive (baseline)
    comparison_df['Improvement'][1:] * 100,
    color='green'
)
ax2.set_xlabel('Improvement over Baseline (%)')
ax2.set_title('Relative Improvement')
ax2.axvline(x=0, color='r', linestyle='--', alpha=0.5)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

#### Cell 23 [M]: Phase 3 Reflection
```markdown
## ✅ Phase 3 Complete!

**What you discovered:**
- Position in context matters significantly
- Different strategies perform differently
- Strategic placement can improve accuracy by 10-20%

### Typical Results

| Strategy | Expected Accuracy | Improvement |
|----------|------------------|-------------|
| Naive    | 65-72%           | Baseline    |
| Primacy  | 70-77%           | +5-8%       |
| Recency  | 75-82%           | +10-15%     |
| Sandwich | 78-85%           | +15-20%     |

**Key Insight:** The sandwich strategy usually wins by avoiding the "lost in the middle" problem!

**But can we do even better?** Let's find out! ⬇️

---
```

---

### Section 5: Phase 4 - Optimization (Cells 33-40)

#### Cell 24 [M]: Phase 4 Introduction
```markdown
# Phase 4: Advanced Optimization (5 minutes)

You've mastered strategic placement. Now let's add one more optimization!

## Choose YOUR Optimization

Pick ONE of these three approaches to implement:

### Option A: Hierarchical Summarization
- Summarize less-relevant documents
- Keep full text only for most relevant
- Trade tokens for coverage

### Option B: Semantic Chunking
- Split documents at semantic boundaries
- Include only most relevant chunks
- Better granularity than full documents

### Option C: Dynamic Token Allocation
- Allocate tokens proportional to relevance scores
- High-relevance docs get more space
- Ensures coverage across all documents

**Choose the one that interests you most!**
```

#### Cell 25 [M]: Option A - Hierarchical Summarization
```markdown
## Option A: Hierarchical Summarization

### Concept
Create short summaries of less-relevant documents, include full text only for top-ranked documents.

### Benefits
- Cover more documents in same token budget
- Maintain awareness of all content
- Focus detail where it matters most

### Implementation Strategy
1. Rank documents by relevance
2. Full text for top 3 documents
3. Generate summaries for remaining documents
4. Assemble using sandwich strategy

**If you choose this option, implement it in the next cell!**
```

#### Cell 28 [T]: TODO - Option B Implementation
```python
# Cell 28: TODO - Option B: Semantic Chunking
# ONLY implement this if you chose Option B!

def semantic_chunking_assembly(documents, query, token_limit=4000, embedder=None):
    """
    Semantic chunking: Rank and select individual chunks rather than full documents.
    
    Args:
        documents: List of document dicts
        query: Question string
        token_limit: Max tokens
        embedder: SentenceTransformer for ranking
    
    Returns:
        Assembled context string
    """
    # TODO: Implement if you chose Option B
    # Step 1: Split all documents into chunks (paragraphs)
    # Step 2: Rank ALL chunks by relevance to query
    # Step 3: Select top-ranked chunks until token limit
    # Step 4: Assemble using sandwich strategy
    
    # Hint: Split on double newlines or use sentence boundaries
    # Hint: Track which document each chunk came from
    # Hint: Format chunks with document context
    
    pass

# Test (only if implementing Option B)
# test_chunk_context = semantic_chunking_assembly(
#     documents,
#     questions[0]['question'],
#     embedder=embedder
# )
# print(f"✅ Semantic chunking complete!")
# print(f"📏 Tokens: ~{count_tokens(test_chunk_context)}")
```

#### Cell 29 [M]: Option C - Dynamic Token Allocation
```markdown
## Option C: Dynamic Token Allocation

### Concept
Allocate tokens to documents proportionally based on relevance scores. High-relevance documents get more tokens, low-relevance get fewer.

### Benefits
- Ensures coverage of all documents
- Allocates "attention budget" intelligently
- Adapts to query-specific relevance

### Implementation Strategy
1. Rank documents by relevance
2. Calculate token allocation for each doc based on relevance score
3. Truncate documents to their allocated token budgets
4. Assemble using sandwich strategy

**If you choose this option, implement it in the next cell!**
```

#### Cell 30 [T]: TODO - Option C Implementation
```python
# Cell 30: TODO - Option C: Dynamic Token Allocation
# ONLY implement this if you chose Option C!

def dynamic_allocation_assembly(documents, query, token_limit=4000, embedder=None):
    """
    Dynamic token allocation: Assign tokens proportional to relevance.
    
    Args:
        documents: List of document dicts
        query: Question string
        token_limit: Max tokens
        embedder: SentenceTransformer for ranking
    
    Returns:
        Assembled context string
    """
    # TODO: Implement if you chose Option C
    # Step 1: Rank documents with relevance scores
    # Step 2: Calculate total relevance score
    # Step 3: Allocate tokens: (doc_score / total_score) * available_tokens
    # Step 4: Truncate each doc to its allocation
    # Step 5: Assemble using sandwich strategy
    
    # Hint: Ensure minimum allocation per doc (e.g., 100 tokens)
    # Hint: Handle edge cases where allocation exceeds doc length
    
    pass

# Test (only if implementing Option C)
# test_dynamic_context = dynamic_allocation_assembly(
#     documents,
#     questions[0]['question'],
#     embedder=embedder
# )
# print(f"✅ Dynamic allocation complete!")
# print(f"📏 Tokens: ~{count_tokens(test_dynamic_context)}")
```

#### Cell 31 [C]: Evaluate Your Optimization
```python
# Cell 31: Evaluate your chosen optimization
# Update this based on which option you implemented!

print("🔬 Evaluating your optimization...")
print("This will take 2-3 minutes...\n")

# IMPORTANT: Update the function name based on your choice!
# Option A: hierarchical_summary_assembly
# Option B: semantic_chunking_assembly
# Option C: dynamic_allocation_assembly

YOUR_OPTIMIZATION_FUNCTION = hierarchical_summary_assembly  # TODO: Update this!
optimization_name = "your_optimization"  # TODO: Give it a name!

optimization_results = []

for q in tqdm(questions, desc="Evaluating optimization"):
    # Assemble context using your optimization
    context = YOUR_OPTIMIZATION_FUNCTION(
        documents,
        q['question'],
        token_limit=4000,
        embedder=embedder
    )
    
    # Generate and score
    answer = evaluator.generate_answer(context, q['question'])
    score = evaluator.score_answer(answer, q['ground_truth_answer'])
    
    optimization_results.append({
        'question_id': q['id'],
        'score': score,
        'tokens_used': count_tokens(context)
    })

# Calculate metrics
opt_accuracy = np.mean([r['score'] for r in optimization_results])
opt_tokens = np.mean([r['tokens_used'] for r in optimization_results])

# Calculate improvements
accuracy_improvement = (opt_accuracy - baseline_metrics['accuracy']) / baseline_metrics['accuracy']
token_reduction = (baseline_metrics['avg_tokens'] - opt_tokens) / baseline_metrics['avg_tokens']

print(f"\n📊 {optimization_name.upper()} Results:")
print(f"   Accuracy: {opt_accuracy:.2%}")
print(f"   Avg Tokens: {opt_tokens:.0f}")
print(f"   Accuracy Improvement: {accuracy_improvement:+.1%} vs baseline")
print(f"   Token Reduction: {token_reduction:+.1%} vs baseline")

# Save results
all_results[optimization_name] = {
    'strategy': optimization_name,
    'accuracy': opt_accuracy,
    'avg_tokens': opt_tokens,
    'all_results': optimization_results
}

# Check if optimization passes threshold
if accuracy_improvement >= 0.10 or token_reduction >= 0.20:
    print(f"\n✅ Optimization successful! Meets improvement threshold.")
else:
    print(f"\n⚠️ Optimization below threshold. Consider tweaking your approach.")
```

#### Cell 32 [M]: Phase 4 Reflection
```markdown
## ✅ Phase 4 Complete!

**What you accomplished:**
- Implemented an advanced optimization technique
- Measured its impact quantitatively
- Compared against baseline and strategic approaches

### Typical Optimization Results

- **Hierarchical Summarization:** 15-20% accuracy improvement, covers more documents
- **Semantic Chunking:** 18-25% accuracy improvement, best precision
- **Dynamic Allocation:** 12-18% accuracy improvement, best coverage

**Key Insight:** Advanced optimizations can significantly boost performance, but require careful implementation!

---
```

---

### Section 6: Phase 5 - Final Results (Cells 33-40)

#### Cell 33 [M]: Final Results Introduction
```markdown
# Phase 5: Final Results & Comparison

Let's see how all your implementations stack up!

We'll compare:
1. **Naive baseline** (no optimization)
2. **Primacy** (relevant at start)
3. **Recency** (relevant at end)
4. **Sandwich** (relevant at both ends)
5. **Your optimization** (advanced technique)

Time to see your progress! 📊
```

#### Cell 34 [C]: Comprehensive Comparison
```python
# Cell 34: Create comprehensive comparison
print("📊 FINAL RESULTS - ALL STRATEGIES\n")
print("=" * 80)

# Create detailed comparison
final_comparison = []
for name, metrics in all_results.items():
    baseline_acc = all_results['naive']['accuracy']
    improvement = (metrics['accuracy'] - baseline_acc) / baseline_acc * 100
    
    final_comparison.append({
        'Strategy': name.replace('_', ' ').title(),
        'Accuracy': f"{metrics['accuracy']:.1%}",
        'Avg Tokens': f"{metrics['avg_tokens']:.0f}",
        'Improvement': f"{improvement:+.1f}%",
        'Raw Accuracy': metrics['accuracy']  # For sorting
    })

# Sort by accuracy
final_comparison.sort(key=lambda x: x['Raw Accuracy'], reverse=True)

# Display as formatted table
comparison_df = pd.DataFrame(final_comparison)
comparison_df = comparison_df.drop('Raw Accuracy', axis=1)

print(comparison_df.to_string(index=False))
print("\n" + "=" * 80)

# Find best strategy
best_strategy = final_comparison[0]['Strategy']
best_accuracy = final_comparison[0]['Raw Accuracy']
best_improvement = float(final_comparison[0]['Improvement'].strip('%+'))

print(f"\n🏆 BEST STRATEGY: {best_strategy}")
print(f"   Accuracy: {best_accuracy:.1%}")
print(f"   Improvement: {best_improvement:+.1f}% over baseline")
```

#### Cell 35 [C]: Visualization - Complete Comparison
```python
# Cell 35: Comprehensive visualization
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Accuracy comparison (bar chart)
strategies = [item['Strategy'] for item in final_comparison]
accuracies = [item['Raw Accuracy'] * 100 for item in final_comparison]
colors = ['lightcoral' if s == 'Naive' else 'steelblue' for s in strategies]

axes[0, 0].barh(strategies, accuracies, color=colors, alpha=0.7)
axes[0, 0].set_xlabel('Accuracy (%)', fontsize=12)
axes[0, 0].set_title('Strategy Accuracy Comparison', fontsize=14, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3, axis='x')
axes[0, 0].axvline(x=all_results['naive']['accuracy'] * 100, 
                    color='red', linestyle='--', alpha=0.5, label='Baseline')
axes[0, 0].legend()

# 2. Improvement over baseline (bar chart)
improvements = [float(item['Improvement'].strip('%+')) for item in final_comparison[1:]]
strategy_names = [item['Strategy'] for item in final_comparison[1:]]
improvement_colors = ['green' if imp > 0 else 'red' for imp in improvements]

axes[0, 1].barh(strategy_names, improvements, color=improvement_colors, alpha=0.7)
axes[0, 1].set_xlabel('Improvement over Baseline (%)', fontsize=12)
axes[0, 1].set_title('Relative Performance Gains', fontsize=14, fontweight='bold')
axes[0, 1].axvline(x=0, color='black', linestyle='-', linewidth=0.8)
axes[0, 1].grid(True, alpha=0.3, axis='x')

# 3. Token efficiency (scatter plot)
token_counts = [all_results[name]['avg_tokens'] for name in all_results.keys()]
accuracy_vals = [all_results[name]['accuracy'] * 100 for name in all_results.keys()]
labels = [name.replace('_', ' ').title() for name in all_results.keys()]

axes[1, 0].scatter(token_counts, accuracy_vals, s=200, alpha=0.6, c=range(len(labels)), cmap='viridis')
for i, label in enumerate(labels):
    axes[1, 0].annotate(label, (token_counts[i], accuracy_vals[i]), 
                        fontsize=9, ha='right', va='bottom')
axes[1, 0].set_xlabel('Average Tokens Used', fontsize=12)
axes[1, 0].set_ylabel('Accuracy (%)', fontsize=12)
axes[1, 0].set_title('Token Efficiency Analysis', fontsize=14, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

# 4. Per-question performance heatmap
# Create matrix of scores per strategy per question
score_matrix = []
strategy_order = [item['Strategy'] for item in final_comparison]
for strategy in strategy_order:
    strategy_key = strategy.lower().replace(' ', '_')
    if strategy_key in all_results:
        scores = [r['score'] for r in all_results[strategy_key]['all_results']]
        score_matrix.append(scores)

im = axes[1, 1].imshow(score_matrix, aspect='auto', cmap='RdYlGn', vmin=0, vmax=1)
axes[1, 1].set_yticks(range(len(strategy_order)))
axes[1, 1].set_yticklabels(strategy_order, fontsize=9)
axes[1, 1].set_xlabel('Question Number', fontsize=12)
axes[1, 1].set_title('Per-Question Performance Heatmap', fontsize=14, fontweight='bold')
plt.colorbar(im, ax=axes[1, 1], label='Score')

plt.tight_layout()
plt.show()

print("\n✅ Visualizations complete!")
```

#### Cell 36 [C]: Statistical Analysis
```python
# Cell 36: Statistical significance testing
from scipy import stats

print("📈 STATISTICAL ANALYSIS\n")
print("Testing if improvements are statistically significant...\n")

# Get score arrays
naive_scores = [r['score'] for r in all_results['naive']['all_results']]

for strategy_name in all_results.keys():
    if strategy_name == 'naive':
        continue
    
    strategy_scores = [r['score'] for r in all_results[strategy_name]['all_results']]
    
    # Paired t-test (same questions for both strategies)
    t_stat, p_value = stats.ttest_rel(strategy_scores, naive_scores)
    
    is_significant = "✅ YES" if p_value < 0.05 else "❌ NO"
    
    print(f"{strategy_name.replace('_', ' ').title()}:")
    print(f"  p-value: {p_value:.4f}")
    print(f"  Statistically significant (p < 0.05)? {is_significant}")
    print()

print("💡 Lower p-value = more confident the improvement is real, not random chance")
```

#### Cell 37 [M]: Learning Insights
```markdown
## 🎓 Key Learning Insights

### What You Discovered

1. **Position Matters**
   - Information at the start and end is recalled better than middle
   - The "sandwich" strategy consistently outperforms simple approaches

2. **Relevance Ranking is Critical**
   - Not all documents are equally useful for a given query
   - Semantic similarity helps identify relevant content

3. **Optimization Has Trade-offs**
   - Compression saves tokens but may lose detail
   - Chunking increases precision but adds complexity
   - Dynamic allocation balances coverage and relevance

4. **Measurement is Essential**
   - Quantitative evaluation reveals what actually works
   - Intuitions about performance are often wrong
   - Small changes can have significant impacts

### Real-World Applications

These techniques apply to:
- **RAG Systems:** Optimize retrieved document assembly
- **Chatbots:** Manage conversation history efficiently
- **Document Q&A:** Handle long documents within token limits
- **Production LLMs:** Reduce costs while maintaining quality

---
```

#### Cell 38 [C]: Save Results
```python
# Cell 38: Save all results to file
import json
from datetime import datetime

# Prepare results for saving
results_to_save = {
    'metadata': {
        'lesson': 'context_engineering',
        'timestamp': datetime.now().isoformat(),
        'model_used': MODEL_NAME,
        'embedding_model': EMBED_MODEL,
        'num_questions': len(questions),
        'num_documents': len(documents)
    },
    'strategies': {}
}

for strategy_name, metrics in all_results.items():
    results_to_save['strategies'][strategy_name] = {
        'accuracy': metrics['accuracy'],
        'avg_tokens': metrics['avg_tokens'],
        'improvement_vs_baseline': (
            (metrics['accuracy'] - all_results['naive']['accuracy']) / 
            all_results['naive']['accuracy']
        ) if strategy_name != 'naive' else 0.0,
        'per_question_scores': [r['score'] for r in metrics['all_results']]
    }

# Save to progress folder
output_path = Path('../progress/lesson_results.json')
output_path.parent.mkdir(exist_ok=True)

with open(output_path, 'w') as f:
    json.dump(results_to_save, f, indent=2)

print(f"✅ Results saved to: {output_path}")
print("\nYou can now run the verification script to get your grade!")
```

#### Cell 39 [M]: Next Steps
```markdown
## ✅ Lesson Complete! 🎉

Congratulations! You've successfully completed the Context Engineering micro-lesson.

### What You Built

✅ Token budget calculator  
✅ Naive context assembly (baseline)  
✅ Primacy placement strategy  
✅ Recency placement strategy  
✅ Sandwich placement strategy  
✅ Advanced optimization (your choice)  
✅ Comprehensive evaluation system  

### Your Results

Check the visualizations above to see your performance across all strategies!

---

## 🏆 Get Your Grade

To verify your completion and get your official grade, run:

```bash
python src/verify.py
```

This will:
1. Check that all strategies are implemented
2. Verify metrics meet requirements
3. Generate your completion certificate: `progress/lesson_progress.json`

---

## 📚 Continue Learning

Want to go deeper? Try:
- Implement the other optimization options you didn't choose
- Test with different token limits (2K, 8K, 16K)
- Try different LLMs (Mistral-7B, Llama-2-7B)
- Build a complete RAG system using these techniques
- Optimize for different objectives (speed vs accuracy vs cost)

---

## 🤝 Feedback

This lesson is open source! If you found bugs or have suggestions:
- Open an issue on GitHub
- Submit a pull request with improvements
- Share your results with the community

**Thank you for learning with us!** 🙏
```

#### Cell 40 [C]: Final Cleanup
```python
# Cell 40: Cleanup and final message
print("=" * 80)
print(" " * 20 + "CONTEXT ENGINEERING LESSON COMPLETE")
print("=" * 80)
print()
print("🎓 You've mastered the fundamentals of context engineering!")
print()
print("Next steps:")
print("  1. Run: python src/verify.py")
print("  2. Check: progress/lesson_progress.json")
print("  3. Celebrate your achievement! 🎉")
print()
print("=" * 80)

# Show best result one more time
best_strategy_name = max(all_results.keys(), 
                         key=lambda k: all_results[k]['accuracy'])
best_accuracy = all_results[best_strategy_name]['accuracy']
improvement = (best_accuracy - all_results['naive']['accuracy']) / all_results['naive']['accuracy']

print(f"\n🏆 Your Best Strategy: {best_strategy_name.replace('_', ' ').title()}")
print(f"   Final Accuracy: {best_accuracy:.1%}")
print(f"   Total Improvement: {improvement:+.1%}")
print()
```

---

## Notebook Design Requirements

### Code Quality
- **Docstrings:** Every function has clear docstring
- **Comments:** Explain complex logic
- **Error Handling:** Graceful failures with helpful messages
- **Progress Bars:** Use tqdm for long-running operations
- **Memory Management:** Clean up large variables when done

### Student Experience
- **TODO Markers:** Clear indication of what students must implement
- **Hints:** Progressive hint system (commented %load statements)
- **Validation:** Immediate feedback on implementations
- **Visualization:** Charts and graphs for all comparisons
- **Timing:** Realistic time estimates for each phase

### Interactive Elements
- **Progressive Reveal:** Each cell builds on previous
- **Immediate Feedback:** Test code runs after each implementation
- **Visual Progress:** Charts show improvement in real-time
- **Comparison Tables:** Easy-to-read result summaries
- **Hints System:** Gradual help without giving away solutions

### Pedagogical Structure
1. **Introduce Concept** (Markdown)
2. **Show Example** (Code)
3. **Student Implements** (TODO cell)
4. **Test & Validate** (Code)
5. **Visualize Results** (Code)
6. **Reflect on Learning** (Markdown)

---

## Hint Files Structure

Create separate hint files in `src/hints/`:

### `hint_calculate_fit.py`
```python
# Hint for token budget calculation
def calculate_fit_analysis(documents, window_sizes=[2048, 4096, 8192]):
    results = {}
    overhead = 300
    
    for window_size in window_sizes:
        available = window_size - overhead
        cumulative = 0
        docs_fit = 0
        indices = []
        
        for i, doc in enumerate(documents):
            if cumulative + doc['tokens'] <= available:
                cumulative += doc['tokens']
                docs_fit += 1
                indices.append(i)
            else:
                break
        
        total_tokens = sum(d['tokens'] for d in documents)
        
        results[window_size] = {
            'docs_fit': docs_fit,
            'tokens_used': cumulative,
            'percentage': (cumulative / total_tokens) * 100,
            'doc_indices': indices
        }
    
    return results
```

### `hint_naive_assembly.py`
```python
# Hint for naive context assembly
def naive_context_assembly(documents, query, token_limit=4000):
    context_parts = []
    used_tokens = 0
    available_tokens = token_limit - 50
    
    for doc in documents:
        if used_tokens + doc['tokens'] <= available_tokens:
            context_parts.append(f"Document: {doc['title']}\n{doc['content']}")
            used_tokens += doc['tokens']
        else:
            break
    
    return "\n\n---\n\n".join(context_parts)
```

### Similar hints for all TODO cells

---

## Notebook Testing Checklist

Before finalizing, verify:

- [ ] All cells run sequentially without errors
- [ ] Model downloads work on first run
- [ ] Token counting is accurate
- [ ] All visualizations render properly
- [ ] TODO cells have clear instructions
- [ ] Hints are accessible but not visible by default
- [ ] Progress bars work correctly
- [ ] Results save to correct location
- [ ] Memory usage stays under 16 GB
- [ ] Runs in ~30 minutes on reference hardware
- [ ] Clear error messages for common issues
- [ ] Compatible with Jupyter Notebook and VS Code

---

## Next Steps

1. Save this document as `docs/03_index_html_and_notebook_spec.md`
2. Review the complete specifications
3. Ready for Chunk 4: Source code specifications (verify.py, context_strategies.py, etc.)

**Ready for Chunk 4 when you are!** you choose this option, implement it in the next cell!**
```

#### Cell 26 [T]: TODO - Option A Implementation
```python
# Cell 26: TODO - Option A: Hierarchical Summarization
# ONLY implement this if you chose Option A!

def hierarchical_summary_assembly(documents, query, token_limit=4000, embedder=None):
    """
    Hierarchical summarization: Full text for top docs, summaries for others.
    
    Args:
        documents: List of document dicts
        query: Question string
        token_limit: Max tokens
        embedder: SentenceTransformer for ranking
    
    Returns:
        Assembled context string
    """
    # TODO: Implement if you chose Option A
    # Step 1: Rank documents by relevance
    # Step 2: Identify top N docs for full inclusion (try N=3)
    # Step 3: Generate summaries for remaining docs
    # Step 4: Assemble using sandwich strategy
    # Step 5: Ensure within token limit
    
    # Hint: Use the evaluator to generate summaries
    # Hint: Summary prompt: "Summarize this in 2-3 sentences: {content}"
    
    pass

# Test (only if implementing Option A)
# test_hier_context = hierarchical_summary_assembly(
#     documents,
#     questions[0]['question'],
#     embedder=embedder
# )
# print(f"✅ Hierarchical assembly complete!")
# print(f"📏 Tokens: ~{count_tokens(test_hier_context)}")
```

#### Cell 27 [M]: Option B - Semantic Chunking
```markdown
## Option B: Semantic Chunking

### Concept
Split documents into semantic chunks (paragraphs), rank chunks individually, include only most relevant chunks.

### Benefits
- Finer granularity than full documents
- Can mix content from multiple documents
- More precise relevance matching

### Implementation Strategy
1. Split all documents into paragraphs/chunks
2. Rank ALL chunks by relevance to query
3. Select top-ranked chunks until token limit
4. Assemble using sandwich strategy

**If