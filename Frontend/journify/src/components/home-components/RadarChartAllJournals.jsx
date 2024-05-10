import React, { useEffect, useState, useRef } from 'react';
import { useAuth } from '../../providers/AuthProvider';
import Chart from 'chart.js/auto';

const RadarChartAllJournals = ({cells}) => {
    const { token, userInfo } = useAuth();
    const [report, setReport] = useState(null);

    const chartRef = useRef(null);

    useEffect(() => {
        const fetchReport = async () => {   
            const data = await fetch('http://localhost:8888/all_report', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `${token}`
                },
                body: JSON.stringify({
                  email: userInfo.email,
                  spotify_id: userInfo.id
                })
            });
           
            const reportData = await data.json();
            setReport(reportData);
        };

        if (userInfo && token) {
            fetchReport();
        }
    }, [token, userInfo, cells]); 

    useEffect(() => {
        if (report) {
            if (chartRef.current) {
                chartRef.current.destroy(); // Destroy existing chart if it exists
            }
            const radarChart = document.getElementById('radarChart').getContext('2d');
            chartRef.current = new Chart(radarChart, {
                type: 'radar',
                data: {
                    labels: Object.keys(report),
                    datasets: [{
                        label: 'All Journals Report',
                        data: Object.values(report),
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(255, 255, 255, 1)', 
                        borderWidth: 1
                    }]
                },
                options: {
                    plugins: {
                        title: {
                            display: true,
                            text: 'All Journals Report', // Title for the chart
                            fontSize: 20
                        },
                        legend: {
                            display: true,
                            position: 'bottom', // Positioning the legend at the bottom
                            labels: {
                                boxWidth: 20, // Width of each legend box
                                padding: 20, // Padding between legend items
                            }
                        }
                    },
                    elements: {
                        line: {
                            borderColor: 'rgba(255, 255, 255, 1)' 
                        }
                    },
                    scales: {
                        r: {
                            angleLines: {
                                color: 'rgba(255, 255, 255, 1)', 
                            },
                            pointLabels: {
                                display: true, 
                            },
                            ticks: {
                                display: false, 
                            }
                        }
                    }
                }
            });
        }
    }, [report,cells]); 
    

    return (
        <canvas id="radarChart" width="400" height="400"></canvas>
    );
};

export default RadarChartAllJournals;
