import React from 'react';
import { ScatterChart, Scatter, CartesianGrid, XAxis, YAxis, Tooltip, Label } from 'recharts';
import './App.css';

function App() {
    const hardcodedData = [
        { x: 500, y: 1000, bedrooms: 1, floorplanName: "Plan A" },
        { x: 600, y: 1500, bedrooms: 1, floorplanName: "Plan B" },
        { x: 700, y: 1800, bedrooms: 2, floorplanName: "Plan C" },
        { x: 650, y: 1300, bedrooms: 2, floorplanName: "Plan D" },
        { x: 800, y: 2200, bedrooms: 3, floorplanName: "Plan E" },
    ];

    const bedroomCounts = Array.from(new Set(hardcodedData.map(data => data.bedrooms)));

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip">
                    <p className="label">{`Floorplan: ${payload[0].payload.floorplanName}`}</p>
                    <p className="desc">{`Price: $${payload[0].value}`}</p>
                </div>
            );
        }
        return null;
    };

    return (
        <div className="App">
            {bedroomCounts.map(bedroom => {
                const filteredData = hardcodedData.filter(data => data.bedrooms === bedroom);

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
