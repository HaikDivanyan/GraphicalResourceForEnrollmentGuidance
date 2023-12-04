import * as React from 'react';
import * as d3 from 'd3';
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
import { useRef, useEffect, useState } from 'react';
import Chart from "chart.js/auto";
import html2canvas from 'html2canvas';
import canvasToSvg from "canvas-to-svg";

  const Schedule = ({ schedule }) => {

    const chartRef = useRef(null);
    const [data, setData] = useState();
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
      if (classes) {
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
  
              const categories = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F'];
              // // console.log("COURSE", course,jk course.gradeDistributions);
              // console.log("COURSE", course);
              const datasets = Object.entries(course.gradeDistributions).map(([key, values]) => ({
                  label: key,
                  data: values,
                  backgroundColor: 'rgba(75, 192, 192, 0.2)',
                  borderColor: 'rgba(75, 192, 192, 1)',
                  borderWidth: 1
              }));
  
             
             
              const canvas = document.createElement('canvas');
              canvas.width = 400;
              canvas.height = 200;
              var ctx = canvas.getContext('2d');
             
           
             const image = new Image();
             image.src = canvas.toDataURL();
             const imageString = new XMLSerializer().serializeToString(image);
             console.log("IMAGE", imageString);
      
             canvas.style.zIndex = '99';
             canvas.id = "test-canvas"
             

             const svgElement = document.createElementNS("http://www.w3.org/2000/svg", "svg");
             
             // Set attributes for the SVG element
             svgElement.setAttribute("width", "500");
             svgElement.setAttribute("height", "300");

             const height = 100;
             const width = 300;
             let maxFreq = 0
             datasets.forEach((dataset) => {
              console.log("DATASET", dataset);
              dataset.data.forEach(frequency => {
                maxFreq = Math.max(maxFreq, frequency);
              })
           
       
             console.log("MAX FREQ", maxFreq);
             const svg = d3.select(svgElement);
             const xScale = d3.scaleBand().domain(categories).range([0, width]).paddingOuter(.9); //0.1
             const yScale = d3.scaleLinear().domain([0, Math.ceil(maxFreq*1.1)]).range([height,0]);
             yScale.domain([0, Math.ceil(maxFreq * 1.1)]);
             console.log("DATA", datasets[0].data)
             svg.selectAll(".bar")
                .data(datasets[0].data) // convert this to averages or something
                .enter().append("rect")
                .attr("class", "bar")
                .attr("x", (d, i)=> xScale(categories[i]))
                .attr("y", d=> 100 - d)
                .attr('width', xScale.bandwidth())
                .attr("height", d=> d)
                .attr("fill", "red")
              svg.append("g")
                .attr("transform", "translate(0," + height +")")
                .call(d3.axisBottom(xScale));
              svg.append("g")
                //.attr("transform", "translate(0," + 10 +")")
                .call(d3.axisLeft(yScale).ticks(2));
              console.log(svgElement, new XMLSerializer().serializeToString(svgElement));
            }) 
              const appointment = {
                title: `${course.subjectArea} ${course.name}`,
                startDate,
                endDate,
                professors: lecture.professors.join(', '),
                rating: course.rating,
                units: course.units,
                discussions: lecture.discussions,
                hotseatGraph: course.hotseatGraph,
                gradeHistogram: new XMLSerializer().serializeToString(svgElement)
              
  
              };
              appointments.push(appointment);
            });
          });
        });
      });
      }
      else {
        console.log("NO CLASSES")
      }
      console.log("appintments: ", appointments);
      return appointments;
    };
    useEffect(() => {
      setData( generateAppointments(schedule.classes))
    }, [schedule]);
    
    return (
      <Paper>
        <Scheduler data={data} height={660}>
          <ViewState currentDate={schedule.currentDate} />
          <WeekView startDayHour={8} endDayHour={22} />
          <div onClick={()=>{console.log("TEST")}}>
          <Appointments/>
          </div>
          <AppointmentTooltip
           // onOpenButtonClick={()=>{console.log("OPENBUTTON")}}
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
                    <div >
                            HotSeat
                        {/* <canvas id="gradeHistogram" width="10" height="5"></canvas> */}
            
                    </div>
                    <div>
                    {/* Render the hotseatGraph HTML content */}
                    <div dangerouslySetInnerHTML={{ __html: appointmentData.hotseatGraph }} />
                    <div >BruinWalk</div>
                    <div dangerouslySetInnerHTML={{ __html: appointmentData.gradeHistogram }} />
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
  
      console.log('schedules in constructor:', this.props.sendScheduleIn);
  
      this.state = {
        currentDate: '2023-12-03',
        startDayHour: 8,
        endDayHour: 22,
        currentScheduleIndex: 0,
      };
    }
   
    handleNextSchedule = () => {
      this.setState((prevState) => ({
        currentScheduleIndex: (prevState.currentScheduleIndex + 1) % this.props.sendScheduleIn.length,
      }));
    };
  
    handlePrevSchedule = () => {
      this.setState((prevState) => ({
        currentScheduleIndex:
          (prevState.currentScheduleIndex - 1 + this.props.sendScheduleIn.length) % this.props.sendScheduleIn.length,
      }));
    };

  
    render() {
      
          
    const handleCaptureScreenshot = () => {
      const element = document.getElementById('capture'); // Replace 'capture' with the ID of the element you want to capture
  
      html2canvas(element).then(canvas => {
        // Convert canvas to image data URL
        const dataURL = canvas.toDataURL('image/png');
  
        // Create a download link
        const downloadLink = document.createElement('a');
        downloadLink.href = dataURL;
        downloadLink.download = 'my_schedule.png';
        document.body.appendChild(downloadLink);
  
        // Trigger the download
        downloadLink.click();
  
        // Clean up
        document.body.removeChild(downloadLink);
      });
    };
    
      const { currentScheduleIndex } = this.state;
      let currentSchedule1 = '';
      if (this.props.sendScheduleIn) {
        currentSchedule1 = this.props.sendScheduleIn;
        //[currentScheduleIndex];
        console.log("Current schedule")
        console.log(currentSchedule1)
        console.log(currentSchedule1[0].classes)
      
      }
      const currentSchedule = currentSchedule1[currentScheduleIndex];
      return (
        <div id='capture'> 
          {this.props.sendScheduleIn ? (
          <>
          <Schedule schedule={currentSchedule} />
          <div className="BoxContainer" style={{ marginTop: '15px' }}>
            <button className="prevSchedule" onClick={this.handlePrevSchedule}>Previous Schedule</button>
            <button className="nextSchedule" onClick={this.handleNextSchedule}>Next Schedule</button>
            <button className="downloadSchedule" onClick={handleCaptureScreenshot}>Save Schedule</button>
          </div>
          <div className="BoxContainer">
            <div className='scheduleIndex'>Showing Schedule {currentScheduleIndex + 1} of {this.props.sendScheduleIn.length}</div>
          
          </div>
          </>
           ) : console.log("not ready")}
        </div>
      );
    }
  }
