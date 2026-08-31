
# ================================================================
# AI LEARNING MODULE
# Skill input → Learning Roadmap + Docs + Video Links
# Phase 1: Keyword-based (static structured data)
# Phase 2 (future): GPT-generated personalized roadmap
# ================================================================

LEARNING_DATA = {

    # ==================== IT ====================

    "python": {
        "title"      : "Python Programming",
        "description": "Python ek versatile language hai jo web dev, data science, AI sab mein use hoti hai.",
        "levels": {
            "beginner": {
                "duration" : "4 weeks",
                "roadmap"  : [
                    "Python install karo aur environment setup karo",
                    "Variables, data types (int, str, float, bool) samjho",
                    "Control flow: if/else, for loop, while loop",
                    "Functions define karna aur call karna",
                    "Lists, Tuples, Dictionaries, Sets",
                    "File I/O — files padhna aur likhna",
                    "Basic error handling (try/except)",
                    "5 beginner projects banao (calculator, to-do list, etc.)"
                ],
                "resources": [
                    {"type": "docs",    "title": "Python Official Docs",         "url": "https://docs.python.org/3/tutorial/"},
                    {"type": "docs",    "title": "W3Schools Python",             "url": "https://www.w3schools.com/python/"},
                    {"type": "video",   "title": "Python for Beginners (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw"},
                    {"type": "video",   "title": "100 Days of Python (Udemy)",   "url": "https://www.youtube.com/results?search_query=python+beginner+tutorial"},
                    {"type": "practice","title": "HackerRank Python Practice",   "url": "https://www.hackerrank.com/domains/python"}
                ]
            },
            "intermediate": {
                "duration" : "6 weeks",
                "roadmap"  : [
                    "OOP — Classes, Objects, Inheritance, Polymorphism",
                    "List comprehensions aur generators",
                    "Decorators aur context managers",
                    "Modules aur packages banana",
                    "Regular expressions (re module)",
                    "Working with APIs (requests library)",
                    "Database connection (SQLite/MongoDB)",
                    "Unit testing (pytest/unittest)",
                    "3 intermediate projects (API client, web scraper, etc.)"
                ],
                "resources": [
                    {"type": "docs",    "title": "Real Python — Intermediate",   "url": "https://realpython.com/"},
                    {"type": "docs",    "title": "Python Cookbook",              "url": "https://www.dabeaz.com/cookbook.html"},
                    {"type": "video",   "title": "Intermediate Python (Patrick Loeber)", "url": "https://www.youtube.com/watch?v=HGOBQPFzWKo"},
                    {"type": "practice","title": "LeetCode Python Problems",     "url": "https://leetcode.com/problemset/all/?difficulty=MEDIUM&listId=wpwgkgt"}
                ]
            },
            "expert": {
                "duration" : "8 weeks",
                "roadmap"  : [
                    "Asynchronous programming (asyncio, aiohttp)",
                    "Multithreading vs Multiprocessing",
                    "Memory management aur GIL",
                    "Metaclasses aur advanced OOP",
                    "Design patterns in Python",
                    "Performance optimization (cProfile, caching)",
                    "Build aur publish a Python package",
                    "CI/CD pipeline setup karo"
                ],
                "resources": [
                    {"type": "docs",    "title": "Python Docs — Advanced",       "url": "https://docs.python.org/3/"},
                    {"type": "video",   "title": "Advanced Python (Corey Schafer)", "url": "https://www.youtube.com/c/Coreyms"},
                    {"type": "practice","title": "LeetCode Hard Problems",       "url": "https://leetcode.com/problemset/all/?difficulty=HARD"}
                ]
            }
        }
    },

    "java": {
        "title"      : "Java Programming",
        "description": "Java ek robust, platform-independent language hai jo enterprise applications ke liye use hoti hai.",
        "levels": {
            "beginner": {
                "duration" : "4 weeks",
                "roadmap"  : [
                    "JDK install karo, Hello World likho",
                    "Variables, data types, operators",
                    "Control structures: if/else, switch, loops",
                    "Arrays aur Strings",
                    "Methods define karna",
                    "Basic OOP: Classes aur Objects",
                    "Exception handling basics",
                    "Simple projects (calculator, student grade system)"
                ],
                "resources": [
                    {"type": "docs",    "title": "Oracle Java Tutorials",        "url": "https://docs.oracle.com/javase/tutorial/"},
                    {"type": "docs",    "title": "W3Schools Java",               "url": "https://www.w3schools.com/java/"},
                    {"type": "video",   "title": "Java Full Course (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=grEKMHGYyns"},
                    {"type": "practice","title": "HackerRank Java",              "url": "https://www.hackerrank.com/domains/java"}
                ]
            },
            "intermediate": {
                "duration" : "6 weeks",
                "roadmap"  : [
                    "Advanced OOP: Inheritance, Polymorphism, Abstraction",
                    "Interfaces aur Abstract classes",
                    "Collections Framework (ArrayList, HashMap, etc.)",
                    "Generics",
                    "File I/O aur Serialization",
                    "Multithreading basics",
                    "Lambda expressions aur Stream API",
                    "JDBC (database connection)"
                ],
                "resources": [
                    {"type": "docs",    "title": "Baeldung Java Guides",         "url": "https://www.baeldung.com/"},
                    {"type": "video",   "title": "Java Intermediate (Telusko)", "url": "https://www.youtube.com/c/Telusko"},
                    {"type": "practice","title": "CodeChef Java Practice",       "url": "https://www.codechef.com/"}
                ]
            },
            "expert": {
                "duration" : "8 weeks",
                "roadmap"  : [
                    "Spring Boot framework",
                    "JPA/Hibernate (ORM)",
                    "Microservices architecture",
                    "JVM internals aur performance tuning",
                    "Design patterns (GoF)",
                    "Unit testing with JUnit + Mockito",
                    "Docker + Kubernetes basics",
                    "Build REST API with Spring Boot"
                ],
                "resources": [
                    {"type": "docs",    "title": "Spring Boot Docs",             "url": "https://spring.io/projects/spring-boot"},
                    {"type": "video",   "title": "Spring Boot (Amigoscode)",     "url": "https://www.youtube.com/watch?v=9SGDpanrc8U"},
                    {"type": "practice","title": "LeetCode Java",                "url": "https://leetcode.com/"}
                ]
            }
        }
    },

    "c++": {
        "title"      : "C++ Programming",
        "description": "C++ ek powerful systems programming language hai jo game dev, embedded systems mein use hoti hai.",
        "levels": {
            "beginner": {
                "duration" : "4 weeks",
                "roadmap"  : [
                    "C++ setup karo (GCC / Visual Studio)",
                    "Basic syntax, cin/cout",
                    "Variables, data types, operators",
                    "Control flow: if/else, loops",
                    "Functions aur recursion",
                    "Arrays aur Strings",
                    "Pointers basics",
                    "Simple projects"
                ],
                "resources": [
                    {"type": "docs",    "title": "cppreference.com",             "url": "https://en.cppreference.com/"},
                    {"type": "docs",    "title": "W3Schools C++",                "url": "https://www.w3schools.com/cpp/"},
                    {"type": "video",   "title": "C++ Full Course (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y"},
                    {"type": "practice","title": "HackerRank C++",               "url": "https://www.hackerrank.com/domains/cpp"}
                ]
            },
            "intermediate": {
                "duration" : "6 weeks",
                "roadmap"  : [
                    "OOP: Classes, Inheritance, Polymorphism",
                    "Operator overloading",
                    "Templates (generic programming)",
                    "STL: vectors, maps, sets, algorithms",
                    "Smart pointers (unique_ptr, shared_ptr)",
                    "Exception handling",
                    "File I/O",
                    "Build a small game or utility"
                ],
                "resources": [
                    {"type": "docs",    "title": "learncpp.com",                 "url": "https://www.learncpp.com/"},
                    {"type": "video",   "title": "C++ STL (The Cherno)",         "url": "https://www.youtube.com/c/TheChernoProject"},
                    {"type": "practice","title": "Codeforces Problems",          "url": "https://codeforces.com/"}
                ]
            },
            "expert": {
                "duration" : "8 weeks",
                "roadmap"  : [
                    "Move semantics aur rvalue references",
                    "Concurrency (threads, mutex, atomic)",
                    "Memory management deep dive",
                    "Metaprogramming (SFINAE, constexpr)",
                    "Design patterns in C++",
                    "Profiling aur optimization",
                    "CMake build system",
                    "Contribute to open source C++ project"
                ],
                "resources": [
                    {"type": "docs",    "title": "ISO C++ Standard Docs",        "url": "https://isocpp.org/"},
                    {"type": "video",   "title": "CppCon Talks",                 "url": "https://www.youtube.com/user/CppCon"},
                    {"type": "practice","title": "LeetCode C++",                 "url": "https://leetcode.com/"}
                ]
            }
        }
    },

    "web development": {
        "title"      : "Web Development",
        "description": "Websites aur web apps banana — frontend (UI) se backend (server) tak.",
        "levels": {
            "beginner": {
                "duration" : "5 weeks",
                "roadmap"  : [
                    "HTML structure samjho (tags, forms, tables)",
                    "CSS styling (selectors, flexbox, grid)",
                    "Responsive design (media queries)",
                    "JavaScript basics (variables, DOM manipulation)",
                    "Simple static website banao",
                    "Git aur GitHub basics",
                    "Deploy on GitHub Pages"
                ],
                "resources": [
                    {"type": "docs",    "title": "MDN Web Docs",                 "url": "https://developer.mozilla.org/en-US/docs/Web"},
                    {"type": "docs",    "title": "W3Schools HTML/CSS/JS",        "url": "https://www.w3schools.com/"},
                    {"type": "video",   "title": "Web Dev for Beginners (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=zJSY8tbf_ys"},
                    {"type": "practice","title": "Frontend Mentor Challenges",   "url": "https://www.frontendmentor.io/"}
                ]
            },
            "intermediate": {
                "duration" : "8 weeks",
                "roadmap"  : [
                    "JavaScript advanced (ES6+, Promises, async/await)",
                    "React.js fundamentals (components, hooks, state)",
                    "REST APIs consume karna (fetch/axios)",
                    "Node.js + Express backend banana",
                    "MongoDB integration",
                    "Authentication (JWT)",
                    "Full stack project deploy karo"
                ],
                "resources": [
                    {"type": "docs",    "title": "React Official Docs",          "url": "https://react.dev/"},
                    {"type": "docs",    "title": "Node.js Docs",                 "url": "https://nodejs.org/en/docs"},
                    {"type": "video",   "title": "MERN Stack (Traversy Media)",  "url": "https://www.youtube.com/watch?v=-0exw-9YJBo"},
                    {"type": "practice","title": "Full Stack Open Course",       "url": "https://fullstackopen.com/en/"}
                ]
            },
            "expert": {
                "duration" : "10 weeks",
                "roadmap"  : [
                    "Next.js (SSR, SSG, App Router)",
                    "TypeScript",
                    "State management (Redux / Zustand)",
                    "Testing (Jest, React Testing Library)",
                    "Performance optimization (lazy loading, caching)",
                    "CI/CD pipeline",
                    "Docker containerization",
                    "Cloud deployment (AWS/Vercel/Render)"
                ],
                "resources": [
                    {"type": "docs",    "title": "Next.js Docs",                 "url": "https://nextjs.org/docs"},
                    {"type": "docs",    "title": "TypeScript Handbook",          "url": "https://www.typescriptlang.org/docs/"},
                    {"type": "video",   "title": "Next.js Full Course",          "url": "https://www.youtube.com/results?search_query=nextjs+full+course"},
                    {"type": "practice","title": "Build & Deploy Projects",      "url": "https://www.frontendmentor.io/challenges"}
                ]
            }
        }
    },

    "cybersecurity": {
        "title"      : "Cybersecurity",
        "description": "Systems, networks aur data ko attacks se protect karna.",
        "levels": {
            "beginner": {
                "duration" : "4 weeks",
                "roadmap"  : [
                    "Cybersecurity fundamentals samjho",
                    "Networking basics (TCP/IP, DNS, HTTP)",
                    "Linux command line basics",
                    "Common threats: phishing, malware, ransomware",
                    "Password security aur 2FA",
                    "Basic cryptography (hashing, encryption)",
                    "TryHackMe beginner rooms complete karo"
                ],
                "resources": [
                    {"type": "docs",    "title": "OWASP Top 10",                 "url": "https://owasp.org/www-project-top-ten/"},
                    {"type": "video",   "title": "Cybersecurity for Beginners",  "url": "https://www.youtube.com/watch?v=U_P23SqJaDc"},
                    {"type": "practice","title": "TryHackMe",                    "url": "https://tryhackme.com/"},
                    {"type": "practice","title": "Cybrary Free Courses",         "url": "https://www.cybrary.it/"}
                ]
            },
            "intermediate": {
                "duration" : "6 weeks",
                "roadmap"  : [
                    "Network security (firewalls, VPN, IDS/IPS)",
                    "Web app security (XSS, SQL injection, CSRF)",
                    "Penetration testing basics (Kali Linux)",
                    "Vulnerability scanning (Nmap, Nessus)",
                    "Incident response process",
                    "Security certifications prep (CompTIA Security+)"
                ],
                "resources": [
                    {"type": "docs",    "title": "NIST Cybersecurity Framework", "url": "https://www.nist.gov/cyberframework"},
                    {"type": "video",   "title": "Ethical Hacking (TCM Security)", "url": "https://www.youtube.com/c/TCMSecurityAcademy"},
                    {"type": "practice","title": "HackTheBox",                   "url": "https://www.hackthebox.com/"}
                ]
            },
            "expert": {
                "duration" : "10 weeks",
                "roadmap"  : [
                    "Advanced penetration testing",
                    "Exploit development",
                    "Malware analysis",
                    "Security operations (SIEM, SOC)",
                    "Cloud security (AWS/Azure security)",
                    "Zero-day research",
                    "Bug bounty programs",
                    "CEH / OSCP certification"
                ],
                "resources": [
                    {"type": "docs",    "title": "MITRE ATT&CK Framework",       "url": "https://attack.mitre.org/"},
                    {"type": "video",   "title": "Advanced Ethical Hacking",     "url": "https://www.youtube.com/results?search_query=advanced+ethical+hacking"},
                    {"type": "practice","title": "Bug Bounty (HackerOne)",        "url": "https://www.hackerone.com/"}
                ]
            }
        }
    },

    "cloud computing": {
        "title"      : "Cloud Computing",
        "description": "Internet ke through computing resources access karna — AWS, Azure, GCP.",
        "levels": {
            "beginner": {
                "duration" : "4 weeks",
                "roadmap"  : [
                    "Cloud computing concepts (IaaS, PaaS, SaaS)",
                    "AWS free tier account banao",
                    "EC2 (virtual machines) setup karo",
                    "S3 (storage) use karo",
                    "IAM (users, roles, permissions)",
                    "Basic networking in cloud (VPC, subnets)",
                    "AWS Certified Cloud Practitioner prep"
                ],
                "resources": [
                    {"type": "docs",    "title": "AWS Documentation",            "url": "https://docs.aws.amazon.com/"},
                    {"type": "video",   "title": "AWS for Beginners (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=ubCNZFQZZWw"},
                    {"type": "practice","title": "AWS Free Tier Hands-on",       "url": "https://aws.amazon.com/free/"}
                ]
            },
            "intermediate": {
                "duration" : "6 weeks",
                "roadmap"  : [
                    "Docker aur containers",
                    "Kubernetes orchestration",
                    "CI/CD pipelines (GitHub Actions)",
                    "Load balancing aur auto-scaling",
                    "RDS (managed databases)",
                    "CloudWatch (monitoring)",
                    "Serverless (Lambda functions)",
                    "AWS Solutions Architect Associate prep"
                ],
                "resources": [
                    {"type": "docs",    "title": "Kubernetes Docs",              "url": "https://kubernetes.io/docs/home/"},
                    {"type": "video",   "title": "Docker + Kubernetes (TechWorld)", "url": "https://www.youtube.com/c/TechWorldwithNana"},
                    {"type": "practice","title": "Katacoda Cloud Labs",          "url": "https://www.katacoda.com/"}
                ]
            },
            "expert": {
                "duration" : "8 weeks",
                "roadmap"  : [
                    "Multi-cloud strategy",
                    "Infrastructure as Code (Terraform)",
                    "Advanced Kubernetes (Helm, operators)",
                    "Cloud security best practices",
                    "Cost optimization",
                    "Disaster recovery planning",
                    "AWS DevOps Professional certification"
                ],
                "resources": [
                    {"type": "docs",    "title": "Terraform Docs",               "url": "https://developer.hashicorp.com/terraform/docs"},
                    {"type": "video",   "title": "Terraform Full Course",        "url": "https://www.youtube.com/watch?v=7xngnjfIlK4"},
                    {"type": "practice","title": "A Cloud Guru Labs",            "url": "https://acloudguru.com/"}
                ]
            }
        }
    },

    "verbal communication": {
        "title"      : "Verbal Communication",
        "description": "Clearly aur confidently bolna — personal aur professional life mein.",
        "levels": {
            "beginner": {
                "duration" : "3 weeks",
                "roadmap"  : [
                    "Active listening skills develop karo",
                    "Clarity aur conciseness practice karo",
                    "Eye contact aur body language basics",
                    "Daily 5-minute speaking exercises",
                    "Mirror ke saamne practice karo",
                    "Simple conversations initiate karo"
                ],
                "resources": [
                    {"type": "video",   "title": "Communication Skills (Coursera)", "url": "https://www.coursera.org/learn/communication-beginners"},
                    {"type": "video",   "title": "How to Speak (MIT OpenCourseWare)", "url": "https://www.youtube.com/watch?v=Unzc731iCUY"},
                    {"type": "practice","title": "Toastmasters International",   "url": "https://www.toastmasters.org/"}
                ]
            },
            "intermediate": {
                "duration" : "4 weeks",
                "roadmap"  : [
                    "Persuasion techniques seekho",
                    "Storytelling aur structure",
                    "Handling difficult conversations",
                    "Presentation skills",
                    "Giving and receiving feedback",
                    "Recorded practice sessions review karo"
                ],
                "resources": [
                    {"type": "docs",    "title": "Harvard — Difficult Conversations", "url": "https://hbr.org/topic/communication"},
                    {"type": "video",   "title": "Public Speaking Tips (TED)",   "url": "https://www.ted.com/playlists/226/before_public_speaking"},
                    {"type": "practice","title": "Speeko App",                   "url": "https://speeko.co/"}
                ]
            },
            "expert": {
                "duration" : "5 weeks",
                "roadmap"  : [
                    "Negotiation mastery",
                    "Cross-cultural communication",
                    "Leadership communication",
                    "Crisis communication",
                    "Media/press communication",
                    "Conduct workshops aur seminars"
                ],
                "resources": [
                    {"type": "docs",    "title": "Harvard Negotiation Project",  "url": "https://www.pon.harvard.edu/"},
                    {"type": "video",   "title": "Advanced Communication (LinkedIn Learning)", "url": "https://www.linkedin.com/learning/topics/communication"},
                    {"type": "practice","title": "Debate Clubs / MUNs",          "url": "https://www.mun.ca/"}
                ]
            }
        }
    },

    "english grammar": {
        "title"      : "English Grammar",
        "description": "English language ka proper usage — writing aur speaking dono ke liye.",
        "levels": {
            "beginner": {
                "duration" : "3 weeks",
                "roadmap"  : [
                    "Parts of speech (noun, verb, adjective, etc.)",
                    "Basic sentence structure",
                    "Tenses (present, past, future)",
                    "Articles (a, an, the)",
                    "Punctuation basics",
                    "Daily writing practice (diary/journal)"
                ],
                "resources": [
                    {"type": "docs",    "title": "Grammarly Handbook",           "url": "https://www.grammarly.com/blog/category/handbook/"},
                    {"type": "docs",    "title": "British Council Grammar",      "url": "https://learnenglish.britishcouncil.org/grammar"},
                    {"type": "video",   "title": "English Grammar (BBC Learning)", "url": "https://www.bbc.co.uk/learningenglish/"},
                    {"type": "practice","title": "Duolingo English",             "url": "https://www.duolingo.com/"}
                ]
            },
            "intermediate": {
                "duration" : "4 weeks",
                "roadmap"  : [
                    "Complex sentences aur clauses",
                    "Active vs Passive voice",
                    "Direct aur indirect speech",
                    "Conditional sentences",
                    "Phrasal verbs",
                    "Essay writing structure"
                ],
                "resources": [
                    {"type": "docs",    "title": "Purdue OWL Writing Lab",       "url": "https://owl.purdue.edu/owl/general_writing/"},
                    {"type": "video",   "title": "Intermediate Grammar (engVid)", "url": "https://www.engvid.com/"},
                    {"type": "practice","title": "Grammar Quizzes Online",       "url": "https://www.grammarbook.com/"}
                ]
            },
            "expert": {
                "duration" : "5 weeks",
                "roadmap"  : [
                    "Advanced syntax aur style",
                    "Academic writing",
                    "Business writing",
                    "Editing aur proofreading",
                    "Style guides (APA, MLA, Chicago)",
                    "Write aur publish articles"
                ],
                "resources": [
                    {"type": "docs",    "title": "The Elements of Style",        "url": "https://www.bartleby.com/141/"},
                    {"type": "video",   "title": "Academic Writing (Coursera)",  "url": "https://www.coursera.org/learn/writing-and-editing"},
                    {"type": "practice","title": "Write for Medium/LinkedIn",    "url": "https://medium.com/"}
                ]
            }
        }
    },

    "psychology": {
        "title"      : "Psychology",
        "description": "Human mind, behavior aur emotions ka scientific study.",
        "levels": {
            "beginner": {
                "duration" : "4 weeks",
                "roadmap"  : [
                    "Psychology kya hai — basic concepts",
                    "Major psychological theories",
                    "Perception, memory, learning",
                    "Emotions aur motivation",
                    "Personality types",
                    "Introduction to mental health"
                ],
                "resources": [
                    {"type": "docs",    "title": "Simply Psychology",            "url": "https://www.simplypsychology.org/"},
                    {"type": "video",   "title": "Intro to Psychology (Crash Course)", "url": "https://www.youtube.com/playlist?list=PL8dPuuaLjXtOPRKzVLY0jJY-uHOH9KVU6"},
                    {"type": "practice","title": "Psychology Today",             "url": "https://www.psychologytoday.com/"}
                ]
            },
            "intermediate": {
                "duration" : "5 weeks",
                "roadmap"  : [
                    "Cognitive psychology deep dive",
                    "Social psychology aur group behavior",
                    "Behaviorism vs Humanism",
                    "Developmental psychology",
                    "Abnormal psychology basics",
                    "Research methods in psychology"
                ],
                "resources": [
                    {"type": "docs",    "title": "APA Psychology Resources",    "url": "https://www.apa.org/topics"},
                    {"type": "video",   "title": "Social Psychology (Coursera)", "url": "https://www.coursera.org/learn/social-psychology"},
                    {"type": "practice","title": "Khan Academy Psychology",      "url": "https://www.khanacademy.org/science/ap-psychology"}
                ]
            },
            "expert": {
                "duration" : "8 weeks",
                "roadmap"  : [
                    "Psychoanalytic theory (Freud, Jung)",
                    "Cognitive behavioral therapy (CBT)",
                    "Neuropsychology",
                    "Psychological assessment methods",
                    "Ethics in psychology",
                    "Research paper padhna aur likhna",
                    "Case studies analyze karo"
                ],
                "resources": [
                    {"type": "docs",    "title": "NCBI Psychology Papers",       "url": "https://pubmed.ncbi.nlm.nih.gov/"},
                    {"type": "video",   "title": "Clinical Psychology (Yale)",   "url": "https://oyc.yale.edu/psychology"},
                    {"type": "practice","title": "ResearchGate Psychology",      "url": "https://www.researchgate.net/"}
                ]
            }
        }
    },

    "economics": {
        "title"      : "Economics",
        "description": "Resources ka allocation, production, consumption aur trade ka study.",
        "levels": {
            "beginner": {
                "duration" : "4 weeks",
                "roadmap"  : [
                    "Economics kya hai — micro vs macro",
                    "Demand aur supply",
                    "Market types",
                    "Price, inflation, GDP basics",
                    "Trade aur money basics",
                    "Indian economy overview"
                ],
                "resources": [
                    {"type": "docs",    "title": "Investopedia Economics",       "url": "https://www.investopedia.com/economics-4689800"},
                    {"type": "video",   "title": "Economics (Crash Course)",     "url": "https://www.youtube.com/playlist?list=PL1oDmcs0xTD-dJN1PL2N1urX0EKupBJkQ"},
                    {"type": "practice","title": "Khan Academy Economics",       "url": "https://www.khanacademy.org/economics-finance-domain"}
                ]
            },
            "intermediate": {
                "duration" : "6 weeks",
                "roadmap"  : [
                    "Microeconomics deep dive (elasticity, costs)",
                    "Macroeconomics (fiscal + monetary policy)",
                    "International trade theory",
                    "Economic models aur graphs",
                    "Unemployment aur inflation relationship",
                    "Indian budget aur policies"
                ],
                "resources": [
                    {"type": "docs",    "title": "NCERT Economics Books",        "url": "https://ncert.nic.in/textbook.php"},
                    {"type": "video",   "title": "Intermediate Economics (MIT)", "url": "https://ocw.mit.edu/courses/economics/"},
                    {"type": "practice","title": "Economics Quiz (ProProfs)",    "url": "https://www.proprofs.com/quiz-school/topic/economics"}
                ]
            },
            "expert": {
                "duration" : "8 weeks",
                "roadmap"  : [
                    "Econometrics (data + economics)",
                    "Game theory",
                    "Behavioral economics",
                    "Financial markets aur instruments",
                    "Economic research paper likhna",
                    "Policy analysis"
                ],
                "resources": [
                    {"type": "docs",    "title": "NBER Working Papers",          "url": "https://www.nber.org/papers"},
                    {"type": "video",   "title": "Advanced Economics (Yale)",    "url": "https://oyc.yale.edu/economics"},
                    {"type": "practice","title": "World Bank Open Data",         "url": "https://data.worldbank.org/"}
                ]
            }
        }
    },

    "geography": {
        "title"      : "Geography",
        "description": "Earth ki physical features, climate, population aur human activities ka study.",
        "levels": {
            "beginner": {
                "duration" : "3 weeks",
                "roadmap"  : [
                    "Physical geography basics (continents, oceans)",
                    "Maps, latitude, longitude samjho",
                    "Climate zones",
                    "Natural resources",
                    "India ka geography overview",
                    "World capitals aur countries"
                ],
                "resources": [
                    {"type": "docs",    "title": "National Geographic",          "url": "https://www.nationalgeographic.com/"},
                    {"type": "video",   "title": "Geography (Crash Course)",     "url": "https://www.youtube.com/playlist?list=PL8dPuuaLjXtO85OEsty4Yml284k_eqh2B"},
                    {"type": "practice","title": "Seterra Geography Games",      "url": "https://www.seterra.com/"}
                ]
            },
            "intermediate": {
                "duration" : "4 weeks",
                "roadmap"  : [
                    "Plate tectonics aur earthquakes",
                    "Weathering, erosion, landforms",
                    "Population geography",
                    "Urbanization aur migration",
                    "Agricultural patterns",
                    "GIS basics"
                ],
                "resources": [
                    {"type": "docs",    "title": "USGS Geography Resources",     "url": "https://www.usgs.gov/"},
                    {"type": "video",   "title": "Physical Geography (Dr. Baber)", "url": "https://www.youtube.com/results?search_query=physical+geography+lectures"},
                    {"type": "practice","title": "GIS Tutorial (Esri)",          "url": "https://learn.arcgis.com/"}
                ]
            },
            "expert": {
                "duration" : "6 weeks",
                "roadmap"  : [
                    "Remote sensing aur satellite data",
                    "Climate change analysis",
                    "Geopolitics aur international relations",
                    "Urban planning",
                    "Environmental geography",
                    "Research paper likhna"
                ],
                "resources": [
                    {"type": "docs",    "title": "UN Environment Programme",     "url": "https://www.unep.org/"},
                    {"type": "video",   "title": "Advanced GIS (Esri MOOC)",     "url": "https://www.esri.com/training/mooc/"},
                    {"type": "practice","title": "Google Earth Engine",          "url": "https://earthengine.google.com/"}
                ]
            }
        }
    },

    "history": {
        "title"      : "History",
        "description": "Past events, civilizations aur unka aaj par impact ka study.",
        "levels": {
            "beginner": {
                "duration" : "3 weeks",
                "roadmap"  : [
                    "Ancient civilizations (Egypt, Indus, Mesopotamia)",
                    "Indian history overview",
                    "World history timeline",
                    "Important historical figures",
                    "Primary vs secondary sources samjho"
                ],
                "resources": [
                    {"type": "docs",    "title": "World History Encyclopedia",   "url": "https://www.worldhistory.org/"},
                    {"type": "video",   "title": "World History (Crash Course)", "url": "https://www.youtube.com/playlist?list=PLBDA2E52FB1EF80C9"},
                    {"type": "practice","title": "Khan Academy History",         "url": "https://www.khanacademy.org/humanities/world-history"}
                ]
            },
            "intermediate": {
                "duration" : "5 weeks",
                "roadmap"  : [
                    "Medieval history",
                    "Industrial Revolution",
                    "World War I aur II",
                    "Colonialism aur independence movements",
                    "Cold War era",
                    "Modern India history (1857–1947)"
                ],
                "resources": [
                    {"type": "docs",    "title": "NCERT History Books",          "url": "https://ncert.nic.in/textbook.php"},
                    {"type": "video",   "title": "Modern History (Yale OYC)",    "url": "https://oyc.yale.edu/history"},
                    {"type": "practice","title": "History Quiz (ProProfs)",      "url": "https://www.proprofs.com/quiz-school/topic/history"}
                ]
            },
            "expert": {
                "duration" : "8 weeks",
                "roadmap"  : [
                    "Historiography (history of history writing)",
                    "Post-colonial studies",
                    "Economic history",
                    "Comparative history methodology",
                    "Primary source research",
                    "Academic paper likhna"
                ],
                "resources": [
                    {"type": "docs",    "title": "JSTOR History Articles",       "url": "https://www.jstor.org/"},
                    {"type": "video",   "title": "Advanced Historical Methods",  "url": "https://www.youtube.com/results?search_query=historiography+lectures"},
                    {"type": "practice","title": "Harvard History Resources",    "url": "https://history.harvard.edu/"}
                ]
            }
        }
    },

    "political science": {
        "title"      : "Political Science",
        "description": "Government systems, political behavior aur public policy ka study.",
        "levels": {
            "beginner": {
                "duration" : "3 weeks",
                "roadmap"  : [
                    "Political science kya hai",
                    "Types of government (democracy, monarchy, etc.)",
                    "Indian Constitution basics",
                    "Fundamental rights aur duties",
                    "Parliament structure",
                    "Elections aur voting system"
                ],
                "resources": [
                    {"type": "docs",    "title": "India.gov.in Constitution",    "url": "https://india.gov.in/my-government/constitution-india"},
                    {"type": "video",   "title": "Political Science (Crash Course)", "url": "https://www.youtube.com/playlist?list=PL8dPuuaLjXtOPRKzVLY0jJY-uHOH9KVU6"},
                    {"type": "practice","title": "Khan Academy Civics",          "url": "https://www.khanacademy.org/humanities/us-government-and-civics"}
                ]
            },
            "intermediate": {
                "duration" : "5 weeks",
                "roadmap"  : [
                    "Political ideologies (liberalism, conservatism, socialism)",
                    "Federalism aur separation of powers",
                    "International relations basics",
                    "Public policy process",
                    "Comparative politics",
                    "Indian political parties"
                ],
                "resources": [
                    {"type": "docs",    "title": "NCERT Political Science",      "url": "https://ncert.nic.in/textbook.php"},
                    {"type": "video",   "title": "Political Theory (Yale OYC)",  "url": "https://oyc.yale.edu/political-science"},
                    {"type": "practice","title": "Political Science Quiz",       "url": "https://www.proprofs.com/quiz-school/topic/political-science"}
                ]
            },
            "expert": {
                "duration" : "8 weeks",
                "roadmap"  : [
                    "Political philosophy (Rawls, Machiavelli, Locke)",
                    "Geopolitics aur international law",
                    "Electoral systems comparison",
                    "Diplomacy aur foreign policy",
                    "Research methodology in political science",
                    "Policy paper likhna"
                ],
                "resources": [
                    {"type": "docs",    "title": "UN International Law",         "url": "https://www.un.org/en/global-issues/international-law"},
                    {"type": "video",   "title": "Advanced Political Theory",    "url": "https://www.youtube.com/results?search_query=political+philosophy+lectures"},
                    {"type": "practice","title": "Council on Foreign Relations", "url": "https://www.cfr.org/"}
                ]
            }
        }
    }
}


# ================================================================
# MAIN FUNCTION: Get Learning Roadmap
# ================================================================
def get_learning_roadmap(skill, level="beginner"):
    """
    Skill aur level ke basis pe learning roadmap return karta hai.

    Args:
        skill (str): e.g. "python", "web development"
        level (str): "beginner" / "intermediate" / "expert"

    Returns:
        dict: Full roadmap with resources
    """

    skill_key = skill.lower().strip()
    level_key = level.lower().strip()

    # -------- SKILL NOT FOUND -------- #
    if skill_key not in LEARNING_DATA:
        # Fuzzy match try karo
        close = [k for k in LEARNING_DATA if skill_key in k or k in skill_key]
        if close:
            skill_key = close[0]
        else:
            return {
                "error"            : f"'{skill}' skill ka roadmap abhi available nahi hai.",
                "available_skills" : list(LEARNING_DATA.keys())
            }

    # -------- LEVEL NOT FOUND -------- #
    valid_levels = ["beginner", "intermediate", "expert"]
    if level_key not in valid_levels:
        return {
            "error"         : f"Invalid level '{level}'. Choose: beginner, intermediate, expert",
            "valid_levels"  : valid_levels
        }

    skill_data  = LEARNING_DATA[skill_key]
    level_data  = skill_data["levels"][level_key]

    return {
        "skill"       : skill_data["title"],
        "description" : skill_data["description"],
        "level"       : level_key,
        "duration"    : level_data["duration"],
        "roadmap"     : level_data["roadmap"],
        "resources"   : level_data["resources"],
        "total_steps" : len(level_data["roadmap"])
    }


# ================================================================
# AVAILABLE SKILLS LIST
# ================================================================
def get_available_skills():
    return {
        "skills": list(LEARNING_DATA.keys()),
        "total" : len(LEARNING_DATA)
    }


# -------- DIRECT RUN → Quick test -------- #
if __name__ == "__main__":
    import json
    result = get_learning_roadmap("python", "beginner")
    print(json.dumps(result, indent=2))
