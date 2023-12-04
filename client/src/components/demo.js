import * as React from 'react';
import Paper from '@mui/material/Paper';
import { ViewState } from '@devexpress/dx-react-scheduler';
import {
  Scheduler,
  WeekView,
  Appointments,
  AppointmentForm,
  AppointmentTooltip,
} from '@devexpress/dx-react-scheduler-material-ui';
import './demo.css';

// import { schedules } from './Demo/scheduleData';
import { schedules } from './Demo/data';


const generateAppointments = (classes) => {
    const appointments = [];
  
    const parseHours = (hoursString) => {
        const [startPart, endPart] = hoursString.split('-').map(part => part.trim());
        
        const parseTimePart = (timePart) => {
            const [hourStr, minuteStr] = timePart.match(/\d+|\bam\b|\bpm\b/g);
            const amPm = timePart.includes('pm') ? 'pm' : timePart.includes('am') ? 'am' : '';
            let hour = parseInt(hourStr, 10);
            const minute = minuteStr ? parseInt(minuteStr, 10) : 0;
          
            if (amPm === 'pm' && hour < 12) {
              // Convert to 24-hour format
              hour += 12;
            } else if (amPm === 'am' && hour === 12) {
              // Special case: 12 am should be 0 in 24-hour format
              hour = 0;
            }
          
            return { hour, minute };
          };
      
        const { hour: startHour, minute: startMinute } = parseTimePart(startPart);
        const { hour: endHour, minute: endMinute } = parseTimePart(endPart);
      
        return {
          startHour,
          startMinute,
          endHour,
          endMinute,
        };
      };
  
    classes.forEach((course) => {
      course.lectures.forEach((lecture) => {
        lecture.times.forEach(({ days, hours }) => {
          let { startHour, startMinute, endHour, endMinute } = parseHours(hours);

          days.split('').forEach((day) => {
            const dayOffset = {
              M: 0,
              T: 1,
              W: 2,
              R: 3,
              F: 4,
            }[day];
  
            const startDate = new Date(2023, 11, 4);
            startDate.setDate(startDate.getDate() + dayOffset);
            startDate.setHours(startHour, startMinute);
  
            const endDate = new Date(2023, 11, 4);
            endDate.setDate(endDate.getDate() + dayOffset);
            endDate.setHours(endHour, endMinute);
  
            const appointment = {
              title: `${course.subjectArea} ${course.name}`,
              startDate,
              endDate,
              professors: lecture.professors.join(', '),
              rating: course.rating,
              units: course.units,
              discussions: lecture.discussions,
              hotseatGraph: course.hotseatGraph,

            };
            appointments.push(appointment);
          });
        });
      });
    });
  
    console.log("appintments: ", appointments);
    return appointments;
  };

  const Schedule = ({ schedule }) => {
    const data = generateAppointments(schedule.classes);
  
    return (
      <Paper>
        <Scheduler data={data} height={660}>
          <ViewState currentDate={schedule.currentDate} />
          <WeekView startDayHour={8} endDayHour={22} />
          <Appointments />
          <AppointmentTooltip
            showCloseButton
            contentComponent={({ style, appointmentData, ...restProps }) => (
              <AppointmentTooltip.Content
                {...restProps}
                appointmentData={appointmentData}
                style={{ ...style, whiteSpace: 'normal' }}
              >
                <div>
                    <div>
                        {`Professor: ${appointmentData.professors}`}
                    </div>
                    <div>
                        {`Units: ${appointmentData.units}`}
                    </div>
                    <div>
                        {`Bruinwalk Rating: ${appointmentData.rating}`}
                    </div>
                    <div>
                        Discussions:
                        <ul>
                            {appointmentData.discussions.map((discussion) => (
                                <li key={discussion.id}>
                                {`${discussion.id} - ${discussion.times[0].days} ${discussion.times[0].hours}`}
                                </li>
                            ))}
                        </ul>
                    </div>
                    <div>
                    {/* Render the hotseatGraph HTML content */}
                    <div dangerouslySetInnerHTML={{ __html: appointmentData.hotseatGraph }} />
                  </div>
                </div>
              </AppointmentTooltip.Content>
            )}
          />
          <AppointmentForm />
        </Scheduler>
      </Paper>
    );
  };

  export default class Demo extends React.PureComponent {
    constructor(props) {
      super(props);
  
      console.log('schedules in constructor:', schedules);
  
      this.state = {
        currentDate: '2023-12-03',
        startDayHour: 8,
        endDayHour: 22,
        currentScheduleIndex: 0,
      };
    }

    handleNextSchedule = () => {
      this.setState((prevState) => ({
        currentScheduleIndex: (prevState.currentScheduleIndex + 1) % schedules.length,
      }));
    };
  
    handlePrevSchedule = () => {
      this.setState((prevState) => ({
        currentScheduleIndex:
          (prevState.currentScheduleIndex - 1 + schedules.length) % schedules.length,
      }));
    };
  
    render() {
      const { currentScheduleIndex } = this.state;
      const currentSchedule = schedules[currentScheduleIndex];
  
      return (
        <div>
          <Schedule schedule={currentSchedule} />
          <div className="BoxContainer" style={{ marginTop: '15px' }}>
            <button className="prevSchedule" onClick={this.handlePrevSchedule}>Previous Schedule</button>
            <button className="nextSchedule" onClick={this.handleNextSchedule}>Next Schedule</button>
          </div>
          <div className="BoxContainer">
            <div className='scheduleIndex'>Showing Schedule {currentScheduleIndex + 1} of {schedules.length}</div>
          </div>
        </div>
      );
    }
  }
