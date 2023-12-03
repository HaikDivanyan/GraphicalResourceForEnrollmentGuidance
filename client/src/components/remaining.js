import React from "react";
import './remaining.css';

export default function Remaining({sendRemainingClasses, sendRemainingProfessors, sendRemainingRequirements}) {

    return (
    <div className="RemainingSection">
      <div className="SectionTitle">
        Remaining Courses
      </div>
        <div className="SectionDescription">
            Here are the courses you have left to take at UCLA
        </div>
        <div className="BoxContainer">
            <div className="CoursesBox">
            {console.log(sendRemainingClasses)}
              {console.log(sendRemainingRequirements)}
              {sendRemainingRequirements && sendRemainingRequirements.map((course, index) => (
                  <div key={index}>
                    {course.name}
                    {course.subrequirements.map((subreq, subIndex) => (
                        <li key={subIndex}>
                          {subreq.classes}
                          </li>
                      ))}
                  </div>
              ))}
                {/* course 1
                <br></br>
                course 2
                <br></br>
                course 3
                <br></br> */}
            </div>
        </div>
    </div>
    );
  }