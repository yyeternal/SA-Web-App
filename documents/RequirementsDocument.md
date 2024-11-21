# Software Requirements and Use Cases

## SA Recruitment Web App
--------
Prepared by:

* `Jonathan Tinti`,`WPI`
* `Oliver Reera`,`WPI`
* `Alan Wang`,`WPI`
* `Chris Smith`,`WPI`

---

**Course** : CS 3733 - Software Engineering

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Requirements Specification](#2-requirements-specification)
  - [2.1 Customer, Users, and Stakeholders](#21-customer-users-and-stakeholders)
  - [2.2 User Stories](#22-user-stories)
  - [2.3 Use Cases](#23-use-cases)
- [3. User Interface](#3-user-interface)
- [4. Product Backlog](#4-product-backlog)
- [4. References](#4-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)

<a name="revision-history"> </a>

## Document Revision History

| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2024-11-07 |Initial draft | 1.0 |
|Revision 2 |2024-11-07 |Added use cases and user stories | 1.3 |
|      |      |         |         |

----
# 1. Introduction

This application will be used as a resource for student assistant applications for courses in Computer Science at WPI. There will be an option to sign in as a potential student assistant or an instructor. Depending on if the user is a student or if they are an instructor, there will be different features contained in the app; For example, it would not make sense to have a section of the app dedicated to looking for SA positions for users who are instructors. Rather, there should be a section that allows instructors to create SA positions themselves and then look at students who have shown interest in the position. For SAs there will be options to look for open positions and allow them to apply for those positions online, and withdraw if they no longer want to pursue that position. For instructors, they will be able to easily look through SA applications and hire the right fit for their class. 

----
# 2. Requirements Specification

Considering that there will be information stored in the way of usernames, passwords, contact info, SA positions, and more, a database will be required to store the necessary information. For this, we will use Postgres. Additionally, HTML will be used as an interface between the users and the database.

## 2.1 Customer, Users, and Stakeholders

The Customer is Worcester Polytechnic Institute and, as such, the stakeholders will be the faculty members of WPI, students applying for SA positions, and students in classes who have SAs. The users of this application will be instructors and students on campus. To be more specific, the users will be instructors interested in having student assistants in their classes, and students who are interested in becoming SA’s.

----
## 2.2 User Stories

1. As an SA, I want to make an account to search for SA positions.
2. As an SA, I want to log in to my student account using WPI credentials or SSO in order to access the app.
3. As a student, I want to be able to view all open SA positions to see what would appeal most to me.
4. As a student, I want to be able to view my recommended SA positions in a ranked list to give me a better understanding of what positions I should be       applying to. 
5. As a student, I want to be able to view all of the important information about the position to see if I am available and willing to SA this class. 
6. As a student, I want to be able to apply for multiple SA positions with my academic information in order to potentially get the role. 
7. As a student, I want to be able to view my application status so I can know if I have been accepted.
8. As a student, I want to be able to withdraw my application if I no longer want to be an SA for that class. 

9. As an instructor, I want to be able to create my instructor account using my WPI credentials in order to find SA positions for my class. 
11. As an instructor, I want to be able to log in to my instructor account using WPI credentials or SSO to look for SA positions for my classes.
<<<<<<< HEAD
12. As an instructor, I want to add course sections to the available Computer Science courses that I will be teaching that may require SA’s.
=======
12. As an instructor, I want to add course sections that I will be teaching that may require SA’s.
>>>>>>> 8ef44c38c8690f22f6212dca024c913b555be09e
13. As an instructor, I want to be able to create an SA position for my course so students can apply for it. 
14. As an instructor, I want to view all of the SA applications related to my course sections.
15. As an instructor, I want to be able to set qualifications for the position as well as the number of openings to find the right people for the job. 
16. As an instructor, I want to be able to view the students who have applied to the position to see how many have applied for this course. 
17. As an instructor, I want to be able to view each student’s qualifications to see who meets the requirements for the position. 
18. As an instructor, I would like the option to add an SA applicant to an SA position.

----
## 2.3 Use Cases

| Use case # 1      |   |
| ------------------ |--|
| Name              | Create Account  |
| Participating actor  | Both students and instructors  |
| Entry condition(s)   | Selecting a “create account” path.  |
| Exit condition(s)    | Either by pressing submit or cancel.  |
| Flow of events |1. The user selects "Create a new account."  
                  2. The system responds by prompting the user to specify “student” or “instructor."
                  3. The user selects the “student” option.
                  4. The system gives the user fields to enter information that includes a username, password, name, last name, WPI ID, email, phone number, major, cumulative GPA, expected graduation date, and previous SA experience.
                  5. The user hits submit.
                  6. The system notifies the user that their account has been created.
                  7. The user is redirected to the login page.|
| Alternative flow of events    | Instead of selecting “student,” “instructor” is selected instead. The system then prompts the user to fill in the fields for  username, password, first name, last name, WPI ID, email, and phone number. User clicks submit. The system notifies the user that the account was created successfully. User is redirected to the login page.|
| Iteration #         | 1 |

| Use case # 2      |   |
| ------------------ |--|
| Name              | Login  |
| Participating actor  | Both students and instructors  |
| Entry condition(s)   | Selecting a "login" option.  |
| Exit condition(s)    | Logging in, or a redirect with a “try again” message  |
| Flow of events |1. The user selects the login option.
                  2. The system responds with two fields, a username and a password field.
                  3. The user enters their username and password, clicking “log in” when complete.
                  4. The system redirects to a home page with options depending on if it is a student login or an instructor login.|
| Alternative flow of events    | In step 3, if the username or password is incorrect, a “try again” message will pop up, and the user will not be logged in. |
| Iteration #         | 1 |

| Use case # 3      |   |
| ------------------ |--|
| Name              | View Open SA Positions  |
| Participating actor  | Student users  |
| Entry condition(s)   | The student is logged into the system and selects the view option.  |
| Exit condition(s)    | Either navigating to a different part of the app or clicking on an SA position.  |
| Flow of events |1. The student selects a “view SA positions” option.
                  2. The system responds with a list of all open SA positions.
                  3. The student peruses the options and clicks on one.
                  4. The System exits the view format and displays information about the selected SA position. |
| Alternative flow of events    | Instead of clicking on an option, the user decides to go to the home menu instead. |
| Iteration #         | 2  |

| Use case # 4      |   |
| ------------------ |--|
| Name              | View Recommended Positions  |
| Participating actor  | Student users  |
| Entry condition(s)   | The student clicked the view SA positions and the system displayed the available options.  |
| Exit condition(s)    | Either navigating to a different part of the app or clicking on an SA position.  |
| Flow of events |1. The student selects “View Recommended Positions”
                  2. The system responds by filtering the listed positions and finding only the recommended SA positions for that person. 
                  3. The student peruses the options and clicks on one.
                  4. The System exits the view format and displays information about the selected SA position.|
| Alternative flow of events    | Instead of clicking on an option, the user decides to go to the home menu instead. |
| Iteration #         | 3 |

| Use case # 5      |   |
| ------------------ |--|
| Name              | Apply for an SA Position  |
| Participating actor  | Student users  |
| Entry condition(s)   | Be logged in as a student, click on “apply for SA position”.  |
| Exit condition(s)    | Either hitting submit, or hitting cancel.  |
| Flow of events |1. The student clicks on a desired position.
                  2. The system gives the user three fields to enter information: the grade earned in the course when the student took the course,
                     the year and term that they took the course, and the year and term that the student is applying for.
                  3. After hitting submit, the system responds by telling the user “Application submitted” and redirecting back to the “view SA positions” list. |
| Alternative flow of events    | In step 2, the user changes their mind and decides to cancel. As a result, the system redirects them back to the view 
                                  SA positions part of the app. |
| Iteration #         | 2 |

| Use case # 6      |   |
| ------------------ |--|
| Name              | View Applications’ Status  |
| Participating actor  | Student users  |
| Entry condition(s)   | Be logged in as a student, click on "view my current applications".  |
| Exit condition(s)    | Navigating to another part of the app.  |
| Flow of events |1. The user selects “View my current SA applications.”
                  2. The system responds with a list of “pending” and “assigned” status applications.
                  3. The user clicks on a particular application.
                  4. If it has a “pending” status, there will be an option to withdraw the application. |
| Alternative flow of events    | In step 3, the user clicks on an “assigned” application.The system shows further information about the SA position. |
| Iteration #         | 3 |

| Use case # 7      |   |
| ------------------ |--|
| Name              | Withdraw SA Application  |
| Participating actor  | Student users  |
| Entry condition(s)   | Logged in as a Student, is viewing one of their applications  |
| Exit condition(s)    | Either by pressing yes or cancel.  |
| Flow of events |1. The user clicks “Withdraw Application” on a pending SA application.
                  2. The system asks the user if they want to remove the application, giving a yes or no option as confirmation.
                  3. The user clicks yes.
                  4. The system redirects the user back to “View my current SA applications” and gives the user a message saying “SA Application successfully removed.” |
| Alternative flow of events    | In step 3, no is selected by the user instead of yes. 
                                  The system redirects to the SA application in question, rather than redirecting to the full list of current SA applications. |
| Iteration #         | 3 |

| Use case # 8      |   |
| ------------------ |--|
| Name              | Add Course Sections  |
| Participating actor  | Instructor user  |
| Entry condition(s)   | Logged in as an instructor, clicks the “add course section” feature  |
<<<<<<< HEAD
| Exit condition(s)    | New course section has been added  |
| Flow of events |1. The user selects “add course section.”
                  2. The system responds by asking the user to select a course from a list, and then requests a course section and term.
=======
| Exit condition(s)    | Either hitting submit, or hitting cancel  |
| Flow of events |1. The user selects “add course section.”
                  2. The system responds by requesting that the user enter the name of the class and then provides a course section and term.
>>>>>>> 8ef44c38c8690f22f6212dca024c913b555be09e
                  3. After filling in the necessary information, the user clicks “submit.”
                  4. The system redirects the user back to the homepage and displays a message saying “Course section added.”|
| Alternative flow of events    |Upon submitting, the system realizes that the course section is already in the database.
                                 The system responds by saying that “The course is already in the system, please double-check your course section field.” |
| Iteration #         | 1 |

| Use case # 9      |   |
| ------------------ |--|
| Name              | Create SA Position  |
| Participating actor  | Instructor user  |
| Entry condition(s)   | Logged in as an instructor, clicks the “add SA position” feature while viewing one of their classes.  |
| Exit condition(s)    | Either hitting submit, or hitting cancel  |
| Flow of events |1. The user clicks on an already existing course that they created.
                  2. The user clicks an “add SA position button.”
                  3. The system responds by asking for the number of SA positions desired for the course section and asking for requirements such as GPA, minimum grade earned, and prior SA experience.
                  4. After all the information is included, the user submits the positions.
                  5. The system notifies the user that the positions were added, and then the system redirects the user to their other courses. |
| Alternative flow of events    | If there is nothing added to the qualifications field, then the position will be added without these constraints. |
| Iteration #         | 1 |

| Use case # 10      |   |
| ------------------ |--|
| Name              | View SA Applications  |
| Participating actor  | Instructor user  |
| Entry condition(s)   | Logged in as an instructor, clicks the “view current applications” feature while viewing one of their classes.  |
| Exit condition(s)    | Navigating to another part of the app.  |
| Flow of events |1. The user clicks “view current applications.”
                  2. The system provides a list of SA applicants, the course section they applied for, and whether or not they have been assigned to another course or not.
                  3. The user can look through all of the applicants for their courses.|
| Alternative flow of events    | N/A |
| Iteration #         | 2 |

| Use case # 11      |   |
| ------------------ |--|
| Name              | View SA Qualifications  |
| Participating actor  | Instructor user  |
| Entry condition(s)   | Logged in as an instructor, clicks the “view qualifications” feature while viewing SA applications.  |
| Exit condition(s)    | Clicking a different part of the app, or hitting a back button.  |
| Flow of events |1. The user selects “view qualifications” on an SA application from the list of all applications.
                  2. The system responds with information about the SA applicant, such as GPA, grades, and prior experience.
                  3. The user views the information, and can either go back to other applicants, or select other features of the app. |
| Alternative flow of events    | N/A |
| Iteration #         | 3 |

| Use case # 12      |   |
| ------------------ |--|
| Name              | Add SA to Course  |
| Participating actor  | Instructor user  |
| Entry condition(s)   | Logged in as an instructor, clicks the “add SA to course section” feature while viewing a student application.  |
| Exit condition(s)    | Either hitting submit, or hitting cancel.  |
| Flow of events |1. The user clicks on the “Add SA to Course Section” from an SA application.
                  2. The system responds by asking for a confirmation of “yes” or “no” to add the SA to the course section.
                  3. The user selects the “yes” option.
                  4. The system responds by giving the message “SA successfully enrolled.” Furthermore, the SA applicant’s assigned value becomes true. 
                     The user is then redirected to their SA applications view. |
| Alternative flow of events    | When hitting the “no” button, the system cancels everything, redirecting back to the view SA applications section of the app. |
| Iteration #         | 3 |

| Use case # 13      |   |
| ------------------ |--|
| Name              | Edit Account  |
| Participating actor  | Either an instructor or student user.  |
| Entry condition(s)   | Logged in as an instructor or student.  |
| Exit condition(s)    | Either hitting submit, or hitting cancel.  |
| Flow of events |1. The user selects the edit profile option.
                  2. The system redirects to an “edit profile” form, where the user can change their password and other information.
                  3. After the user fills in the information, the user submits the edits.
                  4. The system asks for confirmation with a message: “Would you like to make these changes?”
                  5. The user responds with yes.
                  6. The system responds with a message: “Profile successfully edited” and redirects to the home screen. |
| Alternative flow of events    | If 5 is “No,” then the edit is canceled. |
| Iteration #         | 1 |


----
# 3. User Interface
Here are featured some of the main pages for our web app's use cases. *Created with Figma*

  <kbd>
      <img src="images/Frame 1.jpg"  border="2">
  </kbd>

  <kbd>
      <img src="images/Frame 2.jpg"  border="2">
  </kbd>

  <kbd>
      <img src="images/Frame 3.jpg"  border="2">
  </kbd>

  <kbd>
      <img src="images/Frame 4.jpg"  border="2">
  </kbd>
  
  <kbd>
      <img src="images/Frame 5.jpg"  border="2">
  </kbd>
  
  <kbd>
      <img src="images/Frame 6.jpg"  border="2">
  </kbd>
  
  <kbd>
      <img src="images/Frame 7.jpg"  border="2">
  </kbd>
  
  <kbd>
      <img src="images/Frame 8.jpg"  border="2">
  </kbd>
  
  <kbd>
      <img src="images/Frame 9.jpg"  border="2">
  </kbd>
  
  <kbd>
      <img src="images/Frame 10.jpg"  border="2">
  </kbd>
  
  <kbd>
      <img src="images/Frame 11.jpg"  border="2">
  </kbd>
  
  <kbd>
      <img src="images/Frame 12.jpg"  border="2">
  </kbd>
  
  <kbd>
      <img src="images/Frame 13.jpg"  border="2">
  </kbd>
  
----
# 4. Product Backlog

  Here is our GitHub issues page that outlines this project's product backlog: 
  
  https://github.com/WPI-CS3733-2024B/team-stackoverflowheroes/issues

----
# 5. References

Creating an issue. (n.d.). GitHub Docs. Retrieved November 7, 2024, from https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue

<<<<<<< HEAD
=======

----
----
# Appendix: Grading Rubric


| Max Points  | **Content** |
| ----------- | ------- |
| 4          | Do the requirements clearly state the customers’ needs? |
| 2          | Do the requirements avoid specifying a design (note: customer-specified design elements are allowed)? |
| | |  
|    | **Completeness** |
| 14 | Are user stories complete? Are all major user stories included in the document?  |
| 5 | Are user stories written in correct form? | 
| 14 |  Are all major use cases (except registeration and login) included in the document? |
| 15 | Are use cases written in sufficient detail to allow for design and planning? Are the "flow of events" in use case descriptions written in the form of "user actions and system responses to those"? Are alternate flow of events provided (when applicable)? | 
| 6 |  Are the User Interface Requirements given with some detail? Are there some sketches, mockups?  |
| | |  
|   | **Clarity** |
| 5 | Is the document carefully written, without typos and grammatical errors? <br> Is each part of the document in agreement with all other parts? <br> Are all items clear and not ambiguous? |
| | |
|**65**|**TOTAL**|


>>>>>>> 8ef44c38c8690f22f6212dca024c913b555be09e
