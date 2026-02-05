#!/usr/bin/env python3
"""
Populate database with skills for CSE-related jobs and VLSI domain
"""

import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run import create_app
from extensions import db
from models.skill import Skill

def populate_skills():
    """Populate the database with CSE and VLSI related skills"""
    
    # Define skills data categorized for easier management
    skills_data = [
        # Programming Languages
        {'skill_name': 'Python', 'category': 'Programming Languages', 'description': 'High-level programming language for web development, data science, and automation'},
        {'skill_name': 'Java', 'category': 'Programming Languages', 'description': 'Object-oriented programming language for enterprise applications'},
        {'skill_name': 'C++', 'category': 'Programming Languages', 'description': 'High-performance programming language for system programming'},
        {'skill_name': 'C', 'category': 'Programming Languages', 'description': 'Low-level programming language for system programming'},
        {'skill_name': 'JavaScript', 'category': 'Programming Languages', 'description': 'Dynamic programming language for web development'},
        {'skill_name': 'TypeScript', 'category': 'Programming Languages', 'description': 'Typed superset of JavaScript'},
        {'skill_name': 'Go', 'category': 'Programming Languages', 'description': 'Open source programming language for scalable applications'},
        {'skill_name': 'Rust', 'category': 'Programming Languages', 'description': 'Systems programming language focused on safety and performance'},
        {'skill_name': 'C#', 'category': 'Programming Languages', 'description': 'Object-oriented programming language developed by Microsoft'},
        {'skill_name': 'PHP', 'category': 'Programming Languages', 'description': 'Server-side scripting language for web development'},
        {'skill_name': 'Ruby', 'category': 'Programming Languages', 'description': 'Dynamic programming language with focus on simplicity'},
        {'skill_name': 'Swift', 'category': 'Programming Languages', 'description': 'Programming language for iOS and macOS development'},
        {'skill_name': 'Kotlin', 'category': 'Programming Languages', 'description': 'Modern programming language for Android development'},
        {'skill_name': 'Scala', 'category': 'Programming Languages', 'description': 'Functional and object-oriented programming language'},
        {'skill_name': 'R', 'category': 'Programming Languages', 'description': 'Statistical computing and graphics programming language'},
        
        # Web Development
        {'skill_name': 'React.js', 'category': 'Web Development', 'description': 'JavaScript library for building user interfaces'},
        {'skill_name': 'Angular', 'category': 'Web Development', 'description': 'TypeScript-based web application framework'},
        {'skill_name': 'Vue.js', 'category': 'Web Development', 'description': 'Progressive JavaScript framework for building UIs'},
        {'skill_name': 'Node.js', 'category': 'Web Development', 'description': 'JavaScript runtime for server-side development'},
        {'skill_name': 'Express.js', 'category': 'Web Development', 'description': 'Fast, minimalist web framework for Node.js'},
        {'skill_name': 'Django', 'category': 'Web Development', 'description': 'High-level Python web framework'},
        {'skill_name': 'Flask', 'category': 'Web Development', 'description': 'Lightweight Python web framework'},
        {'skill_name': 'Spring Boot', 'category': 'Web Development', 'description': 'Java-based framework for creating microservices'},
        {'skill_name': 'ASP.NET', 'category': 'Web Development', 'description': 'Web framework developed by Microsoft'},
        {'skill_name': 'Laravel', 'category': 'Web Development', 'description': 'PHP web application framework'},
        {'skill_name': 'HTML5', 'category': 'Web Development', 'description': 'Latest version of HTML markup language'},
        {'skill_name': 'CSS3', 'category': 'Web Development', 'description': 'Latest version of Cascading Style Sheets'},
        {'skill_name': 'Sass/SCSS', 'category': 'Web Development', 'description': 'CSS preprocessor with enhanced features'},
        {'skill_name': 'Bootstrap', 'category': 'Web Development', 'description': 'CSS framework for responsive web design'},
        {'skill_name': 'Tailwind CSS', 'category': 'Web Development', 'description': 'Utility-first CSS framework'},
        {'skill_name': 'Next.js', 'category': 'Web Development', 'description': 'React framework for production applications'},
        {'skill_name': 'Nuxt.js', 'category': 'Web Development', 'description': 'Vue.js framework for universal applications'},
        
        # Databases
        {'skill_name': 'MySQL', 'category': 'Databases', 'description': 'Open-source relational database management system'},
        {'skill_name': 'PostgreSQL', 'category': 'Databases', 'description': 'Advanced open-source relational database'},
        {'skill_name': 'MongoDB', 'category': 'Databases', 'description': 'NoSQL document-based database'},
        {'skill_name': 'Redis', 'category': 'Databases', 'description': 'In-memory data structure store'},
        {'skill_name': 'SQLite', 'category': 'Databases', 'description': 'Lightweight embedded SQL database'},
        {'skill_name': 'Oracle Database', 'category': 'Databases', 'description': 'Enterprise relational database management system'},
        {'skill_name': 'SQL Server', 'category': 'Databases', 'description': 'Microsoft relational database management system'},
        {'skill_name': 'Elasticsearch', 'category': 'Databases', 'description': 'Distributed search and analytics engine'},
        {'skill_name': 'Cassandra', 'category': 'Databases', 'description': 'Distributed NoSQL database'},
        {'skill_name': 'DynamoDB', 'category': 'Databases', 'description': 'Amazon managed NoSQL database service'},
        
        # Cloud & DevOps
        {'skill_name': 'AWS', 'category': 'Cloud & DevOps', 'description': 'Amazon Web Services cloud platform'},
        {'skill_name': 'Azure', 'category': 'Cloud & DevOps', 'description': 'Microsoft cloud computing platform'},
        {'skill_name': 'Google Cloud Platform', 'category': 'Cloud & DevOps', 'description': 'Google cloud computing services'},
        {'skill_name': 'Docker', 'category': 'Cloud & DevOps', 'description': 'Platform for containerizing applications'},
        {'skill_name': 'Kubernetes', 'category': 'Cloud & DevOps', 'description': 'Container orchestration platform'},
        {'skill_name': 'Jenkins', 'category': 'Cloud & DevOps', 'description': 'Automation server for CI/CD pipelines'},
        {'skill_name': 'GitLab CI/CD', 'category': 'Cloud & DevOps', 'description': 'Continuous integration and deployment'},
        {'skill_name': 'Terraform', 'category': 'Cloud & DevOps', 'description': 'Infrastructure as Code tool'},
        {'skill_name': 'Ansible', 'category': 'Cloud & DevOps', 'description': 'Automation engine for configuration management'},
        {'skill_name': 'Linux', 'category': 'Cloud & DevOps', 'description': 'Open-source operating system'},
        {'skill_name': 'Git', 'category': 'Cloud & DevOps', 'description': 'Distributed version control system'},
        {'skill_name': 'GitHub', 'category': 'Cloud & DevOps', 'description': 'Web-based Git repository hosting service'},
        {'skill_name': 'Nginx', 'category': 'Cloud & DevOps', 'description': 'Web server and reverse proxy'},
        {'skill_name': 'Apache', 'category': 'Cloud & DevOps', 'description': 'Open-source web server'},
        
        # Machine Learning
        {'skill_name': 'Supervised Learning', 'category': 'Machine Learning', 'description': 'Learning with labeled training data'},
        {'skill_name': 'Unsupervised Learning', 'category': 'Machine Learning', 'description': 'Finding patterns in unlabeled data'},
        {'skill_name': 'Reinforcement Learning', 'category': 'Machine Learning', 'description': 'Learning through interaction and rewards'},
        {'skill_name': 'Deep Learning', 'category': 'Machine Learning', 'description': 'Neural networks with multiple layers'},
        {'skill_name': 'Neural Networks', 'category': 'Machine Learning', 'description': 'Computing systems inspired by biological neural networks'},
        {'skill_name': 'Convolutional Neural Networks', 'category': 'Machine Learning', 'description': 'Deep learning for image processing'},
        {'skill_name': 'Recurrent Neural Networks', 'category': 'Machine Learning', 'description': 'Neural networks for sequential data'},
        {'skill_name': 'Transformer Models', 'category': 'Machine Learning', 'description': 'Attention-based neural network architecture'},
        {'skill_name': 'LSTM Networks', 'category': 'Machine Learning', 'description': 'Long Short-Term Memory networks'},
        {'skill_name': 'GAN (Generative Adversarial Networks)', 'category': 'Machine Learning', 'description': 'Generative models using adversarial training'},
        {'skill_name': 'Random Forest', 'category': 'Machine Learning', 'description': 'Ensemble learning method using decision trees'},
        {'skill_name': 'Support Vector Machines', 'category': 'Machine Learning', 'description': 'Classification and regression analysis'},
        {'skill_name': 'K-Means Clustering', 'category': 'Machine Learning', 'description': 'Unsupervised clustering algorithm'},
        {'skill_name': 'Linear Regression', 'category': 'Machine Learning', 'description': 'Statistical method for modeling relationships'},
        {'skill_name': 'Logistic Regression', 'category': 'Machine Learning', 'description': 'Statistical model for binary classification'},
        {'skill_name': 'Decision Trees', 'category': 'Machine Learning', 'description': 'Tree-like model for decision making'},
        {'skill_name': 'Gradient Boosting', 'category': 'Machine Learning', 'description': 'Ensemble method building models sequentially'},
        {'skill_name': 'XGBoost', 'category': 'Machine Learning', 'description': 'Optimized gradient boosting framework'},
        {'skill_name': 'Feature Engineering', 'category': 'Machine Learning', 'description': 'Process of selecting and transforming features'},
        {'skill_name': 'Hyperparameter Tuning', 'category': 'Machine Learning', 'description': 'Optimizing model parameters for performance'},
        {'skill_name': 'Cross Validation', 'category': 'Machine Learning', 'description': 'Technique for assessing model performance'},
        {'skill_name': 'Time Series Analysis', 'category': 'Machine Learning', 'description': 'Analyzing time-ordered data points'},
        {'skill_name': 'Ensemble Methods', 'category': 'Machine Learning', 'description': 'Combining multiple models for better performance'},
        {'skill_name': 'TensorFlow', 'category': 'Machine Learning', 'description': 'Open-source machine learning framework'},
        {'skill_name': 'PyTorch', 'category': 'Machine Learning', 'description': 'Machine learning library for Python'},
        {'skill_name': 'Scikit-learn', 'category': 'Machine Learning', 'description': 'Machine learning library for Python'},
        {'skill_name': 'Keras', 'category': 'Machine Learning', 'description': 'High-level neural networks API'},
        
        # AI Engineering
        {'skill_name': 'MLOps', 'category': 'AI Engineering', 'description': 'Machine Learning Operations and DevOps practices'},
        {'skill_name': 'Model Deployment', 'category': 'AI Engineering', 'description': 'Deploying ML models to production'},
        {'skill_name': 'Model Monitoring', 'category': 'AI Engineering', 'description': 'Tracking model performance in production'},
        {'skill_name': 'A/B Testing for ML', 'category': 'AI Engineering', 'description': 'Experimental design for machine learning'},
        {'skill_name': 'Model Versioning', 'category': 'AI Engineering', 'description': 'Managing different versions of ML models'},
        {'skill_name': 'Pipeline Automation', 'category': 'AI Engineering', 'description': 'Automating ML workflows and pipelines'},
        {'skill_name': 'TensorFlow Serving', 'category': 'AI Engineering', 'description': 'Serving TensorFlow models in production'},
        {'skill_name': 'PyTorch Lightning', 'category': 'AI Engineering', 'description': 'Research framework for PyTorch'},
        {'skill_name': 'Kubeflow', 'category': 'AI Engineering', 'description': 'Machine learning workflows on Kubernetes'},
        {'skill_name': 'MLflow', 'category': 'AI Engineering', 'description': 'Platform for ML lifecycle management'},
        {'skill_name': 'DVC (Data Version Control)', 'category': 'AI Engineering', 'description': 'Version control for machine learning projects'},
        {'skill_name': 'Weights & Biases', 'category': 'AI Engineering', 'description': 'Experiment tracking and model management'},
        {'skill_name': 'Model Performance Optimization', 'category': 'AI Engineering', 'description': 'Optimizing models for speed and efficiency'},
        {'skill_name': 'ONNX', 'category': 'AI Engineering', 'description': 'Open Neural Network Exchange format'},
        {'skill_name': 'TensorRT', 'category': 'AI Engineering', 'description': 'NVIDIA platform for high-performance inference'},
        {'skill_name': 'Edge AI Deployment', 'category': 'AI Engineering', 'description': 'Deploying AI models on edge devices'},
        {'skill_name': 'Model Compression', 'category': 'AI Engineering', 'description': 'Reducing model size for deployment'},
        {'skill_name': 'Quantization', 'category': 'AI Engineering', 'description': 'Reducing model precision for efficiency'},
        {'skill_name': 'Model Distillation', 'category': 'AI Engineering', 'description': 'Creating smaller models from larger ones'},
        
        # AI Agent Development
        {'skill_name': 'LangChain', 'category': 'AI Agent Development', 'description': 'Framework for developing LLM applications'},
        {'skill_name': 'OpenAI API', 'category': 'AI Agent Development', 'description': 'Interface for GPT and other OpenAI models'},
        {'skill_name': 'Anthropic Claude API', 'category': 'AI Agent Development', 'description': 'Interface for Claude AI assistant'},
        {'skill_name': 'Prompt Engineering', 'category': 'AI Agent Development', 'description': 'Crafting effective prompts for AI models'},
        {'skill_name': 'RAG (Retrieval Augmented Generation)', 'category': 'AI Agent Development', 'description': 'Enhancing LLMs with external knowledge'},
        {'skill_name': 'Vector Databases', 'category': 'AI Agent Development', 'description': 'Specialized databases for embeddings'},
        {'skill_name': 'Pinecone', 'category': 'AI Agent Development', 'description': 'Managed vector database service'},
        {'skill_name': 'Weaviate', 'category': 'AI Agent Development', 'description': 'Open-source vector search engine'},
        {'skill_name': 'ChromaDB', 'category': 'AI Agent Development', 'description': 'Open-source embedding database'},
        {'skill_name': 'Semantic Search', 'category': 'AI Agent Development', 'description': 'Search based on meaning rather than keywords'},
        {'skill_name': 'Text Embeddings', 'category': 'AI Agent Development', 'description': 'Converting text to numerical representations'},
        {'skill_name': 'Function Calling', 'category': 'AI Agent Development', 'description': 'Enabling AI models to call external functions'},
        {'skill_name': 'Tool Integration', 'category': 'AI Agent Development', 'description': 'Connecting AI agents with external tools'},
        {'skill_name': 'Multi-Agent Systems', 'category': 'AI Agent Development', 'description': 'Systems with multiple interacting AI agents'},
        {'skill_name': 'LlamaIndex', 'category': 'AI Agent Development', 'description': 'Framework for LLM data integration'},
        {'skill_name': 'Hugging Face Transformers', 'category': 'AI Agent Development', 'description': 'Library for state-of-the-art NLP models'},
        {'skill_name': 'AutoGen', 'category': 'AI Agent Development', 'description': 'Framework for multi-agent conversation'},
        {'skill_name': 'CrewAI', 'category': 'AI Agent Development', 'description': 'Framework for orchestrating AI agents'},
        {'skill_name': 'Conversational AI', 'category': 'AI Agent Development', 'description': 'Building natural conversation systems'},
        {'skill_name': 'Memory Management', 'category': 'AI Agent Development', 'description': 'Managing context and conversation history'},
        {'skill_name': 'Agent Orchestration', 'category': 'AI Agent Development', 'description': 'Coordinating multiple AI agents'},
        {'skill_name': 'Fine-tuning LLMs', 'category': 'AI Agent Development', 'description': 'Customizing large language models'},
        {'skill_name': 'RLHF (Reinforcement Learning from Human Feedback)', 'category': 'AI Agent Development', 'description': 'Training AI with human preferences'},
        
        # Data Science & Visualization
        {'skill_name': 'Data Analysis', 'category': 'Data Science & Visualization', 'description': 'Examining and interpreting data patterns'},
        {'skill_name': 'Statistical Analysis', 'category': 'Data Science & Visualization', 'description': 'Applying statistical methods to data'},
        {'skill_name': 'Pandas', 'category': 'Data Science & Visualization', 'description': 'Data manipulation and analysis library'},
        {'skill_name': 'NumPy', 'category': 'Data Science & Visualization', 'description': 'Fundamental package for scientific computing'},
        {'skill_name': 'Matplotlib', 'category': 'Data Science & Visualization', 'description': 'Plotting library for Python'},
        {'skill_name': 'Seaborn', 'category': 'Data Science & Visualization', 'description': 'Statistical data visualization library'},
        {'skill_name': 'Plotly', 'category': 'Data Science & Visualization', 'description': 'Interactive plotting library'},
        {'skill_name': 'Jupyter Notebook', 'category': 'Data Science & Visualization', 'description': 'Interactive computational environment'},
        {'skill_name': 'Tableau', 'category': 'Data Science & Visualization', 'description': 'Business intelligence and data visualization'},
        {'skill_name': 'Power BI', 'category': 'Data Science & Visualization', 'description': 'Microsoft business analytics solution'},
        {'skill_name': 'Apache Spark', 'category': 'Data Science & Visualization', 'description': 'Unified analytics engine for big data'},
        {'skill_name': 'Hadoop', 'category': 'Data Science & Visualization', 'description': 'Distributed storage and processing framework'},
        {'skill_name': 'Data Mining', 'category': 'Data Science & Visualization', 'description': 'Discovering patterns in large datasets'},
        {'skill_name': 'ETL Processes', 'category': 'Data Science & Visualization', 'description': 'Extract, Transform, Load data processes'},
        {'skill_name': 'Data Warehousing', 'category': 'Data Science & Visualization', 'description': 'Centralized data storage for analytics'},
        {'skill_name': 'Business Intelligence', 'category': 'Data Science & Visualization', 'description': 'Converting data into actionable insights'},
        
        # Natural Language Processing
        {'skill_name': 'Natural Language Processing', 'category': 'Natural Language Processing', 'description': 'AI for understanding human language'},
        {'skill_name': 'Text Classification', 'category': 'Natural Language Processing', 'description': 'Categorizing text into predefined classes'},
        {'skill_name': 'Named Entity Recognition', 'category': 'Natural Language Processing', 'description': 'Identifying entities in text'},
        {'skill_name': 'Sentiment Analysis', 'category': 'Natural Language Processing', 'description': 'Determining emotional tone of text'},
        {'skill_name': 'Text Summarization', 'category': 'Natural Language Processing', 'description': 'Creating concise summaries of text'},
        {'skill_name': 'Machine Translation', 'category': 'Natural Language Processing', 'description': 'Automatic translation between languages'},
        {'skill_name': 'Speech Recognition', 'category': 'Natural Language Processing', 'description': 'Converting speech to text'},
        {'skill_name': 'Text-to-Speech', 'category': 'Natural Language Processing', 'description': 'Converting text to speech'},
        {'skill_name': 'NLTK', 'category': 'Natural Language Processing', 'description': 'Natural Language Toolkit for Python'},
        {'skill_name': 'spaCy', 'category': 'Natural Language Processing', 'description': 'Industrial-strength NLP library'},
        {'skill_name': 'BERT', 'category': 'Natural Language Processing', 'description': 'Bidirectional Encoder Representations from Transformers'},
        {'skill_name': 'GPT Models', 'category': 'Natural Language Processing', 'description': 'Generative Pre-trained Transformer models'},
        {'skill_name': 'Word2Vec', 'category': 'Natural Language Processing', 'description': 'Word embedding technique'},
        {'skill_name': 'GloVe', 'category': 'Natural Language Processing', 'description': 'Global Vectors for Word Representation'},
        
        # Computer Vision
        {'skill_name': 'Computer Vision', 'category': 'Computer Vision', 'description': 'AI for analyzing visual content'},
        {'skill_name': 'Image Classification', 'category': 'Computer Vision', 'description': 'Categorizing images into classes'},
        {'skill_name': 'Object Detection', 'category': 'Computer Vision', 'description': 'Identifying and locating objects in images'},
        {'skill_name': 'Image Segmentation', 'category': 'Computer Vision', 'description': 'Partitioning images into meaningful regions'},
        {'skill_name': 'Facial Recognition', 'category': 'Computer Vision', 'description': 'Identifying individuals from facial features'},
        {'skill_name': 'Optical Character Recognition', 'category': 'Computer Vision', 'description': 'Converting images of text to text'},
        {'skill_name': 'OpenCV', 'category': 'Computer Vision', 'description': 'Open-source computer vision library'},
        {'skill_name': 'YOLO', 'category': 'Computer Vision', 'description': 'You Only Look Once object detection'},
        {'skill_name': 'R-CNN', 'category': 'Computer Vision', 'description': 'Region-based Convolutional Neural Networks'},
        {'skill_name': 'Image Processing', 'category': 'Computer Vision', 'description': 'Digital image manipulation and analysis'},
        {'skill_name': 'Video Analysis', 'category': 'Computer Vision', 'description': 'Processing and analyzing video content'},
        {'skill_name': 'Medical Image Analysis', 'category': 'Computer Vision', 'description': 'AI for medical imaging applications'},
        
        # Mobile Development
        {'skill_name': 'Android Development', 'category': 'Mobile Development', 'description': 'Native Android app development'},
        {'skill_name': 'iOS Development', 'category': 'Mobile Development', 'description': 'Native iOS app development'},
        {'skill_name': 'React Native', 'category': 'Mobile Development', 'description': 'Cross-platform mobile app framework'},
        {'skill_name': 'Flutter', 'category': 'Mobile Development', 'description': 'Google UI toolkit for cross-platform apps'},
        {'skill_name': 'Xamarin', 'category': 'Mobile Development', 'description': 'Microsoft cross-platform app development'},
        {'skill_name': 'Ionic', 'category': 'Mobile Development', 'description': 'Hybrid mobile app development framework'},
        
        # Networking
        {'skill_name': 'Network Administration', 'category': 'Networking', 'description': 'Managing and maintaining computer networks'},
        {'skill_name': 'TCP/IP', 'category': 'Networking', 'description': 'Internet protocol suite fundamentals'},
        {'skill_name': 'OSI Model', 'category': 'Networking', 'description': 'Open Systems Interconnection reference model'},
        {'skill_name': 'Routing Protocols', 'category': 'Networking', 'description': 'Protocols for directing network traffic'},
        {'skill_name': 'Switching Technologies', 'category': 'Networking', 'description': 'Network switching and VLAN management'},
        {'skill_name': 'Wireless Networking', 'category': 'Networking', 'description': 'Wi-Fi and wireless communication protocols'},
        {'skill_name': 'Network Troubleshooting', 'category': 'Networking', 'description': 'Diagnosing and resolving network issues'},
        {'skill_name': 'Cisco Networking', 'category': 'Networking', 'description': 'Cisco network equipment configuration'},
        {'skill_name': 'CCNA', 'category': 'Networking', 'description': 'Cisco Certified Network Associate'},
        {'skill_name': 'CCNP', 'category': 'Networking', 'description': 'Cisco Certified Network Professional'},
        {'skill_name': 'Network Monitoring', 'category': 'Networking', 'description': 'Tools and techniques for network observation'},
        {'skill_name': 'SNMP', 'category': 'Networking', 'description': 'Simple Network Management Protocol'},
        {'skill_name': 'Network Design', 'category': 'Networking', 'description': 'Planning and architecting network infrastructure'},
        {'skill_name': 'VPN Technologies', 'category': 'Networking', 'description': 'Virtual Private Network implementation'},
        {'skill_name': 'Firewall Configuration', 'category': 'Networking', 'description': 'Network security device management'},
        {'skill_name': 'Load Balancers', 'category': 'Networking', 'description': 'Distributing network traffic across servers'},
        {'skill_name': 'DNS Management', 'category': 'Networking', 'description': 'Domain Name System administration'},
        {'skill_name': 'DHCP', 'category': 'Networking', 'description': 'Dynamic Host Configuration Protocol'},
        {'skill_name': 'Network Automation', 'category': 'Networking', 'description': 'Automating network configuration and management'},
        {'skill_name': 'SDN (Software Defined Networking)', 'category': 'Networking', 'description': 'Programmable network infrastructure'},
        {'skill_name': 'Network Function Virtualization', 'category': 'Networking', 'description': 'Virtualizing network services'},
        {'skill_name': 'BGP (Border Gateway Protocol)', 'category': 'Networking', 'description': 'Internet routing protocol'},
        {'skill_name': 'OSPF', 'category': 'Networking', 'description': 'Open Shortest Path First routing protocol'},
        {'skill_name': 'MPLS', 'category': 'Networking', 'description': 'Multiprotocol Label Switching'},
        {'skill_name': 'Quality of Service (QoS)', 'category': 'Networking', 'description': 'Network traffic prioritization'},
        {'skill_name': 'Network Performance Optimization', 'category': 'Networking', 'description': 'Improving network speed and reliability'},
        {'skill_name': 'Wireshark', 'category': 'Networking', 'description': 'Network protocol analyzer'},
        {'skill_name': 'PacketCapture Analysis', 'category': 'Networking', 'description': 'Analyzing network traffic captures'},
        {'skill_name': 'Network Segmentation', 'category': 'Networking', 'description': 'Dividing networks for security and performance'},
        {'skill_name': '5G Networks', 'category': 'Networking', 'description': 'Fifth generation mobile network technology'},
        {'skill_name': 'IoT Networking', 'category': 'Networking', 'description': 'Internet of Things network protocols'},
        
        # Cybersecurity
        {'skill_name': 'Information Security', 'category': 'Cybersecurity', 'description': 'Protecting information systems and data'},
        {'skill_name': 'Network Security', 'category': 'Cybersecurity', 'description': 'Protecting network infrastructure'},
        {'skill_name': 'Penetration Testing', 'category': 'Cybersecurity', 'description': 'Ethical hacking to find vulnerabilities'},
        {'skill_name': 'Vulnerability Assessment', 'category': 'Cybersecurity', 'description': 'Identifying security weaknesses'},
        {'skill_name': 'Ethical Hacking', 'category': 'Cybersecurity', 'description': 'Legal hacking to improve security'},
        {'skill_name': 'Incident Response', 'category': 'Cybersecurity', 'description': 'Managing security breach responses'},
        {'skill_name': 'Digital Forensics', 'category': 'Cybersecurity', 'description': 'Investigating cyber crimes and incidents'},
        {'skill_name': 'Malware Analysis', 'category': 'Cybersecurity', 'description': 'Analyzing malicious software'},
        {'skill_name': 'Cryptography', 'category': 'Cybersecurity', 'description': 'Secure communication techniques'},
        {'skill_name': 'PKI (Public Key Infrastructure)', 'category': 'Cybersecurity', 'description': 'Managing digital certificates and keys'},
        {'skill_name': 'SIEM Tools', 'category': 'Cybersecurity', 'description': 'Security Information and Event Management'},
        {'skill_name': 'Security Frameworks', 'category': 'Cybersecurity', 'description': 'NIST, ISO 27001, and other security standards'},
        {'skill_name': 'Risk Assessment', 'category': 'Cybersecurity', 'description': 'Evaluating and managing security risks'},
        {'skill_name': 'Compliance Management', 'category': 'Cybersecurity', 'description': 'Ensuring adherence to security regulations'},
        {'skill_name': 'Identity and Access Management', 'category': 'Cybersecurity', 'description': 'Managing user identities and permissions'},
        {'skill_name': 'Multi-Factor Authentication', 'category': 'Cybersecurity', 'description': 'Enhanced authentication security'},
        {'skill_name': 'Zero Trust Architecture', 'category': 'Cybersecurity', 'description': 'Security model with no implicit trust'},
        {'skill_name': 'Cloud Security', 'category': 'Cybersecurity', 'description': 'Securing cloud computing environments'},
        {'skill_name': 'Application Security', 'category': 'Cybersecurity', 'description': 'Securing software applications'},
        {'skill_name': 'Web Application Security', 'category': 'Cybersecurity', 'description': 'OWASP principles and web security'},
        {'skill_name': 'Mobile Security', 'category': 'Cybersecurity', 'description': 'Securing mobile applications and devices'},
        {'skill_name': 'Endpoint Security', 'category': 'Cybersecurity', 'description': 'Protecting end-user devices'},
        {'skill_name': 'Data Loss Prevention', 'category': 'Cybersecurity', 'description': 'Preventing unauthorized data disclosure'},
        {'skill_name': 'Security Monitoring', 'category': 'Cybersecurity', 'description': 'Continuous security surveillance'},
        {'skill_name': 'Threat Intelligence', 'category': 'Cybersecurity', 'description': 'Gathering and analyzing threat data'},
        {'skill_name': 'Security Awareness Training', 'category': 'Cybersecurity', 'description': 'Educating users about security practices'},
        {'skill_name': 'Red Team Operations', 'category': 'Cybersecurity', 'description': 'Simulated attacks for security testing'},
        {'skill_name': 'Blue Team Defense', 'category': 'Cybersecurity', 'description': 'Defensive security operations'},
        {'skill_name': 'Purple Team', 'category': 'Cybersecurity', 'description': 'Collaborative red and blue team approach'},
        {'skill_name': 'Security Automation', 'category': 'Cybersecurity', 'description': 'Automating security processes and responses'},
        {'skill_name': 'SOAR (Security Orchestration)', 'category': 'Cybersecurity', 'description': 'Security Orchestration, Automation and Response'},
        {'skill_name': 'Cyber Threat Hunting', 'category': 'Cybersecurity', 'description': 'Proactively searching for threats'},
        {'skill_name': 'Security Architecture', 'category': 'Cybersecurity', 'description': 'Designing secure system architectures'},
        {'skill_name': 'Business Continuity Planning', 'category': 'Cybersecurity', 'description': 'Planning for security incident recovery'},
        {'skill_name': 'Disaster Recovery', 'category': 'Cybersecurity', 'description': 'Recovering from security incidents'},
        {'skill_name': 'Firewall Management', 'category': 'Cybersecurity', 'description': 'Configuring and managing firewalls'},
        {'skill_name': 'Intrusion Detection Systems', 'category': 'Cybersecurity', 'description': 'IDS/IPS configuration and monitoring'},
        {'skill_name': 'Security Policy Development', 'category': 'Cybersecurity', 'description': 'Creating organizational security policies'},
        {'skill_name': 'ISO 27001', 'category': 'Cybersecurity', 'description': 'International security management standard'},
        {'skill_name': 'CISSP', 'category': 'Cybersecurity', 'description': 'Certified Information Systems Security Professional'},
        {'skill_name': 'CEH (Certified Ethical Hacker)', 'category': 'Cybersecurity', 'description': 'Ethical hacking certification'},
        {'skill_name': 'CISM', 'category': 'Cybersecurity', 'description': 'Certified Information Security Manager'},
        
        # VLSI Design & Engineering
        {'skill_name': 'Verilog', 'category': 'VLSI Design', 'description': 'Hardware description language for digital design'},
        {'skill_name': 'VHDL', 'category': 'VLSI Design', 'description': 'VHSIC Hardware Description Language'},
        {'skill_name': 'SystemVerilog', 'category': 'VLSI Design', 'description': 'Extended Verilog for verification and design'},
        {'skill_name': 'Cadence Tools', 'category': 'VLSI Design', 'description': 'EDA tools for IC design and verification'},
        {'skill_name': 'Synopsys Tools', 'category': 'VLSI Design', 'description': 'Electronic design automation tools'},
        {'skill_name': 'Mentor Graphics', 'category': 'VLSI Design', 'description': 'EDA software for electronic design'},
        {'skill_name': 'FPGA Design', 'category': 'VLSI Design', 'description': 'Field-Programmable Gate Array development'},
        {'skill_name': 'RTL Design', 'category': 'VLSI Design', 'description': 'Register Transfer Level design'},
        {'skill_name': 'DFT (Design for Test)', 'category': 'VLSI Design', 'description': 'Making circuits more testable'},
        {'skill_name': 'Physical Design', 'category': 'VLSI Design', 'description': 'Layout and placement of IC components'},
        {'skill_name': 'Analog IC Design', 'category': 'VLSI Design', 'description': 'Analog integrated circuit design'},
        {'skill_name': 'Digital IC Design', 'category': 'VLSI Design', 'description': 'Digital integrated circuit design'},
        {'skill_name': 'ASIC Design', 'category': 'VLSI Design', 'description': 'Application-Specific Integrated Circuit design'},
        {'skill_name': 'SoC Design', 'category': 'VLSI Design', 'description': 'System on Chip design methodology'},
        {'skill_name': 'Low Power Design', 'category': 'VLSI Design', 'description': 'Power-efficient circuit design techniques'},
        {'skill_name': 'Clock Domain Crossing', 'category': 'VLSI Design', 'description': 'Managing multiple clock domains'},
        {'skill_name': 'Static Timing Analysis', 'category': 'VLSI Design', 'description': 'Timing verification methodology'},
        {'skill_name': 'Logic Synthesis', 'category': 'VLSI Design', 'description': 'Converting RTL to gate-level netlist'},
        {'skill_name': 'Place and Route', 'category': 'VLSI Design', 'description': 'Physical implementation of IC layout'},
        {'skill_name': 'Signal Integrity', 'category': 'VLSI Design', 'description': 'Maintaining signal quality in high-speed designs'},
        {'skill_name': 'Power Integrity', 'category': 'VLSI Design', 'description': 'Power distribution network analysis'},
        {'skill_name': 'EMI/EMC Design', 'category': 'VLSI Design', 'description': 'Electromagnetic interference/compatibility'},
        
        # VLSI Verification
        {'skill_name': 'UVM (Universal Verification Methodology)', 'category': 'VLSI Verification', 'description': 'Standard methodology for verification'},
        {'skill_name': 'Functional Verification', 'category': 'VLSI Verification', 'description': 'Verifying design functionality'},
        {'skill_name': 'Constrained Random Testing', 'category': 'VLSI Verification', 'description': 'Advanced verification technique'},
        {'skill_name': 'Coverage-Driven Verification', 'category': 'VLSI Verification', 'description': 'Metric-based verification approach'},
        {'skill_name': 'Assertion-Based Verification', 'category': 'VLSI Verification', 'description': 'Property-based verification method'},
        {'skill_name': 'Formal Verification', 'category': 'VLSI Verification', 'description': 'Mathematical proof-based verification'},
        {'skill_name': 'Post-Silicon Validation', 'category': 'VLSI Verification', 'description': 'Hardware validation after fabrication'},
        {'skill_name': 'Protocol Verification', 'category': 'VLSI Verification', 'description': 'Verifying communication protocols'},
        
        # VLSI Tools & Technologies
        {'skill_name': 'Xilinx Vivado', 'category': 'VLSI Tools', 'description': 'FPGA design suite from Xilinx'},
        {'skill_name': 'Intel Quartus', 'category': 'VLSI Tools', 'description': 'FPGA development software from Intel'},
        {'skill_name': 'ModelSim', 'category': 'VLSI Tools', 'description': 'Hardware simulation and debug environment'},
        {'skill_name': 'VCS', 'category': 'VLSI Tools', 'description': 'Verilog compiled simulator'},
        {'skill_name': 'QuestaSim', 'category': 'VLSI Tools', 'description': 'Advanced verification simulator'},
        {'skill_name': 'PrimeTime', 'category': 'VLSI Tools', 'description': 'Static timing analysis tool'},
        {'skill_name': 'Design Compiler', 'category': 'VLSI Tools', 'description': 'Logic synthesis tool'},
        {'skill_name': 'ICC (IC Compiler)', 'category': 'VLSI Tools', 'description': 'Physical design implementation tool'},
        {'skill_name': 'Star-RC', 'category': 'VLSI Tools', 'description': 'Parasitic extraction tool'},
        {'skill_name': 'HSPICE', 'category': 'VLSI Tools', 'description': 'Analog circuit simulator'},
        {'skill_name': 'Spectre', 'category': 'VLSI Tools', 'description': 'Advanced analog simulator'},
        {'skill_name': 'Calibre', 'category': 'VLSI Tools', 'description': 'Physical verification platform'},
        
        # Software Engineering
        {'skill_name': 'Agile Methodology', 'category': 'Software Engineering', 'description': 'Iterative software development approach'},
        {'skill_name': 'Scrum', 'category': 'Software Engineering', 'description': 'Agile framework for project management'},
        {'skill_name': 'Test-Driven Development', 'category': 'Software Engineering', 'description': 'Development approach starting with tests'},
        {'skill_name': 'Microservices Architecture', 'category': 'Software Engineering', 'description': 'Distributed system design pattern'},
        {'skill_name': 'Design Patterns', 'category': 'Software Engineering', 'description': 'Reusable solutions to common problems'},
        {'skill_name': 'API Design', 'category': 'Software Engineering', 'description': 'Application Programming Interface design'},
        {'skill_name': 'Code Review', 'category': 'Software Engineering', 'description': 'Systematic examination of source code'},
        {'skill_name': 'Unit Testing', 'category': 'Software Engineering', 'description': 'Testing individual components'},
        {'skill_name': 'Integration Testing', 'category': 'Software Engineering', 'description': 'Testing combined components'},
        {'skill_name': 'Performance Testing', 'category': 'Software Engineering', 'description': 'Testing system performance under load'},
        
        # System Design
        {'skill_name': 'System Architecture', 'category': 'System Design', 'description': 'High-level system structure design'},
        {'skill_name': 'Distributed Systems', 'category': 'System Design', 'description': 'Multi-node system design'},
        {'skill_name': 'Load Balancing', 'category': 'System Design', 'description': 'Distributing workloads across resources'},
        {'skill_name': 'Caching Strategies', 'category': 'System Design', 'description': 'Data storage optimization techniques'},
        {'skill_name': 'Database Design', 'category': 'System Design', 'description': 'Structured data organization'},
        {'skill_name': 'Scalability Design', 'category': 'System Design', 'description': 'Designing for growth and load'},
        {'skill_name': 'High Availability', 'category': 'System Design', 'description': 'Designing fault-tolerant systems'},
        {'skill_name': 'Message Queues', 'category': 'System Design', 'description': 'Asynchronous communication patterns'},
    ]
    
    app = create_app()
    
    with app.app_context():
        try:
            # Check if skills already exist
            existing_count = Skill.query.count()
            if existing_count > 0:
                print(f"Skills already exist in database ({existing_count} skills found)")
                print("Do you want to add new skills anyway? (y/n)")
                response = input().lower().strip()
                if response != 'y' and response != 'yes':
                    print("Operation cancelled.")
                    return
            
            print(f"Adding {len(skills_data)} skills to database...")
            print("Categories included:")
            print("  - Programming Languages (15 skills)")
            print("  - Web Development (17 skills)")
            print("  - Databases (10 skills)")
            print("  - Cloud & DevOps (14 skills)")
            print("  - Machine Learning (27 skills)")
            print("  - AI Engineering (19 skills)")
            print("  - AI Agent Development (23 skills)")
            print("  - Data Science & Visualization (16 skills)")
            print("  - Natural Language Processing (14 skills)")
            print("  - Computer Vision (12 skills)")
            print("  - Mobile Development (6 skills)")
            print("  - Networking (31 skills)")
            print("  - Cybersecurity (42 skills)")
            print("  - VLSI Design (22 skills)")
            print("  - VLSI Verification (8 skills)")
            print("  - VLSI Tools (12 skills)")
            print("  - Software Engineering (10 skills)")
            print("  - System Design (8 skills)")
            print("")
            
            skills_added = 0
            skills_skipped = 0
            
            for skill_data in skills_data:
                # Check if skill already exists
                existing_skill = Skill.query.filter_by(skill_name=skill_data['skill_name']).first()
                
                if existing_skill:
                    print(f"Skipped: {skill_data['skill_name']} (already exists)")
                    skills_skipped += 1
                    continue
                
                # Create new skill
                skill = Skill(
                    skill_name=skill_data['skill_name'],
                    category=skill_data['category'],
                    description=skill_data['description']
                )
                
                db.session.add(skill)
                skills_added += 1
                print(f"Added: {skill_data['skill_name']} ({skill_data['category']})")
            
            # Commit all changes
            db.session.commit()
            
            print(f"\n✅ Skill population completed!")
            print(f"📊 Summary:")
            print(f"   - Skills added: {skills_added}")
            print(f"   - Skills skipped: {skills_skipped}")
            print(f"   - Total skills in database: {Skill.query.count()}")
            
            # Show skills by category
            print("\n📋 Skills by Category:")
            categories = db.session.query(Skill.category).distinct().all()
            for category_tuple in categories:
                category = category_tuple[0]
                count = Skill.query.filter_by(category=category).count()
                print(f"   - {category}: {count} skills")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error populating skills: {str(e)}")
            raise

if __name__ == '__main__':
    populate_skills()