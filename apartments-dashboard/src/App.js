import React, { useState, useEffect } from 'react';
import { ScatterChart, Scatter, CartesianGrid, XAxis, YAxis, Tooltip, Label } from 'recharts';
import './App.css';

function App() {
    const [apartments, setApartments] = useState([]);
    const COLORS = ["#8884d8", "#82ca9d", "#ffc658", "#a4de6c", "#d0ed57"]; // You can add more colors if you expect more unique complexes

    useEffect(() => {
        fetch("http://127.0.0.1:5000/api/apartments")
        .then(res => res.json())
        .then(data => {
            const formattedData = data.map(apartment => ({
                ...apartment,
                x: apartment.size_range.includes('→') ? (parseInt(apartment.size_range.split(' → ')[0]) + parseInt(apartment.size_range.split(' → ')[1])) / 2 : parseInt(apartment.size_range),
                y: apartment.price ? parseFloat(apartment.price.replace('$', '').replace(',', '')) : 0,
            }));
            setApartments(formattedData);
        })
        .catch(err => console.error("Error fetching apartment data:", err));
    }, []);

    const complexNames = Array.from(new Set(apartments.map(data => data.complex_name)));

    const getComplexColor = (complexName) => {
        return COLORS[complexNames.indexOf(complexName) % COLORS.length];
    };

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip">
                    <p className="label">{`Complex Name: ${payload[0].payload.complex_name}`}</p>
                    <p className="desc">{`Price: $${payload[0].payload.y}`}</p>
                    <p className="sqft">{`Sqft: ${payload[0].payload.size_range}`}</p>
                    <p className="units">{`Available Units: ${payload[0].payload.available_units}`}</p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className="App">
            {apartments.length && <div className="legend">
                {complexNames.map(complexName => (
                    <span key={complexName} className="legend-item">
                        <span className="color-box" style={{backgroundColor: getComplexColor(complexName)}}></span>
                        {complexName}
                    </span>
                ))}
            </div>}
            
            {complexNames.map(complexName => {
                const filteredData = apartments.filter(data => data.complex_name === complexName);

                return (
                    <div key={complexName} style={{ marginBottom: 20 }}>
                        <h4 style={{ fontSize: 24 }}>{complexName}</h4>
                        <ScatterChart width={500} height={300}>
                            <CartesianGrid />
                            <XAxis type="number" dataKey="x" name="Square Footage">
                                <Label value="Square Footage" position="bottom" />
                            </XAxis>
                            <YAxis type="number" dataKey="y" name="Price" unit="$">
                                <Label value="Price" angle={-90} position="left" />
                            </YAxis>
                            <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: '3 3' }} />
                            <Scatter data={filteredData} fill={getComplexColor(complexName)} />
                        </ScatterChart>
                    </div>
                );
            })}
        </div>
    );
}

export default App;
