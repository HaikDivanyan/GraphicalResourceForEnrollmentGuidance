import './filter.css';
import React, { useState } from 'react';
import Select from 'react-select';

export default function Filter({ sendRemainingClasses,  sendRemainingProfessors,  sendRemainingRequirements}) {

  //sending this to backend
  const [filters, setFilters] = useState({
    priorityClasses: [],
    ignoreClasses: [],
    priorityRequirements: [],
    preferredSubjects: [],
    earliestStartTime: '',
    latestEndTime: '',
    preferredDays: [],
    minClassRating: 0,
    //check if we want to change default
    minUnits: 12,
    maxUnits: 21,
    //check if we want to change default
    minNumClasses: 3,
    maxNumClasses: 5,
  });

  const url = "http://127.0.0.1:8000/schedules/";

  //send to backend
  const handleSendFilters = () => {
    console.log('Filters:', filters);

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(filters),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Response from backend:', data);
      })
      .catch(error => {
        console.error('Error sending filters to backend:', error);
      });
  };

  const handlePriorityClassesChange = (selectedOptions) => {
    const selectedPriorityClasses = selectedOptions.map(option => option.value);
    setFilters((prevFilters) => ({ ...prevFilters, priorityClasses: selectedPriorityClasses }));
  };

  const handleIgnoreClassesChange = (selectedOptions) => {
    const selectedIgnoreClasses = selectedOptions.map(option => option.value);
    setFilters((prevFilters) => ({ ...prevFilters, ignoreClasses: selectedIgnoreClasses }));
  };

  const handlePriorityRequirementsChange = (selectedOptions) => {
    const selectedRequirements = selectedOptions.map(option => option.value);
    setFilters((prevFilters) => ({ ...prevFilters, priorityRequirements: selectedRequirements }));
  };

  const handlePreferredSubjectsChange = (selectedOptions) => {
    const selectedSubjects = selectedOptions.map((option) => option.value);
    setFilters((prevFilters) => ({ ...prevFilters, preferredSubjects: selectedSubjects }));
  };

  const handleEarliestStartTimeChange = (e) => {
    setFilters((prevFilters) => ({ ...prevFilters, earliestStartTime: e.target.value }));
  };

  const handleLatestEndTimeChange = (e) => {
    setFilters((prevFilters) => ({ ...prevFilters, latestEndTime: e.target.value }));
  };

  const handlePreferredDaysChange = (selectedOptions) => {
    const selectedDays = selectedOptions.map((option) => option.value);
    setFilters((prevFilters) => ({ ...prevFilters, preferredDays: selectedDays }));
  };

  const handleMinClassRatingChange = (e) => {
    setFilters((prevFilters) => ({ ...prevFilters, minClassRating: parseFloat(e.target.value) || 0 }));
  };

  const handleMaxUnitsChange = (e) => {
    setFilters((prevFilters) => ({ ...prevFilters, maxUnits: parseInt(e.target.value, 10) || 0 }));
  };

  const handleMaxNumClassesChange = (e) => {
    setFilters((prevFilters) => ({ ...prevFilters, maxNumClasses: parseInt(e.target.value, 10) || 0 }));
  };

  console.log("UNIQUE SUBJECTS")
  let subjectOptions1 = [{ value: 'COM SCI', label: 'COM SCI' }];
  let classesOptions1 = [{ value: 'COM SCI 152B', label: 'COM SCI 152B' }];
  let requirementOptions1 = [{value: 'COMPUTER SCIENCE REQUIRED COURSES', label: 'COMPUTER SCIENCE REQUIRED COURSES'}];
  if (sendRemainingClasses) {
    const uniqueSubjectNames = [...new Set(sendRemainingClasses.map(item => item.subjectArea))];
    const uniqueClassNames = [...new Set(sendRemainingClasses.map(item => item.classId))];
    console.log(uniqueSubjectNames)
    if (uniqueSubjectNames && uniqueSubjectNames.length > 0) {
      subjectOptions1 = uniqueSubjectNames.map(subject => ({ value: subject, label: subject }));
    }
    if (uniqueClassNames && uniqueClassNames.length > 0) {
      classesOptions1 = uniqueClassNames.map(classes => ({ value: classes, label: classes }));
    }
  }
  if (sendRemainingRequirements) {
    const uniqueRequirementNames = [...new Set(sendRemainingRequirements.map(item => item.name))];
    if (uniqueRequirementNames && uniqueRequirementNames.length > 0) {
      requirementOptions1 = uniqueRequirementNames.map(requirement => ({ value: requirement, label: requirement}));
    }
  }
  const subjectOptions = subjectOptions1 
  const classesOptions = classesOptions1
  // const classesOptions = [
  //   { value: 'COM SCI 152B', label: 'COM SCI 152B' },
  //   { value: 'COM SCI 162', label: 'COM SCI 174A' },
  //   { value: 'option3', label: 'Option 3' },
  //   { value: 'option4', label: 'Option 4' },
  // ];
  const requirementOptions = requirementOptions1
  // const requirementOptions = [
  //   { value: 'COMPUTER SCIENCE REQUIRED COURSES', label: 'COMPUTER SCIENCE REQUIRED COURSES' },
  //   { value: 'COM SCI 162', label: 'COM SCI 174A' },
  //   { value: 'option3', label: 'Option 3' },
  //   { value: 'option4', label: 'Option 4' },
  // ];
  
  const daysOfWeek = [
    { value: 'Monday', label: 'Monday' },
    { value: 'Tuesday', label: 'Tuesday' },
    { value: 'Wednesday', label: 'Wednesday' },
    { value: 'Thursday', label: 'Thursday' },
    { value: 'Friday', label: 'Friday' }
  ];

    return (
      <div className="PreferenceFilter">

        <div className="SectionTitle">
        Preference Filers
        </div>

        <div className="FilterSection">
          <div className="FilterLeft">
            <div className="FilterTitle">
              Priorities
            </div>
            <div className="FilterText">
              These classes/subjects have to be in my schedule...
            </div>
          </div>

          <div className="FilterRight">
            <div className="FilterText">
              Subjects:
            </div>
            <Select
              id="subjects"
              isMulti
              options={subjectOptions}
              isSearchable
              placeholder="Search..."
              onChange={handlePreferredSubjectsChange}
            />
            <div className="FilterText">
              Classes:
            </div>
            <Select
              id="classes"
              isMulti
              options={classesOptions}
              isSearchable
              placeholder="Search..."
              onChange={handlePriorityClassesChange}
            />
          </div>
        </div>

        <div className="FilterSection">
          <div className="FilterLeft">
            <div className="FilterTitle">
              Requirements
            </div>
            <div className="FilterText">
              I want to prioritized these DARS requirements
            </div>
          </div>

          <div className="FilterRight">
            <div className="FilterText">
              Requirements
            </div>
            <Select
              id="subjects"
              isMulti
              options={requirementOptions}
              isSearchable
              placeholder="Search..."
              onChange={handlePriorityRequirementsChange}
            />
          </div>
        </div>

        <div className="FilterSection">
          <div className="FilterLeft">
            <div className="FilterTitle">
              Time of Day
            </div>
            <div className="FilterText">
              I want to start/end my classes no earlier/later than...
            </div>
          </div>

          <div className="FilterRight">
            <div className="FilterText">
                Start time:
            </div>
            <input
              type="time"
              id="startTime"
              onChange={handleEarliestStartTimeChange}
            />
            <div className="FilterText">
                End time:
            </div>
            <input
                  type="time"
                  id="endTime"
                  onChange={handleLatestEndTimeChange}
            />
          </div>
        </div>

        <div className="FilterSection">
          <div className="FilterLeft">
            <div className="FilterTitle">
              Days
            </div>
            <div className="FilterText">
              I want to have classes on...
            </div>
          </div>

          <div className="FilterRight">
            <div className="FilterText">
              Days
            </div>
            <Select
              id="days"
              isMulti
              options={daysOfWeek}
              isSearchable
              placeholder="Search..."
              onChange={handlePreferredDaysChange}
            />
          </div>
        </div>

        <div className="FilterSection">
          <div className="FilterLeft">
            <div className="FilterTitle">
              Ignore Classes
            </div>
            <div className="FilterText">
              These classes should not be in my schedule...
            </div>
          </div>

          <div className="FilterRight">
            <div className="FilterText">
              Classes:
            </div>
            <Select
              id="subjects"
              isMulti
              options={subjectOptions}
              isSearchable
              placeholder="Search..."
              onChange={handleIgnoreClassesChange}
            />
          </div>
        </div>

        <div className="FilterSection">
          <div className="FilterLeft">
            <div className="FilterTitle">
              Class Rating
            </div>
            <div className="FilterText">
              I want my classes to have rating...
            </div>
          </div>

          <div className="FilterRight">
            <div className="FilterText">
                Rating greater than:
            </div>
            <input
                  type="number"
                  id="rating"
                  step="0.01" 
                  onChange={handleMinClassRatingChange}
            />
          </div>
        </div>

        <div className="FilterSection">
          <div className="FilterLeft">
            <div className="FilterTitle">
              Class Units
            </div>
            <div className="FilterText">
              I want to take this many units..
            </div>
          </div>

          <div className="FilterRight">
            <div className="FilterText">
                Units:
            </div>
            <input
                  type="number"
                  id="UnitNum"
                  onChange={handleMaxUnitsChange}
            />
          </div>
        </div>

        <div className="FilterSection">
          <div className="FilterLeft">
            <div className="FilterTitle">
              Number of Class
            </div>
            <div className="FilterText">
              I want to take this many classes..
            </div>
          </div>

          <div className="FilterRight">
            <div className="FilterText">
                Classes:
            </div>
            <input
                  type="number"
                  id="ClassNum"
                  onChange={handleMaxNumClassesChange}
            />
          </div>
        </div>

        <div className="ButtonContainer">
          <button className="generateButton"onClick={handleSendFilters}>Generate Schedule</button>
        </div>

      </div>
    );
  }