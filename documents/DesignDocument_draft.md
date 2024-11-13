# Project Design Document

## Your Project Title
--------
Prepared by:

* `Jonathan Tinti`,`WPI`
* `Alan Wang`,`WPI`
* `Oliver Reera`,`WPI`
* `Chris Smith`,`WPI`
---

**Course** : CS 3733 - Software Engineering 

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Software Design](#2-software-design)
    - [2.1 Database Model](#21-model)
    - [2.2 Subsystems and Interfaces](#22-subsystems-and-interfaces)
    - [2.2.1 Overview](#221-overview)
    - [2.2.2 Interfaces](#222-interfaces)
    - [2.3 User Interface Design](#23-view-and-user-interface-design)
- [3. References](#3-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)

<a name="revision-history"> </a>

### Document Revision History

| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2024-11-15 |Initial draft | 1.0        |
|      |      |         |         |


# 1. Introduction

The purpose of this document is to create a skeleton for the project so we know what basic templates and database tables to have in the project. We establish all of the relations for different tables in this document so when we begin to code, we already understand how the different classes interact. This will create a more efficient system when we begin to start coding. This is what our final product plan is, so it is an example for what our final product should look like so we can work to create a similar product. 

# 2. Software Design

(**Note**: For all subsections of Section-2: You should describe the design for the end product (completed application) - not only your iteration1 version. You will revise this document and add more details later.)

## 2.1 Database Model

1. User: abstract class that stores the common information for instructor and student.
2. Student: stores information for each system such as GPA, experience, and graduation date.
3. Instructor: stores information for each instructor such as the course sections they are teaching to allow for them to create SA positions
4. Course: stores information on each course offered in the CS department such course number and name.
5. Course section: stores information for a specific course such as when the course is offered and the section name
6. SA Position: stores information for the position the instructor created which specifies requirements such as minimum GPA and the number of SA positons available
7. SA Application: stores information for the application a Student submitted such as their grade in the class and year they took the class. 

Provide a UML diagram of your database model showing the associations and relationships among tables. 

## 2.2 Subsystems and Interfaces

### 2.2.1 Overview

Describe the high-level architecture of your software:  i.e., the major subsystems and how they fit together. Provide a UML component diagram that illustrates the architecture of your software. Briefly mention the role of each subsystem in your architectural design. Please refer to the "System Level Design" lectures in Week 4. 

### 2.2.2 Interfaces

Include a detailed description of the routes your application will implement. 
* Brainstorm with your team members and identify all routes you need to implement for the **completed** application.
* For each route specify its “methods”, “URL path”, and “a description of the operation it implements”.  
* You can use the following table template to list your route specifications. 
* Organize this section according to your subsytem decomposition, i.e., include a sub-section for each subsytem and list all routes for that sub-section in a table.  

#### 2.2.2.1 \<Subsystem1> Routes

|   | Methods           | URL Path   | Description  |
|:--|:------------------|:-----------|:-------------|
|1. |                   |            |              |
|2. |                   |            |              |
|3. |                   |            |              |
|4. |                   |            |              |
|5. |                   |            |              |
|6. |                   |            |              |

#### 2.2.2.2 \<Subsystem2> Routes

|   | Methods           | URL Path   | Description  |
|:--|:------------------|:-----------|:-------------|
|1. |                   |            |              |
|2. |                   |            |              |
|3. |                   |            |              |
|4. |                   |            |              |
|5. |                   |            |              |
|6. |                   |            |              |

Repeat the above for other subsystems you included in your application. 

### 2.3 User Interface Design 
1. login.html
2. register_instructor.html
3. register_student.html
4. _create_position.html
5. _create_section.html
6. edit_instrcutorprofile.html
7. edit_instrcutorstudent.html
8. _apply.html
9. view_application.html
10. base.html
11. index.html

Provide a list of the page templates you plan to create and supplement your description with UI sketches or screenshots. Make sure to mention which user-stories in your “Requirements and Use Cases" document will utilize these interfaces for user interaction. 

# 3. References

Cite your references here.

For the papers you cite give the authors, the title of the article, the journal name, journal volume number, date of publication and inclusive page numbers. Giving only the URL for the journal is not appropriate.

For the websites, give the title, author (if applicable) and the website URL.

