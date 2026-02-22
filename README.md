<p align="center">
  <img src="./img.png" alt="Project Banner" width="100%">
</p>

# [SkillSakhi] 🎯

## Basic Details

### Team Name: [HerImpact]

### Team Members
- Member 1: [Smrithi S] - [Toc H Institute of science and Technology]
- Member 2: [Rose Theresa P R] - [Toc H Institute of science and Technology]

### Hosted Project Link
[https://tinkher-skill-sakhi-8iy1.vercel.app/]

### Project Description
[SkillSakhi is a women-only skill exchange platform where members teach and learn from each other using a credit-based system. Instead of money, users earn credits by sharing their skills and spend them to learn new ones. It empowers women to grow, connect, and build knowledge together in a supportive community.]

### The Problem statement
[SkillSakhi solves the problem of limited access to affordable and safe learning spaces for women. Many women have valuable skills but lack platforms to share them or learn new ones without financial barriers.

We create a trusted, women-only community where skills can be exchanged using credits instead of money—making learning accessible, empowering, and collaborative.]


### The Solution
[We solve this by creating a women-only digital platform where members can exchange skills using a credit-based system instead of money.

Users earn credits by teaching a skill and use those credits to learn something new from others.

By combining skill listings, session scheduling, and a credit wallet system, SkillSakhi makes learning accessible, affordable, and empowering.]

---

## Technical Details

### Technologies/Components Used

**For Software:**
- Languages used: [Python,HTML5,CSS3,SQL (MySQL),JavaScript]
- Frameworks used: [Flask,Bootstrap 5]
- Libraries used: [Flask-MySQLdb,Werkzeug (Security),Jinja2,DateTime,Functools (wraps)]
- Tools used: [VS Code (Visual Studio Code),MySQL Workbench / Command Line,Jinja2 Template Debugger,Bootstrap Icons / Emojis]

---

## Features

List the key features of your project:
- Feature 1: [Smart Peer Matching System-
The platform uses a matching algorithm in the backend to scan the database and suggest "Skill Sakhis" based on a mutual exchange: someone who teaches what you want to learn and vice versa.]

- Feature 2: [Dynamic Credit Wallet-
To ensure a fair exchange, the project implements a credit system where users start with a balance (e.g., 5 or 7 credits) that fluctuates as they teach or learn.The backend automatically handles credit transfers: the teacher gains 1 credit and the learner loses 1 credit once a session is marked as "Complete".]

- Feature 3: [Interactive Session Hub & Real-time Chat- 
Once a swap is accepted, partners can enter a dedicated "Interaction Room" featuring a built-in chat system to communicate and coordinate their learning journey.]

- Feature 4: [Automated Session Scheduling & Timeline- Users can schedule multi-day learning plans, which are then displayed in a "Session Timeline" on the dashboard.The feature includes a frontend JavaScript formatter that automatically converts 24-hour database time into a user-friendly 12-hour AM/PM format.]

---

## Implementation

### For Software:

#### Installation
```bash
[Installation commands - git clone https://github.com/your-username/SkillSakhi.git
cd SkillSakhi, pip install flask flask-mysqldb werkzeug]
```

#### Run
```bash
[Run commands - python app.py]
```

## Project Documentation

### For Software:

#### Screenshots
<img width="1366" height="768" alt="Screenshot (87)" src="https://github.com/user-attachments/assets/af65e9df-20ce-4148-89bb-d3f83b25137e" />

<img width="1366" height="768" alt="login" src="https://github.com/user-attachments/assets/c686f613-8d9c-4bff-8fc7-ccd87ccce4cd" />

<img width="1366" height="768" alt="Dashboard" src="https://github.com/user-attachments/assets/93aea730-25a7-4332-906e-7aef5626d606" />

<img width="1366" height="768" alt="RequestSwap" src="https://github.com/user-attachments/assets/5f6eaded-3a26-47c7-8734-4792cc324059" />
<img width="1366" height="768" alt="scheduling" src="https://github.com/user-attachments/assets/c0d50f77-d7f6-45d7-9d16-af6363c14de8" />
<img width="1366" height="768" alt="Communication" src="https://github.com/user-attachments/assets/48c67685-65ee-4b67-aa8e-e451f8690d25" />


#### Diagrams

**System Architecture:**

![Architecture Diagram](docs/architecture.png)
*Explain your system architecture - components, data flow, tech stack interaction*

**Application Workflow:**

![Workflow](docs/workflow.png)
*Add caption explaining your workflow*

---




## Additional Documentation

### For Web Projects with Backend:

#### API Documentation

**Base URL:** `https://tinkher-skill-sakhi-8iy1.vercel.app/`

##### Endpoints

**GET /api/endpoint**
- **Description:** [Retrieves the logged-in user's profile, active swap matches, and scheduled session timelines]
- **Parameters:**
  - `param1` (string): [Description]
  - `param2` (integer): [Description]
- **Response:**
```{
  "user": {"name": "anna sojan", "credits": 7, "teaches": "bharathanatyam", "learns": "python"},
  "matches": [{"partner_name": "Mushrifa G B", "status": "accepted"}],
  "session_days": []
}


**POST /api/endpoint**
- **Description:** [What it does]
- **Request Body:**
```json
{
  "field1": "value1",
  "field2": "value2"
}
```
- **Response:**
```json
{
  "status": "success",
  "message": "Operation completed"
}
```

[Add more endpoints as needed...]

---


### For Scripts/CLI Tools:

#### Command Reference

**Basic Usage:**
```bash
python script.py [options] [arguments]
```

**Available Commands:**
- `command1 [args]` - Description of what command1 does
- `command2 [args]` - Description of what command2 does
- `command3 [args]` - Description of what command3 does

**Options:**
- `-h, --help` - Show help message and exit
- `-v, --verbose` - Enable verbose output
- `-o, --output FILE` - Specify output file path
- `-c, --config FILE` - Specify configuration file
- `--version` - Show version information

**Examples:**

```bash
# Example 1: Basic usage
python script.py input.txt

# Example 2: With verbose output
python script.py -v input.txt

# Example 3: Specify output file
python script.py -o output.txt input.txt

# Example 4: Using configuration
python script.py -c config.json --verbose input.txt
```

#### Demo Output

**Example 1: Basic Processing**

**Input:**
-- Sample user registration data for testing
INSERT INTO users (name, email, password, teaches, learns, credits) 
VALUES ('anna sojan', 'anna@example.com', 'hashed_pass', 'Python', 'Dance', 7);

**Command:**
# Running the Flask backend from the backend directory
```cd backend
python app.py```

**Output:**
```
* Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Processing: Database Connection... Success
Connected to: skillsakhi_db
Active Sessions monitored: 2
Credit system status: Operational
```

**Example 2: Advanced Usage**

**Input:**
```json
{
  "name": "test",
  "value": 123
}
```

**Command:**
```bash
python script.py -v --format json data.json
```

**Output:**
```
[VERBOSE] Loading configuration...
[VERBOSE] Parsing JSON input...
[VERBOSE] Processing data...
{
  "status": "success",
  "processed": true,
  "result": {
    "name": "test",
    "value": 123,
    "timestamp": "2024-02-07T10:30:00"
  }
}
[VERBOSE] Operation completed in 0.23s
```

---

## Project Demo

### Video
[Add your demo video link here - YouTube, Google Drive, etc.]

*Explain what the video demonstrates - key features, user flow, technical highlights*

### Additional Demos
[Add any extra demo materials/links - Live site, APK download, online demo, etc.]

---

## AI Tools Used (Optional - For Transparency Bonus)

If you used AI tools during development, document them here for transparency:

**Tool Used:** [e.g., GitHub Copilot, v0.dev, Cursor, ChatGPT, Claude]

**Purpose:** [What you used it for]
- Example: "Generated boilerplate React components"
- Example: "Debugging assistance for async functions"
- Example: "Code review and optimization suggestions"

**Key Prompts Used:**
- "Create a REST API endpoint for user authentication"
- "Debug this async function that's causing race conditions"
- "Optimize this database query for better performance"

**Percentage of AI-generated code:** [Approximately X%]

**Human Contributions:**
- Architecture design and planning
- Custom business logic implementation
- Integration and testing
- UI/UX design decisions

*Note: Proper documentation of AI usage demonstrates transparency and earns bonus points in evaluation!*

---

## Team Contributions

- [Smrithi S]: [Specific contributions - Frontend development, UI design]
- [Rose Theresa P R]: [Specific contributions -  Backend development, Database design]


---

## License

This project is licensed under the [LICENSE_NAME] License - see the [LICENSE](LICENSE) file for details.

**Common License Options:**
- MIT License (Permissive, widely used)
- Apache 2.0 (Permissive with patent grant)
- GPL v3 (Copyleft, requires derivative works to be open source)

---

Made with ❤️ at TinkerHub
