import React, { useState, useEffect } from 'react';
import { ScatterChart, Scatter, CartesianGrid, XAxis, YAxis, Tooltip, Label } from 'recharts';
import './App.css';

function App() {

    const [apartments, setApartments] = useState([]);

    useEffect(() => {
        fetch("http://127.0.0.1:5000/api/apartments")
            .then(res => res.json())
            .then(data => {
                const formattedData = data.map(apartment => ({
                    x: (parseInt(apartment.size_range.split(' → ')[0]) + parseInt(apartment.size_range.split(' → ')[1])) / 2,
                    y: apartment.price ? parseFloat(apartment.price.replace('$', '').replace(',', '')) : 0,
                    bedrooms: apartment.bedrooms,
                    floorplanName: apartment.floorplan_name,
                    availableUnits: apartment.available_units,
                    sizeRange: apartment.size_range
                }));
                
                setApartments(formattedData);
            })
            
            .catch(err => console.error("Error fetching apartment data:", err));
    }, []);

    const bedroomCounts = Array.from(new Set(apartments.map(data => data.bedrooms)));

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip">
                    <p className="label">{`Floorplan Name: ${payload[0].payload.floorplanName}`}</p>
                    <p className="desc">{`Price: $${payload[0].payload.y}`}</p> {/* Note the change from value to y */}
                    <p className="sqft">{`Sqft: ${payload[0].payload.sizeRange}`}</p>
                    <p className="units">{`Available Units: ${payload[0].payload.availableUnits}`}</p>
                </div>
            );
        }
        return null;
    };
    

    return (
        <div className="App">
            {bedroomCounts.map(bedroom => {
                const filteredData = apartments.filter(data => data.bedrooms === bedroom);

                return (
                    <div key={bedroom} style={{ marginBottom: 20 }}>
                        <h4 style={{ fontSize: 24 }}>{bedroom} Bedroom Apartments</h4>
                        <ScatterChart width={500} height={300}>
                            <CartesianGrid />
                            <XAxis type="number" dataKey="x" name="Square Footage">
                                <Label value="Square Footage" position="bottom" />
                            </XAxis>
                            <YAxis type="number" dataKey="y" name="Price" unit="$">
                                <Label value="Price" angle={-90} position="left" />
                            </YAxis>
                            <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: '3 3' }} />
                            <Scatter data={filteredData} fill="#8884d8" />
                        </ScatterChart>
                    </div>
                );
            })}
        </div>
    );
}

export default App;
