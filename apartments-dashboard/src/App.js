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
                const formattedData = data
                    .map(apartment => ({
                        x: apartment.size_range.includes('→') ? 
                            (parseInt(apartment.size_range.split(' → ')[0]) + parseInt(apartment.size_range.split(' → ')[1])) / 2 : 
                            parseInt(apartment.size_range),
                        y: apartment.price ? parseFloat(apartment.price.replace('$', '').replace(',', '')) : 0,
                        bedrooms: apartment.bedrooms,
                        floorplanName: apartment.floorplan_name,
                        availableUnits: apartment.available_units,
                        sizeRange: apartment.size_range,
                        complex_name: apartment.complex_name // Add the complex_name
                    }))
                    .filter(apartment => apartment.bedrooms === 1); // Filter only 1-bedroom apartments
                
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
            const data = payload[0].payload;
            return (
                <div className="custom-tooltip">
                    <p className="label">{`Complex Name: ${data.complex_name || 'N/A'}`}</p>
                    <p className="desc">{`Price: $${data.y || 'N/A'}`}</p>
                    <p className="sqft">{`Sqft: ${data.sizeRange || 'N/A'}`}</p>
                    <p className="units">{`Available Units: ${data.availableUnits || 'N/A'}`}</p>
                    <p className="floorplan">{`Floor Plan Name: ${data.floorplanName || 'N/A'}`}</p> {/* Added this line */}
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
                        <span className="color-box" style={{ backgroundColor: getComplexColor(complexName) }}></span>
                        {complexName}
                    </span>
                ))}
            </div>}
        
            <div>
                <h3>1 Bedroom</h3>
                <ScatterChart width={500} height={300}>
                    <CartesianGrid />
                    <XAxis 
                        type="number" 
                        dataKey="x" 
                        name="Square Footage" 
                        domain={[Math.min(...apartments.map(ap => ap.x)), Math.max(...apartments.map(ap => ap.x))]}
                    >
                        <Label value="Square Footage" position="bottom" />
                    </XAxis>
                    <YAxis 
                        type="number" 
                        dataKey="y" 
                        name="Price" 
                        unit="$"
                        domain={[Math.min(...apartments.map(ap => ap.y)), Math.max(...apartments.map(ap => ap.y))]}
                    >
                        <Label value="Price" angle={-90} position="left" />
                    </YAxis>
                    <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: '3 3' }} />
                    {complexNames.map(complexName => (
                        <Scatter 
                            key={complexName} 
                            data={apartments.filter(ap => ap.complex_name === complexName)} 
                            fill={getComplexColor(complexName)} 
                            name={complexName} 
                        />
                    ))}
                </ScatterChart>
            </div>
        </div>
    );
}

export default App;