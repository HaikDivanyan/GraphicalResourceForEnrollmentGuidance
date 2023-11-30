import React from "react";
import './instruction.css';

export default function Instruction() {

    return (
      <div className="Instruction" id="how-to-use">
            <h1>How does greg work?</h1>
            <div className="Description">
                GREG simplifies class scheduling by analyzing UCLA student's DARS HTML file and 
                using data from sources like the UCLA class schedule and Bruinwalk to 
                provide personalized schedule options.
            </div>
            <div className="Boxes">
                <div className="Box" style={{ backgroundColor: '#005587' }}>
                    <div className="BoxText">
                        Upload DARS
                    </div>
                </div>
                <div className="Box" style={{ backgroundColor: '#8BB8E8' }}>
                    <div className="BoxText">
                        Select Preferences
                    </div>
                </div>
                <div className="Box" style={{ backgroundColor: '#FFB81C' }}>
                    <div className="BoxText">
                        View Options
                    </div>
                </div>
                <div className="Box" style={{ backgroundColor: '#FFD100' }}>
                    <div className="BoxText">
                        Download Perfect Schedule
                    </div>
                </div>
            </div>
      </div>
    );
  }