import React, { useState, useEffect } from 'react';
import Landing from './components/landing';
import NavBar from './components/navbar';
import Instruction from './components/instruction';
import Upload from './components/upload';
import Remaining from './components/remaining';
import Footer from './components/footer';
import Filter from './components/filter';
import Schedule from './components/schedule';
import Download from './components/download';
import Demo from './components/demo';
import './App.css';

function App() {
  const [remainingClasses, setClasses] = useState();
  const [remainingProfessors, setProfessors ] = useState();
  const [remainingRequirements, setRequirements] = useState();
  const [file, setFile] = useState();
  const [schedules, setSchedules] = useState();

  useEffect(() => {
    // This code will run every time remainingClasses is updated
    console.log('Schedules:', schedules);
  }, [remainingClasses, remainingProfessors, remainingRequirements, file, schedules]);

  return(
    <div>
      <NavBar/>
      <Landing/>
      <div className='BlueSection'></div>
      <Instruction/>
      <div className='BlueSection'></div>
      <Upload
        setRemainingClasses={setClasses}
        setRemainingProfessors={setProfessors}
        setRemainingRequirements={setRequirements}
        setDarsFile = {setFile}
      />
      {console.log("Dars file given")}
      {console.log(file)}
      <div className='BlueSection'></div>
      <Remaining
        sendRemainingClasses = {remainingClasses}
        sendRemainingProfessors = {remainingProfessors}
        sendRemainingRequirements = {remainingRequirements}
      />
      <div className='BlueSection'></div>
      <Filter
        sendRemainingClasses = {remainingClasses}
        sendRemainingProfessors = {remainingProfessors}
        sendRemainingRequirements = {remainingRequirements}
        sendFileBack = {file}
        setReturnedSchedule = {setSchedules}
      />
      <div className='BlueSection'></div>
      {/* <Schedule/> */}
      <Demo
        sendScheduleIn = {schedules}
      />
      <div className='BlueSection'></div>
      {/* <Download/> */}
      <Footer/>
    </div>
  )
}

export default App;