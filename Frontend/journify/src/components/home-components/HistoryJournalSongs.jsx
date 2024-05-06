import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';

import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';


import { Navigation, Pagination, FreeMode } from 'swiper/modules';

const HistoryJournalSongs = ({ journal }) => {
    console.log('JOURNAL HERE', journal);
    return (
        <div className='history-journal-songs'>
            <Swiper
                modules={[Navigation,Pagination, FreeMode]}
                navigation={true}
                pagination={{ clickable: true }}
                className="myHistoryJournalSongsSwiper"
                slidesPerView={1}
                spaceBetween={50}
                history={{ key: 'slide', }}
            >
                {journal.questions.map((question) => (
                    <SwiperSlide>
                        <div className="journal-history-song">
                            <img src={question.img} alt={`Song cover for ${question.answer}`}></img>
                            <p>{question.question}</p>
                            <p>{question.answer}</p>
                            <p>{question.emotion}</p>
                        </div>
                    </SwiperSlide>
                ))}


            </Swiper>
        </div>
    );
}
export default HistoryJournalSongs;