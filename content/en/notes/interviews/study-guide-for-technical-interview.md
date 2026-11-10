---
title: Study Guide for Technical Interview
category: Interviews
description: 1. What is the difference between an abstract class and an interface?
tags:
- interview
---

<!-- imported from ObsidianVault/webdev/interviews/Study Guide for Technical Interview.md. Edit the source, then run sync.py. -->

# Study Guide for Technical Interview

`interview`

## **Programming in Java I**

- Java syntax, variables, data types
- Control structures (loops, conditionals)
- Object-Oriented Programming (OOP) concepts: Classes, Objects, Encapsulation, Inheritance, Polymorphism
- Exception handling
- Input/Output (I/O) in Java
- Basic collections (ArrayList, HashMap)
- Basic multithreading (Runnable, Thread class)

## **Programming in Java II**

- Advanced OOP concepts (Abstract classes, Interfaces)
- Java Generics
- Java Streams and Lambda expressions
- File handling (BufferedReader, FileWriter, etc.)
- Concurrency (ExecutorService, Synchronization, Locks)
- Java Networking (Sockets, HTTP requests)
- JDBC (Java Database Connectivity)

## **OS Concepts & Usage**

- Process management (scheduling, states, IPC)
- Memory management (paging, segmentation, virtual memory)
- File systems and storage management
- Basic shell scripting and command-line usage
- Threads and concurrency

## **Computer Organization**

- CPU architecture (ALU, Control Unit, Registers)
- Memory hierarchy (Cache, RAM, Virtual Memory, Disk)
- Instruction Set Architecture (ISA)
- Pipelining and performance optimization
- I/O systems and buses

## **Intro to Database & Modeling**

- Relational database concepts (tables, primary/foreign keys, normalization)
- SQL (SELECT, JOIN, INSERT, DELETE, UPDATE, GROUP BY, HAVING)
- Entity-Relationship (ER) modeling
- ACID properties
- Indexing and Query Optimization

## **Data Structures & Algorithms**

- Time and space complexity (Big O notation)
- Arrays, Linked Lists, Stacks, Queues, HashTables
- Trees (Binary Trees, BST, Heaps, Trie)
- Graphs (BFS, DFS, Dijkstra's Algorithm)
- Sorting algorithms (Merge Sort, Quick Sort, Bubble Sort)
- Dynamic programming ([[web/memoization|Memoization]], Tabulation)

## **Design of IT Systems (CI/CD, etc)**

- Continuous Integration/Continuous Deployment (CI/CD)
- DevOps principles and tools (Jenkins, Docker, Kubernetes)
- [[cloud/infrastructure-as-code|Infrastructure as Code]] (Terraform, Ansible)
- Monitoring and Logging (Prometheus, Grafana, ELK stack)

## **Intro to Software Engineering (Agile, Waterfall methods)**

- Software development lifecycle (SDLC)
- Agile methodologies (Scrum, Kanban)
- Waterfall model
- Requirements gathering and analysis
- Unit testing and test-driven development (TDD)

## **OS Internals and Design (Linux)**

- Linux file system structure
- Process scheduling and management
- Memory management in Linux
- Kernel modules and device drivers
- Shell scripting

## **Comparative Languages**

- Object-Oriented Programming (Java, Python, Ruby)
- Functional Programming (Haskell, Racket, Lambda expressions)
- Dynamic vs Static typing
- Scripting languages vs compiled languages
- Concurrency and Parallelism in different languages

## **[[security/cryptography|Cryptography]] & Data Security**

- Symmetric vs Asymmetric encryption (AES, RSA, ECC)
- Hashing algorithms (SHA, MD5, bcrypt)
- Digital Signatures and Certificates
- Public Key Infrastructure (PKI)
- Secure Communication (SSL/TLS, HTTPS)

## **Intro to Machine Learning**

- Supervised vs Unsupervised learning
- Common algorithms (Linear Regression, Decision Trees, SVM, Neural Networks)
- Overfitting and Underfitting
- Model evaluation metrics (Precision, Recall, F1-Score)
- Feature Engineering and Data Preprocessing

## **Network Security Attacks and Defenses**

- [[networking/osi-model|OSI Model]] and TCP/IP Stack
- Common attacks (MITM, DDoS, Phishing, SQL Injection)
- Firewall and IDS/IPS
- VPN and encryption protocols (IPSec, TLS)
- Public and Private IP addressing, NAT

## **Cyber Network Security**

- Authentication mechanisms ([[cloud/multi-factor-authentication|MFA]], OAuth, SAML)
- Secure coding practices (OWASP Top 10)
- Endpoint security
- Secure network architecture
- Incident response and forensic analysis

## **Theory of Computing**

- Finite Automata (DFA, NFA)
- Regular expressions and regular languages
- Pushdown Automata and Context-Free Grammars
- Turing Machines and decidability
- Complexity classes (P, NP, NP-Complete)

### **Programming in Java I & II**

1. What is the difference between an abstract class and an interface?
	- abstract class can define a method and its implementation.
	- Use an **abstract class** when you need to provide some shared behavior across related classes.
	- Use an **interface** when you want to enforce a contract without specifying any implementation (especially for unrelated classes that share common behavior).
2. How does Java handle memory management?
3. What are Java Streams and how do they work?
4. What is the purpose of the `synchronized` keyword in Java? ...

### **OS Concepts & Usage**

5. What is virtual memory and how does it work?
6. Explain the different types of process scheduling algorithms. ...

### **Computer Organization**

7. What is pipelining and how does it improve CPU performance?
8. Explain the concept of cache memory. ...

### **Database & Modeling**

9. What is the difference between normalization and denormalization?
10. How does indexing improve query performance? ...

### **Data Structures & Algorithms**

11. What is the time complexity of quicksort in the average case?
12. Explain the difference between BFS and DFS.
	- **Use BFS** when you need the **shortest path** in an **unweighted** graph (e.g., shortest path in a maze or social network).
	- **Use DFS** for **topological sorting, cycle detection, and solving puzzles** (like mazes where you need to explore all possibilities before backtracking).

### **Design of IT Systems (CI/CD, etc)**

13. What is the purpose of a CI/CD pipeline?
14. Explain the role of Docker in DevOps. ...

### **Intro to Software Engineering**

15. What are the key differences between Agile and Waterfall methodologies?
16. What is Test-Driven Development (TDD)? ...

### **OS Internals and Linux**

17. What are the main responsibilities of the Linux kernel?
18. How does process management work in Linux? ...

### **Comparative Languages**

19. What are the differences between dynamic and static typing?
20. Explain functional programming and give an example. ...

### **Cryptography & Data Security**

21. What is the difference between symmetric and asymmetric encryption?
22. How does SSL/TLS work? ...

### **Network Security & Theory of Computing**

23. What is the OSI model and why is it important?
24. Explain the concept of finite automata. ...
