import React, { useEffect, useState, useRef } from 'react';
import { useAuth } from '../../providers/AuthProvider';
import Chart from 'chart.js/auto';
import { fetchPieChartReportFromAPI } from '../../providers/API';

const PieChartLatestJournal = ({cells}) => {
    const { token, userInfo } = useAuth();
    const [report, setReport] = useState(null);
    const chartRef = useRef(null);

    useEffect(() => {
        const fetchReport = async () => {   
            const reportData = await fetchPieChartReportFromAPI(token, userInfo);
            setReport(reportData);
        };

        if (userInfo && token) {
            fetchReport();
        }
    }, [token, userInfo, cells]); 

    useEffect(() => {
        if (report) {
            if (chartRef.current) {
                chartRef.current.destroy();
            }
            const pieChart = document.getElementById('pieChart').getContext('2d');
            chartRef.current = new Chart(pieChart, {
                type: 'pie',
                data: {
                    labels: Object.keys(report),
                    datasets: [{
                        label: 'Latest Journal Report',
                        data: Object.values(report),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.6)',
                            'rgba(54, 162, 235, 0.6)',
                            'rgba(255, 206, 86, 0.6)',
                            'rgba(75, 192, 192, 0.6)',
                            'rgba(153, 102, 255, 0.6)',
                            'rgba(255, 159, 64, 0.6)',
                            'rgba(255, 99, 132, 0.6)'
                        ]
                    }]
                },
                options: {
                    plugins: {
                        title: {
                            display: true,
                            text: 'Latest Journal Report',
                            fontSize: 20
                        },
                        legend: {
                            display: true,
                            position: 'bottom', 
                            labels: {
                                boxWidth: 20, 
                                padding: 20,
                            }
                        }
                    }
                }
            });
        }
    }, [report]);
    

    return (
        <canvas id="pieChart" width="200" height="200"></canvas>
    );
};

export default PieChartLatestJournal;
