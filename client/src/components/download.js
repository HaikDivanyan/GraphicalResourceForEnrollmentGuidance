import './download.css';
<<<<<<< HEAD
import React, { useEffect, useRef } from 'react';
import html2canvas from 'html2canvas';
import Chart from "chart.js/auto";

export default function Download() {
  
    const chartRef = useRef(null);

=======
import React, { useState } from 'react';
import html2canvas from 'html2canvas';

export default function Download() {
  
>>>>>>> e58ac87 (Download rough with main)
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

<<<<<<< HEAD
  useEffect(() => {
    const gradeDistributions = {
        "('SARRAFZADEH', '21F')": [5, 5, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "('SARRAFZADEH', '22W')": [1, 16, 4, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        "('SARRAFZADEH', '22S')": [4, 14, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        "('SARRAFZADEH', '22F')": [4, 5, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "('SARRAFZADEH', '23S')": [7, 9, 3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    };
        
    
    const categories = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F'];
    
    const datasets = Object.entries(gradeDistributions).map(([key, values]) => ({
        label: key,
        data: values,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
    }));
    
     // Destroy the previous Chart instance if it exists
    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const ctx = document.getElementById('gradeHistogram').getContext('2d');
    
    chartRef.current = new Chart(ctx, {
        type: 'bar',
        data: {
        labels: categories,
        datasets: datasets
        },
        options: {
        scales: {
            x: {
                type: 'category',
                labels: categories
            },
            y: {
                beginAtZero: true,
                stepSize: 1
            }
        }
        }
    });
    }, []);

=======
>>>>>>> e58ac87 (Download rough with main)
  return (
    <div>
      <div className="UploadSection" id="capture">
      <div className="SectionTitle">
          Download
      </div>
        {/* Content to capture */}
        <h1>Hello, this is the content to capture!</h1>
      </div>
      <div className="ButtonContainer">
        <button className="generateButton" onClick={handleCaptureScreenshot}>Download Screenshot</button>
      </div>
<<<<<<< HEAD
      <div className="Canvas">
      <canvas id="gradeHistogram" width="10" height="5"></canvas>
      </div>
=======
>>>>>>> e58ac87 (Download rough with main)
    </div>
  );
}