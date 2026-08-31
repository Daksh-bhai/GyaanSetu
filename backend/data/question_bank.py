question_bank = {
    "IT": {
        "Python": {
            "beginner": [
                {"question":"What is Python primarily used for?","options":["Web development","Programming language","Operating system","Database"],"answer":"Programming language"},
                {"question":"Which keyword is used to define a function in Python?","options":["func","define","def","function"],"answer":"def"},
                {"question":"Which of the following is a correct file extension for Python?","options":[".py",".java",".cpp",".txt"],"answer":".py"},
                {"question":"Which data type is used to store text in Python?","options":["int","str","float","bool"],"answer":"str"},
                {"question":"Which symbol is used to write a comment in Python?","options":["#","//","/*","--"],"answer":"#"},
                {"question":"What does the print() function do in Python?","options":["Takes input","Displays output","Stores data","Deletes data"],"answer":"Displays output"},
                {"question":"Which of the following is a Boolean value in Python?","options":["Yes","1","True","On"],"answer":"True"},
                {"question":"What is the correct way to declare a variable in Python?","options":["int x=5","x=5","declare x=5","var x=5"],"answer":"x=5"},
                {"question":"Is indentation required in Python?","options":["Yes","No","Optional","Only for loops"],"answer":"Yes"},
                {"question":"Which of the following is a list in Python?","options":["(1,2,3)","{1,2,3}","[1,2,3]","<1,2,3>"],"answer":"[1,2,3]"}
            ],
            "intermediate": [
                {"question":"What is a tuple in Python?","options":["Mutable collection","Immutable collection","Loop","Function"],"answer":"Immutable collection"},
                {"question":"Which keyword is used for exception handling in Python?","options":["try","catch","error","handle"],"answer":"try"},
                {"question":"What does the len() function return?","options":["Length","Type","Value","Index"],"answer":"Length"},
                {"question":"What is a dictionary in Python?","options":["List of values","Key-value pairs","Tuple","Set"],"answer":"Key-value pairs"},
                {"question":"Which loop is used to iterate over a sequence in Python?","options":["repeat","for","loop","iterate"],"answer":"for"},
                {"question":"What is list comprehension in Python?","options":["Loop","Short syntax for creating lists","Function","Error"],"answer":"Short syntax for creating lists"},
                {"question":"What is the purpose of the 'self' keyword in Python?","options":["Refers to current object","Loop variable","Function name","Class name"],"answer":"Refers to current object"},
                {"question":"What does the 'break' statement do?","options":["Ends loop","Skips iteration","Prints output","Starts loop"],"answer":"Ends loop"},
                {"question":"Which data structure stores only unique values?","options":["List","Tuple","Set","Dictionary"],"answer":"Set"},
                {"question":"What is a module in Python?","options":["Function","File containing code","Loop","Class"],"answer":"File containing code"}
            ],
            "expert": [
                {"question":"What is the purpose of the Global Interpreter Lock (GIL) in Python?","options":["Memory management","Thread control","Loop execution","Compilation"],"answer":"Thread control"},
                {"question":"What is a decorator in Python?","options":["Function wrapper","Loop","Class","Variable"],"answer":"Function wrapper"},
                {"question":"What is the use of the '__init__' method?","options":["Destructor","Constructor","Loop","None"],"answer":"Constructor"},
                {"question":"Which keyword is used to create a generator in Python?","options":["return","yield","break","pass"],"answer":"yield"},
                {"question":"What is the purpose of virtual environments in Python?","options":["Speed","Isolation of dependencies","Memory","Compilation"],"answer":"Isolation of dependencies"},
                {"question":"What is asynchronous programming used for?","options":["Parallel execution","Looping","Error handling","Compilation"],"answer":"Parallel execution"},
                {"question":"What is a metaclass in Python?","options":["Class of a class","Function","Loop","Variable"],"answer":"Class of a class"},
                {"question":"What does the pickle module do?","options":["Encryption","Serialization","Loop","Sorting"],"answer":"Serialization"},
                {"question":"What is the purpose of context managers?","options":["Resource handling","Looping","Printing","Sorting"],"answer":"Resource handling"},
                {"question":"What is the main advantage of using generators?","options":["Faster loops","Memory efficiency","Better syntax","Compilation"],"answer":"Memory efficiency"}
            ]
        },
        "C++": {
            "beginner": [
                {"question":"What is C++ primarily used for?","options":["Web browsing","Programming","Gaming only","Networking"],"answer":"Programming"},
                {"question":"Which function is the entry point of a C++ program?","options":["start()","main()","run()","init()"],"answer":"main()"},
                {"question":"Which keyword is used to include libraries in C++?","options":["import","#include","using","define"],"answer":"#include"},
                {"question":"Which operator is used for output in C++?","options":["<<",">>","==","="],"answer":"<<"},
                {"question":"What does a variable store?","options":["Function","Value","Loop","Class"],"answer":"Value"},
                {"question":"Which symbol is used for single-line comments?","options":["#","//","/*","--"],"answer":"//"},
                {"question":"Which data type is used for integers?","options":["int","float","char","bool"],"answer":"int"},
                {"question":"Which loop is used in C++?","options":["for","repeat","loop","iterate"],"answer":"for"},
                {"question":"Which keyword is used to return a value?","options":["exit","stop","return","break"],"answer":"return"},
                {"question":"What does 'cout' do?","options":["Input","Output","Loop","Store"],"answer":"Output"}
            ],
            "intermediate": [
                {"question":"What does OOP stand for?","options":["Object Oriented Programming","Only Object Programming","Open Oriented Programming","None"],"answer":"Object Oriented Programming"},
                {"question":"What is a class in C++?","options":["Blueprint","Function","Loop","Variable"],"answer":"Blueprint"},
                {"question":"What is encapsulation?","options":["Data hiding","Looping","Sorting","None"],"answer":"Data hiding"},
                {"question":"What is inheritance used for?","options":["Reusability","Looping","Sorting","None"],"answer":"Reusability"},
                {"question":"What is polymorphism?","options":["Many forms","Loop","Error","None"],"answer":"Many forms"},
                {"question":"What does a pointer store?","options":["Value","Address","Loop","Class"],"answer":"Address"},
                {"question":"Which symbol represents a reference?","options":["&","*","#","%"],"answer":"&"},
                {"question":"What is a constructor used for?","options":["Initialization","Destruction","Looping","None"],"answer":"Initialization"},
                {"question":"What is a destructor used for?","options":["Destroy object","Create object","Loop","None"],"answer":"Destroy object"},
                {"question":"What is a namespace used for?","options":["Avoid naming conflicts","Loop","Error","None"],"answer":"Avoid naming conflicts"}
            ],
            "expert": [
                {"question":"What is the Standard Template Library (STL)?","options":["Library of templates","Loop","Error","None"],"answer":"Library of templates"},
                {"question":"What is a vector in C++?","options":["Dynamic array","Static array","Loop","None"],"answer":"Dynamic array"},
                {"question":"What does a map store?","options":["Key-value pairs","List","Loop","None"],"answer":"Key-value pairs"},
                {"question":"What is heap memory used for?","options":["Dynamic allocation","Static allocation","Loop","None"],"answer":"Dynamic allocation"},
                {"question":"What is stack memory used for?","options":["Static allocation","Dynamic allocation","Loop","None"],"answer":"Static allocation"},
                {"question":"What is a smart pointer?","options":["Automatic memory management","Loop","Error","None"],"answer":"Automatic memory management"},
                {"question":"What is a template in C++?","options":["Generic programming","Loop","Error","None"],"answer":"Generic programming"},
                {"question":"What is operator overloading?","options":["Custom operator behavior","Loop","Error","None"],"answer":"Custom operator behavior"},
                {"question":"What is a friend function?","options":["Access private members","Loop","Error","None"],"answer":"Access private members"},
                {"question":"What is inline function?","options":["Faster execution","Loop","Error","None"],"answer":"Faster execution"}
            ]
        },
        "Java": {
            "beginner": [
                {"question":"What is Java mainly used for?","options":["Programming","Gaming only","Networking","Database"],"answer":"Programming"},
                {"question":"Which method is the entry point of a Java program?","options":["main()","start()","run()","init()"],"answer":"main()"},
                {"question":"What does JVM stand for?","options":["Java Virtual Machine","Java Variable Method","Just Virtual Machine","None"],"answer":"Java Virtual Machine"},
                {"question":"Which keyword is used to define a class?","options":["class","define","object","struct"],"answer":"class"},
                {"question":"Which function is used for output?","options":["print()","System.out.println()","echo()","write()"],"answer":"System.out.println()"},
                {"question":"Which data type stores integers?","options":["int","float","char","bool"],"answer":"int"},
                {"question":"Which loop is used in Java?","options":["for","repeat","loop","iterate"],"answer":"for"},
                {"question":"Which symbol is used for comments?","options":["//","#","--","/*"],"answer":"//"},
                {"question":"What is an object in Java?","options":["Instance of class","Loop","Function","Variable"],"answer":"Instance of class"},
                {"question":"What is a class?","options":["Blueprint","Loop","Function","Variable"],"answer":"Blueprint"}
            ],
            "intermediate": [
                {"question":"What is encapsulation in Java?","options":["Data hiding","Looping","Sorting","None"],"answer":"Data hiding"},
                {"question":"What is inheritance used for?","options":["Reusability","Loop","Error","None"],"answer":"Reusability"},
                {"question":"What is polymorphism?","options":["Many forms","Loop","Error","None"],"answer":"Many forms"},
                {"question":"What is an interface?","options":["Abstract type","Loop","Error","None"],"answer":"Abstract type"},
                {"question":"What is an abstract class?","options":["Incomplete class","Loop","Error","None"],"answer":"Incomplete class"},
                {"question":"What is exception handling used for?","options":["Handling errors","Loop","None","Both"],"answer":"Handling errors"},
                {"question":"What is an array?","options":["Collection of elements","Loop","Error","None"],"answer":"Collection of elements"},
                {"question":"What is a string in Java?","options":["Immutable","Mutable","None","Both"],"answer":"Immutable"},
                {"question":"What is a package?","options":["Group of classes","Loop","Error","None"],"answer":"Group of classes"},
                {"question":"What is method overloading?","options":["Same name different parameters","Loop","Error","None"],"answer":"Same name different parameters"}
            ],
            "expert": [
                {"question":"What is Just-In-Time (JIT) compiler?","options":["Runtime compilation","Loop","Error","None"],"answer":"Runtime compilation"},
                {"question":"What is garbage collection?","options":["Automatic memory management","Loop","Error","None"],"answer":"Automatic memory management"},
                {"question":"What is multithreading?","options":["Parallel execution","Loop","Error","None"],"answer":"Parallel execution"},
                {"question":"What is synchronization?","options":["Thread safety","Loop","Error","None"],"answer":"Thread safety"},
                {"question":"What is Stream API used for?","options":["Data processing","Loop","Error","None"],"answer":"Data processing"},
                {"question":"What is lambda expression?","options":["Function","Loop","Error","None"],"answer":"Function"},
                {"question":"What is reflection?","options":["Inspect classes","Loop","Error","None"],"answer":"Inspect classes"},
                {"question":"What is serialization?","options":["Object to byte stream","Loop","Error","None"],"answer":"Object to byte stream"},
                {"question":"What is Executor framework?","options":["Thread pool management","Loop","Error","None"],"answer":"Thread pool management"},
                {"question":"What is Spring framework?","options":["Java framework","Loop","Error","None"],"answer":"Java framework"}
            ]
        },
        "Web Development": {
            "beginner": [
                {"question":"What does HTML stand for?","options":["Hyper Text Markup Language","High Text Machine Language","Hyper Tool Mark Language","None"],"answer":"Hyper Text Markup Language"},
                {"question":"What is the main purpose of CSS?","options":["Styling web pages","Programming logic","Database management","Server handling"],"answer":"Styling web pages"},
                {"question":"Which language is used for client-side scripting?","options":["JavaScript","Python","Java","C++"],"answer":"JavaScript"},
                {"question":"Which HTML tag is used to create a hyperlink?","options":["<a>","<link>","<href>","<url>"],"answer":"<a>"},
                {"question":"Which HTML tag is used to display an image?","options":["<img>","<image>","<src>","<pic>"],"answer":"<img>"},
                {"question":"What does HTTP stand for?","options":["HyperText Transfer Protocol","High Transfer Text Protocol","Hyper Tool Transfer Protocol","None"],"answer":"HyperText Transfer Protocol"},
                {"question":"Which part of a website handles user interaction?","options":["Frontend","Backend","Database","Server"],"answer":"Frontend"},
                {"question":"What is a browser used for?","options":["Displaying web pages","Storing data","Programming","Networking"],"answer":"Displaying web pages"},
                {"question":"Which CSS property changes text color?","options":["color","font","text","background"],"answer":"color"},
                {"question":"Which HTML tag is used for headings?","options":["<h1>","<p>","<div>","<span>"],"answer":"<h1>"}
            ],
            "intermediate": [
                {"question":"What is the DOM in web development?","options":["Document Object Model","Data Object Model","Design Object Model","None"],"answer":"Document Object Model"},
                {"question":"What is Flexbox used for?","options":["Layout design","Database","Logic","Animation"],"answer":"Layout design"},
                {"question":"What is an API in web development?","options":["Interface between systems","Database","Programming language","Server"],"answer":"Interface between systems"},
                {"question":"What is JSON used for?","options":["Data exchange","Styling","Looping","None"],"answer":"Data exchange"},
                {"question":"What is an event in JavaScript?","options":["User action","Loop","Variable","Function"],"answer":"User action"},
                {"question":"What does responsive design mean?","options":["Adapts to screen size","Fast loading","Secure","None"],"answer":"Adapts to screen size"},
                {"question":"What is the fetch() function used for?","options":["Making API requests","Looping","Styling","None"],"answer":"Making API requests"},
                {"question":"What is local storage used for?","options":["Store data in browser","Server storage","Database","None"],"answer":"Store data in browser"},
                {"question":"What does a form do in HTML?","options":["Collect user input","Display data","Style page","None"],"answer":"Collect user input"},
                {"question":"Which HTTP method is used to retrieve data?","options":["GET","POST","PUT","DELETE"],"answer":"GET"}
            ],
            "expert": [
                {"question":"What does REST stand for in web development?","options":["Representational State Transfer","Remote State Transfer","Random State Transfer","None"],"answer":"Representational State Transfer"},
                {"question":"What is JWT used for?","options":["Authentication","Styling","Database","Looping"],"answer":"Authentication"},
                {"question":"What is CORS used for?","options":["Security control","Styling","Looping","Database"],"answer":"Security control"},
                {"question":"What is Server-Side Rendering (SSR)?","options":["Rendering on server","Rendering on client","Styling","None"],"answer":"Rendering on server"},
                {"question":"What is a Single Page Application (SPA)?","options":["One page app","Multiple pages","Database","None"],"answer":"One page app"},
                {"question":"What is Webpack used for?","options":["Bundling files","Styling","Looping","Database"],"answer":"Bundling files"},
                {"question":"What is Babel used for?","options":["Transpiling JS","Styling","Looping","Database"],"answer":"Transpiling JS"},
                {"question":"What is middleware in web apps?","options":["Request handler","Database","Loop","None"],"answer":"Request handler"},
                {"question":"What is a session in web development?","options":["User state","Loop","Error","None"],"answer":"User state"},
                {"question":"What is OAuth used for?","options":["Authorization","Authentication","Loop","None"],"answer":"Authorization"}
            ]
        },
        "Cybersecurity": {
            "beginner": [
                {"question":"What is cybersecurity mainly concerned with?","options":["Protecting systems","Building apps","Designing UI","None"],"answer":"Protecting systems"},
                {"question":"What is a virus in computing?","options":["Malicious software","Safe program","Tool","None"],"answer":"Malicious software"},
                {"question":"What is a firewall used for?","options":["Security","Styling","Looping","Database"],"answer":"Security"},
                {"question":"What is phishing?","options":["Cyber attack","Protection","Backup","None"],"answer":"Cyber attack"},
                {"question":"What is encryption?","options":["Securing data","Deleting data","Copying data","None"],"answer":"Securing data"},
                {"question":"What is antivirus software used for?","options":["Protection","Attack","Loop","None"],"answer":"Protection"},
                {"question":"What is a hacker?","options":["Attacker","User","Developer","None"],"answer":"Attacker"},
                {"question":"What is a data breach?","options":["Data leak","Backup","Protection","None"],"answer":"Data leak"},
                {"question":"What is a strong password?","options":["Secure password","Weak password","Simple password","None"],"answer":"Secure password"},
                {"question":"What is backup used for?","options":["Data recovery","Attack","Loop","None"],"answer":"Data recovery"}
            ],
            "intermediate": [
                {"question":"What does HTTPS provide?","options":["Secure communication","Fast speed","Styling","None"],"answer":"Secure communication"},
                {"question":"What is SQL Injection?","options":["Attack method","Protection","Loop","None"],"answer":"Attack method"},
                {"question":"What is Cross-Site Scripting (XSS)?","options":["Attack","Protection","Loop","None"],"answer":"Attack"},
                {"question":"What is a VPN used for?","options":["Secure network","Styling","Loop","None"],"answer":"Secure network"},
                {"question":"What is authentication?","options":["Verify identity","Grant access","Loop","None"],"answer":"Verify identity"},
                {"question":"What is authorization?","options":["Grant permissions","Verify identity","Loop","None"],"answer":"Grant permissions"},
                {"question":"What is hashing?","options":["One-way encryption","Two-way encryption","Loop","None"],"answer":"One-way encryption"},
                {"question":"What is two-factor authentication?","options":["Extra security","Loop","Error","None"],"answer":"Extra security"},
                {"question":"What is malware?","options":["Malicious software","Safe program","Loop","None"],"answer":"Malicious software"},
                {"question":"What is a threat?","options":["Potential risk","Loop","Error","None"],"answer":"Potential risk"}
            ],
            "expert": [
                {"question":"What is a zero-day vulnerability?","options":["Unknown exploit","Known exploit","Loop","None"],"answer":"Unknown exploit"},
                {"question":"What is penetration testing?","options":["Testing security","Loop","Error","None"],"answer":"Testing security"},
                {"question":"What is IDS (Intrusion Detection System)?","options":["Detect threats","Prevent threats","Loop","None"],"answer":"Detect threats"},
                {"question":"What is SIEM used for?","options":["Security monitoring","Loop","Error","None"],"answer":"Security monitoring"},
                {"question":"What is public key cryptography?","options":["Encryption method","Loop","Error","None"],"answer":"Encryption method"},
                {"question":"What is private key used for?","options":["Decryption","Encryption","Loop","None"],"answer":"Decryption"},
                {"question":"What is CSRF attack?","options":["Security attack","Protection","Loop","None"],"answer":"Security attack"},
                {"question":"What is sandboxing?","options":["Isolation","Loop","Error","None"],"answer":"Isolation"},
                {"question":"What is digital signature used for?","options":["Verification","Loop","Error","None"],"answer":"Verification"},
                {"question":"What is endpoint security?","options":["Device protection","Loop","Error","None"],"answer":"Device protection"}
            ]
        },
        "Cloud Computing": {
            "beginner": [
                {"question":"What is cloud computing?","options":["Remote server usage","Local storage","Programming","None"],"answer":"Remote server usage"},
                {"question":"What is AWS?","options":["Cloud platform","Operating system","Browser","None"],"answer":"Cloud platform"},
                {"question":"What is cloud storage used for?","options":["Store data","Delete data","Loop","None"],"answer":"Store data"},
                {"question":"What is a server?","options":["Host system","Loop","Error","None"],"answer":"Host system"},
                {"question":"What is virtualization?","options":["Creating virtual systems","Loop","Error","None"],"answer":"Creating virtual systems"},
                {"question":"What is a database in cloud?","options":["Store data","Loop","Error","None"],"answer":"Store data"},
                {"question":"What is compute in cloud?","options":["Processing power","Storage","Loop","None"],"answer":"Processing power"},
                {"question":"What type of cloud is public cloud?","options":["Open to public","Private","Hybrid","None"],"answer":"Open to public"},
                {"question":"What is backup in cloud?","options":["Save data","Delete data","Loop","None"],"answer":"Save data"},
                {"question":"What is internet required for cloud?","options":["Yes","No","Optional","None"],"answer":"Yes"}
            ],
            "intermediate": [
                {"question":"What does IaaS stand for?","options":["Infrastructure as a Service","Platform as a Service","Software as a Service","None"],"answer":"Infrastructure as a Service"},
                {"question":"What does PaaS stand for?","options":["Platform as a Service","Infrastructure as a Service","Software as a Service","None"],"answer":"Platform as a Service"},
                {"question":"What does SaaS stand for?","options":["Software as a Service","Platform as a Service","Infrastructure as a Service","None"],"answer":"Software as a Service"},
                {"question":"What is load balancing?","options":["Distributing traffic","Loop","Error","None"],"answer":"Distributing traffic"},
                {"question":"What is scalability?","options":["Increase resources","Decrease resources","Loop","None"],"answer":"Increase resources"},
                {"question":"What is latency?","options":["Delay","Speed","Loop","None"],"answer":"Delay"},
                {"question":"What is CDN used for?","options":["Content delivery","Storage","Loop","None"],"answer":"Content delivery"},
                {"question":"What is Docker used for?","options":["Containers","Loop","Error","None"],"answer":"Containers"},
                {"question":"What is Kubernetes used for?","options":["Container orchestration","Loop","Error","None"],"answer":"Container orchestration"},
                {"question":"What is a container?","options":["Isolated app","Loop","Error","None"],"answer":"Isolated app"}
            ],
            "expert": [
                {"question":"What is serverless computing?","options":["No server management","Server required","Loop","None"],"answer":"No server management"},
                {"question":"What is auto-scaling?","options":["Dynamic scaling","Static scaling","Loop","None"],"answer":"Dynamic scaling"},
                {"question":"What is multi-cloud strategy?","options":["Multiple providers","Single provider","Loop","None"],"answer":"Multiple providers"},
                {"question":"What is disaster recovery?","options":["Restore systems","Delete systems","Loop","None"],"answer":"Restore systems"},
                {"question":"What is high availability?","options":["Always accessible","Slow system","Loop","None"],"answer":"Always accessible"},
                {"question":"What is IAM used for?","options":["Access control","Storage","Loop","None"],"answer":"Access control"},
                {"question":"What is VPC?","options":["Private network","Public network","Loop","None"],"answer":"Private network"},
                {"question":"What is edge computing?","options":["Processing near data","Remote processing","Loop","None"],"answer":"Processing near data"},
                {"question":"What is hybrid cloud?","options":["Mix of clouds","Single cloud","Loop","None"],"answer":"Mix of clouds"},
                {"question":"What is cloud security?","options":["Protect cloud systems","Loop","Error","None"],"answer":"Protect cloud systems"}
            ]
        }
    },
    "Communication": {
        "Verbal Communication": {
            "beginner": [
                {"question":"What is verbal communication?","options":["Communication using words","Communication using signs","Communication using images","None"],"answer":"Communication using words"},
                {"question":"Which of the following is an example of verbal communication?","options":["Speaking","Gestures","Facial expressions","None"],"answer":"Speaking"},
                {"question":"What is the main purpose of communication?","options":["Sharing information","Keeping silence","Avoiding people","None"],"answer":"Sharing information"},
                {"question":"What is tone in communication?","options":["Style of speaking","Speed","Volume","None"],"answer":"Style of speaking"},
                {"question":"What is clarity in communication?","options":["Clear message","Loud voice","Fast speaking","None"],"answer":"Clear message"},
                {"question":"What is listening in communication?","options":["Understanding message","Ignoring","Talking","None"],"answer":"Understanding message"},
                {"question":"What is feedback in communication?","options":["Response","Silence","Message","None"],"answer":"Response"},
                {"question":"What is formal communication?","options":["Official communication","Casual talk","Personal chat","None"],"answer":"Official communication"},
                {"question":"What is informal communication?","options":["Casual communication","Official communication","Formal writing","None"],"answer":"Casual communication"},
                {"question":"What is pronunciation?","options":["Correct speaking","Writing","Reading","None"],"answer":"Correct speaking"}
            ],
            "intermediate": [
                {"question":"What is active listening?","options":["Fully focusing on speaker","Ignoring speaker","Talking more","None"],"answer":"Fully focusing on speaker"},
                {"question":"What is body language in communication?","options":["Non-verbal signals","Verbal signals","Writing","None"],"answer":"Non-verbal signals"},
                {"question":"What is communication barrier?","options":["Obstacles in communication","Message","Feedback","None"],"answer":"Obstacles in communication"},
                {"question":"What is empathy in communication?","options":["Understanding others","Ignoring others","Talking more","None"],"answer":"Understanding others"},
                {"question":"What is persuasion?","options":["Influencing others","Ignoring","Avoiding","None"],"answer":"Influencing others"},
                {"question":"What is public speaking?","options":["Speaking to audience","Private talk","Writing","None"],"answer":"Speaking to audience"},
                {"question":"What is confidence in communication?","options":["Self-belief","Fear","Silence","None"],"answer":"Self-belief"},
                {"question":"What is message encoding?","options":["Creating message","Receiving message","Ignoring message","None"],"answer":"Creating message"},
                {"question":"What is message decoding?","options":["Understanding message","Sending message","Ignoring message","None"],"answer":"Understanding message"},
                {"question":"What is assertive communication?","options":["Expressing clearly","Aggressive speaking","Silent behavior","None"],"answer":"Expressing clearly"}
            ],
            "expert": [
                {"question":"What is effective communication?","options":["Clear and understood message","Fast speaking","Loud speaking","None"],"answer":"Clear and understood message"},
                {"question":"What is intercultural communication?","options":["Between cultures","Within same culture","None","Error"],"answer":"Between cultures"},
                {"question":"What is communication strategy?","options":["Planned communication","Random speaking","None","Error"],"answer":"Planned communication"},
                {"question":"What is negotiation?","options":["Reaching agreement","Avoiding talk","None","Error"],"answer":"Reaching agreement"},
                {"question":"What is conflict resolution?","options":["Solving disputes","Creating conflict","None","Error"],"answer":"Solving disputes"},
                {"question":"What is emotional intelligence in communication?","options":["Managing emotions","Ignoring emotions","None","Error"],"answer":"Managing emotions"},
                {"question":"What is communication model?","options":["Process of communication","Tool","None","Error"],"answer":"Process of communication"},
                {"question":"What is semantic barrier?","options":["Meaning misunderstanding","Noise","None","Error"],"answer":"Meaning misunderstanding"},
                {"question":"What is communication channel?","options":["Medium of communication","Message","None","Error"],"answer":"Medium of communication"},
                {"question":"What is feedback loop?","options":["Continuous response","Silence","None","Error"],"answer":"Continuous response"}
            ]
        },
        "English Grammar": {
            "beginner": [
                {"question":"What is a noun?","options":["Name of person/place/thing","Action word","Describing word","None"],"answer":"Name of person/place/thing"},
                {"question":"What is a verb?","options":["Action word","Name","Place","None"],"answer":"Action word"},
                {"question":"What is an adjective?","options":["Describing word","Action word","Name","None"],"answer":"Describing word"},
                {"question":"What is a pronoun?","options":["Replaces noun","Action word","Describes","None"],"answer":"Replaces noun"},
                {"question":"Which sentence is correct?","options":["She is going","She going","She go","None"],"answer":"She is going"},
                {"question":"What is a sentence?","options":["Group of words","Single word","Letter","None"],"answer":"Group of words"},
                {"question":"What is punctuation?","options":["Marks in writing","Words","Sentences","None"],"answer":"Marks in writing"},
                {"question":"What is plural of 'cat'?","options":["cats","cat","cates","None"],"answer":"cats"},
                {"question":"What is past tense of 'go'?","options":["went","goes","gone","None"],"answer":"went"},
                {"question":"What is an article?","options":["a, an, the","Verb","Noun","None"],"answer":"a, an, the"}
            ],
            "intermediate": [
                {"question":"What is present continuous tense?","options":["Ongoing action","Past action","Future action","None"],"answer":"Ongoing action"},
                {"question":"What is subject in a sentence?","options":["Doer","Action","Object","None"],"answer":"Doer"},
                {"question":"What is object in a sentence?","options":["Receiver of action","Doer","Verb","None"],"answer":"Receiver of action"},
                {"question":"What is preposition?","options":["Shows relation","Action","Name","None"],"answer":"Shows relation"},
                {"question":"What is conjunction?","options":["Joining words","Describing","Action","None"],"answer":"Joining words"},
                {"question":"What is passive voice?","options":["Object focus","Subject focus","None","Error"],"answer":"Object focus"},
                {"question":"What is active voice?","options":["Subject focus","Object focus","None","Error"],"answer":"Subject focus"},
                {"question":"What is clause?","options":["Group of words with subject","Sentence","Word","None"],"answer":"Group of words with subject"},
                {"question":"What is direct speech?","options":["Exact words","Changed words","None","Error"],"answer":"Exact words"},
                {"question":"What is indirect speech?","options":["Reported speech","Exact words","None","Error"],"answer":"Reported speech"}
            ],
            "expert": [
                {"question":"What is a complex sentence?","options":["Multiple clauses","Single clause","None","Error"],"answer":"Multiple clauses"},
                {"question":"What is subject-verb agreement?","options":["Matching subject and verb","Mismatch","None","Error"],"answer":"Matching subject and verb"},
                {"question":"What is gerund?","options":["Verb as noun","Verb","Noun","None"],"answer":"Verb as noun"},
                {"question":"What is infinitive?","options":["To + verb","Verb","Noun","None"],"answer":"To + verb"},
                {"question":"What is modal verb?","options":["Helping verb","Main verb","None","Error"],"answer":"Helping verb"},
                {"question":"What is conditional sentence?","options":["If condition","Statement","None","Error"],"answer":"If condition"},
                {"question":"What is phrasal verb?","options":["Verb + preposition","Verb","Noun","None"],"answer":"Verb + preposition"},
                {"question":"What is parallelism?","options":["Balanced structure","Unbalanced","None","Error"],"answer":"Balanced structure"},
                {"question":"What is ellipsis?","options":["Omission of words","Addition","None","Error"],"answer":"Omission of words"},
                {"question":"What is cohesion in writing?","options":["Logical flow","Random text","None","Error"],"answer":"Logical flow"}
            ]
        },
        "Psychology": {
            "beginner": [
                {"question":"What is psychology?","options":["Study of mind","Study of body","Study of society","None"],"answer":"Study of mind"},
                {"question":"What is behavior?","options":["Actions","Thoughts","Feelings","None"],"answer":"Actions"},
                {"question":"What is emotion?","options":["Feeling","Action","Thought","None"],"answer":"Feeling"},
                {"question":"What is stress?","options":["Mental pressure","Relaxation","Joy","None"],"answer":"Mental pressure"},
                {"question":"What is memory?","options":["Storing information","Forgetting","Learning","None"],"answer":"Storing information"},
                {"question":"What is learning?","options":["Gaining knowledge","Forgetting","Sleeping","None"],"answer":"Gaining knowledge"},
                {"question":"What is motivation?","options":["Drive to act","Fear","Stress","None"],"answer":"Drive to act"},
                {"question":"What is perception?","options":["Understanding","Seeing","Hearing","None"],"answer":"Understanding"},
                {"question":"What is personality?","options":["Behavior pattern","Mood","Emotion","None"],"answer":"Behavior pattern"},
                {"question":"What is intelligence?","options":["Ability to learn","Strength","Speed","None"],"answer":"Ability to learn"}
            ],
            "intermediate": [
                {"question":"What is cognitive psychology?","options":["Study of thinking","Behavior","Emotion","None"],"answer":"Study of thinking"},
                {"question":"What is conditioning?","options":["Learning process","Memory","Emotion","None"],"answer":"Learning process"},
                {"question":"What is reinforcement?","options":["Strengthening behavior","Weakening","None","Error"],"answer":"Strengthening behavior"},
                {"question":"What is punishment?","options":["Reducing behavior","Increasing behavior","None","Error"],"answer":"Reducing behavior"},
                {"question":"What is attitude?","options":["Belief system","Emotion","Memory","None"],"answer":"Belief system"},
                {"question":"What is social behavior?","options":["Interaction","Isolation","None","Error"],"answer":"Interaction"},
                {"question":"What is mental health?","options":["Emotional well-being","Physical health","None","Error"],"answer":"Emotional well-being"},
                {"question":"What is attention?","options":["Focus","Memory","Emotion","None"],"answer":"Focus"},
                {"question":"What is habit?","options":["Repeated behavior","New action","None","Error"],"answer":"Repeated behavior"},
                {"question":"What is learning theory?","options":["Explanation of learning","Emotion","None","Error"],"answer":"Explanation of learning"}
            ],
            "expert": [
                {"question":"What is cognitive dissonance?","options":["Conflicting thoughts","Agreement","None","Error"],"answer":"Conflicting thoughts"},
                {"question":"What is emotional intelligence?","options":["Understanding emotions","Ignoring emotions","None","Error"],"answer":"Understanding emotions"},
                {"question":"What is behaviorism?","options":["Study of behavior","Mind","None","Error"],"answer":"Study of behavior"},
                {"question":"What is psychoanalysis?","options":["Study of unconscious","Conscious","None","Error"],"answer":"Study of unconscious"},
                {"question":"What is personality theory?","options":["Explains personality","Emotion","None","Error"],"answer":"Explains personality"},
                {"question":"What is motivation theory?","options":["Explains motivation","Emotion","None","Error"],"answer":"Explains motivation"},
                {"question":"What is perception theory?","options":["Explains perception","Memory","None","Error"],"answer":"Explains perception"},
                {"question":"What is learning curve?","options":["Rate of learning","Speed","None","Error"],"answer":"Rate of learning"},
                {"question":"What is self-awareness?","options":["Understanding self","Ignoring self","None","Error"],"answer":"Understanding self"},
                {"question":"What is resilience?","options":["Ability to recover","Weakness","None","Error"],"answer":"Ability to recover"}
            ]
        }
    },
    "Social Science": {
        "Geography": {
            "beginner": [
                {"question":"What is geography the study of?","options":["Earth and its features","History","Economics","None"],"answer":"Earth and its features"},
                {"question":"Which is the largest continent?","options":["Asia","Africa","Europe","None"],"answer":"Asia"},
                {"question":"Which is the largest ocean?","options":["Pacific Ocean","Atlantic Ocean","Indian Ocean","None"],"answer":"Pacific Ocean"},
                {"question":"What is a map?","options":["Representation of area","Story","Book","None"],"answer":"Representation of area"},
                {"question":"What is climate?","options":["Weather over time","Daily weather","Temperature","None"],"answer":"Weather over time"},
                {"question":"What is a river?","options":["Flowing water","Mountain","Lake","None"],"answer":"Flowing water"},
                {"question":"What is a mountain?","options":["High landform","River","Ocean","None"],"answer":"High landform"},
                {"question":"What is a desert?","options":["Dry region","Wet region","Forest","None"],"answer":"Dry region"},
                {"question":"What is latitude?","options":["Horizontal lines","Vertical lines","None","Error"],"answer":"Horizontal lines"},
                {"question":"What is longitude?","options":["Vertical lines","Horizontal lines","None","Error"],"answer":"Vertical lines"}
            ],
            "intermediate": [
                {"question":"What is the equator?","options":["0° latitude","0° longitude","Tropic","None"],"answer":"0° latitude"},
                {"question":"What is the prime meridian?","options":["0° longitude","0° latitude","None","Error"],"answer":"0° longitude"},
                {"question":"What is population density?","options":["People per area","Total people","None","Error"],"answer":"People per area"},
                {"question":"What is urbanization?","options":["Growth of cities","Decline of cities","None","Error"],"answer":"Growth of cities"},
                {"question":"What is a plateau?","options":["Flat elevated land","Mountain","Valley","None"],"answer":"Flat elevated land"},
                {"question":"What is erosion?","options":["Wearing away of land","Building land","None","Error"],"answer":"Wearing away of land"},
                {"question":"What is natural resource?","options":["Resource from nature","Man-made","None","Error"],"answer":"Resource from nature"},
                {"question":"What is renewable resource?","options":["Can be replenished","Cannot be replenished","None","Error"],"answer":"Can be replenished"},
                {"question":"What is monsoon?","options":["Seasonal wind","Storm","Rain","None"],"answer":"Seasonal wind"},
                {"question":"What is GIS?","options":["Geographic Information System","Mapping tool","None","Error"],"answer":"Geographic Information System"}
            ],
            "expert": [
                {"question":"What is plate tectonics?","options":["Movement of plates","Climate change","None","Error"],"answer":"Movement of plates"},
                {"question":"What is globalization?","options":["Global interaction","Isolation","None","Error"],"answer":"Global interaction"},
                {"question":"What is sustainable development?","options":["Balanced growth","Fast growth","None","Error"],"answer":"Balanced growth"},
                {"question":"What is urban sprawl?","options":["City expansion","City decline","None","Error"],"answer":"City expansion"},
                {"question":"What is carbon footprint?","options":["Environmental impact","Energy use","None","Error"],"answer":"Environmental impact"},
                {"question":"What is biodiversity?","options":["Variety of life","Single species","None","Error"],"answer":"Variety of life"},
                {"question":"What is remote sensing?","options":["Data from satellites","Ground data","None","Error"],"answer":"Data from satellites"},
                {"question":"What is geomorphology?","options":["Study of landforms","Climate","None","Error"],"answer":"Study of landforms"},
                {"question":"What is hydrology?","options":["Study of water","Land","None","Error"],"answer":"Study of water"},
                {"question":"What is climate change?","options":["Long-term weather change","Daily weather","None","Error"],"answer":"Long-term weather change"}
            ]
        },
        "History": {
            "beginner": [
                {"question":"What is history?","options":["Study of past","Future study","Science","None"],"answer":"Study of past"},
                {"question":"Who was the first President of India?","options":["Rajendra Prasad","Nehru","Gandhi","None"],"answer":"Rajendra Prasad"},
                {"question":"What is a civilization?","options":["Advanced society","Village","None","Error"],"answer":"Advanced society"},
                {"question":"Who discovered India route by sea?","options":["Vasco da Gama","Columbus","None","Error"],"answer":"Vasco da Gama"},
                {"question":"What is ancient history?","options":["Old times","Modern times","None","Error"],"answer":"Old times"},
                {"question":"What is a monument?","options":["Historical building","Modern building","None","Error"],"answer":"Historical building"},
                {"question":"Who was Mahatma Gandhi?","options":["Leader","Scientist","None","Error"],"answer":"Leader"},
                {"question":"What is independence?","options":["Freedom","Slavery","None","Error"],"answer":"Freedom"},
                {"question":"What is a war?","options":["Conflict","Peace","None","Error"],"answer":"Conflict"},
                {"question":"What is a king?","options":["Ruler","Worker","None","Error"],"answer":"Ruler"}
            ],
            "intermediate": [
                {"question":"What was the Industrial Revolution?","options":["Technological change","War","None","Error"],"answer":"Technological change"},
                {"question":"What was the French Revolution?","options":["Political change","War","None","Error"],"answer":"Political change"},
                {"question":"What was World War I?","options":["Global war","Local war","None","Error"],"answer":"Global war"},
                {"question":"What was World War II?","options":["Global conflict","Local war","None","Error"],"answer":"Global conflict"},
                {"question":"What is colonialism?","options":["Control of territory","Freedom","None","Error"],"answer":"Control of territory"},
                {"question":"What is nationalism?","options":["Love for nation","Hate","None","Error"],"answer":"Love for nation"},
                {"question":"Who was Napoleon?","options":["French leader","Scientist","None","Error"],"answer":"French leader"},
                {"question":"What is a dynasty?","options":["Ruling family","Group","None","Error"],"answer":"Ruling family"},
                {"question":"What is a revolution?","options":["Major change","Minor change","None","Error"],"answer":"Major change"},
                {"question":"What is independence movement?","options":["Freedom struggle","War","None","Error"],"answer":"Freedom struggle"}
            ],
            "expert": [
                {"question":"What is historiography?","options":["Study of history writing","History events","None","Error"],"answer":"Study of history writing"},
                {"question":"What is imperialism?","options":["Expansion of power","Peace","None","Error"],"answer":"Expansion of power"},
                {"question":"What is cold war?","options":["Political tension","Hot war","None","Error"],"answer":"Political tension"},
                {"question":"What is renaissance?","options":["Cultural revival","War","None","Error"],"answer":"Cultural revival"},
                {"question":"What is enlightenment?","options":["Intellectual movement","War","None","Error"],"answer":"Intellectual movement"},
                {"question":"What is feudalism?","options":["Land system","Trade","None","Error"],"answer":"Land system"},
                {"question":"What is socialism?","options":["Economic system","War","None","Error"],"answer":"Economic system"},
                {"question":"What is capitalism?","options":["Private ownership","Public ownership","None","Error"],"answer":"Private ownership"},
                {"question":"What is democracy?","options":["Rule by people","Rule by king","None","Error"],"answer":"Rule by people"},
                {"question":"What is global history?","options":["World history","Local history","None","Error"],"answer":"World history"}
            ]
        },
        "Political Science": {
            "beginner": [
                {"question":"What is political science?","options":["Study of politics","Study of economy","None","Error"],"answer":"Study of politics"},
                {"question":"What is a government?","options":["Governing body","People","None","Error"],"answer":"Governing body"},
                {"question":"What is democracy?","options":["Rule by people","Rule by king","None","Error"],"answer":"Rule by people"},
                {"question":"What is a constitution?","options":["Set of laws","Book","None","Error"],"answer":"Set of laws"},
                {"question":"Who is a citizen?","options":["Member of country","Visitor","None","Error"],"answer":"Member of country"},
                {"question":"What is voting?","options":["Choosing leaders","Fighting","None","Error"],"answer":"Choosing leaders"},
                {"question":"What is parliament?","options":["Law-making body","Court","None","Error"],"answer":"Law-making body"},
                {"question":"What is election?","options":["Selection process","War","None","Error"],"answer":"Selection process"},
                {"question":"What is law?","options":["Rules","Advice","None","Error"],"answer":"Rules"},
                {"question":"What is rights?","options":["Freedom","Rules","None","Error"],"answer":"Freedom"}
            ],
            "intermediate": [
                {"question":"What is federalism?","options":["Power division","Single power","None","Error"],"answer":"Power division"},
                {"question":"What is separation of powers?","options":["Division of roles","Unity","None","Error"],"answer":"Division of roles"},
                {"question":"What is judiciary?","options":["Court system","Police","None","Error"],"answer":"Court system"},
                {"question":"What is executive?","options":["Implement laws","Make laws","None","Error"],"answer":"Implement laws"},
                {"question":"What is legislature?","options":["Make laws","Implement laws","None","Error"],"answer":"Make laws"},
                {"question":"What is political party?","options":["Group with ideology","Random group","None","Error"],"answer":"Group with ideology"},
                {"question":"What is public policy?","options":["Government decisions","Personal decisions","None","Error"],"answer":"Government decisions"},
                {"question":"What is sovereignty?","options":["Supreme power","Weak power","None","Error"],"answer":"Supreme power"},
                {"question":"What is civil rights?","options":["Basic rights","Rules","None","Error"],"answer":"Basic rights"},
                {"question":"What is governance?","options":["Administration","War","None","Error"],"answer":"Administration"}
            ],
            "expert": [
                {"question":"What is political ideology?","options":["Belief system","Action","None","Error"],"answer":"Belief system"},
                {"question":"What is liberalism?","options":["Freedom ideology","Control ideology","None","Error"],"answer":"Freedom ideology"},
                {"question":"What is conservatism?","options":["Traditional ideology","Modern ideology","None","Error"],"answer":"Traditional ideology"},
                {"question":"What is socialism?","options":["Public ownership","Private ownership","None","Error"],"answer":"Public ownership"},
                {"question":"What is communism?","options":["Classless society","Capitalist society","None","Error"],"answer":"Classless society"},
                {"question":"What is globalization?","options":["Global integration","Isolation","None","Error"],"answer":"Global integration"},
                {"question":"What is political theory?","options":["Study of politics ideas","Events","None","Error"],"answer":"Study of politics ideas"},
                {"question":"What is electoral system?","options":["Voting system","Law system","None","Error"],"answer":"Voting system"},
                {"question":"What is public administration?","options":["Managing public services","Private work","None","Error"],"answer":"Managing public services"},
                {"question":"What is international relations?","options":["Relations between countries","Local relations","None","Error"],"answer":"Relations between countries"}
            ]
        },
        "Economics": {
            "beginner": [
                {"question":"What is economics?","options":["Study of resources","History","Science","None"],"answer":"Study of resources"},
                {"question":"What is demand?","options":["Need for goods","Supply","None","Error"],"answer":"Need for goods"},
                {"question":"What is supply?","options":["Availability of goods","Demand","None","Error"],"answer":"Availability of goods"},
                {"question":"What is market?","options":["Place to buy/sell","Factory","None","Error"],"answer":"Place to buy/sell"},
                {"question":"What is price?","options":["Value of product","Profit","None","Error"],"answer":"Value of product"},
                {"question":"What is money?","options":["Medium of exchange","Product","None","Error"],"answer":"Medium of exchange"},
                {"question":"What is trade?","options":["Exchange of goods","Production","None","Error"],"answer":"Exchange of goods"},
                {"question":"What is production?","options":["Making goods","Selling","None","Error"],"answer":"Making goods"},
                {"question":"What is consumption?","options":["Using goods","Making goods","None","Error"],"answer":"Using goods"},
                {"question":"What is income?","options":["Earnings","Loss","None","Error"],"answer":"Earnings"}
            ],
            "intermediate": [
                {"question":"What is inflation?","options":["Rise in prices","Fall in prices","None","Error"],"answer":"Rise in prices"},
                {"question":"What is GDP?","options":["Total output","Profit","None","Error"],"answer":"Total output"},
                {"question":"What is unemployment?","options":["Lack of jobs","Working","None","Error"],"answer":"Lack of jobs"},
                {"question":"What is fiscal policy?","options":["Government spending","Market","None","Error"],"answer":"Government spending"},
                {"question":"What is monetary policy?","options":["Control money supply","Tax","None","Error"],"answer":"Control money supply"},
                {"question":"What is elasticity?","options":["Responsiveness","Rigid","None","Error"],"answer":"Responsiveness"},
                {"question":"What is opportunity cost?","options":["Alternative cost","Profit","None","Error"],"answer":"Alternative cost"},
                {"question":"What is demand curve?","options":["Graph of demand","Supply graph","None","Error"],"answer":"Graph of demand"},
                {"question":"What is supply curve?","options":["Graph of supply","Demand graph","None","Error"],"answer":"Graph of supply"},
                {"question":"What is equilibrium?","options":["Balance point","Imbalance","None","Error"],"answer":"Balance point"}
            ],
            "expert": [
                {"question":"What is microeconomics?","options":["Individual behavior","National economy","None","Error"],"answer":"Individual behavior"},
                {"question":"What is macroeconomics?","options":["Whole economy","Individual","None","Error"],"answer":"Whole economy"},
                {"question":"What is market structure?","options":["Market type","Demand","None","Error"],"answer":"Market type"},
                {"question":"What is perfect competition?","options":["Many sellers","Few sellers","None","Error"],"answer":"Many sellers"},
                {"question":"What is monopoly?","options":["Single seller","Many sellers","None","Error"],"answer":"Single seller"},
                {"question":"What is oligopoly?","options":["Few sellers","Many sellers","None","Error"],"answer":"Few sellers"},
                {"question":"What is game theory?","options":["Strategic decisions","Games","None","Error"],"answer":"Strategic decisions"},
                {"question":"What is economic growth?","options":["Increase output","Decrease output","None","Error"],"answer":"Increase output"},
                {"question":"What is development?","options":["Improvement","Decline","None","Error"],"answer":"Improvement"},
                {"question":"What is globalization?","options":["Global trade","Local trade","None","Error"],"answer":"Global trade"}
            ]
        }
    }
}

