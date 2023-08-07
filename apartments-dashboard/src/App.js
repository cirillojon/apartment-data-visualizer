import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
    const [apartments, setApartments] = useState([]);

    useEffect(() => {
        fetch("http://127.0.0.1:5000/api/apartments")
            .then(res => res.json())
            .then(data => {
              console.log(data); 
              setApartments(data);
          });
    }, []);

    return (
        <div className="App">
          <div><p>test</p></div>
            {/* Here, display the data as needed. For instance: */}
            {apartments.map(apartment => (
                <div key={apartment.id}>
                    {apartment.floorplan_name} - {apartment.available_units} units available
                </div>
            ))}
        </div>
    );
}

export default App;
