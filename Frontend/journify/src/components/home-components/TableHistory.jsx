import React from "react";
import JournalHistoryItem from "./JournalHistoryItem";
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/free-mode';
import 'swiper/css/pagination';

import { Navigation } from 'swiper/modules';

const TableHistory = ({ setIsHistoryModalVisible, history, setCurrentSelectedJournal }) => {
    const mockJournals = [
        {
            "spotify_id": "hcg94v1nqfjz2312ap71hh95t",
            "email": "denismoldovan1@gmail.com",
            "date": {
                "$numberLong": "1714131823"
            },
            "emotion": "not set",
            "questions": [
                {
                    "question": "Receiving a handwritten letter from a friend, I felt like...",
                    "answer": "Bad Habits - Ed Sheeran",
                    "emotion": "Happy",
                    "img": "https://i.scdn.co/image/ab67616d0000b273ef24c3fdbf856340d55cfeb2",
                    "index": 0
                },
                {
                    "question": "Trying to fix a leaky faucet without any plumbing experience, I felt like...",
                    "answer": "not set",
                    "emotion": "not set",
                    "img": "",
                    "index": 1
                },
                {
                    "question": "Trying to navigate a busy airport during the holidays, I felt like...",
                    "answer": "not set",
                    "emotion": "not set",
                    "img": "",
                    "index": 2
                },
                {
                    "question": "Riding a roller coaster for the first time, I felt like...",
                    "answer": "not set",
                    "emotion": "not set",
                    "img": "",
                    "index": 3
                },
                {
                    "question": "Volunteering at a local charity event, I felt like...",
                    "answer": "not set",
                    "emotion": "not set",
                    "img": "",
                    "index": 4
                },
                {
                    "question": "Enjoying a quiet moment alone with a good book, I felt like...",
                    "answer": "not set",
                    "emotion": "not set",
                    "img": "",
                    "index": 5
                },
                {
                    "question": "Helping a stranger carry groceries to their car, I felt like...",
                    "answer": "not set",
                    "emotion": "not set",
                    "img": "",
                    "index": 6
                },
                {
                    "question": "Burning dinner in the oven, I felt like...",
                    "answer": "not set",
                    "emotion": "not set",
                    "img": "",
                    "index": 7
                },
                {
                    "question": "Planting flowers in the garden under the warm sun, I felt like...",
                    "answer": "not set",
                    "emotion": "not set",
                    "img": "",
                    "index": 8
                },
                {
                    "question": "Reuniting with a childhood friend after many years, I felt like...",
                    "answer": "not set",
                    "emotion": "not set",
                    "img": "",
                    "index": 9
                },
                {
                    "question": "Attending a crowded concert in the city, I felt like...",
                    "answer": "not set",
                    "emotion": "not set",
                    "img": "",
                    "index": 10
                },
                {
                    "question": "Battling rush hour traffic during my commute, I felt like...",
                    "answer": "not set",
                    "emotion": "not set",
                    "img": "",
                    "index": 11
                }
            ]
        },

    ]
    // history = mockJournals;
    return (
        <div className="table-history">
            <Swiper
                modules={[Navigation]}
                slidesPerView={7}
                freeMode={true}
                pagination={{ clickable: true }}
                className="mySwiper"
            >

                {history.map((journal) =>
                (
                    <SwiperSlide>
                        <JournalHistoryItem journal={journal} onClick={() => { setCurrentSelectedJournal(journal); setIsHistoryModalVisible(true) }} />
                    </SwiperSlide>)
                )}
            </Swiper>
        </div>

    );
};
export default TableHistory;
